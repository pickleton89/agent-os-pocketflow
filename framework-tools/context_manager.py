#!/usr/bin/env python3
"""
Context Manager for Planning-to-Implementation Handoff

Role: Extracts project context from repository docs (requirements, design,
architecture) to inform PocketFlow generation inputs. This is a design-time
content extractor, not a runtime coordinator.

Do not confuse this with `agent_coordination.CoordinationContext`, which
represents runtime coordination state during agent handoffs and orchestration.

Implements Phase 2 requirements per docs/POCKETFLOW_ORCHESTRATOR_UPDATE_PLAN.md.
"""

import re
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class DocumentType(Enum):
    """Types of planning documents we can process."""

    REQUIREMENTS = "requirements"
    ROADMAP = "roadmap"
    DESIGN = "design"
    ARCHITECTURE = "architecture"
    USER_STORIES = "user_stories"
    TECHNICAL_SPEC = "technical_spec"
    API_SPEC = "api_spec"


@dataclass
class ExtractedRequirement:
    """A single extracted requirement with context."""

    text: str
    type: str  # functional, technical, performance, etc.
    priority: str  # high, medium, low
    source_file: str
    confidence: float
    patterns: List[str] = field(default_factory=list)


@dataclass
class ProjectContext:
    """Complete project context extracted from design documents."""

    project_name: str
    description: str
    requirements: List[ExtractedRequirement] = field(default_factory=list)
    technical_stack: List[str] = field(default_factory=list)
    patterns_detected: List[str] = field(default_factory=list)
    complexity_indicators: List[str] = field(default_factory=list)
    integration_needs: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    source_documents: List[str] = field(default_factory=list)


