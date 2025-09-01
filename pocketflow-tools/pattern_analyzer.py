#!/usr/bin/env python3
"""
Pattern Analysis Engine for PocketFlow

Analyzes user requirements and identifies optimal PocketFlow patterns.
Part of the Pattern Analyzer Agent implementation.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Supported PocketFlow pattern types."""
    RAG = "RAG"
    AGENT = "AGENT" 
    TOOL = "TOOL"
    WORKFLOW = "WORKFLOW"
    MAPREDUCE = "MAPREDUCE"
    MULTI_AGENT = "MULTI-AGENT"
    STRUCTURED_OUTPUT = "STRUCTURED-OUTPUT"
    HYBRID = "HYBRID"


@dataclass
class PatternIndicator:
    """Individual pattern indicator with scoring."""
    pattern: PatternType
    keywords: List[str]
    weight: float
    context_multipliers: Dict[str, float] = field(default_factory=dict)


@dataclass  
class RequirementAnalysis:
    """Analysis of user requirements."""
    raw_text: str
    extracted_keywords: List[str] = field(default_factory=list)
    complexity_indicators: List[str] = field(default_factory=list)
    technical_requirements: List[str] = field(default_factory=list)
    functional_requirements: List[str] = field(default_factory=list)
    integration_needs: List[str] = field(default_factory=list)


@dataclass
class PatternScore:
    """Pattern scoring result."""
    pattern: PatternType
    base_score: float
    context_score: float
    total_score: float
    matched_indicators: List[str] = field(default_factory=list)
    confidence_factors: List[str] = field(default_factory=list)


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


