import os
import uuid
import logging
from typing import Any, Dict
from app.aws.s3 import S3Helper
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    """
    High-level service class for persisting migration records and execution results to S3.
    Accessed by the orchestration or report building layers.
    """
    
    def __init__(self):
        self.s3_helper = S3Helper()
        self.bucket_name = settings.S3_STORAGE_BUCKET
        self.enabled = settings.AWS_STORAGE_ENABLED
        
    def save_comparison_result(self, comparison_data: Dict[str, Any]) -> str:
        """
        Saves the outcome of a Bedrock vs Source comparison to S3.
        Returns the unique identifier (object key) of the generated record.
        """
        record_id = str(uuid.uuid4())
        object_key = f"comparisons/{record_id}.json"
        
        if not self.enabled:
            logger.info(f"[Storage Disabled] Mock saved comparison to {object_key}")
            return record_id
            
        success = self.s3_helper.upload_json(
            bucket_name=self.bucket_name,
            object_key=object_key,
            data=comparison_data
        )
        
        if not success:
            logger.warning("Failed to persist comparison outcome to S3.")
            
        return record_id
        
    def save_migration_report(self, report_data: Dict[str, Any]) -> str:
        """
        Saves the final 'Evaluation Engine' generated report.
        """
        report_id = str(uuid.uuid4())
        object_key = f"reports/{report_id}.json"
        
        if not self.enabled:
            logger.info(f"[Storage Disabled] Mock saved report to {object_key}")
            return report_id
            
        success = self.s3_helper.upload_json(
            bucket_name=self.bucket_name,
            object_key=object_key,
            data=report_data
        )
        
        if not success:
            logger.warning("Failed to persist migration report to S3.")
            
        return report_id
