from fastapi import APIRouter
from app.models.migration import CompareRequest, CompareResponse
from app.services.analysis.prompt_analyzer import PromptAnalyzer
from app.services.execution.orchestrator import ExecutionOrchestrator

router = APIRouter()

@router.post("/", response_model=CompareResponse)
async def compare_models(request: CompareRequest):

    # Step 1: Analyze + Translate
    analysis = PromptAnalyzer.analyze_and_translate(
        payload=request.payload,
        source_model=request.model
    )

    # Step 2: Extract formatted payloads to match strict Orchestrator requirements
    source_messages = request.payload.get("messages", [])
    bedrock_messages = analysis["target"]["bedrock_payload"].get("messages", [])

    # Step 3: Execute both models concurrently
    orchestrator = ExecutionOrchestrator()
    execution_result = await orchestrator.run_comparison(
        source_provider=request.provider,
        source_model=request.model,
        source_messages=source_messages,
        bedrock_model=analysis["target"]["model"],
        bedrock_messages=bedrock_messages,
        inference_config={"temperature": 0.7, "max_tokens": 1000}
    )

    # Step 4: Return combined result
    return {
        "analysis": analysis,
        "execution": execution_result
    }