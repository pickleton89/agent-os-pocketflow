#!/usr/bin/env python3
"""
Centralized Pattern Definitions for PocketFlow

Single source of truth for pattern node templates (names, descriptions, node types).

This module is framework-owned and imported by both:
- generator.PocketFlowGenerator (to build node specs)
- workflow_graph_generator.WorkflowGraphGenerator (to render graphs)

Notes:
- Canonical keys use the enum `PatternType` from `pattern_analyzer`.
- Auxiliary/simple patterns that aren’t part of the enum remain string-keyed.
- Functions return deep copies to prevent accidental mutation of canonical data.
"""

from typing import Dict, List, Any, Union
import copy

# Support relative and absolute imports to allow both package and script usage
try:  # pragma: no cover - import convenience
    from .pattern_analyzer import PatternType  # type: ignore
except Exception:  # pragma: no cover - standalone fallback
    from pattern_analyzer import PatternType  # type: ignore


# Canonical node templates for enum-based patterns
CORE_PATTERN_NODE_TEMPLATES: Dict[PatternType, List[Dict[str, str]]] = {
    PatternType.RAG: [
        {
            "name": "DocumentLoader",
            "description": "Load and preprocess documents for retrieval",
            "type": "Node",
        },
        {
            "name": "EmbeddingGenerator",
            "description": "Generate embeddings for document chunks",
            "type": "AsyncNode",
        },
        {
            "name": "QueryProcessor",
            "description": "Process and enhance user queries",
            "type": "Node",
        },
        {
            "name": "Retriever",
            "description": "Retrieve relevant documents based on query",
            "type": "AsyncNode",
        },
        {
            "name": "ContextFormatter",
            "description": "Format retrieved documents for generation",
            "type": "Node",
        },
        {
            "name": "LLMGenerator",
            "description": "Generate response using LLM with context",
            "type": "AsyncNode",
        },
    ],
    PatternType.AGENT: [
        {
            "name": "TaskAnalyzer",
            "description": "Analyze and understand the given task",
            "type": "Node",
        },
        {
            "name": "PlanningEngine",
            "description": "Create execution plan for the task",
            "type": "AsyncNode",
        },
        {
            "name": "ReasoningNode",
            "description": "Apply reasoning to make decisions",
            "type": "AsyncNode",
        },
        {
            "name": "ActionExecutor",
            "description": "Execute planned actions",
            "type": "AsyncNode",
        },
        {
            "name": "ResultEvaluator",
            "description": "Evaluate and validate results",
            "type": "Node",
        },
    ],
    PatternType.TOOL: [
        {
            "name": "InputValidator",
            "description": "Validate and sanitize input data",
            "type": "Node",
        },
        {
            "name": "AuthHandler",
            "description": "Handle authentication for external services",
            "type": "AsyncNode",
        },
        {
            "name": "APIClient",
            "description": "Make requests to external APIs",
            "type": "AsyncNode",
        },
        {
            "name": "DataTransformer",
            "description": "Transform data between formats",
            "type": "Node",
        },
        {
            "name": "ResponseProcessor",
            "description": "Process and format API responses",
            "type": "Node",
        },
    ],
    PatternType.WORKFLOW: [
        {
            "name": "InputProcessor",
            "description": "Process and validate workflow input",
            "type": "Node",
        },
        {
            "name": "BusinessLogic",
            "description": "Execute core business logic",
            "type": "Node",
        },
        {
            "name": "DataProcessor",
            "description": "Process and transform data",
            "type": "Node",
        },
        {
            "name": "OutputFormatter",
            "description": "Format and prepare output",
            "type": "Node",
        },
    ],
    PatternType.MAPREDUCE: [
        {
            "name": "TaskDistributor",
            "description": "Distribute tasks across workers",
            "type": "BatchNode",
        },
        {
            "name": "MapProcessor",
            "description": "Process individual data chunks",
            "type": "AsyncBatchNode",
        },
        {
            "name": "IntermediateAggregator",
            "description": "Aggregate intermediate results",
            "type": "BatchNode",
        },
        {
            "name": "ReduceProcessor",
            "description": "Reduce results to final output",
            "type": "AsyncBatchNode",
        },
        {
            "name": "ResultCollector",
            "description": "Collect and format final results",
            "type": "Node",
        },
    ],
    PatternType.MULTI_AGENT: [
        {
            "name": "TaskCoordinator",
            "description": "Coordinate tasks among multiple agents",
            "type": "Node",
        },
        {
            "name": "SpecialistAgent",
            "description": "Execute specialized tasks",
            "type": "AsyncNode",
        },
        {
            "name": "ConsensusManager",
            "description": "Manage consensus between agents",
            "type": "Node",
        },
        {
            "name": "ResultIntegrator",
            "description": "Integrate results from multiple agents",
            "type": "Node",
        },
    ],
    PatternType.STRUCTURED_OUTPUT: [
        {
            "name": "SchemaValidator",
            "description": "Validate input against schema",
            "type": "Node",
        },
        {
            "name": "DataProcessor",
            "description": "Process data according to schema",
            "type": "Node",
        },
        {
            "name": "OutputStructurer",
            "description": "Structure output according to schema",
            "type": "Node",
        },
        {
            "name": "FormatValidator",
            "description": "Validate final output format",
            "type": "Node",
        },
    ],
}


