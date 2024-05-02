use super::{
    calculate_inputs, get_model_paths, get_xlora_paths, Loader, ModelInputs, ModelKind, ModelPaths,
    Pipeline, TokenSource, XLoraPaths,
};
use crate::aici::bintokens::build_tok_trie;
use crate::aici::toktree::TokTrie;
use crate::models::Cache;
use crate::pipeline::chat_template::calculate_eos_tokens;
use crate::pipeline::{ChatTemplate, SimpleModelPaths};
use crate::utils::varbuilder_utils::from_mmaped_safetensors;
use crate::xlora_models::NonGranularState;
use crate::{deserialize_chat_template, get_paths, DeviceMapMetadata};
use crate::{
    models::quantized_llama::ModelWeights as QLlama, models::quantized_phi2::ModelWeights as QPhi,
    sequence::Sequence, utils::tokens::get_token, xlora_models::XLoraModelWeights as XLoraQLlama,
};
use anyhow::{bail, Result};
use candle_core::quantized::{gguf_file, GgmlDType};
use candle_core::{DType, Device, Tensor};
use hf_hub::{api::sync::ApiBuilder, Repo, RepoType};
use mistralrs_lora::Ordering;
use serde_json::Value;
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use std::str::FromStr;
use std::sync::Arc;
use std::sync::Mutex;
use tokenizers::Tokenizer;
use tracing::info;

enum Model {
    Llama(QLlama),
    Phi2(QPhi),
    XLoraLlama(XLoraQLlama),
}

pub struct GGUFPipeline {
    model: Model,
    config: GGUFSpecificConfig,
    tokenizer: Arc<Tokenizer>,
    tok_trie: Arc<TokTrie>,
    no_kv_cache: bool,
    chat_template: ChatTemplate,
    model_id: String,
    eos_tok: Vec<u32>,
    non_granular_state: Option<NonGranularState>,
    is_lora: bool,
}

pub struct GGUFLoader {
    model_id: String,
    config: GGUFSpecificConfig,
    quantized_model_id: Option<String>,
    quantized_filename: Option<String>,
    xlora_model_id: Option<String>,
    xlora_order: Option<Ordering>,
    no_kv_cache: bool,
    chat_template: Option<String>,
    tokenizer_json: Option<String>,
    kind: ModelKind,
    tgt_non_granular_index: Option<usize>,
}

#[derive(Debug)]
enum GGUFArchitecture {
    Llama,
    Mpt,
    Gptneox,
    Gptj,
    Gpt2,
    Bloom,
    Falcon,
    Mamba,
    Rwkv,
    Phi2,
}

impl FromStr for GGUFArchitecture {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "llama" => Ok(GGUFArchitecture::Llama),
            "mpt" => Ok(GGUFArchitecture::Mpt),
            "gptneox" => Ok(GGUFArchitecture::Gptneox),
            "gptj" => Ok(GGUFArchitecture::Gptj),
            "gpt2" => Ok(GGUFArchitecture::Gpt2),
            "bloom" => Ok(GGUFArchitecture::Bloom),
            "falcon" => Ok(GGUFArchitecture::Falcon),
            "mamba" => Ok(GGUFArchitecture::Mamba),
            "rwkv" => Ok(GGUFArchitecture::Rwkv),
            "phi2" => Ok(GGUFArchitecture::Phi2),
            a => Err(format!("Unknown GGUF architecture `{a}`")),
        }
    }
}

#[derive(Clone, Copy, Default)]
/// A config for a GGUF loader.
pub struct GGUFSpecificConfig {
    pub repeat_last_n: usize,
}

#[derive(Default)]
/// A builder for a GGUF loader.
pub struct GGUFLoaderBuilder {
    model_id: Option<String>,
    config: GGUFSpecificConfig,
    quantized_model_id: String,
    quantized_filename: String,
    xlora_model_id: Option<String>,
    kind: ModelKind,
    xlora_order: Option<Ordering>,
    no_kv_cache: bool,
    chat_template: Option<String>,
    tokenizer_json: Option<String>,
    tgt_non_granular_index: Option<usize>,
}

