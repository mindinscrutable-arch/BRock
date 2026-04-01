import os
import uuid
import logging
from decimal import Decimal
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.aws.dynamodb import DynamoDBHelper
from app.core.config import settings

logger = logging.getLogger(__name__)

class JobHistoryService:
    """
    High-level service class for persisting "Job History" to DynamoDB.
    While S3 handles the huge artifacts, Dynamo tracks the metadata and execution status for the UI lists.
    """
    
    def __init__(self):
        self.db_helper = DynamoDBHelper()
        self.table_name = settings.DYNAMODB_JOBS_TABLE
        self.enabled = settings.AWS_STORAGE_ENABLED
        
    def create_job(self, source_provider: str, model_id: str, submitted_by: str = "anonymous") -> str:
        """
        Registers a new migration job in DynamoDB, returning the specific Job ID.
        """
        job_id = str(uuid.uuid4())
        
        item = {
            "job_id": job_id,
            "source_provider": source_provider,
            "source_model": model_id,
            "status": "IN_PROGRESS",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "submitted_by": submitted_by
        }
        
        if not self.enabled:
            logger.info(f"[Storage Disabled] Mock created job {job_id} in DynamoDB")
            return job_id
            
        success = self.db_helper.put_item(
            table_name=self.table_name,
            item=item
        )
        
        if not success:
            logger.warning(f"DynamoDB failed to create job {job_id}. Falling back to mock storage.")
            # We don't raise an exception here because we want the demo to survive cloud failures.
            
        return job_id
        
    def complete_job(self, job_id: str, report_s3_key: str, cost_savings_pct: float) -> bool:
        """
        Updates a job row with the completed execution data, pointing it to the final S3 Artifact.
        """
        if not self.enabled:
            logger.info(f"[Storage Disabled] Mock completed job {job_id}")
            return True
        
        try:
            table = self.db_helper.resource.Table(self.table_name)
            table.update_item(
                Key={"job_id": job_id},
                UpdateExpression="set #status_col = :s, report_s3_key = :r, cost_savings_pct = :c, completed_at = :t",
                ExpressionAttributeNames={"#status_col": "status"},
                ExpressionAttributeValues={
                    ":s": "COMPLETED",
                    ":r": report_s3_key,
                    ":c": Decimal(str(cost_savings_pct)),
                    ":t": datetime.now(timezone.utc).isoformat()
                }
            )
            return True
        except Exception as e:
            logger.error(f"Failed to complete job {job_id}: {str(e)}")
            return False
            
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Fetch the tracking state of a specific migration."""
        if not self.enabled:
            return {"job_id": job_id, "status": "MOCK_MODE_ENABLED"}
            
        return self.db_helper.get_item(self.table_name, {"job_id": job_id})
