#!/usr/bin/env python3
"""Pattern Analysis Engine for PocketFlow - DEPRECATED.

⚠️ DEPRECATION WARNING:
This module has been refactored into the pattern_analysis package for better modularity.
Please update your imports:

    OLD: from pattern_analyzer import PatternAnalyzer, PatternType
    NEW: from pattern_analysis import PatternAnalyzer, PatternType

This file will be removed in a future version.

For now, this file re-exports everything from pattern_analysis for backwards compatibility.
"""

import warnings

from pattern_analysis import (
    # Main class
    PatternAnalyzer,
    # Types and Enums
    PatternType,
    PatternIndicator,
    RequirementAnalysis,
    PatternScore,
    PatternRecommendation,
    # Constants
    DEFAULT_COMBINATION_RULES,
    # Functions
    load_pattern_indicators,
    load_context_rules,
    analyze_requirements,
    score_patterns,
    detect_combinations,
    assess_complexity,
    get_graduated_complexity_mapping,
    enhance_pattern_mapping,
    get_universal_pattern_mapping,
    generate_detailed_justification,
    get_pattern_specific_recommendations,
    generate_template_customizations,
    generate_workflow_suggestions,
    generate_recommendation,
    estimate_node_count,
    suggest_utilities,
)

# Issue deprecation warning after imports so ruff keeps module-order happy
warnings.warn(
    "pattern_analyzer module is deprecated. "
    "Please use 'from pattern_analysis import ...' instead. "
    "This compatibility shim will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "PatternAnalyzer",
    "PatternType",
    "PatternIndicator",
    "RequirementAnalysis",
    "PatternScore",
    "PatternRecommendation",
    "DEFAULT_COMBINATION_RULES",
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
