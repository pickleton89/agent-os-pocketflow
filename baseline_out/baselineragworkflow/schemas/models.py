from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime


class SharedStoreModel(BaseModel):
    """Pydantic model for SharedStore validation."""

    query: str
    documents: List[Dict[str, Any]]
    embeddings: List[List[float]]
    search_results: List[Dict[str, Any]]
    context: str
    response: str


class SearchQueryRequest(BaseModel):
    """Request model for SearchQuery endpoint."""

    query: str
    limit: Optional[int]


class SearchQueryResponse(BaseModel):
    """Response model for SearchQuery endpoint."""

    results: List[Dict[str, Any]]
    count: int

