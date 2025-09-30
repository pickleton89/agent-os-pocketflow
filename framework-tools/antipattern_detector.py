#!/usr/bin/env python3
"""
PocketFlow Antipattern Detector

A tool to identify common mistakes and antipatterns in PocketFlow implementations.
This detector helps maintain code quality by catching problematic patterns early
in the development process.

Architecture:
    - Models: Severity enum and AntipatternViolation dataclass
    - PocketFlowASTVisitor: AST-based pattern analysis
    - AntipatternDetector: Detection engine with regex patterns
    - AntipatternReporter: Report generation (console, JSON, markdown)
    - CLI: Command-line interface

Usage:
    python antipattern_detector.py [path] [options]
    python antipattern_detector.py --help

Author: Agent OS + PocketFlow Framework
Version: 1.0.0
"""

import ast
import os
import re
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# MODELS: Data structures for antipattern detection
# ============================================================================

class Severity(Enum):
    """Severity levels for antipattern violations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AntipatternViolation:
    """Represents a detected antipattern violation"""
    antipattern_id: str
    name: str
    severity: Severity
    file_path: str
    line_number: int
    message: str
    suggestion: str
    code_snippet: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


# ============================================================================
# AST VISITOR: Abstract Syntax Tree analysis for pattern detection
# ============================================================================

class PocketFlowASTVisitor(ast.NodeVisitor):
    """AST visitor to analyze PocketFlow code patterns"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: List[AntipatternViolation] = []
        self.current_class: Optional[str] = None
        self.current_method: Optional[str] = None
        self.node_classes: List[Dict[str, Any]] = []
        self.utility_functions: List[Dict[str, Any]] = []
        self.is_test_file = self._is_test_or_demo_file(file_path)

    # ------------------------------------------------------------------------
    # AST Visitor Methods
    # ------------------------------------------------------------------------

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definitions to analyze node patterns"""
        old_class = self.current_class
        self.current_class = node.name
        
        # Check if this is a PocketFlow node (framework-aware)
        base_names = [self._get_base_class_name(base) for base in node.bases]
        is_node_class = self._is_pocketflow_node_class(base_names)
        
        if is_node_class:
            methods = self._extract_methods(node)
            self.node_classes.append({
                'name': node.name,
                'lineno': node.lineno,
                'bases': base_names,
                'methods': methods
            })
            
            # Check for antipatterns in node design
            self._check_monolithic_node(node, methods)
            self._check_node_lifecycle_violations(node, methods)
        
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions to analyze method patterns"""
        old_method = self.current_method
        self.current_method = node.name
        
        # Analyze utility functions (functions outside classes)
        if self.current_class is None:
            self.utility_functions.append({
                'name': node.name,
                'lineno': node.lineno,
                'args': [arg.arg for arg in node.args.args],
                'ast_node': node
            })
            self._check_business_logic_in_utility(node)
        
        # Analyze node methods
        elif self.current_class and node.name in ['prep', 'exec', 'exec_async', 'post', 'post_async']:
            self._check_method_patterns(node)
        
        self.generic_visit(node)
        self.current_method = old_method

    # ------------------------------------------------------------------------
    # Antipattern Check Methods
    # ------------------------------------------------------------------------

    def _extract_methods(self, class_node: ast.ClassDef) -> Dict[str, Dict[str, Any]]:
        """Extract method information from a class"""
        methods = {}
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                methods[node.name] = {
                    'lineno': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'ast_node': node
                }
        return methods
    
    def _check_monolithic_node(self, class_node: ast.ClassDef, methods: Dict[str, Any]) -> None:
        """Check for monolithic node antipattern"""
        if 'exec' in methods or 'exec_async' in methods:
            exec_method = methods.get('exec') or methods.get('exec_async')
            exec_node = exec_method['ast_node']
            
            # Count lines in exec method
            method_lines = self._count_method_lines(exec_node)
            
            # Check for multiple responsibilities
            llm_calls = self._count_llm_calls(exec_node)
            
            if method_lines > 20:
                self.violations.append(AntipatternViolation(
                    antipattern_id="monolithic_node",
                    name="Monolithic Node Syndrome",
                    severity=self._adjust_severity_for_context(Severity.CRITICAL),
                    file_path=self.file_path,
                    line_number=exec_node.lineno,
                    message=f"{class_node.name}.{exec_node.name}(): Method too long ({method_lines} lines)",
                    suggestion="Split into focused nodes with single responsibilities",
                    context={"method_lines": method_lines, "class_name": class_node.name}
                ))
            
            if llm_calls > 2:
                self.violations.append(AntipatternViolation(
                    antipattern_id="monolithic_node",
                    name="Monolithic Node Syndrome",
                    severity=self._adjust_severity_for_context(Severity.HIGH),
                    file_path=self.file_path,
                    line_number=exec_node.lineno,
                    message=f"{class_node.name}.{exec_node.name}(): Multiple LLM calls ({llm_calls}) suggest multiple responsibilities",
                    suggestion="Split each LLM call into separate nodes",
                    context={"llm_calls": llm_calls, "class_name": class_node.name}
                ))
            
            # Check for multiple verb class names (ProcessAndValidate, etc.)
            if self._has_multiple_verbs(class_node.name):
                self.violations.append(AntipatternViolation(
                    antipattern_id="monolithic_node",
                    name="Monolithic Node Syndrome",
                    severity=self._adjust_severity_for_context(Severity.MEDIUM),
                    file_path=self.file_path,
                    line_number=class_node.lineno,
                    message=f"{class_node.name}: Class name suggests multiple responsibilities",
                    suggestion="Use single-responsibility class names (e.g., ProcessDocuments → ValidateDocuments, ExtractText)",
                    context={"class_name": class_node.name}
                ))
    
    def _check_node_lifecycle_violations(self, class_node: ast.ClassDef, methods: Dict[str, Any]) -> None:
        """Check for node lifecycle violations"""
        # Check for shared store access in exec
        if 'exec' in methods or 'exec_async' in methods:
            exec_method = methods.get('exec') or methods.get('exec_async')
            exec_node = exec_method['ast_node']
            
            shared_access = self._find_shared_store_access(exec_node)
            if shared_access:
                for lineno, access_pattern in shared_access:
                    self.violations.append(AntipatternViolation(
                        antipattern_id="shared_store_in_exec",
                        name="Shared Store Access in exec()",
                        severity=self._adjust_severity_for_context(Severity.CRITICAL),
                        file_path=self.file_path,
                        line_number=lineno,
                        message=f"{class_node.name}.{exec_node.name}(): Direct SharedStore access detected: {access_pattern}",
                        suggestion="Access data through prep_result parameter instead of self.shared",
                        context={"access_pattern": access_pattern, "class_name": class_node.name}
                    ))
        
        # Check for lifecycle method confusion
        self._check_lifecycle_confusion(class_node, methods)
    
    def _check_method_patterns(self, method_node: ast.FunctionDef) -> None:
        """Check for method-specific antipatterns"""
        method_name = method_node.name
        
        if method_name in ['prep', 'prep_async']:
            # Check for computation in prep
            if self._has_complex_computation(method_node):
                self.violations.append(AntipatternViolation(
                    antipattern_id="lifecycle_confusion",
                    name="Lifecycle Method Confusion",
                    severity=self._adjust_severity_for_context(Severity.MEDIUM),
                    file_path=self.file_path,
                    line_number=method_node.lineno,
                    message=f"{self.current_class}.{method_name}(): Complex computation detected",
                    suggestion="Move computation to exec() method, keep prep() for data access only",
                    context={"method": method_name, "class_name": self.current_class}
                ))
            
            # Check for LLM calls in prep
            if self._count_llm_calls(method_node) > 0:
                self.violations.append(AntipatternViolation(
                    antipattern_id="lifecycle_confusion",
                    name="Lifecycle Method Confusion",
                    severity=self._adjust_severity_for_context(Severity.HIGH),
                    file_path=self.file_path,
                    line_number=method_node.lineno,
                    message=f"{self.current_class}.{method_name}(): LLM calls should be in exec() for proper retry handling",
                    suggestion="Move LLM calls to exec() method",
                    context={"method": method_name, "class_name": self.current_class}
                ))
        
        elif method_name in ['post', 'post_async']:
            # Check for complex computation in post
            if self._has_complex_computation(method_node):
                self.violations.append(AntipatternViolation(
                    antipattern_id="lifecycle_confusion",
                    name="Lifecycle Method Confusion",
                    severity=self._adjust_severity_for_context(Severity.MEDIUM),
                    file_path=self.file_path,
                    line_number=method_node.lineno,
                    message=f"{self.current_class}.{method_name}(): Complex computation detected",
                    suggestion="Move computation to exec() method, keep post() for state updates only",
                    context={"method": method_name, "class_name": self.current_class}
                ))
    
    def _check_business_logic_in_utility(self, func_node: ast.FunctionDef) -> None:
        """Check for business logic in utility functions"""
        # Check for LLM calls in utilities
        llm_calls = self._count_llm_calls(func_node)
        if llm_calls > 0:
            self.violations.append(AntipatternViolation(
                antipattern_id="business_logic_in_utils",
                name="Business Logic in Utilities",
                severity=self._adjust_severity_for_context(Severity.HIGH),
                file_path=self.file_path,
                line_number=func_node.lineno,
                message=f"Utility function '{func_node.name}' contains LLM calls",
                suggestion="Move LLM calls to node exec() methods",
                context={"function_name": func_node.name, "llm_calls": llm_calls}
            ))
        
        # Check for complex branching logic
        if_else_count = self._count_if_else_branches(func_node)
        if if_else_count > 2:
            self.violations.append(AntipatternViolation(
                antipattern_id="business_logic_in_utils",
                name="Business Logic in Utilities",
                severity=self._adjust_severity_for_context(Severity.MEDIUM),
                file_path=self.file_path,
                line_number=func_node.lineno,
                message=f"Utility function '{func_node.name}' has complex branching logic ({if_else_count} branches)",
                suggestion="Move decision logic to nodes and flow branching",
                context={"function_name": func_node.name, "branches": if_else_count}
            ))
    
    def _check_lifecycle_confusion(self, class_node: ast.ClassDef, methods: Dict[str, Any]) -> None:
        """Check for lifecycle method confusion patterns"""
        # Additional checks for method role confusion
        pass

    # ------------------------------------------------------------------------
    # Helper Methods: Pattern detection utilities
    # ------------------------------------------------------------------------

    def _count_method_lines(self, method_node: ast.FunctionDef) -> int:
        """Count actual lines of code in a method (not AST nodes) - cross-version compatible"""
        # Get the line range of the method
        start_line = method_node.lineno
        
        # Find the end line by looking at all child nodes
        end_line = start_line
        for child in ast.walk(method_node):
            if hasattr(child, 'lineno') and child.lineno:
                end_line = max(end_line, child.lineno)
            
            # Only use end_lineno if available (Python 3.8+)
            if hasattr(child, 'end_lineno') and child.end_lineno:
                end_line = max(end_line, child.end_lineno)
        
        # If we couldn't find any child nodes with line numbers, 
        # fall back to a more conservative estimate
        if end_line == start_line:
            # Count non-empty statements in the method body as a fallback
            statement_count = len([stmt for stmt in method_node.body if stmt])
            # Estimate: method definition + statements + potential whitespace
            estimated_lines = 1 + statement_count + max(0, statement_count // 3)  # Add ~33% for whitespace
            return max(1, estimated_lines)
        
        # Calculate total line span (including definition line)
        total_lines = end_line - start_line + 1
        
        # Return the line count, minimum of 1
        return max(1, total_lines)
    
    def _count_llm_calls(self, node: ast.AST) -> int:
        """Count LLM-related function calls"""
        llm_patterns = ['call_llm', 'llm_call', 'openai', 'anthropic', 'gpt', 'claude']
        count = 0
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                func_name = self._get_function_name(child)
                if any(pattern in func_name.lower() for pattern in llm_patterns):
                    count += 1
        
        return count
    
    def _count_loops(self, node: ast.AST) -> int:
        """Count loops in a node"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                count += 1
        return count
    
    def _count_if_else_branches(self, node: ast.AST) -> int:
        """Count if/else decision points in a node (each if/elif/else chain counts as 1)"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                count += 1
                # Note: child.orelse contains else/elif but shouldn't be double-counted
                # Each if/elif/else chain is ONE decision point
        return count
    
    def _has_multiple_verbs(self, class_name: str) -> bool:
        """Check if class name suggests multiple responsibilities"""
        # Common patterns: ProcessAndValidate, CreateAndSend, FetchParseStore
        verb_patterns = [
            r'.*And.*',  # ProcessAndValidate
            r'.*Then.*',  # FetchThenProcess
            r'.*Parse.*Store.*',  # ParseAndStore
            r'.*Create.*Send.*',  # CreateAndSend
        ]
        
        return any(re.search(pattern, class_name) for pattern in verb_patterns)
    
    def _find_shared_store_access(self, node: ast.AST) -> List[Tuple[int, str]]:
        """Find shared store access patterns in exec methods"""
        access_patterns = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Subscript):
                if isinstance(child.value, ast.Attribute):
                    if isinstance(child.value.value, ast.Name) and child.value.value.id == 'self':
                        if child.value.attr == 'shared':
                            line_no = getattr(child, 'lineno', 0)
                            pattern = f"self.shared[{self._ast_to_string(child.slice)}]"
                            access_patterns.append((line_no, pattern))
            
            elif isinstance(child, ast.Attribute):
                if isinstance(child.value, ast.Attribute):
                    if isinstance(child.value.value, ast.Name) and child.value.value.id == 'self':
                        if child.value.attr == 'shared':
                            line_no = getattr(child, 'lineno', 0)
                            pattern = f"self.shared.{child.attr}"
                            access_patterns.append((line_no, pattern))
        
        return access_patterns
    
    def _has_complex_computation(self, node: ast.AST) -> bool:
        """Check if node has complex computation patterns"""
        # Look for indicators of complex computation
        loop_count = self._count_loops(node)
        call_count = 0
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                call_count += 1
        
        # Heuristic: more than 3 function calls or any loops indicate computation
        return loop_count > 0 or call_count > 3
    
    def _get_base_class_name(self, base_node: ast.AST) -> str:
        """Safely extract base class name from AST node"""
        if isinstance(base_node, ast.Name):
            return base_node.id
        elif isinstance(base_node, ast.Attribute):
            # Handle cases like pocketflow.Node or module.submodule.Node
            parts = []
            current = base_node
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return ".".join(reversed(parts))
        elif isinstance(base_node, ast.Subscript):
            # Handle generic types like Generic[T] - extract the base name
            return self._get_base_class_name(base_node.value)
        else:
            # Fallback for other complex expressions
            return "unknown_base"
    
    def _ast_to_string(self, node: ast.AST, _depth: int = 0) -> str:
        """Convert AST node to string with cross-version compatibility and recursion protection"""
        # Prevent infinite recursion by limiting depth
        if _depth > 10:
            return "<deeply_nested>"
        
        if hasattr(ast, 'unparse'):  # Python 3.9+
            try:
                return ast.unparse(node)
            except Exception:
                pass
        
        # Fallback for older Python versions or when unparse fails
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Str):  # Python < 3.8
            return repr(node.s)
        elif isinstance(node, ast.Num):  # Python < 3.8
            return str(node.n)
        elif isinstance(node, ast.Subscript):
            try:
                value_str = self._ast_to_string(node.value, _depth + 1)
                slice_str = self._ast_to_string(node.slice, _depth + 1)
                return f"{value_str}[{slice_str}]"
            except (AttributeError, RecursionError):
                return "<subscript>"
        elif isinstance(node, ast.Attribute):
            try:
                value_str = self._ast_to_string(node.value, _depth + 1)
                return f"{value_str}.{node.attr}"
            except (AttributeError, RecursionError):
                return f"<object>.{node.attr}"
        elif isinstance(node, ast.Index):  # Python < 3.9
            try:
                return self._ast_to_string(node.value, _depth + 1)
            except (AttributeError, RecursionError):
                return "<index>"
        else:
            return "<expression>"
    
    def _is_pocketflow_node_class(self, base_names: List[str]) -> bool:
        """Check if base classes indicate this is a PocketFlow node (framework-aware)"""
        # Direct PocketFlow node types
        pocketflow_nodes = ['Node', 'AsyncNode', 'BatchNode', 'AsyncBatchNode', 'AsyncParallelBatchNode']
        
        # Check for direct matches
        if any(base in pocketflow_nodes for base in base_names):
            return True
        
        # Framework context: also check for qualified imports
        # (e.g., pocketflow.Node, framework.Node)
        for base in base_names:
            if '.' in base:
                class_name = base.split('.')[-1]  # Get the last part
                if class_name in pocketflow_nodes:
                    return True
        
        # Check for common patterns in mock/framework context
        framework_patterns = [
            'MockNode', 'TestNode', 'BaseNode', 'FrameworkNode'
        ]
        if any(base in framework_patterns for base in base_names):
            return True
        
        return False
    
    def _is_test_or_demo_file(self, file_path: str) -> bool:
        """Check if this is a test file or demo file with intentional antipatterns"""
        file_name = os.path.basename(file_path).lower()
        
        # Common test file patterns
        test_patterns = [
            'test_', '_test.', 'tests.', 'test.', 
            'demo', 'example', 'sample',
            'antipattern_demo', 'fixture'
        ]
        
        return any(pattern in file_name for pattern in test_patterns)
    
    def _adjust_severity_for_context(self, severity: Severity) -> Severity:
        """Adjust severity based on file context (e.g., more lenient for test files)"""
        if self.is_test_file:
            # Reduce severity for test/demo files with intentional antipatterns
            if severity == Severity.CRITICAL:
                return Severity.HIGH
            elif severity == Severity.HIGH:
                return Severity.MEDIUM
            elif severity == Severity.MEDIUM:
                return Severity.LOW
        
        return severity
    
    def _get_function_name(self, call_node: ast.Call) -> str:
        """Extract function name from a Call node"""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        else:
            return "unknown"


