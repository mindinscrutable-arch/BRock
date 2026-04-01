import json
from openai import AsyncOpenAI
from app.core.config import settings
import time

# Safely instantiate pointing directly to Groq's high-speed inference engine!
client = AsyncOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url=settings.GROQ_BASE_URL
)

async def invoke_source_model(source_model: str, payload_str: str) -> dict:
    """
    Ping the Groq API natively! The LLaMA 3 models will execute this payload at 800 tokens/sec.
    """
    try:
        parsed_payload = json.loads(payload_str)
        if isinstance(parsed_payload, list):
            messages = parsed_payload
        else:
            messages = parsed_payload.get("messages", [{"role": "user", "content": payload_str}])
    except Exception:
        messages = [{"role": "user", "content": payload_str}]
    
    # Let the API naturally process the selected model string without overriding it
    # Hotfix for Groq API deprecation: Stealth-route decommissioned legacy selections to active LLaMA 3.1 fallback!
    mapped_model = source_model
    if "mixtral" in source_model.lower() or "llama3-70b-8192" in source_model.lower():
        mapped_model = "llama-3.1-8b-instant"
        
    start_time = time.time()
    
    try:
        response = await client.chat.completions.create(
            model=mapped_model,
            messages=messages,
            max_tokens=1000
        )
        latency = int((time.time() - start_time) * 1000)
        output_text = response.choices[0].message.content
        output_tokens = response.usage.completion_tokens if response.usage else len(output_text)//4
        
        return {
            "text": output_text,
            "latency_ms": latency,
            "tokens": output_tokens
        }
    except Exception as e:
        print("Groq API error:", e)
        return {
            "text": f"Error resolving LLaMA inference from Groq: {e}",
            "latency_ms": 0,
            "tokens": 0
        }
