from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime


class SharedStoreModel(BaseModel):
    """Pydantic model for SharedStore validation."""

    request_data: Dict[str, Any]
    auth_token: Optional[str]
    external_response: Dict[str, Any]
    transformed_data: Dict[str, Any]
    response_data: Dict[str, Any]


class ExecuteToolRequest(BaseModel):
    """Request model for ExecuteTool endpoint."""

    operation: str
    parameters: Dict[str, Any]


class ExecuteToolResponse(BaseModel):
    """Response model for ExecuteTool endpoint."""

    status: str
    data: Dict[str, Any]

