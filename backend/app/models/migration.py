from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class AnalyzeRequest(BaseModel):
    provider: str = Field(..., description="Source provider (e.g., openai, vertex, azure)")
    model: str = Field(..., description="Source model name (e.g., gpt-4)")
    prompt: Dict[str, Any] = Field(..., description="JSON structure of the prompt")

class DetectedFeatures(BaseModel):
    has_system_prompt: bool
    is_json_mode: bool

class SourceInfo(BaseModel):
    provider: str
    model: str
    original_payload: Dict[str, Any]
    detected_features: DetectedFeatures

class TargetInfo(BaseModel):
    provider: str
    model: str
    mapping_reasons: List[str]
    bedrock_payload: Dict[str, Any]

class AnalyzeResponse(BaseModel):
    source: SourceInfo
    target: TargetInfo

class CompareResponse(BaseModel):
    analysis: AnalyzeResponse
    execution: Dict[str, Any]

class TranslateRequest(BaseModel):
    provider: str = Field(default="openai", description="Source provider (e.g., openai)")
    source_model: str = Field(..., description="Source model name")
    source_payload: Dict[str, Any] = Field(..., description="JSON structure of the prompt")

class TranslateResponse(BaseModel):
    target_model: str
    bedrock_payload: Dict[str, Any]

class CompareRequest(BaseModel):
    model: str = Field(..., description="Target model name")
    payload: Dict[str, Any] = Field(..., description="Translated or source payload")
    provider: str = Field(default="openai", description="Source provider")

class ReportRequest(BaseModel):
    source_model: str
    destination_model: str
    metrics: Dict[str, Any] = Field(..., description="The output from the /compare endpoint")
    timestamp: str = Field(default="")

class ReportResponse(BaseModel):
    job_id: str
    report_s3_key: str
    status: str
