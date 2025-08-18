# Template Validator Troubleshooting Guide

> Agent OS + PocketFlow Framework - Template Validator Issues & Solutions
> Last Updated: 2025-01-18
>
> **Framework Context**: This guide addresses template validation issues in the framework generator, not end-user implementation problems.

---

## Quick Reference

### Common Commands
```bash
# Validate a generated template directory
bash scripts/validation/validate-template-structure.sh path/to/template

# Use Python validator directly  
python .agent-os/workflows/template_validator.py path/to/template

# Run sub-agent validation checks
bash scripts/validation/validate-sub-agents.sh
```

### Quick Fixes
- **Syntax Errors**: Check for escaped characters in generator smart defaults
- **Missing Methods**: Ensure generator includes all required PocketFlow methods
- **Import Issues**: Verify generator import statements are correct
- **Pattern Violations**: Update generator templates to match PocketFlow API changes

---

## Error Categories and Solutions

### 1. Python Syntax Errors

#### Error: "Syntax error: unexpected character after line continuation character"

**Cause**: Escaped newline characters (`\\n`) in generator string templates

**Example Problem**:
```python
# In generator.py smart defaults:
"exec": 'result = process_data(prep_result)\\n        return result'
```

**Solution**:
```python
# Fix the generator code:
"exec": 'result = process_data(prep_result)\n        return result'
```

**Location**: Check `.agent-os/workflows/generator.py` in smart defaults functions

#### Error: "AST parsing failed: invalid syntax"

**Cause**: Malformed Python code in generated templates

**Debugging Steps**:
1. Identify the specific file with syntax errors
2. Check generator template code for that file type
3. Test template generation with minimal examples
4. Validate generator string formatting

**Common Fixes**:
- Fix f-string formatting in generator code
- Correct indentation in multi-line template strings  
- Ensure proper quoting in generated code
- Validate template variable substitution

### 2. PocketFlow Pattern Violations

#### Error: "Missing required prep() method"

**Cause**: Generator not creating required PocketFlow methods

**Solution**: Update generator's `_generate_nodes()` method to include all required methods

**Template Fix**:
```python
# Ensure generator includes:
def prep(self, shared: Dict[str, Any]) -> Any:
    """Data preparation and validation."""
    # TODO: Implementation guidance
    
def exec(self, prep_result: Any) -> Any:  # or exec_async for AsyncNode
    """Core processing logic."""  
    # TODO: Implementation guidance
    
def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:
    """Post-processing and result storage."""
    # TODO: Implementation guidance
```

#### Error: "Missing required exec_async() method for async node"

**Cause**: Validator not detecting async methods or generator creating wrong method type

**Debugging**:
1. Check if node inherits from AsyncNode but has `exec()` instead of `exec_async()`
2. Verify validator handles `ast.AsyncFunctionDef` correctly
3. Confirm generator smart defaults match node type

**Solution**: Ensure generator creates appropriate method based on node type:
```python
# In generator _generate_nodes():
exec_method = "async def exec_async" if is_async_node else "def exec"
```

#### Error: "Flow class missing required structure"

**Cause**: Generator not creating proper Flow class structure

**Required Structure**:
```python
class MyFlow(Flow):
    def __init__(self):
        nodes = {
            "node1": Node1(),
            "node2": Node2(),
        }
        
        edges = {
            "node1": {"success": "node2", "error": "error_handler"},
            "node2": {"success": None, "error": "error_handler"},
        }
        
        super().__init__(nodes=nodes, edges=edges)
```

### 3. Import and Dependency Issues

#### Error: "Missing PocketFlow imports"

**Cause**: Generator not including required imports

**Solution**: Update generator import generation:
```python
# Ensure these imports in generated files:
from pocketflow import Node, AsyncNode, BatchNode, Flow
from typing import Dict, Any
from pydantic import BaseModel
```

#### Error: "BaseModel used but not imported from pydantic"

**Cause**: Generator creating Pydantic models without proper imports

**Fix**: Update `_generate_pydantic_models()` method:
```python
models = [
    "from pydantic import BaseModel, Field, validator",
    "from typing import Dict, List, Optional, Any",
    # ... rest of model generation
]
```

### 4. Validation Logic Issues

#### Error: "Validator not detecting async functions"

**Cause**: AST visitor only checking `ast.FunctionDef`, not `ast.AsyncFunctionDef`

**Solution**: Update validator to handle both:
```python
if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
    methods[item.name] = {
        'lineno': item.lineno,
        'args': [arg.arg for arg in item.args.args],
        'is_async': isinstance(item, ast.AsyncFunctionDef)
    }
```

#### Error: "Template validation module not available"

**Cause**: Import path issues or missing validator module

**Debugging**:
1. Check if `.agent-os/workflows/template_validator.py` exists
2. Verify Python path configuration in generator
3. Test validator module import manually

