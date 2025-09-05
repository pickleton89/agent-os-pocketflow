# Migration Guide: Fix Lifecycle Violations

**Antipattern**: Lifecycle Method Confusion  
**Severity**: 🟠 Medium  
**Time Estimate**: 1-2 hours  
**Risk Level**: Low (clear patterns to follow)

## Problem Description

PocketFlow nodes follow a strict lifecycle pattern: **prep** (gather data) → **exec** (compute) → **post** (effects). Violating this pattern makes nodes harder to test and breaks the framework's retry mechanisms.

## The PocketFlow Lifecycle

```python
# ✅ CORRECT LIFECYCLE PATTERN
class WellDesignedNode(Node):
    def prep(self):
        """ONLY data gathering - no computation or side effects"""
        return {
            'input_data': self.shared['raw_data'],
            'config': self.shared['processing_config']
        }
    
    def exec(self, prep_result):
        """ONLY pure computation - no data access or side effects"""
        return process_data(
            prep_result['input_data'], 
            prep_result['config']
        )
    
    def post(self, exec_result):
        """ONLY side effects - saving, logging, notifications"""
        self.shared['processed_data'] = exec_result
        self.shared['last_update'] = datetime.now()
        return exec_result
```

## Detecting the Problem

### Automated Detection
```bash
# Run antipattern detector
python pocketflow-tools/antipattern_detector.py your_code/

# Look for violations like:
# "Complex computation detected in prep()"
# "LLM calls should be in exec() for proper retry handling"
# "Complex computation detected in post()"
```

### Manual Inspection
Look for these patterns:

```python
# 🚨 ANTIPATTERN EXAMPLES

class BadLifecycleNode(Node):
    def prep(self):
        # ❌ COMPUTATION IN PREP - Should be in exec()
        raw_data = self.shared['raw_data']
        processed_data = complex_processing(raw_data)  # ❌ Computation
        
        # ❌ LLM CALLS IN PREP - Should be in exec()
        summary = call_llm_summarize(processed_data)  # ❌ LLM call
        
        return {
            'processed_data': processed_data,
            'summary': summary
        }
    
    def exec(self, prep_result):
        # ❌ DATA ACCESS IN EXEC - Should be in prep()
        config = self.shared['config']  # ❌ Shared store access
        
        # ❌ SIDE EFFECTS IN EXEC - Should be in post()
        self.shared['status'] = 'processing'  # ❌ State modification
        
        return format_output(prep_result['processed_data'], config)
    
    def post(self, exec_result):
        # ❌ COMPUTATION IN POST - Should be in exec()
        metrics = calculate_metrics(exec_result)  # ❌ Computation
        
        # ❌ LLM CALLS IN POST - Should be in exec()
        quality_score = call_llm_evaluate(exec_result)  # ❌ LLM call
        
        self.shared['results'] = exec_result
        self.shared['metrics'] = metrics
        return exec_result
```

## Migration Steps

### Step 1: Audit Current Node Lifecycle (15 minutes)

Create a checklist for each node:

```python
# Lifecycle audit template
NODE_AUDIT = {
    "prep()": {
        "data_access": [],      # ✅ Good - list what data is accessed
        "computation": [],      # ❌ Bad - should move to exec()
        "llm_calls": [],        # ❌ Bad - should move to exec() 
        "side_effects": [],     # ❌ Bad - should move to post()
    },
    "exec()": {
        "computation": [],      # ✅ Good - core logic
        "data_access": [],      # ❌ Bad - should be in prep()
        "side_effects": [],     # ❌ Bad - should be in post()
    },
    "post()": {
        "side_effects": [],     # ✅ Good - saving results, logging
        "computation": [],      # ❌ Bad - should be in exec()
        "llm_calls": [],        # ❌ Bad - should be in exec()
    }
}

# Example audit result:
BadNode_AUDIT = {
    "prep()": {
        "data_access": ["self.shared['raw_data']"],  # ✅ Good
        "computation": ["complex_processing()"],     # ❌ Move to exec()
        "llm_calls": ["call_llm_summarize()"],      # ❌ Move to exec()
        "side_effects": [],
    },
    "exec()": {
        "computation": ["format_output()"],          # ✅ Good
        "data_access": ["self.shared['config']"],    # ❌ Move to prep()
        "side_effects": ["self.shared['status'] = ..."], # ❌ Move to post()
    },
    "post()": {
        "side_effects": ["save results"],           # ✅ Good
        "computation": ["calculate_metrics()"],     # ❌ Move to exec()
        "llm_calls": ["call_llm_evaluate()"],      # ❌ Move to exec()
    }
}
```

