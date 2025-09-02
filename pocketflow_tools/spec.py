from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class WorkflowSpec:
    """Specification for generating a PocketFlow workflow.

    Note: This mirrors the legacy spec definition used by the monolithic
    generator to ensure parity during the refactor.
    """

    name: str
    pattern: str  # AGENT/WORKFLOW/RAG/MAPREDUCE/MULTI-AGENT/STRUCTURED-OUTPUT
    description: str
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    utilities: List[Dict[str, Any]] = field(default_factory=list)
    shared_store_schema: Dict[str, Any] = field(default_factory=dict)
    api_endpoints: List[Dict[str, Any]] = field(default_factory=list)
    fast_api_integration: bool = True

