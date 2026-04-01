from typing import Dict, Any, Optional
from app.services.mapping.mapping_rules import MODEL_MAPPING_RULES, get_default_bedrock_model

class ModelMapper:
    """
    Responsible for intelligently mapping models from one provider (like OpenAI) to another (Amazon Bedrock).
    """
    
    @staticmethod
    def map_model(source_model_id: str, provider: str = "xai") -> Dict[str, Any]:
        """
        Takes a source model ID (e.g., 'gpt-4o') and returns the best equivalent Bedrock model.
        """
        source_model_id = source_model_id.lower().strip()
        
        # Exact match in our rules dictionary
        if source_model_id in MODEL_MAPPING_RULES:
            return MODEL_MAPPING_RULES[source_model_id]
            
        # Fallback heuristic based on generic naming patterns if exact match fails
        if "grok-2-mini" in source_model_id or "mini" in source_model_id:
             return MODEL_MAPPING_RULES.get("grok-2-mini", MODEL_MAPPING_RULES.get("gemini-1.5-flash"))
             
        if "grok" in source_model_id or "grok-2" in source_model_id:
             return MODEL_MAPPING_RULES.get("grok-2", MODEL_MAPPING_RULES.get("gemini-1.5-pro"))
             
        if "embed" in source_model_id or "text-embedding" in source_model_id:
             return MODEL_MAPPING_RULES["text-embedding-ada-002"]

        if "gemini-1.5-pro" in source_model_id:
             return MODEL_MAPPING_RULES["gemini-1.5-pro"]
             
        # Ultimate fallback
        return {
             "target_model_id": get_default_bedrock_model(),
             "provider": "anthropic",
             "reasons": ["Default mapping applied as the source model was unknown or unsupported."]
        }
