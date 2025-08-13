from fastapi import APIRouter, HTTPException
from .schemas.models import *
from .flow import TestContentAnalyzerFlow
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=AnalyzeContentResponse)
async def analyzecontent_endpoint(request: AnalyzeContentRequest):
    """
    Analyze content using RAG pattern
    """
    try:
        # Initialize SharedStore
        shared = {
            "request_data": request.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Execute workflow
        flow = TestContentAnalyzerFlow()
        await flow.run_async(shared)
        
        # Check for errors
        if "error" in shared:
            raise HTTPException(
                status_code=422,
                detail=shared.get("error_message", "Workflow execution failed")
            )
        
        # Return response
        return AnalyzeContentResponse(**shared.get("result", {}))
    except Exception as e:
        logger.error(f"Error in AnalyzeContent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

