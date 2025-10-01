# Good PocketFlow Examples ✅

These examples demonstrate **correct** PocketFlow patterns. Use these as templates and learning resources.

## Files Overview

### [`batch_processing.py`](./batch_processing.py)
**Demonstrates:** Correct batch processing patterns
- ✅ `BatchNode` for synchronous collection processing
- ✅ `AsyncParallelBatchNode` for concurrent I/O operations
- ✅ Proper error handling with partial failure support
- ✅ Batch statistics and progress tracking
- ✅ Clean separation of concerns

**Key takeaways:**
- Use `BatchNode` when processing collections of similar items
- Handle partial failures gracefully with success rate thresholds
- Track batch statistics for monitoring and debugging
- Use `AsyncParallelBatchNode` for I/O-heavy operations

### [`error_handling.py`](./error_handling.py)
**Demonstrates:** Proper error handling in PocketFlow
- ✅ Exception-to-branch conversion using `exec_fallback()`
- ✅ Error classification for routing decisions
- ✅ Clean separation of happy path and error handling
- ✅ Retry logic with exponential backoff
- ✅ Circuit breaker patterns for external services

**Key takeaways:**
- Let exceptions propagate naturally from `exec()`
- Use `exec_fallback()` to convert exceptions to routing decisions
- Classify errors for appropriate handling strategies
- Implement dedicated error recovery nodes

### [`shared_store_usage.py`](./shared_store_usage.py)
**Demonstrates:** Correct SharedStore access patterns
- ✅ Clear schema documentation with `REQUIRED_KEYS`/`PRODUCES_KEYS`
- ✅ Data access only in `prep()` and `post()` methods
- ✅ No SharedStore access in `exec()` methods
- ✅ Structured data with consistent naming conventions
- ✅ Data aggregation from multiple SharedStore sources

**Key takeaways:**
- Document your SharedStore schema clearly
- Never access `self.shared` in `exec()` methods
- Use structured data with clear naming patterns
- Validate SharedStore state and perform cleanup

### [`utility_patterns.py`](./utility_patterns.py)
**Demonstrates:** Well-designed utility functions
- ✅ Simple, focused functions with single responsibilities
- ✅ Pure functions without side effects
- ✅ Clear input/output contracts
- ✅ No business logic in utilities
- ✅ Proper error handling (return None vs exceptions)

**Key takeaways:**
- Keep utilities simple and focused on technical operations
- Use pure functions that don't modify global state
- Return structured results or None for error handling
- Provide clear documentation and examples

## Usage Patterns

### Quick Reference

| Pattern | File | Key Class/Function | Use Case |
|---------|------|-------------------|----------|
| Batch Processing | `batch_processing.py` | `DocumentBatchProcessor` | Processing multiple documents |
| Async Batch | `batch_processing.py` | `AsyncDocumentProcessor` | Concurrent API calls |
| Error Handling | `error_handling.py` | `DataValidationNode` | Input validation with fallbacks |
| API Error Handling | `error_handling.py` | `ExternalAPINode` | External service calls |
| SharedStore Schema | `shared_store_usage.py` | `SharedStoreSchemaNode` | Basic data processing |
| Data Aggregation | `shared_store_usage.py` | `DataAggregatorNode` | Combining multiple data sources |
| File Operations | `utility_patterns.py` | `read_file_safe()` | Safe file reading |
| HTTP Requests | `utility_patterns.py` | `make_http_request()` | External API calls |

### Copy-Paste Templates

**Basic Node Template:**
```python
class MyProcessingNode(Node):
    REQUIRED_KEYS = ['input_data', 'config']
    PRODUCES_KEYS = ['processed_data', 'metadata']
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        # Data access and validation only
        return {'data': shared['input_data'], 'config': shared['config']}
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        # All computation here, no SharedStore access
        return {'result': process(prep_result['data'])}
    
    def post(self, shared, prep_result, exec_result) -> Optional[str]:
        # Store results and route
        shared['processed_data'] = exec_result['result']
        return None
```

**Error Handling Template:**
```python
def exec_fallback(self, prep_result, exception: Exception) -> Dict[str, Any]:
    return {
        'error_type': self._classify_error(exception),
        'error_message': str(exception)
    }

def post_fallback(self, shared, prep_result, fallback_result) -> str:
    shared['error'] = fallback_result
    return "error_occurred"
```

**Utility Function Template:**
```python
def simple_operation(input_data: InputType, options: Optional[Dict] = None) -> Optional[OutputType]:
    """Simple utility function with clear contract."""
    try:
        # Simple operation logic
        return process_data(input_data, options or {})
    except (ExpectedError1, ExpectedError2):
        return None  # Let caller handle the None case
```

## Running Examples

Each example file can be run independently:

```bash
# Test batch processing examples
python templates/examples/good/batch_processing.py

# Test error handling examples  
python templates/examples/good/error_handling.py

# Test shared store usage examples
python templates/examples/good/shared_store_usage.py

# Test utility patterns examples
python templates/examples/good/utility_patterns.py
```

## Integration with Your Workflow

1. **Copy and modify**: Use these as starting points for your own nodes
2. **Study the patterns**: Understand why these patterns work well
3. **Validate your code**: Use these as reference for best practices
4. **Test understanding**: Try to identify what makes these examples "good"

## Next Steps

- Review the [bad examples](../bad/) to understand what to avoid
- Read the [main README](../README.md) for comprehensive guidance
- Use the validation tools to check your implementations
- Refer to [PocketFlow Best Practices](../../../docs/POCKETFLOW_BEST_PRACTICES.md)