#!/usr/bin/env python3
"""
Requirement Parser Module

Analyzes user requirements text and extracts key information including
keywords, complexity indicators, technical requirements, and integration needs.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class RequirementAnalysis:
    """Analysis of user requirements."""

    raw_text: str
    extracted_keywords: List[str] = field(default_factory=list)
    complexity_indicators: List[str] = field(default_factory=list)
    technical_requirements: List[str] = field(default_factory=list)
    functional_requirements: List[str] = field(default_factory=list)
    integration_needs: List[str] = field(default_factory=list)


def analyze_requirements(requirements_text: str) -> RequirementAnalysis:
    """Analyze user requirements and extract key information."""
    logger.info("Analyzing requirements text")

    # Normalize text
    normalized_text = requirements_text.lower().strip()

    # Extract keywords using regex patterns
    word_pattern = r"\b\w+\b"
    all_words = re.findall(word_pattern, normalized_text)

    # Filter for meaningful keywords (exclude stop words)
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "this",
        "that",
        "these",
        "those",
    }

    keywords = [word for word in all_words if word not in stop_words and len(word) > 2]

    # Extract complexity indicators
    complexity_patterns = [
        r"complex|complicated|advanced|sophisticated|enterprise",
        r"multi-step|multi-stage|multi-phase",
        r"scalable|scale|performance|optimize",
        r"integrate|coordination|orchestrat",
    ]

    complexity_indicators = []
    for pattern in complexity_patterns:
        matches = re.findall(pattern, normalized_text, re.IGNORECASE)
        complexity_indicators.extend(matches)

    # Extract technical requirements
    technical_patterns = [
        r"api|rest|graphql|websocket",
        r"database|sql|nosql|mongodb|postgresql",
        r"cloud|aws|azure|gcp",
        r"docker|kubernetes|container",
        r"microservice|service|endpoint",
    ]

    technical_requirements = []
    for pattern in technical_patterns:
        matches = re.findall(pattern, normalized_text, re.IGNORECASE)
        technical_requirements.extend(matches)

    # Extract functional requirements (using sentence-level analysis)
    sentences = re.split(r"[.!?]", requirements_text)
    functional_requirements = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 10
        and any(
            func_word in s.lower()
            for func_word in ["need", "want", "require", "should", "must", "will"]
        )
    ]

    # Extract integration needs
    integration_patterns = [
        r"integrate with \w+",
        r"connect to \w+",
        r"api integration",
        r"third.?party",
        r"external system",
    ]

    integration_needs = []
    for pattern in integration_patterns:
        matches = re.findall(pattern, normalized_text, re.IGNORECASE)
        integration_needs.extend(matches)

    return RequirementAnalysis(
        raw_text=requirements_text,
        extracted_keywords=keywords,
        complexity_indicators=complexity_indicators,
        technical_requirements=technical_requirements,
        functional_requirements=functional_requirements,
        integration_needs=integration_needs,
    )