class ContextManager:
    """Manages context extraction and handoff between planning and implementation."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"

        # Pattern recognition for different types of requirements
        self.requirement_patterns = {
            "functional": [
                r"(?:user|system|application) (?:shall|should|must|will) (.+)",
                r"the system (?:provides|enables|supports|allows) (.+)",
                r"users (?:can|are able to|should be able to) (.+)",
                r"(?:feature|capability|function).*?:\s*(.+)",
            ],
            "technical": [
                r"(?:using|with|built on|implemented in|requires) (.+)",
                r"(?:database|storage|framework|library|api|service).*?:\s*(.+)",
                r"(?:performance|scalability|security|reliability) (.+)",
                r"integration with (.+)",
            ],
            "constraint": [
                r"(?:constraint|limitation|restriction).*?:\s*(.+)",
                r"(?:cannot|must not|should not) (.+)",
                r"(?:limited to|within|bounded by) (.+)",
            ],
        }

        # Pattern indicators for PocketFlow patterns
        self.pocketflow_indicators = {
            "RAG": [
                "search",
                "retrieval",
                "knowledge",
                "document",
                "query",
                "semantic",
                "vector",
                "embedding",
                "similarity",
            ],
            "AGENT": [
                "agent",
                "intelligent",
                "autonomous",
                "decision",
                "reasoning",
                "planning",
                "goal",
                "task",
                "conversation",
            ],
            "WORKFLOW": [
                "workflow",
                "process",
                "pipeline",
                "sequence",
                "orchestration",
                "automation",
                "batch",
                "job",
                "scheduling",
            ],
            "TOOL": [
                "tool",
                "utility",
                "function",
                "operation",
                "action",
                "command",
                "execute",
                "invoke",
            ],
            "MULTI_AGENT": [
                "multi-agent",
                "multiple agents",
                "agent collaboration",
                "distributed",
                "coordination",
                "communication",
            ],
        }

    def extract_project_context(
        self, workflow_name: Optional[str] = None
    ) -> ProjectContext:
        """Extract complete project context from design documents."""
        logger.info(f"Extracting project context from {self.docs_dir}")

        if not self.docs_dir.exists():
            logger.warning(f"No docs directory found at {self.docs_dir}")
            return self._create_minimal_context(workflow_name or "UnknownWorkflow")

        context = ProjectContext(
            project_name=workflow_name or self._infer_project_name(),
            description="",
            source_documents=[],
        )

        # Process all relevant documents
        for doc_file in self.docs_dir.glob("**/*.md"):
            logger.debug(f"Processing document: {doc_file}")
            try:
                doc_content = doc_file.read_text(encoding="utf-8")
                doc_type = self._classify_document(doc_file, doc_content)

                context.source_documents.append(
                    str(doc_file.relative_to(self.project_root))
                )

                # Extract content based on document type
                if doc_type == DocumentType.REQUIREMENTS:
                    self._extract_requirements(doc_content, str(doc_file), context)
                    # Also extract technical info from requirements docs
                    self._extract_design_info(doc_content, context)
                elif doc_type == DocumentType.ROADMAP:
                    self._extract_roadmap_info(doc_content, context)
                elif doc_type == DocumentType.DESIGN:
                    self._extract_design_info(doc_content, context)
                elif doc_type == DocumentType.ARCHITECTURE:
                    self._extract_architecture_info(doc_content, context)
                    # Also extract technical info from architecture docs
                    self._extract_design_info(doc_content, context)

            except Exception as e:
                logger.warning(f"Error processing {doc_file}: {e}")
                continue

        # Analyze patterns and complexity
        self._analyze_patterns(context)
        self._assess_complexity(context)

        return context

    def _canonicalize_tech(self, name: str) -> str:
        """Return a canonical display name for common tech terms."""
        mapping = {
            "fastapi": "FastAPI",
            "rest api": "REST API",
            "aws s3": "AWS S3",
            "openai": "OpenAI",
            "postgresql": "PostgreSQL",
            "mongodb": "MongoDB",
            "chromadb": "ChromaDB",
        }
        key = name.strip().lower()
        return mapping.get(key, name.title())

    def _create_minimal_context(self, workflow_name: str) -> ProjectContext:
        """Create minimal context when no design documents exist."""
        return ProjectContext(
            project_name=workflow_name,
            description=f"Workflow implementation for {workflow_name}",
            source_documents=[],
        )

    def _infer_project_name(self) -> str:
        """Infer project name from directory structure or documents."""
        # Try to get from current directory name
        project_name = self.project_root.name

        # Look for project name in documents
        readme_files = list(self.project_root.glob("README*"))
        if readme_files:
            try:
                content = readme_files[0].read_text(encoding="utf-8")
                # Look for title patterns
                title_match = re.search(r"^#\s*(.+)$", content, re.MULTILINE)
                if title_match:
                    project_name = title_match.group(1).strip()
            except Exception:
                pass

        return project_name

    def _classify_document(self, file_path: Path, content: str) -> DocumentType:
        """Classify document type based on filename and content."""
        filename = file_path.name.lower()
        content_lower = content.lower()

        if "requirement" in filename or "spec" in filename:
            return DocumentType.REQUIREMENTS
        elif "roadmap" in filename or "plan" in filename:
            return DocumentType.ROADMAP
        elif "design" in filename:
            return DocumentType.DESIGN
        elif "architecture" in filename or "arch" in filename:
            return DocumentType.ARCHITECTURE
        elif "story" in filename or "user" in filename:
            return DocumentType.USER_STORIES
        elif "api" in filename:
            return DocumentType.API_SPEC

        # Analyze content for classification
        if re.search(r"(?:user story|as a|i want|so that)", content_lower):
            return DocumentType.USER_STORIES
        elif re.search(r"(?:architecture|system design|component)", content_lower):
            return DocumentType.ARCHITECTURE
        elif re.search(r"(?:api|endpoint|request|response)", content_lower):
            return DocumentType.API_SPEC
        elif re.search(r"(?:requirement|shall|must|should)", content_lower):
            return DocumentType.REQUIREMENTS

        return DocumentType.DESIGN  # Default classification

    def _extract_requirements(
        self, content: str, source_file: str, context: ProjectContext
    ):
        """Extract requirements from document content."""
        logger.debug(f"Extracting requirements from {source_file}")

        for req_type, patterns in self.requirement_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    requirement_text = match.group(1).strip()
                    if len(requirement_text) > 10:  # Filter out very short matches
                        req = ExtractedRequirement(
                            text=requirement_text,
                            type=req_type,
                            priority=self._infer_priority(requirement_text),
                            source_file=source_file,
                            confidence=0.8,
                        )
                        context.requirements.append(req)

        # Extract list-based requirements (bullet points, numbered lists)
        list_patterns = [
            r"^\s*[-*+]\s*(.+)$",  # Bullet points
            r"^\s*\d+\.\s*(.+)$",  # Numbered lists
        ]

        for pattern in list_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                requirement_text = match.group(1).strip()
                if len(requirement_text) > 15 and any(
                    word in requirement_text.lower()
                    for word in ["must", "should", "will", "can"]
                ):
                    req = ExtractedRequirement(
                        text=requirement_text,
                        type="functional",
                        priority=self._infer_priority(requirement_text),
                        source_file=source_file,
                        confidence=0.6,
                    )
                    context.requirements.append(req)

    def _extract_roadmap_info(self, content: str, context: ProjectContext):
        """Extract roadmap and planning information."""
        # Look for phases, milestones, and deliverables
        phase_pattern = r"(?:phase|milestone|deliverable|sprint).*?:\s*(.+)"
        matches = re.finditer(phase_pattern, content, re.IGNORECASE)

        for match in matches:
            context.complexity_indicators.append(
                f"Planned phase: {match.group(1).strip()}"
            )

    def _extract_design_info(self, content: str, context: ProjectContext):
        """Extract design and architecture information."""
        # Extract technical stack mentions - patterns with capture groups
        capture_patterns = [
            r"(?:using|with|built on|framework|library|database|technology).*?:\s*(.+)",
            r"- (.+(?:API|framework|database|service|library|tool))",
            r"### (.+(?:Stack|Technology|Framework))",
        ]

        # Patterns without capture groups - match entire expression
        whole_match_patterns = [
            r"(?:python|javascript|react|node|django|flask|fastapi|postgresql|mongodb|redis|docker|chromadb|openai)(?:\s+[\w.]+)?"
        ]

        content_lower = content.lower()

        # Process patterns with capture groups
        for pattern in capture_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if match.group(1):  # First capture group
                    tech = match.group(1).strip()

                    # Clean up the tech name
                    tech = tech.split("\n")[0]  # Take only first line
                    tech = tech.strip("- .")  # Remove list markers

                    if len(tech) > 2 and tech not in context.technical_stack:
                        context.technical_stack.append(tech)

        # Process patterns without capture groups
        for pattern in whole_match_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                tech = match.group(0).strip()

                # Clean up the tech name
                tech = tech.split("\n")[0]  # Take only first line
                tech = tech.strip("- .")  # Remove list markers

                if len(tech) > 2 and tech not in context.technical_stack:
                    context.technical_stack.append(tech)

        # Also look for common technology keywords directly
        common_techs = [
            "python",
            "javascript",
            "react",
            "fastapi",
            "django",
            "flask",
            "postgresql",
            "mongodb",
            "redis",
            "docker",
            "chromadb",
            "openai",
            "aws s3",
            "google drive",
            "vector database",
            "rest api",
        ]

        # Create lowercase set for efficient duplicate checking
        existing_techs_lower = {t.lower() for t in context.technical_stack}

        for tech in common_techs:
            if tech in content_lower and tech not in existing_techs_lower:
                tech_canonical = self._canonicalize_tech(tech)
                context.technical_stack.append(tech_canonical)
                existing_techs_lower.add(
                    tech.lower()
                )  # Update set with lowercase for consistency

    def _extract_architecture_info(self, content: str, context: ProjectContext):
        """Extract architectural patterns and constraints."""
        # Look for architectural patterns and integration needs
        integration_patterns = [
            r"integrat(?:e|ion) with (.+)",
            r"connect to (.+)",
            r"(?:api|service|system) (.+)",
        ]

        for pattern in integration_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                integration = match.group(1).strip()
                if integration not in context.integration_needs:
                    context.integration_needs.append(integration)

    def _infer_priority(self, text: str) -> str:
        """Infer priority from requirement text."""
        text_lower = text.lower()

        if any(
            word in text_lower for word in ["critical", "must", "required", "essential"]
        ):
            return "high"
        elif any(word in text_lower for word in ["should", "important", "preferred"]):
            return "medium"
        elif any(word in text_lower for word in ["could", "optional", "nice to have"]):
            return "low"

        return "medium"  # Default priority

    def _analyze_patterns(self, context: ProjectContext):
        """Analyze content to detect PocketFlow patterns."""
        # Combine all requirement text for pattern analysis
        all_text = " ".join([req.text for req in context.requirements])
        all_text += " " + context.description
        all_text = all_text.lower()

        for pattern_name, indicators in self.pocketflow_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in all_text)
            if matches >= 2:  # Threshold for pattern detection
                context.patterns_detected.append(pattern_name)
                logger.debug(
                    f"Detected pattern {pattern_name} with {matches} indicators"
                )

    def _assess_complexity(self, context: ProjectContext):
        """Assess project complexity based on extracted information."""
        complexity_factors = []

        # Number of requirements
        if len(context.requirements) > 20:
            complexity_factors.append("High requirement count")
        elif len(context.requirements) > 10:
            complexity_factors.append("Moderate requirement count")

        # Technical stack diversity
        if len(context.technical_stack) > 5:
            complexity_factors.append("Complex technical stack")

        # Integration complexity
        if len(context.integration_needs) > 3:
            complexity_factors.append("Multiple integrations required")

        # Multiple patterns detected
        if len(context.patterns_detected) > 2:
            complexity_factors.append("Hybrid pattern implementation needed")

        context.complexity_indicators.extend(complexity_factors)

    def create_workflow_specification(
        self, context: ProjectContext, workflow_name: str
    ) -> Dict[str, Any]:
        """Create a workflow specification from project context."""
        # Determine primary pattern
        primary_pattern = "WORKFLOW"  # Default
        if context.patterns_detected:
            primary_pattern = context.patterns_detected[0]

        # Create specification
        spec = {
            "name": workflow_name,
            "pattern": primary_pattern,
            "description": self._create_description(context),
            "requirements": [
                {
                    "text": req.text,
                    "type": req.type,
                    "priority": req.priority,
                    "source": req.source_file,
                }
                for req in context.requirements[:10]  # Limit for spec size
            ],
            "technical_stack": context.technical_stack,
            "complexity_level": self._assess_complexity_level(context),
            "patterns_detected": context.patterns_detected,
            "integration_needs": context.integration_needs,
            "constraints": context.constraints,
            "context_metadata": {
                "source_documents": context.source_documents,
                "extraction_timestamp": self._get_timestamp(),
                "total_requirements": len(context.requirements),
            },
        }

        return spec

    def _create_description(self, context: ProjectContext) -> str:
        """Create a comprehensive description from context."""
        if context.description:
            return context.description

        # Generate description from requirements
        functional_reqs = [
            req for req in context.requirements if req.type == "functional"
        ]
        if functional_reqs:
            return f"System that {functional_reqs[0].text.lower()}"

        return f"Implementation for {context.project_name}"

    def _assess_complexity_level(self, context: ProjectContext) -> str:
        """Assess overall complexity level."""
        complexity_score = 0

        complexity_score += len(context.requirements) * 0.1
        complexity_score += len(context.technical_stack) * 0.3
        complexity_score += len(context.integration_needs) * 0.5
        complexity_score += len(context.patterns_detected) * 0.4

        if complexity_score > 10:
            return "high"
        elif complexity_score > 5:
            return "medium"
        else:
            return "low"

    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        return datetime.now().isoformat()

    def save_context_analysis(
        self, context: ProjectContext, output_file: str = "context_analysis.json"
    ):
        """Save context analysis to file for debugging and reuse."""
        output_path = self.project_root / output_file

        # Convert to serializable format
        context_dict = {
            "project_name": context.project_name,
            "description": context.description,
            "requirements": [
                {
                    "text": req.text,
                    "type": req.type,
                    "priority": req.priority,
                    "source_file": req.source_file,
                    "confidence": req.confidence,
                    "patterns": req.patterns,
                }
                for req in context.requirements
            ],
            "technical_stack": context.technical_stack,
            "patterns_detected": context.patterns_detected,
            "complexity_indicators": context.complexity_indicators,
            "integration_needs": context.integration_needs,
            "constraints": context.constraints,
            "success_criteria": context.success_criteria,
            "source_documents": context.source_documents,
        }

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(context_dict, f, indent=2, ensure_ascii=False)
            logger.info(f"Context analysis saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save context analysis: {e}")


def main():
    """CLI interface for context manager."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract project context from design documents"
    )
    parser.add_argument(
        "--project-root", "-p", default=".", help="Project root directory"
    )
    parser.add_argument(
        "--workflow-name", "-w", help="Name of the workflow to generate"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="context_analysis.json",
        help="Output file for context analysis",
    )
    parser.add_argument("--spec", "-s", help="Output file for workflow specification")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Extract context
    manager = ContextManager(args.project_root)
    context = manager.extract_project_context(args.workflow_name)

    # Save analysis
    manager.save_context_analysis(context, args.output)

    # Create workflow specification if requested
    if args.spec and args.workflow_name:
        spec = manager.create_workflow_specification(context, args.workflow_name)
        with open(args.spec, "w", encoding="utf-8") as f:
            yaml.dump(spec, f, default_flow_style=False)
        print(f"Workflow specification saved to {args.spec}")

    # Print summary
    print("\n=== Context Analysis Summary ===")
    print(f"Project: {context.project_name}")
    print(f"Requirements found: {len(context.requirements)}")
    print(f"Technical stack: {', '.join(context.technical_stack[:5])}")
    print(f"Patterns detected: {', '.join(context.patterns_detected)}")
    print(f"Source documents: {len(context.source_documents)}")
    print(f"Complexity indicators: {len(context.complexity_indicators)}")


if __name__ == "__main__":
    main()
