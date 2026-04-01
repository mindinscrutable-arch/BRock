import json
import logging
from typing import Any, Dict, Optional

try:
    from app.aws.boto_session import get_boto_client
    boto3_available = True
except ImportError:
    boto3_available = False

from app.core.config import settings

logger = logging.getLogger(__name__)

class S3Helper:
    """Helper module to interface with AWS S3 using Boto3"""
    
    def __init__(self):
        self.enabled = getattr(settings, "AWS_STORAGE_ENABLED", False) and boto3_available
        if self.enabled:
            self.client = get_boto_client("s3")
        else:
            self.client = None
            
    def upload_json(self, bucket_name: str, object_key: str, data: Dict[str, Any]) -> bool:
        if not self.enabled:
            logger.info(f"[MOCK STORAGE] Saved {object_key} to S3 Mock")
            return True
            
        try:
            json_data = json.dumps(data, indent=2)
            self.client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=json_data,
                ContentType="application/json"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to upload JSON to S3: {e}")
            return False
            
    def download_json(self, bucket_name: str, object_key: str) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return {"mock": "data", "status": "simulated"}
            
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to download JSON from S3: {e}")
            return None