# ============================================================================
# DETECTOR: Main antipattern detection engine
# ============================================================================

class AntipatternDetector:
    """Main antipattern detection engine"""
    
    def __init__(self):
        self.antipatterns = self._load_antipattern_definitions()
    
    def _normalize_file_path(self, file_path: str) -> str:
        """Normalize file path for consistent reporting with robust error handling"""
        try:
            # Convert to Path for better handling
            path = Path(file_path)
            
            # Try to make relative to current working directory for cleaner output
            try:
                cwd = Path.cwd()
                relative_path = path.relative_to(cwd)
                return str(relative_path)
            except (ValueError, OSError):
                # If can't make relative, try to use absolute path
                try:
                    return str(path.resolve())
                except (OSError, RuntimeError):
                    # If resolve fails, fall back to the original path
                    return str(path)
        except Exception:
            # If all else fails, return the original string
            # This handles cases with very unusual path formats
            return file_path
    
    def _load_antipattern_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Load antipattern definitions"""
        return {
            "monolithic_node": {
                "name": "Monolithic Node Syndrome",
                "description": "Single nodes that handle multiple distinct responsibilities",
                "severity": "critical",
                "indicators": ["multiple responsibilities", "large exec method", "multiple LLM calls"],
                "fix": "Split into focused nodes with single responsibilities"
            },
            "shared_store_in_exec": {
                "name": "Shared Store Access in exec()",
                "description": "Accessing shared store directly from exec() methods",
                "severity": "critical", 
                "indicators": ["shared[", "self.shared"],
                "fix": "Use prep_result parameter only in exec() methods"
            },
            "lifecycle_confusion": {
                "name": "Lifecycle Method Confusion",
                "description": "Misplacing logic in wrong lifecycle methods",
                "severity": "medium",
                "indicators": ["computation in prep", "LLM calls in prep", "complex logic in post"],
                "fix": "Follow prep (data) → exec (compute) → post (effects) pattern"
            },
            "business_logic_in_utils": {
                "name": "Business Logic in Utilities",
                "description": "Complex business logic in utility functions instead of nodes",
                "severity": "high",
                "indicators": ["LLM calls in utils", "complex branching in utils"],
                "fix": "Move business logic to nodes, keep utilities simple"
            }
        }
    
    def detect_file(self, file_path: str) -> List[AntipatternViolation]:
        """Detect antipatterns in a single file"""
        try:
            # Normalize file path for consistent reporting
            normalized_path = self._normalize_file_path(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse AST
            tree = ast.parse(source_code, filename=file_path)
            
            # Visit AST and collect violations (use normalized path for reporting)
            visitor = PocketFlowASTVisitor(normalized_path)
            visitor.visit(tree)
            
            # Add regex-based detections
            regex_violations = self._detect_regex_patterns(normalized_path, source_code, visitor.is_test_file)
            visitor.violations.extend(regex_violations)
            
            return visitor.violations
            
        except SyntaxError as e:
            return [AntipatternViolation(
                antipattern_id="syntax_error",
                name="Syntax Error",
                severity=Severity.CRITICAL,
                file_path=file_path,
                line_number=e.lineno or 0,
                message=f"Syntax error: {e.msg}",
                suggestion="Fix syntax errors before running antipattern detection"
            )]
        except Exception as e:
            return [AntipatternViolation(
                antipattern_id="analysis_error", 
                name="Analysis Error",
                severity=Severity.LOW,
                file_path=file_path,
                line_number=0,
                message=f"Could not analyze file: {e}",
                suggestion="Check file encoding and permissions"
            )]
    
    def _adjust_severity_for_test_context(self, severity: Severity, is_test_file: bool) -> Severity:
        """Adjust severity for test file context"""
        if is_test_file:
            # Reduce severity for test/demo files with intentional antipatterns
            if severity == Severity.CRITICAL:
                return Severity.HIGH
            elif severity == Severity.HIGH:
                return Severity.MEDIUM
            elif severity == Severity.MEDIUM:
                return Severity.LOW
        return severity
    
    def _detect_regex_patterns(self, file_path: str, source_code: str, is_test_file: bool = False) -> List[AntipatternViolation]:
        """Detect antipatterns using regex patterns"""
        violations = []
        lines = source_code.split('\n')
        
        # Pattern for synchronous collection processing
        for i, line in enumerate(lines, 1):
            if re.search(r'for\s+\w+\s+in\s+.*:', line):
                # Check if this is inside an exec method of a regular Node
                if self._is_in_exec_method(lines, i-1) and 'BatchNode' not in ''.join(lines[max(0, i-10):i+10]):
                    violations.append(AntipatternViolation(
                        antipattern_id="sync_collection_processing",
                        name="Synchronous Collection Processing",
                        severity=self._adjust_severity_for_test_context(Severity.MEDIUM, is_test_file),
                        file_path=file_path,
                        line_number=i,
                        message="Loop in exec() method suggests collection processing in regular Node",
                        suggestion="Use BatchNode or AsyncParallelBatchNode for collection processing",
                        code_snippet=line.strip()
                    ))
        
        # Pattern for blocking I/O in regular nodes
        blocking_io_patterns = [
            r'requests\.get\(',
            r'requests\.post\(',
            r'urllib\.',
            r'open\(',
            r'with\s+open\('
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in blocking_io_patterns:
                if re.search(pattern, line):
                    if self._is_in_exec_method(lines, i-1) and 'AsyncNode' not in ''.join(lines[max(0, i-10):i+10]):
                        violations.append(AntipatternViolation(
                            antipattern_id="blocking_io_in_node",
                            name="Blocking I/O in Regular Node",
                            severity=self._adjust_severity_for_test_context(Severity.MEDIUM, is_test_file),
                            file_path=file_path,
                            line_number=i,
                            message="Blocking I/O operation in regular Node",
                            suggestion="Use AsyncNode for I/O operations",
                            code_snippet=line.strip()
                        ))
        
        return violations
    
    def _is_in_exec_method(self, lines: List[str], line_idx: int) -> bool:
        """Check if a line is inside an exec() method"""
        # Simple heuristic: look backwards for method definition
        for i in range(line_idx, max(0, line_idx - 20), -1):
            if re.search(r'def\s+(exec|exec_async)\s*\(', lines[i]):
                return True
        return False
    
    def detect_directory(self, directory_path: str, extensions: List[str] = None) -> List[AntipatternViolation]:
        """Detect antipatterns in all files in a directory"""
        if extensions is None:
            extensions = ['.py']
        
        all_violations = []
        directory = Path(directory_path)
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                violations = self.detect_file(str(file_path))
                all_violations.extend(violations)
        
        return all_violations


# ============================================================================
# REPORTER: Report generation for detected antipatterns
# ============================================================================

class AntipatternReporter:
    """Generate reports for detected antipatterns"""
    
    def __init__(self, violations: List[AntipatternViolation]):
        self.violations = violations
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of detected violations"""
        summary = {
            "total_violations": len(self.violations),
            "by_severity": {},
            "by_antipattern": {},
            "by_file": {},
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0
        }
        
        for violation in self.violations:
            # By severity
            severity = violation.severity.value
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            
            # Count by severity for quick access
            if violation.severity == Severity.CRITICAL:
                summary["critical_count"] += 1
            elif violation.severity == Severity.HIGH:
                summary["high_count"] += 1
            elif violation.severity == Severity.MEDIUM:
                summary["medium_count"] += 1
            elif violation.severity == Severity.LOW:
                summary["low_count"] += 1
            
            # By antipattern
            antipattern_id = violation.antipattern_id
            summary["by_antipattern"][antipattern_id] = summary["by_antipattern"].get(antipattern_id, 0) + 1
            
            # By file
            file_path = violation.file_path
            summary["by_file"][file_path] = summary["by_file"].get(file_path, 0) + 1
        
        return summary
    
    def generate_console_report(self) -> str:
        """Generate a console-friendly report"""
        if not self.violations:
            return "✅ No antipatterns detected!"
        
        summary = self.generate_summary()
        report_lines = []
        
        # Header
        report_lines.append("🔍 PocketFlow Antipattern Detection Report")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Summary
        report_lines.append(f"Total violations found: {summary['total_violations']}")
        report_lines.append(f"🔴 Critical: {summary['critical_count']}")
        report_lines.append(f"🟡 High: {summary['high_count']}")
        report_lines.append(f"🟠 Medium: {summary['medium_count']}")
        report_lines.append(f"🟢 Low: {summary['low_count']}")
        report_lines.append("")
        
        # Group by file
        violations_by_file = {}
        for violation in self.violations:
            file_path = violation.file_path
            if file_path not in violations_by_file:
                violations_by_file[file_path] = []
            violations_by_file[file_path].append(violation)
        
        # Report violations by file
        for file_path, file_violations in sorted(violations_by_file.items()):
            report_lines.append(f"📁 {file_path}")
            report_lines.append("-" * len(file_path))
            
            for violation in sorted(file_violations, key=lambda v: v.line_number):
                severity_icon = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟡",
                    Severity.MEDIUM: "🟠", 
                    Severity.LOW: "🟢"
                }[violation.severity]
                
                report_lines.append(f"  {severity_icon} Line {violation.line_number}: {violation.name}")
                report_lines.append(f"     Message: {violation.message}")
                report_lines.append(f"     Fix: {violation.suggestion}")
                if violation.code_snippet:
                    report_lines.append(f"     Code: {violation.code_snippet}")
                report_lines.append("")
            
            report_lines.append("")
        
        # Most common antipatterns
        report_lines.append("📊 Most Common Antipatterns:")
        sorted_antipatterns = sorted(summary["by_antipattern"].items(), key=lambda x: x[1], reverse=True)
        for antipattern_id, count in sorted_antipatterns[:5]:
            report_lines.append(f"  {antipattern_id}: {count} violations")
        
        return "\n".join(report_lines)
    
    def generate_json_report(self) -> str:
        """Generate a JSON report"""
        report_data = {
            "summary": self.generate_summary(),
            "violations": [asdict(violation) for violation in self.violations]
        }
        
        # Convert Enum values to strings for JSON serialization
        for violation in report_data["violations"]:
            if isinstance(violation["severity"], Severity):
                violation["severity"] = violation["severity"].value
        
        return json.dumps(report_data, indent=2, default=str)
    
    def generate_markdown_report(self) -> str:
        """Generate a Markdown report"""
        if not self.violations:
            return "# ✅ No Antipatterns Detected\n\nAll PocketFlow code follows best practices!"
        
        summary = self.generate_summary()
        report_lines = []
        
        # Header
        report_lines.append("# 🔍 PocketFlow Antipattern Detection Report")
        report_lines.append("")
        
        # Summary table
        report_lines.append("## Summary")
        report_lines.append("")
        report_lines.append("| Severity | Count |")
        report_lines.append("|----------|-------|")
        report_lines.append(f"| 🔴 Critical | {summary['critical_count']} |")
        report_lines.append(f"| 🟡 High | {summary['high_count']} |")
        report_lines.append(f"| 🟠 Medium | {summary['medium_count']} |")
        report_lines.append(f"| 🟢 Low | {summary['low_count']} |")
        report_lines.append(f"| **Total** | **{summary['total_violations']}** |")
        report_lines.append("")
        
        # Violations by file
        report_lines.append("## Violations by File")
        report_lines.append("")
        
        violations_by_file = {}
        for violation in self.violations:
            file_path = violation.file_path
            if file_path not in violations_by_file:
                violations_by_file[file_path] = []
            violations_by_file[file_path].append(violation)
        
        for file_path, file_violations in sorted(violations_by_file.items()):
            report_lines.append(f"### `{file_path}`")
            report_lines.append("")
            
            for violation in sorted(file_violations, key=lambda v: v.line_number):
                severity_icon = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟡", 
                    Severity.MEDIUM: "🟠",
                    Severity.LOW: "🟢"
                }[violation.severity]
                
                report_lines.append(f"#### {severity_icon} {violation.name} (Line {violation.line_number})")
                report_lines.append("")
                report_lines.append(f"**Message:** {violation.message}")
                report_lines.append("")
                report_lines.append(f"**Suggestion:** {violation.suggestion}")
                report_lines.append("")
                
                if violation.code_snippet:
                    report_lines.append("**Code:**")
                    report_lines.append("```python")
                    report_lines.append(violation.code_snippet)
                    report_lines.append("```")
                    report_lines.append("")
        
        return "\n".join(report_lines)


