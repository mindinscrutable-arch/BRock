import json
from typing import Dict, Any, Tuple

def get_target_bedrock_model(source_model: str) -> str:
    """KI Logic: Maps Groq Source models structurally to distinct NVIDIA target equivalence classes (zero same-family overlaps)."""
    mapping = {
        "llama-3.1-8b-instant": "google/gemma-2-9b-it", # Llama -> Gemma
        "llama3-70b-8192": "mistralai/mixtral-8x22b-instruct-v0.1", # Llama -> Mistral
        "mixtral-8x7b-32768": "meta/llama-3.1-70b-instruct" # Mistral -> Llama
    }
    return mapping.get(source_model.lower(), "google/gemma-2-9b-it")


def translate_groq_to_bedrock(source_payload_str: str, source_model: str) -> Tuple[Dict[str, Any], str]:
    """
    Parses a Groq LLaMA payload string and converts
    its architecture to Amazon Bedrock Converse API format explicitly.
    """
    target_model = get_target_bedrock_model(source_model)
    
    # Extract base variables
    try:
        groq_payload = json.loads(source_payload_str)
    except json.JSONDecodeError:
        # If they just pasted raw text instead of JSON, construct a mock payload wrapper
        groq_payload = {
            "messages": [{"role": "user", "content": source_payload_str}]
        }

    # Bedrock Base Schema
    bedrock_schema: Dict[str, Any] = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [],
        "system": "You are a helpful assistant." # Default fallback
    }

    # 1. Map messages array exactly, extracting 'system' out of the sequence
    messages = []
    if "messages" in groq_payload:
        system_rules = []
        for msg in groq_payload["messages"]:
            if msg.get("role") == "system":
                system_rules.append(msg.get("content", ""))
            else:
                messages.append({
                    "role": msg.get("role"),
                    "content": [{"text": msg.get("content", "")}]
                })
        
        bedrock_schema["messages"] = messages
        if system_rules:
            bedrock_schema["system"] = "\n".join(system_rules)

    # 2. Inherit generation parameters if explicitly set
    if groq_payload.get("temperature") is not None:
        bedrock_schema["temperature"] = groq_payload["temperature"]
        
    return bedrock_schema, target_model