impl GGUFLoaderBuilder {
    pub fn new(
        config: GGUFSpecificConfig,
        chat_template: Option<String>,
        tokenizer_json: Option<String>,
        model_id: Option<String>,
        quantized_model_id: String,
        quantized_filename: String,
    ) -> Self {
        Self {
            config,
            chat_template,
            tokenizer_json,
            model_id,
            kind: ModelKind::QuantizedGGUF,
            quantized_filename,
            quantized_model_id,
            ..Default::default()
        }
    }

    fn with_adapter(
        mut self,
        xlora_model_id: String,
        xlora_order: Ordering,
        no_kv_cache: bool,
        tgt_non_granular_index: Option<usize>,
    ) -> Self {
        self.xlora_model_id = Some(xlora_model_id);
        self.xlora_order = Some(xlora_order);
        self.no_kv_cache = no_kv_cache;
        self.tgt_non_granular_index = tgt_non_granular_index;
        self.model_id = if let Some(id) = self.model_id {
            Some(id)
        } else {
            info!(
                "Using adapter base model ID: `{}`",
                self.xlora_order.as_ref().unwrap().base_model_id
            );
            Some(self.xlora_order.as_ref().unwrap().base_model_id.clone())
        };
        self
    }

    pub fn with_xlora(
        mut self,
        xlora_model_id: String,
        xlora_order: Ordering,
        no_kv_cache: bool,
        tgt_non_granular_index: Option<usize>,
    ) -> Self {
        self.kind = ModelKind::XLoraGGUF;
        self.with_adapter(
            xlora_model_id,
            xlora_order,
            no_kv_cache,
            tgt_non_granular_index,
        )
    }

    pub fn with_lora(
        mut self,
        xlora_model_id: String,
        xlora_order: Ordering,
        no_kv_cache: bool,
        tgt_non_granular_index: Option<usize>,
    ) -> Self {
        self.kind = ModelKind::LoraGGUF;
        self.with_adapter(
            xlora_model_id,
            xlora_order,
            no_kv_cache,
            tgt_non_granular_index,
        )
    }

    pub fn build(self) -> Box<dyn Loader> {
        Box::new(GGUFLoader {
            model_id: self.model_id.unwrap(),
            config: self.config,
            xlora_model_id: self.xlora_model_id,
            kind: self.kind,
            xlora_order: self.xlora_order,
            no_kv_cache: self.no_kv_cache,
            chat_template: self.chat_template,
            tokenizer_json: self.tokenizer_json,
            tgt_non_granular_index: self.tgt_non_granular_index,
            quantized_filename: Some(self.quantized_filename),
            quantized_model_id: Some(self.quantized_model_id),
        })
    }
}

impl GGUFLoader {
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        model_id: Option<String>,
        config: GGUFSpecificConfig,
        quantized_model_id: Option<String>,
        quantized_filename: Option<String>,
        xlora_model_id: Option<String>,
        kind: ModelKind,
        xlora_order: Option<Ordering>,
        no_kv_cache: bool,
        chat_template: Option<String>,
        tokenizer_json: Option<String>,
        tgt_non_granular_index: Option<usize>,
    ) -> Self {
        let model_id = if let Some(id) = model_id {
            id
        } else {
            info!(
                "Using adapter base model ID: `{}`",
                xlora_order.as_ref().unwrap().base_model_id
            );
            xlora_order.as_ref().unwrap().base_model_id.clone()
        };
        Self {
            model_id,
            config,
            quantized_model_id,
            quantized_filename,
            xlora_model_id,
            xlora_order,
            no_kv_cache,
            chat_template,
            tokenizer_json,
            kind,
            tgt_non_granular_index,
        }
    }
}

impl Loader for GGUFLoader {
    fn download_model(
        &self,
        revision: Option<String>,
        token_source: TokenSource,
        silent: bool,
    ) -> Result<Box<dyn ModelPaths>> {
        get_paths!(
            SimpleModelPaths,
            &token_source,
            revision,
            self,
            self.quantized_model_id,
            self.quantized_filename,
            silent
        )
    }