### Step 2: Move Computation from prep() to exec() (30 minutes)

```python
# ❌ Before: Computation in prep()
class BadPrepNode(Node):
    def prep(self):
        raw_data = self.shared['raw_data']
        # ❌ Complex processing in prep()
        processed_data = complex_processing(raw_data)
        summary = call_llm_summarize(processed_data)
        
        return {
            'processed_data': processed_data,
            'summary': summary
        }
    
    def exec(self, prep_result):
        return prep_result['summary']  # Just returning pre-computed result

# ✅ After: Only data gathering in prep(), computation in exec()
class GoodPrepNode(Node):
    def prep(self):
        # ✅ Only gather raw data
        return {
            'raw_data': self.shared['raw_data'],
            'processing_config': self.shared.get('config', {})
        }
    
    def exec(self, prep_result):
        # ✅ Do computation in exec()
        processed_data = complex_processing(
            prep_result['raw_data'], 
            prep_result['processing_config']
        )
        summary = call_llm_summarize(processed_data)
        return summary
```

### Step 3: Move Data Access from exec() to prep() (20 minutes)

```python
# ❌ Before: Data access in exec()
class BadExecNode(Node):
    def prep(self):
        return {'input_data': self.shared['input_data']}
    
    def exec(self, prep_result):
        # ❌ Accessing shared store in exec()
        config = self.shared['config']
        multiplier = self.shared.get('multiplier', 1.0)
        
        result = process_data(prep_result['input_data'], config)
        return result * multiplier

# ✅ After: All data access in prep()
class GoodExecNode(Node):
    def prep(self):
        # ✅ Gather all data needed by exec()
        return {
            'input_data': self.shared['input_data'],
            'config': self.shared['config'],
            'multiplier': self.shared.get('multiplier', 1.0)
        }
    
    def exec(self, prep_result):
        # ✅ Pure computation using only prep_result
        result = process_data(prep_result['input_data'], prep_result['config'])
        return result * prep_result['multiplier']
```

### Step 4: Move Side Effects from exec() to post() (25 minutes)

```python
# ❌ Before: Side effects in exec()
class BadSideEffectsNode(Node):
    def exec(self, prep_result):
        # ❌ State modification in exec()
        self.shared['status'] = 'processing'
        
        result = process_data(prep_result['data'])
        
        # ❌ More side effects in exec()
        self.shared['processed_count'] += 1
        logger.info(f"Processed item {self.shared['processed_count']}")
        
        return result

# ✅ After: Side effects in post()
class GoodSideEffectsNode(Node):
    def exec(self, prep_result):
        # ✅ Pure computation - no side effects
        return process_data(prep_result['data'])
    
    def post(self, exec_result):
        # ✅ All side effects happen in post()
        self.shared['status'] = 'completed'
        self.shared['processed_count'] += 1
        self.shared['last_result'] = exec_result
        logger.info(f"Processed item {self.shared['processed_count']}")
        
        return exec_result
```

### Step 5: Move Computation from post() to exec() (20 minutes)

