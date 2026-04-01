from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'LLM Migration Factory'
    API_V1_STR: str = '/api/v1'
    
    # AWS Config flags (Kept for mock storage compatibility)
    S3_STORAGE_BUCKET: str | None = None
    DYNAMODB_JOBS_TABLE: str | None = None
    AWS_STORAGE_ENABLED: bool = False
    
    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str | None = None
    NVIDIA_API_KEY: str | None = None
    
    # Newly Merged Sahitya Branch Pydantics
    GROQ_API_KEY: str = "gsk_dummy_plz_replace" # Default fallback prevents hard crashes
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
