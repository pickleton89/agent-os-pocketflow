#!/usr/bin/env python3
"""
Code Generation Validation Script (Wrapper)

Delegates core design/nodes/flow checks to the canonical validator at
`framework-tools/template_validator.py` to ensure a single source of truth.
Retains lightweight quality checks (ruff/type) as advisories.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple
import importlib.util


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class WorkflowValidator:
    """Validates generated PocketFlow workflows (delegates to canonical validator)."""

    def __init__(self, workflow_path: Path):
        self.workflow_path = Path(workflow_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validation checks."""
        try:
            # 1) Delegate to canonical Python validator (single source of truth)
            self._delegate_to_canonical_validator()

            # 2) Code quality validation (advisory)
            self._validate_code_quality()

            # 3) Type safety validation (advisory)
            self._validate_type_safety()

            return len(self.errors) == 0, self.errors, self.warnings

        except Exception as e:
            self.errors.append(f"Validation failed with exception: {e}")
            return False, self.errors, self.warnings

    def _delegate_to_canonical_validator(self) -> None:
        """Call framework-tools/template_validator.py for core validation."""
        project_root = Path(__file__).resolve().parents[2]
        validator_path = project_root / "framework-tools" / "template_validator.py"

        if not validator_path.exists():
            # Hard fail: canonical module not found
            self.errors.append(
                f"Canonical validator not found at {validator_path}. "
                "Ensure framework repo layout is intact."
            )
            return

        # Dynamically import the validator module from file path
        spec = importlib.util.spec_from_file_location(
            "pf_template_validator", str(validator_path)
        )
        if spec is None or spec.loader is None:
            self.errors.append("Failed to load canonical validator module spec")
            return

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[arg-type]

        # Instantiate and run validation on the workflow directory
        validator = module.PocketFlowValidator()
        result = validator.validate_directory(self.workflow_path)

        # Map issues into this wrapper's error/warning lists
        for issue in result.issues:
            if issue.level.value == "error":
                self.errors.append(
                    f"{issue.category}: {Path(issue.file_path).name}"
                    + (f":{issue.line_number}" if issue.line_number else "")
                    + f" - {issue.message}"
                )
            elif issue.level.value == "warning":
                self.warnings.append(
                    f"{issue.category}: {Path(issue.file_path).name}"
                    + (f":{issue.line_number}" if issue.line_number else "")
                    + f" - {issue.message}"
                )

    def _validate_code_quality(self):
        """Validate code quality using ruff and other tools."""
        # Run ruff check if available
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", str(self.workflow_path)],
                capture_output=True,
                text=True,
                cwd=self.workflow_path.parent.parent.parent,  # Go to project root
            )
            if result.returncode != 0:
                self.warnings.append(f"Ruff linting issues: {result.stdout}")
        except FileNotFoundError:
            self.warnings.append("Ruff not available for linting check")

    def _validate_type_safety(self):
        """Validate type safety using type checker."""
        # Run type checker if available
        try:
            result = subprocess.run(
                ["uv", "run", "ty", "check", str(self.workflow_path)],
                capture_output=True,
                text=True,
                cwd=self.workflow_path.parent.parent.parent,
            )
            if result.returncode != 0:
                self.warnings.append(f"Type checking issues: {result.stdout}")
        except FileNotFoundError:
            self.warnings.append("Type checker not available")


def validate_workflow_directory(workflow_dir: Path) -> bool:
    """Validate a single workflow directory."""
    print(f"Validating workflow: {workflow_dir.name}")

    validator = WorkflowValidator(workflow_dir)
    success, errors, warnings = validator.validate_all()

    if warnings:
        print("  Warnings:")
        for warning in warnings:
            print(f"    - {warning}")

    if errors:
        print("  Errors:")
        for error in errors:
            print(f"    ✗ {error}")

    if success:
        print("  ✓ Validation passed")
    else:
        print("  ✗ Validation failed")

    return success


def main():
    """Main validation script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate generated PocketFlow workflows"
    )
    parser.add_argument("--workflow", help="Specific workflow directory to validate")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all workflows in .agent-os/workflows/",
    )

    args = parser.parse_args()

    workflows_dir = Path(".agent-os/workflows")

    if not workflows_dir.exists():
        print("Error: .agent-os/workflows directory not found")
        return 1

    success_count = 0
    total_count = 0

    if args.workflow:
        # Validate specific workflow
        workflow_path = workflows_dir / args.workflow
        if not workflow_path.exists():
            print(f"Error: Workflow directory {args.workflow} not found")
            return 1

        success = validate_workflow_directory(workflow_path)
        return 0 if success else 1

    elif args.all:
        # Validate all workflows
        workflow_dirs = [
            d for d in workflows_dir.iterdir() if d.is_dir() and d.name != "__pycache__"
        ]

        if not workflow_dirs:
            print("No workflow directories found")
            return 0

        for workflow_dir in workflow_dirs:
            if workflow_dir.name.startswith("."):
                continue

            success = validate_workflow_directory(workflow_dir)
            total_count += 1
            if success:
                success_count += 1
            print()

        print(f"Validation Summary: {success_count}/{total_count} workflows passed")
        return 0 if success_count == total_count else 1

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
