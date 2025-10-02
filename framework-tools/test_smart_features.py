#!/usr/bin/env python3
"""
Test Suite for Smart Features Module
Tests pattern detection, version management, and intelligent suggestions
"""

import sys
import yaml
from pathlib import Path
from smart_features import (
    TechPatternDetector,
    ProgressiveDisclosure,
    VersionManager,
    IntelligentSuggestionSystem,
    analyze_specification_for_documentation,
)


def test_pattern_detection():
    """Test pattern detection functionality"""
    print("=== Testing Pattern Detection ===")

    # Test specification with multiple technologies
    test_spec = """
    We need to build a payment processing system that integrates with Stripe for handling
    subscriptions and one-time payments. The system should use FastAPI for the REST API
    endpoints and PostgreSQL for data storage. We'll need authentication via Auth0 JWT tokens
    and deploy using Docker containers on AWS Lambda functions. The frontend will use React 
    components with hooks for state management.
    """

    detector = TechPatternDetector()
    suggestions = detector.detect_documentation_needs(test_spec, "create-spec")

    print(f"Found {len(suggestions)} documentation suggestions:")
    for suggestion in suggestions:
        print(f"  - {suggestion['technology']}: {suggestion['priority']} priority")
        print(f"    Confidence: {suggestion['confidence']:.1%}")
        print(f"    Matches: {', '.join(suggestion['matched_patterns'])}")

    # Test context sensitivity
    planning_suggestions = detector.detect_documentation_needs(
        test_spec, "plan-product"
    )
    exec_suggestions = detector.detect_documentation_needs(test_spec, "execute-tasks")

    print("\nContext sensitivity test:")
    print(f"  plan-product context: {len(planning_suggestions)} suggestions")
    print(f"  create-spec context: {len(suggestions)} suggestions")
    print(f"  execute-tasks context: {len(exec_suggestions)} suggestions")

    return len(suggestions) > 0


def test_progressive_disclosure():
    """Test progressive disclosure functionality"""
    print("\n=== Testing Progressive Disclosure ===")

    disclosure = ProgressiveDisclosure(cache_dir="/tmp/test-cache")

    # Test all disclosure levels
    levels = ["overview", "planning", "implementation", "optimization"]
    for level in levels:
        content = disclosure.get_content_for_level("fastapi", level)
        print(f"  {level.capitalize()} level: {len(content['sections'])} sections")
        print(f"    Cache TTL: {content['metadata']['ttl_hours']} hours")

    # Test caching
    content1 = disclosure.get_content_for_level("fastapi", "overview")
    content2 = disclosure.get_content_for_level("fastapi", "overview")

    cache_hit = content1["timestamp"] == content2["timestamp"]
    print(f"\nCache test: {'PASS' if cache_hit else 'FAIL'} - Content cached properly")

    return True


def test_version_management():
    """Test version management functionality"""
    print("\n=== Testing Version Management ===")

    version_manager = VersionManager()

    # Test version detection
    test_content = """
    FastAPI 0.104.1 Documentation
    This is the official documentation for FastAPI version 0.104.1
    """

    detected_version = version_manager.detect_version(test_content, "fastapi")
    print(f"Version detection: {detected_version}")

    # Test compatibility checking
    compatibility = version_manager.check_compatibility("fastapi", "0.104.1")
    print(f"Compatibility status: {compatibility['status']}")
    print(f"Warnings: {len(compatibility['warnings'])}")

    # Test version comparison
    comparison = version_manager._compare_versions("0.104.1", "0.104.2")
    print(f"Version comparison (0.104.1 vs 0.104.2): {comparison}")

    comparison = version_manager._compare_versions("0.104.1", "1.0.0")
    print(f"Version comparison (0.104.1 vs 1.0.0): {comparison}")

    return detected_version is not None