```python
# ❌ Before: Computation in post()
class BadPostNode(Node):
    def exec(self, prep_result):
        return process_data(prep_result['data'])
    
    def post(self, exec_result):
        # ❌ Complex computation in post()
        metrics = calculate_complex_metrics(exec_result)
        quality_score = call_llm_evaluate(exec_result)
        
        self.shared['results'] = exec_result
        self.shared['metrics'] = metrics
        self.shared['quality_score'] = quality_score
        
        return exec_result

# ✅ After: Computation in exec(), only side effects in post()
class GoodPostNode(Node):
    def exec(self, prep_result):
        result = process_data(prep_result['data'])
        
        # ✅ All computation happens in exec()
        metrics = calculate_complex_metrics(result)
        quality_score = call_llm_evaluate(result)
        
        return {
            'result': result,
            'metrics': metrics,
            'quality_score': quality_score
        }
    
    def post(self, exec_result):
        # ✅ Only side effects - saving computed results
        self.shared['results'] = exec_result['result']
        self.shared['metrics'] = exec_result['metrics']
        self.shared['quality_score'] = exec_result['quality_score']
        
        return exec_result
```

### Step 6: Handle Complex Cases (30 minutes)

#### Case A: Conditional Computation

```python
# ❌ Before: Conditional logic split across methods
class BadConditionalNode(Node):
    def prep(self):
        data = self.shared['input_data']
        # ❌ Computation in prep()
        if len(data) > 1000:
            processed = preprocess_large_data(data)  # ❌ Processing
        else:
            processed = data
            
        return {'processed': processed}
    
    def exec(self, prep_result):
        return finalize_data(prep_result['processed'])

# ✅ After: All logic in appropriate methods
class GoodConditionalNode(Node):
    def prep(self):
        # ✅ Only gather data and flags
        data = self.shared['input_data']
        return {
            'input_data': data,
            'is_large_dataset': len(data) > 1000
        }
    
    def exec(self, prep_result):
        # ✅ All computation logic in exec()
        data = prep_result['input_data']
        
        if prep_result['is_large_dataset']:
            processed = preprocess_large_data(data)
        else:
            processed = data
            
        return finalize_data(processed)
```

#### Case B: Multi-Step Computation with Intermediate Storage

```python
# ❌ Before: Computation spread across methods
class BadMultiStepNode(Node):
    def prep(self):
        raw_data = self.shared['input_data']
        # ❌ First computation step in prep()
        step1_result = processing_step_1(raw_data)
        return {'step1_result': step1_result}
    
    def exec(self, prep_result):
        # Second computation step
        step2_result = processing_step_2(prep_result['step1_result'])
        return step2_result
    
    def post(self, exec_result):
        # ❌ Third computation step in post()
        final_result = processing_step_3(exec_result)
        self.shared['result'] = final_result
        return final_result

# ✅ After: All computation in exec()
class GoodMultiStepNode(Node):
    def prep(self):
        # ✅ Only data gathering
        return {
            'input_data': self.shared['input_data'],
            'step_config': self.shared.get('processing_config', {})
        }
    
    def exec(self, prep_result):
        # ✅ All computation steps in exec()
        data = prep_result['input_data']
        config = prep_result['step_config']
        
        step1_result = processing_step_1(data, config)
        step2_result = processing_step_2(step1_result, config)
        final_result = processing_step_3(step2_result, config)
        
        return final_result
    
    def post(self, exec_result):
        # ✅ Only side effects
        self.shared['result'] = exec_result
        return exec_result
```

#### Case C: Error Handling Across Lifecycle

```python
# ❌ Before: Error handling mixed with lifecycle violations
class BadErrorHandlingNode(Node):
    def prep(self):
        try:
            data = self.shared['input_data']
            # ❌ Validation computation in prep()
            validated = validate_data(data)  
            return {'data': validated}
        except ValidationError:
            # ❌ Side effect in prep()
            self.shared['errors'].append('Validation failed')
            return {'data': None}
    
    def exec(self, prep_result):
        if prep_result['data'] is None:
            return None
        return process_data(prep_result['data'])
    
    def post(self, exec_result):
        if exec_result is None:
            # ❌ Side effect computation in post()
            error_report = generate_error_report(self.shared['errors'])
            self.shared['error_report'] = error_report
        return exec_result

# ✅ After: Proper error handling with lifecycle separation
class GoodErrorHandlingNode(Node):
    def prep(self):
        # ✅ Only data gathering, defer validation
        return {
            'input_data': self.shared['input_data'],
            'validation_rules': self.shared.get('validation_rules', {})
        }
    
    def exec(self, prep_result):
        # ✅ All processing (including validation) in exec()
        try:
            data = prep_result['input_data']
            rules = prep_result['validation_rules']
            
            validated_data = validate_data(data, rules)
            processed_data = process_data(validated_data)
            
            return {
                'success': True,
                'data': processed_data,
                'error': None
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }
    
    def post(self, exec_result):
        # ✅ Only side effects based on exec result
        if exec_result['success']:
            self.shared['processed_data'] = exec_result['data']
        else:
            error_list = self.shared.setdefault('errors', [])
            error_list.append(exec_result['error'])
            
        return exec_result
```

