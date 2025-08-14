#!/usr/bin/env python3
"""
Code Generation Validation Script

Validates that generated PocketFlow workflows follow Agent OS standards
and PocketFlow best practices.
"""

import ast
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class WorkflowValidator:
    """Validates generated PocketFlow workflows."""
    
    def __init__(self, workflow_path: Path):
        self.workflow_path = Path(workflow_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validation checks."""
        try:
            # Structure validation
            self._validate_structure()
            
            # Code quality validation
            self._validate_code_quality()
            
            # PocketFlow pattern validation
            self._validate_pocketflow_patterns()
            
            # Type safety validation
            self._validate_type_safety()
            
            # Test coverage validation
            self._validate_test_coverage()
            
            return len(self.errors) == 0, self.errors, self.warnings
            
        except Exception as e:
            self.errors.append(f"Validation failed with exception: {e}")
            return False, self.errors, self.warnings
    
    def _validate_structure(self):
        """Validate directory and file structure."""
        required_files = [
            "docs/design.md",
            "schemas/models.py",
            "nodes.py",
            "flow.py",
            "tasks.md"
        ]
        
        for file_path in required_files:
            full_path = self.workflow_path / file_path
            if not full_path.exists():
                self.errors.append(f"Missing required file: {file_path}")
        
        # Check for utils directory if utilities are defined
        utils_dir = self.workflow_path / "utils"
        if utils_dir.exists():
            if not any(utils_dir.glob("*.py")):
                self.warnings.append("Utils directory exists but contains no Python files")
        
        # Check for tests directory
        tests_dir = self.workflow_path / "tests"
        if not tests_dir.exists():
            self.errors.append("Missing tests directory")
        else:
            test_files = ["test_nodes.py", "test_flow.py"]
            for test_file in test_files:
                if not (tests_dir / test_file).exists():
                    self.errors.append(f"Missing test file: tests/{test_file}")
    
    def _validate_code_quality(self):
        """Validate code quality using ruff and other tools."""
        python_files = list(self.workflow_path.glob("**/*.py"))
        
        for py_file in python_files:
            # Check if file is valid Python
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError as e:
                self.errors.append(f"Syntax error in {py_file}: {e}")
            except Exception as e:
                self.errors.append(f"Error parsing {py_file}: {e}")
        
        # Run ruff check if available
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", str(self.workflow_path)],
                capture_output=True,
                text=True,
                cwd=self.workflow_path.parent.parent.parent  # Go to project root
            )
            if result.returncode != 0:
                self.warnings.append(f"Ruff linting issues: {result.stdout}")
        except FileNotFoundError:
            self.warnings.append("Ruff not available for linting check")
    
    def _validate_pocketflow_patterns(self):
        """Validate PocketFlow-specific patterns."""
        # Check nodes.py
        nodes_file = self.workflow_path / "nodes.py"
        if nodes_file.exists():
            self._validate_nodes_file(nodes_file)
        
        # Check flow.py
        flow_file = self.workflow_path / "flow.py"
        if flow_file.exists():
            self._validate_flow_file(flow_file)
        
        # Check design.md
        design_file = self.workflow_path / "docs" / "design.md"
        if design_file.exists():
            self._validate_design_file(design_file)
    
    def _validate_nodes_file(self, nodes_file: Path):
        """Validate nodes.py follows PocketFlow patterns."""
        with open(nodes_file, 'r') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return  # Already caught in code quality check
        
        # Check for proper imports
        has_pocketflow_import = "from pocketflow import" in content
        if not has_pocketflow_import:
            self.errors.append("nodes.py missing PocketFlow imports")
        
        # Check node classes
        node_classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                node_classes.append(node.name)
                
                # Check if class extends a PocketFlow node type
                base_names = [base.id for base in node.bases if hasattr(base, 'id')]
                valid_bases = ['Node', 'AsyncNode', 'BatchNode']
                if not any(base in valid_bases for base in base_names):
                    self.warnings.append(f"Node class {node.name} may not extend a valid PocketFlow node type")
                
                # Check for required methods (including async methods)
                sync_methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                async_methods = [n.name for n in node.body if isinstance(n, ast.AsyncFunctionDef)]
                all_methods = sync_methods + async_methods
                
                required_methods = ['prep', 'post']
                for method in required_methods:
                    if method not in all_methods:
                        self.errors.append(f"Node {node.name} missing required method: {method}")
                
                # Check for exec method (either exec or exec_async)
                exec_methods = [m for m in all_methods if m.startswith('exec')]
                if not exec_methods:
                    self.errors.append(f"Node {node.name} missing exec or exec_async method (found methods: {all_methods})")
                
                # Check for try/except in exec methods (PocketFlow anti-pattern)
                self._check_try_except_in_node_methods(node)
        
        if not node_classes:
            self.errors.append("nodes.py contains no node class definitions")
    
    def _check_try_except_in_node_methods(self, class_node):
        """Check for try/except blocks in node methods."""
        for method in class_node.body:
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Check exec methods specifically
                if method.name in ['exec', 'exec_async']:
                    for node in ast.walk(method):
                        if isinstance(node, ast.Try):
                            self.errors.append(
                                f"Found try/except in {class_node.name}.{method.name}(). "
                                "Use PocketFlow's max_retries and exec_fallback instead."
                            )
                
                # Check utility-style methods that shouldn't have broad try/catch
                elif method.name not in ['prep', 'post', '__init__']:
                    for node in ast.walk(method):
                        if isinstance(node, ast.Try):
                            if not self._is_legitimate_try_except(node):
                                self.warnings.append(
                                    f"Found try/except in {class_node.name}.{method.name}(). "
                                    "Consider if this should use PocketFlow error handling."
                                )
    
    def _is_legitimate_try_except(self, try_node):
        """Check if try/except is for legitimate parsing/validation."""
        # Allow for JSON parsing, file operations, etc.
        legitimate_exceptions = ['JSONDecodeError', 'FileNotFoundError', 'ValueError', 'KeyError']
        
        for handler in try_node.handlers:
            if handler.type and hasattr(handler.type, 'id'):
                if handler.type.id in legitimate_exceptions:
                    return True
            elif handler.type and hasattr(handler.type, 'attr'):
                if handler.type.attr in legitimate_exceptions:
                    return True
        
        return False
    
    def _validate_flow_file(self, flow_file: Path):
        """Validate flow.py follows PocketFlow patterns."""
        with open(flow_file, 'r') as f:
            content = f.read()
        
        # Check for Flow import
        if "from pocketflow import Flow" not in content:
            self.errors.append("flow.py missing Flow import")
        
        # Check for flow class definition
        if "class" not in content or "Flow)" not in content:
            self.errors.append("flow.py missing Flow class definition")
        
        # Check for nodes and edges definition
        if "nodes = {" not in content:
            self.warnings.append("flow.py may be missing nodes dictionary")
        
        if "edges = {" not in content:
            self.warnings.append("flow.py may be missing edges dictionary")
    
    def _validate_design_file(self, design_file: Path):
        """Validate design.md follows template structure."""
        with open(design_file, 'r') as f:
            content = f.read()
        
        required_sections = [
            "# Design Document",
            "## Requirements",
            "## Flow Design",
            "## Utilities",
            "## Data Design",
            "## Node Design"
        ]
        
        for section in required_sections:
            if section not in content:
                self.errors.append(f"design.md missing required section: {section}")
        
        # Check for Mermaid diagram
        if "```mermaid" not in content:
            self.warnings.append("design.md missing Mermaid diagram")
    
    def _validate_type_safety(self):
        """Validate type safety using type checker."""
        # Check for type hints in Python files
        python_files = list(self.workflow_path.glob("**/*.py"))
        
        for py_file in python_files:
            if py_file.name == "__init__.py":
                continue
                
            with open(py_file, 'r') as f:
                content = f.read()
            
            # Basic check for type hints
            if "from typing import" not in content and ":" not in content:
                self.warnings.append(f"{py_file.name} may be missing type hints")
        
        # Run type checker if available
        try:
            result = subprocess.run(
                ["uv", "run", "ty", "check", str(self.workflow_path)],
                capture_output=True,
                text=True,
                cwd=self.workflow_path.parent.parent.parent
            )
            if result.returncode != 0:
                self.warnings.append(f"Type checking issues: {result.stdout}")
        except FileNotFoundError:
            self.warnings.append("Type checker not available")
    
    def _validate_test_coverage(self):
        """Validate test coverage and structure."""
        tests_dir = self.workflow_path / "tests"
        if not tests_dir.exists():
            return  # Already caught in structure validation
        
        test_files = list(tests_dir.glob("test_*.py"))
        
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
            
            # Check for pytest import
            if "import pytest" not in content:
                self.warnings.append(f"{test_file.name} missing pytest import")
            
            # Check for test class structure
            if "class Test" not in content:
                self.warnings.append(f"{test_file.name} may be missing test class structure")
            
            # Check for async test methods if needed
            if "async def test_" not in content and "AsyncNode" in str(self.workflow_path):
                self.warnings.append(f"{test_file.name} may need async test methods for AsyncNode")


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
    
    parser = argparse.ArgumentParser(description="Validate generated PocketFlow workflows")
    parser.add_argument("--workflow", help="Specific workflow directory to validate")
    parser.add_argument("--all", action="store_true", help="Validate all workflows in .agent-os/workflows/")
    
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
        workflow_dirs = [d for d in workflows_dir.iterdir() if d.is_dir() and d.name != "__pycache__"]
        
        if not workflow_dirs:
            print("No workflow directories found")
            return 0
        
        for workflow_dir in workflow_dirs:
            if workflow_dir.name.startswith('.'):
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