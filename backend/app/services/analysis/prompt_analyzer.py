from typing import Dict, Any

from app.services.analysis.provider_detector import ProviderDetector
from app.services.mapping.model_mapper import ModelMapper
from app.services.translation.openai_translator import OpenAITranslator
from app.services.translation.bedrock_formatter import BedrockFormatter

class PromptAnalyzer:
    """
    Central brain for orchestrating the analysis, mapping, and translation of LLM prompts.
    """
    
    @staticmethod
    def analyze_and_translate(payload: Dict[str, Any], source_model: str) -> Dict[str, Any]:
        """
        Orchestrates the entire translation pipeline:
        1. Detects provider.
        2. Normalizes prompt payload.
        3. Maps the source model to the optimal Bedrock model.
        4. Formats the normalized prompt for the target Bedrock model.
        """
        # 1. Detect Provider based on the user-supplied source model
        provider = ProviderDetector.detect_from_model_name(source_model)
            
        # 2. Extract and Normalize Prompt Elements
        normalized_prompt = {}
        if provider == "openai":
            normalized_prompt = OpenAITranslator.extract_components(payload)
        # TODO: Add VertexTranslator, AzureTranslator, etc.
        else:
            # Fallback for unknown payloads, assume OpenAI-like for now as it's the most common
            normalized_prompt = OpenAITranslator.extract_components(payload)
            
        # 3. Map Model to Bedrock target
        mapped_model_info = ModelMapper.map_model(source_model, provider)
        
        # 4. Format for Bedrock (Assuming Anthropic Claude on Bedrock is the target for now)
        bedrock_payload = BedrockFormatter.format_anthropic_messages_api(normalized_prompt)
        
        return {
            "source": {
                "provider": provider,
                "model": source_model,
                "original_payload": payload,
                "detected_features": {
                    "has_system_prompt": bool(normalized_prompt.get("system")),
                    "is_json_mode": normalized_prompt.get("is_json_mode", False)
                }
            },
            "target": {
                "provider": mapped_model_info.get("provider", "anthropic"),
                "model": mapped_model_info.get("target_model_id"),
                "mapping_reasons": mapped_model_info.get("reasons", []),
                "bedrock_payload": bedrock_payload
            }
        }
