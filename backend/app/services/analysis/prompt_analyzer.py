from typing import Dict, Any

from app.services.analysis.provider_detector import ProviderDetector
from app.services.mapping.model_mapper import ModelMapper
from app.services.translation.openai_translator import OpenAITranslator
from app.services.translator import get_target_bedrock_model

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
        
        # 4. Format for NVIDIA (NVIDIA NIMs support native OpenAI schema structure perfectly!)
        # We physically bypass the target-specific wrappers and pass standard dictionaries!
        nvidia_payload = {
            "messages": normalized_prompt.get("messages", [])
        }
        
        target_model = get_target_bedrock_model(source_model)
        
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
                "provider": "nvidia",
                "model": target_model,
                "mapping_reasons": [f"{target_model} chosen as optimized cross-family variant."],
                "bedrock_payload": nvidia_payload
            }
        }
