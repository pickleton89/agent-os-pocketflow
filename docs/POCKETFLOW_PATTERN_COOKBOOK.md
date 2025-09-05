# PocketFlow Pattern Cookbook

> Quick-reference recipes for common PocketFlow scenarios  
> Version: 1.0.0  
> Date: 2025-09-05  

## Table of Contents

1. [Quick Pattern Selector](#quick-pattern-selector)
2. [File & Data Processing Recipes](#file--data-processing-recipes)
3. [API Integration Recipes](#api-integration-recipes)
4. [Content Generation Recipes](#content-generation-recipes)
5. [Batch Processing Recipes](#batch-processing-recipes)
6. [Error Handling Recipes](#error-handling-recipes)
7. [Performance Optimization Recipes](#performance-optimization-recipes)
8. [Testing Recipes](#testing-recipes)

## Framework Context

🎯 **Framework vs Usage Statement**: This repository IS the Agent OS + PocketFlow framework itself - NOT a project using it.

**This cookbook provides recipes for END-USER projects** where PocketFlow is installed as a dependency and these patterns become working implementations.

⚠️ **IMPORTANT**: All code examples in this cookbook are for END-USER projects, not for this framework repository. In end-user projects:
- `from pocketflow import Node, AsyncNode, SharedStore` - PocketFlow is installed as a dependency
- Placeholder functions (like `process_content_async()`, `call_llm_async()`) need actual implementations
- All imports must be added to your project's requirements
- Flow connections and node classes need to be defined in your project

## Quick Pattern Selector

### "I need to..."

| Scenario | Use This Recipe |
|----------|----------------|
| Process multiple files/documents | [Multiple Files](#recipe-processing-multiple-files) |
| Call external APIs with retries | [API with Retries](#recipe-api-with-retries) |
| Generate content with validation | [Content + Validation](#recipe-content-with-validation) |
| Transform data formats | [Data Transformation](#recipe-data-transformation) |
| Analyze text with LLM | [Content + Validation](#recipe-content-with-validation) |
| Handle user input safely | [Input Sanitization](#recipe-input-sanitization) |
| Cache expensive operations | [Result Caching](#recipe-result-caching) |
| Run parallel processing | [Parallel Processing](#recipe-parallel-processing) |
| Coordinate multiple agents | [Multi-Agent](#recipe-multi-agent-coordination) |
| Build RAG system | [RAG Pipeline](#recipe-rag-pipeline) |

---

## File & Data Processing Recipes

### Recipe: Processing Multiple Files

**When to Use**: Operating on file collections, need parallel processing, results aggregation required

**Node Pattern**: `AsyncParallelBatchNode`

```python
# Required imports for end-user projects
import aiofiles
import asyncio
from typing import Dict, List, Optional, Any
from pocketflow import AsyncParallelBatchNode, SharedStore

# Placeholder function - implement in your project
async def process_content_async(content: str) -> Any:
    """Implement your content processing logic here."""
    # Example: return analyzed_content
    pass

class FileProcessor(AsyncParallelBatchNode):
    async def prep_async(self, shared: SharedStore) -> List[str]:
        """Validate and prepare file list."""
        file_paths = shared.get('file_paths', [])
        if not file_paths:
            raise ValueError("No files provided")
        return file_paths
    
    async def exec_async(self, file_path: str) -> Dict[str, Any]:
        """Process a single file asynchronously."""
        try:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
            
            # Your processing logic here
            result = await process_content_async(content)
            
            return {
                'file_path': file_path,
                'status': 'success',
                'result': result,
                'size': len(content)
            }
        except Exception as e:
            return {
                'file_path': file_path,
                'status': 'error',
                'error': str(e)
            }
    
    async def post_async(self, shared: SharedStore, prep_result, exec_results) -> Optional[str]:
        """Aggregate results and route based on success rate."""
        successful = [r for r in exec_results if r['status'] == 'success']
        failed = [r for r in exec_results if r['status'] == 'error']
        
        shared['processed_files'] = successful
        shared['failed_files'] = failed
        shared['processing_stats'] = {
            'total': len(exec_results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': len(successful) / len(exec_results) if exec_results else 0
        }
        
        # Route based on success rate
        if len(failed) == 0:
            return None  # Complete success
        elif len(successful) == 0:
            return "complete_failure"
        else:
            return "partial_success"

# Usage in flow - Define these nodes in your project:
# 
# class ProcessingCompleteNode(Node): ...
# class ProcessingFailedNode(Node): ...  
# class PartialSuccessNode(Node): ...

file_processor = FileProcessor()
# success_handler = ProcessingCompleteNode()
# failure_handler = ProcessingFailedNode()
# partial_handler = PartialSuccessNode()

# file_processor >> success_handler
# file_processor - "complete_failure" >> failure_handler  
# file_processor - "partial_success" >> partial_handler
```

**Common Mistakes**:
- Using regular `Node` with `for` loop (blocks processing)
- Processing files sequentially instead of in parallel
- Not handling individual file failures gracefully

---

### Recipe: Data Transformation

**When to Use**: Converting between data formats, applying business rules, data cleaning

**Node Pattern**: `Node` (synchronous data transformation)

```python
# Required imports for end-user projects
from typing import Dict, List, Optional, Any
from pocketflow import Node, SharedStore

class DataTransformer(Node):
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Load and validate input data."""
        raw_data = shared.get('raw_data')
        if not raw_data:
            raise ValueError("No raw_data provided")
        
        transform_rules = shared.get('transform_rules', {})
        return {
            'data': raw_data,
            'rules': transform_rules
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply transformation rules to data."""
        data = prep_result['data']
        rules = prep_result['rules']
        
        if isinstance(data, list):
            transformed = [self._transform_item(item, rules) for item in data]
        else:
            transformed = self._transform_item(data, rules)
        
        return {
            'transformed_data': transformed,
            'original_count': len(data) if isinstance(data, list) else 1,
            'transform_stats': self._get_stats(data, transformed)
        }
    
    def post(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        """Store transformed data and validate results."""
        shared['transformed_data'] = exec_result['transformed_data']
        shared['transform_stats'] = exec_result['transform_stats']
        
        # Validate transformation quality
        if exec_result['transform_stats']['success_rate'] < 0.9:
            return "transformation_issues"
        
        return None
    
    def _transform_item(self, item: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a single data item."""
        result = {}
        
        # Apply field mappings
        for source_field, target_field in rules.get('field_mapping', {}).items():
            if source_field in item:
                result[target_field] = item[source_field]
        
        # Apply data type conversions
        for field, target_type in rules.get('type_conversions', {}).items():
            if field in result:
                result[field] = self._convert_type(result[field], target_type)
        
        # Apply business rules
        result = self._apply_business_rules(result, rules.get('business_rules', {}))
        
        return result
```

---

## API Integration Recipes

### Recipe: API with Retries

**When to Use**: Calling external APIs, need resilience against network issues, rate limiting

**Node Pattern**: `AsyncNode` with retry logic

```python
# Required imports for end-user projects
import aiohttp
import asyncio
from typing import Optional, Dict, Any
from pocketflow import AsyncNode, SharedStore

class APICallWithRetries(AsyncNode):
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def prep_async(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare API request parameters."""
        endpoint = shared.get('api_endpoint')
        if not endpoint:
            raise ValueError("api_endpoint is required")
        
        return {
            'endpoint': endpoint,
            'method': shared.get('http_method', 'GET'),
            'headers': shared.get('headers', {}),
            'payload': shared.get('payload'),
            'timeout': shared.get('timeout', 30)
        }
    
    async def exec_async(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Make API call with exponential backoff retry."""
        
        for attempt in range(self.max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method=prep_result['method'],
                        url=prep_result['endpoint'],
                        headers=prep_result['headers'],
                        json=prep_result['payload'],
                        timeout=aiohttp.ClientTimeout(total=prep_result['timeout'])
                    ) as response:
                        
                        result_data = {
                            'status_code': response.status,
                            'headers': dict(response.headers),
                            'data': await response.json() if response.content_type == 'application/json' else await response.text(),
                            'attempt': attempt + 1,
                            'success': True
                        }
                        
                        if response.status >= 400:
                            if response.status == 429:  # Rate limited
                                if attempt < self.max_retries:
                                    delay = self.base_delay * (2 ** attempt)
                                    await asyncio.sleep(delay)
                                    continue
                            
                            result_data['success'] = False
                            result_data['error'] = f"HTTP {response.status}: {await response.text()}"
                        
                        return result_data
                        
            except asyncio.TimeoutError:
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
                    continue
                return {
                    'success': False,
                    'error': 'Request timeout after all retries',
                    'attempt': attempt + 1
                }
            except Exception as e:
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
                    continue
                return {
                    'success': False,
                    'error': str(e),
                    'attempt': attempt + 1
                }
        
        return {
            'success': False,
            'error': 'All retry attempts failed',
            'attempt': self.max_retries + 1
        }
    
    async def post_async(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        """Store API response and route based on success."""
        shared['api_response'] = exec_result
        
        if exec_result['success']:
            shared['api_data'] = exec_result['data']
            return None  # Success path
        else:
            shared['api_error'] = exec_result['error']
            
            # Check if it's a retryable error
            if 'timeout' in exec_result['error'].lower():
                return "timeout_error"
            elif 'rate limit' in exec_result['error'].lower():
                return "rate_limited"
            else:
                return "api_error"

# Usage in flow - Define these nodes in your project:
#
# class ProcessAPIDataNode(Node): ...
# class HandleTimeoutNode(Node): ...
# class HandleRateLimitNode(Node): ...
# class HandleAPIErrorNode(Node): ...

api_call = APICallWithRetries(max_retries=3)
# success_processor = ProcessAPIDataNode()
# timeout_handler = HandleTimeoutNode()
# rate_limit_handler = HandleRateLimitNode()
# error_handler = HandleAPIErrorNode()

# api_call >> success_processor
# api_call - "timeout_error" >> timeout_handler
# api_call - "rate_limited" >> rate_limit_handler
# api_call - "api_error" >> error_handler
```

---

## Content Generation Recipes

### Recipe: Content with Validation

**When to Use**: Generating content with LLMs, need quality assurance, structured output validation

**Node Pattern**: Chain of `AsyncNode` + `Node`

```python
# Required imports for end-user projects  
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from pocketflow import AsyncNode, Node, SharedStore

# Placeholder function - implement in your project
async def call_llm_async(prompt: str, **kwargs) -> str:
    \"\"\"Implement your LLM API call here.\"\"\"\n    # Example: return await openai_client.generate(prompt=prompt, **kwargs)
    pass

class ContentGenerator(AsyncNode):
    async def prep_async(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare content generation parameters."""
        prompt_template = shared.get('prompt_template')
        context_data = shared.get('context_data', {})
        
        if not prompt_template:
            raise ValueError("prompt_template is required")
        
        # Build final prompt from template
        final_prompt = prompt_template.format(**context_data)
        
        return {
            'prompt': final_prompt,
            'model_params': shared.get('model_params', {}),
            'max_retries': shared.get('max_retries', 2)
        }
    
    async def exec_async(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content using LLM."""
        prompt = prep_result['prompt']
        model_params = prep_result['model_params']
        
        # Your LLM call here
        response = await call_llm_async(
            prompt=prompt,
            **model_params
        )
        
        return {
            'raw_content': response,
            'prompt_used': prompt,
            'generation_params': model_params,
            'word_count': len(response.split()),
            'char_count': len(response)
        }
    
    async def post_async(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        """Store generated content for validation."""
        shared['generated_content'] = exec_result['raw_content']
        shared['generation_metadata'] = {
            'word_count': exec_result['word_count'],
            'char_count': exec_result['char_count'],
            'prompt': exec_result['prompt_used']
        }
        return None

class ContentValidator(Node):
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Load content and validation rules."""
        content = shared.get('generated_content')
        validation_rules = shared.get('validation_rules', {})
        
        if not content:
            raise ValueError("No generated content to validate")
        
        return {
            'content': content,
            'rules': validation_rules
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated content against rules."""
        content = prep_result['content']
        rules = prep_result['rules']
        
        validation_results = {}
        
        # Check length requirements
        if 'min_length' in rules:
            validation_results['min_length_met'] = len(content) >= rules['min_length']
        if 'max_length' in rules:
            validation_results['max_length_met'] = len(content) <= rules['max_length']
        
        # Check required keywords
        if 'required_keywords' in rules:
            validation_results['keywords_present'] = all(
                keyword.lower() in content.lower() 
                for keyword in rules['required_keywords']
            )
        
        # Check forbidden patterns
        if 'forbidden_patterns' in rules:
            validation_results['no_forbidden_patterns'] = all(
                pattern.lower() not in content.lower() 
                for pattern in rules['forbidden_patterns']
            )
        
        # Check format requirements (JSON, XML, etc.)
        if 'format_type' in rules:
            validation_results['format_valid'] = self._validate_format(
                content, rules['format_type']
            )
        
        # Overall validation score
        all_checks = list(validation_results.values())
        validation_score = sum(all_checks) / len(all_checks) if all_checks else 0
        
        return {
            'validation_results': validation_results,
            'validation_score': validation_score,
            'is_valid': validation_score >= rules.get('min_score', 0.8),
            'checked_content': content
        }
    
    def post(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        """Route based on validation results."""
        shared['validation_results'] = exec_result['validation_results']
        shared['validation_score'] = exec_result['validation_score']
        
        if exec_result['is_valid']:
            shared['final_content'] = exec_result['checked_content']
            return None  # Valid content
        else:
            return "validation_failed"
    
    def _validate_format(self, content: str, format_type: str) -> bool:
        """Validate content format."""
        if format_type.lower() == 'json':
            try:
                json.loads(content)
                return True
            except:
                return False
        elif format_type.lower() == 'xml':
            try:
                ET.fromstring(content)
                return True
            except:
                return False
        return True  # Unknown format, assume valid

# Usage in flow
generator = ContentGenerator()
validator = ContentValidator()
content_approved = ContentApprovedNode()
regenerate = RegenerateContentNode()

generator >> validator >> content_approved
validator - "validation_failed" >> regenerate >> generator  # Retry loop
```

---

## Batch Processing Recipes

### Recipe: Parallel Processing

**When to Use**: CPU-intensive operations, independent tasks, need maximum throughput

**Node Pattern**: `AsyncParallelBatchNode`

```python
# Required imports for end-user projects
import time
from typing import Dict, List, Optional, Any
from pocketflow import AsyncParallelBatchNode, SharedStore

# Placeholder function - implement in your project  
async def process_single_task_async(task_data: Any) -> Any:
    \"\"\"Implement your task processing logic here.\"\"\"\n    # Example: return await heavy_computation(task_data)
    pass

class ParallelProcessor(AsyncParallelBatchNode):
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
    
    async def prep_async(self, shared: SharedStore) -> List[Dict[str, Any]]:
        """Prepare tasks for parallel processing."""
        tasks = shared.get('processing_tasks', [])
        if not tasks:
            raise ValueError("No processing_tasks provided")
        
        # Add metadata to each task
        return [
            {
                'task_id': i,
                'data': task,
                'created_at': time.time()
            }
            for i, task in enumerate(tasks)
        ]
    
    async def exec_async(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single task."""
        start_time = time.time()
        
        try:
            # Your processing logic here
            result = await process_single_task_async(task_data['data'])
            
            return {
                'task_id': task_data['task_id'],
                'status': 'success',
                'result': result,
                'processing_time': time.time() - start_time,
                'created_at': task_data['created_at']
            }
            
        except Exception as e:
            return {
                'task_id': task_data['task_id'],
                'status': 'error',
                'error': str(e),
                'processing_time': time.time() - start_time,
                'created_at': task_data['created_at']
            }
    
    async def post_async(self, shared: SharedStore, prep_result, exec_results) -> Optional[str]:
        """Aggregate parallel processing results."""
        successful = [r for r in exec_results if r['status'] == 'success']
        failed = [r for r in exec_results if r['status'] == 'error']
        
        # Calculate performance metrics
        processing_times = [r['processing_time'] for r in exec_results]
        total_time = time.time() - min(r['created_at'] for r in exec_results)
        
        shared['results'] = successful
        shared['failed_tasks'] = failed
        shared['performance_metrics'] = {
            'total_tasks': len(exec_results),
            'successful_tasks': len(successful),
            'failed_tasks': len(failed),
            'success_rate': len(successful) / len(exec_results) if exec_results else 0,
            'avg_processing_time': sum(processing_times) / len(processing_times),
            'max_processing_time': max(processing_times),
            'min_processing_time': min(processing_times),
            'total_elapsed_time': total_time,
            'tasks_per_second': len(exec_results) / total_time
        }
        
        # Route based on results
        if len(failed) == 0:
            return None  # All successful
        elif len(successful) == 0:
            return "all_failed"
        else:
            return "partial_success"

# Usage with concurrency control
processor = ParallelProcessor(max_concurrent=5)
all_success = AllTasksCompleteNode()
partial_success = PartialSuccessNode()
all_failed = AllTasksFailedNode()

processor >> all_success
processor - "partial_success" >> partial_success
processor - "all_failed" >> all_failed
```

---

## Error Handling Recipes

### Recipe: Input Sanitization

**When to Use**: Processing user input, need security validation, data cleaning

**Node Pattern**: `Node` with comprehensive validation

```python
# Required imports for end-user projects
import re
import html
from typing import Any, Dict, List, Optional
from pocketflow import Node, SharedStore

class InputSanitizer(Node):
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Load input data and validation rules."""
        user_input = shared.get('user_input')
        if user_input is None:
            raise ValueError("user_input is required")
        
        validation_schema = shared.get('validation_schema', {})
        return {
            'input': user_input,
            'schema': validation_schema
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize and validate input data."""
        user_input = prep_result['input']
        schema = prep_result['schema']
        
        sanitized_data = {}
        validation_errors = []
        security_issues = []
        
        # Handle different input types
        if isinstance(user_input, dict):
            sanitized_data, errors, security = self._sanitize_dict(user_input, schema)
        elif isinstance(user_input, str):
            sanitized_data, errors, security = self._sanitize_string(user_input, schema)
        elif isinstance(user_input, list):
            sanitized_data, errors, security = self._sanitize_list(user_input, schema)
        else:
            validation_errors.append(f"Unsupported input type: {type(user_input)}")
            sanitized_data = None
        
        validation_errors.extend(errors)
        security_issues.extend(security)
        
        return {
            'sanitized_data': sanitized_data,
            'validation_errors': validation_errors,
            'security_issues': security_issues,
            'is_safe': len(security_issues) == 0,
            'is_valid': len(validation_errors) == 0,
            'original_input': user_input
        }
    
    def post(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        """Route based on validation results."""
        shared['sanitized_input'] = exec_result['sanitized_data']
        shared['input_validation'] = {
            'errors': exec_result['validation_errors'],
            'security_issues': exec_result['security_issues'],
            'is_safe': exec_result['is_safe'],
            'is_valid': exec_result['is_valid']
        }
        
        if not exec_result['is_safe']:
            return "security_threat"
        elif not exec_result['is_valid']:
            return "invalid_input"
        
        return None  # Input is clean and valid
    
    def _sanitize_string(self, input_str: str, schema: Dict[str, Any]) -> tuple:
        """Sanitize string input."""
        errors = []
        security_issues = []
        sanitized = input_str.strip()
        
        # Check for security threats
        security_patterns = [
            r'<script.*?>.*?</script>',  # XSS
            r'javascript:',              # JavaScript URLs
            r'on\w+\s*=',               # Event handlers
            r'(union\s+select|drop\s+table|delete\s+from)',  # SQL injection
            r'\.\./',                   # Path traversal
            r'<\s*iframe.*?>',         # Iframe injection
        ]
        
        for pattern in security_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                security_issues.append(f"Detected potential security threat: {pattern}")
        
        # Apply length limits
        max_length = schema.get('max_length', 10000)
        if len(sanitized) > max_length:
            if self.strict_mode:
                errors.append(f"String too long: {len(sanitized)} > {max_length}")
            else:
                sanitized = sanitized[:max_length]
        
        # Check required patterns
        if 'pattern' in schema:
            if not re.match(schema['pattern'], sanitized):
                errors.append(f"String doesn't match required pattern: {schema['pattern']}")
        
        # Remove or escape HTML
        if schema.get('allow_html', False):
            sanitized = self._escape_html(sanitized)
        else:
            sanitized = self._strip_html(sanitized)
        
        return sanitized, errors, security_issues
    
    def _sanitize_dict(self, input_dict: Dict[str, Any], schema: Dict[str, Any]) -> tuple:
        """Sanitize dictionary input."""
        errors = []
        security_issues = []
        sanitized = {}
        
        # Check required fields
        required_fields = schema.get('required_fields', [])
        for field in required_fields:
            if field not in input_dict:
                errors.append(f"Missing required field: {field}")
        
        # Check allowed fields
        allowed_fields = schema.get('allowed_fields')
        if allowed_fields:
            for field in input_dict:
                if field not in allowed_fields:
                    errors.append(f"Field not allowed: {field}")
                    continue
        
        # Sanitize each field
        field_schemas = schema.get('field_schemas', {})
        for field, value in input_dict.items():
            if allowed_fields and field not in allowed_fields:
                continue
            
            field_schema = field_schemas.get(field, {})
            
            if isinstance(value, str):
                sanitized_value, field_errors, field_security = self._sanitize_string(value, field_schema)
                sanitized[field] = sanitized_value
                errors.extend([f"{field}: {e}" for e in field_errors])
                security_issues.extend([f"{field}: {s}" for s in field_security])
            else:
                sanitized[field] = value
        
        return sanitized, errors, security_issues
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML characters."""
        import html
        return html.escape(text)
    
    def _strip_html(self, text: str) -> str:
        """Remove HTML tags."""
        return re.sub(r'<[^>]+>', '', text)

# Usage in flow
sanitizer = InputSanitizer(strict_mode=True)
process_clean_input = ProcessCleanInputNode()
handle_security_threat = SecurityThreatNode()
handle_invalid_input = InvalidInputNode()

sanitizer >> process_clean_input
sanitizer - "security_threat" >> handle_security_threat
sanitizer - "invalid_input" >> handle_invalid_input
```

---

## Performance Optimization Recipes

### Recipe: Result Caching

**When to Use**: Expensive operations, repeated computations, need to avoid redundant work

**Node Pattern**: `Node` with caching layer

```python
# Required imports for end-user projects
import hashlib
import json
import time
from typing import Any, Dict, Optional
from pocketflow import Node, SharedStore

class CachedProcessor(Node):
    def __init__(self, cache_ttl: int = 3600, max_cache_size: int = 1000):
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = cache_ttl
        self.max_cache_size = max_cache_size
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare data and generate cache key."""
        processing_data = shared.get('processing_data')
        if not processing_data:
            raise ValueError("processing_data is required")
        
        # Generate cache key based on input data
        cache_key = self._generate_cache_key(processing_data)
        
        return {
            'data': processing_data,
            'cache_key': cache_key,
            'processing_params': shared.get('processing_params', {})
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process data with caching."""
        cache_key = prep_result['cache_key']
        data = prep_result['data']
        params = prep_result['processing_params']
        
        # Check cache first
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return {
                'result': cached_result,
                'cache_hit': True,
                'processing_time': 0,
                'cache_key': cache_key
            }
        
        # Process data (expensive operation)
        start_time = time.time()
        
        # Your expensive processing logic here
        result = self._expensive_processing(data, params)
        
        processing_time = time.time() - start_time
        
        # Cache the result
        self._store_in_cache(cache_key, result)
        
        return {
            'result': result,
            'cache_hit': False,
            'processing_time': processing_time,
            'cache_key': cache_key
        }
    
    def post(self, shared: SharedStore, prep_result, exec_result) -> Optional[str]:
        """Store result and cache statistics."""
        shared['processed_result'] = exec_result['result']
        shared['cache_stats'] = {
            'cache_hit': exec_result['cache_hit'],
            'processing_time': exec_result['processing_time'],
            'cache_key': exec_result['cache_key'],
            'cache_size': len(self.cache)
        }
        
        return None
    
    def _generate_cache_key(self, data: Any) -> str:
        """Generate a consistent cache key for the data."""
        # Convert data to JSON string and hash it
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Retrieve data from cache if not expired."""
        if cache_key not in self.cache:
            return None
        
        # Check if cache entry has expired
        if cache_key in self.cache_timestamps:
            age = time.time() - self.cache_timestamps[cache_key]
            if age > self.cache_ttl:
                # Remove expired entry
                del self.cache[cache_key]
                del self.cache_timestamps[cache_key]
                return None
        
        return self.cache[cache_key]
    
    def _store_in_cache(self, cache_key: str, result: Any):
        """Store result in cache with timestamp."""
        # Implement LRU eviction if cache is full
        if len(self.cache) >= self.max_cache_size:
            self._evict_oldest()
        
        self.cache[cache_key] = result
        self.cache_timestamps[cache_key] = time.time()
    
    def _evict_oldest(self):
        """Remove oldest cache entry."""
        if not self.cache_timestamps:
            return
        
        oldest_key = min(self.cache_timestamps.keys(), 
                        key=lambda k: self.cache_timestamps[k])
        
        del self.cache[oldest_key]
        del self.cache_timestamps[oldest_key]
    
    def _expensive_processing(self, data: Any, params: Dict[str, Any]) -> Any:
        """Placeholder for expensive processing logic."""
        # Replace with your actual processing logic
        time.sleep(0.1)  # Simulate work
        return f"processed_{data}"
    
    def clear_cache(self):
        """Manually clear the cache."""
        self.cache.clear()
        self.cache_timestamps.clear()

# Usage with cache management
cached_processor = CachedProcessor(cache_ttl=1800, max_cache_size=500)
result_handler = ProcessResultNode()

cached_processor >> result_handler

# Flow with cache clearing option
cache_cleaner = CacheClearNode()
cached_processor - "cache_full" >> cache_cleaner >> cached_processor
```

---

## Testing Recipes

### Recipe: Node Testing Template

**When to Use**: Unit testing individual nodes, integration testing flows

**Pattern**: pytest with mocks

```python
# Required imports for end-user project testing
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from typing import Dict, Any, List
from pocketflow import SharedStore, Node, AsyncNode, BatchNode, Flow

# Import your actual node classes here:
# from your_project.nodes import YourNode, YourAsyncNode, YourBatchNode

class TestYourNode:
    """Template for testing PocketFlow nodes."""
    
    @pytest.fixture
    def shared_store(self):
        """Create a shared store for testing."""
        return SharedStore({
            'test_data': 'sample_value',
            'config': {'param1': 'value1'}
        })
    
    @pytest.fixture
    def node_instance(self):
        """Create node instance for testing."""
        return YourNode()
    
    def test_prep_success(self, node_instance, shared_store):
        """Test successful prep phase."""
        result = node_instance.prep(shared_store)
        
        assert result is not None
        assert 'required_field' in result
        assert result['required_field'] == expected_value
    
    def test_prep_missing_data(self, node_instance):
        """Test prep with missing required data."""
        empty_store = SharedStore({})
        
        with pytest.raises(ValueError, match="required_field is missing"):
            node_instance.prep(empty_store)
    
    def test_exec_success(self, node_instance):
        """Test successful exec phase."""
        prep_result = {
            'data': 'test_data',
            'config': {'setting': 'value'}
        }
        
        result = node_instance.exec(prep_result)
        
        assert result is not None
        assert result['status'] == 'success'
        assert 'processed_data' in result
    
    def test_exec_error_handling(self, node_instance):
        """Test exec error handling."""
        invalid_prep = {'invalid': 'data'}
        
        # Should not raise, should handle gracefully
        result = node_instance.exec(invalid_prep)
        
        assert result is not None
        assert result.get('status') == 'error'
        assert 'error_message' in result
    
    def test_post_success_path(self, node_instance, shared_store):
        """Test post phase success path."""
        prep_result = {'test': 'data'}
        exec_result = {
            'status': 'success',
            'processed_data': 'result'
        }
        
        route = node_instance.post(shared_store, prep_result, exec_result)
        
        assert route is None  # Success path
        assert shared_store['processed_data'] == 'result'
    
    def test_post_error_routing(self, node_instance, shared_store):
        """Test post phase error routing."""
        prep_result = {'test': 'data'}
        exec_result = {
            'status': 'error',
            'error': 'processing failed'
        }
        
        route = node_instance.post(shared_store, prep_result, exec_result)
        
        assert route == 'error_handler'
        assert 'error_info' in shared_store
    
    @patch('your_module.external_api_call')
    def test_with_external_dependency(self, mock_api, node_instance, shared_store):
        """Test node with mocked external dependencies."""
        mock_api.return_value = {'result': 'mocked_data'}
        
        result = node_instance.exec({'api_endpoint': 'test'})
        
        mock_api.assert_called_once()
        assert result['data'] == 'mocked_data'

class TestAsyncNode:
    """Template for testing async nodes."""
    
    @pytest.mark.asyncio
    async def test_prep_async(self):
        """Test async prep phase."""
        node = YourAsyncNode()
        shared_store = SharedStore({'input': 'test'})
        
        result = await node.prep_async(shared_store)
        
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_exec_async_with_mock(self):
        """Test async exec with mocked async calls."""
        node = YourAsyncNode()
        
        with patch('your_module.async_operation', new_callable=AsyncMock) as mock_op:
            mock_op.return_value = 'async_result'
            
            result = await node.exec_async({'data': 'test'})
            
            mock_op.assert_called_once()
            assert result['async_data'] == 'async_result'
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test async operation timeout handling."""
        node = YourAsyncNode()
        
        with patch('your_module.slow_async_operation', new_callable=AsyncMock) as mock_slow:
            mock_slow.side_effect = asyncio.TimeoutError()
            
            result = await node.exec_async({'timeout': 1})
            
            assert result['status'] == 'timeout'

class TestBatchNode:
    """Template for testing batch nodes."""
    
    @pytest.mark.asyncio
    async def test_parallel_batch_processing(self):
        """Test parallel batch processing."""
        node = YourBatchNode()
        shared_store = SharedStore({
            'items_to_process': ['item1', 'item2', 'item3']
        })
        
        # Test prep
        prep_result = await node.prep_async(shared_store)
        assert len(prep_result) == 3
        
        # Test exec (single item)
        exec_result = await node.exec_async('item1')
        assert exec_result is not None
        
        # Test post with multiple results
        exec_results = ['result1', 'result2', 'result3']
        route = await node.post_async(shared_store, prep_result, exec_results)
        
        assert shared_store['batch_results'] == exec_results
    
    def test_batch_error_handling(self):
        """Test batch processing with some failures."""
        # Test partial success scenarios
        pass

class TestFlowIntegration:
    """Template for testing complete flows."""
    
    @pytest.mark.asyncio
    async def test_simple_flow(self):
        """Test a complete flow end-to-end."""
        # Setup nodes
        input_node = InputProcessorNode()
        transform_node = DataTransformNode() 
        output_node = OutputFormatterNode()
        
        # Connect flow
        input_node >> transform_node >> output_node
        
        # Setup shared store
        shared_store = SharedStore({
            'input_data': 'test_input'
        })
        
        # Run flow
        flow = Flow(start=input_node)
        await flow.run_async(shared_store)
        
        # Verify results
        assert 'final_output' in shared_store
        assert shared_store['final_output'] is not None
    
    @pytest.mark.asyncio
    async def test_branching_flow(self):
        """Test flow with conditional branching."""
        # Setup nodes with branching
        decision_node = DecisionNode()
        path_a = PathANode()
        path_b = PathBNode()
        final_node = FinalNode()
        
        # Setup branching
        decision_node - "condition_a" >> path_a >> final_node
        decision_node - "condition_b" >> path_b >> final_node
        
        # Test both paths
        for condition in ['condition_a', 'condition_b']:
            shared_store = SharedStore({'condition': condition})
            flow = Flow(start=decision_node)
            await flow.run_async(shared_store)
            
            assert shared_store['flow_completed'] is True

# Utility functions for testing
def create_test_shared_store(**kwargs) -> SharedStore:
    """Create a SharedStore with test data."""
    defaults = {
        'test_mode': True,
        'timestamp': '2025-09-05T12:00:00Z'
    }
    defaults.update(kwargs)
    return SharedStore(defaults)

def assert_node_result(result: Dict[str, Any], expected_keys: List[str]):
    """Assert that node result has expected structure."""
    assert result is not None
    for key in expected_keys:
        assert key in result, f"Missing expected key: {key}"

@pytest.fixture
async def mock_llm_call():
    """Mock LLM API calls for testing."""
    with patch('your_module.call_llm_async') as mock:
        mock.return_value = "Mocked LLM response"
        yield mock

# Performance testing helpers
@pytest.mark.performance
def test_node_performance():
    """Test node performance characteristics."""
    node = PerformanceCriticalNode()
    
    import time
    start_time = time.time()
    
    # Run multiple iterations
    for i in range(100):
        result = node.exec({'iteration': i})
    
    elapsed_time = time.time() - start_time
    
    # Assert performance requirements
    assert elapsed_time < 1.0, f"Performance test failed: {elapsed_time}s > 1.0s"
```

---

## Additional Recipes

### Recipe: RAG Pipeline

**When to Use**: Document retrieval and generation, question answering, knowledge-based systems

```python
class RAGPipeline:
    """Complete RAG implementation with all components."""
    
    class DocumentLoader(AsyncNode):
        async def exec_async(self, prep_result):
            # Load documents from various sources
            pass
    
    class EmbeddingGenerator(AsyncBatchNode):
        async def exec_async(self, document):
            # Generate embeddings for document chunks
            pass
    
    class QueryProcessor(Node):
        def exec(self, prep_result):
            # Process and enhance user queries
            pass
    
    class Retriever(AsyncNode):
        async def exec_async(self, prep_result):
            # Retrieve relevant documents
            pass
    
    class ContextFormatter(Node):
        def exec(self, prep_result):
            # Format retrieved documents for generation
            pass
    
    class LLMGenerator(AsyncNode):
        async def exec_async(self, prep_result):
            # Generate response using LLM with context
            pass
```

### Recipe: Multi-Agent Coordination

**When to Use**: Complex tasks requiring specialized agents, consensus building, distributed processing

```python
class MultiAgentCoordinator:
    """Coordinate multiple specialized agents."""
    
    class TaskCoordinator(Node):
        def exec(self, prep_result):
            # Distribute tasks among agents
            pass
    
    class SpecialistAgent(AsyncNode):
        async def exec_async(self, prep_result):
            # Execute specialized tasks
            pass
    
    class ConsensusManager(Node):
        def exec(self, prep_result):
            # Manage consensus between agents
            pass
    
    class ResultIntegrator(Node):
        def exec(self, prep_result):
            # Integrate results from multiple agents
            pass
```

---

## Best Practices Summary

### ✅ DO (Good Patterns)

1. **Use appropriate node types**:
   - `Node` for synchronous processing
   - `AsyncNode` for I/O operations  
   - `BatchNode` for collection processing
   - `AsyncParallelBatchNode` for concurrent operations

2. **Follow the lifecycle pattern**:
   - `prep()`: Data access and validation only
   - `exec()`: Pure business logic, no SharedStore access
   - `post()`: Result storage and routing decisions

3. **Handle errors gracefully**:
   - Use try/catch in exec methods
   - Return error information instead of raising
   - Route to appropriate error handlers

4. **Design for testability**:
   - Keep nodes focused and small
   - Mock external dependencies
   - Test each lifecycle phase separately

### ❌ DON'T (Antipatterns)

1. **Don't mix responsibilities**:
   - One node, one responsibility
   - Don't put business logic in utilities
   - Don't access SharedStore in exec()

2. **Don't use wrong node types**:
   - No loops in regular nodes
   - No blocking I/O in sync nodes
   - No single items in batch nodes

3. **Don't ignore error handling**:
   - Don't let exceptions bubble up
   - Don't fail fast without cleanup
   - Don't ignore partial failures

4. **Don't create testing nightmares**:
   - No monolithic nodes
   - No hidden dependencies
   - No untestable external calls

---

## Related Documentation

- [PocketFlow Best Practices](./POCKETFLOW_BEST_PRACTICES.md) - Comprehensive implementation guide
- [Common Antipatterns](./COMMON_ANTIPATTERNS.md) - Detailed antipattern analysis  
- [Migration Guides](./migrations/) - Specific migration scenarios
- [Example Templates](../templates/examples/) - Working code examples

---

*This cookbook provides quick-reference recipes for common PocketFlow scenarios. For detailed explanations and comprehensive guidance, refer to the best practices and antipatterns documentation.*