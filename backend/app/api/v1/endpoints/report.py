from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.migration import ReportRequest, ReportResponse
from app.services.storage.s3_service import StorageService
from app.services.storage.dynamodb_service import JobHistoryService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Finalizes the migration by logging the complete execution payload to Amazon S3
    and writing the summary metadata state into DynamoDB for the frontend table view.
    """
    
    try:
        storage_service = StorageService()
        job_service = JobHistoryService()
        
        # Step 1: Create an IN_PROGRESS tracking job in DynamoDB
        job_id = job_service.create_job(
            source_provider=request.provider,
            model_id=request.model,
            submitted_by="API_USER"
        )
        
        # Step 2: Push the massive execution artifact to S3
        # Because we only need cost_savings dynamically, we pass the execution payload directly
        s3_key = storage_service.save_migration_report(report_data=request.comparison_data)
        
        # Step 3: Mark the job COMPLETED in DynamoDB so the frontend picks it up immediately
        success = job_service.complete_job(
            job_id=job_id,
            report_s3_key=s3_key,
            cost_savings_pct=request.cost_savings_pct
        )
        
        if not success:
            logger.warning(f"S3 uploaded successfully, but failed to finalize DynamoDB job {job_id}")

        return {
            "job_id": job_id,
            "report_s3_key": s3_key,
            "status": "COMPLETED"
        }
        
    except Exception as e:
        logger.error(f"Failed to generate and store report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
