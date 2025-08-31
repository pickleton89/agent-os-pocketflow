from fastapi import APIRouter, HTTPException
from .schemas.models import *
from .flow import ContentAnalyzerFlow
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    """
    Analyze content using RAG pattern
    """
    # Initialize SharedStore
    shared = {
        "request_data": request.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }

    # Execute workflow - let PocketFlow handle retries and errors
    flow = ContentAnalyzerFlow()
    await flow.run_async(shared)

    # Check for flow-level errors
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail=shared.get("error_message", "Workflow execution failed")
        )

    # Return response
    return AnalyzeResponse(**shared.get("result", {}))