    fn _setup_model(
        &self,
        paths: &dyn ModelPaths,
        _dtype: Option<DType>,
        device: &Device,
        silent: bool,
        mapper: DeviceMapMetadata,
        in_situ_quant: Option<GgmlDType>,
    ) -> Result<Arc<Mutex<dyn Pipeline + Send + Sync>>> {
        if in_situ_quant.is_some() {
            anyhow::bail!(
                "You are trying to in-situ quantize a GGUF model. This will not do anything."
            );
        }
        let mut file = std::fs::File::open(paths.get_weight_filenames().first().unwrap())?;
        let model = gguf_file::Content::read(&mut file)
            .map_err(|e| e.with_path(paths.get_weight_filenames().first().unwrap()))?;
        let arch: GGUFArchitecture = model.metadata["general.architecture"]
            .to_string()
            .unwrap()
            .parse()
            .map_err(anyhow::Error::msg)?;

        let mut is_lora = false;
        let model = match self.kind {
            ModelKind::QuantizedGGUF => match arch {
                GGUFArchitecture::Llama => {
                    Model::Llama(QLlama::from_gguf(model, &mut file, device, mapper)?)
                }
                GGUFArchitecture::Phi2 => {
                    Model::Phi2(QPhi::from_gguf(model, &mut file, device, mapper)?)
                }
                a => bail!("Unsupported architecture `{a:?}`"),
            },
            ModelKind::XLoraGGUF => {
                let vb = from_mmaped_safetensors(
                    vec![paths.get_classifier_path().as_ref().unwrap().to_path_buf()],
                    paths
                        .get_adapter_filenames()
                        .as_ref()
                        .unwrap()
                        .iter()
                        .map(|(_, x)| (*x).to_owned())
                        .collect::<Vec<_>>(),
                    DType::F32,
                    device,
                    silent,
                )?;

                match arch {
                    GGUFArchitecture::Llama => Model::XLoraLlama(XLoraQLlama::from_gguf(
                        model,
                        &mut file,
                        device,
                        paths.get_adapter_configs().as_ref().unwrap(),
                        &vb,
                        paths.get_ordering().as_ref().unwrap(),
                        Some(paths.get_classifier_config().as_ref().unwrap().clone()),
                        mapper,
                    )?),
                    a => bail!("Unsupported architecture for GGUF X-LoRA `{a:?}`"),
                }
            }
            ModelKind::LoraGGUF => {
                is_lora = true;
                let vb = from_mmaped_safetensors(
                    vec![],
                    paths
                        .get_adapter_filenames()
                        .as_ref()
                        .unwrap()
                        .iter()
                        .map(|(_, x)| (*x).to_owned())
                        .collect::<Vec<_>>(),
                    DType::F32,
                    device,
                    silent,
                )?;

                match arch {
                    GGUFArchitecture::Llama => Model::XLoraLlama(XLoraQLlama::from_gguf(
                        model,
                        &mut file,
                        device,
                        paths.get_adapter_configs().as_ref().unwrap(),
                        &vb,
                        paths.get_ordering().as_ref().unwrap(),
                        None,
                        mapper,
                    )?),
                    a => bail!("Unsupported architecture for GGUF X-LoRA `{a:?}`"),
                }
            }
            _ => unreachable!(),
        };

        let tokenizer =
            Tokenizer::from_file(paths.get_tokenizer_filename()).map_err(anyhow::Error::msg)?;

        let (chat_template, gen_conf) = deserialize_chat_template!(paths, self);

        Ok(Arc::new(Mutex::new(GGUFPipeline {
            model,
            config: self.config,
            eos_tok: calculate_eos_tokens(&chat_template, gen_conf, &tokenizer),
            tok_trie: build_tok_trie(tokenizer.clone()).into(),
            tokenizer: tokenizer.into(),
            no_kv_cache: self.no_kv_cache,
            chat_template,
            model_id: self.model_id.clone(),
            non_granular_state: self.tgt_non_granular_index.map(|tgt_non_granular_index| {
                NonGranularState {
                    non_granular_index: Arc::new(Mutex::new(0)),
                    tgt_non_granular_index,
                }
            }),
            is_lora,
        })))
    }

