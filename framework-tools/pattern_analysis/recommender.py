#!/usr/bin/env python3
"""
Recommender Module

Generates pattern recommendations with detailed justifications,
template customizations, and workflow suggestions.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List

from .indicators import PatternType
from .requirement_parser import RequirementAnalysis
from .scoring_engine import PatternScore, estimate_node_count, suggest_utilities
from .pattern_matcher import assess_complexity, get_graduated_complexity_mapping

logger = logging.getLogger(__name__)


@dataclass
class PatternRecommendation:
    """Complete pattern recommendation."""

    primary_pattern: PatternType
    confidence_score: float
    secondary_patterns: List[PatternType] = field(default_factory=list)
    rationale: str = ""
    detailed_justification: str = ""
    template_customizations: Dict[str, Any] = field(default_factory=dict)
    workflow_suggestions: Dict[str, Any] = field(default_factory=dict)


def generate_detailed_justification(
    pattern_scores: List[PatternScore], analysis: RequirementAnalysis
) -> str:
    """Generate detailed justification for pattern selection."""

    if not pattern_scores:
        return "No pattern indicators found in the requirements. Using default workflow pattern."

    primary_score = pattern_scores[0]

    justification_parts = []

    # Primary pattern justification
    justification_parts.append(
        f"**Primary Pattern Selection: {primary_score.pattern.value}**"
    )
    justification_parts.append(
        f"Selected with confidence score of {primary_score.total_score:.2f}"
    )
    justification_parts.append("")

    # Detailed indicator analysis
    justification_parts.append("**Key Indicators Found:**")
    for indicator in primary_score.matched_indicators[:5]:  # Top 5
        justification_parts.append(
            f"- '{indicator}' - Strong indicator for {primary_score.pattern.value} pattern"
        )
    justification_parts.append("")

    # Context factors
    if primary_score.confidence_factors:
        justification_parts.append("**Supporting Context:**")
        for factor in primary_score.confidence_factors[:3]:  # Top 3
            justification_parts.append(f"- {factor}")
        justification_parts.append("")

    # Alternative patterns considered
    if len(pattern_scores) > 1:
        justification_parts.append("**Alternative Patterns Considered:**")
        for alt_score in pattern_scores[1:4]:  # Top 3 alternatives
            if alt_score.total_score > 0:
                justification_parts.append(
                    f"- {alt_score.pattern.value}: Score {alt_score.total_score:.2f} "
                    f"(Indicators: {', '.join(alt_score.matched_indicators[:2])})"
                )
        justification_parts.append("")

    # Requirements complexity assessment
    complexity_assessment = assess_complexity(analysis)
    justification_parts.append(f"**Complexity Assessment:** {complexity_assessment}")
    justification_parts.append("")

    # Technical requirements alignment
    if analysis.technical_requirements:
        justification_parts.append("**Technical Requirements Alignment:**")
        for tech_req in analysis.technical_requirements[:3]:
            justification_parts.append(
                f"- {tech_req} - Compatible with {primary_score.pattern.value} pattern"
            )
        justification_parts.append("")

    # Pattern-specific recommendations
    pattern_recs = get_pattern_specific_recommendations(primary_score.pattern, analysis)
    if pattern_recs:
        justification_parts.append("**Pattern-Specific Recommendations:**")
        for rec in pattern_recs:
            justification_parts.append(f"- {rec}")
        justification_parts.append("")

    return "\n".join(justification_parts)


def get_pattern_specific_recommendations(
    pattern: PatternType, analysis: RequirementAnalysis
) -> List[str]:
    """Get pattern-specific implementation recommendations."""

    recommendations = []

    if pattern == PatternType.RAG:
        recommendations.extend(
            [
                "Consider using chromadb or pinecone for vector storage",
                "Implement chunking strategy for large documents",
                "Add semantic similarity scoring for retrieved content",
            ]
        )
        if "real-time" in analysis.raw_text.lower():
            recommendations.append("Implement caching for frequently queried content")

    elif pattern == PatternType.AGENT:
        recommendations.extend(
            [
                "Implement structured reasoning with chain-of-thought prompting",
                "Add memory management for context persistence",
                "Consider tool integration for external actions",
            ]
        )
        if "planning" in analysis.raw_text.lower():
            recommendations.append("Implement multi-step planning with backtracking")

    elif pattern == PatternType.TOOL:
        recommendations.extend(
            [
                "Implement robust error handling for external API failures",
                "Add rate limiting and retry mechanisms",
                "Consider webhook integration for async operations",
            ]
        )
        if len(analysis.integration_needs) > 2:
            recommendations.append("Consider implementing circuit breaker pattern")

    elif pattern == PatternType.WORKFLOW:
        recommendations.extend(
            [
                "Add workflow state persistence for long-running processes",
                "Implement checkpoint and resume functionality",
                "Consider adding approval gates for critical steps",
            ]
        )

    return recommendations


def generate_template_customizations(
    pattern: PatternType, analysis: RequirementAnalysis
) -> Dict[str, Any]:
    """Generate template customization suggestions based on pattern and requirements."""
    customizations = {}

    # Pattern-specific customizations
    if pattern == PatternType.RAG:
        customizations.update(
            {
                "vector_database": "chromadb"
                if "chroma" in analysis.raw_text.lower()
                else "default",
                "embedding_model": "sentence-transformers"
                if "embedding" in analysis.raw_text.lower()
                else "default",
                "retrieval_strategy": "semantic"
                if "semantic" in analysis.raw_text.lower()
                else "keyword",
                "chunk_size": 1000,
                "similarity_threshold": 0.7,
            }
        )

    elif pattern == PatternType.AGENT:
        customizations.update(
            {
                "llm_provider": "openai"
                if "openai" in analysis.raw_text.lower()
                else "anthropic",
                "reasoning_type": "chain-of-thought"
                if "reasoning" in analysis.raw_text.lower()
                else "direct",
                "memory_enabled": "conversation" in analysis.raw_text.lower(),
                "tool_calling": len(analysis.integration_needs) > 0,
            }
        )

    elif pattern == PatternType.TOOL:
        customizations.update(
            {
                "integration_type": "rest"
                if "rest" in analysis.raw_text.lower()
                else "webhook",
                "authentication": "oauth"
                if "oauth" in analysis.raw_text.lower()
                else "api_key",
                "rate_limiting": "performance" in analysis.complexity_indicators,
                "error_handling": "retry"
                if "reliable" in analysis.raw_text.lower()
                else "fail_fast",
            }
        )

    # Add common customizations based on complexity
    if "enterprise" in analysis.complexity_indicators:
        customizations["logging_level"] = "detailed"
        customizations["monitoring"] = "enabled"
        customizations["caching"] = "redis"

    return customizations


def generate_workflow_suggestions(
    pattern: PatternType, analysis: RequirementAnalysis
) -> Dict[str, Any]:
    """Generate workflow structure suggestions."""
    suggestions = {
        "estimated_nodes": estimate_node_count(analysis),
        "suggested_utilities": suggest_utilities(pattern, analysis),
        "error_handling": "comprehensive"
        if "enterprise" in analysis.complexity_indicators
        else "basic",
        "async_processing": any(
            async_indicator in analysis.raw_text.lower()
            for async_indicator in [
                "async",
                "concurrent",
                "parallel",
                "api",
                "external",
            ]
        ),
    }

    # Pattern-specific suggestions
    if pattern == PatternType.RAG:
        suggestions.update(
            {
                "preprocessing_nodes": ["document_loader", "chunker", "embedder"],
                "retrieval_nodes": ["query_processor", "retriever", "ranker"],
                "generation_nodes": ["context_formatter", "llm_generator"],
            }
        )

    elif pattern == PatternType.AGENT:
        suggestions.update(
            {
                "planning_nodes": ["task_analyzer", "planner"],
                "execution_nodes": ["reasoning_engine", "action_executor"],
                "reflection_nodes": ["result_evaluator", "memory_updater"],
            }
        )

    elif pattern == PatternType.TOOL:
        suggestions.update(
            {
                "integration_nodes": [
                    "auth_handler",
                    "api_client",
                    "response_processor",
                ],
                "transformation_nodes": ["input_formatter", "output_parser"],
                "validation_nodes": ["request_validator", "response_validator"],
            }
        )

    return suggestions


def generate_recommendation(
    pattern_scores: List[PatternScore],
    analysis: RequirementAnalysis,
    detect_combinations_func,
) -> PatternRecommendation:
    """Generate final pattern recommendation from scores."""
    logger.info("Generating pattern recommendation")

    if not pattern_scores:
        return PatternRecommendation(
            primary_pattern=PatternType.WORKFLOW,
            confidence_score=0.5,
            rationale="No clear pattern indicators found. Defaulting to basic WORKFLOW pattern.",
        )

    # Get primary pattern (highest score)
    primary_score = pattern_scores[0]
    primary_pattern = primary_score.pattern

    # Calculate confidence based on score separation and absolute score
    max_possible_score = len(analysis.extracted_keywords) * 2.0  # Rough estimate
    confidence_score = (
        min(primary_score.total_score / max_possible_score, 1.0)
        if max_possible_score > 0
        else 0.5
    )

    # Boost confidence if there's a clear winner
    if len(pattern_scores) > 1:
        score_separation = primary_score.total_score - pattern_scores[1].total_score
        if score_separation > 2.0:
            confidence_score = min(confidence_score * 1.2, 1.0)

    # Determine secondary patterns (scores within 70% of primary)
    threshold = primary_score.total_score * 0.7
    secondary_patterns = [
        score.pattern
        for score in pattern_scores[1:6]  # Top 5 alternatives
        if score.total_score >= threshold and score.total_score > 0
    ]

    # Generate detailed rationale
    detailed_rationale = generate_detailed_justification(pattern_scores, analysis)

    # Also generate a brief rationale for backward compatibility
    rationale_parts = [
        f"Primary pattern {primary_pattern.value} selected based on {len(primary_score.matched_indicators)} matching indicators"
    ]

    if primary_score.matched_indicators:
        rationale_parts.append(
            f"Key indicators: {', '.join(primary_score.matched_indicators[:3])}"
        )

    if primary_score.confidence_factors:
        rationale_parts.append(
            f"Supporting factors: {', '.join(primary_score.confidence_factors[:2])}"
        )

    if secondary_patterns:
        rationale_parts.append(
            f"Alternative patterns considered: {', '.join([p.value for p in secondary_patterns[:2]])}"
        )

    rationale = ". ".join(rationale_parts) + "."

    # Generate template customizations based on pattern and analysis
    template_customizations = generate_template_customizations(
        primary_pattern, analysis
    )

    # Phase 1/4: Detect normalized combinations (HYBRID as metadata only) and
    # augment rationale + confidence for robust combos.
    try:
        combinations = detect_combinations_func(pattern_scores)
    except Exception as e:  # Defensive: never break recommendation on combo detection
        logger.debug(f"Combination detection failed: {e}")
        combinations = {}
    if combinations:
        template_customizations["combination_info"] = combinations
        template_customizations["hybrid_candidate"] = True

        # Compute normalized scores by pattern for the current run
        max_score = max((s.total_score for s in pattern_scores), default=0.0) or 1.0
        norm_map: Dict[PatternType, float] = {
            s.pattern: (s.total_score / max_score) for s in pattern_scores
        }

        # Choose the strongest detected combination to summarize
        best_key = max(
            combinations,
            key=lambda k: float(combinations[k].get("combined_score", 0)),
            default=None,
        )
        combo_summary = None
        if best_key:
            try:
                pats = combinations[best_key].get("patterns", [])
                # Compose display like "RAG + AGENT"
                combo_summary = " + ".join(str(p) for p in pats)
            except Exception:
                combo_summary = None

        # Prepare top-2 normalized pattern summary
        top_two = pattern_scores[:2]
        top_two_str = ", ".join(
            f"{ps.pattern.value} ({(ps.total_score / max_score):.2f})"
            for ps in top_two
            if max_score > 0
        )

        combo_prefix = None
        if combo_summary:
            combo_prefix = f"Detected composite scenario: {combo_summary}. Top patterns: {top_two_str}."
        else:
            # Fallback to only top-2 if unable to build combo summary
            combo_prefix = f"Top patterns: {top_two_str}."

        # Prepend to existing brief rationale
        if combo_prefix:
            rationale = f"{combo_prefix} {rationale}"

        # Confidence bump for robust combinations: all members have norm >= 0.8
        try:
            robust = False
            for info in combinations.values():
                member_norms = []
                for p_str in info.get("patterns") or []:
                    try:
                        p_enum = PatternType(p_str)
                    except Exception:
                        continue
                    member_norms.append(norm_map.get(p_enum, 0.0))
                if member_norms and min(member_norms) >= 0.8:
                    robust = True
                    break
            if robust:
                confidence_score = min(confidence_score + 0.05, 1.0)
        except Exception:
            pass

    # Generate workflow suggestions
    workflow_suggestions = generate_workflow_suggestions(primary_pattern, analysis)

    # Add graduated complexity mapping
    complexity_mapping = get_graduated_complexity_mapping(analysis, primary_pattern)

    # Enhance template customizations with complexity info
    template_customizations.update(
        {
            "complexity_mapping": complexity_mapping,
            "graduated_structure": complexity_mapping.get(
                "recommended_structure", "DEFAULT"
            ),
        }
    )

    # Add complexity info to workflow suggestions
    workflow_suggestions.update(
        {
            "complexity_level": complexity_mapping["complexity_level"],
            "recommended_node_count": complexity_mapping["node_count"],
            "template_type": complexity_mapping["template_complexity"],
        }
    )

    return PatternRecommendation(
        primary_pattern=primary_pattern,
        confidence_score=confidence_score,
        secondary_patterns=secondary_patterns,
        rationale=rationale,
        detailed_justification=detailed_rationale,
        template_customizations=template_customizations,
        workflow_suggestions=workflow_suggestions,
    )
