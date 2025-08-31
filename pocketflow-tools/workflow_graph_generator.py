#!/usr/bin/env python3
"""
Workflow Graph Generation for PocketFlow

Generates Mermaid diagrams and workflow structures based on pattern analysis.
Part of the Pattern Analyzer Agent implementation.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
# Support running as a package (relative) and as a standalone script (absolute)
try:
    from .pattern_analyzer import PatternType, PatternRecommendation  # type: ignore
except ImportError:  # pragma: no cover - fallback for standalone execution
    from pattern_analyzer import PatternType, PatternRecommendation

# Import centralized pattern node templates
try:  # pragma: no cover - import convenience
    from .pattern_definitions import get_node_templates  # type: ignore
except Exception:  # pragma: no cover - standalone fallback
    from pattern_definitions import get_node_templates  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class WorkflowNode:
    """Represents a workflow node in the graph."""
    name: str
    description: str
    node_type: str  # Node, AsyncNode, BatchNode, etc.
    position: int
    inputs: List[str] = None
    outputs: List[str] = None
    
    def __post_init__(self):
        if self.inputs is None:
            self.inputs = []
        if self.outputs is None:
            self.outputs = []


@dataclass
class WorkflowEdge:
    """Represents a connection between workflow nodes."""
    source: str
    target: str
    condition: str = "success"  # success, error, conditional
    label: Optional[str] = None


@dataclass
class WorkflowGraph:
    """Complete workflow graph structure."""
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]
    pattern: PatternType
    complexity_level: str = "medium"  # simple, medium, complex


class WorkflowGraphGenerator:
    """Generates workflow graphs based on patterns and requirements."""
    
    def __init__(self):
        self.pattern_flows = self._load_pattern_flows()
        
    def _load_pattern_flows(self) -> Dict[PatternType, Dict[str, Any]]:
        """Load predefined workflow flows for each pattern."""
        
        return {
            PatternType.RAG: {
                "flow_type": "sequential_with_branches",
                "core_nodes": get_node_templates(PatternType.RAG),
                "flow_patterns": [
                    ("DocumentLoader", "EmbeddingGenerator", "success"),
                    ("EmbeddingGenerator", "QueryProcessor", "success"),
                    ("QueryProcessor", "Retriever", "success"), 
                    ("Retriever", "ContextFormatter", "success"),
                    ("ContextFormatter", "LLMGenerator", "success")
                ],
                "error_handling": [
                    ("DocumentLoader", "ErrorHandler", "error"),
                    ("EmbeddingGenerator", "ErrorHandler", "error"),
                    ("Retriever", "ErrorHandler", "error"),
                    ("LLMGenerator", "ErrorHandler", "error")
                ]
            },
            
            PatternType.AGENT: {
                "flow_type": "decision_tree",
                "core_nodes": get_node_templates(PatternType.AGENT),
                "flow_patterns": [
                    ("TaskAnalyzer", "PlanningEngine", "success"),
                    ("PlanningEngine", "ReasoningNode", "success"),
                    ("ReasoningNode", "ActionExecutor", "success"),
                    ("ActionExecutor", "ResultEvaluator", "success"),
                    ("ResultEvaluator", "ReasoningNode", "needs_refinement"),
                    ("ResultEvaluator", "ActionExecutor", "retry_action")
                ],
                "error_handling": [
                    ("TaskAnalyzer", "ErrorHandler", "error"),
                    ("PlanningEngine", "ErrorHandler", "error"),
                    ("ReasoningNode", "ErrorHandler", "error"),
                    ("ActionExecutor", "ErrorHandler", "error")
                ]
            },
            
            PatternType.TOOL: {
                "flow_type": "linear_with_validation",
                "core_nodes": get_node_templates(PatternType.TOOL),
                "flow_patterns": [
                    ("InputValidator", "AuthHandler", "valid"),
                    ("AuthHandler", "APIClient", "authenticated"),
                    ("APIClient", "DataTransformer", "success"),
                    ("DataTransformer", "ResponseProcessor", "success")
                ],
                "error_handling": [
                    ("InputValidator", "ErrorHandler", "invalid"),
                    ("AuthHandler", "ErrorHandler", "auth_failed"),
                    ("APIClient", "ErrorHandler", "api_error"),
                    ("DataTransformer", "ErrorHandler", "transform_error")
                ]
            },
            
            PatternType.WORKFLOW: {
                "flow_type": "sequential",
                "core_nodes": get_node_templates(PatternType.WORKFLOW),
                "flow_patterns": [
                    ("InputProcessor", "BusinessLogic", "success"),
                    ("BusinessLogic", "DataProcessor", "success"),
                    ("DataProcessor", "OutputFormatter", "success")
                ],
                "error_handling": [
                    ("InputProcessor", "ErrorHandler", "error"),
                    ("BusinessLogic", "ErrorHandler", "error"),
                    ("DataProcessor", "ErrorHandler", "error")
                ]
            },
            
            PatternType.MAPREDUCE: {
                "flow_type": "parallel_with_aggregation",
                "core_nodes": get_node_templates(PatternType.MAPREDUCE),
                "flow_patterns": [
                    ("TaskDistributor", "MapProcessor", "distributed"),
                    ("MapProcessor", "IntermediateAggregator", "mapped"),
                    ("IntermediateAggregator", "ReduceProcessor", "aggregated"),
                    ("ReduceProcessor", "ResultCollector", "reduced")
                ],
                "error_handling": [
                    ("TaskDistributor", "ErrorHandler", "distribution_error"),
                    ("MapProcessor", "ErrorHandler", "map_error"),
                    ("ReduceProcessor", "ErrorHandler", "reduce_error")
                ]
            },
            
            PatternType.MULTI_AGENT: {
                "flow_type": "collaborative",
                "core_nodes": get_node_templates(PatternType.MULTI_AGENT),
                "flow_patterns": [
                    ("TaskCoordinator", "SpecialistAgent", "task_assigned"),
                    ("SpecialistAgent", "ConsensusManager", "completed"),
                    ("ConsensusManager", "ResultIntegrator", "consensus_reached"),
                    ("ConsensusManager", "SpecialistAgent", "needs_revision")
                ],
                "error_handling": [
                    ("TaskCoordinator", "ErrorHandler", "coordination_error"),
                    ("SpecialistAgent", "ErrorHandler", "agent_error"),
                    ("ConsensusManager", "ErrorHandler", "consensus_error")
                ]
            },
            
            PatternType.STRUCTURED_OUTPUT: {
                "flow_type": "validation_pipeline",
                "core_nodes": get_node_templates(PatternType.STRUCTURED_OUTPUT),
                "flow_patterns": [
                    ("SchemaValidator", "DataProcessor", "valid"),
                    ("DataProcessor", "OutputStructurer", "processed"),
                    ("OutputStructurer", "FormatValidator", "structured")
                ],
                "error_handling": [
                    ("SchemaValidator", "ErrorHandler", "schema_error"),
                    ("DataProcessor", "ErrorHandler", "processing_error"),
                    ("OutputStructurer", "ErrorHandler", "structure_error"),
                    ("FormatValidator", "ErrorHandler", "format_error")
                ]
            }
        }
    
    def generate_workflow_graph(self, pattern: PatternType, 
                              requirements: str = "",
                              complexity_level: str = "medium") -> WorkflowGraph:
        """Generate a complete workflow graph for a given pattern."""
        
        logger.info(f"Generating workflow graph for pattern: {pattern.value}")
        
        # Get pattern flow definition
        pattern_flow = self.pattern_flows.get(pattern, self.pattern_flows[PatternType.WORKFLOW])
        
        # Create nodes
        nodes = []
        for i, node_def in enumerate(pattern_flow["core_nodes"]):
            node = WorkflowNode(
                name=node_def["name"],
                description=node_def["description"],
                node_type=node_def["type"],
                position=i
            )
            nodes.append(node)
        
        # Create edges
        edges = []
        
        # Add success flow edges
        for source, target, condition in pattern_flow["flow_patterns"]:
            edge = WorkflowEdge(
                source=source,
                target=target,
                condition=condition,
                label=condition if condition != "success" else None
            )
            edges.append(edge)
        
        # Add error handling edges if complexity allows
        if complexity_level in ["medium", "complex"]:
            for source, target, condition in pattern_flow.get("error_handling", []):
                edge = WorkflowEdge(
                    source=source,
                    target=target,
                    condition=condition,
                    label=condition
                )
                edges.append(edge)
        
        # Add complexity-specific enhancements
        if complexity_level == "complex":
            nodes, edges = self._add_complex_features(nodes, edges, pattern)
        
        return WorkflowGraph(
            nodes=nodes,
            edges=edges,
            pattern=pattern,
            complexity_level=complexity_level
        )
    
    def _add_complex_features(self, nodes: List[WorkflowNode], 
                            edges: List[WorkflowEdge], 
                            pattern: PatternType) -> tuple:
        """Add complex features like monitoring, caching, retry logic."""
        
        # Add monitoring node
        monitor_node = WorkflowNode(
            name="MonitoringNode",
            description="Monitor workflow execution and metrics",
            node_type="Node",
            position=len(nodes)
        )
        nodes.append(monitor_node)
        
        # Add caching node for patterns that benefit from it
        if pattern in [PatternType.RAG, PatternType.AGENT]:
            cache_node = WorkflowNode(
                name="CacheManager",
                description="Manage caching for performance optimization",
                node_type="Node",
                position=len(nodes)
            )
            nodes.append(cache_node)
        
        # Add retry mechanism
        retry_node = WorkflowNode(
            name="RetryManager",
            description="Handle retry logic for failed operations",
            node_type="Node", 
            position=len(nodes)
        )
        nodes.append(retry_node)
        
        return nodes, edges
    
    def generate_mermaid_diagram(self, workflow_graph: WorkflowGraph) -> str:
        """Generate a Mermaid diagram from workflow graph."""
        
        logger.info(f"Generating Mermaid diagram for {workflow_graph.pattern.value} pattern")
        
        mermaid_lines = [
            "```mermaid",
            "graph TD"
        ]
        
        # Add nodes
        node_shapes = {
            "Node": ("", ""),
            "AsyncNode": ("((", "))"),
            "BatchNode": ("[[", "]]"),
            "AsyncBatchNode": ("[(", ")]")
        }
        
        for node in workflow_graph.nodes:
            shape_start, shape_end = node_shapes.get(node.node_type, ("", ""))
            node_id = node.name.replace(" ", "_")
            mermaid_lines.append(f"    {node_id}{shape_start}[{node.name}]{shape_end}")
        
        # Add edges
        for edge in workflow_graph.edges:
            source_id = edge.source.replace(" ", "_")
            target_id = edge.target.replace(" ", "_")
            
            if edge.label and edge.condition != "success":
                mermaid_lines.append(f"    {source_id} -->|{edge.label}| {target_id}")
            else:
                mermaid_lines.append(f"    {source_id} --> {target_id}")
        
        # Add styling based on pattern
        styling = self._get_pattern_styling(workflow_graph.pattern)
        mermaid_lines.extend(styling)
        
        mermaid_lines.append("```")
        
        return "\n".join(mermaid_lines)
    
    def _get_pattern_styling(self, pattern: PatternType) -> List[str]:
        """Get Mermaid styling for different patterns."""
        
        styling_map = {
            PatternType.RAG: [
                "    classDef rag fill:#e1f5fe,stroke:#0277bd,stroke-width:2px",
                "    class DocumentLoader,EmbeddingGenerator,QueryProcessor,Retriever,ContextFormatter,LLMGenerator rag"
            ],
            PatternType.AGENT: [
                "    classDef agent fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px",
                "    class TaskAnalyzer,PlanningEngine,ReasoningNode,ActionExecutor,ResultEvaluator agent"
            ],
            PatternType.TOOL: [
                "    classDef tool fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px",
                "    class InputValidator,AuthHandler,APIClient,DataTransformer,ResponseProcessor tool"
            ],
            PatternType.WORKFLOW: [
                "    classDef workflow fill:#fff3e0,stroke:#ef6c00,stroke-width:2px",
                "    class InputProcessor,BusinessLogic,DataProcessor,OutputFormatter workflow"
            ]
        }
        
        return styling_map.get(pattern, [
            "    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px"
        ])
    
    def generate_workflow_description(self, workflow_graph: WorkflowGraph) -> str:
        """Generate a textual description of the workflow."""
        
        description_parts = [
            f"# {workflow_graph.pattern.value} Workflow",
            "",
            f"**Pattern:** {workflow_graph.pattern.value}",
            f"**Complexity:** {workflow_graph.complexity_level.title()}",
            f"**Nodes:** {len(workflow_graph.nodes)}",
            f"**Connections:** {len(workflow_graph.edges)}",
            "",
            "## Node Sequence",
            ""
        ]
        
        # Add node descriptions
        for i, node in enumerate(workflow_graph.nodes, 1):
            description_parts.append(f"{i}. **{node.name}** ({node.node_type})")
            description_parts.append(f"   - {node.description}")
            description_parts.append("")
        
        # Add flow description
        description_parts.extend([
            "## Workflow Flow",
            ""
        ])
        
        # Group edges by condition
        success_edges = [e for e in workflow_graph.edges if e.condition == "success"]
        error_edges = [e for e in workflow_graph.edges if e.condition != "success"]
        
        if success_edges:
            description_parts.append("### Success Flow")
            for edge in success_edges:
                description_parts.append(f"- {edge.source} → {edge.target}")
            description_parts.append("")
        
        if error_edges:
            description_parts.append("### Error Handling")
            for edge in error_edges:
                description_parts.append(f"- {edge.source} →[{edge.condition}] {edge.target}")
            description_parts.append("")
        
        return "\n".join(description_parts)


def generate_workflow_from_recommendation(recommendation: PatternRecommendation, 
                                        complexity_level: str = "medium") -> WorkflowGraph:
    """Convenience function to generate workflow from pattern recommendation."""
    
    generator = WorkflowGraphGenerator()
    return generator.generate_workflow_graph(
        recommendation.primary_pattern,
        complexity_level=complexity_level
    )


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    generator = WorkflowGraphGenerator()
    
    # Test each pattern
    for pattern in PatternType:
        if pattern == PatternType.HYBRID:
            continue  # Skip hybrid for now
            
        print(f"\n{'='*60}")
        print(f"Testing {pattern.value} Pattern")
        print('='*60)
        
        # Generate workflow graph
        workflow_graph = generator.generate_workflow_graph(pattern, complexity_level="medium")
        
        # Generate Mermaid diagram
        mermaid_diagram = generator.generate_mermaid_diagram(workflow_graph)
        
        # Generate description
        description = generator.generate_workflow_description(workflow_graph)
        
        print("Mermaid Diagram:")
        print(mermaid_diagram)
        print("\nWorkflow Description:")
        print(description[:300] + "..." if len(description) > 300 else description)