    fn get_id(&self) -> &str {
        self.xlora_model_id.as_deref().unwrap_or(&self.model_id)
    }

    fn get_kind(&self) -> ModelKind {
        self.kind
    }
}

impl Pipeline for GGUFPipeline {
    fn forward(
        &mut self,
        input_toks: &[&mut Sequence],
        is_prompt: bool,
    ) -> Result<Tensor, candle_core::Error> {
        let ModelInputs {
            input_ids,
            input_ids_full,
            seqlen_offsets,
            seqlen_offsets_full,
            seqlen_offsets_kernel,
            seqlen_offsets_kernel_full,
            context_lens,
            position_ids: _, // NOTE(EricLBuehler): ignore, it is for phi3
        } = calculate_inputs(
            input_toks,
            is_prompt,
            self.is_xlora(),
            self.device(),
            self.no_kv_cache,
        )
        .unwrap();
        match self.model {
            Model::Llama(ref mut model) => model.forward(
                &input_ids,
                &seqlen_offsets,
                seqlen_offsets_kernel,
                context_lens,
            ),
            Model::Phi2(ref mut model) => model.forward(&input_ids, &seqlen_offsets, context_lens),
            Model::XLoraLlama(ref mut model) => model.forward(
                &input_ids,
                input_ids_full.as_ref().unwrap_or(&input_ids),
                &seqlen_offsets,
                seqlen_offsets_full.as_ref().unwrap_or(&seqlen_offsets),
                seqlen_offsets_kernel.clone(),
                seqlen_offsets_kernel_full.unwrap_or(seqlen_offsets_kernel),
                self.no_kv_cache,
                &self.non_granular_state,
                context_lens,
            ),
        }
    }
    fn device(&self) -> &Device {
        match self.model {
            Model::Llama(ref model) => &model.device,
            Model::Phi2(ref model) => &model.device,
            Model::XLoraLlama(ref model) => &model.device,
        }
    }
    fn num_hidden_layers(&self) -> usize {
        self.cache().lock().len()
    }
    fn cache(&self) -> &Cache {
        match self.model {
            Model::Llama(ref model) => &model.cache,
            Model::Phi2(ref model) => &model.cache,
            Model::XLoraLlama(ref model) => &model.cache,
        }
    }
    fn get_repeat_last_n(&self) -> usize {
        self.config.repeat_last_n
    }
    fn tokenizer(&self) -> Arc<Tokenizer> {
        self.tokenizer.clone()
    }
    fn eos_tok(&self) -> &[u32] {
        &self.eos_tok
    }
    fn name(&self) -> String {
        self.model_id.clone()
    }
    fn get_max_seq_len(&self) -> usize {
        match &self.model {
            Model::Llama(model) => model.max_seq_len,
            Model::Phi2(model) => model.max_seq_len,
            Model::XLoraLlama(model) => model.max_seq_len,
        }
    }
    fn is_xlora(&self) -> bool {
        match &self.model {
            Model::Llama(_) | Model::Phi2(_) => false,
            Model::XLoraLlama(_) => !self.is_lora,
        }
    }
    fn has_no_kv_cache(&self) -> bool {
        self.no_kv_cache
    }
    fn get_chat_template(&self) -> &ChatTemplate {
        &self.chat_template
    }
    fn get_non_granular_state(&self) -> &Option<NonGranularState> {
        &None
    }
    fn tok_trie(&self) -> Arc<TokTrie> {
        self.tok_trie.clone()
    }
    fn re_isq_model(&mut self, _dtype: GgmlDType) -> Result<()> {
        anyhow::bail!(
            "You are trying to in-situ requantize a GGML model. This will not do anything."
        )
    }
}
