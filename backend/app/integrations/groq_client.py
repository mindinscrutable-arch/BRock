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
        groq_dict = json.loads(payload_str)
    except Exception:
        groq_dict = {
            "messages": [{"role": "user", "content": payload_str}]
        }
    
    # Safely map to the correct open-source alias!
    mapped_model = "llama-3.1-8b-instant" if "llama" in source_model.lower() else source_model
        
    start_time = time.time()
    
    try:
        response = await client.chat.completions.create(
            model=mapped_model,
            messages=groq_dict.get("messages", [{"role": "user", "content": payload_str}]),
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
