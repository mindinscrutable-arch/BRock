from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'LLM Migration Factory'
    API_V1_STR: str = '/api/v1'
    
    # AWS Settings
    AWS_REGION: str = 'us-east-1'
    AWS_PROFILE: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_STORAGE_ENABLED: bool = False
    DYNAMODB_JOBS_TABLE: str = 'MigrationJobs'
    S3_STORAGE_BUCKET: str | None = None
    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str | None = None
    NVIDIA_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    GROQ_BASE_URL: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
