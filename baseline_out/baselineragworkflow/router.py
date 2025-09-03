from fastapi import APIRouter, HTTPException
from .schemas.models import *
from .flow import BaselineRAGWorkflowFlow
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/search", response_model=SearchQueryResponse)
async def searchquery_endpoint(request: SearchQueryRequest):
    """
    Search knowledge base with query
    """
    # TODO: Add authentication and authorization logic here
    
    # TODO: Add input validation and sanitization
    
    # Initialize SharedStore
    shared = {
        "request_data": request.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }

    # Execute workflow - let PocketFlow handle retries and errors
    flow = BaselineRAGWorkflowFlow()
    await flow.run_async(shared)

    # TODO: Customize error handling and response codes
    # Check for flow-level errors
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail=shared.get("error_message", "Workflow execution failed")
        )

    # Return response
    return SearchQueryResponse(**shared.get("result", {}))

