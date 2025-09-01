#!/usr/bin/env python3
"""
PocketFlow Workflow Generator

Generates complete PocketFlow workflow implementations from design documents
and templates, following the 8-step Agentic Coding methodology.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, TYPE_CHECKING, Optional
from dataclasses import dataclass, field
import logging

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class WorkflowSpec:
    """Specification for generating a PocketFlow workflow."""

    name: str
    pattern: str  # AGENT/WORKFLOW/RAG/MAPREDUCE/MULTI-AGENT/STRUCTURED-OUTPUT
    description: str
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    utilities: List[Dict[str, Any]] = field(default_factory=list)
    shared_store_schema: Dict[str, Any] = field(default_factory=dict)
    api_endpoints: List[Dict[str, Any]] = field(default_factory=list)
    fast_api_integration: bool = True


if TYPE_CHECKING:
    # Import canonical types for type hints only (avoid runtime import coupling)
    try:
        from .pattern_analyzer import PatternRecommendation as AnalyzerPatternRecommendation, PatternType as AnalyzerPatternType  # type: ignore
    except Exception:  # pragma: no cover - typing only
        from pattern_analyzer import PatternRecommendation as AnalyzerPatternRecommendation, PatternType as AnalyzerPatternType  # type: ignore
    try:
        from .dependency_orchestrator import DependencyConfig as OrchestratorDependencyConfig  # type: ignore
    except Exception:  # pragma: no cover - typing only
        from dependency_orchestrator import DependencyConfig as OrchestratorDependencyConfig  # type: ignore
    try:
        from .template_validator import ValidationResult as ValidatorValidationResult  # type: ignore
    except Exception:  # pragma: no cover - typing only
        from template_validator import ValidationResult as ValidatorValidationResult  # type: ignore


logger = logging.getLogger(__name__)


class PocketFlowGenerator:
    """Generate complete PocketFlow workflows from specifications."""

    def __init__(
        self,
        templates_path: str = "templates",
        output_path: str = ".agent-os/workflows",
        enable_hybrid_promotion: bool = False,
    ):
        self.templates_path = Path(templates_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True)
        # Phase 3: optional hybrid composition (default off)
        self.enable_hybrid_promotion = enable_hybrid_promotion

        # Validate templates directory exists
        if not self.templates_path.exists():
            raise FileNotFoundError(
                f"Templates directory not found: {self.templates_path}"
            )
        if not self.templates_path.is_dir():
            raise NotADirectoryError(
                f"Templates path is not a directory: {self.templates_path}"
            )

        # Load templates
        self.templates = self._load_templates()
        
        # Load enhanced extensions for better template generation
        self.extensions = self._load_enhanced_extensions()

    def _load_templates(self) -> Dict[str, str]:
        """Load all template files."""
        templates = {}
        for template_file in self.templates_path.glob("*.md"):
            templates[template_file.stem] = template_file.read_text()
        return templates
    
    def _load_enhanced_extensions(self) -> Dict[str, Any]:
        """Load enhanced extensions for improved template generation."""
        extensions = {}
        
        # Path to enhanced extensions
        extensions_path = Path("instructions/extensions")
        
        if not extensions_path.exists():
            # Fallback for different relative paths
            extensions_path = Path("../instructions/extensions")
            if not extensions_path.exists():
                logging.warning("Enhanced extensions not found, using basic template generation")
                return {}
        
        try:
            # Load enhanced extensions with template extraction
            extension_files = {
                "design_enforcement": "design-first-enforcement.md",
                "llm_workflow": "llm-workflow-extension.md", 
                "pocketflow_integration": "pocketflow-integration.md"
            }
            
            for key, filename in extension_files.items():
                ext_file = extensions_path / filename
                if ext_file.exists():
                    content = ext_file.read_text()
                    extensions[key] = self._parse_extension_templates(content)
                else:
                    logging.warning(f"Extension not found: {filename}")
            
        except Exception as e:
            logging.warning(f"Failed to load enhanced extensions: {e}")
            return {}
        
        return extensions
    
    def _parse_extension_templates(self, content: str) -> Dict[str, Any]:
        """Parse extension content to extract template guidance."""
        import re
        
        templates = {
            "code_templates": [],
            "todo_guidance": [],
            "orchestrator_integration": []
        }
        
        # Extract code templates (content between ```python or ```bash)
        code_blocks = re.findall(r'```(?:python|bash)\n(.*?)```', content, re.DOTALL)
        templates["code_templates"] = code_blocks
        
        # Extract TODO guidance lines
        todo_lines = re.findall(r'#.*TODO:.*', content)
        templates["todo_guidance"] = todo_lines
        
        # Extract orchestrator integration examples
        orchestrator_matches = re.findall(r'claude-code.*orchestrator[^\n]*', content)
        templates["orchestrator_integration"] = orchestrator_matches
        
        return templates
    
    def generate_spec_from_analysis(self, name: str, description: str, recommendation: "AnalyzerPatternRecommendation") -> WorkflowSpec:
        """Generate a WorkflowSpec from pattern analysis recommendation."""
        
        # Adapter: support enum-based PatternType or raw strings
        def _pattern_str(p: Any) -> str:
            return getattr(p, "value", p)

        # Extract suggested nodes and structure recommendations
        suggested_utilities = recommendation.template_customizations.get("suggested_utilities", [])
        # Start with analyzer-provided workflow suggestions (copy to avoid mutation)
        workflow_suggestions = dict(getattr(recommendation, 'workflow_suggestions', {}) or {})
        # Phase 2: honor simple structure recommendations from analyzer customizations
        try:
            tc = getattr(recommendation, 'template_customizations', {}) or {}
            if isinstance(tc, dict):
                # Prefer explicit graduated_structure if present
                if tc.get("graduated_structure"):
                    workflow_suggestions.setdefault("recommended_structure", tc["graduated_structure"])
                # Also pass through full complexity mapping for downstream use if available
                if isinstance(tc.get("complexity_mapping"), dict):
                    workflow_suggestions.setdefault("complexity_mapping", tc["complexity_mapping"])
        except Exception:
            # Defensive: never block generation if metadata missing/malformed
            pass

        # Phase 3: If hybrid promotion is enabled and combinations detected, prepare override nodes
        try:
            if self.enable_hybrid_promotion:
                combo_info = (getattr(recommendation, 'template_customizations', {}) or {}).get('combination_info', {})
                if isinstance(combo_info, dict) and combo_info:
                    # Skip hybrid override if a simple structure is explicitly recommended
                    simple_set = {"SIMPLE_WORKFLOW", "BASIC_API", "SIMPLE_ETL"}
                    recommended_simple = workflow_suggestions.get("recommended_structure") or (
                        (workflow_suggestions.get("complexity_mapping") or {}).get("recommended_structure")
                        if isinstance(workflow_suggestions.get("complexity_mapping"), dict)
                        else None
                    )
                    if recommended_simple not in simple_set:
                        # Choose combination with highest combined_score
                        best = None
                        for k, v in combo_info.items():
                            if not best or float(v.get('combined_score', 0)) > float(best.get('combined_score', 0)):
                                best = v
                        if best and isinstance(best.get('patterns'), list):
                            try:
                                try:
                                    from .pattern_analyzer import PatternType as AnalyzerPatternType  # type: ignore
                                except Exception:
                                    from pattern_analyzer import PatternType as AnalyzerPatternType  # type: ignore
                                try:
                                    try:
                                        from .pattern_definitions import compose_hybrid_node_templates  # type: ignore
                                    except Exception:
                                        from pattern_definitions import compose_hybrid_node_templates  # type: ignore
                                    base_patterns = []
                                    for p in best['patterns']:
                                        try:
                                            base_patterns.append(AnalyzerPatternType(p))
                                        except Exception:
                                            pass
                                    if base_patterns:
                                        workflow_suggestions['override_node_templates'] = compose_hybrid_node_templates(base_patterns)
                                except Exception:
                                    pass
                            except Exception:
                                pass
        except Exception:
            pass
        
        # Generate nodes based on pattern and suggestions
        nodes = self._generate_nodes_from_pattern(
            _pattern_str(recommendation.primary_pattern), 
            workflow_suggestions
        )
        
        # Generate utilities; align with simple structures when recommended (Phase 2)
        try:
            simple_set = {"SIMPLE_WORKFLOW", "BASIC_API", "SIMPLE_ETL"}
            recommended_simple = None
            if isinstance(workflow_suggestions, dict):
                recommended_simple = workflow_suggestions.get("recommended_structure")
                if not recommended_simple:
                    cm = workflow_suggestions.get("complexity_mapping", {}) or {}
                    if isinstance(cm, dict):
                        recommended_simple = cm.get("recommended_structure")
            effective_pattern_for_utils = (
                recommended_simple if recommended_simple in simple_set else _pattern_str(recommendation.primary_pattern)
            )
        except Exception:
            effective_pattern_for_utils = _pattern_str(recommendation.primary_pattern)

        utilities = self._generate_utilities_from_pattern(
            effective_pattern_for_utils,
            suggested_utilities
        )
        
        # Generate shared store schema based on pattern
        shared_store_schema = self._generate_shared_store_from_pattern(
            _pattern_str(recommendation.primary_pattern)
        )
        
        # Always enable FastAPI integration as part of universal PocketFlow architecture
        fast_api_integration = True
        
        # Generate API endpoints for all workflows
        api_endpoints = [{
                "name": "Process",
                "method": "post",
                "path": "/process",
                "description": f"Execute {name} workflow",
                "request_fields": [
                    {"name": "input_data", "type": "str"},
                    {"name": "options", "type": "Optional[Dict[str, Any]]"}
                ],
                "response_fields": [
                    {"name": "result", "type": "Dict[str, Any]"},
                    {"name": "status", "type": "str"},
                    {"name": "processing_time", "type": "float"}
                ]
            }]
        
        return WorkflowSpec(
            name=name,
            pattern=_pattern_str(recommendation.primary_pattern),
            description=description,
            nodes=nodes,
            utilities=utilities,
            shared_store_schema=shared_store_schema,
            api_endpoints=api_endpoints,
            fast_api_integration=fast_api_integration
        )
        
    def _generate_nodes_from_pattern(self, pattern: str, workflow_suggestions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate node specifications based on pattern type with enhanced extension guidance.

        Centralized: imports canonical node templates from `pattern_definitions`.
        """
        # Import centrally defined pattern nodes (relative then absolute fallback)
        try:  # type: ignore
            from .pattern_definitions import get_node_templates  # type: ignore
        except Exception:  # pragma: no cover - fallback for standalone usage
            from pattern_definitions import get_node_templates  # type: ignore

        # Allow override hybrid nodes first (Phase 3)
        default_nodes = None
        if isinstance(workflow_suggestions, dict):
            override = workflow_suggestions.get("override_node_templates")
            if isinstance(override, list) and override:
                default_nodes = override
        if default_nodes is None:
            # Determine if a simple structure was recommended (Phase 2)
            recommended = None
            try:
                if isinstance(workflow_suggestions, dict):
                    recommended = workflow_suggestions.get("recommended_structure")
                    if not recommended:
                        # Optional: support nested complexity mapping source
                        cm = workflow_suggestions.get("complexity_mapping", {}) or {}
                        if isinstance(cm, dict):
                            recommended = cm.get("recommended_structure")
            except Exception:
                recommended = None

            # Get nodes honoring simple structures when recommended
            if recommended in {"SIMPLE_WORKFLOW", "BASIC_API", "SIMPLE_ETL"}:
                default_nodes = get_node_templates(recommended)
            else:
                # Fall back to canonical nodes for the primary pattern
                default_nodes = get_node_templates(pattern)
        
        # Customize based on workflow suggestions if available
        if workflow_suggestions:
            # Override nodes if specific suggestions are provided
            for node_type in ["preprocessing_nodes", "retrieval_nodes", "generation_nodes", 
                             "planning_nodes", "execution_nodes", "reflection_nodes",
                             "integration_nodes", "transformation_nodes", "validation_nodes"]:
                if node_type in workflow_suggestions:
                    suggested_names = workflow_suggestions[node_type]
                    # Replace relevant nodes with suggested ones
                    for i, node_name in enumerate(suggested_names[:len(default_nodes)]):
                        if i < len(default_nodes):
                            default_nodes[i]["name"] = "".join(word.capitalize() for word in node_name.split("_"))
                            default_nodes[i]["description"] = f"Handle {node_name.replace('_', ' ')} operations"
        
        # Enhance nodes with extension guidance for better TODO templates
        enhanced_nodes = self._enhance_nodes_with_extensions(default_nodes, pattern)
        
        return enhanced_nodes
    
    def _enhance_nodes_with_extensions(self, nodes: List[Dict[str, Any]], pattern: str) -> List[Dict[str, Any]]:
        """Enhance node specifications with guidance from enhanced extensions."""
        if not self.extensions:
            return nodes
        
        # Add enhanced TODO guidance and orchestrator integration
        for node in nodes:
            # Add pattern-specific TODO guidance
            if pattern == "RAG" and "llm_workflow" in self.extensions:
                node["enhanced_todos"] = [
                    "TODO: Implement vector similarity search for document retrieval",
                    "TODO: Add context window management for large documents", 
                    "TODO: Integrate with your preferred embedding model (OpenAI, Anthropic, etc.)",
                    "TODO: Add error handling for retrieval failures",
                    "TODO: Implement caching for frequently accessed documents"
                ]
            elif pattern == "AGENT" and "llm_workflow" in self.extensions:
                node["enhanced_todos"] = [
                    "TODO: Implement decision-making algorithm based on input context",
                    "TODO: Add state management for agent memory and learning",
                    "TODO: Integrate with LLM for dynamic reasoning capabilities",
                    "TODO: Add action validation and safety constraints",
                    "TODO: Implement feedback loop for continuous improvement"
                ]
            else:
                # Generic enhanced TODO guidance
                node["enhanced_todos"] = [
                    f"TODO: Implement {node['name']} logic for {pattern} pattern",
                    "TODO: Add comprehensive error handling and logging",
                    "TODO: Add input validation and sanitization",  
                    "TODO: Implement proper async/await patterns if needed",
                    "TODO: Add metrics and monitoring for production use"
                ]
            
            # Add orchestrator integration guidance
            if "pocketflow_integration" in self.extensions:
                orchestrator_examples = self.extensions["pocketflow_integration"].get("orchestrator_integration", [])
                if orchestrator_examples:
                    node["orchestrator_guidance"] = [
                        "# Template Validator Integration Example:",
                        "# claude-code agent invoke template-validator --task validate-node --node " + node['name'],
                        "# Use this to validate node implementation during development"
                    ]
            
            # Add framework boundary reminders
            node["framework_reminders"] = [
                "# NOTE: This is template code for end-user projects",
                "# TODO: Customize this implementation for your specific use case",
                "# TODO: Replace placeholder logic with actual business logic",
                "# TODO: Add proper error handling and logging for production"
            ]
        
        return nodes
    
    def _get_enhanced_todos_for_node(self, node: Dict[str, Any]) -> List[str]:
        """Extract enhanced TODO guidance from node specification."""
        return node.get("enhanced_todos", [])
    
    def _get_orchestrator_guidance_for_node(self, node: Dict[str, Any]) -> List[str]:
        """Extract orchestrator guidance from node specification."""
        return node.get("orchestrator_guidance", [])
    
    def _get_framework_reminders_for_node(self, node: Dict[str, Any]) -> List[str]:
        """Extract framework boundary reminders from node specification.""" 
        return node.get("framework_reminders", [])
    
    def _generate_utilities_from_pattern(self, pattern: str, suggested_utilities: List[str]) -> List[Dict[str, Any]]:
        """Generate utility function specifications based on pattern."""
        
        pattern_utility_templates = {
            # Simple Pattern Utilities (Task 1.2 Implementation)
            "SIMPLE_WORKFLOW": [
                {
                    "name": "flow_controller",
                    "description": "Control flow between workflow steps",
                    "parameters": [
                        {"name": "current_step", "type": "str"},
                        {"name": "input_data", "type": "Dict[str, Any]"}
                    ],
                    "return_type": "Dict[str, Any]"
                },
                {
                    "name": "state_manager",
                    "description": "Manage workflow state and data",
                    "parameters": [
                        {"name": "state_data", "type": "Dict[str, Any]"},
                        {"name": "operation", "type": "str"}
                    ],
                    "return_type": "Dict[str, Any]"
                }
            ],
            "BASIC_API": [
                {
                    "name": "request_parser",
                    "description": "Parse and validate API requests",
                    "parameters": [
                        {"name": "request_data", "type": "Dict[str, Any]"},
                        {"name": "schema", "type": "Dict[str, Any]", "optional": True}
                    ],
                    "return_type": "Dict[str, Any]"
                },
                {
                    "name": "response_formatter",
                    "description": "Format API responses consistently",
                    "parameters": [
                        {"name": "data", "type": "Any"},
                        {"name": "status_code", "type": "int", "optional": True}
                    ],
                    "return_type": "Dict[str, Any]"
                }
            ],
            "SIMPLE_ETL": [
                {
                    "name": "data_validator",
                    "description": "Validate data quality and format",
                    "parameters": [
                        {"name": "data", "type": "Any"},
                        {"name": "validation_rules", "type": "Dict[str, Any]"}
                    ],
                    "return_type": "Dict[str, Any]"
                },
                {
                    "name": "batch_processor",
                    "description": "Process data in configurable batches",
                    "parameters": [
                        {"name": "data_source", "type": "Any"},
                        {"name": "batch_size", "type": "int", "optional": True}
                    ],
                    "return_type": "List[Any]",
                    "async": True
                }
            ],
            
            # Enhanced Pattern Utilities
            "RAG": [
                {
                    "name": "vector_search",
                    "description": "Search vectors using similarity matching",
                    "parameters": [
                        {"name": "query_vector", "type": "List[float]"},
                        {"name": "top_k", "type": "int", "optional": True}
                    ],
                    "return_type": "List[Dict[str, Any]]",
                    "async": True
                },
                {
                    "name": "document_processor", 
                    "description": "Process documents into chunks with embeddings",
                    "parameters": [
                        {"name": "documents", "type": "List[str]"},
                        {"name": "chunk_size", "type": "int", "optional": True}
                    ],
                    "return_type": "List[Dict[str, Any]]",
                    "async": True
                }
            ],
            "AGENT": [
                {
                    "name": "llm_client",
                    "description": "Interface with LLM for reasoning and generation", 
                    "parameters": [
                        {"name": "prompt", "type": "str"},
                        {"name": "model_config", "type": "Dict[str, Any]", "optional": True}
                    ],
                    "return_type": "str",
                    "async": True
                },
                {
                    "name": "reasoning_engine",
                    "description": "Apply structured reasoning to problems",
                    "parameters": [
                        {"name": "context", "type": "Dict[str, Any]"},
                        {"name": "reasoning_type", "type": "str", "optional": True}
                    ],
                    "return_type": "Dict[str, Any]",
                    "async": True
                }
            ],
            "TOOL": [
                {
                    "name": "api_client",
                    "description": "Generic HTTP client for external API calls",
                    "parameters": [
                        {"name": "endpoint", "type": "str"},
                        {"name": "method", "type": "str"}, 
                        {"name": "data", "type": "Dict[str, Any]", "optional": True}
                    ],
                    "return_type": "Dict[str, Any]",
                    "async": True
                },
                {
                    "name": "data_transformer",
                    "description": "Transform data between different formats",
                    "parameters": [
                        {"name": "data", "type": "Any"},
                        {"name": "target_format", "type": "str"}
                    ],
                    "return_type": "Any"
                }
            ]
        }
        
        # Start with pattern-specific utilities
        utilities = pattern_utility_templates.get(pattern, [])
        
        # Add utilities based on suggestions
        for suggestion in suggested_utilities:
            if not any(util["name"] == suggestion for util in utilities):
                utilities.append({
                    "name": suggestion,
                    "description": f"Utility function for {suggestion.replace('_', ' ')}",
                    "parameters": [{"name": "input_data", "type": "Any"}],
                    "return_type": "Any",
                    "async": True if "client" in suggestion or "api" in suggestion else False
                })
        
        return utilities
    
    def _generate_shared_store_from_pattern(self, pattern: str) -> Dict[str, str]:
        """Generate shared store schema based on pattern."""
        
        pattern_schemas = {
            "RAG": {
                "query": "str",
                "documents": "List[Dict[str, Any]]",
                "embeddings": "List[List[float]]",
                "retrieved_docs": "List[Dict[str, Any]]",
                "context": "str",
                "generated_response": "str",
                "metadata": "Dict[str, Any]"
            },
            "AGENT": {
                "task": "str",
                "plan": "List[Dict[str, Any]]",
                "current_state": "Dict[str, Any]",
                "reasoning_history": "List[str]",
                "actions_taken": "List[Dict[str, Any]]",
                "result": "Dict[str, Any]",
                "confidence": "float"
            },
            "TOOL": {
                "input_data": "Dict[str, Any]",
                "processed_data": "Dict[str, Any]",
                "api_responses": "List[Dict[str, Any]]",
                "transformed_data": "Dict[str, Any]",
                "final_result": "Dict[str, Any]",
                "error_info": "Optional[str]"
            },
            "WORKFLOW": {
                "input_data": "Any",
                "processing_state": "Dict[str, Any]", 
                "intermediate_results": "List[Any]",
                "output_data": "Any",
                "metadata": "Dict[str, Any]"
            }
        }
        
        return pattern_schemas.get(pattern, pattern_schemas["WORKFLOW"])

    def generate_workflow_from_requirements(self, name: str, requirements: str) -> Dict[str, str]:
        """Generate complete workflow from natural language requirements using pattern analysis."""
        
        # Step 1: Analyze requirements to determine optimal pattern
        print(f"Analyzing requirements for pattern recognition...")
        recommendation = self.request_pattern_analysis(requirements, project_name=name)
        
        print(f"Pattern Analysis Results:")
        # Adapter: enum-safe pattern display
        primary_pattern_str = getattr(recommendation.primary_pattern, "value", recommendation.primary_pattern)
        print(f"   Primary Pattern: {primary_pattern_str}")
        print(f"   Confidence: {recommendation.confidence_score:.2f}")
        print(f"   Rationale: {recommendation.rationale}")
        
        if recommendation.secondary_patterns:
            alt_patterns = [getattr(p, "value", p) for p in recommendation.secondary_patterns]
            print(f"   Alternative Patterns: {', '.join(alt_patterns)}")
        
        # Step 2: Generate WorkflowSpec from analysis
        print(f"Generating workflow specification...")
        spec = self.generate_spec_from_analysis(name, requirements, recommendation)
        
        print(f"Generated Specification:")
        print(f"   Nodes: {len(spec.nodes)}")
        print(f"   Utilities: {len(spec.utilities)}")
        print(f"   FastAPI Integration: Enabled (Universal)")
        
        # Step 3: Generate workflow files
        print(f"Generating workflow implementation...")
        workflow_files = self.generate_workflow(spec)
        
        # Step 4: Add pattern analysis to design document
        self._enhance_design_with_pattern_analysis(workflow_files, recommendation, spec)
        
        return workflow_files
    
    def _enhance_design_with_pattern_analysis(self, workflow_files: Dict[str, str], 
                                           recommendation: "AnalyzerPatternRecommendation", 
                                           spec: WorkflowSpec) -> None:
        """Enhance the design document with pattern analysis details."""
        
        if "docs/design.md" in workflow_files:
            design_content = workflow_files["docs/design.md"]
            
            # Generate workflow graph
            try:
                # Import graph generator and analyzer types with relative-then-absolute fallback
                try:
                    from .workflow_graph_generator import WorkflowGraphGenerator  # type: ignore
                except ImportError:
                    from workflow_graph_generator import WorkflowGraphGenerator
                try:
                    from .pattern_analyzer import PatternType as AnalyzerPatternType  # type: ignore
                except ImportError:
                    from pattern_analyzer import PatternType as AnalyzerPatternType
                
                # If a simple structure was recommended, reflect actual nodes using basic Mermaid
                simple_set = {"SIMPLE_WORKFLOW", "BASIC_API", "SIMPLE_ETL"}
                recommended_simple = (
                    recommendation.template_customizations.get("graduated_structure")
                    or recommendation.template_customizations.get("complexity_mapping", {}).get("recommended_structure")
                )

                if recommended_simple in simple_set:
                    mermaid_diagram = self._generate_basic_mermaid(spec)
                    workflow_description = f"Simple structure ({recommended_simple}) selected; diagram reflects generated nodes."
                else:
                    # Hybrid composition path (Phase 3) if enabled and available
                    combo = (recommendation.template_customizations or {}).get('combination_info', {})
                    if self.enable_hybrid_promotion and isinstance(combo, dict) and combo:
                        # Select best combo by combined_score
                        best = None
                        for k, v in combo.items():
                            if not best or float(v.get('combined_score', 0)) > float(best.get('combined_score', 0)):
                                best = v
                        if best and isinstance(best.get('patterns'), list):
                            try:
                                base = []
                                for p in best['patterns']:
                                    try:
                                        base.append(AnalyzerPatternType(p))
                                    except Exception:
                                        pass
                                if base:
                                    graph_generator = WorkflowGraphGenerator()
                                    workflow_graph = graph_generator.generate_hybrid_graph(base, complexity_level="medium")
                                    mermaid_diagram = graph_generator.generate_mermaid_diagram(workflow_graph)
                                    workflow_description = graph_generator.generate_workflow_description(workflow_graph)
                                else:
                                    raise ValueError("No valid base patterns for hybrid graph")
                            except Exception:
                                # Fallback to standard single-pattern graph
                                pattern_value = getattr(
                                    recommendation.primary_pattern, "value", recommendation.primary_pattern
                                )
                                pattern_enum = AnalyzerPatternType(pattern_value)
                                graph_generator = WorkflowGraphGenerator()
                                workflow_graph = graph_generator.generate_workflow_graph(pattern_enum, complexity_level="medium")
                                mermaid_diagram = graph_generator.generate_mermaid_diagram(workflow_graph)
                                workflow_description = graph_generator.generate_workflow_description(workflow_graph)
                    else:
                        # Standard single-pattern graph
                        pattern_value = getattr(
                            recommendation.primary_pattern, "value", recommendation.primary_pattern
                        )
                        pattern_enum = AnalyzerPatternType(pattern_value)
                        graph_generator = WorkflowGraphGenerator()
                        workflow_graph = graph_generator.generate_workflow_graph(pattern_enum, complexity_level="medium")
                        mermaid_diagram = graph_generator.generate_mermaid_diagram(workflow_graph)
                        workflow_description = graph_generator.generate_workflow_description(workflow_graph)
                
            except ImportError:
                mermaid_diagram = self._generate_basic_mermaid(spec)
                workflow_description = "Workflow graph generator not available."
            except Exception as e:
                mermaid_diagram = self._generate_basic_mermaid(spec)
                workflow_description = f"Graph generation failed: {str(e)}"
            
            # Add pattern analysis section after the pattern classification
            # Use detailed justification if available, otherwise fall back to brief rationale
            detailed_analysis = getattr(recommendation, 'detailed_justification', '') or recommendation.rationale
            
            pattern_analysis_section = f"""

### Pattern Analysis Results

**Analysis Confidence:** {recommendation.confidence_score:.1%}

#### Detailed Pattern Justification

{detailed_analysis}

#### Template Customizations Applied
{self._format_customizations_for_doc(recommendation.template_customizations)}

#### Generated Architecture
- **Nodes Generated:** {len(spec.nodes)} specialized processing nodes
- **Utilities Generated:** {len(spec.utilities)} pattern-specific utility functions
- **API Integration:** Enabled (Universal PocketFlow)
- **Shared Store Schema:** Optimized for {getattr(recommendation.primary_pattern, 'value', recommendation.primary_pattern)} pattern workflows

### Workflow Graph

{mermaid_diagram}

### Workflow Analysis

{workflow_description[:500] + ('...' if len(workflow_description) > 500 else '')}"""

            # Insert after the pattern classification section
            if "### Design Pattern Classification" in design_content:
                parts = design_content.split("### Input/Output Specification", 1)
                if len(parts) == 2:
                    workflow_files["docs/design.md"] = (
                        parts[0] + pattern_analysis_section + "\n\n### Input/Output Specification" + parts[1]
                    )
    
    def _generate_basic_mermaid(self, spec: WorkflowSpec) -> str:
        """Generate a basic Mermaid diagram as fallback."""
        lines = [
            "```mermaid",
            "graph TD",
            "    A[Start] --> B[Input Validation]"
        ]
        
        # Add nodes
        prev_node = "B"
        for i, node in enumerate(spec.nodes):
            node_id = chr(ord("C") + i)
            lines.append(f"    {prev_node} --> {node_id}[{node['name']}]")
            prev_node = node_id
        
        lines.append(f"    {prev_node} --> Z[End]")
        lines.append("```")
        
        return "\n".join(lines)
    
    def _format_customizations_for_doc(self, customizations: Dict[str, Any]) -> str:
        """Format customizations for documentation."""
        if not customizations:
            return "- No specific customizations applied"
        
        formatted = []
        for key, value in customizations.items():
            formatted.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        
        return "\n".join(formatted)

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        """Generate complete workflow implementation from spec."""
        output_files = {}

        # Generate design document
        output_files["docs/design.md"] = self._generate_design_doc(spec)

        # Generate data models
        output_files["schemas/models.py"] = self._generate_pydantic_models(spec)

        # Generate utility functions
        for utility in spec.utilities:
            file_path = f"utils/{utility['name']}.py"
            output_files[file_path] = self._generate_utility(utility)

        # Generate nodes
        output_files["nodes.py"] = self._generate_nodes(spec)

        # Generate flow
        output_files["flow.py"] = self._generate_flow(spec)

        # Generate FastAPI integration for all workflows
        output_files["main.py"] = self._generate_fastapi_main(spec)
        output_files["router.py"] = self._generate_fastapi_router(spec)

        # Generate tests
        output_files["tests/test_nodes.py"] = self._generate_node_tests(spec)
        output_files["tests/test_flow.py"] = self._generate_flow_tests(spec)
        output_files["tests/test_api.py"] = self._generate_api_tests(spec)

        # Generate tasks file
        output_files["tasks.md"] = self._generate_tasks(spec)
        
        # Generate installation checker reference
        output_files["check-install.py"] = self._generate_install_checker_reference()
        
        # Generate dependency configuration files
        dependency_files = self._generate_dependency_files(spec)
        output_files.update(dependency_files)
        
        # Generate package initialization files
        output_files["__init__.py"] = self._generate_init_file(spec, is_root=True)
        output_files["tests/__init__.py"] = self._generate_init_file(spec, is_test=True)
        output_files["schemas/__init__.py"] = self._generate_init_file(spec, is_schema=True)
        output_files["utils/__init__.py"] = self._generate_init_file(spec, is_utils=True)
        output_files["docs/__init__.py"] = ""  # Empty init for docs

        return output_files

    def _generate_init_file(self, spec: WorkflowSpec, is_root=False, is_test=False, is_schema=False, is_utils=False) -> str:
        """Generate appropriate __init__.py file content."""
        # workflow_name = spec.name.lower().replace(" ", "")  # Currently unused
        
        if is_root:
            # Root package init - expose main classes
            return f'''"""
{spec.name} - PocketFlow Workflow

{spec.description}

Generated by Agent OS + PocketFlow Generator
"""

from .flow import {spec.name}Flow
from .nodes import {", ".join(node["name"] for node in spec.nodes)}

__version__ = "0.1.0"
__all__ = [
    "{spec.name}Flow",
    {", ".join(f'"{node["name"]}"' for node in spec.nodes)}
]
'''
        elif is_test:
            # Test package init
            return f'''"""
Test package for {spec.name} workflow.
"""
'''
        elif is_schema:
            # Schema package init
            return f'''"""
Pydantic models and schemas for {spec.name} workflow.
"""

from .models import *
'''
        elif is_utils:
            # Utils package init  
            return f'''"""
Utility functions for {spec.name} workflow.
"""

# Import all utility functions
from pathlib import Path
import importlib

_utils_dir = Path(__file__).parent
for util_file in _utils_dir.glob("*.py"):
    if util_file.name not in ["__init__.py"]:
        module_name = util_file.stem
        try:
            importlib.import_module(f".{{module_name}}", package=__name__)
        except ImportError:
            pass  # Skip utility files with missing dependencies
'''
        else:
            # Default empty init
            return ""

    def _generate_install_checker_reference(self) -> str:
        """Generate a reference script that points to the main installation checker."""
        return '''#!/usr/bin/env python3
"""
PocketFlow Installation Checker

This script checks if your project has the necessary dependencies
to run PocketFlow workflows.

Usage:
    python check-install.py [--install]
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run the main installation checker."""
    # Path to the main checker in Agent OS
    agent_os_checker = Path.home() / ".agent-os" / "pocketflow-tools" / "check-pocketflow-install.py"
    
    if not agent_os_checker.exists():
        print("❌ Agent OS + PocketFlow installation checker not found.")
        print("   Please ensure Agent OS is properly installed in ~/.agent-os/")
        return 1
    
    # Forward all arguments to the main checker
    cmd = [sys.executable, str(agent_os_checker)] + sys.argv[1:]
    return subprocess.run(cmd).returncode

if __name__ == "__main__":
    sys.exit(main())
'''

    def _generate_dependency_files(self, spec: WorkflowSpec) -> Dict[str, str]:
        """Generate dependency configuration files using dependency orchestrator."""
        files = {}
        
        try:
            from .dependency_orchestrator import DependencyOrchestrator
            
            orchestrator = DependencyOrchestrator()
            project_name = spec.name.lower().replace(" ", "-")
            
            # Generate pyproject.toml
            files["pyproject.toml"] = orchestrator.generate_pyproject_toml(
                project_name, 
                spec.pattern,
                spec.description
            )
            
            # Generate UV configuration files
            uv_files = orchestrator.generate_uv_config(project_name, spec.pattern)
            files.update(uv_files)
            
            # Generate requirements files for easier manual management
            config = orchestrator.generate_config_for_pattern(spec.pattern)
            
            # requirements.txt (runtime dependencies)
            runtime_deps = list(set(config.base_dependencies + config.pattern_dependencies))
            files["requirements.txt"] = "\n".join(sorted(runtime_deps)) + "\n"
            
            # requirements-dev.txt (development dependencies)
            files["requirements-dev.txt"] = "\n".join(sorted(config.dev_dependencies)) + "\n"
            
            # .gitignore optimized for Python projects
            files[".gitignore"] = self._generate_gitignore()
            
            # README.md with dependency setup instructions
            files["README.md"] = self._generate_readme(spec, config)
            
        except Exception as e:
            logger.warning(f"Failed to generate dependency files: {e}")
            # Fallback to basic files
            files["pyproject.toml"] = self._generate_basic_pyproject(spec)
            files["requirements.txt"] = "pocketflow\npydantic>=2.0\nfastapi>=0.104.0\n"
            files["requirements-dev.txt"] = "pytest>=7.0.0\nruff>=0.1.0\n"
            files[".gitignore"] = self._generate_gitignore()
            files["README.md"] = self._generate_basic_readme(spec)
        
        return files
    
    def _generate_gitignore(self) -> str:
        """Generate .gitignore file for Python projects."""
        return '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
