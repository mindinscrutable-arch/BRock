import json
from typing import Dict, Any, Tuple

def get_target_google_model(source_model: str) -> str:
    """KI Logic: Maps OpenAI/Groq models to their closest Google Gemini equivalent."""
    mapping = {
        "gpt-4o": "gemini-2.5-flash",
        "llama3-70b-8192": "gemini-2.5-flash", 
    }
    return mapping.get(source_model.lower(), "gemini-2.5-flash")


def translate_groq_to_google(source_payload_str: str, source_model: str) -> Tuple[Dict[str, Any], str]:
    """
    Parses a Groq LLaMA payload string and converts
    its architecture to Google Gemini AI API format explicitly.
    """
    target_model = get_target_google_model(source_model)
    
    # Extract base variables
    try:
        groq_payload = json.loads(source_payload_str)
    except json.JSONDecodeError:
        # If they just pasted raw text instead of JSON, construct a mock payload wrapper
        groq_payload = {
            "messages": [{"role": "user", "content": source_payload_str}]
        }

    # Google Gemini Base Schema
    google_schema: Dict[str, Any] = {
        "contents": [],
    }

    # 1. Map messages array to Gemini contents structure
    contents = []
    if "messages" in groq_payload:
        system_rules = []
        for msg in groq_payload["messages"]:
            if msg.get("role") == "system":
                system_rules.append(msg.get("content", ""))
            else:
                contents.append({
                    "role": msg.get("role") if msg.get("role") != "assistant" else "model",
                    "parts": [{"text": msg.get("content", "")}]
                })
        
        google_schema["contents"] = contents
        if system_rules:
            # Add Gemini specific System Instructions natively
            google_schema["systemInstruction"] = {
                "parts": [{"text": "\n".join(system_rules)}]
            }

    # 2. Inherit generation parameters mapping natively to Gemini GenerationConfig
    gen_config = {}
    if groq_payload.get("temperature") is not None:
        gen_config["temperature"] = groq_payload["temperature"]
    if gen_config:
        google_schema["generationConfig"] = gen_config
        
    return google_schema, target_model
