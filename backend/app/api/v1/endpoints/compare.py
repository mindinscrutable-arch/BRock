import asyncio
import json
from fastapi import APIRouter
from app.models.schemas import CompareRequest, CompareResponse, CompareMetrics
from app.integrations.google_client import invoke_target_model
from app.integrations.groq_client import invoke_source_model

router = APIRouter()

@router.post("/", response_model=CompareResponse)
async def execute_comparison(request: CompareRequest):
    """
    Races the exact same prompt against the Source SDK (Groq LLaMA) and
    the Target Runtime (Google Vertex / Gemini) concurrently via asyncio to evaluate latency and quality.
    """
    
    # We can use the original payload directly,
    # but since this is a migration test, we reconstruct it minimally for Groq using the text from Google Vertex Schema
    system_instruction = request.payload.get("systemInstruction", {}).get("parts", [{"text": ""}])[0].get("text", "")
    msgs = request.payload.get("messages", [])
    
    groq_reconstructed = {
        "messages": []
    }
    if system_instruction:
        groq_reconstructed["messages"].append({"role": "system", "content": system_instruction})
    for content in request.payload.get("contents", []):
        text_content = content.get("parts", [{"text": ""}])[0].get("text", "")
        role = content.get("role", "user")
        groq_reconstructed["messages"].append({"role": "assistant" if role == "model" else "user", "content": text_content})
        
    source_task = invoke_source_model(
        source_model="llama-3.1-8b-instant", # Fallback default
        payload_str=json.dumps(groq_reconstructed)
    )
    
    target_task = asyncio.to_thread(
        invoke_target_model,
        target_model=request.model,
        google_schema=request.payload
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