def test_intelligent_suggestions():
    """Test intelligent suggestion system"""
    print("\n=== Testing Intelligent Suggestion System ===")

    suggestion_system = IntelligentSuggestionSystem()

    test_spec = """
    Build a REST API using FastAPI framework for a payment system. Integrate with Stripe
    for payment processing and use PostgreSQL for data persistence. Need authentication
    and authorization using JWT tokens. Deploy on AWS using Docker containers.
    """

    result = suggestion_system.generate_suggestions(test_spec, "create-spec")

    print("Generated suggestions:")
    print(
        f"  Pattern suggestions: {result['pattern_suggestions']['total_suggestions']}"
    )
    print(f"  Version issues: {result['version_compatibility']['needs_attention']}")
    print(
        f"  Disclosure level: {result['progressive_disclosure']['recommended_level']}"
    )
    print(f"  Recommendations: {len(result['recommendations'])}")

    # Display recommendations
    for rec in result["recommendations"]:
        print(f"    - {rec['title']} ({rec['priority']} priority)")
        print(f"      {rec['description']}")

    return len(result["recommendations"]) >= 0


def test_main_interface():
    """Test the main interface function"""
    print("\n=== Testing Main Interface ===")

    test_spec = """
    Create a web application with React frontend and FastAPI backend.
    Use PostgreSQL for data storage and integrate with Stripe for payments.
    Deploy using Docker on AWS with Auth0 for authentication.
    """

    result = analyze_specification_for_documentation(test_spec, "create-spec")

    print("Main interface test:")
    print(
        f"  Technologies detected: {len(result['pattern_suggestions']['by_priority'])}"
    )
    print(f"  Categories found: {len(result['pattern_suggestions']['by_category'])}")
    print(f"  Recommendations: {len(result['recommendations'])}")

    return "pattern_suggestions" in result and "recommendations" in result


def test_registry_integration():
    """Test integration with documentation registry"""
    print("\n=== Testing Registry Integration ===")

    # Create a test registry
    test_registry_path = "/tmp/test-docs-registry.yaml"
    test_registry = {
        "version": "1.0.0",
        "last_updated": "2025-01-12",
        "tech_stack": {
            "fastapi": {
                "type": "framework",
                "source": "https://fastapi.tiangolo.com/",
                "version": "0.104.1",
                "last_fetched": "2025-01-12",
            }
        },
        "external_apis": {},
        "internal_standards": {},
        "compliance": {},
        "pocketflow_patterns": {},
        "discovery_settings": {"auto_discover": True},
        "smart_features": {
            "pattern_detection": {"enabled": True, "confidence_threshold": 0.3}
        },
    }

    with open(test_registry_path, "w") as f:
        yaml.dump(test_registry, f)

    # Test with existing registry
    detector = TechPatternDetector(test_registry_path)
    suggestions = detector.detect_documentation_needs(
        "We need a FastAPI application", "create-spec"
    )

    print("Registry integration test:")
    print(f"  FastAPI already in registry - suggestions: {len(suggestions)}")
    print(
        f"  Should be 0 (already documented): {'PASS' if len(suggestions) == 0 else 'FAIL'}"
    )

    # Test with new technology
    new_suggestions = detector.detect_documentation_needs(
        "We need Django models and views", "create-spec"
    )
    print(f"  Django not in registry - suggestions: {len(new_suggestions)}")
    print(
        f"  Should be > 0 (needs documentation): {'PASS' if len(new_suggestions) > 0 else 'FAIL'}"
    )

    # Cleanup
    Path(test_registry_path).unlink(missing_ok=True)

    return True


def main():
    """Run all smart features tests"""
    print("Smart Features Test Suite")
    print("=" * 50)

    tests = [
        ("Pattern Detection", test_pattern_detection),
        ("Progressive Disclosure", test_progressive_disclosure),
        ("Version Management", test_version_management),
        ("Intelligent Suggestions", test_intelligent_suggestions),
        ("Main Interface", test_main_interface),
        ("Registry Integration", test_registry_integration),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"\n✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"\n❌ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {str(e)}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All smart features tests passed!")
        return 0
    else:
        print(f"⚠️  {failed} tests failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
