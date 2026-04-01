import time
import asyncio
from typing import Dict, Any

from app.integrations.nvidia_client import call_nvidia
from app.integrations.groq_client import invoke_source_model

class ExecutionOrchestrator:
    """
    Orchestrates execution of the source provider model and the configured target model side-by-side.
    Tracks latency and maps both results to a consistent schema for the downstream evaluation engine.
    """
    
    def __init__(self):
        pass # Cleaned up obsolete clients

    async def run_comparison(
        self, 
        source_provider: str,
        source_model: str,
        source_messages: list,
        bedrock_model: str,
        bedrock_messages: list,
        inference_config: dict = None
    ) -> Dict[str, Any]:
        """
        Run both models concurrently and track their latency.
        """
        inference_config = inference_config or {}

        # 1. Source Task: We dynamically trigger Sahitya's Groq LLaMA pipeline
        try:
            import json
            payload_str = json.dumps(source_messages) 
        except Exception:
            payload_str = str(source_messages)
            
        source_task = invoke_source_model(source_model, payload_str)

        # 2. Target Task: Trigger Native NVIDIA Mapping dynamically over distinct families synchronously 
        target_task = asyncio.to_thread(call_nvidia, bedrock_messages, bedrock_model)

        # 3. Parallel Execution Join
        groq_result, target_result = await asyncio.gather(source_task, target_task)

        # 4. Homogeneous Payload Formatting for the UI Dashboard
        mapped_source_result = {
            "success": groq_result.get("latency_ms", 0) > 0,
            "content": groq_result.get("text", "Groq Execution Failed."),
            "latency_ms": groq_result.get("latency_ms", 0),
            "tokens": groq_result.get("tokens", 1)
        }

        return {
            "source": mapped_source_result,
            "target": {
                "success": target_result["success"], 
                "content": target_result["content"],
                "latency_ms": target_result["latency_ms"],
                "tokens": target_result["tokens"],
                "raw_response": {"model": bedrock_model}
            }
        }