# ============================================================================
# CLI: Command-line interface
# ============================================================================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="PocketFlow Antipattern Detector - Identify common mistakes in PocketFlow implementations"
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to file or directory to analyze (default: current directory)'
    )
    
    parser.add_argument(
        '--format',
        choices=['console', 'json', 'markdown'],
        default='console',
        help='Output format (default: console)'
    )
    
    parser.add_argument(
        '--severity',
        choices=['critical', 'high', 'medium', 'low'],
        help='Only show violations of this severity level or higher'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--include-patterns',
        nargs='+',
        default=['*.py'],
        help='File patterns to include (default: *.py)'
    )
    
    parser.add_argument(
        '--exclude-patterns',
        nargs='+',
        default=[],
        help='File patterns to exclude'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--fail-on-violations',
        action='store_true',
        help='Exit with non-zero code if violations found'
    )
    
    args = parser.parse_args()
    
    # Create detector
    detector = AntipatternDetector()
    
    # Detect violations
    if os.path.isfile(args.path):
        violations = detector.detect_file(args.path)
    else:
        extensions = [f".{pattern.replace('*.', '')}" for pattern in args.include_patterns]
        violations = detector.detect_directory(args.path, extensions)
    
    # Filter by severity if specified
    if args.severity:
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        min_severity = severity_order[args.severity]
        violations = [
            v for v in violations 
            if severity_order[v.severity.value] <= min_severity
        ]
    
    # Generate report
    reporter = AntipatternReporter(violations)
    
    if args.format == 'console':
        report = reporter.generate_console_report()
    elif args.format == 'json':
        report = reporter.generate_json_report()
    elif args.format == 'markdown':
        report = reporter.generate_markdown_report()
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        if args.verbose:
            print(f"Report saved to {args.output}")
    else:
        print(report)
    
    # Exit with appropriate code
    if args.fail_on_violations and violations:
        critical_count = sum(1 for v in violations if v.severity == Severity.CRITICAL)
        high_count = sum(1 for v in violations if v.severity == Severity.HIGH)
        if critical_count > 0:
            sys.exit(2)  # Critical violations
        elif high_count > 0:
            sys.exit(1)  # High severity violations
        else:
            sys.exit(0)  # Only medium/low violations
    
    sys.exit(0)


if __name__ == '__main__':
    main()