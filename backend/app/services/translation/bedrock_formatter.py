from typing import Dict, Any, List

class BedrockFormatter:
    """
    Formats normalized prompt components into Amazon Bedrock / Claude compatible payloads.
    """
    
    @staticmethod
    def format_anthropic_messages_api(normalized_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats a normalized prompt specifically for Anthropic Claude 3 models on Bedrock.
        """
        system_instructions = normalized_prompt.get("system", "")
        messages = normalized_prompt.get("messages", [])
        parameters = normalized_prompt.get("parameters", {})
        is_json_mode = normalized_prompt.get("is_json_mode", False)
        
        # Anthropic Claude 3 models expect alternating User/Assistant messages.
        # Ensure the conversation starts with a User message.
        if is_json_mode:
            # Claude 3 doesn't have a strict API flag for JSON mode, we must append it to the prompt.
            json_instruction = "\n\nPlease respond strictly in valid JSON format. Do not include any conversational text before or after the JSON."
            
            # If we don't have a system prompt, add it. If we do, append to it.
            if system_instructions:
                system_instructions += json_instruction
            else:
                system_instructions = json_instruction
        
        # AWS Converse API requires 'content' to be a list of blocks, e.g. [{"text": "string content"}]
        bedrock_messages = []
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                formatted_content = [{"text": content}]
            elif isinstance(content, list):
                # If it's already a list (like OpenAI vision payloads), map text fields properly
                formatted_content = []
                for block in content:
                    if block.get("type") == "text":
                        formatted_content.append({"text": block.get("text", "")})
                    else:
                        formatted_content.append(block) # Pass through other unknown blocks natively
            else:
                formatted_content = [{"text": str(content)}]
                
            bedrock_messages.append({
                "role": msg.get("role", "user"),
                "content": formatted_content
            })

        formatted_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": parameters.get("max_tokens", 1000),
            "temperature": parameters.get("temperature", 0.7),
            "top_p": parameters.get("top_p", 1.0),
            "messages": bedrock_messages
        }
        
        # System is a top level parameter in Claude Messages API
        if system_instructions:
            formatted_payload["system"] = system_instructions
            
        return formatted_payload