*.log
temp/
tmp/
'''

    def _generate_readme(self, spec: WorkflowSpec, config: Any) -> str:
        """Generate README.md with setup instructions."""
        project_name = spec.name.lower().replace(" ", "-")
        
        return f'''# {spec.name}

{spec.description}

## Overview

This is a PocketFlow {spec.pattern} pattern implementation generated by Agent OS + PocketFlow Framework.

## Setup

### Prerequisites

- Python {config.python_version}
- UV package manager (recommended) or pip

### Installation with UV (Recommended)

```bash
# Install dependencies
uv sync

# Activate virtual environment
uv shell

# Install development dependencies
uv sync --dev
```

### Installation with pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## Development

### Running Tests

```bash
# With UV
uv run pytest

# With pip
pytest
```

### Code Quality

```bash
# Linting and formatting
uv run ruff check --fix .
uv run ruff format .

# Type checking
uv run ty check
```

### Running the Application

```bash
# Development server (FastAPI enabled for all workflows)
uv run uvicorn main:app --reload

# Or run the flow directly
uv run python -c "from flow import {spec.name}Flow; import asyncio; flow = {spec.name}Flow(); asyncio.run(flow.run_async({{}}))"
```

## Architecture

### Pattern: {spec.pattern}

This workflow implements the {spec.pattern} pattern with the following components:

