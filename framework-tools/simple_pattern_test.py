#!/usr/bin/env python3
"""
Simple test for Pattern Analyzer
"""

# Support running as a package (relative) and as a standalone script (absolute)
try:
    from .pattern_analyzer import PatternAnalyzer  # type: ignore
except ImportError:  # pragma: no cover - fallback for standalone execution
    from pattern_analyzer import PatternAnalyzer


def test_pattern_analysis():
    """Test pattern analysis functionality."""

    analyzer = PatternAnalyzer()

    test_cases = [
        "I need to build a document search system using vector embeddings",
        "Create an intelligent agent that makes autonomous decisions",
        "Build an API integration system for external services",
        "Design a multi-step workflow for data processing",
    ]

    print("Pattern Analysis Test Results:")
    print("=" * 50)

    for i, requirement in enumerate(test_cases, 1):
        print(f"\nTest {i}: {requirement}")
        print("-" * 30)

        try:
            recommendation = analyzer.analyze_and_recommend(requirement)
            print(f"Pattern: {recommendation.primary_pattern.value}")
            print(f"Confidence: {recommendation.confidence_score:.2f}")
            print(f"Rationale: {recommendation.rationale[:80]}...")

        except Exception as e:
            print(f"Error: {e}")

    print("\nTest complete!")


if __name__ == "__main__":
    test_pattern_analysis()
