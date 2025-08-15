#!/usr/bin/env python3
"""
Orchestration Integration Validation Script

This script validates that the PocketFlow orchestrator integration is working
correctly with the Agent OS instruction files and coordination system.
"""

import sys
import yaml
from pathlib import Path
from typing import List, Optional, Tuple


class OrchestrationValidator:
    """Validates orchestration integration components."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.agent_os_path = self.project_root / ".agent-os"
        self.claude_path = self.project_root / ".claude"
        self.templates_path = self.project_root / "templates"
        self.validation_results: List[Tuple[str, bool, Optional[str]]] = []

    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("🔍 Validating PocketFlow Orchestrator Integration...")
        print("=" * 60)

        # Core component validations
        self.validate_orchestrator_agent()
        self.validate_orchestration_hooks()
        self.validate_coordination_config()
        self.validate_dependency_validation()
        self.validate_instruction_file_integration()
        self.validate_template_files()

        # Report results
        return self.report_results()

    def validate_orchestrator_agent(self):
        """Validate the PocketFlow orchestrator agent exists and is properly configured."""
        agent_path = self.claude_path / "agents" / "pocketflow-orchestrator.md"

        if not agent_path.exists():
            self.add_result(
                "Orchestrator Agent", False, f"Agent file not found: {agent_path}"
            )
            return

        # Check agent content
        content = agent_path.read_text()
        required_sections = [
            "name: pocketflow-orchestrator",
            "MUST BE USED PROACTIVELY",
            "tools:",
            "Core Mission",
            "Strategic Planning & Pattern Analysis",
            "Workflow Design & Visualization",
            "Code Generation & Implementation",
            "Coordination Protocol",
        ]

        missing_sections = [
            section for section in required_sections if section not in content
        ]

        if missing_sections:
            self.add_result(
                "Orchestrator Agent", False, f"Missing sections: {missing_sections}"
            )
        else:
            self.add_result("Orchestrator Agent", True)

    def validate_orchestration_hooks(self):
        """Validate orchestration hooks system."""
        hooks_path = (
            self.agent_os_path
            / "instructions"
            / "orchestration"
            / "orchestrator-hooks.md"
        )

        if not hooks_path.exists():
            self.add_result(
                "Orchestration Hooks", False, f"Hooks file not found: {hooks_path}"
            )
            return

        content = hooks_path.read_text()
        required_hooks = [
            "validate_design_document",
            "validate_workflow_implementation",
            "orchestrator_fallback",
        ]

        missing_hooks = [hook for hook in required_hooks if hook not in content]

        if missing_hooks:
            self.add_result(
                "Orchestration Hooks", False, f"Missing hooks: {missing_hooks}"
            )
        else:
            self.add_result("Orchestration Hooks", True)

    def validate_coordination_config(self):
        """Validate coordination configuration."""
        coord_path = (
            self.agent_os_path / "instructions" / "orchestration" / "coordination.yaml"
        )

        if not coord_path.exists():
            self.add_result(
                "Coordination Config",
                False,
                f"Coordination file not found: {coord_path}",
            )
            return

        try:
            with open(coord_path) as f:
                config = yaml.safe_load(f)

            required_keys = ["coordination_map", "hooks", "error_handling"]
            missing_keys = [key for key in required_keys if key not in config]

            if missing_keys:
                self.add_result(
                    "Coordination Config", False, f"Missing keys: {missing_keys}"
                )
                return

            # Check coordination map
            coord_map = config["coordination_map"]
            required_instructions = ["plan-product", "create-spec", "execute-tasks"]
            missing_instructions = [
                instr for instr in required_instructions if instr not in coord_map
            ]

            if missing_instructions:
                self.add_result(
                    "Coordination Config",
                    False,
                    f"Missing instruction mappings: {missing_instructions}",
                )
            else:
                self.add_result("Coordination Config", True)

        except Exception as e:
            self.add_result("Coordination Config", False, f"YAML parsing error: {e}")

    def validate_dependency_validation(self):
        """Validate dependency validation system."""
        dep_path = (
            self.agent_os_path
            / "instructions"
            / "orchestration"
            / "dependency-validation.md"
        )

        if not dep_path.exists():
            self.add_result(
                "Dependency Validation",
                False,
                f"Dependency validation file not found: {dep_path}",
            )
            return

        content = dep_path.read_text()
        required_elements = [
            "Dependency Chain",
            "execute-tasks.md Dependencies",
            "create-spec.md Dependencies",
            "Dependency Resolution Protocol",
            "validate_execute_tasks_dependencies",
            "Auto-Resolution",
        ]

        missing_elements = [elem for elem in required_elements if elem not in content]

        if missing_elements:
            self.add_result(
                "Dependency Validation", False, f"Missing elements: {missing_elements}"
            )
        else:
            self.add_result("Dependency Validation", True)

    def validate_instruction_file_integration(self):
        """Validate that core instruction files have orchestration integration."""
        instruction_files = [
            ("plan-product.md", ["@include orchestration/orchestrator-hooks.md"]),
            ("create-spec.md", ["@include orchestration/orchestrator-hooks.md"]),
            ("execute-tasks.md", ["@include orchestration/orchestrator-hooks.md"]),
        ]

        all_integrated = True
        missing_integrations = []

        for filename, required_includes in instruction_files:
            file_path = self.agent_os_path / "instructions" / "core" / filename

            if not file_path.exists():
                missing_integrations.append(f"{filename} (file not found)")
                all_integrated = False
                continue

            content = file_path.read_text()
            missing_includes = [inc for inc in required_includes if inc not in content]

            if missing_includes:
                missing_integrations.append(f"{filename} (missing: {missing_includes})")
                all_integrated = False

        if all_integrated:
            self.add_result("Instruction File Integration", True)
        else:
            self.add_result(
                "Instruction File Integration", False, f"Issues: {missing_integrations}"
            )

    def validate_template_files(self):
        """Validate that required template files exist."""
        template_files = [
            "pocketflow-templates.md",
            "fastapi-templates.md",
            "task-templates.md",
        ]

        templates_path = self.templates_path
        missing_templates = []

        for template in template_files:
            template_path = templates_path / template
            if not template_path.exists():
                missing_templates.append(template)

        if missing_templates:
            self.add_result(
                "Template Files", False, f"Missing templates: {missing_templates}"
            )
        else:
            self.add_result("Template Files", True)

    def add_result(self, component: str, success: bool, error: Optional[str] = None):
        """Add a validation result."""
        self.validation_results.append((component, success, error))

    def report_results(self) -> bool:
        """Report validation results and return overall success."""
        print("\n📊 Validation Results:")
        print("=" * 60)

        all_passed = True

        for component, success, error in self.validation_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {component}")

            if error:
                print(f"      {error}")

            if not success:
                all_passed = False

        print("\n" + "=" * 60)

        if all_passed:
            print("🎉 All orchestration integration validations PASSED!")
            print("✨ Phase 2: Orchestration system is fully implemented.")
        else:
            print("⚠️  Some validations FAILED. Please review and fix issues above.")

        return all_passed


def main():
    """Main validation entry point."""
    validator = OrchestrationValidator()
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
