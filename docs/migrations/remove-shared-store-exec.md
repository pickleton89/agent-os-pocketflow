# Migration Guide: Remove Shared Store from exec()

**Antipattern**: Shared Store Access in exec()  
**Severity**: 🔴 Critical  
**Time Estimate**: 30-60 minutes  
**Risk Level**: Low (mechanical refactoring)

## Problem Description

Accessing the shared store directly in `exec()` methods breaks PocketFlow's retry mechanism and makes nodes harder to test. The framework expects `exec()` methods to be pure functions that only use their `prep_result` parameter.

## Detecting the Problem

### Automated Detection
```bash
# Run antipattern detector
python pocketflow-tools/antipattern_detector.py your_code/

# Look for violations like:
# "Direct SharedStore access detected: self.shared['key']"
# "Direct SharedStore access detected: self.shared.attribute"
```

### Manual Inspection
Look for these patterns in `exec()` methods:

```python
# 🚨 ANTIPATTERN EXAMPLES
class BadNode(Node):
    def exec(self, prep_result):
        # ❌ Direct shared store access
        user_id = self.shared['current_user']
        settings = self.shared['user_settings'][user_id]
        data = self.shared.get('cached_data', {})
        
        return process_user_data(data, settings)

    def exec_another_bad_example(self, prep_result):
        # ❌ Conditional shared store access  
        if self.shared['debug_mode']:
            return self.shared['debug_result']
        
        # ❌ Shared store modification in exec
        self.shared['last_processed'] = datetime.now()
        return normal_processing()
```

## Migration Steps

### Step 1: Identify Shared Store Access (5 minutes)

Find all `self.shared` usage in your `exec()` methods:

```bash
# Search for shared store access in exec methods
grep -n "self\.shared" your_nodes.py

# Or use a more specific search
grep -A 5 -B 5 "def exec" your_nodes.py | grep -C 3 "self\.shared"
```

Document what data is being accessed:
```python
# Example audit:
# Line 45: user_id = self.shared['current_user'] 
# Line 46: settings = self.shared['user_settings'][user_id]
# Line 52: if self.shared['debug_mode']:
# Line 55: self.shared['last_processed'] = datetime.now()  # ❌ Modification!
```

### Step 2: Move Data Access to prep() (15 minutes)

Move all data reading from `exec()` to `prep()`:

```python
# ✅ CORRECTED VERSION
class GoodNode(Node):
    def prep(self):
        """Gather all data needed by exec()"""
        user_id = self.shared['current_user']
        settings = self.shared['user_settings'][user_id]
        cached_data = self.shared.get('cached_data', {})
        debug_mode = self.shared.get('debug_mode', False)
        
        return {
            'user_id': user_id,
            'settings': settings, 
            'cached_data': cached_data,
            'debug_mode': debug_mode
        }
    
    def exec(self, prep_result):
        """Pure function using only prep_result"""
        if prep_result['debug_mode']:
            # Return debug data from prep_result instead of shared store
            return prep_result.get('debug_result', 'Debug mode active')
        
        return process_user_data(
            prep_result['cached_data'],
            prep_result['settings']
        )
    
    def post(self, exec_result):
        """Handle side effects after exec() completes"""
        # ✅ State modifications go in post()
        self.shared['last_processed'] = datetime.now()
        return exec_result
```

### Step 3: Handle Complex Cases (20 minutes)

#### Case A: Conditional Data Access

```python
# ❌ Before: Conditional access in exec()
class BadConditionalNode(Node):
    def exec(self, prep_result):
        if prep_result['use_cache']:
            # ❌ Conditional shared store access
            data = self.shared['cache'][prep_result['cache_key']]
        else:
            data = fetch_fresh_data(prep_result['query'])
        return process_data(data)

# ✅ After: All access in prep()  
class GoodConditionalNode(Node):
    def prep(self):
        base_data = {'query': self.shared['query']}
        
        # Always fetch both options in prep()
        if self.shared.get('use_cache', False):
            cache_key = self.shared.get('cache_key')
            base_data.update({
                'use_cache': True,
                'cached_data': self.shared['cache'].get(cache_key),
                'cache_key': cache_key
            })
        else:
            base_data['use_cache'] = False
            
        return base_data
    
    def exec(self, prep_result):
        if prep_result['use_cache'] and prep_result['cached_data']:
            data = prep_result['cached_data']
        else:
            data = fetch_fresh_data(prep_result['query'])
        return process_data(data)
```

#### Case B: Dynamic Key Access

