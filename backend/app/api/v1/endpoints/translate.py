from fastapi import APIRouter
from app.models.schemas import TranslateRequest, TranslateResponse
from app.services.translator import translate_groq_to_bedrock

router = APIRouter()

@router.post("/", response_model=TranslateResponse)
async def translate_prompt(request: TranslateRequest):
    """
    Receives an OpenAI JSON payload and completely translates the
    architecture format to an Amazon Bedrock Converse API format explicitly via 'KI'.
    """
    bedrock_schema, mapped_model = translate_groq_to_bedrock(
        source_payload_str=request.source_payload,
        source_model=request.source_model
    )
    
    return TranslateResponse(
        converted_schema=bedrock_schema,
        target_model=mapped_model
    )