### Step 7: Update Tests (15 minutes)

Update tests to work with the corrected lifecycle:

```python
# ✅ Testing the corrected lifecycle
class TestGoodLifecycleNode:
    def test_prep_only_gathers_data(self):
        """Test that prep() only accesses data, no computation"""
        node = GoodLifecycleNode()
        node.shared = {
            'input_data': [1, 2, 3],
            'config': {'multiplier': 2}
        }
        
        prep_result = node.prep()
        
        # Should only contain raw data, no computed results
        assert prep_result == {
            'input_data': [1, 2, 3],
            'config': {'multiplier': 2}
        }
    
    def test_exec_is_pure_function(self):
        """Test that exec() is a pure function"""
        node = GoodLifecycleNode()
        
        prep_result = {
            'input_data': [1, 2, 3],
            'config': {'multiplier': 2}
        }
        
        # Call exec() multiple times - should get same result
        result1 = node.exec(prep_result)
        result2 = node.exec(prep_result)
        
        assert result1 == result2  # Pure function property
        assert result1 == [2, 4, 6]  # Expected computation result
    
    def test_post_handles_side_effects(self):
        """Test that post() only handles side effects"""
        node = GoodLifecycleNode()
        node.shared = {}  # Start with empty shared store
        
        exec_result = [2, 4, 6]
        returned_result = node.post(exec_result)
        
        # Should save result to shared store
        assert node.shared['processed_data'] == [2, 4, 6]
        # Should return the result unchanged
        assert returned_result == exec_result
    
    def test_full_lifecycle_integration(self):
        """Test the complete lifecycle works together"""
        node = GoodLifecycleNode()
        node.shared = {
            'input_data': [1, 2, 3],
            'config': {'multiplier': 3}
        }
        
        # Full lifecycle
        prep_result = node.prep()
        exec_result = node.exec(prep_result)
        final_result = node.post(exec_result)
        
        assert final_result == [3, 6, 9]
        assert node.shared['processed_data'] == [3, 6, 9]
```

## Common Patterns and Solutions

### Pattern: Data Validation

```python
# ✅ Validation as computation in exec()
class DataValidationNode(Node):
    def prep(self):
        return {
            'raw_data': self.shared['input_data'],
            'validation_schema': self.shared['schema'],
            'strict_mode': self.shared.get('strict_validation', False)
        }
    
    def exec(self, prep_result):
        # Validation is computation - belongs in exec()
        validator = DataValidator(prep_result['validation_schema'])
        
        try:
            validated_data = validator.validate(
                prep_result['raw_data'],
                strict=prep_result['strict_mode']
            )
            return {
                'valid': True,
                'data': validated_data,
                'errors': []
            }
        except ValidationError as e:
            return {
                'valid': False,  
                'data': None,
                'errors': e.errors
            }
```

### Pattern: Configuration Processing

```python
# ✅ Configuration processing in exec()
class ConfigurableProcessingNode(Node):
    def prep(self):
        return {
            'data': self.shared['input_data'],
            'raw_config': self.shared['processing_config']
        }
    
    def exec(self, prep_result):
        # Configuration processing is computation
        config = self._parse_config(prep_result['raw_config'])
        processor = ProcessorFactory.create(config.processor_type)
        
        return processor.process(prep_result['data'], config)
    
    def _parse_config(self, raw_config):
        """Helper method for config processing"""
        # This is still part of exec() computation
        return ProcessingConfig.from_dict(raw_config)
```

