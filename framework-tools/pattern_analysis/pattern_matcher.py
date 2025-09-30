#!/usr/bin/env python3
"""
Pattern Matcher Module

Handles pattern complexity assessment, graduated complexity mapping,
and universal pattern mapping for PocketFlow patterns.
"""

from typing import Dict, Any
from .indicators import PatternType
from .requirement_parser import RequirementAnalysis


def assess_complexity(analysis: RequirementAnalysis) -> str:
    """Assess the complexity level of requirements with graduated mapping."""

    complexity_score = 0

    # Factor in various complexity indicators
    complexity_score += len(analysis.complexity_indicators) * 2
    complexity_score += len(analysis.technical_requirements)
    complexity_score += len(analysis.integration_needs) * 2
    complexity_score += min(len(analysis.functional_requirements), 5)

    # Word count as complexity indicator
    word_count = len(analysis.extracted_keywords)
    if word_count > 50:
        complexity_score += 3
    elif word_count > 30:
        complexity_score += 2
    elif word_count > 20:
        complexity_score += 1

    if complexity_score >= 15:
        return "High - Complex multi-system integration with advanced requirements"
    elif complexity_score >= 8:
        return "Medium - Moderate complexity with multiple components"
    else:
        return "Low - Simple workflow with basic requirements"


def get_graduated_complexity_mapping(analysis: RequirementAnalysis, primary_pattern: PatternType) -> Dict[str, Any]:
    """
    Map requirements to graduated PocketFlow patterns based on complexity.
    Implements the graduated complexity system from the mission statement:

    Simple Task → Basic WORKFLOW pattern (3 nodes)
    Multi-step Process → Enhanced WORKFLOW pattern (5-7 nodes + utilities)
    Complex Integration → TOOL/AGENT pattern (full PocketFlow architecture)
    LLM Applications → Complete Agentic Coding methodology
    """
    complexity_assessment = assess_complexity(analysis)

    mapping = {
        "complexity_level": complexity_assessment,
        "suggested_pattern": primary_pattern,
        "node_count": 3,  # Default minimum
        "requires_utilities": False,
        "requires_advanced_features": False,
        "template_complexity": "basic"
    }

    # Simple Tasks (Low Complexity)
    if "Low" in complexity_assessment:
        if primary_pattern == PatternType.WORKFLOW:
            mapping.update({
                "suggested_pattern": PatternType.WORKFLOW,
                "node_count": 3,  # Basic: Input→Process→Output
                "template_complexity": "simple",
                "recommended_structure": "SIMPLE_WORKFLOW",
                "description": "Basic 3-node workflow for straightforward tasks"
            })
        elif primary_pattern == PatternType.TOOL:
            mapping.update({
                "suggested_pattern": PatternType.TOOL,
                "node_count": 3,  # Request→Process→Response
                "template_complexity": "simple",
                "recommended_structure": "BASIC_API",
                "description": "Simple API integration with basic request/response"
            })

    # Multi-step Processes (Medium Complexity)
    elif "Medium" in complexity_assessment:
        if primary_pattern == PatternType.WORKFLOW:
            mapping.update({
                "node_count": 6,  # Enhanced workflow with validation, processing, formatting
                "requires_utilities": True,
                "template_complexity": "enhanced",
                "recommended_structure": "ENHANCED_WORKFLOW",
                "description": "Multi-step workflow with validation and error handling"
            })
        elif primary_pattern == PatternType.TOOL:
            mapping.update({
                "node_count": 5,  # Auth→Validate→Process→Transform→Response
                "requires_utilities": True,
                "template_complexity": "enhanced",
                "recommended_structure": "INTEGRATION_TOOL",
                "description": "Full integration with authentication and data transformation"
            })
        elif primary_pattern == PatternType.MAPREDUCE:
            mapping.update({
                "node_count": 4,  # Split→Map→Reduce→Collect
                "requires_utilities": True,
                "template_complexity": "enhanced",
                "recommended_structure": "DATA_PROCESSING",
                "description": "Parallel data processing pipeline"
            })

    # Complex Integration (High Complexity)
    elif "High" in complexity_assessment:
        mapping.update({
            "requires_utilities": True,
            "requires_advanced_features": True,
            "template_complexity": "full"
        })

        if primary_pattern == PatternType.AGENT:
            mapping.update({
                "node_count": 8,  # Full agentic workflow
                "recommended_structure": "AGENT_SYSTEM",
                "description": "Complete agentic system with reasoning and tool integration"
            })
        elif primary_pattern == PatternType.RAG:
            mapping.update({
                "node_count": 7,  # Document processing, indexing, retrieval, generation
                "recommended_structure": "RAG_SYSTEM",
                "description": "Full RAG system with vector storage and semantic search"
            })
        elif primary_pattern == PatternType.MULTI_AGENT:
            mapping.update({
                "node_count": 10,  # Multiple coordinated agents
                "recommended_structure": "MULTI_AGENT_SYSTEM",
                "description": "Collaborative multi-agent system with coordination"
            })

    # Add pattern-specific mappings regardless of complexity
    enhance_pattern_mapping(mapping, primary_pattern, analysis)

    return mapping


