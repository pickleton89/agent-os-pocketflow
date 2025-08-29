#!/usr/bin/env python3
"""
Validation Feedback Loop System

Provides intelligent feedback loops between validation results and template generation.
Implements Phase 2 feedback requirements from INTEGRATION_GAP.md.
"""

import json
import os
import logging
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import yaml

logger = logging.getLogger(__name__)


class FeedbackType(Enum):
    """Types of feedback that can be generated."""
    PATTERN_MISMATCH = "pattern_mismatch"
    MISSING_IMPLEMENTATION = "missing_implementation"
    DEPENDENCY_ISSUE = "dependency_issue"
    STRUCTURE_ISSUE = "structure_issue"
    CONTEXT_GAP = "context_gap"
    QUALITY_IMPROVEMENT = "quality_improvement"


@dataclass
class ValidationFeedback:
    """Structured feedback from validation results."""
    feedback_type: FeedbackType
    severity: str  # high, medium, low
    component: str  # Which component needs attention
    issue_description: str
    recommended_action: str
    automation_possible: bool = False
    context_needed: List[str] = field(default_factory=list)


@dataclass
class FeedbackLoop:
    """Complete feedback loop with context and actions."""
    workflow_name: str
    validation_issues: List[ValidationFeedback] = field(default_factory=list)
    context_gaps: List[str] = field(default_factory=list)
    suggested_iterations: List[Dict[str, Any]] = field(default_factory=list)
    auto_fix_actions: List[str] = field(default_factory=list)
    manual_review_needed: List[str] = field(default_factory=list)


