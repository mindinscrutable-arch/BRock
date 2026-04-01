import boto3
from botocore.config import Config
from app.core.config import settings

def get_boto_session() -> boto3.Session:
    """
    Creates and returns a configured Boto3 session.
    It uses the AWS_PROFILE and AWS_REGION from settings if provided.
    """
    kwargs = {}
    if getattr(settings, "AWS_PROFILE", None):
        kwargs["profile_name"] = settings.AWS_PROFILE
    if getattr(settings, "AWS_REGION", None):
        kwargs["region_name"] = settings.AWS_REGION
    if hasattr(settings, "AWS_ACCESS_KEY_ID") and settings.AWS_ACCESS_KEY_ID:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
    if hasattr(settings, "AWS_SECRET_ACCESS_KEY") and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

    return boto3.Session(**kwargs)

def get_boto_client(service_name: str, **kwargs) -> boto3.client:
    """
    Returns a Boto3 client for the specified service name.
    """
    session = get_boto_session()
    
    # Configure retry behavior
    boto_config = Config(
        retries=dict(
            max_attempts=3
        )
    )
    
    return session.client(
        service_name=service_name,
        config=boto_config,
        **kwargs
    )
