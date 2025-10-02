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
    # 
    # FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
    # framework provides templates and structure, but YOU implement the specific
    # business logic for your use case.
    #
    # Why? This ensures maximum flexibility and prevents vendor lock-in.
    # 
    # Next Steps:
    # 1. Review docs/design.md for your specific requirements
    # 2. Implement auth strategy (JWT, OAuth, API keys, etc.)
    # 3. See ~/.agent-os/standards/best-practices.md for patterns
    
    # TODO: Add input validation and sanitization
    # 
    # FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
    # framework provides templates and structure, but YOU implement the specific
    # business logic for your use case.
    #
    # Why? This ensures maximum flexibility and prevents vendor lock-in.
    # 
    # Next Steps:
    # 1. Review docs/design.md for your specific requirements
    # 2. Add Pydantic validators or custom validation logic
    # 3. See ~/.agent-os/standards/best-practices.md for patterns
    
    # Initialize SharedStore
    shared = {
        "request_data": request.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }

    # Execute workflow - let PocketFlow handle retries and errors
    flow = BaselineRAGWorkflowFlow()
    await flow.run_async(shared)

    # TODO: Customize error handling and response codes
    # 
    # FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
    # framework provides templates and structure, but YOU implement the specific
    # business logic for your use case.
    #
    # Why? This ensures maximum flexibility and prevents vendor lock-in.
    # 
    # Next Steps:
    # 1. Review docs/design.md for your specific requirements
    # 2. Follow FastAPI error handling patterns
    # 3. See ~/.agent-os/standards/best-practices.md for patterns
    # Check for flow-level errors
    if "error" in shared:
        raise HTTPException(
            status_code=422,
            detail=shared.get("error_message", "Workflow execution failed")
        )

    # Return response
    return SearchQueryResponse(**shared.get("result", {}))