#### Nodes
{chr(10).join(f'- **{node["name"]}**: {node["description"]}' for node in spec.nodes)}

#### Utilities
{chr(10).join(f'- **{util["name"]}**: {util["description"]}' for util in spec.utilities)}

### FastAPI Integration

✅ Enabled - API endpoints available at `/api/v1/`

## Project Structure

```
{project_name}/
├── pyproject.toml          # Project configuration and dependencies
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── docs/
│   └── design.md          # Detailed design document
├── schemas/
│   └── models.py          # Pydantic models
├── utils/                 # Utility functions
├── nodes.py               # PocketFlow nodes
├── flow.py                # Main workflow
├── tests/                 # Test files
├── main.py               # FastAPI application
└── router.py             # API routes
```

## Next Steps

1. **Review Design**: Check `docs/design.md` for complete specifications
2. **Implement Utilities**: Complete functions in `utils/` directory
3. **Implement Nodes**: Complete business logic in `nodes.py`
4. **Test**: Run tests and ensure all pass
5. **Deploy**: Follow your deployment process

## Generated Files

This project was generated by Agent OS + PocketFlow Framework. Key files to customize:

- **`utils/*.py`**: Implement your utility functions
- **`nodes.py`**: Complete node implementations
- **`docs/design.md`**: Review and complete design specifications