**Solution**:
```python
# In generator coordinate_template_validation():
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from template_validator import PocketFlowValidator
```

### 5. Educational Quality Issues

#### Warning: "Found generic TODO comments"

**Cause**: Generator creating TODO comments like "TODO: implement"

**Solution**: Enhance generator smart defaults with specific guidance:
```python
# Poor:
"# TODO: implement this function"

# Better:
"# TODO: Connect to your vector database and search for relevant documents\n# Use similarity search with the query embedding"
```

#### Warning: "Utility file should raise NotImplementedError"

**Cause**: Generator not including proper error handling in utility functions

**Solution**: Update utility generation:
```python
# In _generate_utility():
f'    raise NotImplementedError("Utility function {utility["name"]} not implemented - {utility["description"]}")'
```

### 6. Integration Issues

#### Error: "Validation failed during generation"

**Cause**: Generator changes broke validation integration

**Debugging Steps**:
1. Test generator independently of validation
2. Test validator independently of generator  
3. Check coordination function error handling
4. Verify file paths and permissions

**Solution**: Add proper error handling in generator:
```python
def coordinate_template_validation(self, template_path: str) -> ValidationResult:
    try:
        # validation logic
    except ImportError:
        return ValidationResult(is_valid=True, warnings=["Validation skipped"])
    except Exception as e:
        return ValidationResult(is_valid=False, errors=[f"Validation failed: {e}"])
```

---

## Diagnostic Commands

### Test Generator Output
```bash
# Create test template
cd .agent-os/workflows
python -c "
from generator import PocketFlowGenerator, WorkflowSpec
spec = WorkflowSpec(name='Test', pattern='AGENT', description='Test workflow', nodes=[])
gen = PocketFlowGenerator(templates_path='../..', output_path='test_output')
gen.templates = {}
files = gen.generate_workflow(spec)
gen.save_workflow(spec, files)
"
```

### Test Validator Independently
```bash
# Run validator on existing template
python .agent-os/workflows/template_validator.py path/to/template
```

### Test Sub-Agent Integration
```bash
# Check if template-validator agent is properly configured
bash scripts/validation/validate-sub-agents.sh
```

### Debug AST Issues
```bash
# Test Python syntax on specific file
python -c "
import ast
with open('path/to/file.py') as f:
    content = f.read()
    tree = ast.parse(content)
    print('Syntax valid')
"
```

---

## Performance Issues

### Slow Validation
**Cause**: Large template directories or inefficient validation logic

**Solutions**:
- Implement validation result caching
- Skip validation for unchanged files
- Parallel validation for multiple files
- Optimize AST parsing logic

### Memory Issues
**Cause**: Large AST trees or memory leaks in validation

**Solutions**:
- Process files individually rather than batch
- Clear AST references after validation
- Monitor memory usage during validation

---

## Framework Development Workflow

### Adding New Validation Rules

1. **Update Template Standards**: Document new criteria in `template-standards.md`
2. **Implement Validator Logic**: Add validation functions to `template_validator.py`
3. **Test with Examples**: Create test cases for new validation rules
4. **Update Generator**: Ensure generator creates compliant templates
5. **Document Troubleshooting**: Add common issues and solutions to this guide

### Testing Validation Changes

1. **Unit Tests**: Test individual validation functions
2. **Integration Tests**: Test with generated templates
3. **Regression Tests**: Ensure existing templates still validate
4. **Performance Tests**: Verify validation speed with large templates

### Debugging Validation Issues

1. **Isolate Problem**: Test generator and validator separately
2. **Check File Contents**: Manually inspect generated files
3. **Trace Execution**: Add debugging output to validation logic
4. **Compare Working**: Diff against known good templates

---

## Getting Help

### Internal Resources
- **Template Standards**: `.agent-os/instructions/orchestration/template-standards.md`
- **Sub-Agent Config**: `.claude/agents/template-validator.md`
- **Implementation Docs**: `docs/sub-agents-implementation.md`

### Diagnostic Files
- **Validator Module**: `.agent-os/workflows/template_validator.py`
- **Generator Module**: `.agent-os/workflows/generator.py`  
- **Validation Scripts**: `scripts/validation/`

### Common Investigation Steps
1. Check recent changes to generator code
2. Test with minimal example templates
3. Compare with working validation examples
4. Review error messages for specific line numbers
5. Check file permissions and path issues

---

## Framework Philosophy Reminder

When troubleshooting template validation:

- **Templates are learning tools**: Validation ensures educational quality, not completeness
- **Missing implementations are intentional**: Don't "fix" TODO stubs or NotImplementedError
- **Framework generates starting points**: Validation maintains structure for user customization
- **Quality over completeness**: Better to have clear placeholders than completed implementations

The Template Validator maintains the balance between structural correctness and educational value, ensuring the framework generates high-quality starting points for PocketFlow development.