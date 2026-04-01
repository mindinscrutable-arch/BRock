from typing import Dict, Any, List

# Core mapping rules from source providers to Amazon Bedrock models
MODEL_MAPPING_RULES: Dict[str, Dict[str, Any]] = {
    # OpenAI to Bedrock Mappings
    "gpt-4": {
        "target_model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "provider": "anthropic",
        "reasons": ["Comparable reasoning capabilities", "Better cost-efficiency", "Equivalent or better context window"],
    },
    "gpt-4o": {
        "target_model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "provider": "anthropic",
        "reasons": ["Similar speed and high intelligence", "Native multimodal support (if needed)"],
    },
    "gpt-4-turbo": {
        "target_model_id": "anthropic.claude-3-opus-20240229-v1:0",
        "provider": "anthropic",
        "reasons": ["High complexity task handling equivalent"],
    },
    "gpt-3.5-turbo": {
        "target_model_id": "anthropic.claude-3-haiku-20240307-v1:0", # or amazon.titan-text-express-v1
        "provider": "anthropic",
        "reasons": ["High speed, low cost equivalent", "Excellent for standard text tasks"],
    },
    "text-embedding-ada-002": {
        "target_model_id": "amazon.titan-embed-text-v1",
        "provider": "amazon",
        "reasons": ["Standard equivalent embedding model on Bedrock"],
    },
    "text-embedding-3-small": {
         "target_model_id": "amazon.titan-embed-text-v2:0",
         "provider": "amazon",
         "reasons": ["Latest generation efficient embeddings"],
    },
    
    # Vertex / Google to Bedrock Mappings
    "gemini-1.5-pro": {
        "target_model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "provider": "anthropic",
        "reasons": ["Long-context reasoning match"],
    },
    "gemini-1.5-flash": {
        "target_model_id": "anthropic.claude-3-haiku-20240307-v1:0",
        "provider": "anthropic",
        "reasons": ["Speed and cost optimized equivalent"],
    }
}

def get_default_bedrock_model() -> str:
    """Returns a safe default model if mapping fails."""
    return "anthropic.claude-3-haiku-20240307-v1:0"