## Support

For questions about PocketFlow patterns and implementation:
- Check the design document: `docs/design.md`
- Review PocketFlow documentation
- Check Agent OS documentation

Generated on: {datetime.now().isoformat()[:10]}
'''

    def _generate_basic_pyproject(self, spec: WorkflowSpec) -> str:
        """Generate basic pyproject.toml as fallback."""
        project_name = spec.name.lower().replace(" ", "-")
        
        return f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "{spec.description}"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pocketflow",
    "pydantic>=2.0",
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "ty>=0.5.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
'''

    def _generate_basic_readme(self, spec: WorkflowSpec) -> str:
        """Generate basic README.md as fallback."""
        project_name = spec.name.lower().replace(" ", "-")
        
        return f'''# {spec.name}

{spec.description}

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

Pattern: {spec.pattern}
Generated: {datetime.now().isoformat()[:10]}
'''

    def _generate_design_doc(self, spec: WorkflowSpec) -> str:
        """Generate design document from template."""
        # Create a comprehensive design document
        design_doc = f"""# Design Document

> Spec: {spec.name}
> Created: {datetime.now().isoformat()[:10]}
> Status: Design Phase
> Framework: PocketFlow

**CRITICAL**: This design document MUST be completed before any code implementation begins.

## Requirements

### Problem Statement
{spec.description}

### Success Criteria
- Successful implementation of {spec.pattern} pattern
- All nodes execute correctly in sequence
- Proper error handling and validation
- Complete test coverage

### Design Pattern Classification
**Primary Pattern:** {spec.pattern}
**Secondary Patterns:** FastAPI Integration (Universal)

### Input/Output Specification
- **Input Format:** Request data from API or direct invocation
- **Output Format:** Processed results with metadata
- **Error Conditions:** Validation errors, processing failures, timeout errors

## Flow Design

### High-Level Architecture
```mermaid
graph TD
    A[Start] --> B[Input Validation]
    B --> C[{spec.nodes[0]["name"] if spec.nodes else "Processing"}]"""

        # Add nodes to mermaid diagram
        if spec.nodes:
            for i, node in enumerate(spec.nodes):
                current = chr(ord("C") + i)
                next_node = chr(ord("C") + i + 1) if i < len(spec.nodes) - 1 else "Z"
                design_doc += f"\n    {current}[{node['name']}] --> {next_node}[{'Next Node' if i < len(spec.nodes) - 1 else 'End'}]"

        design_doc += "\n```\n"

        # Add node sequence
        design_doc += "\n### Node Sequence\n"
        for i, node in enumerate(spec.nodes, 1):
            design_doc += f"{i}. **{node['name']}** - {node['description']}\n"

        # Add utilities section
        design_doc += "\n## Utilities\n\n"
        design_doc += 'Following PocketFlow\'s "implement your own" philosophy, specify all utility functions needed.\n\n'
        design_doc += "### Required Utility Functions\n\n"

        for utility in spec.utilities:
            design_doc += f"#### {utility['name']}\n"
            design_doc += f"- **Purpose:** {utility['description']}\n"
            params_str = ", ".join(
                [f"{p['name']}: {p['type']}" for p in utility.get("parameters", [])]
            )
            design_doc += f"- **Input:** {params_str}\n"
            design_doc += f"- **Output:** {utility.get('return_type', 'Any')}\n\n"

        # Add shared store schema
        design_doc += "\n## Data Design\n\n"
        design_doc += "### SharedStore Schema\n"
        design_doc += "Following PocketFlow's shared store pattern, all data flows through a common dictionary.\n\n"
        design_doc += "```python\n"
        design_doc += "SharedStore = {\n"
        for key, value_type in spec.shared_store_schema.items():
            design_doc += f'    "{key}": {value_type},\n'
        design_doc += "}\n```\n"

        # Add node design section
        design_doc += "\n## Node Design\n\n"
        design_doc += "Following PocketFlow's node-based architecture, each processing step is implemented as a discrete node.\n\n"
        
        for i, node in enumerate(spec.nodes, 1):
            design_doc += f"### {i}. {node['name']}\n"
            design_doc += f"**Purpose:** {node['description']}\n\n"
            
            # Add input/output details if available
            if 'inputs' in node:
                inputs_str = ", ".join(node['inputs']) if node['inputs'] else "SharedStore"
                design_doc += f"**Inputs:** {inputs_str}\n"
            else:
                design_doc += "**Inputs:** SharedStore\n"
                
            if 'outputs' in node:
                outputs_str = ", ".join(node['outputs']) if node['outputs'] else "Updates SharedStore"
                design_doc += f"**Outputs:** {outputs_str}\n"
            else:
                design_doc += "**Outputs:** Updates SharedStore\n"
                
            design_doc += "\n"

        # Add implementation notes
        design_doc += "\n## Implementation Notes\n\n"
        design_doc += f"- Pattern: {spec.pattern}\n"
        design_doc += f"- Nodes: {len(spec.nodes)}\n"
        design_doc += f"- Utilities: {len(spec.utilities)}\n"
        design_doc += f"- FastAPI Integration: Enabled (Universal)\n"
        design_doc += "\nThis design document was generated automatically. Please review and complete with specific implementation details."

        return design_doc

    def _generate_pydantic_models(self, spec: WorkflowSpec) -> str:
        """Generate Pydantic models from shared store schema."""
        models = [
            "from pydantic import BaseModel, Field, validator",
            "from typing import Dict, List, Optional, Any",
            "from datetime import datetime",
            "",
            "",
        ]

        # Generate SharedStore model
        models.extend(
            [
                "class SharedStoreModel(BaseModel):",
                '    """Pydantic model for SharedStore validation."""',
                "",
            ]
        )

        for key, value_type in spec.shared_store_schema.items():
            models.append(f"    {key}: {value_type}")

        models.extend(["", ""])

        # Generate API models (always included in universal architecture)
        for endpoint in spec.api_endpoints:
            # Request model
            models.extend(
                [
                    f"class {endpoint['name']}Request(BaseModel):",
                    f'    """Request model for {endpoint["name"]} endpoint."""',
                    "",
                ]
            )

            for field in endpoint.get("request_fields", []):
                models.append(f"    {field['name']}: {field['type']}")

            models.extend(["", ""])

            # Response model
            models.extend(
                [
                    f"class {endpoint['name']}Response(BaseModel):",
                    f'    """Response model for {endpoint["name"]} endpoint."""',
                    "",
                ]
            )

            for field in endpoint.get("response_fields", []):
                models.append(f"    {field['name']}: {field['type']}")

            models.extend(["", ""])

        return "\n".join(models)

    def _generate_utility(self, utility: Dict[str, Any]) -> str:
        """Generate utility function from specification."""
        utility_code = [
            '"""',
            f"{utility['description']}",
            '"""',
            "",
            "from typing import Any, Optional",
            "",
            "",
        ]

        # Function signature
        params = []
        for param in utility.get("parameters", []):
            if param.get("optional", False):
                params.append(f"{param['name']}: Optional[{param['type']}] = None")
            else:
                params.append(f"{param['name']}: {param['type']}")

        # Determine if utility should be async based on description or explicit flag
        is_async_utility = utility.get("async", False) or any(
            keyword in utility["description"].lower()
            for keyword in [
                "llm",
                "api",
                "database",
                "file",
                "network",
                "http",
                "fetch",
                "request",
            ]
        )

        func_def = (
            f"async def {utility['name']}("
            if is_async_utility
            else f"def {utility['name']}("
        )
        test_call = (
            f"    # asyncio.run({utility['name']}())"
            if is_async_utility
            else f"    # {utility['name']}()"
        )

        utility_code.extend(
            [
                func_def,
                f"    {', '.join(params)}",
                f") -> {utility.get('return_type', 'Any')}:",
                '    """',
                f"    {utility['description']}",
                '    """',
                f"    # TODO: Implement {utility['name']}",
                f'    raise NotImplementedError("Utility function {utility["name"]} not implemented")',
                "",
                "",
                'if __name__ == "__main__":',
                f"    # Test {utility['name']} function",
            ]
        )

        if is_async_utility:
            utility_code.extend(["    import asyncio", test_call, "    pass"])
        else:
            utility_code.extend([test_call, "    pass"])

        return "\n".join(utility_code)

    def _get_smart_node_defaults(self, node: Dict[str, Any], is_async: bool = False) -> Dict[str, str]:
        """Generate smart defaults based on node name and description."""
        name = node.get("name", "").lower()
        description = node.get("description", "").lower()
        
        # Common patterns for different node types
        prep_examples = {
            "retriever": 'return shared.get("query", "")',
            "loader": 'return shared.get("file_path", "")',
            "analyzer": 'return shared.get("content", "")',
            "formatter": 'return shared.get("raw_data", "")',
            "validator": 'return shared.get("input_data", "")',
            "transformer": 'return shared.get("input_data", "")',
            "llm": 'prompt = f"Process this: {shared.get(\"content\", \"\")}"\n        return prompt',
            "embedding": 'return shared.get("text", "")',
            "search": 'return shared.get("query", "")',
            "filter": 'return shared.get("items", [])',
        }
        
        # Async exec examples
        exec_examples_async = {
            "retriever": 'search_results = await search_documents(prep_result)\n        return search_results',
            "loader": 'async with aiofiles.open(prep_result, "r") as f:\n            content = await f.read()\n        return content',
            "analyzer": 'analysis = await analyze_content(prep_result)\n        return analysis',
            "formatter": 'formatted_data = await format_response_async(prep_result)\n        return formatted_data',
            "validator": 'is_valid = await validate_input_async(prep_result)\n        return {"valid": is_valid, "data": prep_result}',
            "transformer": 'transformed = await transform_data_async(prep_result)\n        return transformed',
            "llm": 'response = await call_llm(prep_result)\n        return response',
            "embedding": 'embedding = await get_embedding(prep_result)\n        return embedding',
            "search": 'results = await search_vector_db(prep_result)\n        return results',
            "filter": 'filtered = await filter_async(prep_result)\n        return filtered',
        }
        
        # Sync exec examples  
        exec_examples_sync = {
            "retriever": 'search_results = search_documents(prep_result)\n        return search_results',
            "loader": 'with open(prep_result, "r") as f:\n            content = f.read()\n        return content',
            "analyzer": 'analysis = analyze_content(prep_result)\n        return analysis',
            "formatter": 'formatted_data = format_response(prep_result)\n        return formatted_data',
            "validator": 'is_valid = validate_input(prep_result)\n        return {"valid": is_valid, "data": prep_result}',
            "transformer": 'transformed = transform_data(prep_result)\n        return transformed',
            "llm": 'response = call_llm_sync(prep_result)\n        return response',
            "embedding": 'embedding = get_embedding_sync(prep_result)\n        return embedding',
            "search": 'results = search_vector_db_sync(prep_result)\n        return results',
            "filter": 'filtered = [item for item in prep_result if meets_criteria(item)]\n        return filtered',
        }
        
        # Choose appropriate exec examples based on async flag
        exec_examples = exec_examples_async if is_async else exec_examples_sync
        
        post_examples = {
            "retriever": 'shared["retrieved_docs"] = exec_result',
            "loader": 'shared["loaded_content"] = exec_result',
            "analyzer": 'shared["analysis_result"] = exec_result',
            "formatter": 'shared["formatted_output"] = exec_result',
            "validator": 'shared["validation_result"] = exec_result',
            "transformer": 'shared["transformed_data"] = exec_result',
            "llm": 'shared["llm_response"] = exec_result',
            "embedding": 'shared["embeddings"] = exec_result',
            "search": 'shared["search_results"] = exec_result',
            "filter": 'shared["filtered_data"] = exec_result',
        }
        
        # Match based on name or description
        for pattern in prep_examples.keys():
            if pattern in name or pattern in description:
                return {
                    "prep": prep_examples[pattern],
                    "exec": exec_examples[pattern], 
                    "post": post_examples[pattern]
                }
        
        # Default fallback
        return {
            "prep": 'return shared.get("input_data")',
            "exec": '# Implement your core logic here\n        return "success"',
            "post": 'shared["output_data"] = exec_result'
        }

    def _generate_nodes(self, spec: WorkflowSpec) -> str:
        """Generate PocketFlow nodes from specification."""
        nodes_code = [
            "from pocketflow import Node, AsyncNode, BatchNode",
            "from typing import Dict, Any",
            "import logging",
            "",
            "logger = logging.getLogger(__name__)",
            "",
            "",
        ]

        for node in spec.nodes:
            # Default to Node (sync) unless explicitly specified as async
            node_type = node.get("type", "Node")
            
            # Validate node type
            valid_node_types = {
                "Node", "AsyncNode", "BatchNode", 
                "AsyncBatchNode", "AsyncParallelBatchNode"
            }
            if node_type not in valid_node_types:
                raise ValueError(
                    f"Invalid node type '{node_type}' for node '{node['name']}'. "
                    f"Valid types are: {', '.join(sorted(valid_node_types))}"
                )

            # Use BatchNode for operations that process lists of items
            batch_comment = ""
            if node_type == "BatchNode":
                batch_comment = "\n    # NOTE: BatchNode used for processing multiple items in parallel"

            # Determine method signature based on node type
            is_async_node = node_type in [
                "AsyncNode",
                "AsyncBatchNode",
                "AsyncParallelBatchNode",
            ]
            exec_method = "async def exec_async" if is_async_node else "def exec"
            exec_signature = f"    {exec_method}(self, prep_result: Any) -> str:"

            # Get smart defaults based on node name/description
            smart_defaults = self._get_smart_node_defaults(node, is_async_node)
            
            # Generate enhanced TODO guidance from extensions
            enhanced_todos = self._get_enhanced_todos_for_node(node)
            orchestrator_guidance = self._get_orchestrator_guidance_for_node(node)
            framework_reminders = self._get_framework_reminders_for_node(node)

            nodes_code.extend(
                [
                    f"class {node['name']}({node_type}):",
                    '    """',
                    f"    {node['description']}",
                    f'    """{batch_comment}',
                    "",
                ]
            )
            
            # Add framework reminders at class level
            if framework_reminders:
                for reminder in framework_reminders:
                    nodes_code.append(f"    {reminder}")
                nodes_code.append("")
            
            # Add orchestrator guidance at class level  
            if orchestrator_guidance:
                for guidance in orchestrator_guidance:
                    nodes_code.append(f"    {guidance}")
                nodes_code.append("")

            nodes_code.extend([
                    "    def prep(self, shared: Dict[str, Any]) -> Any:",
                    '        """Data preparation and validation."""',
                    f'        logger.info(f"Preparing data for {node["name"]}")',
                    "",
                    "        # Enhanced TODO guidance from framework extensions:",
                ]
            )
            
            # Add enhanced TODOs for prep method
            prep_todos = enhanced_todos[:2] if enhanced_todos else ["# TODO: Customize this prep logic based on your needs"]
            for todo in prep_todos:
                nodes_code.append(f"        {todo}")
            
            nodes_code.extend([
                    f"        {smart_defaults['prep']}",
                    "",
                    exec_signature,
                    '        """Core processing logic."""',
                    f'        logger.info(f"Executing {node["name"]}")',
                    "",
                    "        # Enhanced TODO guidance from framework extensions:",
                ]
            )
            
            # Add enhanced TODOs for exec method
            exec_todos = enhanced_todos[2:4] if len(enhanced_todos) > 2 else ["# TODO: Customize this exec logic based on your needs"]
            for todo in exec_todos:
                nodes_code.append(f"        {todo}")
            
            nodes_code.extend([
                    f"        {smart_defaults['exec']}",
                    "",
                    "    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:",
                    '        """Post-processing and result storage."""',
                    f'        logger.info(f"Post-processing for {node["name"]}")',
                    "",
                    "        # Enhanced TODO guidance from framework extensions:",
                ]
            )
            
            # Add enhanced TODOs for post method
            post_todos = enhanced_todos[4:] if len(enhanced_todos) > 4 else ["# TODO: Customize this post logic based on your needs"]  
            for todo in post_todos:
                nodes_code.append(f"        {todo}")
            
            nodes_code.extend([
                    f"        {smart_defaults['post']}",
                    "",
                    "",
                ]
            )

        return "\n".join(nodes_code)

    def _generate_flow(self, spec: WorkflowSpec) -> str:
        """Generate PocketFlow flow assembly."""
        flow_code = [
            "from pocketflow import Flow",
            "from .nodes import " + ", ".join(node["name"] for node in spec.nodes),
            "import logging",
            "",
            "logger = logging.getLogger(__name__)",
            "",
            "",
        ]

        # Create flow class
        flow_code.extend(
            [
                f"class {spec.name}Flow(Flow):",
                '    """',
                f"    {spec.description}",
                '    """',
                "",
                "    def __init__(self):",
                "        nodes = {",
            ]
        )

        for node in spec.nodes:
            flow_code.append(f'            "{node["name"].lower()}": {node["name"]}(),')

        flow_code.extend(
            [
                "        }",
                "",
                "        edges = {",
            ]
        )

        # Generate edges based on node sequence
        for i, node in enumerate(spec.nodes):
            node_name = node["name"].lower()
            if i < len(spec.nodes) - 1:
                next_node = spec.nodes[i + 1]["name"].lower()
                flow_code.append(
                    f'            "{node_name}": {{"success": "{next_node}", "error": "error_handler"}},'
                )
            else:
                flow_code.append(
                    f'            "{node_name}": {{"success": None, "error": "error_handler"}},'
                )

        flow_code.extend(
            [
                "        }",
                "",
                "        super().__init__(nodes=nodes, edges=edges)",
                "",
                "",
            ]
        )

        return "\n".join(flow_code)

    def _generate_fastapi_main(self, spec: WorkflowSpec) -> str:
        """Generate FastAPI main application."""
        main_code = [
            "from fastapi import FastAPI, HTTPException",
            "from fastapi.middleware.cors import CORSMiddleware",
            f"from .router import router as {spec.name.lower()}_router",
            "import logging",
            "",
            "logging.basicConfig(level=logging.INFO)",
            "",
            "app = FastAPI(",
            f'    title="{spec.name} API",',
            f'    description="{spec.description}",',
            '    version="1.0.0"',
            ")",
            "",
            "app.add_middleware(",
            "    CORSMiddleware,",
            '    allow_origins=["*"],',
            "    allow_credentials=True,",
            '    allow_methods=["*"],',
            '    allow_headers=["*"],',
            ")",
            "",
            f'app.include_router({spec.name.lower()}_router, prefix="/api/v1", tags=["{spec.name}"])',
            "",
            '@app.get("/health")',
            "async def health_check():",
            '    return {"status": "healthy"}',
        ]

        return "\n".join(main_code)

    def _generate_fastapi_router(self, spec: WorkflowSpec) -> str:
        """Generate FastAPI router with endpoints."""
        router_code = [
            "from fastapi import APIRouter, HTTPException",
            "from .schemas.models import *",
            f"from .flow import {spec.name}Flow",
            "from typing import Dict, Any",
            "import logging",
            "from datetime import datetime",
            "",
            "logger = logging.getLogger(__name__)",
            "router = APIRouter()",
            "",
        ]

        for endpoint in spec.api_endpoints:
            method = endpoint.get("method", "post").lower()
            path = endpoint.get("path", f"/{endpoint['name'].lower()}")
            endpoint_name = endpoint["name"]
            default_desc = f"Execute {endpoint_name} workflow"

            router_code.extend([
                f'@router.{method}("{path}", response_model={endpoint_name}Response)',
                f"async def {endpoint_name.lower()}_endpoint(request: {endpoint_name}Request):",
                '    """',
                f"    {endpoint.get('description', default_desc)}",
                '    """',
                "    # Initialize SharedStore",
                "    shared = {",
                '        "request_data": request.dict(),',
                '        "timestamp": datetime.utcnow().isoformat()',
                "    }",
                "",
                "    # Execute workflow - let PocketFlow handle retries and errors",
                f"    flow = {spec.name}Flow()",
                "    await flow.run_async(shared)",
                "",
                "    # Check for flow-level errors",
                '    if "error" in shared:',
                "        raise HTTPException(",
                "            status_code=422,",
                '            detail=shared.get("error_message", "Workflow execution failed")',
                "        )",
                "",
                "    # Return response",
                f'    return {endpoint["name"]}Response(**shared.get("result", {{}}))',
                "",
                "",
            ])

        return "\n".join(router_code)

    def _generate_node_tests(self, spec: WorkflowSpec) -> str:
        """Generate tests for nodes."""
        # Use absolute imports for better type checker compatibility
        workflow_name = spec.name.lower().replace(" ", "")
        test_code = [
            "import pytest",
            "from unittest.mock import AsyncMock, patch",
            f"from {workflow_name}.nodes import " + ", ".join(node["name"] for node in spec.nodes),
            "",
            "",
        ]

        for node in spec.nodes:
            test_code.extend(
                [
                    f"class Test{node['name']}:",
                    f'    """Tests for {node["name"]} node."""',
                    "",
                    "    @pytest.fixture",
                    "    def node(self):",
                    f"        return {node['name']}()",
                    "",
                    "    @pytest.fixture",
                    "    def shared_store(self):",
                    '        return {"input_data": "test_data"}',
                    "",
                    "    def test_prep(self, node, shared_store):",
                    '        """Test prep method."""',
                    "        result = node.prep(shared_store)",
                    '        assert result == "test_data"',
                    "",
                    "    @pytest.mark.asyncio",
                    "    async def test_exec_async(self, node):",
                    '        """Test exec_async method."""',
                    '        result = await node.exec_async("test_data")',
                    '        assert result == "success"',
                    "",
                    "    def test_post(self, node, shared_store):",
                    '        """Test post method."""',
                    '        node.post(shared_store, "prep_result", "exec_result")',
                    '        assert "output_data" in shared_store',
                    "",
                    "",
                ]
            )

        return "\n".join(test_code)

    def _generate_flow_tests(self, spec: WorkflowSpec) -> str:
        """Generate tests for flow."""
        # Use absolute imports for better type checker compatibility
        workflow_name = spec.name.lower().replace(" ", "")
        test_code = [
            "import pytest",
            "from unittest.mock import AsyncMock, patch",
            f"from {workflow_name}.flow import {spec.name}Flow",
            "",
            "",
            f"class Test{spec.name}Flow:",
            f'    """Tests for {spec.name}Flow."""',
            "",
            "    @pytest.fixture",
            "    def flow(self):",
            f"        return {spec.name}Flow()",
            "",
            "    @pytest.fixture",
            "    def shared_store(self):",
            '        return {"input_data": "test_data"}',
            "",
            "    @pytest.mark.asyncio",
            "    async def test_flow_execution(self, flow, shared_store):",
            '        """Test complete flow execution."""',
            "        await flow.run_async(shared_store)",
            '        assert "output_data" in shared_store',
            "",
            "    @pytest.mark.asyncio",
            "    async def test_flow_error_handling(self, flow, shared_store):",
            '        """Test flow error handling."""',
            "        # Test with invalid input",
            '        shared_store["input_data"] = None',
            "        with pytest.raises(Exception):",
            "            await flow.run_async(shared_store)",
            "",
        ]

        return "\n".join(test_code)

    def _generate_api_tests(self, spec: WorkflowSpec) -> str:
        """Generate tests for FastAPI endpoints."""
        # Use absolute imports for better type checker compatibility
        workflow_name = spec.name.lower().replace(" ", "")
        test_code = [
            "import pytest",
            "from fastapi.testclient import TestClient",
            "from unittest.mock import AsyncMock, patch",
            f"from {workflow_name}.main import app",
            "",
            "client = TestClient(app)",
            "",
            "",
        ]

        for endpoint in spec.api_endpoints:
            method = endpoint.get("method", "post").upper()
            path = endpoint.get("path", f"/{endpoint['name'].lower()}")

            test_code.extend(
                [
                    f"class Test{endpoint['name']}Endpoint:",
                    f'    """Tests for {endpoint["name"]} endpoint."""',
                    "",
                    f"    def test_{endpoint['name'].lower()}_success(self):",
                    f'        """Test successful {endpoint["name"]} request."""',
                    '        request_data = {"test": "data"}',
                    f'        response = client.{method.lower()}("/api/v1{path}", json=request_data)',
                    "        assert response.status_code == 200",
                    "",
                    f"    def test_{endpoint['name'].lower()}_validation_error(self):",
                    '        """Test validation error handling."""',
                    f'        response = client.{method.lower()}("/api/v1{path}", json={{}})',
                    "        assert response.status_code == 422",
                    "",
                    "",
                ]
            )

        return "\n".join(test_code)

    def _generate_tasks(self, spec: WorkflowSpec) -> str:
        """Generate tasks.md file from template."""
        current_date = datetime.now().isoformat()[:10]
        spec_name = spec.name.lower().replace(" ", "-")

        tasks = f"""# Spec Tasks

These are the tasks to be completed for the spec detailed in @.agent-os/specs/{current_date}-{spec_name}/spec.md

> Created: {current_date}
> Status: Ready for Implementation

## Tasks

Following PocketFlow's 8-step Agentic Coding methodology:

### Phase 0: Design Document (LLM/AI Components Only)
- [x] 0.1 Create `docs/design.md` with complete PocketFlow design ✓ (Generated)
- [ ] 0.2 Review and complete Requirements section with problem statement and success criteria
- [ ] 0.3 Validate Flow Design with Mermaid diagram and node sequence
- [ ] 0.4 Review all Utility functions with input/output contracts
- [ ] 0.5 Validate SharedStore schema with complete data structure
- [ ] 0.6 Complete Node Design with prep/exec/post specifications
- [ ] 0.7 Validate design completeness before proceeding

### Phase 1: Pydantic Schemas & Data Models
- [ ] 1.1 Write tests for Pydantic model validation
- [x] 1.2 Create request/response models in `schemas/models.py` ✓ (Generated)
- [ ] 1.3 Implement core entity models with validation rules
- [ ] 1.4 Create SharedStore transformation models
- [ ] 1.5 Add custom validators and field constraints
- [ ] 1.6 Create error response models with standardized format
- [ ] 1.7 Verify all Pydantic models pass validation tests

### Phase 2: Utility Functions Implementation
- [ ] 2.1 Write tests for utility functions (with mocked external dependencies)
- [x] 2.2 Implement utility functions in `utils/` directory ✓ (Generated templates)"""

        # Add specific utilities
        for utility in spec.utilities:
            tasks += f"\n- [ ] 2.2.{utility['name']}: Complete implementation of `utils/{utility['name']}.py`"

        tasks += """
- [ ] 2.3 Add proper type hints and docstrings for all utilities
- [ ] 2.4 Implement LLM integration utilities (if applicable)
- [ ] 2.5 Add error handling without try/catch (fail fast approach)
- [ ] 2.6 Create standalone main() functions for utility testing
- [ ] 2.7 Verify all utility tests pass with mocked dependencies

### Phase 3: FastAPI Endpoints (Universal Architecture)"""

        tasks += """
- [ ] 3.1 Write tests for FastAPI endpoints (with mocked flows)
- [x] 3.2 Create FastAPI application structure in `main.py` ✓ (Generated)
- [x] 3.3 Implement route handlers with proper async patterns ✓ (Generated)
- [x] 3.4 Add request/response model integration ✓ (Generated)
- [ ] 3.5 Implement error handling and status code mapping
- [ ] 3.6 Add authentication and middleware (if required)
- [ ] 3.7 Verify all FastAPI endpoint tests pass"""

        tasks += """

### Phase 4: PocketFlow Nodes (LLM/AI Components)
- [ ] 4.1 Write tests for individual node lifecycle methods
- [x] 4.2 Implement nodes in `nodes.py` following design.md specifications ✓ (Generated templates)"""

        # Add specific nodes
        for node in spec.nodes:
            tasks += (
                f"\n- [ ] 4.2.{node['name']}: Complete implementation of {node['name']}"
            )

        tasks += """
- [ ] 4.3 Create prep() methods for data access and validation
- [ ] 4.4 Implement exec() methods with utility function calls
- [ ] 4.5 Add post() methods for result storage and action determination
- [ ] 4.6 Implement error handling as action string routing
- [ ] 4.7 Verify all node tests pass in isolation

### Phase 5: PocketFlow Flow Assembly (LLM/AI Components)
- [ ] 5.1 Write tests for complete flow execution scenarios
- [x] 5.2 Create flow assembly in `flow.py` ✓ (Generated)
- [ ] 5.3 Connect nodes with proper action string routing
- [ ] 5.4 Implement error handling and retry strategies
- [ ] 5.5 Add flow-level logging and monitoring
- [ ] 5.6 Test all flow paths including error scenarios
- [ ] 5.7 Verify flow integration with SharedStore schema

### Phase 6: Integration & Testing
- [ ] 6.1 Write end-to-end integration tests
- [ ] 6.2 Integrate FastAPI endpoints with PocketFlow workflows
- [ ] 6.3 Test complete request→flow→response cycle
- [ ] 6.4 Validate error propagation from flow to API responses
- [ ] 6.5 Test performance under expected load
- [ ] 6.6 Verify type safety across all boundaries
- [ ] 6.7 Run complete test suite and ensure 100% pass rate

### Phase 7: Optimization & Reliability
- [ ] 7.1 Add comprehensive logging throughout the system
- [ ] 7.2 Implement caching strategies (if applicable)
- [ ] 7.3 Add monitoring and observability hooks
- [ ] 7.4 Optimize async operations and batch processing
- [ ] 7.5 Add retry mechanisms and circuit breakers
- [ ] 7.6 Create health check endpoints
- [ ] 7.7 Verify system reliability under various conditions

**Development Toolchain Validation (Every Phase):**
- Run `uv run ruff check --fix .` for linting
- Run `uv run ruff format .` for code formatting  
- Run `uv run ty check` for type checking
- Run `pytest` for all tests
- Verify all checks pass before proceeding to next phase

## Generated Files Summary

The following files have been generated and need completion:

### Core Files ✓
- `docs/design.md` - Design document (review and complete)
- `schemas/models.py` - Pydantic models (review and extend)
- `nodes.py` - PocketFlow nodes (implement logic)
- `flow.py` - Flow assembly (review connections)

### Utility Files ✓"""

        for utility in spec.utilities:
            tasks += f"\n- `utils/{utility['name']}.py` - {utility['description']}"

        tasks += """

### FastAPI Files ✓
- `main.py` - FastAPI application
- `router.py` - API routes and handlers"""

        tasks += """

### Test Files ✓
- `tests/test_nodes.py` - Node unit tests
- `tests/test_flow.py` - Flow integration tests
- `tests/test_api.py` - API endpoint tests"""

        tasks += f"""

### Next Steps
1. Review the design document and complete any missing sections
2. Implement the utility functions with actual logic
3. Complete the node implementations with proper business logic
4. Test the complete workflow end-to-end
5. Deploy and validate in staging environment

Generated on: {current_date}
Workflow Pattern: {spec.pattern}
FastAPI Integration: Enabled (Universal)"""

        return tasks

    def _extract_template_section(self, template: str, section_name: str) -> str:
        """Extract a specific section from a template file."""
        lines = template.split("\n")
        in_section = False
        section_lines = []

        for line in lines:
            if section_name in line:
                in_section = True
                continue
            elif in_section and line.startswith("##") and section_name not in line:
                break
            elif in_section:
                section_lines.append(line)

        # If no section found, return a basic template
        if not section_lines:
            return f"""# Design Document

> Spec: {section_name}
> Created: {datetime.now().isoformat()[:10]}
> Status: Design Phase
> Framework: PocketFlow

## Requirements

### Problem Statement
[CLEAR_PROBLEM_DEFINITION_FROM_USER_PERSPECTIVE]

### Success Criteria
- [MEASURABLE_OUTCOME_1]
- [MEASURABLE_OUTCOME_2]

## Flow Design

### High-Level Architecture
```mermaid
graph TD
    A[Start] --> B[Processing]
    B --> C[End]
```

## Implementation Notes

This is a generated design document template. Please complete with actual requirements and design details.
"""

        return "\n".join(section_lines)

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        """Save generated workflow files to disk."""
        workflow_dir = self.output_path / spec.name.lower().replace(" ", "_")
        workflow_dir.mkdir(exist_ok=True)

        # Track directories that need __init__.py files
        directories_needing_init = set()

        for file_path, content in output_files.items():
            full_path = workflow_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            
            # Add parent directories to the set for __init__.py creation
            directories_needing_init.add(full_path.parent)

        # Create __init__.py files for proper package structure
        # This ensures relative imports in tests work correctly
        for directory in directories_needing_init:
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")

        # Also create __init__.py in the root workflow directory
        root_init = workflow_dir / "__init__.py"
        if not root_init.exists():
            root_init.write_text("")

        print(f"Generated workflow saved to: {workflow_dir}")
        
        # Automatically validate generated templates
        print("\n🔍 Running template validation...")
        validation_result = self.coordinate_template_validation(str(workflow_dir))

        # Helper to normalize issue messages across object/dict fallbacks
        def _issue_msg(issue: Any) -> str:
            return getattr(issue, "message", str(issue))

        # Accessors for errors/warnings that may be properties or dict entries
        errors = getattr(validation_result, "errors", [])
        warnings = getattr(validation_result, "warnings", [])

        if getattr(validation_result, "is_valid", True):
            print("✅ Template validation passed!")
        else:
            print("❌ Template validation issues found:")
            for error in errors:
                print(f"  • Error: {_issue_msg(error)}")
            for warning in warnings:
                print(f"  • Warning: {_issue_msg(warning)}")
        
        if warnings:
            print("⚠️  Validation warnings (non-blocking):")
            for warning in warnings:
                print(f"  • {_issue_msg(warning)}")

    def coordinate_template_validation(self, template_path: str) -> Any:
        """Coordinate with template-validator agent for post-generation validation."""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent))
            from template_validator import PocketFlowValidator
            
            validator = PocketFlowValidator()
            template_dir = Path(template_path)
            
            result = validator.validate_directory(template_dir)
            # Return canonical validator result directly
            return result
            
        except ImportError:
            # Minimal fallback object to preserve expected attributes
            class _FallbackValidation:
                def __init__(self):
                    self.is_valid = True
                    self.errors = []
                    # Create simple issue-like objects with a message attribute
                    class _Issue:
                        def __init__(self, msg: str):
                            self.message = msg
                        def __str__(self) -> str:
                            return self.message
                    self.warnings = [_Issue("Template validation module not available - skipping validation")]
            return _FallbackValidation()
        except Exception as e:
            class _FallbackValidationError:
                def __init__(self, msg: str):
                    self.is_valid = False
                    class _Issue:
                        def __init__(self, m: str):
                            self.message = m
                        def __str__(self) -> str:
                            return self.message
                    self.errors = [_Issue(f"Validation failed: {msg}")]
                    self.warnings = []
            return _FallbackValidationError(str(e))

    def request_pattern_analysis(self, requirements: str, project_name: Optional[str] = None) -> Any:
        """Request pattern analysis using the unified coordination entrypoint.

        Note: Prefer `agent_coordination.coordinate_pattern_analysis` as the high-level pathway.
        This method remains as a thin wrapper for backward compatibility and returns the
        canonical `pattern_analyzer.PatternRecommendation` type.
        """
        # Soft deprecation notice
        try:
            import warnings
            warnings.warn(
                "PocketFlowGenerator.request_pattern_analysis is a thin wrapper; "
                "prefer agent_coordination.coordinate_pattern_analysis",
                DeprecationWarning,
                stacklevel=2,
            )
        except Exception:
            pass
        # Try the coordination entrypoint first (preferred path)
        try:
            try:
                from .agent_coordination import coordinate_pattern_analysis  # type: ignore
            except ImportError:
                from agent_coordination import coordinate_pattern_analysis  # type: ignore

            # Use provided project name when available; otherwise use a sensible default
            project = project_name or "PocketFlowWorkflow"
            context = coordinate_pattern_analysis(project, requirements)
            if getattr(context, "pattern_recommendation", None) is not None:
                return context.pattern_recommendation
            # If coordination returned no recommendation, fall through to analyzer fallback
        except Exception as coord_err:
            logger.debug(f"Coordination entrypoint unavailable or failed: {coord_err}")

        # Fallback: call analyzer directly to preserve behavior in minimal environments
        try:
            try:
                from .pattern_analyzer import PatternAnalyzer  # type: ignore
            except ImportError:
                from pattern_analyzer import PatternAnalyzer  # type: ignore

            analyzer = PatternAnalyzer()
            return analyzer.analyze_and_recommend(requirements)
        except ImportError:
            # Minimal fallback object to preserve expected attributes
            class _FallbackPatternRecommendation:
                def __init__(self):
                    self.primary_pattern = "WORKFLOW"
                    self.confidence_score = 0.6
                    self.secondary_patterns = []
                    self.rationale = (
                        "Pattern analyzer not available - using default WORKFLOW pattern"
                    )
                    self.detailed_justification = ""
                    self.template_customizations = {}
                    self.workflow_suggestions = {}

            return _FallbackPatternRecommendation()
        except Exception as e:
            class _FallbackPatternRecommendationError:
                def __init__(self, msg: str):
                    self.primary_pattern = "WORKFLOW"
                    self.confidence_score = 0.5
                    self.secondary_patterns = []
                    self.rationale = (
                        f"Pattern analysis failed ({msg}) - using default WORKFLOW pattern"
                    )
                    self.detailed_justification = ""
                    self.template_customizations = {}
                    self.workflow_suggestions = {}

            return _FallbackPatternRecommendationError(str(e))

    def generate_dependency_config(self, pattern: str) -> Any:
        """Generate dependency configuration via dependency-orchestrator agent."""
        try:
            from .dependency_orchestrator import DependencyOrchestrator
            
            orchestrator = DependencyOrchestrator()
            config = orchestrator.generate_config_for_pattern(pattern)
            return config
            
        except ImportError:
            # Fallback implementation if orchestrator not available
            return self._generate_basic_dependency_config(pattern)
        except Exception as e:
            logger.warning(f"Dependency orchestrator failed: {e}, using fallback")
            return self._generate_basic_dependency_config(pattern)

    def _generate_basic_dependency_config(self, pattern: str) -> Any:
        """Generate basic dependency configuration as fallback."""
        # Import canonical type if available
        try:
            try:
                from .dependency_orchestrator import DependencyConfig as OrchestratorDependencyConfig  # type: ignore
            except ImportError:
                from dependency_orchestrator import DependencyConfig as OrchestratorDependencyConfig  # type: ignore
        except Exception:
            OrchestratorDependencyConfig = None  # type: ignore
        base_deps = ["pocketflow", "pydantic", "fastapi"]
        
        pattern_deps = {
            "RAG": ["chromadb", "sentence-transformers"],
            "AGENT": ["openai", "anthropic"],
            "TOOL": ["requests", "aiohttp"],
            "WORKFLOW": [],
            "MAPREDUCE": ["celery", "redis"],
            "MULTI-AGENT": ["openai", "anthropic"],
            "STRUCTURED-OUTPUT": ["jsonschema"]
        }
        
        if OrchestratorDependencyConfig is not None:
            return OrchestratorDependencyConfig(
                base_dependencies=base_deps,
                pattern_dependencies=pattern_deps.get(pattern, []),
                dev_dependencies=["pytest", "pytest-asyncio", "ruff", "mypy"],
                tool_configs={
                    "ruff": {"line-length": 88, "target-version": "py312"},
                    "mypy": {"python_version": "3.12", "strict": True}
                }
            )
        else:
            # Minimal dict fallback to avoid type dependency
            return {
                "base_dependencies": base_deps,
                "pattern_dependencies": pattern_deps.get(pattern, []),
                "dev_dependencies": ["pytest", "pytest-asyncio", "ruff", "mypy"],
                "tool_configs": {
                    "ruff": {"line-length": 88, "target-version": "py312"},
                    "mypy": {"python_version": "3.12", "strict": True}
                },
            }


