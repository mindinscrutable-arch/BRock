import logging
from typing import Dict, Any, Optional

try:
    from app.aws.boto_session import get_boto_session
    boto3_available = True
except ImportError:
    boto3_available = False

from app.core.config import settings

logger = logging.getLogger(__name__)

class DynamoDBHelper:
    """Helper module to interface with AWS DynamoDB using Boto3"""
    
    def __init__(self):
        self.enabled = getattr(settings, "AWS_STORAGE_ENABLED", False) and boto3_available
        if self.enabled:
            self.session = get_boto_session()
            self.resource = self.session.resource("dynamodb")
        else:
            self.resource = None

    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        if not self.enabled:
            logger.info(f"[MOCK STORAGE] Saved item to DynamoDB Mock: {item.get('job_id', 'unknown')}")
            return True
            
        try:
            table = self.resource.Table(table_name)
            table.put_item(Item=item)
            return True
        except Exception as e:
            logger.error(f"Failed to put item in DynamoDB: {e}")
            return False
            
    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return {"mock": "data", "status": "simulated"}
            
        try:
            table = self.resource.Table(table_name)
            response = table.get_item(Key=key)
            return response.get('Item')
        except Exception as e:
            logger.error(f"Failed to get item from DynamoDB: {e}")
            return None
            
    def update_item_status(self, table_name: str, key: Dict[str, Any], status: str) -> bool:
        """
        Specific helper to quickly update a job's status field.
        """
        try:
            table = self.resource.Table(table_name)
            table.update_item(
                Key=key,
                UpdateExpression="set #status_col = :s",
                ExpressionAttributeNames={"#status_col": "status"},
                ExpressionAttributeValues={":s": status}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update status in DynamoDB ({table_name}): {str(e)}")
            return False
