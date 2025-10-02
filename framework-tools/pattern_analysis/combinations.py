#!/usr/bin/env python3
"""
Combinations Module

Detects meaningful pattern combinations using normalized scores
for hybrid PocketFlow pattern recommendations.
"""

from typing import Dict, Any, List
from .indicators import PatternType
from .scoring_engine import PatternScore


# Default combination detection rules
# Normalized thresholds are evaluated against max score in the current analysis run.
DEFAULT_COMBINATION_RULES = {
    "intelligent_rag": {
        "patterns": [PatternType.RAG, PatternType.AGENT],
        # Lower threshold to recognize mixed RAG/AGENT even if TOOL dominates
        "min_norm": 0.33,
    },
    "integration_workflow": {
        "patterns": [PatternType.TOOL, PatternType.WORKFLOW],
        "min_norm": 0.65,
    },
    "smart_processing": {
        "patterns": [PatternType.MAPREDUCE, PatternType.AGENT],
        "min_norm": 0.70,
    },
}


def detect_combinations(
    pattern_scores: List[PatternScore],
    combination_rules: Dict[str, Dict[str, Any]],
    top_n: int = 4,
) -> Dict[str, Any]:
    """Detect meaningful pattern combinations using normalized scores.

    - Normalizes by the maximum total score among all patterns (guard against zero).
    - Checks predefined combos within the top-N ranked patterns only.
    - Triggers when all combo members are in the top-N and each meets its min normalized threshold.

    Thresholds are read from `combination_rules` which can be adjusted per instance.

    Returns a mapping like:
    {
        "intelligent_rag": {
            "patterns": ["RAG", "AGENT"],
            "combined_score": 1.55,   # sum of norms
            "rank_window": 3
        },
        ...
    }
    """
    if not pattern_scores:
        return {}

    # Consider only top-N items for combination detection
    window = min(top_n, len(pattern_scores))
    top_scores = pattern_scores[:window]

    max_score = max((s.total_score for s in pattern_scores), default=0.0)
    if max_score <= 0:
        return {}

    # Map pattern -> normalized score within the top window
    norm_by_pattern: Dict[PatternType, float] = {
        s.pattern: (s.total_score / max_score) for s in top_scores
    }

    # Use provided combination rules (normalized thresholds)
    combos = combination_rules or {}

    detected: Dict[str, Any] = {}
    for key, cfg in combos.items():
        members: List[PatternType] = cfg["patterns"]
        threshold: float = cfg["min_norm"]

        # All members must be present in the top window and meet threshold
        norms: List[float] = []
        all_present = True
        for p in members:
            if p not in norm_by_pattern:
                all_present = False
                break
            norm_val = norm_by_pattern[p]
            if norm_val < threshold:
                all_present = False
                break
            norms.append(norm_val)

        if all_present and norms:
            detected[key] = {
                "patterns": [p.value for p in members],
                "combined_score": round(sum(norms), 4),
                "rank_window": window,
            }

    return detected
