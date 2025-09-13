# PocketFlow Example Templates

This directory contains reference implementations demonstrating correct and incorrect PocketFlow patterns. These examples serve as:

- **Learning Resources**: Clear examples of proper PocketFlow design
- **Copy-Paste Templates**: Starting points for new implementations
- **Validation Test Cases**: Examples for testing validation tools
- **Antipattern Education**: What NOT to do and why

## Directory Structure

```
templates/examples/
├── good/                          # ✅ CORRECT patterns to follow
│   ├── batch_processing.py        # Proper batch node usage
│   ├── error_handling.py          # Exception-to-branch conversion
│   ├── shared_store_usage.py      # Clean data access patterns
│   └── utility_patterns.py        # Simple, focused utilities
└── bad/                           # ❌ ANTIPATTERNS to avoid
    ├── monolithic_node.py         # Multiple responsibilities
    ├── hidden_logic.py            # Business logic in utilities
    └── lifecycle_violations.py    # prep/exec/post violations
```

## Good Examples (✅ Use These)

### `good/batch_processing.py`

**What it demonstrates:**
- Correct use of `BatchNode` for collection processing
- Proper use of `AsyncParallelBatchNode` for concurrent I/O
- Error handling with partial failure support
- Batch statistics tracking
- Clear separation of concerns

**Key patterns:**
```python
class DocumentBatchProcessor(BatchNode):
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        # Only data access and validation
        documents = shared.get('documents', [])
        return {'documents': documents, 'batch_size': batch_size}
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        # Pure batch processing logic
        # No SharedStore access here!
        return {'processed_results': results, 'batch_stats': stats}
    
    def post(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        # Store results and route based on success rate
        shared['processed_documents'] = exec_result['processed_results']
        return "partial_failure" if success_rate < 0.9 else None
```

**When to use:** When processing collections of similar items (documents, files, API calls).

### `good/error_handling.py`

**What it demonstrates:**
- Exception-to-branch conversion pattern
- Use of `exec_fallback()` and `post_fallback()` methods
- Error classification for routing decisions
- Clean separation of happy path and error handling
- Retry logic and circuit breaker patterns

**Key patterns:**
```python
class DataValidationNode(Node):
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        # Pure validation logic - let exceptions propagate
        validate_required_fields(data, rules)  # May raise ValueError
        return {'validated_data': data}
    
    def exec_fallback(self, prep_result, exception: Exception) -> Dict[str, Any]:
        # Convert exception to structured error info
        return {
            'error_type': self._classify_error(exception),
            'error_message': str(exception)
        }
    
    def post_fallback(self, shared, prep_result, fallback_result) -> str:
        # Convert error info to routing decision
        shared['validation_error'] = fallback_result
        return "validation_failed"
```

**When to use:** For any node that might encounter errors, especially validation and external API calls.

### `good/shared_store_usage.py`

**What it demonstrates:**
- Clear SharedStore schema documentation
- Data access only in `prep()` and `post()`
- No SharedStore access in `exec()`
- Structured data with consistent naming
- Data aggregation from multiple sources

**Key patterns:**
```python
class SharedStoreSchemaNode(Node):
    REQUIRED_KEYS = ['user_data', 'processing_config']
    PRODUCES_KEYS = ['processed_user', 'processing_metadata']
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        # All SharedStore reading here
        for key in self.REQUIRED_KEYS:
            if key not in shared:
                raise ValueError(f"Required key '{key}' missing")
        return {'user_data': shared['user_data'], 'config': shared['processing_config']}
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        # Only uses prep_result - NO SharedStore access
        return {'processed_user': process_user(prep_result['user_data'])}
    
    def post(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        # All SharedStore writing here
        shared['processed_user'] = exec_result['processed_user']
        return None
```

**When to use:** For all nodes - this is the fundamental PocketFlow data access pattern.

### `good/utility_patterns.py`

**What it demonstrates:**
- Simple, focused utility functions
- Pure functions without side effects
- Clear input/output contracts
- No business logic in utilities
- External service abstraction

**Key patterns:**
```python
def read_file_safe(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
    """Simple file reading - returns None on error."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError):
        return None

def make_http_request(url: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[Dict]:
    """HTTP utility - returns structured result or None."""
    try:
        response = requests.post(url, json=data) if method == 'POST' else requests.get(url)
        return {'status_code': response.status_code, 'data': response.json()}
    except requests.RequestException:
        return None
```

**When to use:** For simple, reusable operations that don't contain business logic.

## Bad Examples (❌ Avoid These)

### `bad/monolithic_node.py`

