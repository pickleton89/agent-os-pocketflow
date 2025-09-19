#!/usr/bin/env python3
"""
Document Consistency Validator for Agent OS + PocketFlow Framework

Validates consistency across generated documents from document creation agents.
Part of Phase 4 optimization for the document creation subagent refactoring.

Usage:
    python3 document-consistency-validator.py [project_root] [--fix-issues]
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "ERROR"      # Must be fixed
    WARNING = "WARNING"  # Should be fixed
    INFO = "INFO"       # Nice to fix


@dataclass
class ValidationIssue:
    """Represents a validation issue found in documents"""
    level: ValidationLevel
    category: str
    file_path: str
    issue: str
    suggestion: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class DocumentContent:
    """Container for document content and metadata"""
    file_path: Path
    content: str
    yaml_frontmatter: Optional[Dict[str, Any]] = None
    markdown_sections: Dict[str, str] = None


class DocumentConsistencyValidator:
    """Validates consistency across Agent OS + PocketFlow generated documents"""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.issues: List[ValidationIssue] = []
        self.documents: Dict[str, DocumentContent] = {}

        # Define expected document locations
        self.document_paths = {
            'mission': self.project_root / '.agent-os' / 'product' / 'mission.md',
            'tech_stack': self.project_root / '.agent-os' / 'product' / 'tech-stack.md',
            'roadmap': self.project_root / '.agent-os' / 'product' / 'roadmap.md',
            'pre_flight': self.project_root / '.agent-os' / 'checklists' / 'pre-flight.md',
            'design': self.project_root / 'docs' / 'design.md',
            'claude_md': self.project_root / 'CLAUDE.md'
        }

    def load_documents(self) -> None:
        """Load all available documents for validation"""
        for doc_type, doc_path in self.document_paths.items():
            if doc_path.exists():
                try:
                    content = doc_path.read_text(encoding='utf-8')
                    doc_content = DocumentContent(
                        file_path=doc_path,
                        content=content
                    )

                    # Parse YAML frontmatter if present
                    if content.startswith('---\n'):
                        try:
                            end_idx = content.find('\n---\n', 4)
                            if end_idx != -1:
                                yaml_content = content[4:end_idx]
                                doc_content.yaml_frontmatter = yaml.safe_load(yaml_content)
                        except yaml.YAMLError as e:
                            self.add_issue(ValidationLevel.ERROR, "YAML", str(doc_path),
                                         f"Invalid YAML frontmatter: {e}")

                    # Parse markdown sections
                    doc_content.markdown_sections = self._parse_markdown_sections(content)
                    self.documents[doc_type] = doc_content

                except Exception as e:
                    self.add_issue(ValidationLevel.ERROR, "FILE_READ", str(doc_path),
                                 f"Failed to read document: {e}")

    def _parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections based on headers"""
        sections = {}
        current_section = ""
        current_content = []

        for line in content.split('\n'):
            if line.startswith('#'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.strip('#').strip().lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def add_issue(self, level: ValidationLevel, category: str, file_path: str,
                  issue: str, suggestion: Optional[str] = None,
                  line_number: Optional[int] = None) -> None:
        """Add a validation issue to the results"""
        self.issues.append(ValidationIssue(
            level=level,
            category=category,
            file_path=file_path,
            issue=issue,
            suggestion=suggestion,
            line_number=line_number
        ))

    def validate_feature_consistency(self) -> None:
        """Validate that features are consistent across mission and roadmap documents"""
        if 'mission' not in self.documents or 'roadmap' not in self.documents:
            return

        mission_doc = self.documents['mission']
        roadmap_doc = self.documents['roadmap']

        # Extract features from mission document
        mission_features = self._extract_features_from_mission(mission_doc.content)

        # Extract features from roadmap document
        roadmap_features = self._extract_features_from_roadmap(roadmap_doc.content)

        # Check for missing features
        mission_set = set(mission_features)
        roadmap_set = set(roadmap_features)

        missing_in_roadmap = mission_set - roadmap_set
        missing_in_mission = roadmap_set - mission_set

        for feature in missing_in_roadmap:
            self.add_issue(
                ValidationLevel.WARNING,
                "FEATURE_CONSISTENCY",
                str(roadmap_doc.file_path),
                f"Feature '{feature}' present in mission but missing from roadmap",
                "Add feature to appropriate roadmap phase"
            )

        for feature in missing_in_mission:
            self.add_issue(
                ValidationLevel.WARNING,
                "FEATURE_CONSISTENCY",
                str(mission_doc.file_path),
                f"Feature '{feature}' present in roadmap but missing from mission",
                "Add feature to mission document or remove from roadmap"
            )

    def _extract_features_from_mission(self, content: str) -> List[str]:
        """Extract feature names from mission document"""
        features = []
        in_features_section = False

        for line in content.split('\n'):
            if line.strip().lower().startswith('## key features') or \
               line.strip().lower().startswith('## features'):
                in_features_section = True
                continue
            elif line.startswith('##') and in_features_section:
                break
            elif in_features_section and line.strip().startswith('-'):
                feature_match = re.match(r'-\s*\*\*([^*]+)\*\*', line.strip())
                if feature_match:
                    features.append(feature_match.group(1).strip())

        return features

    def _extract_features_from_roadmap(self, content: str) -> List[str]:
        """Extract feature names from roadmap document"""
        features = []

        # Look for features in phase sections
        phase_pattern = r'###\s*Phase\s*\d+[^#]*?\n(.*?)(?=###|\Z)'
        matches = re.findall(phase_pattern, content, re.DOTALL | re.IGNORECASE)

        for phase_content in matches:
            feature_matches = re.findall(r'-\s*\*\*([^*]+)\*\*', phase_content)
            features.extend(match.strip() for match in feature_matches)

        return features

    def validate_tech_stack_alignment(self) -> None:
        """Validate tech stack choices are consistent across documents"""
        if 'tech_stack' not in self.documents or 'design' not in self.documents:
            return

        tech_doc = self.documents['tech_stack']
        design_doc = self.documents['design']

        # Extract tech choices from tech-stack document
        tech_choices = self._extract_tech_choices(tech_doc.content)

        # Check if design document mentions different technologies
        design_content = design_doc.content.lower()

        for tech_type, chosen_tech in tech_choices.items():
            if chosen_tech and chosen_tech.lower() not in design_content:
                self.add_issue(
                    ValidationLevel.INFO,
                    "TECH_ALIGNMENT",
                    str(design_doc.file_path),
                    f"Tech stack choice '{chosen_tech}' for {tech_type} not mentioned in design document",
                    f"Consider adding {chosen_tech} to technical architecture section"
                )

    def _extract_tech_choices(self, content: str) -> Dict[str, Optional[str]]:
        """Extract technology choices from tech-stack document"""
        choices = {
            'database': None,
            'frontend': None,
            'backend': None,
            'deployment': None
        }

        # Look for technology choice patterns
        patterns = {
            'database': r'database[^:]*:\s*([^\n]+)',
            'frontend': r'frontend[^:]*:\s*([^\n]+)',
            'backend': r'backend[^:]*:\s*([^\n]+)',
            'deployment': r'deployment[^:]*:\s*([^\n]+)'
        }

        content_lower = content.lower()
        for tech_type, pattern in patterns.items():
            match = re.search(pattern, content_lower)
            if match:
                choices[tech_type] = match.group(1).strip()

        return choices

    def validate_pocketflow_patterns(self) -> None:
        """Validate PocketFlow pattern consistency across documents"""
        pattern_mentions = {}

        # Look for PocketFlow patterns mentioned in each document
        pocketflow_patterns = ['WORKFLOW', 'TOOL', 'AGENT', 'RAG', 'MAPREDUCE']

        for doc_type, doc_content in self.documents.items():
            patterns_found = []
            for pattern in pocketflow_patterns:
                if pattern in doc_content.content:
                    patterns_found.append(pattern)
            pattern_mentions[doc_type] = patterns_found

        # Check for consistency between mission and design documents
        if 'mission' in pattern_mentions and 'design' in pattern_mentions:
            mission_patterns = set(pattern_mentions['mission'])
            design_patterns = set(pattern_mentions['design'])

            if mission_patterns != design_patterns:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "POCKETFLOW_CONSISTENCY",
                    str(self.documents['design'].file_path),
                    f"PocketFlow patterns mismatch: mission has {mission_patterns}, design has {design_patterns}",
                    "Ensure consistent pattern selection across documents"
                )

    def validate_claude_md_references(self) -> None:
        """Validate CLAUDE.md contains references to all generated documents"""
        if 'claude_md' not in self.documents:
            return

        claude_content = self.documents['claude_md'].content

        # Check for references to key documents
        expected_references = [
            ('.agent-os/product/mission.md', 'mission'),
            ('.agent-os/product/tech-stack.md', 'tech_stack'),
            ('.agent-os/product/roadmap.md', 'roadmap'),
            ('docs/design.md', 'design')
        ]

        for file_path, doc_type in expected_references:
            if doc_type in self.documents and file_path not in claude_content:
                self.add_issue(
                    ValidationLevel.INFO,
                    "CLAUDE_MD_REFERENCES",
                    str(self.documents['claude_md'].file_path),
                    f"Missing reference to {file_path}",
                    f"Add reference to {file_path} in relevant workflow section"
                )

    def validate_template_compliance(self) -> None:
        """Validate documents follow expected template structures"""
        template_requirements = {
            'mission': [
                'pitch',
                'users',
                'problems',
                'differentiators',
                'key_features',
                'architecture_strategy'
            ],
            'tech_stack': [
                'programming_language',
                'framework',
                'database',
                'deployment'
            ],
            'roadmap': [
                'phase_1',
                'phase_2',
                'phase_3'
            ]
        }

        for doc_type, required_sections in template_requirements.items():
            if doc_type not in self.documents:
                continue

            doc_content = self.documents[doc_type]
            content_lower = doc_content.content.lower()

            for section in required_sections:
                if section.replace('_', ' ') not in content_lower and \
                   section.replace('_', '') not in content_lower:
                    self.add_issue(
                        ValidationLevel.WARNING,
                        "TEMPLATE_COMPLIANCE",
                        str(doc_content.file_path),
                        f"Missing required section: {section}",
                        f"Add {section} section to match expected template structure"
                    )

    def run_all_validations(self) -> None:
        """Run all validation checks"""
        print("🔍 Loading documents...")
        self.load_documents()

        print("✅ Validating feature consistency...")
        self.validate_feature_consistency()

        print("🔧 Validating tech stack alignment...")
        self.validate_tech_stack_alignment()

        print("🌊 Validating PocketFlow patterns...")
        self.validate_pocketflow_patterns()

        print("📝 Validating CLAUDE.md references...")
        self.validate_claude_md_references()

        print("📋 Validating template compliance...")
        self.validate_template_compliance()

    def generate_report(self) -> str:
        """Generate a formatted validation report"""
        if not self.issues:
            return "✅ All document consistency validations passed!\n"

        # Group issues by level and category
        errors = [i for i in self.issues if i.level == ValidationLevel.ERROR]
        warnings = [i for i in self.issues if i.level == ValidationLevel.WARNING]
        infos = [i for i in self.issues if i.level == ValidationLevel.INFO]

        report = []
        report.append("# Document Consistency Validation Report\n")

        # Summary
        report.append("## Summary")
        report.append(f"- 🔴 Errors: {len(errors)}")
        report.append(f"- 🟡 Warnings: {len(warnings)}")
        report.append(f"- 🔵 Info: {len(infos)}")
        report.append("")

        # Detailed issues
        for level_name, issues in [("Errors", errors), ("Warnings", warnings), ("Info", infos)]:
            if not issues:
                continue

            report.append(f"## {level_name}\n")

            for issue in issues:
                report.append(f"### {issue.category}: {Path(issue.file_path).name}")
                report.append(f"**Issue**: {issue.issue}")
                if issue.suggestion:
                    report.append(f"**Suggestion**: {issue.suggestion}")
                if issue.line_number:
                    report.append(f"**Line**: {issue.line_number}")
                report.append("")

        return "\n".join(report)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate document consistency for Agent OS + PocketFlow projects")
    parser.add_argument("project_root", nargs="?", default=".",
                       help="Project root directory (default: current directory)")
    parser.add_argument("--output", "-o", help="Output report to file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        print(f"❌ Project root does not exist: {project_root}")
        return 1

    validator = DocumentConsistencyValidator(project_root)
    validator.run_all_validations()

    if args.json:
        # JSON output for programmatic consumption
        issues_dict = {
            "summary": {
                "errors": len([i for i in validator.issues if i.level == ValidationLevel.ERROR]),
                "warnings": len([i for i in validator.issues if i.level == ValidationLevel.WARNING]),
                "info": len([i for i in validator.issues if i.level == ValidationLevel.INFO])
            },
            "issues": [
                {
                    "level": issue.level.value,
                    "category": issue.category,
                    "file": issue.file_path,
                    "issue": issue.issue,
                    "suggestion": issue.suggestion,
                    "line": issue.line_number
                }
                for issue in validator.issues
            ]
        }
        output = json.dumps(issues_dict, indent=2)
    else:
        output = validator.generate_report()

    if args.output:
        Path(args.output).write_text(output)
        print(f"📄 Report written to: {args.output}")
    else:
        print(output)

    # Return non-zero exit code if there are errors
    error_count = len([i for i in validator.issues if i.level == ValidationLevel.ERROR])
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    exit(main())