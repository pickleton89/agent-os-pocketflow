from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime


class SharedStoreModel(BaseModel):
    """Pydantic model for SharedStore validation."""

    task: str
    context: Optional[str]
    reasoning_steps: List[str]
    action_plan: List[Dict[str, str]]
    actions_taken: List[str]
    result: str
    memory: Dict[str, Any]


class ProcessTaskRequest(BaseModel):
    """Request model for ProcessTask endpoint."""

    task: str
    context: Optional[str]


class ProcessTaskResponse(BaseModel):
    """Response model for ProcessTask endpoint."""

    result: str
    actions_taken: List[str]

