from fastapi import APIRouter
from app.models.schemas import TranslateRequest, TranslateResponse
from app.services.translator import translate_groq_to_google

router = APIRouter()

@router.post("/", response_model=TranslateResponse)
async def translate_prompt(request: TranslateRequest):
    """
    Receives a valid LLM JSON payload and completely translates the
    architecture format to an explicitly mapped Google Gemini API format via Engine logic.
    """
    google_schema, mapped_model = translate_groq_to_google(
        source_payload_str=request.source_payload,
        source_model=request.source_model
    )
    
    return TranslateResponse(
        converted_schema=google_schema,
        target_model=mapped_model
    )
