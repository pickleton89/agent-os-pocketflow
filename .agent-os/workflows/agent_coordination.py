#!/usr/bin/env python3
"""
Agent Coordination System for Pattern Recognizer

Handles coordination between pattern-recognizer and pocketflow-orchestrator agents.
Implements handoff protocols and pattern override capabilities.
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from pattern_analyzer import PatternRecommendation, PatternType

logger = logging.getLogger(__name__)


class CoordinationPhase(Enum):
    """Phases of agent coordination."""
    PATTERN_ANALYSIS = "pattern_analysis"
    ORCHESTRATOR_PLANNING = "orchestrator_planning"
    TEMPLATE_GENERATION = "template_generation"
    VALIDATION = "validation"
    COMPLETION = "completion"


@dataclass
class CoordinationContext:
    """Context information for agent coordination."""
    phase: CoordinationPhase
    project_name: str
    requirements: str
    pattern_recommendation: Optional[PatternRecommendation] = None
    orchestrator_feedback: Optional[Dict[str, Any]] = None
    user_overrides: Optional[Dict[str, Any]] = None
    coordination_history: List[str] = None
    
    def __post_init__(self):
        if self.coordination_history is None:
            self.coordination_history = []


@dataclass
class HandoffPackage:
    """Package of information for handoff between agents."""
    source_agent: str
    target_agent: str
    payload: Dict[str, Any]
    coordination_context: CoordinationContext
    handoff_type: str  # "analysis_to_orchestrator", "orchestrator_to_validator", etc.


class PatternOverrideManager:
    """Manages pattern overrides and user preferences."""
    
    def __init__(self):
        self.override_rules = self._load_override_rules()
    
    def _load_override_rules(self) -> Dict[str, Any]:
        """Load pattern override rules and preferences."""
        return {
            "preference_weights": {
                PatternType.RAG: 1.0,
                PatternType.AGENT: 1.0,
                PatternType.TOOL: 1.0,
                PatternType.WORKFLOW: 1.0,
                PatternType.MAPREDUCE: 0.8,  # Slightly discouraged unless clear need
                PatternType.MULTI_AGENT: 0.7,  # More complex, needs justification
                PatternType.STRUCTURED_OUTPUT: 1.0
            },
            "complexity_thresholds": {
                "simple": {"max_nodes": 4, "max_utilities": 3},
                "medium": {"max_nodes": 8, "max_utilities": 6},
                "complex": {"max_nodes": 15, "max_utilities": 10}
            },
            "pattern_conflicts": {
                # Patterns that shouldn't be combined
                PatternType.WORKFLOW: [PatternType.MULTI_AGENT],
                PatternType.MAPREDUCE: [PatternType.AGENT]
            }
        }
    
    def apply_user_overrides(self, recommendation: PatternRecommendation, 
                           user_overrides: Dict[str, Any]) -> PatternRecommendation:
        """Apply user overrides to pattern recommendation."""
        
        if not user_overrides:
            return recommendation
        
        logger.info("Applying user overrides to pattern recommendation")
        
        # Pattern override
        if "force_pattern" in user_overrides:
            forced_pattern = PatternType(user_overrides["force_pattern"])
            logger.info(f"User forced pattern: {forced_pattern.value}")
            
            recommendation.primary_pattern = forced_pattern
            recommendation.confidence_score = min(recommendation.confidence_score, 0.8)  # Reduce confidence for forced patterns
            recommendation.rationale += f" [USER OVERRIDE: Pattern forced to {forced_pattern.value}]"
        
        # Complexity override
        if "complexity_preference" in user_overrides:
            complexity = user_overrides["complexity_preference"]
            logger.info(f"User complexity preference: {complexity}")
            
            estimated_nodes = recommendation.workflow_suggestions.get("estimated_nodes", 4)
            if complexity == "simple" and estimated_nodes > 4:
                # Simplify the workflow
                recommendation.template_customizations["simplify"] = True
                recommendation.workflow_suggestions["estimated_nodes"] = 4
        
        # Feature overrides
        if "disable_features" in user_overrides:
            disabled = user_overrides["disable_features"]
            for feature in disabled:
                recommendation.template_customizations[f"disable_{feature}"] = True
                logger.info(f"Disabled feature: {feature}")
        
        return recommendation
    
    def validate_pattern_combination(self, primary: PatternType, 
                                   secondary: List[PatternType]) -> bool:
        """Validate that pattern combinations are compatible."""
        
        conflicts = self.override_rules.get("pattern_conflicts", {})
        
        if primary in conflicts:
            conflicting_patterns = conflicts[primary]
            for secondary_pattern in secondary:
                if secondary_pattern in conflicting_patterns:
                    logger.warning(f"Pattern conflict detected: {primary.value} + {secondary_pattern.value}")
                    return False
        
        return True


class AgentCoordinator:
    """Coordinates between pattern-recognizer and pocketflow-orchestrator agents."""
    
    def __init__(self):
        self.override_manager = PatternOverrideManager()
        self.coordination_log = []
    
    def create_handoff_to_orchestrator(self, context: CoordinationContext) -> HandoffPackage:
        """Create handoff package from pattern-recognizer to pocketflow-orchestrator."""
        
        logger.info("Creating handoff package for pocketflow-orchestrator")
        
        if not context.pattern_recommendation:
            raise ValueError("Pattern recommendation required for orchestrator handoff")
        
        # Prepare payload for orchestrator
        payload = {
            "project_name": context.project_name,
            "requirements": context.requirements,
            "pattern_analysis": {
                "primary_pattern": context.pattern_recommendation.primary_pattern.value,
                "confidence_score": context.pattern_recommendation.confidence_score,
                "secondary_patterns": [p.value for p in context.pattern_recommendation.secondary_patterns],
                "rationale": context.pattern_recommendation.rationale,
                "detailed_justification": getattr(context.pattern_recommendation, 'detailed_justification', ''),
                "template_customizations": context.pattern_recommendation.template_customizations,
                "workflow_suggestions": context.pattern_recommendation.workflow_suggestions
            },
            "coordination_metadata": {
                "phase": context.phase.value,
                "timestamp": self._get_timestamp(),
                "coordination_id": self._generate_coordination_id(),
                "user_overrides_applied": bool(context.user_overrides)
            }
        }
        
        handoff = HandoffPackage(
            source_agent="pattern-recognizer",
            target_agent="pocketflow-orchestrator",
            payload=payload,
            coordination_context=context,
            handoff_type="analysis_to_orchestrator"
        )
        
        self._log_coordination("handoff_created", handoff.handoff_type, payload["coordination_metadata"]["coordination_id"])
        
        return handoff
    
    def process_orchestrator_feedback(self, handoff: HandoffPackage, 
                                    orchestrator_response: Dict[str, Any]) -> CoordinationContext:
        """Process feedback from pocketflow-orchestrator."""
        
        logger.info("Processing orchestrator feedback")
        
        context = handoff.coordination_context
        context.orchestrator_feedback = orchestrator_response
        
        # Check for pattern modifications from orchestrator
        if "pattern_modifications" in orchestrator_response:
            modifications = orchestrator_response["pattern_modifications"]
            logger.info(f"Orchestrator suggested pattern modifications: {modifications}")
            
            # Apply modifications to pattern recommendation
            if "complexity_adjustment" in modifications:
                new_complexity = modifications["complexity_adjustment"]
                context.pattern_recommendation.template_customizations["complexity"] = new_complexity
            
            if "additional_nodes" in modifications:
                additional_nodes = modifications["additional_nodes"]
                context.pattern_recommendation.workflow_suggestions["additional_nodes"] = additional_nodes
        
        # Update coordination history
        context.coordination_history.append(f"Orchestrator feedback processed: {orchestrator_response.get('status', 'unknown')}")
        
        # Determine next phase
        if orchestrator_response.get("status") == "approved":
            context.phase = CoordinationPhase.TEMPLATE_GENERATION
        elif orchestrator_response.get("status") == "needs_revision":
            context.phase = CoordinationPhase.PATTERN_ANALYSIS  # Go back to analysis
        else:
            context.phase = CoordinationPhase.ORCHESTRATOR_PLANNING  # Stay in planning
        
        self._log_coordination("feedback_processed", f"status_{orchestrator_response.get('status')}", context.coordination_history[-1])
        
        return context
    
    def handle_pattern_override_request(self, context: CoordinationContext, 
                                      override_request: Dict[str, Any]) -> CoordinationContext:
        """Handle user pattern override requests."""
        
        logger.info(f"Handling pattern override request: {override_request}")
        
        # Validate override request
        if "pattern" in override_request:
            try:
                requested_pattern = PatternType(override_request["pattern"])
                logger.info(f"User requested pattern override to: {requested_pattern.value}")
            except ValueError:
                logger.error(f"Invalid pattern requested: {override_request['pattern']}")
                return context
        
        # Apply overrides using override manager
        context.user_overrides = override_request
        if context.pattern_recommendation:
            context.pattern_recommendation = self.override_manager.apply_user_overrides(
                context.pattern_recommendation,
                override_request
            )
        
        # Update coordination history
        context.coordination_history.append(f"Pattern override applied: {override_request}")
        
        # Reset to pattern analysis phase to re-evaluate
        context.phase = CoordinationPhase.PATTERN_ANALYSIS
        
        self._log_coordination("override_applied", "pattern_override", str(override_request))
        
        return context
    
    def create_coordination_summary(self, context: CoordinationContext) -> Dict[str, Any]:
        """Create a summary of the coordination process."""
        
        summary = {
            "project_name": context.project_name,
            "final_phase": context.phase.value,
            "pattern_selected": context.pattern_recommendation.primary_pattern.value if context.pattern_recommendation else "none",
            "confidence_score": context.pattern_recommendation.confidence_score if context.pattern_recommendation else 0.0,
            "user_overrides_applied": bool(context.user_overrides),
            "orchestrator_involved": bool(context.orchestrator_feedback),
            "coordination_steps": len(context.coordination_history),
            "coordination_log": context.coordination_history,
            "final_customizations": context.pattern_recommendation.template_customizations if context.pattern_recommendation else {},
            "success": context.phase == CoordinationPhase.COMPLETION
        }
        
        self._log_coordination("summary_generated", "coordination_complete", summary["pattern_selected"])
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
    
    def _generate_coordination_id(self) -> str:
        """Generate unique coordination ID."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _log_coordination(self, action: str, event_type: str, details: str):
        """Log coordination events."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "action": action,
            "event_type": event_type,
            "details": details
        }
        self.coordination_log.append(log_entry)
        logger.debug(f"Coordination logged: {action} - {event_type} - {details}")


# Convenience functions for easy integration

def coordinate_pattern_analysis(project_name: str, requirements: str, 
                              user_overrides: Optional[Dict[str, Any]] = None) -> CoordinationContext:
    """High-level function to coordinate pattern analysis with orchestrator."""
    
    from pattern_analyzer import PatternAnalyzer
    
    logger.info(f"Starting pattern analysis coordination for project: {project_name}")
    
    # Initialize coordination context
    context = CoordinationContext(
        phase=CoordinationPhase.PATTERN_ANALYSIS,
        project_name=project_name,
        requirements=requirements,
        user_overrides=user_overrides
    )
    
    # Perform pattern analysis
    analyzer = PatternAnalyzer()
    recommendation = analyzer.analyze_and_recommend(requirements)
    
    # Apply user overrides if provided
    coordinator = AgentCoordinator()
    if user_overrides:
        recommendation = coordinator.override_manager.apply_user_overrides(recommendation, user_overrides)
    
    context.pattern_recommendation = recommendation
    context.phase = CoordinationPhase.ORCHESTRATOR_PLANNING
    
    logger.info(f"Pattern analysis completed: {recommendation.primary_pattern.value} (confidence: {recommendation.confidence_score:.2f})")
    
    return context


def create_orchestrator_handoff(context: CoordinationContext) -> HandoffPackage:
    """Create handoff package for pocketflow-orchestrator."""
    
    coordinator = AgentCoordinator()
    return coordinator.create_handoff_to_orchestrator(context)


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test coordination workflow
    test_requirements = """
    Create a document processing system that can:
    1. Accept PDF documents and extract text content
    2. Use AI to analyze and categorize the documents 
    3. Store processed documents with metadata in a vector database
    4. Provide REST API endpoints for document upload and search
    5. Return relevant documents based on semantic similarity queries
    """
    
    # Test basic coordination
    context = coordinate_pattern_analysis(
        project_name="SmartDocProcessor",
        requirements=test_requirements
    )
    
    print(f"Pattern Analysis Result: {context.pattern_recommendation.primary_pattern.value}")
    print(f"Confidence: {context.pattern_recommendation.confidence_score:.2f}")
    
    # Test handoff creation
    handoff = create_orchestrator_handoff(context)
    print(f"Handoff created: {handoff.source_agent} -> {handoff.target_agent}")
    print(f"Payload keys: {list(handoff.payload.keys())}")
    
    # Test pattern override
    coordinator = AgentCoordinator()
    override_request = {"force_pattern": "TOOL", "complexity_preference": "simple"}
    updated_context = coordinator.handle_pattern_override_request(context, override_request)
    print(f"After override: {updated_context.pattern_recommendation.primary_pattern.value}")
    
    # Generate final summary
    summary = coordinator.create_coordination_summary(updated_context)
    print(f"Coordination Summary: {summary['success']} - {summary['coordination_steps']} steps")