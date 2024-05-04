use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use anyhow::{Context, Result};
use internal_baml_core::ir::ClientWalker;
use internal_baml_jinja::{ChatMessagePart, RenderContext_Client, RenderedChatMessage};

use serde_json::json;

use crate::internal::llm_client::{
    expression_helper::to_value,
    state::LlmClientState,
    traits::{WithChat, WithClient, WithNoCompletion, WithRetryPolicy},
    LLMResponse, ModelFeatures,
};

use crate::RuntimeContext;

fn resolve_properties(
    client: &ClientWalker,
    ctx: &RuntimeContext,
) -> Result<PostRequestProperities> {
    let mut properties = (&client.item.elem.options)
        .iter()
        .map(|(k, v)| {
            Ok((
                k.into(),
                to_value(ctx, v).context(format!(
                    "client {} could not resolve options.{}",
                    client.name(),
                    k
                ))?,
            ))
        })
        .collect::<Result<HashMap<_, _>>>()?;

    let default_role = properties
        .remove("default_role")
        .and_then(|v| v.as_str().map(|s| s.to_string()))
        .unwrap_or_else(|| "system".to_string());

    let base_url = properties
        .remove("base_url")
        .and_then(|v| v.as_str().map(|s| s.to_string()))
        .unwrap_or_else(|| "https://api.openai.com/v1".to_string());

    let api_key = properties
        .remove("api_key")
        .and_then(|v| v.as_str().map(|s| s.to_string()))
        .or_else(|| ctx.env.get("OPENAI_API_KEY").map(|s| s.to_string()));

    let headers = properties.remove("headers").map(|v| {
        if let Some(v) = v.as_object() {
            v.iter()
                .map(|(k, v)| {
                    Ok((
                        k.to_string(),
                        match v {
                            serde_json::Value::String(s) => s.to_string(),
                            _ => anyhow::bail!("Header '{k}' must be a string"),
                        },
                    ))
                })
                .collect::<Result<HashMap<String, String>>>()
        } else {
            Ok(Default::default())
        }
    });
    let headers = match headers {
        Some(h) => h?,
        None => Default::default(),
    };

    Ok(PostRequestProperities {
        default_role,
        base_url,
        api_key,
        headers,
        properties,
    })
}
struct PostRequestProperities {
    default_role: String,
    base_url: String,
    api_key: Option<String>,
    headers: HashMap<String, String>,

    // These are passed directly to the OpenAI API.
    properties: HashMap<String, serde_json::Value>,
}

pub struct OpenAIClient {
    // client: ClientWalker<'ir>,
    retry_policy: Option<String>,
    context: RenderContext_Client,
    features: ModelFeatures,
    properties: PostRequestProperities,

    internal_state: Arc<Mutex<LlmClientState>>,
}

impl WithRetryPolicy for OpenAIClient {
    fn retry_policy_name(&self) -> Option<&str> {
        self.retry_policy.as_deref()
    }
}

impl WithClient for OpenAIClient {
    fn context(&self) -> &RenderContext_Client {
        &self.context
    }

    fn model_features(&self) -> &ModelFeatures {
        &self.features
    }
}

impl WithNoCompletion for OpenAIClient {}

impl WithChat for OpenAIClient {
    fn chat_options(&self, _ctx: &RuntimeContext) -> Result<internal_baml_jinja::ChatOptions> {
        Ok(internal_baml_jinja::ChatOptions::new(
            self.properties.default_role.clone(),
            None,
        ))
    }

    #[cfg(not(feature = "network"))]
    async fn chat(
        &self,
        _ctx: &RuntimeContext,
        _prompt: &Vec<RenderedChatMessage>,
    ) -> Result<LLMResponse> {
        Err(anyhow::anyhow!("Network feature is not enabled"))
    }

