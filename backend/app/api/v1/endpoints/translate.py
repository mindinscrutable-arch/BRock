from fastapi import APIRouter
from app.models.migration import TranslateRequest, TranslateResponse
from app.services.analysis.prompt_analyzer import PromptAnalyzer

router = APIRouter()

@router.post("/", response_model=TranslateResponse)
async def translate_prompt(request: TranslateRequest):
    """
    Translates an OpenAI/Vertex prompt directly into the optimal Claude 3 Bedrock format.
    Does not execute the models or compare latency.
    """
    
    # Let the analysis engine figure out the optimal parameters and translation
    analysis = PromptAnalyzer.analyze_and_translate(
        payload=request.source_payload,
        source_model=request.source_model
    )
    
    # Extract only the necessary bits for the translation response
    return {
        "target_model": analysis["target"]["model"],
        "bedrock_payload": analysis["target"]["bedrock_payload"]
    }
