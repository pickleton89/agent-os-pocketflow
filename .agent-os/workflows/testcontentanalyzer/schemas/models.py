from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime


class SharedStoreModel(BaseModel):
    """Pydantic model for SharedStore validation."""

    input_query: str
    retrieved_docs: List[Dict[str, Any]]
    context: str
    llm_response: str
    analysis_result: Dict[str, Any]
    timestamp: datetime


class AnalyzeContentRequest(BaseModel):
    """Request model for AnalyzeContent endpoint."""

    query: str
    options: Optional[Dict[str, Any]]


class AnalyzeContentResponse(BaseModel):
    """Response model for AnalyzeContent endpoint."""

    analysis: Dict[str, Any]
    confidence: float
    sources: List[str]

