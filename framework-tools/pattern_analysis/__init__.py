#!/usr/bin/env python3
"""
Pattern Analysis Package

Refactored pattern analyzer with modular components.
Provides the main PatternAnalyzer class and all supporting types.
"""

import logging
from typing import Dict, Any, List, Optional

# Import all public types and functions
from .indicators import (
    PatternType,
    PatternIndicator,
    load_pattern_indicators,
    load_context_rules,
)
from .requirement_parser import RequirementAnalysis, analyze_requirements
from .scoring_engine import (
    PatternScore,
    score_patterns,
    estimate_node_count,
    suggest_utilities,
)
from .pattern_matcher import (
    assess_complexity,
    get_graduated_complexity_mapping,
    enhance_pattern_mapping,
    get_universal_pattern_mapping,
)
from .combinations import DEFAULT_COMBINATION_RULES, detect_combinations
from .recommender import (
    PatternRecommendation,
    generate_detailed_justification,
    get_pattern_specific_recommendations,
    generate_template_customizations,
    generate_workflow_suggestions,
    generate_recommendation,
)

logger = logging.getLogger(__name__)


class PatternAnalyzer:
    """Core pattern analysis engine.

    Phase 4 additions:
    - Combination detection thresholds (min_norm) are configurable at the class level via
      `DEFAULT_COMBINATION_RULES` and copied to `self.combination_rules` on init.
    - Rationale optionally prepends a brief composite scenario line with top-2 normalized scores.
    - Confidence gets a small bump for robust combinations (all members have norm >= 0.8).
    """

    # Class-level defaults for combination detection thresholds.
    # Normalized thresholds are evaluated against max score in the current analysis run.
    DEFAULT_COMBINATION_RULES = DEFAULT_COMBINATION_RULES

    def __init__(self, combination_rules: Optional[Dict[str, Dict[str, Any]]] = None):
        self.pattern_indicators = load_pattern_indicators()
        self.context_rules = load_context_rules()
        # Expose combination thresholds at the instance level for easy tuning
        self.combination_rules: Dict[str, Dict[str, Any]] = (
            (combination_rules or {}).copy()
            if combination_rules
            else self.DEFAULT_COMBINATION_RULES.copy()
        )
        # Simple caching for performance optimization
        self._analysis_cache = {}
        self._cache_size_limit = 100

    def analyze_requirements(self, requirements_text: str) -> RequirementAnalysis:
        """Analyze user requirements and extract key information."""
        return analyze_requirements(requirements_text)

    def score_patterns(self, analysis: RequirementAnalysis) -> List[PatternScore]:
        """Score all patterns based on requirement analysis."""
        return score_patterns(analysis, self.pattern_indicators, self.context_rules)

    def detect_combinations(
        self, pattern_scores: List[PatternScore], top_n: int = 4
    ) -> Dict[str, Any]:
        """Detect meaningful pattern combinations using normalized scores."""
        return detect_combinations(pattern_scores, self.combination_rules, top_n)

    def generate_recommendation(
        self, pattern_scores: List[PatternScore], analysis: RequirementAnalysis
    ) -> PatternRecommendation:
        """Generate final pattern recommendation from scores."""
        return generate_recommendation(
            pattern_scores, analysis, self.detect_combinations
        )

    def analyze_and_recommend(self, requirements_text: str) -> PatternRecommendation:
        """Complete analysis and recommendation pipeline with caching."""
        # Check cache first for performance optimization
        cache_key = hash(requirements_text.strip().lower())
        if cache_key in self._analysis_cache:
            logger.debug("Cache hit for requirements analysis")
            return self._analysis_cache[cache_key]

        logger.info(
            f"Starting pattern analysis for requirements: {requirements_text[:100]}..."
        )

        # Step 1: Analyze requirements
        analysis = self.analyze_requirements(requirements_text)
        logger.info(
            f"Extracted {len(analysis.extracted_keywords)} keywords, "
            f"{len(analysis.complexity_indicators)} complexity indicators"
        )

        # Step 2: Score patterns
        pattern_scores = self.score_patterns(analysis)
        logger.info(f"Scored {len(pattern_scores)} patterns")

        # Step 3: Generate recommendation
        recommendation = self.generate_recommendation(pattern_scores, analysis)
        logger.info(
            f"Recommended {recommendation.primary_pattern.value} with "
            f"confidence {recommendation.confidence_score:.2f}"
        )

        # Cache the result for future use
        self._cache_result(cache_key, recommendation)

        return recommendation

    def _cache_result(self, cache_key: int, recommendation: PatternRecommendation):
        """Cache analysis result with size management."""
        if len(self._analysis_cache) >= self._cache_size_limit:
            # Simple LRU: remove oldest entry (first key)
            oldest_key = next(iter(self._analysis_cache))
            del self._analysis_cache[oldest_key]

        self._analysis_cache[cache_key] = recommendation

    def clear_cache(self):
        """Clear the analysis cache."""
        self._analysis_cache.clear()
        logger.debug("Pattern analysis cache cleared")

    # Expose helper methods for backwards compatibility
    def get_graduated_complexity_mapping(
        self, analysis: RequirementAnalysis, primary_pattern: PatternType
    ) -> Dict[str, Any]:
        """Map requirements to graduated PocketFlow patterns based on complexity."""
        return get_graduated_complexity_mapping(analysis, primary_pattern)

    def get_universal_pattern_mapping(self) -> Dict[str, Dict[str, Any]]:
        """Return the universal pattern mapping that covers all workflow types."""
        return get_universal_pattern_mapping()


# Export all public APIs
__all__ = [
    # Main class
    "PatternAnalyzer",
    # Types and Enums
    "PatternType",
    "PatternIndicator",
    "RequirementAnalysis",
    "PatternScore",
    "PatternRecommendation",
    # Constants
    "DEFAULT_COMBINATION_RULES",
    # Functions (for advanced usage)
    "load_pattern_indicators",
    "load_context_rules",
    "analyze_requirements",
    "score_patterns",
    "detect_combinations",
    "assess_complexity",
    "get_graduated_complexity_mapping",
    "enhance_pattern_mapping",
    "get_universal_pattern_mapping",
    "generate_detailed_justification",
    "get_pattern_specific_recommendations",
    "generate_template_customizations",
    "generate_workflow_suggestions",
    "generate_recommendation",
    "estimate_node_count",
    "suggest_utilities",
]
