#!/usr/bin/env python3
"""
Analyzer-focused tests for Phase 5.

Validates:
- Combination detection (RAG + AGENT) appears in `combination_info` metadata.
- Graduated simple structure recommendation for CRUD/forms → SIMPLE_WORKFLOW.
"""

import sys
from pathlib import Path

# Ensure we can import analyzer module from repo root
sys.path.insert(0, str(Path('pocketflow-tools')))

import pattern_analyzer as pa  # type: ignore


def test_detect_combination_rag_agent():
    analyzer = pa.PatternAnalyzer()
    req = (
        "RAG with semantic search, retrieval and vector embeddings plus an intelligent agent "
        "that performs decision making, planning, reasoning and autonomous action execution"
    )
    rec = analyzer.analyze_and_recommend(req)

    # Primary remains a concrete enum (no HYBRID promotion in analyzer)
    assert isinstance(rec.primary_pattern, pa.PatternType)
    assert rec.primary_pattern != pa.PatternType.HYBRID

    combo = (rec.template_customizations or {}).get("combination_info", {})
    assert isinstance(combo, dict) and combo, "combination_info should be present for mixed RAG/AGENT"

    # Verify that at least one detected combo includes both RAG and AGENT
    has_rag_agent = False
    for info in combo.values():
        try:
            pats = set(info.get("patterns") or [])
        except Exception:
            continue
        if {"RAG", "AGENT"}.issubset(pats):
            has_rag_agent = True
            break
    assert has_rag_agent, "Expected RAG + AGENT combination to be detected"


def test_simple_structure_recommendation():
    analyzer = pa.PatternAnalyzer()
    req = "Simple CRUD form to submit and review entries with basic features"
    rec = analyzer.analyze_and_recommend(req)

    gs = (rec.template_customizations or {}).get("graduated_structure")
    assert gs == "SIMPLE_WORKFLOW", "Expected SIMPLE_WORKFLOW for simple CRUD/forms text"