```python  
# ❌ Before: Dynamic key construction in exec()
class BadDynamicNode(Node):
    def exec(self, prep_result):
        user_type = prep_result['user_type']
        # ❌ Dynamic key construction using shared store
        settings_key = f"{user_type}_settings"
        settings = self.shared[settings_key]  
        return apply_settings(prep_result['data'], settings)

# ✅ After: Pre-compute all possible keys in prep()
class GoodDynamicNode(Node):
    def prep(self):
        user_type = self.shared['user_type']
        settings_key = f"{user_type}_settings"
        
        return {
            'user_type': user_type,
            'settings': self.shared[settings_key],
            'data': self.shared['input_data']
        }
    
    def exec(self, prep_result):
        return apply_settings(
            prep_result['data'], 
            prep_result['settings']
        )
```

#### Case C: Shared Store Modifications

```python
# ❌ Before: Modifying shared store in exec()
class BadModifyingNode(Node):
    def exec(self, prep_result):
        result = process_data(prep_result['data'])
        
        # ❌ Shared store modification in exec()
        self.shared['results_cache'][prep_result['key']] = result
        self.shared['last_update'] = datetime.now()
        
        return result

# ✅ After: Modifications in post()
class GoodModifyingNode(Node):
    def exec(self, prep_result):
        # Pure function - no side effects
        return process_data(prep_result['data'])
    
    def post(self, exec_result):
        # ✅ All modifications happen in post()
        cache_key = self.shared['current_key']
        self.shared['results_cache'][cache_key] = exec_result
        self.shared['last_update'] = datetime.now()
        return exec_result
```

### Step 4: Update Tests (10 minutes)

Modify tests to work with the new pattern:

```python
# ✅ Updated tests for clean separation
class TestGoodNode:
    def test_exec_with_debug_mode(self):
        node = GoodNode()
        
        # Test exec() as pure function
        prep_result = {
            'user_id': 'user123',
            'settings': {'theme': 'dark'},
            'cached_data': {'key': 'value'},
            'debug_mode': True
        }
        
        result = node.exec(prep_result)
        assert result == 'Debug mode active'
    
    def test_exec_normal_processing(self):
        node = GoodNode()
        
        prep_result = {
            'user_id': 'user123', 
            'settings': {'theme': 'dark'},
            'cached_data': {'key': 'value'},
            'debug_mode': False
        }
        
        with patch('your_module.process_user_data', return_value='processed'):
            result = node.exec(prep_result)
            assert result == 'processed'
    
    def test_prep_gathers_required_data(self):
        node = GoodNode()
        
        # Mock shared store
        node.shared = {
            'current_user': 'user123',
            'user_settings': {'user123': {'theme': 'light'}},
            'cached_data': {'some': 'data'},
            'debug_mode': False
        }
        
        prep_result = node.prep()
        
        assert prep_result['user_id'] == 'user123'
        assert prep_result['settings'] == {'theme': 'light'}
        assert prep_result['cached_data'] == {'some': 'data'}
        assert prep_result['debug_mode'] is False
```

### Step 5: Validate Changes (5 minutes)

```bash
# Run antipattern detector to confirm fix
python pocketflow-tools/antipattern_detector.py your_code/

# Should show zero "Shared Store Access in exec()" violations

# Run your tests
python -m pytest tests/test_your_nodes.py -v

# Run integration tests if available
python -m pytest tests/integration/ -v
```

## Common Patterns and Solutions

### Pattern: Error Handling with Shared Store

```python
# ❌ Before: Error handling with shared store access
class BadErrorHandling(Node):
    def exec(self, prep_result):
        try:
            return process_data(prep_result['data'])
        except Exception as e:
            # ❌ Accessing shared store in error handler
            if self.shared['fail_fast_mode']:
                raise
            else:
                return self.shared['default_response']

# ✅ After: Error handling data from prep_result  
class GoodErrorHandling(Node):
    def prep(self):
        return {
            'data': self.shared['input_data'],
            'fail_fast_mode': self.shared.get('fail_fast_mode', False),
            'default_response': self.shared.get('default_response', None)
        }
    
    def exec(self, prep_result):
        try:
            return process_data(prep_result['data'])
        except Exception as e:
            if prep_result['fail_fast_mode']:
                raise
            else:
                return prep_result['default_response']
```

### Pattern: Logging with Context

```python
# ❌ Before: Logging with shared store access
class BadLogging(Node):
    def exec(self, prep_result):
        try:
            result = process_data(prep_result['data'])
            # ❌ Shared store access for logging
            logger.info(f"User {self.shared['current_user']} processed {len(result)} items")
            return result
        except Exception as e:
            logger.error(f"Processing failed for user {self.shared['current_user']}: {e}")
            raise

# ✅ After: Logging context from prep_result
class GoodLogging(Node):
    def prep(self):
        return {
            'data': self.shared['input_data'],
            'current_user': self.shared.get('current_user', 'unknown')
        }
    
    def exec(self, prep_result):
        try:
            result = process_data(prep_result['data'])
            logger.info(f"User {prep_result['current_user']} processed {len(result)} items")
            return result
        except Exception as e:
            logger.error(f"Processing failed for user {prep_result['current_user']}: {e}")
            raise
```

