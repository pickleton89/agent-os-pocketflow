#!/usr/bin/env python3
"""
Complex Scenario Tests for Pattern Analyzer Agent

Tests complex requirements and edge cases to ensure robust pattern recognition.
"""

import logging
# Support running as a package (relative) and as a standalone script (absolute)
try:
    from .pattern_analyzer import PatternAnalyzer  # type: ignore
    from .agent_coordination import coordinate_pattern_analysis, AgentCoordinator  # type: ignore
except ImportError:  # pragma: no cover - fallback for standalone execution
    from pattern_analyzer import PatternAnalyzer
    from agent_coordination import coordinate_pattern_analysis, AgentCoordinator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ComplexScenarioTester:
    """Tests complex scenarios for pattern recognition."""
    
    def __init__(self):
        self.analyzer = PatternAnalyzer()
        self.coordinator = AgentCoordinator()
        self.test_results = []
    
    def run_all_tests(self):
        """Run all complex scenario tests."""
        
        print("=" * 80)
        print("COMPLEX SCENARIO TESTS FOR PATTERN ANALYZER AGENT")
        print("=" * 80)
        
        test_methods = [
            self.test_hybrid_requirements,
            self.test_ambiguous_requirements,
            self.test_enterprise_complexity,
            self.test_multi_domain_integration,
            self.test_performance_critical_systems,
            self.test_security_focused_requirements,
            self.test_real_time_systems,
            self.test_legacy_system_integration
        ]
        
        for test_method in test_methods:
            try:
                print(f"\n{'-' * 60}")
                print(f"Running: {test_method.__name__}")
                print(f"{'-' * 60}")
                test_method()
                print("✅ Test PASSED")
            except Exception as e:
                print(f"❌ Test FAILED: {e}")
                self.test_results.append({"test": test_method.__name__, "status": "failed", "error": str(e)})
            else:
                self.test_results.append({"test": test_method.__name__, "status": "passed"})
        
        self.print_test_summary()
    
    def test_hybrid_requirements(self):
        """Test requirements that span multiple patterns."""
        
        requirements = """
        Build an intelligent document processing platform that:
        1. Accepts documents via REST API endpoints 
        2. Uses AI to extract and analyze document content
        3. Stores processed data in a vector database for semantic search
        4. Provides real-time search capabilities with relevance ranking
        5. Integrates with external CRM systems via webhooks
        6. Processes documents in parallel for high throughput
        7. Makes autonomous decisions about document categorization
        8. Maintains structured output format for downstream systems
        """
        
        # This should detect multiple patterns with RAG being primary
        context = coordinate_pattern_analysis("HybridDocPlatform", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Confidence: {recommendation.confidence_score:.2f}")
        print(f"Secondary Patterns: {[p.value for p in recommendation.secondary_patterns]}")
        
        # Should identify RAG as primary with TOOL and AGENT as secondary
        assert recommendation.primary_pattern.value in ["RAG", "AGENT"], "Should identify RAG or AGENT for hybrid system"
        assert len(recommendation.secondary_patterns) >= 1, "Should identify multiple patterns"
    
    def test_ambiguous_requirements(self):
        """Test vague or ambiguous requirements."""
        
        requirements = """
        Create a smart system that processes stuff and makes things work better.
        It should be fast and handle data efficiently. Users should be able to 
        interact with it somehow and get results that make sense.
        """
        
        context = coordinate_pattern_analysis("AmbiguousSystem", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Confidence: {recommendation.confidence_score:.2f}")
        
        # Should default to WORKFLOW with low confidence
        assert recommendation.confidence_score < 0.4, "Ambiguous requirements should have low confidence"
        assert recommendation.primary_pattern.value == "WORKFLOW", "Should default to WORKFLOW for ambiguous requirements"
    
    def test_enterprise_complexity(self):
        """Test enterprise-level complex requirements."""
        
        requirements = """
        Develop a comprehensive enterprise AI platform that:
        1. Integrates with 15+ external systems including Salesforce, SAP, and Oracle
        2. Processes 10M+ documents daily with 99.9% uptime SLA
        3. Supports multi-tenant architecture with role-based access control
        4. Implements advanced AI reasoning for business process automation
        5. Provides real-time analytics dashboard with custom reporting
        6. Ensures GDPR, SOX, and HIPAA compliance across all operations
        7. Scales horizontally across multiple cloud regions
        8. Maintains audit trails for all system interactions
        9. Supports A/B testing for AI model deployment
        10. Implements disaster recovery with <1 hour RTO
        """
        
        context = coordinate_pattern_analysis("EnterpriseAIPlatform", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Confidence: {recommendation.confidence_score:.2f}")
        print(f"Template Customizations: {list(recommendation.template_customizations.keys())}")
        
        # Should identify high complexity and suggest appropriate patterns
        assert recommendation.confidence_score > 0.5, "Clear enterprise requirements should have high confidence"
        assert "enterprise" in recommendation.detailed_justification.lower(), "Should identify enterprise complexity"
    
    def test_multi_domain_integration(self):
        """Test requirements spanning multiple business domains."""
        
        requirements = """
        Build a unified platform that connects:
        - Customer service chatbot with natural language understanding
        - Inventory management with predictive analytics
        - Financial reporting with automated reconciliation
        - Marketing automation with customer segmentation
        - Supply chain optimization with demand forecasting
        - Quality control with computer vision inspection
        Each domain needs specialized processing but data flows between all systems.
        """
        
        context = coordinate_pattern_analysis("MultiDomainPlatform", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Secondary Patterns: {[p.value for p in recommendation.secondary_patterns]}")
        
        # Should suggest MULTI_AGENT or complex WORKFLOW pattern
        assert recommendation.primary_pattern.value in ["MULTI-AGENT", "WORKFLOW", "AGENT"], \
            "Multi-domain systems should suggest agent-based or workflow patterns"
    
    def test_performance_critical_systems(self):
        """Test high-performance, low-latency requirements."""
        
        requirements = """
        Create a high-frequency trading system that:
        - Processes market data streams at microsecond latency
        - Makes autonomous trading decisions in real-time
        - Handles 1M+ transactions per second
        - Implements risk management with immediate circuit breakers
        - Maintains sub-millisecond response times for API calls
        - Processes parallel data streams from multiple exchanges
        """
        
        context = coordinate_pattern_analysis("HFTradingSystem", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Performance Customizations: {recommendation.template_customizations}")
        
        # Should identify need for parallel processing patterns
        assert recommendation.primary_pattern.value in ["MAPREDUCE", "AGENT", "TOOL"], \
            "Performance-critical systems should suggest optimized patterns"
    
    def test_security_focused_requirements(self):
        """Test security-critical requirements."""
        
        requirements = """
        Develop a secure document management system that:
        - Encrypts all data at rest and in transit using AES-256
        - Implements zero-trust security model with multi-factor authentication
        - Provides end-to-end audit logging for compliance
        - Sanitizes and validates all input data to prevent injection attacks
        - Uses secure enclaves for sensitive document processing
        - Implements role-based access control with least privilege principle
        - Supports secure API authentication with OAuth 2.0 and JWT
        """
        
        context = coordinate_pattern_analysis("SecureDocSystem", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Security Features: {recommendation.template_customizations}")
        
        # Should identify security requirements and suggest appropriate customizations
        security_keywords = ["encrypt", "secure", "auth", "validation", "compliance"]
        assert any(keyword in str(recommendation.template_customizations).lower() 
                  for keyword in security_keywords), "Should identify security requirements"
    
    def test_real_time_systems(self):
        """Test real-time processing requirements."""
        
        requirements = """
        Build a real-time fraud detection system that:
        - Analyzes credit card transactions as they occur
        - Makes accept/reject decisions within 100ms
        - Learns from new fraud patterns continuously
        - Processes streaming data from multiple payment processors
        - Maintains 99.99% accuracy with minimal false positives
        - Scales to handle Black Friday traffic spikes
        - Provides real-time dashboards for fraud analysts
        """
        
        context = coordinate_pattern_analysis("FraudDetectionSystem", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Real-time Features: {recommendation.workflow_suggestions}")
        
        # Should suggest patterns optimized for real-time processing
        assert "real" in str(recommendation.template_customizations).lower() or \
               "stream" in str(recommendation.template_customizations).lower(), \
               "Should identify real-time requirements"
    
    def test_legacy_system_integration(self):
        """Test integration with legacy systems."""
        
        requirements = """
        Create an integration layer that connects modern AI services with:
        - Mainframe systems running COBOL applications
        - Legacy Oracle databases with proprietary schemas
        - SOAP-based web services from 2005
        - File-based ETL processes using CSV and XML
        - On-premise Windows applications with COM interfaces
        The system needs to transform data formats and handle connection failures gracefully.
        """
        
        context = coordinate_pattern_analysis("LegacyIntegrationLayer", requirements)
        recommendation = context.pattern_recommendation
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Integration Features: {recommendation.template_customizations}")
        
        # Should identify TOOL pattern for integration needs
        assert recommendation.primary_pattern.value in ["TOOL", "WORKFLOW"], \
            "Legacy integration should suggest TOOL or WORKFLOW patterns"
        
        # Should identify integration complexity
        assert len(recommendation.template_customizations) > 0, "Should suggest integration-specific customizations"
    
    def print_test_summary(self):
        """Print summary of test results."""
        
        print(f"\n{'=' * 80}")
        print("TEST SUMMARY")
        print(f"{'=' * 80}")
        
        passed = sum(1 for result in self.test_results if result["status"] == "passed")
        total = len(self.test_results)
        
        print(f"Tests Run: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if result["status"] == "failed":
                    print(f"  - {result['test']}: {result['error']}")
        
        print(f"\n{'=' * 80}")


def test_edge_cases():
    """Test edge cases and error conditions."""
    
    print("\n" + "=" * 60)
    print("EDGE CASE TESTS")
    print("=" * 60)
    
    analyzer = PatternAnalyzer()
    
    # Test empty requirements
    try:
        result = analyzer.analyze_and_recommend("")
        print(f"Empty requirements: {result.primary_pattern.value} (confidence: {result.confidence_score:.2f})")
    except Exception as e:
        print(f"Empty requirements error: {e}")
    
    # Test very long requirements
    long_requirements = "Create a system that processes data. " * 100
    result = analyzer.analyze_and_recommend(long_requirements)
    print(f"Long requirements: {result.primary_pattern.value} (confidence: {result.confidence_score:.2f})")
    
    # Test requirements with only technical jargon
    tech_requirements = "Implement microservices architecture with Kubernetes, Docker, Redis, PostgreSQL, and GraphQL APIs"
    result = analyzer.analyze_and_recommend(tech_requirements)
    print(f"Tech jargon: {result.primary_pattern.value} (confidence: {result.confidence_score:.2f})")


if __name__ == "__main__":
    # Run complex scenario tests
    tester = ComplexScenarioTester()
    tester.run_all_tests()
    
    # Run edge case tests
    test_edge_cases()
    
    print(f"\n{'*' * 80}")
    print("ALL TESTS COMPLETED")
    print(f"{'*' * 80}")
