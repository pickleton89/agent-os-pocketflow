#!/usr/bin/env python3
"""
Coordination module for agent-tool integration

This module provides a unified interface for Claude Code agents to access
framework-tools functionality, implementing agent handoff protocols and
coordination between pattern analysis, workflow generation, and validation.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Add framework-tools to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_coordination import coordinate_pattern_analysis, create_subagent_handoff, AgentCoordinator
from pattern_analyzer import PatternAnalyzer
from dependency_orchestrator import DependencyOrchestrator
from workflow_graph_generator import WorkflowGraphGenerator
from template_validator import TemplateValidator

logger = logging.getLogger(__name__)


class ToolCoordinator:
    """
    Unified interface for agents to access framework-tools functionality.
    
    This class serves as the bridge between Claude Code agents and the
    framework-tools system, providing agent handoff protocols and 
    coordination between different workflow phases.
    """
    
    def __init__(self):
        """Initialize the tool coordinator with all required components."""
        self.pattern_analyzer = PatternAnalyzer()
        self.dependency_orchestrator = DependencyOrchestrator()
        self.workflow_generator = WorkflowGraphGenerator()
        self.template_validator = TemplateValidator()
        self.agent_coordinator = AgentCoordinator()
        
        logger.info("ToolCoordinator initialized with all framework-tools components")
    
    def analyze_pattern(self, project_name: str, requirements: str) -> Dict[str, Any]:
        """
        Analyze requirements and return pattern recommendation with handoff.
        
        This method combines pattern analysis with agent coordination to
        provide a complete workflow analysis including recommended next steps.
        
        Args:
            project_name: Name of the project being analyzed
            requirements: Natural language requirements text
            
        Returns:
            Dictionary containing pattern analysis results and handoff information
        """
        logger.info(f"Analyzing pattern for project: {project_name}")
        
        # Use agent coordination system for comprehensive analysis
        context = coordinate_pattern_analysis(project_name, requirements)
        handoff = create_subagent_handoff(context)
        
        return {
            "pattern": context.pattern_recommendation.primary_pattern.value,
            "confidence": context.pattern_recommendation.confidence_score,
            "secondary_patterns": [p.value for p in context.pattern_recommendation.secondary_patterns],
            "rationale": context.pattern_recommendation.rationale,
            "template_customizations": context.pattern_recommendation.template_customizations,
            "workflow_suggestions": context.pattern_recommendation.workflow_suggestions,
            "handoff": handoff.payload,
            "target_agent": handoff.target_agent,
            "coordination_context": {
                "phase": context.phase.value,
                "project_name": context.project_name,
                "coordination_id": handoff.payload.get("coordination_metadata", {}).get("coordination_id")
            }
        }
    
    def generate_dependencies(self, project_name: str, pattern: str) -> Dict[str, Any]:
        """
        Generate dependency configurations for a specific pattern.
        
        Args:
            project_name: Name of the project
            pattern: PocketFlow pattern type (RAG, AGENT, TOOL, etc.)
            
        Returns:
            Dictionary containing dependency configuration files and metadata
        """
        logger.info(f"Generating dependencies for {pattern} pattern")
        
        try:
            config = self.dependency_orchestrator.generate_config_for_pattern(pattern)
            pyproject_content = self.dependency_orchestrator.generate_pyproject_toml(project_name, pattern)
            uv_config = self.dependency_orchestrator.generate_uv_config(project_name, pattern)
            
            return {
                "status": "success",
                "pattern": pattern,
                "project_name": project_name,
                "pyproject_toml": pyproject_content,
                "uv_config": uv_config,
                "dependency_summary": {
                    "base_dependencies": len(config.base_dependencies),
                    "pattern_dependencies": len(config.pattern_dependencies),
                    "dev_dependencies": len(config.dev_dependencies)
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate dependencies: {e}")
            return {
                "status": "error",
                "error": str(e),
                "pattern": pattern,
                "project_name": project_name
            }
    
    def generate_workflow_graph(self, pattern: str, requirements: str = "", 
                               complexity_level: str = "medium") -> Dict[str, Any]:
        """
        Generate workflow graph and Mermaid diagram for a pattern.
        
        Args:
            pattern: PocketFlow pattern type
            requirements: Additional requirements for customization
            complexity_level: Complexity level (simple, medium, complex)
            
        Returns:
            Dictionary containing workflow graph and Mermaid diagram
        """
        logger.info(f"Generating workflow graph for {pattern} pattern")
        
        try:
            from pattern_analyzer import PatternType
            pattern_type = PatternType(pattern.upper())
            
            workflow_graph = self.workflow_generator.generate_workflow_graph(
                pattern_type, requirements, complexity_level
            )
            
            mermaid_diagram = self.workflow_generator.generate_mermaid_diagram(workflow_graph)
            
            return {
                "status": "success",
                "pattern": pattern,
                "complexity_level": complexity_level,
                "workflow_graph": {
                    "nodes": [{"name": n.name, "type": n.node_type, "description": n.description} 
                             for n in workflow_graph.nodes],
                    "edges": [{"source": e.source, "target": e.target, "condition": e.condition}
                             for e in workflow_graph.edges]
                },
                "mermaid_diagram": mermaid_diagram,
                "node_count": len(workflow_graph.nodes),
                "edge_count": len(workflow_graph.edges)
            }
        except Exception as e:
            logger.error(f"Failed to generate workflow graph: {e}")
            return {
                "status": "error",
                "error": str(e),
                "pattern": pattern
            }
    
    def validate_templates(self, template_dir: str, pattern: str = "") -> Dict[str, Any]:
        """
        Validate generated templates for structural correctness.
        
        Args:
            template_dir: Directory containing generated templates
            pattern: Expected pattern type for validation
            
        Returns:
            Dictionary containing validation results and recommendations
        """
        logger.info(f"Validating templates in: {template_dir}")
        
        try:
            # Discover template files
            template_files = self.template_validator.discover_template_files(template_dir)
            
            validation_results = []
            
            # Perform comprehensive validation
            for file_path in template_files:
                # Syntax validation
                syntax_result = self.template_validator.validate_python_syntax(file_path)
                
                # Pattern compliance validation
                pattern_result = self.template_validator.validate_pocketflow_patterns(file_path)
                
                # Pydantic model validation
                model_result = self.template_validator.validate_pydantic_models(file_path)
                
                # Placeholder quality validation
                placeholder_result = self.template_validator.validate_placeholder_quality(file_path)
                
                validation_results.append({
                    "file": file_path,
                    "syntax": syntax_result.to_dict() if hasattr(syntax_result, 'to_dict') else {"passed": True},
                    "patterns": pattern_result.to_dict() if hasattr(pattern_result, 'to_dict') else {"passed": True},
                    "models": model_result.to_dict() if hasattr(model_result, 'to_dict') else {"passed": True},
                    "placeholders": placeholder_result.to_dict() if hasattr(placeholder_result, 'to_dict') else {"passed": True}
                })
            
            # Generate summary
            total_files = len(template_files)
            passed_files = sum(1 for r in validation_results 
                             if all(v.get("passed", True) for v in r.values() if isinstance(v, dict)))
            
            return {
                "status": "success",
                "template_dir": template_dir,
                "pattern": pattern,
                "summary": {
                    "total_files": total_files,
                    "passed_files": passed_files,
                    "failed_files": total_files - passed_files,
                    "success_rate": f"{(passed_files/total_files*100):.1f}%" if total_files > 0 else "N/A"
                },
                "detailed_results": validation_results
            }
        except Exception as e:
            logger.error(f"Failed to validate templates: {e}")
            return {
                "status": "error",
                "error": str(e),
                "template_dir": template_dir
            }
    
    def coordinate_handoff(self, handoff_payload: Dict[str, Any], 
                          agent_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process agent handoff and coordination.
        
        Args:
            handoff_payload: Original handoff payload from agent coordination
            agent_response: Response from the target agent
            
        Returns:
            Updated coordination context and next steps
        """
        logger.info("Processing agent handoff coordination")
        
        try:
            # Create a minimal handoff package for processing
            from agent_coordination import HandoffPackage, CoordinationContext, CoordinationPhase
            
            # Reconstruct coordination context from payload
            context = CoordinationContext(
                project_name=handoff_payload.get("project_name", ""),
                requirements=handoff_payload.get("requirements", ""),
                phase=CoordinationPhase.WORKFLOW_COORDINATION
            )
            
            # Create handoff package
            handoff = HandoffPackage(
                source_agent="pattern-analyzer",
                target_agent=handoff_payload.get("target_agent", "file-creator"),
                payload=handoff_payload,
                coordination_context=context,
                handoff_type="coordination_processing"
            )
            
            # Process feedback through agent coordinator
            updated_context = self.agent_coordinator.process_subagent_feedback(handoff, agent_response)
            
            return {
                "status": "success",
                "updated_context": {
                    "phase": updated_context.phase.value,
                    "project_name": updated_context.project_name,
                    "next_steps": self._determine_next_steps(updated_context)
                },
                "coordination_summary": self.agent_coordinator.create_coordination_summary(updated_context)
            }
        except Exception as e:
            logger.error(f"Failed to process handoff coordination: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _determine_next_steps(self, context) -> list:
        """Determine recommended next steps based on coordination context."""
        next_steps = []
        
        if context.phase.value == "TEMPLATE_GENERATION":
            next_steps.append("Generate templates using file-creator agent")
            next_steps.append("Validate templates using template-validator")
        elif context.phase.value == "VALIDATION":
            next_steps.append("Review validation results")
            next_steps.append("Address any identified issues")
            next_steps.append("Proceed to completion phase")
        elif context.phase.value == "COMPLETION":
            next_steps.append("Review final deliverables")
            next_steps.append("Documentation and handoff")
        
        return next_steps


if __name__ == "__main__":
    """CLI interface for agents to invoke ToolCoordinator functionality."""
    import argparse
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    parser = argparse.ArgumentParser(description="PocketFlow Tools Coordinator")
    parser.add_argument("command", choices=["analyze", "deps", "graph", "validate", "handoff"])
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--requirements", help="Requirements text or file path")
    parser.add_argument("--pattern", help="Pattern type (RAG, AGENT, TOOL, etc.)")
    parser.add_argument("--template-dir", help="Template directory for validation")
    parser.add_argument("--complexity", default="medium", choices=["simple", "medium", "complex"])
    parser.add_argument("--output", choices=["json", "text"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    # Initialize coordinator
    coordinator = ToolCoordinator()
    
    try:
        if args.command == "analyze":
            if not args.requirements:
                parser.error("--requirements is required for analyze command")
            result = coordinator.analyze_pattern(args.project, args.requirements)
            
        elif args.command == "deps":
            if not args.pattern:
                parser.error("--pattern is required for deps command")
            result = coordinator.generate_dependencies(args.project, args.pattern)
            
        elif args.command == "graph":
            if not args.pattern:
                parser.error("--pattern is required for graph command")
            result = coordinator.generate_workflow_graph(
                args.pattern, args.requirements or "", args.complexity
            )
            
        elif args.command == "validate":
            if not args.template_dir:
                parser.error("--template-dir is required for validate command")
            result = coordinator.validate_templates(args.template_dir, args.pattern or "")
            
        else:  # handoff
            print("Handoff command requires interactive usage - not supported in CLI mode")
            sys.exit(1)
        
        # Output results
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            # Text output format
            if result.get("status") == "success":
                print(f"✅ {args.command.title()} completed successfully")
                if "pattern" in result:
                    print(f"Pattern: {result['pattern']}")
                if "confidence" in result:
                    print(f"Confidence: {result['confidence']:.2f}")
                if "target_agent" in result:
                    print(f"Next Agent: {result['target_agent']}")
            else:
                print(f"❌ {args.command.title()} failed: {result.get('error', 'Unknown error')}")
                sys.exit(1)
                
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)