### Pattern: Configuration Access

```python
# ❌ Before: Configuration access in exec()
class BadConfig(Node):
    def exec(self, prep_result):
        # ❌ Config access in exec()
        max_retries = self.shared['config']['max_retries']
        timeout = self.shared['config']['timeout']
        
        return process_with_config(prep_result['data'], max_retries, timeout)

# ✅ After: Config in prep_result
class GoodConfig(Node):
    def prep(self):
        config = self.shared.get('config', {})
        return {
            'data': self.shared['input_data'],
            'max_retries': config.get('max_retries', 3),
            'timeout': config.get('timeout', 30)
        }
    
    def exec(self, prep_result):
        return process_with_config(
            prep_result['data'],
            prep_result['max_retries'],
            prep_result['timeout']
        )
```

## Risk Mitigation

### Performance Considerations

**Issue**: Prep() might fetch too much data
```python
# Problem: Over-fetching in prep()
def prep(self):
    return {
        'small_data': self.shared['small_item'],
        'huge_data': self.shared['massive_dataset'],  # ❌ Always fetched
        'condition': self.shared['use_huge_data']
    }

# Solution: Conditional data fetching
def prep(self):
    base_data = {
        'small_data': self.shared['small_item'],
        'condition': self.shared['use_huge_data']
    }
    
    if self.shared['use_huge_data']:
        base_data['huge_data'] = self.shared['massive_dataset']
    
    return base_data
```

### Memory Considerations

**Issue**: Prep_result becomes too large
```python
# Monitor prep_result size
import sys

def prep(self):
    prep_result = {
        # ... your data
    }
    
    # Check size
    size_mb = sys.getsizeof(prep_result) / (1024 * 1024)
    if size_mb > 10:  # Warning for >10MB
        logger.warning(f"Large prep_result: {size_mb:.2f}MB")
    
    return prep_result
```

### Testing Considerations

**Issue**: Tests need to provide more mock data
```python
# Helper function to create comprehensive prep_result for tests
def create_test_prep_result(**overrides):
    """Create a standard prep_result for testing"""
    defaults = {
        'user_id': 'test_user',
        'settings': {'theme': 'light'},
        'config': {'timeout': 30},
        'debug_mode': False
    }
    defaults.update(overrides)
    return defaults

# Use in tests
def test_node_behavior(self):
    node = YourNode()
    prep_result = create_test_prep_result(debug_mode=True)
    result = node.exec(prep_result)
    # ... assertions
```

## Success Criteria

✅ **Code Quality**
- Zero `self.shared` access in any `exec()` method
- All data access moved to `prep()` methods
- All side effects moved to `post()` methods  
- Pure functions in `exec()` methods

✅ **Testing**
- `exec()` methods are easily testable with mock prep_result
- No need to mock shared store for `exec()` tests
- Tests run faster due to isolated functions

✅ **Framework Compatibility**
- Retry mechanism works correctly
- Nodes can be composed and reused easily
- Clear separation of concerns

## Troubleshooting

### Common Issues

**Issue**: "Missing key in prep_result"
```python
# Problem: prep_result key doesn't match exec() expectation
def prep(self):
    return {'user_data': self.shared['user_info']}  # ❌ Wrong key name

def exec(self, prep_result):
    return prep_result['user_info']  # ❌ KeyError

# Solution: Consistent naming
def prep(self):
    return {'user_info': self.shared['user_info']}  # ✅ Matches
```

**Issue**: "prep() called multiple times"
```python
# This is normal PocketFlow behavior - prep() may be called multiple times
# Ensure prep() is idempotent and doesn't have side effects

# ❌ Bad: Side effects in prep()
def prep(self):
    self.shared['prep_count'] += 1  # ❌ Side effect
    return {'data': self.shared['input_data']}

# ✅ Good: Pure data gathering
def prep(self):
    return {'data': self.shared['input_data']}  # ✅ Pure function
```

**Issue**: "Complex data structures in prep_result"
```python
# Keep prep_result simple and JSON-serializable when possible
def prep(self):
    return {
        # ✅ Simple types
        'count': 42,
        'name': 'example',
        'is_enabled': True,
        'items': ['a', 'b', 'c'],
        
        # ❌ Avoid complex objects when possible
        'database_connection': db_conn,  # Hard to test/serialize
        'file_handle': open('file.txt'), # Resource leak risk
    }
```

## Related Guides

- [Fix Lifecycle Violations](fix-lifecycle-violations.md) - For other lifecycle method issues
- [Monolithic to Focused Nodes](monolithic-to-focused.md) - If nodes are doing too much
- [Move Logic from Utils to Nodes](utils-to-nodes.md) - For business logic placement