### Pattern: Multi-Modal Processing

```python
# ✅ Different processing modes in exec()
class MultiModalNode(Node):
    def prep(self):
        return {
            'data': self.shared['input_data'],
            'mode': self.shared.get('processing_mode', 'standard'),
            'llm_config': self.shared.get('llm_config', {}),
            'cache_config': self.shared.get('cache_config', {})
        }
    
    def exec(self, prep_result):
        data = prep_result['data']
        mode = prep_result['mode']
        
        if mode == 'llm':
            # LLM processing in exec()
            return call_llm_process(data, prep_result['llm_config'])
        elif mode == 'cached':
            # Cache lookup + processing in exec()  
            cached_result = self._check_cache(data, prep_result['cache_config'])
            if cached_result:
                return cached_result
            else:
                result = standard_process(data)
                self._update_cache_data(data, result, prep_result['cache_config'])
                return result
        else:
            return standard_process(data)
    
    def _check_cache(self, data, cache_config):
        """Pure function - part of exec() computation"""
        # This is computation, not a side effect
        cache_key = generate_cache_key(data, cache_config)
        return lookup_cached_result(cache_key)
    
    def _update_cache_data(self, data, result, cache_config):
        """Returns cache update instructions for post() to handle"""
        return {
            'cache_key': generate_cache_key(data, cache_config),
            'cache_data': result
        }
```

## Success Criteria

✅ **Lifecycle Compliance**
- `prep()` methods only access data from shared store
- `exec()` methods only use `prep_result` parameter
- `post()` methods only handle side effects
- No computation in `prep()` or `post()`
- No LLM calls in `prep()` or `post()`

✅ **Testing**
- `exec()` methods are pure functions - easily testable
- Tests don't need to mock shared store for `exec()` testing
- Side effects are isolated and testable in `post()` methods

✅ **Performance**
- Retry mechanism works correctly (only `exec()` is retried)
- No redundant computation in lifecycle methods
- Clear separation makes optimization easier

## Time Estimates by Complexity

| Node Complexity | Violations | Estimated Time |
|----------------|------------|----------------|
| Simple (1-2 methods) | 1-2 violations | 30-45 minutes |
| Medium (3-4 methods) | 3-5 violations | 1-1.5 hours |
| Complex (5+ methods) | 6+ violations | 1.5-2 hours |

Add time for:
- Complex conditional logic: +30 minutes
- Multiple LLM calls: +15 minutes per call
- Extensive test updates: +30 minutes

## Troubleshooting

### Issue: "exec() needs data not in prep_result"
```python
# Problem: exec() trying to access data not gathered by prep()
def exec(self, prep_result):
    config = prep_result['config']  # ❌ KeyError if not in prep()
    
# Solution: Update prep() to include all needed data
def prep(self):
    return {
        'data': self.shared['input_data'],
        'config': self.shared['config']  # ✅ Add missing data
    }
```

### Issue: "Can't move LLM call - depends on exec() result"
```python
# Problem: LLM call in post() that depends on exec() result
def post(self, exec_result):
    # This IS valid - evaluation based on exec result
    quality_score = call_llm_evaluate(exec_result)
    self.shared['quality_score'] = quality_score

# But if it's complex computation, restructure:
def exec(self, prep_result):
    result = main_processing(prep_result['data'])
    quality_score = call_llm_evaluate(result)  # Move here
    
    return {
        'result': result,
        'quality_score': quality_score
    }

def post(self, exec_result):
    self.shared['result'] = exec_result['result']
    self.shared['quality_score'] = exec_result['quality_score']
```

## Related Guides

- [Remove Shared Store from exec()](remove-shared-store-exec.md) - Often needed together
- [Monolithic to Focused Nodes](monolithic-to-focused.md) - For overly complex nodes
- [Move Logic from Utils to Nodes](utils-to-nodes.md) - For proper responsibility placement