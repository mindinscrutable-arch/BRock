from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# --- TRANSLATION ENDPOINT SCHEMAS ---

class TranslateRequest(BaseModel):
    source_payload: str
    source_model: str = Field(..., description="E.g., gpt-4o, gpt-4-turbo")

class TranslateResponse(BaseModel):
    converted_schema: Dict[str, Any]
    target_model: str

# --- COMPARE ENDPOINT SCHEMAS ---

class CompareRequest(BaseModel):
    payload: Dict[str, Any]
    model: str = Field(..., description="The Amazon Bedrock target model ID")

class CompareMetrics(BaseModel):
    qualityScore: str
    sourceQuality: str
    latencyDiff: str
    sourceLatency: str
    targetLatency: str
    tokenDiff: str
    sourceTokens: str
    targetTokens: str
    savingsAmount: str
    sourceCost: str
    targetCost: str
    verdict: str
    confidence: str

class CompareResponse(BaseModel):
    latency: int
    sourceOutput: str
    targetOutput: str
    metrics: CompareMetrics

# --- DYNAMODB REPORTING SCHEMAS ---

class SaveReportRequest(BaseModel):
    source_model: str
    destination_model: str
    metrics: Dict[str, Any]
    timestamp: str