def main():
    """CLI interface for the workflow generator."""
    import argparse

    if not YAML_AVAILABLE:
        print(
            "Error: PyYAML is required for CLI usage. Install with: pip install pyyaml"
        )
        return 1

    parser = argparse.ArgumentParser(
        description="Generate PocketFlow workflows from specifications"
    )
    parser.add_argument(
        "--spec", required=True, help="Path to workflow specification YAML file"
    )
    parser.add_argument(
        "--output", help="Output directory (default: .agent-os/workflows)"
    )

    args = parser.parse_args()

    # Load specification
    try:
        with open(args.spec, "r") as f:
            spec_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Specification file not found: {args.spec}")
        return 1
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in specification file: {e}")
        return 1

    try:
        spec = WorkflowSpec(**spec_data)
    except TypeError as e:
        print(f"Error: Invalid specification format: {e}")
        return 1

    # Generate workflow
    try:
        # Initialize generator with custom paths if provided
        generator_kwargs = {}
        if args.output:
            generator_kwargs["output_path"] = args.output

        generator = PocketFlowGenerator(**generator_kwargs)
        output_files = generator.generate_workflow(spec)
        generator.save_workflow(spec, output_files)

        print(f"Successfully generated workflow: {spec.name}")
        return 0
    except Exception as e:
        print(f"Error: Workflow generation failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
