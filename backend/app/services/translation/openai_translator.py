from typing import Dict, Any, List

class OpenAITranslator:
    """
    Extracts the core semantic components of an OpenAI formatted prompt.
    """
    
    @staticmethod
    def extract_components(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a raw OpenAI API payload and extracts the system context, user messages, and parameters.
        Returns a normalized structure.
        """
        messages = payload.get("messages", [])
        system_prompt = ""
        user_messages = []
        
        # 1. Separate System messages from other roles (User/Assistant)
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "system":
                # Aggregate system messages if there are multiple (not common but possible)
                system_prompt += content + "\n"
            else:
                user_messages.append({"role": role, "content": content})
                
        # 2. Extract configuration/parameters mapping
        parameters = {
            "temperature": payload.get("temperature", 0.7),
            "max_tokens": payload.get("max_tokens", 1000), # Using 1000 as a sane default if not present
            "top_p": payload.get("top_p", 1.0)
        }
        
        # 3. Detect JSON mode or special requirements
        response_format = payload.get("response_format", {})
        is_json_mode = False
        if isinstance(response_format, dict) and response_format.get("type") == "json_object":
            is_json_mode = True
            
        return {
            "system": system_prompt.strip(),
            "messages": user_messages,
            "parameters": parameters,
            "is_json_mode": is_json_mode
        }
