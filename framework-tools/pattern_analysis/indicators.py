#!/usr/bin/env python3
"""
Pattern Indicators Module

Defines pattern indicators with keywords and context multipliers
for PocketFlow pattern detection.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum


class PatternType(Enum):
    """Supported PocketFlow pattern types."""
    RAG = "RAG"
    AGENT = "AGENT"
    TOOL = "TOOL"
    WORKFLOW = "WORKFLOW"
    MAPREDUCE = "MAPREDUCE"
    MULTI_AGENT = "MULTI-AGENT"
    STRUCTURED_OUTPUT = "STRUCTURED-OUTPUT"
    HYBRID = "HYBRID"


@dataclass
class PatternIndicator:
    """Individual pattern indicator with scoring."""
    pattern: PatternType
    keywords: List[str]
    weight: float
    context_multipliers: Dict[str, float] = field(default_factory=dict)


def load_pattern_indicators() -> List[PatternIndicator]:
    """Load pattern indicator definitions with enhanced non-LLM pattern support."""
    return [
        # RAG Pattern Indicators
        PatternIndicator(
            pattern=PatternType.RAG,
            keywords=[
                "search", "knowledge base", "documentation", "retrieval", "query",
                "semantic", "vector", "embedding", "similarity", "document",
                "index", "content", "find", "lookup", "information"
            ],
            weight=1.0,
            context_multipliers={
                "database": 1.2,
                "text": 1.1,
                "question": 1.3,
                "answer": 1.3
            }
        ),

        # Agent Pattern Indicators
        PatternIndicator(
            pattern=PatternType.AGENT,
            keywords=[
                "decision", "planning", "reasoning", "autonomous", "intelligent",
                "adaptive", "llm", "ai", "model", "conversation", "chat",
                "think", "analyze", "determine", "choose", "conclude"
            ],
            weight=1.0,
            context_multipliers={
                "complex": 1.2,
                "multi-step": 1.3,
                "workflow": 1.1,
                "conditional": 1.2
            }
        ),

        # Tool Pattern Indicators - Enhanced for traditional web/API apps
        PatternIndicator(
            pattern=PatternType.TOOL,
            keywords=[
                "integration", "api", "external service", "automation", "connection",
                "interface", "system", "service", "endpoint", "webhook",
                "connector", "plugin", "bridge", "sync", "import", "export",
                # Traditional web app indicators
                "rest", "graphql", "http", "web service", "microservice",
                "database", "sql", "crud", "backend", "frontend", "client",
                "authentication", "authorization", "session", "middleware"
            ],
            weight=1.2,  # Higher weight for common web patterns
            context_multipliers={
                "third-party": 1.3,
                "external": 1.2,
                "integrate": 1.2,
                "connect": 1.1,
                # Web app multipliers
                "web": 1.4,
                "api": 1.3,
                "rest": 1.3,
                "service": 1.2,
                "database": 1.2,
                "auth": 1.1
            }
        ),

        # Workflow Pattern Indicators - Enhanced for traditional business apps
        PatternIndicator(
            pattern=PatternType.WORKFLOW,
            keywords=[
                "process", "flow", "sequence", "step", "pipeline", "chain",
                "orchestration", "coordination", "execution", "batch",
                "serial", "sequential", "ordered", "stages",
                # Traditional business process indicators
                "crud", "form", "submit", "create", "read", "update", "delete",
                "user", "dashboard", "admin", "management", "tracking",
                "simple", "basic", "straightforward", "standard"
            ],
            weight=1.1,  # Slightly higher for common patterns
            context_multipliers={
                "business": 1.2,
                "approval": 1.3,
                "review": 1.2,
                "multi-step": 1.1,
                # Business app multipliers
                "crud": 1.4,
                "form": 1.3,
                "user": 1.2,
                "admin": 1.2,
                "simple": 1.3,
                "basic": 1.3
            }
        ),

        # MapReduce Pattern Indicators
        PatternIndicator(
            pattern=PatternType.MAPREDUCE,
            keywords=[
                "parallel", "distribute", "scale", "concurrent", "batch",
                "aggregate", "reduce", "map", "partition", "chunk",
                "divide", "split", "merge", "combine", "bulk",
                # Data processing indicators
                "etl", "data processing", "transform", "load", "extract",
                "analytics", "reporting", "large dataset", "big data"
            ],
            weight=1.0,
            context_multipliers={
                "large": 1.3,
                "volume": 1.2,
                "performance": 1.2,
                "scalability": 1.3,
                "data": 1.2,
                "analytics": 1.3,
                "etl": 1.4
            }
        ),

        # Multi-Agent Pattern Indicators
        PatternIndicator(
            pattern=PatternType.MULTI_AGENT,
            keywords=[
                "multi-agent", "collaborative", "coordination", "specialist",
                "expert", "team", "role", "delegate", "distribute",
                "consensus", "voting", "committee", "panel", "group"
            ],
            weight=1.0,
            context_multipliers={
                "complex": 1.3,
                "specialized": 1.2,
                "expert": 1.2,
                "collaborative": 1.1
            }
        ),

        # Structured Output Pattern Indicators - Enhanced for APIs
        PatternIndicator(
            pattern=PatternType.STRUCTURED_OUTPUT,
            keywords=[
                "structured", "format", "schema", "json", "xml", "csv",
                "template", "form", "validation", "constraint", "field",
                "data model", "specification", "standard", "compliance",
                # API response indicators
                "response", "payload", "output", "format", "serialize",
                "model", "pydantic", "schema validation", "type checking"
            ],
            weight=1.0,
            context_multipliers={
                "validation": 1.3,
                "compliance": 1.2,
                "format": 1.2,
                "standard": 1.1,
                "api": 1.2,
                "json": 1.2,
                "schema": 1.3
            }
        )
    ]


def load_context_rules() -> Dict[str, float]:
    """Load context-specific scoring rules."""
    return {
        # Complexity indicators
        "simple": 0.8,
        "basic": 0.8,
        "complex": 1.3,
        "advanced": 1.2,
        "enterprise": 1.4,

        # Scale indicators
        "small": 0.9,
        "large": 1.2,
        "massive": 1.4,
        "scale": 1.2,

        # Performance indicators
        "fast": 1.1,
        "performance": 1.2,
        "realtime": 1.3,
        "batch": 1.1,

        # Integration indicators
        "integrate": 1.2,
        "external": 1.2,
        "third-party": 1.3,
        "api": 1.1
    }
