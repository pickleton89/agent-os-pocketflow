# PocketFlow Migration Guides

Step-by-step guides for fixing common antipatterns and improving PocketFlow implementations.

## Overview

These migration guides help you systematically refactor existing PocketFlow code to follow best practices. Each guide provides:

- **Problem identification**: How to spot the antipattern
- **Risk assessment**: What problems the current code might cause
- **Step-by-step migration**: Detailed refactoring steps
- **Testing strategy**: How to verify the migration was successful
- **Time estimates**: Expected effort for the migration

## Available Migration Guides

### Critical Severity

| Guide | Antipattern | Time Estimate |
|-------|-------------|---------------|
| [Monolithic to Focused Nodes](monolithic-to-focused.md) | Monolithic Node Syndrome | 2-4 hours |
| [Remove Shared Store from exec()](remove-shared-store-exec.md) | Shared Store Access in exec() | 30-60 minutes |

### High/Medium Severity

| Guide | Antipattern | Time Estimate |
|-------|-------------|---------------|
| [Fix Lifecycle Violations](fix-lifecycle-violations.md) | Lifecycle Method Confusion | 1-2 hours |
| [Move Logic from Utils to Nodes](utils-to-nodes.md) | Business Logic in Utilities | 2-3 hours |
| [Async Collection Processing](async-collection-processing.md) | Synchronous Collection Processing | 1-2 hours |

## Quick Assessment

Use this checklist to identify which migration guides you need:

### 🔴 Critical Issues (Fix First)
- [ ] `exec()` methods longer than 20 lines
- [ ] Multiple LLM calls in single `exec()` method
- [ ] Direct `self.shared[key]` access in `exec()` methods
- [ ] Class names with multiple verbs (ProcessAndValidate, FetchParseStore)

### 🟡 High Priority Issues
- [ ] LLM calls in utility functions
- [ ] Complex branching logic in utility functions
- [ ] LLM calls in `prep()` methods
- [ ] Complex computation in `prep()` or `post()` methods

### 🟠 Medium Priority Issues  
- [ ] Loops in regular Node `exec()` methods (should use BatchNode)
- [ ] Blocking I/O in regular Node (should use AsyncNode)
- [ ] Mixed sync/async patterns

## General Migration Strategy

### 1. Assessment Phase (15-30 minutes)
```bash
# Run antipattern detection
python pocketflow-tools/antipattern_detector.py your_code/

# Run best practices validation  
python scripts/validation/validate-best-practices.py your_code/
```

### 2. Planning Phase (30-60 minutes)
- Prioritize critical issues first
- Group related changes together
- Plan testing approach
- Estimate time and resources needed

### 3. Migration Phase (varies by guide)
- Follow specific migration guide steps
- Make incremental changes
- Test after each major change
- Update documentation as needed

### 4. Validation Phase (30 minutes)
```bash
# Verify antipatterns are fixed
python pocketflow-tools/antipattern_detector.py your_code/

# Run comprehensive tests
python -m pytest tests/

# Validate best practices
python scripts/validation/validate-best-practices.py your_code/
```

## Risk Mitigation

### Before Starting Migration
1. **Create a backup branch**: `git checkout -b pre-migration-backup`
2. **Document current behavior**: Note any quirks or special cases
3. **Identify dependencies**: List what other code depends on the current implementation
4. **Plan rollback strategy**: Know how to revert if problems occur

### During Migration
1. **Make incremental changes**: Small, testable steps
2. **Run tests frequently**: Don't accumulate untested changes
3. **Commit working states**: Save progress with descriptive commit messages
4. **Monitor for regressions**: Watch for unexpected behavior changes

### After Migration
1. **Performance testing**: Ensure new code performs adequately
2. **Integration testing**: Verify compatibility with dependent code
3. **Documentation updates**: Update any relevant documentation
4. **Team communication**: Notify team of significant changes

## Common Migration Patterns

### Pattern: Split Large Methods
```python
# Before: Monolithic exec() method
def exec(self, prep_result):
    # 30 lines of mixed concerns
    data = prep_result['raw_data']
    validated = validate_data(data)
    processed = process_data(validated)  
    result = call_llm_for_analysis(processed)
    formatted = format_output(result)
    return formatted

# After: Focused nodes in a flow
class ValidationNode(Node):
    def exec(self, prep_result):
        return validate_data(prep_result['raw_data'])

class ProcessingNode(Node):
    def exec(self, prep_result):
        return process_data(prep_result['validated_data'])

class AnalysisNode(Node):
    def exec(self, prep_result):
        return call_llm_for_analysis(prep_result['processed_data'])
```

### Pattern: Extract Data Access
```python
# Before: Shared store access in exec()
def exec(self, prep_result):
    user_id = self.shared['current_user_id']  # ❌ Direct access
    data = self.shared['user_data'][user_id]  # ❌ Direct access
    return process_user_data(data)

# After: Data access through prep_result
def prep(self):
    user_id = self.shared['current_user_id']
    return {
        'user_data': self.shared['user_data'][user_id]
    }

def exec(self, prep_result):
    return process_user_data(prep_result['user_data'])  # ✅ Clean
```

### Pattern: Move Business Logic to Nodes
```python
# Before: Business logic in utilities
def smart_data_processor(data, user_context, options):
    if user_context.premium:
        result = call_llm_advanced(data, options)
    else:
        result = call_llm_basic(data)
    
    if result.confidence < 0.8:
        result = call_llm_fallback(data)
    
    return result

# After: Logic in dedicated node
class SmartProcessingNode(Node):
    def exec(self, prep_result):
        data = prep_result['data']
        user_context = prep_result['user_context']
        options = prep_result['options']
        
        if user_context.premium:
            result = call_llm_advanced(data, options)
        else:
            result = call_llm_basic(data)
        
        if result.confidence < 0.8:
            result = call_llm_fallback(data)
        
        return result
```

## Success Criteria

A successful migration should achieve:

- ✅ Zero critical antipattern violations
- ✅ All tests passing
- ✅ Performance maintained or improved  
- ✅ Code is more maintainable and testable
- ✅ Clear separation of concerns
- ✅ Proper PocketFlow lifecycle usage

## Getting Help

If you encounter issues during migration:

1. Check the specific migration guide for troubleshooting tips
2. Review the [PocketFlow Best Practices](../POCKETFLOW_BEST_PRACTICES.md)
3. Run validation tools for specific guidance
4. Consult the [Common Antipatterns](../COMMON_ANTIPATTERNS.md) documentation

## Contributing

To add new migration guides:

1. Follow the template structure in each guide
2. Include realistic time estimates based on testing
3. Provide both "before" and "after" code examples
4. Test the migration steps with real code
5. Update this README with the new guide