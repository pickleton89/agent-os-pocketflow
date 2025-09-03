from fastapi import APIRouter, HTTPException
from .schemas.models import *
from .flow import BaselineAGENTWorkflowFlow
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/process", response_model=ProcessTaskResponse)
async def processtask_endpoint(request: ProcessTaskRequest):
    """
    Process task using agent reasoning
    """
    # TODO: Add authentication and authorization logic here
    
    # TODO: Add input validation and sanitization
    
    # Initialize SharedStore
    shared = {
        "request_data": request.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }

    # Execute workflow - let PocketFlow handle retries and errors
    flow = BaselineAGENTWorkflowFlow()
    await flow.run_async(shared)

    # TODO: Customize error handling and response codes
    # Check for flow-level errors
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail=shared.get("error_message", "Workflow execution failed")
        )

    # Return response
    return ProcessTaskResponse(**shared.get("result", {}))

