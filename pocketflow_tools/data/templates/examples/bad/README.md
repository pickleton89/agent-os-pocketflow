# Bad PocketFlow Examples ❌

⚠️ **WARNING: These examples demonstrate ANTIPATTERNS - what NOT to do in PocketFlow.**

These examples are educational tools showing common mistakes and why they're problematic. **DO NOT copy these patterns** - use the [good examples](../good/) instead.

## Files Overview

### [`monolithic_node.py`](./monolithic_node.py)
**Demonstrates:** Monolithic node antipatterns
- ❌ Nodes with multiple responsibilities
- ❌ `exec()` methods longer than 50 lines
- ❌ Multiple LLM calls in one node
- ❌ Class names with multiple verbs (ProcessAndValidateAndSend)
- ❌ God classes that know about everything

**Why it's bad:**
- Hard to test individual components
- Difficult to debug when errors occur
- Cannot reuse parts of functionality
- Error handling becomes overly complex
- Violates single responsibility principle

**How to fix:** Split into focused nodes with single responsibilities.

### [`hidden_logic.py`](./hidden_logic.py)
**Demonstrates:** Business logic hidden in utilities
- ❌ LLM calls in utility functions
- ❌ Complex business decisions in utilities
- ❌ "Smart" utilities that appear simple but do complex work
- ❌ External API calls in utilities
- ❌ Nodes that delegate complexity to utilities

**Why it's bad:**
- Business logic is invisible in flow diagrams
- LLM calls don't get proper retry handling
- Makes testing and debugging difficult
- Violates the principle that utilities should be simple

**How to fix:** Move business logic to nodes, keep utilities simple and pure.

### [`lifecycle_violations.py`](./lifecycle_violations.py)
**Demonstrates:** prep/exec/post lifecycle violations
- ❌ Accessing `self.shared` in `exec()` methods
- ❌ Complex computation in `prep()` methods
- ❌ External calls in `post()` methods
- ❌ Mixing sync and async operations incorrectly
- ❌ Using BatchNode for single items

**Why it's bad:**
- Breaks framework retry mechanisms
- Makes nodes untestable in isolation
- Violates the prep/exec/post lifecycle pattern
- Causes async/sync conflicts

**How to fix:** Follow the strict lifecycle pattern - data access in prep/post, computation in exec.

## Common Antipatterns Explained

### 1. Monolithic Nodes
```python
# ❌ BAD: One node doing everything
class ProcessAndValidateAndSendNode(Node):
    def exec(self, prep_result):
        # 100+ lines of code doing:
        # - Data validation
        # - Data processing  
        # - API calls
        # - Email sending
        # - File operations
        # - Report generation
        # - Multiple LLM calls
        pass

# ✅ GOOD: Split into focused nodes
class DataValidationNode(Node): pass
class DataProcessingNode(Node): pass  
class ExternalAPINode(AsyncNode): pass
class EmailSendingNode(AsyncNode): pass
# etc.
```

### 2. Hidden Business Logic
```python
# ❌ BAD: Complex business logic in utilities
def process_customer_data(customer, rules):
    # Hidden inside: risk scoring, LLM calls, 
    # business decisions, external API calls
    if customer['tier'] == 'premium':
        llm_result = call_llm(...)  # Hidden!
        if risk_score > threshold:
            make_api_call(...)      # Hidden!
    return enhanced_customer

# ✅ GOOD: Business logic in nodes, simple utilities
def normalize_name(name: str) -> str:
    return name.strip().title()

def validate_email(email: str) -> bool:
    return '@' in email and '.' in email.split('@')[-1]
```

### 3. Lifecycle Violations
```python
# ❌ BAD: SharedStore access in exec()
class ViolatingNode(Node):
    def exec(self, prep_result):
        user_data = self.shared['user_data']  # WRONG!
        self.shared['status'] = 'processing'  # WRONG!
        return result

# ✅ GOOD: Proper lifecycle
class CorrectNode(Node):
    def prep(self, shared: SharedStore):
        return {'user_data': shared['user_data']}
    
    def exec(self, prep_result):
        # Only use prep_result, never self.shared
        return process(prep_result['user_data'])
    
    def post(self, shared, prep_result, exec_result):
        shared['processed_user'] = exec_result
```

## Validation Tool Testing

These examples are designed to be caught by PocketFlow validation tools:

### Expected Antipattern Detector Results

```bash
$ python framework-tools/antipattern_detector.py templates/examples/bad/

# Should detect:
# - Monolithic node syndrome
# - SharedStore access in exec()
# - Business logic in utilities
# - Lifecycle method confusion
# - Blocking I/O in regular nodes
# - Multiple LLM calls per node
```

### Expected Best Practices Validator Results

```bash
$ python scripts/validation/validate-best-practices.py templates/examples/bad/

# Should identify violations:
# - Missing lifecycle methods
# - Improper method responsibilities
# - Wrong node type selection
# - Complex utility functions
```

## Learning Exercise

For each bad example, try to:

1. **Identify the problems**: What specific antipatterns do you see?
2. **Understand why it's bad**: What problems would this cause in practice?
3. **Design a fix**: How would you split this into proper PocketFlow patterns?
4. **Compare with good examples**: How do the good examples solve this correctly?

### Example Analysis: `ProcessAndValidateAndSendNode`

**Problems identified:**
- 8 different responsibilities in one node
- 100+ line exec() method
- 3 different LLM calls
- Mix of validation, processing, I/O, and notification logic

**Why it's bad:**
- If email fails, entire process fails
- Can't test validation logic in isolation
- Can't reuse email sending in other flows
- Debug complexity: which of 8 operations failed?

**Correct design:**
```
DataValidationNode → DataProcessingNode → ExternalAPINode
                                      → DatabaseNode
                                      → EmailNode
                                      → ReportNode
```

## DO NOT USE THESE IN PRODUCTION

These examples are intentionally broken and should never be used in real applications. They exist solely for:

1. **Education**: Understanding what not to do
2. **Validation testing**: Ensuring detection tools work correctly
3. **Code review training**: Recognizing antipatterns in real code
4. **Design discussions**: Explaining why certain patterns are problematic

## How to Fix Antipatterns

### General Principles

1. **Single Responsibility**: Each node should do one thing well
2. **Clear Dependencies**: Make external calls explicit in dedicated nodes
3. **Proper Lifecycle**: Follow prep (data) → exec (compute) → post (effects)
4. **Simple Utilities**: Keep utilities pure and focused on technical operations
5. **Explicit Flow**: Business logic should be visible in the flow structure

### Refactoring Steps

1. **Identify responsibilities**: List what the monolithic node does
2. **Create focused nodes**: One node per responsibility  
3. **Design data flow**: Define SharedStore keys between nodes
4. **Extract utilities**: Move technical operations to simple utilities
5. **Test individually**: Each node should be testable in isolation

## Next Steps

- Study the [good examples](../good/) to see correct patterns
- Read the [main README](../README.md) for comprehensive guidance
- Use validation tools on your own code to catch these antipatterns
- Review [PocketFlow Best Practices](../../../docs/POCKETFLOW_BEST_PRACTICES.md) for detailed guidelines

Remember: **These are examples of what NOT to do. Always use the good examples as your reference!**