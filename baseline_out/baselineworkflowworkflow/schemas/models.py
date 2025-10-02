from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime


class SharedStoreModel(BaseModel):
    """Pydantic model for SharedStore validation."""

    input_data: Dict[str, Any]
    validation_result: Dict[str, Any]
    processed_data: Dict[str, Any]
    output_data: Dict[str, Any]


class ProcessWorkflowRequest(BaseModel):
    """Request model for ProcessWorkflow endpoint."""

    input_data: Dict[str, Any]


class ProcessWorkflowResponse(BaseModel):
    """Response model for ProcessWorkflow endpoint."""

    output_data: Dict[str, Any]
    status: str

