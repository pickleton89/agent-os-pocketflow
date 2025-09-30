#!/usr/bin/env python3
"""
Scoring Engine Module

Scores patterns based on requirement analysis, calculating base scores,
context scores, and suggesting utilities and node counts.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List

from .indicators import PatternType, PatternIndicator
from .requirement_parser import RequirementAnalysis

logger = logging.getLogger(__name__)


@dataclass
class PatternScore:
    """Pattern scoring result."""
    pattern: PatternType
    base_score: float
    context_score: float
    total_score: float
    matched_indicators: List[str] = field(default_factory=list)
    confidence_factors: List[str] = field(default_factory=list)


def score_patterns(
    analysis: RequirementAnalysis,
    pattern_indicators: List[PatternIndicator],
    context_rules: Dict[str, float]
) -> List[PatternScore]:
    """Score all patterns based on requirement analysis."""
    logger.info("Scoring patterns against requirements")

    pattern_scores = []

    for indicator in pattern_indicators:
        # Calculate base score from keyword matches
        base_score = 0.0
        matched_keywords = []

        for keyword in indicator.keywords:
            if any(keyword.lower() in req_keyword.lower() for req_keyword in analysis.extracted_keywords):
                base_score += indicator.weight
                matched_keywords.append(keyword)

            # Also check in raw text for phrase matches
            if keyword.lower() in analysis.raw_text.lower():
                base_score += indicator.weight * 0.5  # Partial credit for text match
                if keyword not in matched_keywords:
                    matched_keywords.append(keyword)

        # Apply context multipliers
        context_score = 0.0
        confidence_factors = []

        for context_key, multiplier in indicator.context_multipliers.items():
            if any(context_key.lower() in keyword.lower() for keyword in analysis.extracted_keywords):
                context_score += base_score * (multiplier - 1.0)
                confidence_factors.append(f"Context: {context_key}")

        # Apply global context rules
        for rule_key, rule_multiplier in context_rules.items():
            if any(rule_key.lower() in keyword.lower() for keyword in analysis.extracted_keywords):
                context_score += base_score * (rule_multiplier - 1.0)
                confidence_factors.append(f"Rule: {rule_key}")

        total_score = base_score + context_score

        pattern_scores.append(PatternScore(
            pattern=indicator.pattern,
            base_score=base_score,
            context_score=context_score,
            total_score=total_score,
            matched_indicators=matched_keywords,
            confidence_factors=confidence_factors
        ))

    # Sort by total score descending
    pattern_scores.sort(key=lambda x: x.total_score, reverse=True)

    return pattern_scores


def estimate_node_count(analysis: RequirementAnalysis) -> int:
    """Estimate the number of nodes needed based on complexity."""
    base_count = 3  # Minimum nodes for any workflow

    # Add nodes based on complexity indicators
    complexity_bonus = len(analysis.complexity_indicators) * 2

    # Add nodes based on functional requirements
    functional_bonus = min(len(analysis.functional_requirements), 5)

    # Add nodes based on integration needs
    integration_bonus = len(analysis.integration_needs)

    return base_count + complexity_bonus + functional_bonus + integration_bonus


def suggest_utilities(pattern: PatternType, analysis: RequirementAnalysis) -> List[str]:
    """Suggest utility functions based on pattern and requirements."""
    utilities = []

    # Pattern-specific utilities
    pattern_utilities = {
        PatternType.RAG: ["vector_search", "document_processor", "embedding_generator"],
        PatternType.AGENT: ["llm_client", "reasoning_engine", "memory_manager"],
        PatternType.TOOL: ["api_client", "data_transformer", "error_handler"],
        PatternType.WORKFLOW: ["flow_controller", "state_manager"],
        PatternType.MAPREDUCE: ["task_distributor", "result_aggregator"],
        PatternType.MULTI_AGENT: ["agent_coordinator", "consensus_manager"],
        PatternType.STRUCTURED_OUTPUT: ["schema_validator", "output_formatter"]
    }

    utilities.extend(pattern_utilities.get(pattern, []))

    # Add utilities based on technical requirements
    if any("api" in req.lower() for req in analysis.technical_requirements):
        utilities.append("api_client")

    if any("database" in req.lower() for req in analysis.technical_requirements):
        utilities.append("database_connector")

    if "performance" in analysis.complexity_indicators:
        utilities.append("performance_monitor")

    # Remove duplicates and limit to reasonable number
    return list(set(utilities))[:8]
