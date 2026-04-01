from typing import Dict, Any, Optional

class ProviderDetector:
    """
    Detects the source AI provider based on the payload structure or explicit configuration.
    """
    

    @staticmethod
    def detect_from_model_name(model_name: str) -> str:
        """
        Attempts to detect the provider based on the model string.
        """
        model_name = model_name.lower()
        if "gpt-" in model_name or "o1-" in model_name:
            return "openai"
        elif "gemini-" in model_name or "text-bison" in model_name:
            return "vertex"
        elif "claude-" in model_name:
            return "anthropic"
        elif "llama" in model_name:
            return "meta"
        
        return "unknown"