class ValidationFeedbackAnalyzer:
    """Analyzes validation results and creates actionable feedback."""
    
    def __init__(self):
        self.feedback_patterns = self._load_feedback_patterns()
        
    def _load_feedback_patterns(self) -> Dict[str, Any]:
        """Load patterns for converting validation issues to actionable feedback."""
        return {
            "missing_todo_implementation": {
                "feedback_type": FeedbackType.MISSING_IMPLEMENTATION,
                "severity": "medium",
                "auto_fixable": False,
                "template": "TODO placeholder found in {component}: {detail}"
            },
            "import_error": {
                "feedback_type": FeedbackType.DEPENDENCY_ISSUE,
                "severity": "high",
                "auto_fixable": True,
                "template": "Missing dependency or import issue in {component}"
            },
            "pattern_mismatch": {
                "feedback_type": FeedbackType.PATTERN_MISMATCH,
                "severity": "high",
                "auto_fixable": False,
                "template": "Generated pattern doesn't match requirements in {component}"
            },
            "structure_issue": {
                "feedback_type": FeedbackType.STRUCTURE_ISSUE,
                "severity": "medium",
                "auto_fixable": True,
                "template": "File structure or organization issue in {component}"
            },
            "context_gap": {
                "feedback_type": FeedbackType.CONTEXT_GAP,
                "severity": "low",
                "auto_fixable": False,
                "template": "Additional context needed for {component}"
            }
        }

    def analyze_validation_results(self, validation_output_file: str, 
                                 context_file: Optional[str] = None,
                                 workflow_spec_file: Optional[str] = None) -> FeedbackLoop:
        """Analyze validation results and create feedback loop."""
        logger.info(f"Analyzing validation results from {validation_output_file}")
        
        # Parse validation output
        validation_issues = self._parse_validation_output(validation_output_file)
        
        # Load context if available
        context_data = self._load_context_data(context_file) if context_file else {}
        
        # Load workflow spec if available
        spec_data = self._load_spec_data(workflow_spec_file) if workflow_spec_file else {}
        
        # Create feedback loop
        feedback_loop = FeedbackLoop(
            workflow_name=spec_data.get('name', 'Unknown')
        )
        
        # Analyze each validation issue
        for issue in validation_issues:
            feedback = self._create_feedback_from_issue(issue, context_data, spec_data)
            if feedback:
                feedback_loop.validation_issues.append(feedback)
        
        # Identify context gaps
        feedback_loop.context_gaps = self._identify_context_gaps(
            validation_issues, context_data, spec_data
        )
        
        # Generate suggested iterations
        feedback_loop.suggested_iterations = self._generate_iteration_suggestions(
            feedback_loop.validation_issues, context_data
        )
        
        # Separate auto-fixable vs manual issues
        feedback_loop.auto_fix_actions = [
            f.recommended_action for f in feedback_loop.validation_issues 
            if f.automation_possible
        ]
        feedback_loop.manual_review_needed = [
            f.recommended_action for f in feedback_loop.validation_issues 
            if not f.automation_possible
        ]
        
        return feedback_loop

    def _parse_validation_output(self, output_file: str) -> List[Dict[str, Any]]:
        """Parse validation output file and extract issues."""
        issues = []
        
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse different validation output formats
            if content.strip().startswith('{'):
                # JSON format
                data = json.loads(content)
                if isinstance(data, dict) and 'issues' in data:
                    issues = data['issues']
                elif isinstance(data, list):
                    issues = data
            else:
                # Text format - parse line by line
                issues = self._parse_text_validation_output(content)
                
        except Exception as e:
            logger.warning(f"Could not parse validation output: {e}")
            
        return issues

    def _parse_text_validation_output(self, content: str) -> List[Dict[str, Any]]:
        """Parse text-based validation output."""
        issues = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Look for common validation patterns
            if 'ERROR' in line.upper():
                issues.append({
                    'level': 'error',
                    'message': line,
                    'category': 'general_error'
                })
            elif 'WARNING' in line.upper():
                issues.append({
                    'level': 'warning',
                    'message': line,
                    'category': 'general_warning'
                })
            elif 'TODO' in line.upper():
                issues.append({
                    'level': 'info',
                    'message': line,
                    'category': 'missing_implementation'
                })
            elif 'IMPORT' in line.upper() and ('ERROR' in line.upper() or 'FAIL' in line.upper()):
                issues.append({
                    'level': 'error',
                    'message': line,
                    'category': 'import_error'
                })
                
        return issues

    def _load_context_data(self, context_file: str) -> Dict[str, Any]:
        """Load context data from file."""
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load context data: {e}")
            return {}

    def _load_spec_data(self, spec_file: str) -> Dict[str, Any]:
        """Load workflow specification data."""
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                if spec_file.endswith('.yaml') or spec_file.endswith('.yml'):
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load spec data: {e}")
            return {}

    def _create_feedback_from_issue(self, issue: Dict[str, Any], 
                                   context_data: Dict[str, Any],
                                   spec_data: Dict[str, Any]) -> Optional[ValidationFeedback]:
        """Create structured feedback from a validation issue."""
        category = issue.get('category', 'unknown')
        message = issue.get('message', '')
        level = issue.get('level', 'info')
        
        if category == 'missing_implementation' or 'TODO' in message:
            return ValidationFeedback(
                feedback_type=FeedbackType.MISSING_IMPLEMENTATION,
                severity="medium",
                component=self._extract_component_from_message(message),
                issue_description=f"TODO placeholder needs implementation: {message}",
                recommended_action="Review requirements and implement placeholder function",
                automation_possible=False,
                context_needed=self._get_relevant_context_for_todo(message, context_data)
            )
        elif category == 'import_error' or 'import' in message.lower():
            return ValidationFeedback(
                feedback_type=FeedbackType.DEPENDENCY_ISSUE,
                severity="high",
                component=self._extract_component_from_message(message),
                issue_description=f"Import or dependency issue: {message}",
                recommended_action="Check dependency installation and import paths",
                automation_possible=True,
                context_needed=["technical_stack", "dependencies"]
            )
        elif level == 'error':
            return ValidationFeedback(
                feedback_type=FeedbackType.STRUCTURE_ISSUE,
                severity="high",
                component=self._extract_component_from_message(message),
                issue_description=f"Validation error: {message}",
                recommended_action="Review and fix structural issues",
                automation_possible=False
            )
        
        return None

    def _extract_component_from_message(self, message: str) -> str:
        """Extract component name from validation message."""
        # Look for file paths or component names in the message
        
        # Match file paths
        file_match = re.search(r'(\w+\.py)', message)
        if file_match:
            return file_match.group(1)
        
        # Match function/class names
        func_match = re.search(r'(\w+\.\w+|\w+)', message)
        if func_match:
            return func_match.group(1)
        
        return "unknown_component"

    def _get_relevant_context_for_todo(self, message: str, 
                                     context_data: Dict[str, Any]) -> List[str]:
        """Get relevant context information for TODO implementation."""
        context_needed = []
        
        message_lower = message.lower()
        
        if 'database' in message_lower or 'storage' in message_lower:
            context_needed.extend(["technical_stack", "requirements"])
        if 'api' in message_lower or 'endpoint' in message_lower:
            context_needed.extend(["integration_needs", "technical_requirements"])
        if 'process' in message_lower or 'workflow' in message_lower:
            context_needed.extend(["functional_requirements", "patterns_detected"])
        
        # Add specific requirements that might help
        for req in context_data.get('requirements', []):
            if any(word in req.get('text', '').lower() for word in ['database', 'api', 'process']):
                context_needed.append(f"requirement: {req.get('text', '')[:50]}...")
        
        return list(set(context_needed))  # Remove duplicates

    def _identify_context_gaps(self, validation_issues: List[Dict[str, Any]], 
                             context_data: Dict[str, Any],
                             spec_data: Dict[str, Any]) -> List[str]:
        """Identify gaps in context that might help resolve issues."""
        gaps = []
        
        # Check if we have enough requirements
        if len(context_data.get('requirements', [])) < 3:
            gaps.append("Insufficient requirements - consider adding more detailed specifications")
        
        # Check technical stack coverage
        if len(context_data.get('technical_stack', [])) == 0:
            gaps.append("No technical stack specified - may cause dependency issues")
        
        # Check for pattern clarity
        if len(context_data.get('patterns_detected', [])) == 0:
            gaps.append("No clear patterns detected - may need more specific requirements")
        
        return gaps

    def _generate_iteration_suggestions(self, feedback_issues: List[ValidationFeedback],
                                      context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate suggestions for iterative improvements."""
        suggestions = []
        
        # Group issues by type
        issue_types = {}
        for issue in feedback_issues:
            if issue.feedback_type not in issue_types:
                issue_types[issue.feedback_type] = []
            issue_types[issue.feedback_type].append(issue)
        
        # Generate type-specific suggestions
        if FeedbackType.MISSING_IMPLEMENTATION in issue_types:
            suggestions.append({
                "type": "implementation_iteration",
                "priority": "high",
                "description": "Focus on implementing TODO placeholders",
                "actions": [
                    "Review context requirements for each TODO",
                    "Implement core functionality first",
                    "Add error handling and validation"
                ],
                "estimated_effort": "medium"
            })
        
        if FeedbackType.DEPENDENCY_ISSUE in issue_types:
            suggestions.append({
                "type": "dependency_iteration",
                "priority": "high",
                "description": "Resolve dependency and import issues",
                "actions": [
                    "Run dependency orchestrator again",
                    "Check Python path and imports",
                    "Validate package installations"
                ],
                "estimated_effort": "low"
            })
        
        if FeedbackType.PATTERN_MISMATCH in issue_types:
            suggestions.append({
                "type": "pattern_refinement",
                "priority": "medium",
                "description": "Refine pattern selection and implementation",
                "actions": [
                    "Re-analyze requirements with pattern analyzer",
                    "Consider hybrid pattern approach",
                    "Review generated template structure"
                ],
                "estimated_effort": "high"
            })
        
        return suggestions

    def create_feedback_report(self, feedback_loop: FeedbackLoop, 
                             output_file: str):
        """Create a comprehensive feedback report."""
        report = {
            "workflow_name": feedback_loop.workflow_name,
            "summary": {
                "total_issues": len(feedback_loop.validation_issues),
                "auto_fixable": len(feedback_loop.auto_fix_actions),
                "manual_review": len(feedback_loop.manual_review_needed),
                "context_gaps": len(feedback_loop.context_gaps)
            },
            "validation_issues": [
                {
                    "type": issue.feedback_type.value,
                    "severity": issue.severity,
                    "component": issue.component,
                    "description": issue.issue_description,
                    "action": issue.recommended_action,
                    "auto_fixable": issue.automation_possible,
                    "context_needed": issue.context_needed
                }
                for issue in feedback_loop.validation_issues
            ],
            "context_gaps": feedback_loop.context_gaps,
            "iteration_suggestions": feedback_loop.suggested_iterations,
            "immediate_actions": {
                "auto_fix": feedback_loop.auto_fix_actions,
                "manual_review": feedback_loop.manual_review_needed
            }
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Feedback report saved to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save feedback report: {e}")

    def create_markdown_report(self, feedback_loop: FeedbackLoop, 
                             output_file: str):
        """Create a human-readable markdown feedback report."""
        report_lines = [
            f"# Validation Feedback Report: {feedback_loop.workflow_name}",
            "",
            "## Summary",
            f"- **Total Issues**: {len(feedback_loop.validation_issues)}",
            f"- **Auto-fixable**: {len(feedback_loop.auto_fix_actions)}",
            f"- **Manual Review**: {len(feedback_loop.manual_review_needed)}",
            f"- **Context Gaps**: {len(feedback_loop.context_gaps)}",
            "",
            "## Validation Issues",
            ""
        ]
        
        for i, issue in enumerate(feedback_loop.validation_issues, 1):
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue.severity, "⚪")
            auto_fix_emoji = "🤖" if issue.automation_possible else "👤"
            
            report_lines.extend([
                f"### {i}. {issue.component} {severity_emoji} {auto_fix_emoji}",
                f"**Type**: {issue.feedback_type.value}",
                f"**Description**: {issue.issue_description}",
                f"**Recommended Action**: {issue.recommended_action}",
                ""
            ])
            
            if issue.context_needed:
                report_lines.extend([
                    "**Context Needed**:",
                    *[f"- {ctx}" for ctx in issue.context_needed],
                    ""
                ])
        
        if feedback_loop.context_gaps:
            report_lines.extend([
                "## Context Gaps",
                "",
                *[f"- {gap}" for gap in feedback_loop.context_gaps],
                ""
            ])
        
        if feedback_loop.suggested_iterations:
            report_lines.extend([
                "## Iteration Suggestions",
                ""
            ])
            
            for suggestion in feedback_loop.suggested_iterations:
                priority_emoji = {"high": "🔥", "medium": "⚡", "low": "💡"}.get(
                    suggestion.get('priority', 'medium'), "💡"
                )
                
                report_lines.extend([
                    f"### {suggestion.get('description', 'Suggestion')} {priority_emoji}",
                    f"**Effort**: {suggestion.get('estimated_effort', 'unknown')}",
                    "",
                    "**Actions**:",
                    *[f"- {action}" for action in suggestion.get('actions', [])],
                    ""
                ])
        
        report_content = "\n".join(report_lines)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            logger.info(f"Markdown feedback report saved to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save markdown report: {e}")


def main():
    """CLI interface for validation feedback analyzer."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze validation results and create feedback loops")
    parser.add_argument("validation_output", help="Validation output file")
    parser.add_argument("--context", "-c", help="Context analysis file (JSON)")
    parser.add_argument("--spec", "-s", help="Workflow specification file")
    parser.add_argument("--output", "-o", default="validation_feedback.json",
                       help="Output file for feedback report")
    parser.add_argument("--markdown", "-m", 
                       help="Output file for markdown report")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Analyze validation results
    analyzer = ValidationFeedbackAnalyzer()
    feedback_loop = analyzer.analyze_validation_results(
        args.validation_output,
        args.context,
        args.spec
    )
    
    # Create reports
    analyzer.create_feedback_report(feedback_loop, args.output)
    
    if args.markdown:
        analyzer.create_markdown_report(feedback_loop, args.markdown)
    
    # Print summary
    print(f"\n=== Validation Feedback Summary ===")
    print(f"Workflow: {feedback_loop.workflow_name}")
    print(f"Issues found: {len(feedback_loop.validation_issues)}")
    print(f"Auto-fixable: {len(feedback_loop.auto_fix_actions)}")
    print(f"Manual review needed: {len(feedback_loop.manual_review_needed)}")
    print(f"Context gaps: {len(feedback_loop.context_gaps)}")
    print(f"Iteration suggestions: {len(feedback_loop.suggested_iterations)}")


if __name__ == "__main__":
    main()