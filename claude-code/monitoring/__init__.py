"""
Performance monitoring and metrics collection for Agent OS + PocketFlow Framework

This module provides comprehensive performance tracking for document creation workflows,
including agent execution times, token usage, parallel execution optimization, and
historical trend analysis.

Key Components:
- DocumentCreationMetrics: Main metrics collection and analysis class
- AgentMetric: Individual agent performance tracking
- OrchestrationMetric: Session-level orchestration performance tracking
"""

from .document_creation_metrics import (
    DocumentCreationMetrics,
    AgentMetric,
    OrchestrationMetric,
)

__all__ = ["DocumentCreationMetrics", "AgentMetric", "OrchestrationMetric"]
__version__ = "1.0.0"