def enhance_pattern_mapping(mapping: Dict[str, Any], pattern: PatternType, analysis: RequirementAnalysis):
    """Enhance the mapping with pattern-specific details."""

    # Universal PocketFlow pattern mappings as specified in implementation plan
    pattern_mappings = {
        PatternType.WORKFLOW: {
            "use_case": "Simple CRUD Operations, Business Processes",
            "node_patterns": ["InputValidator", "BusinessLogic", "OutputFormatter"],
            "typical_flows": ["validation -> processing -> response"]
        },
        PatternType.TOOL: {
            "use_case": "API Services/Integrations, External System Connections",
            "node_patterns": ["RequestHandler", "ExternalConnector", "ResponseProcessor"],
            "typical_flows": ["auth -> api_call -> data_transform"]
        },
        PatternType.MAPREDUCE: {
            "use_case": "Data Processing/ETL, Analytics, Bulk Operations",
            "node_patterns": ["DataSplitter", "Processor", "Aggregator"],
            "typical_flows": ["chunk -> process -> combine"]
        },
        PatternType.AGENT: {
            "use_case": "Complex Multi-step Logic, Intelligent Decision Making",
            "node_patterns": ["TaskAnalyzer", "ReasoningEngine", "ActionExecutor"],
            "typical_flows": ["analyze -> reason -> act"]
        },
        PatternType.RAG: {
            "use_case": "Search/Query Operations, Knowledge Systems",
            "node_patterns": ["QueryProcessor", "Retriever", "Generator"],
            "typical_flows": ["query -> retrieve -> generate"]
        },
        PatternType.STRUCTURED_OUTPUT: {
            "use_case": "Simple Workflows with Validation, Form Processing",
            "node_patterns": ["InputParser", "Validator", "OutputBuilder"],
            "typical_flows": ["parse -> validate -> format"]
        }
    }

    if pattern in pattern_mappings:
        pattern_info = pattern_mappings[pattern]
        mapping.update({
            "pattern_use_case": pattern_info["use_case"],
            "typical_node_patterns": pattern_info["node_patterns"],
            "typical_flows": pattern_info["typical_flows"]
        })


def get_universal_pattern_mapping() -> Dict[str, Dict[str, Any]]:
    """
    Return the universal pattern mapping that covers all workflow types.
    This implements the key transformation from the implementation plan:
    removing conditional LLM/AI logic and making PocketFlow universal.
    """
    return {
        "Simple CRUD Operations": {
            "recommended_pattern": PatternType.WORKFLOW,
            "complexity": "simple",
            "description": "Basic create, read, update, delete operations",
            "indicators": ["crud", "form", "user", "admin", "simple", "basic"]
        },
        "API Services/Integrations": {
            "recommended_pattern": PatternType.TOOL,
            "complexity": "simple_to_enhanced",
            "description": "REST APIs, external service integrations",
            "indicators": ["api", "rest", "service", "integration", "external"]
        },
        "Data Processing/ETL": {
            "recommended_pattern": PatternType.MAPREDUCE,
            "complexity": "enhanced",
            "description": "Extract, transform, load operations",
            "indicators": ["etl", "data", "processing", "transform", "analytics"]
        },
        "Complex Multi-step Logic": {
            "recommended_pattern": PatternType.AGENT,
            "complexity": "full",
            "description": "Intelligent workflows requiring reasoning",
            "indicators": ["decision", "reasoning", "intelligent", "complex", "multi-step"]
        },
        "Search/Query Operations": {
            "recommended_pattern": PatternType.RAG,
            "complexity": "full",
            "description": "Document search, knowledge retrieval",
            "indicators": ["search", "query", "knowledge", "retrieval", "document"]
        },
        "Simple Workflows": {
            "recommended_pattern": PatternType.STRUCTURED_OUTPUT,
            "complexity": "simple",
            "description": "Structured data processing with validation",
            "indicators": ["structured", "validation", "format", "schema", "form"]
        }
    }