**What it shows (DON'T DO):**
- Nodes with multiple responsibilities
- `exec()` methods longer than 50 lines
- Multiple LLM calls in one node
- Class names with multiple verbs (ProcessAndValidateAndSend)
- Complex routing logic due to too many failure modes

**Why it's bad:**
- Hard to test individual components
- Difficult to debug when errors occur
- Cannot reuse parts of functionality
- Error handling becomes overly complex
- Violates single responsibility principle

**How to fix:** Split into focused nodes with single responsibilities.

### `bad/hidden_logic.py`

**What it shows (DON'T DO):**
- Business logic hidden in utility functions
- LLM calls in utilities instead of nodes
- Complex decision making in utilities
- "Smart" utilities that appear simple but do complex work

**Why it's bad:**
- Business logic is invisible in flow diagrams
- LLM calls don't get proper retry handling
- Makes testing and debugging difficult
- Violates the principle that utilities should be simple

**How to fix:** Move business logic to nodes, keep utilities simple and pure.

### `bad/lifecycle_violations.py`

**What it shows (DON'T DO):**
- Accessing `self.shared` in `exec()` methods
- Complex computation in `prep()` methods
- External calls in `post()` methods
- Mixing sync and async operations incorrectly
- Using BatchNode for single items

**Why it's bad:**
- Breaks framework retry mechanisms
- Makes nodes untestable in isolation
- Violates the prep/exec/post lifecycle pattern
- Causes async/sync conflicts

**How to fix:** Follow the strict lifecycle pattern - data access in prep/post, computation in exec.

## Usage Guidelines

### For Learning

1. **Start with good examples**: Read through the `good/` directory to understand proper patterns
2. **Study the antipatterns**: Review `bad/` examples to learn what to avoid
3. **Compare implementations**: See how the same functionality should vs shouldn't be implemented

### For Development

1. **Copy good templates**: Use `good/` examples as starting points for new nodes
2. **Validate against bad patterns**: Check your code against the antipatterns
3. **Use validation tools**: Run the antipattern detector on your implementations

### For Testing Validators

1. **Good examples should pass**: Validation tools should approve `good/` examples
2. **Bad examples should fail**: Antipattern detectors should flag `bad/` examples
3. **Test specific patterns**: Use individual examples to test specific validation rules

## Integration with Validation Tools

These examples are designed to work with the PocketFlow validation framework:

### Best Practices Validator
```bash
# Should pass without violations
python scripts/validation/validate-best-practices.py templates/examples/good/

# Should identify violations
python scripts/validation/validate-best-practices.py templates/examples/bad/
```

### Antipattern Detector
```bash
# Should find no antipatterns
python framework-tools/antipattern_detector.py templates/examples/good/

# Should detect multiple antipatterns
python framework-tools/antipattern_detector.py templates/examples/bad/
```

## Common Patterns Summary

### ✅ DO (Good Patterns)

| Pattern | Example | Use When |
|---------|---------|-----------|
| Single responsibility nodes | `DataValidationNode` only validates | Always |
| BatchNode for collections | `DocumentBatchProcessor` | Processing multiple similar items |
| Exception-to-branch conversion | `exec_fallback()` → routing | Any error-prone operations |
| Pure utilities | `read_file_safe()` | Simple, reusable operations |
| Clear SharedStore schema | `REQUIRED_KEYS` documentation | All nodes |

### ❌ DON'T (Antipatterns)

| Antipattern | Example | Why Bad |
|-------------|---------|---------|
| Monolithic nodes | `ProcessAndValidateAndSendNode` | Hard to test, debug, reuse |
| SharedStore in exec() | `self.shared['key']` in exec | Breaks retry mechanisms |
| Business logic in utils | LLM calls in utilities | Invisible complexity |
| Complex prep/post | Computation in prep() | Violates lifecycle pattern |
| Wrong node types | BatchNode for single items | Defeats purpose of node types |

## Examples in Production

These templates can be used as-is or adapted for real applications:

1. **File Processing Workflows**: Use batch processing patterns for document processing
2. **API Integration**: Use error handling patterns for external service calls
3. **Data Validation Pipelines**: Use shared store patterns for multi-step validation
4. **Utility Libraries**: Use utility patterns for common operations

## Contributing

When adding new examples:

1. **Good examples**: Should demonstrate a specific pattern clearly
2. **Bad examples**: Should show why the antipattern is problematic
3. **Documentation**: Include clear explanations of what/why/how
4. **Testing**: Ensure examples work with validation tools

## Related Documentation

- [PocketFlow Best Practices](../../docs/POCKETFLOW_BEST_PRACTICES.md)
- [Validation Tools](../../framework-tools/README.md)
- [Implementation Plan](../../docs/POCKETFLOW_IMPLEMENTATION_PLAN.md)
- [Standards Documentation](../../standards/)