    #[cfg(feature = "network")]
    async fn chat(
        &self,
        ctx: &RuntimeContext,
        prompt: &Vec<RenderedChatMessage>,
    ) -> Result<LLMResponse> {
        use crate::internal::llm_client::{
            openai::types::{ChatCompletionResponse, FinishReason, OpenAIErrorResponse},
            ErrorCode, LLMCompleteResponse, LLMErrorResponse,
        };

        let req = self.build_http_request(ctx, "/chat/completions", prompt)?;

        match self.internal_state.clone().lock() {
            Ok(mut state) => {
                state.call_count += 1;
            }
            Err(e) => {
                log::warn!("Failed to increment call count for OpenAIClient: {:#?}", e);
            }
        }
        let now = std::time::SystemTime::now();
        let res = req.send().await?;

        let status = res.status();

        // Raise for status.
        if !status.is_success() {
            let err_code = ErrorCode::from_status(status);

            let err_message = match res.json::<serde_json::Value>().await {
                Ok(body) => match serde_json::from_value::<OpenAIErrorResponse>(body) {
                    Ok(err) => format!("API Error ({}): {}", err.error.r#type, err.error.message),
                    Err(e) => format!("Does this support the OpenAI Response type?\n{:#?}", e),
                },
                Err(e) => {
                    format!("Does this support the OpenAI Response type?\n{:#?}", e)
                }
            };

            return Ok(LLMResponse::LLMFailure(LLMErrorResponse {
                client: self.context.name.to_string(),
                model: None,
                prompt: internal_baml_jinja::RenderedPrompt::Chat(prompt.clone()),
                start_time_unix_ms: now
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_millis() as u64,
                latency_ms: now.elapsed().unwrap().as_millis() as u64,
                message: err_message,
                code: err_code,
            }));
        }

        let body = match res.json::<ChatCompletionResponse>().await {
            Ok(body) => body,
            Err(e) => {
                return Ok(LLMResponse::LLMFailure(LLMErrorResponse {
                    client: self.context.name.to_string(),
                    model: None,
                    prompt: internal_baml_jinja::RenderedPrompt::Chat(prompt.clone()),
                    start_time_unix_ms: now
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap()
                        .as_millis() as u64,
                    latency_ms: now.elapsed().unwrap().as_millis() as u64,
                    message: format!("Does this support the OpenAI Response type?\n{:#?}", e),
                    code: ErrorCode::UnsupportedResponse(status.as_u16()),
                }));
            }
        };

        if body.choices.len() < 1 {
            return Ok(LLMResponse::LLMFailure(LLMErrorResponse {
                client: self.context.name.to_string(),
                model: None,
                prompt: internal_baml_jinja::RenderedPrompt::Chat(prompt.clone()),
                start_time_unix_ms: now
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_millis() as u64,
                latency_ms: now.elapsed().unwrap().as_millis() as u64,
                message: format!("No content in response:\n{:#?}", body),
                code: ErrorCode::Other(status.as_u16()),
            }));
        }

        let usage = body.usage.as_ref();

        Ok(LLMResponse::Success(LLMCompleteResponse {
            client: self.context.name.to_string(),
            prompt: internal_baml_jinja::RenderedPrompt::Chat(prompt.clone()),
            content: body.choices[0]
                .message
                .content
                .as_ref()
                .map_or("", |s| s.as_str())
                .to_string(),
            start_time_unix_ms: now
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_millis() as u64,
            latency_ms: now.elapsed().unwrap().as_millis() as u64,
            model: body.model,
            metadata: json!({
                "baml_is_complete": match body.choices[0].finish_reason {
                    None => true,
                    Some(FinishReason::Stop) => true,
                    _ => false,
                },
                "finish_reason": body.choices[0].finish_reason,
                "prompt_tokens": usage.map(|u| u.prompt_tokens),
                "output_tokens": usage.map(|u| u.completion_tokens),
                "total_tokens": usage.map(|u| u.total_tokens),
            }),
        }))
    }
}

impl OpenAIClient {
    pub fn new(client: &ClientWalker, ctx: &RuntimeContext) -> Result<OpenAIClient> {
        Ok(Self {
            properties: resolve_properties(client, ctx)?,
            context: RenderContext_Client {
                name: client.name().into(),
                provider: client.elem().provider.clone(),
            },
            features: ModelFeatures {
                chat: true,
                completion: false,
            },
            retry_policy: client
                .elem()
                .retry_policy_id
                .as_ref()
                .map(|s| s.to_string()),
            internal_state: Arc::new(Mutex::new(LlmClientState::new())),
        })
    }

    #[cfg(feature = "network")]
    fn build_http_request(
        &self,
        ctx: &RuntimeContext,
        path: &str,
        prompt: &Vec<RenderedChatMessage>,
    ) -> Result<reqwest::RequestBuilder> {
        // TODO: ideally like to keep this alive longer.
        let client = reqwest::Client::new();

        let mut body = json!(self.properties.properties);
        body.as_object_mut().unwrap().insert(
            "messages".into(),
            prompt
                .iter()
                .map(|m| {
                    json!({
                        "role": m.role,
                        "content": convert_message_parts_to_content(&m.parts)
                    })
                })
                .collect::<serde_json::Value>(),
        );

        log::info!("Request body: {:#?}", body);

        let mut req = client
            .post(format!("{}{}", self.properties.base_url, path))
            .json(&body);
        match self.properties.api_key {
            Some(ref key) => {
                req = req.header("Authorization", format!("Bearer {}", key));
            }
            None => {}
        }
        for (k, v) in &self.properties.headers {
            req = req.header(k, v);
        }

        // Add all the properties as data parameters.
        Ok(req)
    }
}

fn convert_message_parts_to_content(parts: &Vec<ChatMessagePart>) -> serde_json::Value {
    let content: Vec<serde_json::Value> = parts
        .into_iter()
        .map(|part| match part {
            ChatMessagePart::Text(text) => json!({"type": "text", "text": text}),
            ChatMessagePart::Image(image) => match image {
                internal_baml_jinja::BamlImage::Url(image) => {
                    json!({"type": "image_url", "image_url": json!({
                        "url": image.url
                    })})
                }
                internal_baml_jinja::BamlImage::Base64(image) => {
                    json!({"type": "image_url", "image_url": json!({
                        "base64": image.base64
                    })})
                }
            },
        })
        .collect();

    // This is for non-image apis, where there is no "type", and the content is returned as a string instead of the list of parts.
    if content.len() == 1 && content[0].get("type").unwrap() == "text" {
        return serde_json::Value::String(content[0].get("text").unwrap().to_string());
    }

    json!(content)
}
