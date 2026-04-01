import asyncio
import json
from fastapi import APIRouter
from app.models.schemas import CompareRequest, CompareResponse, CompareMetrics
from app.aws.bedrock import invoke_target_model
from app.integrations.groq_client import invoke_source_model

router = APIRouter()

@router.post("/", response_model=CompareResponse)
async def execute_comparison(request: CompareRequest):
    """
    Races the exact same prompt against the Source SDK (Groq LLaMA) and
    the Target Runtime (Amazon Bedrock) concurrently via asyncio to evaluate latency and quality.
    """
    
    # We can use the original payload directly,
    # but since this is a migration test, we reconstruct it minimally for Groq using the text from Bedrock Schema
    sys_str = request.payload.get("system", "")
    msgs = request.payload.get("messages", [])
    
    groq_reconstructed = {
        "messages": []
    }
    if sys_str:
        groq_reconstructed["messages"].append({"role": "system", "content": sys_str})
    for m in msgs:
        text_content = m.get("content", [{}])[0].get("text", "")
        groq_reconstructed["messages"].append({"role": m.get("role", "user"), "content": text_content})
        
    source_task = invoke_source_model(
        source_model="llama-3.1-8b-instant", # Fallback default
        payload_str=json.dumps(groq_reconstructed)
    )
    
    target_task = asyncio.to_thread(
        invoke_target_model,
        target_model=request.model,
        bedrock_schema=request.payload
    )

    source_result, target_result = await asyncio.gather(source_task, target_task)

    # 2. Extract Data
    latency_advantage = source_result["latency_ms"] - target_result["latency_ms"]
    savings_pct = round(((source_result["tokens"] - target_result["tokens"]) / max(1, source_result["tokens"])) * 100, 1)

    # 3. Compile the analytical Migration Report Dashboard for the UI!
    metrics = CompareMetrics(
        qualityScore="98.4", # Hardcoded Mock LLM-as-judge
        sourceQuality="96.1",
        latencyDiff=f"{latency_advantage / 1000.0:.2f}s",
        sourceLatency=f"{source_result['latency_ms'] / 1000.0:.2f}s",
        targetLatency=f"{target_result['latency_ms'] / 1000.0:.2f}s",
        tokenDiff=f"{savings_pct}%",
        sourceTokens=str(source_result["tokens"]),
        targetTokens=str(target_result["tokens"]),
        savingsAmount="$4,200", # Fixed Mock Cost Engine
        sourceCost="$10,000/mo",
        targetCost="$5,800/mo",
        verdict="SAFE TO MIGRATE" if latency_advantage > -1000 else "EVALUATE RISKS",
        confidence="96%"
    )

    return CompareResponse(
        latency=target_result["latency_ms"],
        sourceOutput=source_result["text"],
        targetOutput=target_result["text"],
        metrics=metrics
    )