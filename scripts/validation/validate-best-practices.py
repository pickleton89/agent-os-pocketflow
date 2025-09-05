#!/usr/bin/env python3
"""
PocketFlow Best Practices Validator

Validates PocketFlow implementations against established best practices including:
- Node lifecycle compliance (prep/exec/post patterns)
- Batch node usage patterns
- Utility function philosophy
- Context management guidelines
- Error handling patterns

Version: 1.0.0
Part of Agent OS Framework Task 3.1
"""

import ast
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re


class ViolationLevel(Enum):
    """Severity levels for best practice violations."""
    ERROR = "error"
    WARNING = "warning" 
    INFO = "info"


@dataclass
class BestPracticeViolation:
    """Represents a best practice violation."""
    level: ViolationLevel
    category: str
    file_path: str
    line_number: Optional[int]
    message: str
    suggestion: str
    rule_id: str


class NodeLifecycleAnalyzer(ast.NodeVisitor):
    """AST analyzer for PocketFlow node lifecycle patterns."""
    
    def __init__(self):
        self.violations: List[BestPracticeViolation] = []
        self.current_file = ""
        self.current_class = None
        self.node_classes: List[Dict[str, Any]] = []
        
    def analyze_file(self, file_path: Path) -> List[BestPracticeViolation]:
        """Analyze a single Python file for node lifecycle violations."""
        self.violations = []
        self.node_classes = []  # Reset node classes for each file
        self.current_file = str(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            self.visit(tree)
            
            # Analyze collected node classes
            for node_class in self.node_classes:
                self._validate_node_lifecycle(node_class)
                
        except SyntaxError as e:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="parsing",
                file_path=self.current_file,
                line_number=getattr(e, 'lineno', None),
                message=f"Syntax error: {e}",
                suggestion="Fix Python syntax errors in the file",
                rule_id="SYNTAX_ERROR"
            ))
        except UnicodeDecodeError as e:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="parsing",
                file_path=self.current_file,
                line_number=None,
                message=f"Encoding error: {e}",
                suggestion="Fix file encoding - ensure UTF-8",
                rule_id="ENCODING_ERROR"
            ))
        except (OSError, IOError) as e:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="parsing",
                file_path=self.current_file,
                line_number=None,
                message=f"File access error: {e}",
                suggestion="Check file permissions and existence",
                rule_id="FILE_ACCESS_ERROR"
            ))
        except Exception as e:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="parsing",
                file_path=self.current_file,
                line_number=None,
                message=f"Unexpected error: {e}",
                suggestion="Report this issue - unexpected validation error",
                rule_id="UNEXPECTED_ERROR"
            ))
            
        return self.violations
    
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions to identify PocketFlow nodes."""
        # Check if this is a PocketFlow node class
        base_names = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_names.append(f"{base.value.id}.{base.attr}" if hasattr(base.value, 'id') else base.attr)
        
        # Look for PocketFlow node base classes
        pocketflow_bases = ['Node', 'AsyncNode', 'BatchNode', 'AsyncBatchNode', 'AsyncParallelBatchNode']
        if any(base in pocketflow_bases for base in base_names):
            # Collect methods (both sync and async functions)
            methods = {}
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods[item.name] = {
                        'lineno': item.lineno,
                        'args': [arg.arg for arg in item.args.args],
                        'body': item.body,
                        'node': item,
                        'is_async': isinstance(item, ast.AsyncFunctionDef)
                    }
            
            self.node_classes.append({
                'name': node.name,
                'lineno': node.lineno,
                'bases': base_names,
                'methods': methods,
                'node': node
            })
        
        self.generic_visit(node)
    
    def _validate_node_lifecycle(self, node_class: Dict[str, Any]):
        """Validate lifecycle methods for a PocketFlow node."""
        name = node_class['name']
        methods = node_class['methods']
        bases = node_class['bases']
        lineno = node_class['lineno']
        
        
        # Check for required methods
        if 'prep' not in methods:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="lifecycle",
                file_path=self.current_file,
                line_number=lineno,
                message=f"{name}: Missing required prep() method",
                suggestion="Add prep(self, shared: Dict[str, Any]) -> Any method",
                rule_id="MISSING_PREP"
            ))
        
        if 'post' not in methods:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="lifecycle",
                file_path=self.current_file,
                line_number=lineno,
                message=f"{name}: Missing required post() method",
                suggestion="Add post(self, shared, prep_result, exec_result) -> str method",
                rule_id="MISSING_POST"
            ))
        
        # Check exec/exec_async based on node type
        is_async = any(base in ['AsyncNode', 'BatchNode', 'AsyncBatchNode', 'AsyncParallelBatchNode'] for base in bases)
        
        if is_async and 'exec_async' not in methods and 'exec' not in methods:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="lifecycle",
                file_path=self.current_file,
                line_number=lineno,
                message=f"{name}: Missing required exec() or exec_async() method",
                suggestion="Add exec() or exec_async() method depending on node type",
                rule_id="MISSING_EXEC"
            ))
        elif not is_async and 'exec' not in methods:
            self.violations.append(BestPracticeViolation(
                level=ViolationLevel.ERROR,
                category="lifecycle",
                file_path=self.current_file,
                line_number=lineno,
                message=f"{name}: Missing required exec() method",
                suggestion="Add exec(self, prep_result) -> Any method",
                rule_id="MISSING_EXEC"
            ))
        
        # Validate method implementations
        if 'prep' in methods:
            self._validate_prep_method(name, methods['prep'])
        
        if 'exec' in methods:
            self._validate_exec_method(name, methods['exec'])
        
        if 'exec_async' in methods:
            self._validate_exec_method(name, methods['exec_async'])
        
        if 'post' in methods:
            self._validate_post_method(name, methods['post'])
    
    def _validate_prep_method(self, class_name: str, method_info: Dict[str, Any]):
        """Validate prep() method implementation."""
        method = method_info['node']
        
        # Check for violations in prep method
        for node in ast.walk(method):
            # Check for external API calls in prep (should be in exec)
            if isinstance(node, ast.Call):
                if self._is_external_call(node):
                    self.violations.append(BestPracticeViolation(
                        level=ViolationLevel.ERROR,
                        category="lifecycle",
                        file_path=self.current_file,
                        line_number=getattr(node, 'lineno', method_info['lineno']),
                        message=f"{class_name}.prep(): External API call detected - should be in exec()",
                        suggestion="Move external API calls to exec() method",
                        rule_id="PREP_EXTERNAL_CALL"
                    ))
            
            # Check for complex computation in prep
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                self.violations.append(BestPracticeViolation(
                    level=ViolationLevel.WARNING,
                    category="lifecycle", 
                    file_path=self.current_file,
                    line_number=getattr(node, 'lineno', method_info['lineno']),
                    message=f"{class_name}.prep(): Complex computation (loops) detected - should be in exec()",
                    suggestion="Move complex computation to exec() method",
                    rule_id="PREP_COMPLEX_COMPUTATION"
                ))
    
    def _validate_exec_method(self, class_name: str, method_info: Dict[str, Any]):
        """Validate exec() method implementation."""
        method = method_info['node']
        
        # Check for SharedStore access in exec (should use prep_result only)
        for node in ast.walk(method):
            if isinstance(node, ast.Subscript):
                if (isinstance(node.value, ast.Attribute) and 
                    hasattr(node.value, 'attr') and node.value.attr == 'shared'):
                    self.violations.append(BestPracticeViolation(
                        level=ViolationLevel.ERROR,
                        category="lifecycle",
                        file_path=self.current_file,
                        line_number=getattr(node, 'lineno', method_info['lineno']),
                        message=f"{class_name}.exec(): Direct SharedStore access - use prep_result only",
                        suggestion="Access data through prep_result parameter instead of self.shared",
                        rule_id="EXEC_SHARED_ACCESS"
                    ))
            
            # Check for side effects in exec
            if isinstance(node, ast.Call):
                if self._is_side_effect_call(node):
                    self.violations.append(BestPracticeViolation(
                        level=ViolationLevel.ERROR,
                        category="lifecycle",
                        file_path=self.current_file,
                        line_number=getattr(node, 'lineno', method_info['lineno']),
                        message=f"{class_name}.exec(): Side effect detected - should be in post()",
                        suggestion="Move side effects to post() method",
                        rule_id="EXEC_SIDE_EFFECT"
                    ))
    
    def _validate_post_method(self, class_name: str, method_info: Dict[str, Any]):
        """Validate post() method implementation."""
        method = method_info['node']
        
        # Check for complex computation in post
        for node in ast.walk(method):
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                self.violations.append(BestPracticeViolation(
                    level=ViolationLevel.WARNING,
                    category="lifecycle",
                    file_path=self.current_file,
                    line_number=getattr(node, 'lineno', method_info['lineno']),
                    message=f"{class_name}.post(): Complex computation detected - should be in exec()",
                    suggestion="Move complex computation to exec() method",
                    rule_id="POST_COMPLEX_COMPUTATION"
                ))
    
    def _ast_to_string(self, node: ast.AST) -> str:
        """Convert AST node to string with proper fallback."""
        if hasattr(ast, 'unparse'):
            return ast.unparse(node)
        else:
            # Fallback for Python < 3.9
            if isinstance(node, ast.Attribute):
                value_str = self._ast_to_string(node.value) if hasattr(node, 'value') else 'unknown'
                return f"{value_str}.{node.attr}"
            elif isinstance(node, ast.Name):
                return node.id
            else:
                return 'unknown'

    def _is_external_call(self, node: ast.Call) -> bool:
        """Check if a call is to an external API."""
        # Look for common external call patterns
        external_patterns = ['requests.', 'urllib.', 'httpx.', 'aiohttp.', 'openai.']
        
        if isinstance(node.func, ast.Attribute):
            func_name = self._ast_to_string(node.func)
            return any(pattern in func_name for pattern in external_patterns)
        
        return False
    
    def _is_side_effect_call(self, node: ast.Call) -> bool:
        """Check if a call represents a side effect."""
        # Look for file operations, database operations, etc.
        side_effect_patterns = ['write(', 'save(', 'insert(', 'update(', 'delete(']
        
        if isinstance(node.func, ast.Name):
            # Removed 'print' - logging/debugging is acceptable in exec
            return node.func.id in ['open', 'write', 'save']
        elif isinstance(node.func, ast.Attribute):
            func_name = self._ast_to_string(node.func)
            return any(pattern in func_name for pattern in side_effect_patterns)
        
        return False


class BestPracticesValidator:
    """Main validator class for PocketFlow best practices."""
    
    def __init__(self):
        pass  # Removed unused instance variable
    
    def check_node_lifecycle(self, file_paths: List[Path]) -> List[BestPracticeViolation]:
        """Verify prep/exec/post lifecycle compliance."""
        violations = []
        
        analyzer = NodeLifecycleAnalyzer()
        for file_path in file_paths:
            if file_path.suffix == '.py':
                file_violations = analyzer.analyze_file(file_path)
                violations.extend(file_violations)
        
        return violations
    
    def check_batch_usage(self, file_paths: List[Path]) -> List[BestPracticeViolation]:
        """Identify collection processing that should use BatchNode."""
        violations = []
        
        for file_path in file_paths:
            if file_path.suffix == '.py':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Look for loop patterns that might benefit from BatchNode
                    if self._has_collection_processing_pattern(content):
                        violations.append(BestPracticeViolation(
                            level=ViolationLevel.INFO,
                            category="batch_usage",
                            file_path=str(file_path),
                            line_number=None,
                            message="File contains collection processing - consider BatchNode",
                            suggestion="Review if BatchNode would be more appropriate for collection processing",
                            rule_id="CONSIDER_BATCH_NODE"
                        ))
                
                except (OSError, IOError, UnicodeDecodeError) as e:
                    violations.append(BestPracticeViolation(
                        level=ViolationLevel.ERROR,
                        category="parsing",
                        file_path=str(file_path),
                        line_number=None,
                        message=f"File access error: {e}",
                        suggestion="Check file permissions and encoding",
                        rule_id="FILE_ACCESS_ERROR"
                    ))
        
        return violations
    
    def check_utility_patterns(self, utils_dir: Path) -> List[BestPracticeViolation]:
        """Ensure utilities follow PocketFlow philosophy."""
        violations = []
        
        if not utils_dir.exists():
            return violations
        
        for file_path in utils_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for complex logic in utilities
                if self._has_complex_logic_pattern(content):
                    violations.append(BestPracticeViolation(
                        level=ViolationLevel.WARNING,
                        category="utility_patterns",
                        file_path=str(file_path),
                        line_number=None,
                        message="Utility contains complex logic - consider moving to nodes",
                        suggestion="Keep utilities simple - move complex reasoning to nodes",
                        rule_id="UTILITY_COMPLEX_LOGIC"
                    ))
                
                # Check for missing main() test function
                if 'if __name__ == "__main__"' not in content:
                    violations.append(BestPracticeViolation(
                        level=ViolationLevel.INFO,
                        category="utility_patterns",
                        file_path=str(file_path),
                        line_number=None,
                        message="Utility missing testable main() function",
                        suggestion="Add 'if __name__ == \"__main__\":' block for standalone testing",
                        rule_id="UTILITY_MISSING_MAIN"
                    ))
                
            except (OSError, IOError, UnicodeDecodeError) as e:
                violations.append(BestPracticeViolation(
                    level=ViolationLevel.ERROR,
                    category="parsing", 
                    file_path=str(file_path),
                    line_number=None,
                    message=f"File access error: {e}",
                    suggestion="Check file permissions and encoding",
                    rule_id="FILE_ACCESS_ERROR"
                ))
        
        return violations
    
    def _has_collection_processing_pattern(self, content: str) -> bool:
        """Check if content has patterns suggesting collection processing."""
        patterns = [
            r'for\s+\w+\s+in\s+\w+\s*:.*process',  # for item in collection with processing
            r'\.map\(',                              # functional map
            r'\.filter\(',                           # functional filter
            r'BatchNode',                            # Already using BatchNode - skip
            r'\[.*for\s+\w+\s+in\s+.*\]',          # list comprehensions with processing
        ]
        
        # Skip if already using BatchNode
        if 'BatchNode' in content:
            return False
            
        # Look for multiple iteration patterns that might benefit from batching
        iteration_count = len(re.findall(r'for\s+\w+\s+in\s+', content))
        return iteration_count >= 2 or any(re.search(pattern, content) for pattern in patterns[:3])
    
    def _has_complex_logic_pattern(self, content: str) -> bool:
        """Check if utility contains complex logic patterns."""
        complex_patterns = [
            r'if\s+.*\s+else\s+.*\s+if',      # nested conditionals  
            r'for\s+.*\s+for',                 # nested loops
            r'while\s+.*:',                    # while loops
            r'try\s*:.*except.*:',             # try-except blocks (flow control)
            r'call_llm.*if.*else',             # conditional LLM calls
        ]
        
        return any(re.search(pattern, content, re.DOTALL) for pattern in complex_patterns)
    
    def validate_directory(self, directory: Path, checks: Optional[List[str]] = None) -> List[BestPracticeViolation]:
        """Validate all best practices for a directory."""
        all_violations = []
        
        # Default to all checks if none specified
        if checks is None:
            checks = ['lifecycle', 'batch', 'utility']
        
        # Find all Python files
        python_files = list(directory.rglob("*.py"))
        
        # Check node lifecycle patterns
        if 'lifecycle' in checks:
            lifecycle_violations = self.check_node_lifecycle(python_files)
            all_violations.extend(lifecycle_violations)
        
        # Check batch usage patterns
        if 'batch' in checks:
            batch_violations = self.check_batch_usage(python_files)
            all_violations.extend(batch_violations)
        
        # Check utility patterns
        if 'utility' in checks:
            utils_dir = directory / "utils"
            utility_violations = self.check_utility_patterns(utils_dir)
            all_violations.extend(utility_violations)
        
        return all_violations


def format_violations(violations: List[BestPracticeViolation]) -> str:
    """Format violations for display."""
    if not violations:
        return "✅ No best practice violations found!"
    
    # Group by level
    errors = [v for v in violations if v.level == ViolationLevel.ERROR]
    warnings = [v for v in violations if v.level == ViolationLevel.WARNING] 
    infos = [v for v in violations if v.level == ViolationLevel.INFO]
    
    output = []
    output.append("📊 Best Practices Validation Results:")
    output.append(f"   Errors: {len(errors)}")
    output.append(f"   Warnings: {len(warnings)}")
    output.append(f"   Info: {len(infos)}")
    output.append("")
    
    for level_name, level_violations in [("ERRORS", errors), ("WARNINGS", warnings), ("INFO", infos)]:
        if level_violations:
            output.append(f"🚨 {level_name}:")
            for violation in level_violations:
                file_name = Path(violation.file_path).name
                location = f"{file_name}:{violation.line_number}" if violation.line_number else file_name
                output.append(f"   [{violation.rule_id}] {location}")
                output.append(f"      {violation.message}")
                output.append(f"      💡 {violation.suggestion}")
                output.append("")
    
    return "\n".join(output)


def main():
    """Main validation script."""
    parser = argparse.ArgumentParser(
        description="Validate PocketFlow best practices compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate current directory
  python validate-best-practices.py
  
  # Validate specific workflow
  python validate-best-practices.py --workflow .agent-os/workflows/my-workflow
  
  # Validate with specific checks only
  python validate-best-practices.py --checks lifecycle,batch
        """
    )
    
    parser.add_argument(
        "--workflow", 
        type=Path,
        help="Specific workflow directory to validate"
    )
    
    parser.add_argument(
        "--checks",
        help="Comma-separated list of checks: lifecycle,batch,utility (default: all)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    # Determine target directory
    if args.workflow:
        target_dir = args.workflow
        if not target_dir.exists():
            print(f"❌ Error: Directory {target_dir} not found")
            return 1
    else:
        # Look for .agent-os/workflows or current directory
        target_dir = Path(".agent-os/workflows") if Path(".agent-os/workflows").exists() else Path(".")
    
    # Parse checks parameter
    checks = None
    if args.checks:
        checks = [check.strip() for check in args.checks.split(',')]
        valid_checks = ['lifecycle', 'batch', 'utility']
        invalid_checks = [c for c in checks if c not in valid_checks]
        if invalid_checks:
            print(f"❌ Error: Invalid checks: {invalid_checks}")
            print(f"Valid checks are: {valid_checks}")
            return 1
    
    # Run validation
    validator = BestPracticesValidator()
    violations = validator.validate_directory(target_dir, checks)
    
    # Display results
    output = format_violations(violations)
    print(output)
    
    # Return appropriate exit code
    error_count = len([v for v in violations if v.level == ViolationLevel.ERROR])
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())