# Auxiliary simple patterns used only by the generator (not enum-based)
SIMPLE_PATTERN_NODE_TEMPLATES: Dict[str, List[Dict[str, str]]] = {
    "SIMPLE_WORKFLOW": [
        {
            "name": "InputProcessor",
            "description": "Process and validate input data",
            "type": "Node",
        },
        {
            "name": "BusinessLogic",
            "description": "Execute core business operations",
            "type": "Node",
        },
        {
            "name": "OutputFormatter",
            "description": "Format and prepare output data",
            "type": "Node",
        },
    ],
    "BASIC_API": [
        {
            "name": "RequestValidator",
            "description": "Validate API request data",
            "type": "Node",
        },
        {
            "name": "DataProcessor",
            "description": "Process business logic",
            "type": "Node",
        },
        {
            "name": "ResponseBuilder",
            "description": "Build API response",
            "type": "Node",
        },
    ],
    "SIMPLE_ETL": [
        {
            "name": "DataExtractor",
            "description": "Extract data from source",
            "type": "Node",
        },
        {
            "name": "DataTransformer",
            "description": "Transform data according to business rules",
            "type": "Node",
        },
        {
            "name": "DataLoader",
            "description": "Load data to destination",
            "type": "Node",
        },
    ],
}


def _deepcopy_nodes(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return a deep copy of node templates to avoid mutation of canonical data."""
    return copy.deepcopy(nodes)


def get_node_templates(pattern: Union[str, PatternType]) -> List[Dict[str, Any]]:
    """Fetch node templates for a given pattern (enum or string).

    - If a `PatternType` is provided, returns the canonical set.
    - If a string is provided, tries to parse it as a `PatternType` by value;
      if not found, falls back to auxiliary simple patterns; otherwise returns
      the WORKFLOW canonical set.
    - Always returns a deep copy to prevent callers from mutating globals.
    """
    # Enum path
    if isinstance(pattern, PatternType):
        templates = CORE_PATTERN_NODE_TEMPLATES.get(pattern)
        if templates:
            return _deepcopy_nodes(templates)
        # Fallback to WORKFLOW if somehow missing
        return _deepcopy_nodes(CORE_PATTERN_NODE_TEMPLATES[PatternType.WORKFLOW])

    # String path: try to convert to enum by value first
    try:
        enum_pattern = PatternType(pattern)
        return _deepcopy_nodes(CORE_PATTERN_NODE_TEMPLATES[enum_pattern])
    except Exception:
        pass

    # Then check auxiliary/simple patterns
    if pattern in SIMPLE_PATTERN_NODE_TEMPLATES:
        return _deepcopy_nodes(SIMPLE_PATTERN_NODE_TEMPLATES[pattern])

    # Final fallback to WORKFLOW canonical set
    return _deepcopy_nodes(CORE_PATTERN_NODE_TEMPLATES[PatternType.WORKFLOW])


__all__ = [
    "PatternType",
    "CORE_PATTERN_NODE_TEMPLATES",
    "SIMPLE_PATTERN_NODE_TEMPLATES",
    "get_node_templates",
    "compose_hybrid_node_templates",
]


def compose_hybrid_node_templates(
    base_patterns: List[Union[str, PatternType]],
) -> List[Dict[str, Any]]:
    """Compose hybrid node templates from multiple base patterns.

    - Accepts a list of `PatternType` or string values convertible to `PatternType`.
    - Fetches canonical node templates for each base pattern.
    - Unions nodes by `name`, preserving first occurrence order across patterns.
    - Returns a deep copy to avoid mutating canonical definitions.
    """
    seen = set()
    result: List[Dict[str, Any]] = []

    for p in base_patterns:
        try:
            nodes = get_node_templates(p)
        except Exception:
            # Skip invalid patterns rather than failing composition
            nodes = []
        for node in nodes:
            name = node.get("name")
            if not name:
                continue
            if name in seen:
                continue
            result.append(copy.deepcopy(node))
            seen.add(name)

    return result
