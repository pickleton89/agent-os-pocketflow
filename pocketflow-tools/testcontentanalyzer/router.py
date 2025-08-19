from fastapi import APIRouter, HTTPException
from .schemas.models import AnalyzeContentRequest, AnalyzeContentResponse
from .flow import TestContentAnalyzerFlow
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeContentResponse)
async def analyzecontent_endpoint(request: AnalyzeContentRequest):
    """
    Analyze content using RAG pattern
    """
    # Initialize SharedStore
    shared = {
        "request_data": request.dict(),
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Execute workflow - let PocketFlow handle retries and errors
    flow = TestContentAnalyzerFlow()
    await flow.run_async(shared)

    # Check for flow-level errors
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail=shared.get("error_message", "Workflow execution failed"),
        )

    # Return response with properly structured data
    result = shared.get("result", {})
    return AnalyzeContentResponse(
        analysis=result.get("analysis", shared.get("analysis_result", {})),
        confidence=result.get("confidence", 0.0),
        sources=result.get("sources", []),
    )