class PatternAnalyzer:
    """Core pattern analysis engine."""

    def __init__(self):
        self.pattern_indicators = self._load_pattern_indicators()
        self.context_rules = self._load_context_rules()
        # Simple caching for performance optimization
        self._analysis_cache = {}
        self._cache_size_limit = 100

    def detect_combinations(self, pattern_scores: List["PatternScore"], top_n: int = 4) -> Dict[str, Any]:
        """Detect meaningful pattern combinations using normalized scores.

        - Normalizes by the maximum total score among all patterns (guarding for zero).
        - Checks predefined combos within the top-N ranked patterns only.
        - Triggers when all combo members are in the top-N and each meets its min normalized threshold.

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

        # Predefined combination rules (normalized thresholds)
        combos = {
            "intelligent_rag": {
                "patterns": [PatternType.RAG, PatternType.AGENT],
                # Calibrated to detect mixed RAG/AGENT scenarios where TOOL may dominate
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

    def _load_pattern_indicators(self) -> List[PatternIndicator]:
        """Load pattern indicator definitions with enhanced non-LLM pattern support."""
        return [
            # RAG Pattern Indicators
            PatternIndicator(
                pattern=PatternType.RAG,
                keywords=[
                    "search", "knowledge base", "documentation", "retrieval", "query",
                    "semantic", "vector", "embedding", "similarity", "document",
                    "index", "content", "find", "lookup", "information"
                ],
                weight=1.0,
                context_multipliers={
                    "database": 1.2,
                    "text": 1.1,
                    "question": 1.3,
                    "answer": 1.3
                }
            ),
            
            # Agent Pattern Indicators  
            PatternIndicator(
                pattern=PatternType.AGENT,
                keywords=[
                    "decision", "planning", "reasoning", "autonomous", "intelligent",
                    "adaptive", "llm", "ai", "model", "conversation", "chat",
                    "think", "analyze", "determine", "choose", "conclude"
                ],
                weight=1.0,
                context_multipliers={
                    "complex": 1.2,
                    "multi-step": 1.3,
                    "workflow": 1.1,
                    "conditional": 1.2
                }
            ),
            
            # Tool Pattern Indicators - Enhanced for traditional web/API apps
            PatternIndicator(
                pattern=PatternType.TOOL,
                keywords=[
                    "integration", "api", "external service", "automation", "connection",
                    "interface", "system", "service", "endpoint", "webhook",
                    "connector", "plugin", "bridge", "sync", "import", "export",
                    # Traditional web app indicators
                    "rest", "graphql", "http", "web service", "microservice", 
                    "database", "sql", "crud", "backend", "frontend", "client",
                    "authentication", "authorization", "session", "middleware"
                ],
                weight=1.2,  # Higher weight for common web patterns
                context_multipliers={
                    "third-party": 1.3,
                    "external": 1.2,
                    "integrate": 1.2,
                    "connect": 1.1,
                    # Web app multipliers
                    "web": 1.4,
                    "api": 1.3,
                    "rest": 1.3,
                    "service": 1.2,
                    "database": 1.2,
                    "auth": 1.1
                }
            ),
            
            # Workflow Pattern Indicators - Enhanced for traditional business apps
            PatternIndicator(
                pattern=PatternType.WORKFLOW,
                keywords=[
                    "process", "flow", "sequence", "step", "pipeline", "chain",
                    "orchestration", "coordination", "execution", "batch",
                    "serial", "sequential", "ordered", "stages",
                    # Traditional business process indicators
                    "crud", "form", "submit", "create", "read", "update", "delete",
                    "user", "dashboard", "admin", "management", "tracking",
                    "simple", "basic", "straightforward", "standard"
                ],
                weight=1.1,  # Slightly higher for common patterns
                context_multipliers={
                    "business": 1.2,
                    "approval": 1.3,
                    "review": 1.2,
                    "multi-step": 1.1,
                    # Business app multipliers
                    "crud": 1.4,
                    "form": 1.3,
                    "user": 1.2,
                    "admin": 1.2,
                    "simple": 1.3,
                    "basic": 1.3
                }
            ),
            
            # MapReduce Pattern Indicators
            PatternIndicator(
                pattern=PatternType.MAPREDUCE,
                keywords=[
                    "parallel", "distribute", "scale", "concurrent", "batch",
                    "aggregate", "reduce", "map", "partition", "chunk",
                    "divide", "split", "merge", "combine", "bulk",
                    # Data processing indicators
                    "etl", "data processing", "transform", "load", "extract",
                    "analytics", "reporting", "large dataset", "big data"
                ],
                weight=1.0,
                context_multipliers={
                    "large": 1.3,
                    "volume": 1.2,
                    "performance": 1.2,
                    "scalability": 1.3,
                    "data": 1.2,
                    "analytics": 1.3,
                    "etl": 1.4
                }
            ),
            
            # Multi-Agent Pattern Indicators
            PatternIndicator(
                pattern=PatternType.MULTI_AGENT,
                keywords=[
                    "multi-agent", "collaborative", "coordination", "specialist",
                    "expert", "team", "role", "delegate", "distribute",
                    "consensus", "voting", "committee", "panel", "group"
                ],
                weight=1.0,
                context_multipliers={
                    "complex": 1.3,
                    "specialized": 1.2,
                    "expert": 1.2,
                    "collaborative": 1.1
                }
            ),
            
            # Structured Output Pattern Indicators - Enhanced for APIs
            PatternIndicator(
                pattern=PatternType.STRUCTURED_OUTPUT,
                keywords=[
                    "structured", "format", "schema", "json", "xml", "csv",
                    "template", "form", "validation", "constraint", "field",
                    "data model", "specification", "standard", "compliance",
                    # API response indicators
                    "response", "payload", "output", "format", "serialize",
                    "model", "pydantic", "schema validation", "type checking"
                ],
                weight=1.0,
                context_multipliers={
                    "validation": 1.3,
                    "compliance": 1.2,
                    "format": 1.2,
                    "standard": 1.1,
                    "api": 1.2,
                    "json": 1.2,
                    "schema": 1.3
                }
            )
        ]

    def _load_context_rules(self) -> Dict[str, float]:
        """Load context-specific scoring rules."""
        return {
            # Complexity indicators
            "simple": 0.8,
            "basic": 0.8,
            "complex": 1.3,
            "advanced": 1.2,
            "enterprise": 1.4,
            
            # Scale indicators
            "small": 0.9,
            "large": 1.2,
            "massive": 1.4,
            "scale": 1.2,
            
            # Performance indicators
            "fast": 1.1,
            "performance": 1.2,
            "realtime": 1.3,
            "batch": 1.1,
            
            # Integration indicators
            "integrate": 1.2,
            "external": 1.2,
            "third-party": 1.3,
            "api": 1.1
        }

    def analyze_requirements(self, requirements_text: str) -> RequirementAnalysis:
        """Analyze user requirements and extract key information."""
        logger.info("Analyzing requirements text")
        
        # Normalize text
        normalized_text = requirements_text.lower().strip()
        
        # Extract keywords using regex patterns
        word_pattern = r'\b\w+\b'
        all_words = re.findall(word_pattern, normalized_text)
        
        # Filter for meaningful keywords (exclude stop words)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        keywords = [word for word in all_words if word not in stop_words and len(word) > 2]
        
        # Extract complexity indicators
        complexity_patterns = [
            r'complex|complicated|advanced|sophisticated|enterprise',
            r'multi-step|multi-stage|multi-phase',
            r'scalable|scale|performance|optimize',
            r'integrate|coordination|orchestrat'
        ]
        
        complexity_indicators = []
        for pattern in complexity_patterns:
            matches = re.findall(pattern, normalized_text, re.IGNORECASE)
            complexity_indicators.extend(matches)
        
        # Extract technical requirements
        technical_patterns = [
            r'api|rest|graphql|websocket',
            r'database|sql|nosql|mongodb|postgresql',
            r'cloud|aws|azure|gcp',
            r'docker|kubernetes|container',
            r'microservice|service|endpoint'
        ]
        
        technical_requirements = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, normalized_text, re.IGNORECASE)
            technical_requirements.extend(matches)
        
        # Extract functional requirements (using sentence-level analysis)
        sentences = re.split(r'[.!?]', requirements_text)
        functional_requirements = [
            s.strip() for s in sentences
            if len(s.strip()) > 10 and any(
                func_word in s.lower() 
                for func_word in ['need', 'want', 'require', 'should', 'must', 'will']
            )
        ]
        
        # Extract integration needs
        integration_patterns = [
            r'integrate with \w+',
            r'connect to \w+',
            r'api integration',
            r'third.?party',
            r'external system'
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
            integration_needs=integration_needs
        )

    def score_patterns(self, analysis: RequirementAnalysis) -> List[PatternScore]:
        """Score all patterns based on requirement analysis."""
        logger.info("Scoring patterns against requirements")
        
        pattern_scores = []
        
        for indicator in self.pattern_indicators:
            # Calculate base score from keyword matches
            base_score = 0.0
            matched_keywords = []
            
            for keyword in indicator.keywords:
                if any(keyword.lower() in req_keyword.lower() for req_keyword in analysis.extracted_keywords):
                    base_score += indicator.weight
                    matched_keywords.append(keyword)
                
                # Also check in raw text for phrase matches
                if keyword.lower() in analysis.raw_text.lower():
                    base_score += indicator.weight * 0.5  # Partial credit for text match
                    if keyword not in matched_keywords:
                        matched_keywords.append(keyword)
            
            # Apply context multipliers
            context_score = 0.0
            confidence_factors = []
            
            for context_key, multiplier in indicator.context_multipliers.items():
                if any(context_key.lower() in keyword.lower() for keyword in analysis.extracted_keywords):
                    context_score += base_score * (multiplier - 1.0)
                    confidence_factors.append(f"Context: {context_key}")
            
            # Apply global context rules
            for rule_key, rule_multiplier in self.context_rules.items():
                if any(rule_key.lower() in keyword.lower() for keyword in analysis.extracted_keywords):
                    context_score += base_score * (rule_multiplier - 1.0)
                    confidence_factors.append(f"Rule: {rule_key}")
            
            total_score = base_score + context_score
            
            pattern_scores.append(PatternScore(
                pattern=indicator.pattern,
                base_score=base_score,
                context_score=context_score,
                total_score=total_score,
                matched_indicators=matched_keywords,
                confidence_factors=confidence_factors
            ))
        
        # Sort by total score descending
        pattern_scores.sort(key=lambda x: x.total_score, reverse=True)
        
        return pattern_scores

    def generate_detailed_justification(self, pattern_scores: List[PatternScore], analysis: RequirementAnalysis) -> str:
        """Generate detailed justification for pattern selection."""
        
        if not pattern_scores:
            return "No pattern indicators found in the requirements. Using default workflow pattern."
        
        primary_score = pattern_scores[0]
        
        justification_parts = []
        
        # Primary pattern justification
        justification_parts.append(f"**Primary Pattern Selection: {primary_score.pattern.value}**")
        justification_parts.append(f"Selected with confidence score of {primary_score.total_score:.2f}")
        justification_parts.append("")
        
        # Detailed indicator analysis
        justification_parts.append("**Key Indicators Found:**")
        for indicator in primary_score.matched_indicators[:5]:  # Top 5
            justification_parts.append(f"- '{indicator}' - Strong indicator for {primary_score.pattern.value} pattern")
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
        complexity_assessment = self._assess_complexity(analysis)
        justification_parts.append(f"**Complexity Assessment:** {complexity_assessment}")
        justification_parts.append("")
        
        # Technical requirements alignment
        if analysis.technical_requirements:
            justification_parts.append("**Technical Requirements Alignment:**")
            for tech_req in analysis.technical_requirements[:3]:
                justification_parts.append(f"- {tech_req} - Compatible with {primary_score.pattern.value} pattern")
            justification_parts.append("")
        
        # Pattern-specific recommendations
        pattern_recs = self._get_pattern_specific_recommendations(primary_score.pattern, analysis)
        if pattern_recs:
            justification_parts.append("**Pattern-Specific Recommendations:**")
            for rec in pattern_recs:
                justification_parts.append(f"- {rec}")
            justification_parts.append("")
        
        return "\n".join(justification_parts)
    
    def _assess_complexity(self, analysis: RequirementAnalysis) -> str:
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

    def get_graduated_complexity_mapping(self, analysis: RequirementAnalysis, primary_pattern: PatternType) -> Dict[str, Any]:
        """
        Map requirements to graduated PocketFlow patterns based on complexity.
        Implements the graduated complexity system from the mission statement:
        
        Simple Task → Basic WORKFLOW pattern (3 nodes)
        Multi-step Process → Enhanced WORKFLOW pattern (5-7 nodes + utilities)  
        Complex Integration → TOOL/AGENT pattern (full PocketFlow architecture)
        LLM Applications → Complete Agentic Coding methodology
        """
        complexity_assessment = self._assess_complexity(analysis)
        
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
        self._enhance_pattern_mapping(mapping, primary_pattern, analysis)
        
        return mapping

    def _enhance_pattern_mapping(self, mapping: Dict[str, Any], pattern: PatternType, analysis: RequirementAnalysis):
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

    def get_universal_pattern_mapping(self) -> Dict[str, Dict[str, Any]]:
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
    
    def _get_pattern_specific_recommendations(self, pattern: PatternType, analysis: RequirementAnalysis) -> List[str]:
        """Get pattern-specific implementation recommendations."""
        
        recommendations = []
        
        if pattern == PatternType.RAG:
            recommendations.extend([
                "Consider using chromadb or pinecone for vector storage",
                "Implement chunking strategy for large documents",
                "Add semantic similarity scoring for retrieved content"
            ])
            if "real-time" in analysis.raw_text.lower():
                recommendations.append("Implement caching for frequently queried content")
        
        elif pattern == PatternType.AGENT:
            recommendations.extend([
                "Implement structured reasoning with chain-of-thought prompting",
                "Add memory management for context persistence",
                "Consider tool integration for external actions"
            ])
            if "planning" in analysis.raw_text.lower():
                recommendations.append("Implement multi-step planning with backtracking")
        
        elif pattern == PatternType.TOOL:
            recommendations.extend([
                "Implement robust error handling for external API failures",
                "Add rate limiting and retry mechanisms",
                "Consider webhook integration for async operations"
            ])
            if len(analysis.integration_needs) > 2:
                recommendations.append("Consider implementing circuit breaker pattern")
        
        elif pattern == PatternType.WORKFLOW:
            recommendations.extend([
                "Add workflow state persistence for long-running processes",
                "Implement checkpoint and resume functionality",
                "Consider adding approval gates for critical steps"
            ])
        
        return recommendations

    def generate_recommendation(self, pattern_scores: List[PatternScore], analysis: RequirementAnalysis) -> PatternRecommendation:
        """Generate final pattern recommendation from scores."""
        logger.info("Generating pattern recommendation")
        
        if not pattern_scores:
            return PatternRecommendation(
                primary_pattern=PatternType.WORKFLOW,
                confidence_score=0.5,
                rationale="No clear pattern indicators found. Defaulting to basic WORKFLOW pattern."
            )
        
        # Get primary pattern (highest score)
        primary_score = pattern_scores[0]
        primary_pattern = primary_score.pattern
        
        # Calculate confidence based on score separation and absolute score
        max_possible_score = len(analysis.extracted_keywords) * 2.0  # Rough estimate
        confidence_score = min(primary_score.total_score / max_possible_score, 1.0) if max_possible_score > 0 else 0.5
        
        # Boost confidence if there's a clear winner
        if len(pattern_scores) > 1:
            score_separation = primary_score.total_score - pattern_scores[1].total_score
            if score_separation > 2.0:
                confidence_score = min(confidence_score * 1.2, 1.0)
        
        # Determine secondary patterns (scores within 70% of primary)
        threshold = primary_score.total_score * 0.7
        secondary_patterns = [
            score.pattern for score in pattern_scores[1:6]  # Top 5 alternatives
            if score.total_score >= threshold and score.total_score > 0
        ]
        
        # Generate detailed rationale
        detailed_rationale = self.generate_detailed_justification(pattern_scores, analysis)
        
        # Also generate a brief rationale for backward compatibility
        rationale_parts = [
            f"Primary pattern {primary_pattern.value} selected based on {len(primary_score.matched_indicators)} matching indicators"
        ]
        
        if primary_score.matched_indicators:
            rationale_parts.append(f"Key indicators: {', '.join(primary_score.matched_indicators[:3])}")
        
        if primary_score.confidence_factors:
            rationale_parts.append(f"Supporting factors: {', '.join(primary_score.confidence_factors[:2])}")
        
        if secondary_patterns:
            rationale_parts.append(f"Alternative patterns considered: {', '.join([p.value for p in secondary_patterns[:2]])}")
        
        rationale = ". ".join(rationale_parts) + "."
        
        # Generate template customizations based on pattern and analysis
        template_customizations = self._generate_template_customizations(primary_pattern, analysis)

        # Phase 1: Detect normalized combinations (HYBRID as metadata only)
        try:
            combinations = self.detect_combinations(pattern_scores)
        except Exception as e:  # Defensive: never break recommendation on combo detection
            logger.debug(f"Combination detection failed: {e}")
            combinations = {}
        if combinations:
            template_customizations["combination_info"] = combinations
            template_customizations["hybrid_candidate"] = True
        
        # Generate workflow suggestions
        workflow_suggestions = self._generate_workflow_suggestions(primary_pattern, analysis)
        
        # Add graduated complexity mapping
        complexity_mapping = self.get_graduated_complexity_mapping(analysis, primary_pattern)
        
        # Enhance template customizations with complexity info
        template_customizations.update({
            "complexity_mapping": complexity_mapping,
            "graduated_structure": complexity_mapping.get("recommended_structure", "DEFAULT")
        })
        
        # Add complexity info to workflow suggestions
        workflow_suggestions.update({
            "complexity_level": complexity_mapping["complexity_level"],
            "recommended_node_count": complexity_mapping["node_count"],
            "template_type": complexity_mapping["template_complexity"]
        })
        
        return PatternRecommendation(
            primary_pattern=primary_pattern,
            confidence_score=confidence_score,
            secondary_patterns=secondary_patterns,
            rationale=rationale,
            detailed_justification=detailed_rationale,
            template_customizations=template_customizations,
            workflow_suggestions=workflow_suggestions
        )

    def _generate_template_customizations(self, pattern: PatternType, analysis: RequirementAnalysis) -> Dict[str, Any]:
        """Generate template customization suggestions based on pattern and requirements."""
        customizations = {}
        
        # Pattern-specific customizations
        if pattern == PatternType.RAG:
            customizations.update({
                "vector_database": "chromadb" if "chroma" in analysis.raw_text.lower() else "default",
                "embedding_model": "sentence-transformers" if "embedding" in analysis.raw_text.lower() else "default",
                "retrieval_strategy": "semantic" if "semantic" in analysis.raw_text.lower() else "keyword",
                "chunk_size": 1000,
                "similarity_threshold": 0.7
            })
        
        elif pattern == PatternType.AGENT:
            customizations.update({
                "llm_provider": "openai" if "openai" in analysis.raw_text.lower() else "anthropic",
                "reasoning_type": "chain-of-thought" if "reasoning" in analysis.raw_text.lower() else "direct",
                "memory_enabled": "conversation" in analysis.raw_text.lower(),
                "tool_calling": len(analysis.integration_needs) > 0
            })
        
        elif pattern == PatternType.TOOL:
            customizations.update({
                "integration_type": "rest" if "rest" in analysis.raw_text.lower() else "webhook",
                "authentication": "oauth" if "oauth" in analysis.raw_text.lower() else "api_key",
                "rate_limiting": "performance" in analysis.complexity_indicators,
                "error_handling": "retry" if "reliable" in analysis.raw_text.lower() else "fail_fast"
            })
        
        # Add common customizations based on complexity
        if "enterprise" in analysis.complexity_indicators:
            customizations["logging_level"] = "detailed"
            customizations["monitoring"] = "enabled"
            customizations["caching"] = "redis"
        
        return customizations

    def _generate_workflow_suggestions(self, pattern: PatternType, analysis: RequirementAnalysis) -> Dict[str, Any]:
        """Generate workflow structure suggestions."""
        suggestions = {
            "estimated_nodes": self._estimate_node_count(analysis),
            "suggested_utilities": self._suggest_utilities(pattern, analysis),
            "error_handling": "comprehensive" if "enterprise" in analysis.complexity_indicators else "basic",
            "async_processing": any(
                async_indicator in analysis.raw_text.lower() 
                for async_indicator in ["async", "concurrent", "parallel", "api", "external"]
            )
        }
        
        # Pattern-specific suggestions
        if pattern == PatternType.RAG:
            suggestions.update({
                "preprocessing_nodes": ["document_loader", "chunker", "embedder"],
                "retrieval_nodes": ["query_processor", "retriever", "ranker"],
                "generation_nodes": ["context_formatter", "llm_generator"]
            })
        
        elif pattern == PatternType.AGENT:
            suggestions.update({
                "planning_nodes": ["task_analyzer", "planner"],
                "execution_nodes": ["reasoning_engine", "action_executor"],
                "reflection_nodes": ["result_evaluator", "memory_updater"]
            })
        
        elif pattern == PatternType.TOOL:
            suggestions.update({
                "integration_nodes": ["auth_handler", "api_client", "response_processor"],
                "transformation_nodes": ["input_formatter", "output_parser"],
                "validation_nodes": ["request_validator", "response_validator"]
            })
        
        return suggestions

    def _estimate_node_count(self, analysis: RequirementAnalysis) -> int:
        """Estimate the number of nodes needed based on complexity."""
        base_count = 3  # Minimum nodes for any workflow
        
        # Add nodes based on complexity indicators
        complexity_bonus = len(analysis.complexity_indicators) * 2
        
        # Add nodes based on functional requirements
        functional_bonus = min(len(analysis.functional_requirements), 5)
        
        # Add nodes based on integration needs
        integration_bonus = len(analysis.integration_needs)
        
        return base_count + complexity_bonus + functional_bonus + integration_bonus

    def _suggest_utilities(self, pattern: PatternType, analysis: RequirementAnalysis) -> List[str]:
        """Suggest utility functions based on pattern and requirements."""
        utilities = []
        
        # Pattern-specific utilities
        pattern_utilities = {
            PatternType.RAG: ["vector_search", "document_processor", "embedding_generator"],
            PatternType.AGENT: ["llm_client", "reasoning_engine", "memory_manager"],
            PatternType.TOOL: ["api_client", "data_transformer", "error_handler"],
            PatternType.WORKFLOW: ["flow_controller", "state_manager"],
            PatternType.MAPREDUCE: ["task_distributor", "result_aggregator"],
            PatternType.MULTI_AGENT: ["agent_coordinator", "consensus_manager"],
            PatternType.STRUCTURED_OUTPUT: ["schema_validator", "output_formatter"]
        }
        
        utilities.extend(pattern_utilities.get(pattern, []))
        
        # Add utilities based on technical requirements
        if any("api" in req.lower() for req in analysis.technical_requirements):
            utilities.append("api_client")
        
        if any("database" in req.lower() for req in analysis.technical_requirements):
            utilities.append("database_connector")
        
        if "performance" in analysis.complexity_indicators:
            utilities.append("performance_monitor")
        
        # Remove duplicates and limit to reasonable number
        return list(set(utilities))[:8]

    def analyze_and_recommend(self, requirements_text: str) -> PatternRecommendation:
        """Complete analysis and recommendation pipeline with caching."""
        # Check cache first for performance optimization
        cache_key = hash(requirements_text.strip().lower())
        if cache_key in self._analysis_cache:
            logger.debug(f"Cache hit for requirements analysis")
            return self._analysis_cache[cache_key]
            
        logger.info(f"Starting pattern analysis for requirements: {requirements_text[:100]}...")
        
        # Step 1: Analyze requirements
        analysis = self.analyze_requirements(requirements_text)
        logger.info(f"Extracted {len(analysis.extracted_keywords)} keywords, "
                   f"{len(analysis.complexity_indicators)} complexity indicators")
        
        # Step 2: Score patterns
        pattern_scores = self.score_patterns(analysis)
        logger.info(f"Scored {len(pattern_scores)} patterns")
        
        # Step 3: Generate recommendation
        recommendation = self.generate_recommendation(pattern_scores, analysis)
        logger.info(f"Recommended {recommendation.primary_pattern.value} with "
                   f"confidence {recommendation.confidence_score:.2f}")
        
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


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test cases
    test_requirements = [
        "I need to build a document search system that can find relevant information from a knowledge base",
        "Create an intelligent agent that can analyze customer requests and make decisions autonomously",
        "Build a system that integrates with external APIs and processes data from multiple sources",
        "I want a complex multi-step workflow that involves approval processes and notifications"
    ]
    
    analyzer = PatternAnalyzer()
    
    for req in test_requirements:
        print(f"\n{'='*60}")
        print(f"Requirement: {req}")
        print('='*60)
        
        recommendation = analyzer.analyze_and_recommend(req)
        
        print(f"Primary Pattern: {recommendation.primary_pattern.value}")
        print(f"Confidence: {recommendation.confidence_score:.2f}")
        print(f"Secondary Patterns: {[p.value for p in recommendation.secondary_patterns]}")
        print(f"Rationale: {recommendation.rationale}")
        print(f"Template Customizations: {recommendation.template_customizations}")
        print(f"Workflow Suggestions: {recommendation.workflow_suggestions}")
