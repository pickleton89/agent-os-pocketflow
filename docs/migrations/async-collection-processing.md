# Migration Guide: Async Collection Processing

**Antipattern**: Synchronous Collection Processing  
**Severity**: 🟠 Medium  
**Time Estimate**: 1-2 hours  
**Risk Level**: Low (framework provides clear patterns)

## Problem Description

Processing collections (lists, arrays) synchronously in regular Node `exec()` methods creates performance bottlenecks. PocketFlow provides specialized node types (BatchNode, AsyncParallelBatchNode) designed for efficient collection processing.

## Detecting the Problem

### Automated Detection
```bash
# Run antipattern detector
python pocketflow-tools/antipattern_detector.py your_code/

# Look for violations like:
# "Loop in exec() method suggests collection processing in regular Node"
# "Blocking I/O operation in regular Node"
```

### Manual Inspection
Look for these patterns in regular Node classes:

```python
# 🚨 ANTIPATTERN EXAMPLES

class BadSyncCollectionNode(Node):  # ❌ Regular Node processing collections
    def exec(self, prep_result):
        documents = prep_result['documents']
        results = []
        
        # ❌ Sequential processing in regular Node
        for doc in documents:
            # ❌ Blocking I/O in loop
            content = requests.get(doc.url).text
            
            # ❌ LLM calls in loop
            summary = call_llm_summarize(content)
            processed = call_llm_analyze(summary)
            
            results.append({
                'document_id': doc.id,
                'summary': summary,
                'analysis': processed
            })
        
        return results


class BadBlockingIONode(Node):  # ❌ Regular Node with blocking I/O
    def exec(self, prep_result):
        urls = prep_result['urls']
        responses = []
        
        # ❌ Blocking I/O operations in regular Node
        for url in urls:
            try:
                response = requests.get(url, timeout=30)  # ❌ Blocks thread
                responses.append(response.json())
            except requests.RequestException:
                responses.append(None)
        
        return responses


class BadMixedPatternNode(Node):  # ❌ Mixed sync/async patterns
    def exec(self, prep_result):
        items = prep_result['items']
        
        # ❌ Some async operations in sync context
        loop = asyncio.get_event_loop()
        results = []
        
        for item in items:
            # ❌ Running async functions in sync loop
            result = loop.run_until_complete(async_process_item(item))
            results.append(result)
        
        return results
```

## Migration Steps

### Step 1: Identify Collection Processing Patterns (15 minutes)

Audit your nodes for collection processing:

```python
# Collection processing audit
COLLECTION_PATTERNS = {
    "sync_loops": "for/while loops over collections",
    "blocking_io": "requests.get/post, file operations in loops",
    "llm_calls_in_loops": "call_llm* inside iterations",
    "mixed_async_sync": "asyncio calls in sync contexts",
    "thread_pool_usage": "ThreadPoolExecutor, multiprocessing"
}

# Example audit results:
node_audit = {
    "DocumentProcessingNode": {
        "patterns": ["sync_loops", "blocking_io", "llm_calls_in_loops"],
        "collection_size": "variable (1-100 docs)",
        "processing_time": "~5 seconds per doc",
        "recommendation": "Use AsyncParallelBatchNode"
    },
    "URLFetcherNode": {
        "patterns": ["blocking_io", "sync_loops"],
        "collection_size": "10-50 URLs",
        "processing_time": "~2 seconds per URL",
        "recommendation": "Use AsyncParallelBatchNode"
    },
    "TextAnalysisNode": {
        "patterns": ["llm_calls_in_loops"],
        "collection_size": "5-20 texts",
        "processing_time": "~3 seconds per text",
        "recommendation": "Use BatchNode or AsyncParallelBatchNode"
    }
}
```

### Step 2: Choose the Right Node Type (10 minutes)

Select appropriate PocketFlow node types:

```python
# Decision matrix for node types

NODE_TYPE_SELECTION = {
    "BatchNode": {
        "when_to_use": [
            "CPU-bound processing of collections",
            "LLM calls without I/O",
            "Simple sequential processing with dependencies"
        ],
        "example": "Text analysis, data transformations, LLM calls"
    },
    
    "AsyncParallelBatchNode": {
        "when_to_use": [
            "I/O-bound collection processing",
            "API calls, file downloads",
            "Independent parallel operations",
            "Mixed I/O and LLM calls"
        ],
        "example": "URL fetching, file uploads, API integrations"
    },
    
    "AsyncBatchNode": {
        "when_to_use": [
            "Async operations that must be sequential",
            "Operations with dependencies between items",
            "Rate-limited APIs requiring sequential access"
        ],
        "example": "Sequential API calls, ordered processing"
    }
}

# Example selection:
migration_plan = {
    "DocumentProcessingNode": {
        "current": "Node with sync loop",
        "recommended": "AsyncParallelBatchNode",
        "reason": "I/O operations (URL fetching) + LLM calls can be parallelized"
    },
    "TextAnalysisNode": {
        "current": "Node with LLM loops", 
        "recommended": "BatchNode",
        "reason": "CPU-bound LLM calls, simpler than async"
    },
    "SequentialAPINode": {
        "current": "Node with ordered API calls",
        "recommended": "AsyncBatchNode", 
        "reason": "Async I/O but must maintain order"
    }
}
```

### Step 3: Convert to BatchNode (20 minutes)

For CPU-bound collection processing:

```python
# ❌ Before: Sync loop in regular Node
class BadTextAnalysisNode(Node):
    def exec(self, prep_result):
        texts = prep_result['texts']
        analyses = []
        
        # ❌ Sequential processing in regular Node
        for text in texts:
            # CPU-bound LLM calls
            sentiment = call_llm_sentiment_analysis(text)
            entities = call_llm_entity_extraction(text)
            summary = call_llm_summarize(text)
            
            analyses.append({
                'text_id': text.id,
                'sentiment': sentiment,
                'entities': entities,
                'summary': summary
            })
        
        return analyses

# ✅ After: BatchNode for collection processing
class GoodTextAnalysisBatchNode(BatchNode):
    """Process single text item - framework handles the collection"""
    
    def exec(self, single_text):
        # Process single item - BatchNode handles iteration
        sentiment = call_llm_sentiment_analysis(single_text.content)
        entities = call_llm_entity_extraction(single_text.content)
        summary = call_llm_summarize(single_text.content)
        
        return {
            'text_id': single_text.id,
            'sentiment': sentiment,
            'entities': entities,
            'summary': summary
        }

# Usage in flow:
class TextAnalysisFlow(Flow):
    def __init__(self):
        super().__init__()
        
        # BatchNode automatically processes collections
        self.add_node("analyze_texts", GoodTextAnalysisBatchNode())
        
    def run(self, input_data):
        # Pass collection directly - BatchNode handles iteration
        return super().run({
            'texts': input_data['text_collection']  # List of texts
        })
```

### Step 4: Convert to AsyncParallelBatchNode (30 minutes)

For I/O-bound operations that can be parallelized:

```python
# ❌ Before: Blocking I/O in regular Node
class BadURLFetcherNode(Node):
    def exec(self, prep_result):
        urls = prep_result['urls']
        results = []
        
        # ❌ Sequential blocking operations
        for url in urls:
            try:
                response = requests.get(url, timeout=30)  # ❌ Blocks
                content = response.text
                
                # ❌ Follow-up LLM call in loop
                analysis = call_llm_analyze_content(content)
                
                results.append({
                    'url': url,
                    'content': content[:1000],  # Truncate for storage
                    'analysis': analysis,
                    'success': True
                })
            except requests.RequestException as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'success': False
                })
        
        return results

# ✅ After: AsyncParallelBatchNode for parallel I/O
class GoodURLFetcherBatchNode(AsyncParallelBatchNode):
    """Fetch and analyze single URL - framework handles parallelization"""
    
    async def exec_async(self, single_url):
        # Process single item - AsyncParallelBatchNode handles parallel execution
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                # ✅ Async I/O operation
                async with session.get(single_url, timeout=30) as response:
                    content = await response.text()
                    
                    # ✅ LLM call still works in async context
                    analysis = call_llm_analyze_content(content)
                    
                    return {
                        'url': single_url,
                        'content': content[:1000],
                        'analysis': analysis,
                        'success': True
                    }
                    
        except Exception as e:
            return {
                'url': single_url,
                'error': str(e),
                'success': False
            }

# Usage configuration:
class URLAnalysisFlow(Flow):
    def __init__(self):
        super().__init__()
        
        # Configure parallel processing
        batch_config = AsyncParallelBatchConfig(
            max_concurrency=5,  # Process 5 URLs simultaneously
            timeout_per_item=30,  # 30 seconds per URL
            retry_failed=True
        )
        
        self.add_node("fetch_urls", 
                     GoodURLFetcherBatchNode(config=batch_config))
```

### Step 5: Convert to AsyncBatchNode (25 minutes)

For async operations that must be sequential:

```python
# ❌ Before: Mixed async/sync with dependencies
class BadSequentialAPINode(Node):
    def exec(self, prep_result):
        user_ids = prep_result['user_ids']
        loop = asyncio.get_event_loop()
        results = []
        
        # ❌ Sequential processing with async operations in sync context
        for user_id in user_ids:
            # ❌ Running async in sync context
            user_data = loop.run_until_complete(
                fetch_user_data_async(user_id)
            )
            
            # Dependencies require sequential processing
            if user_data and user_data.requires_premium_analysis:
                # ❌ Another async call in sync loop
                premium_analysis = loop.run_until_complete(
                    call_premium_llm_async(user_data.content)
                )
                user_data.analysis = premium_analysis
            
            results.append(user_data)
        
        return results

# ✅ After: AsyncBatchNode for sequential async processing
class GoodSequentialAPIBatchNode(AsyncBatchNode):
    """Process single user sequentially with async operations"""
    
    async def exec_async(self, single_user_id):
        # ✅ Proper async context for single item
        user_data = await fetch_user_data_async(single_user_id)
        
        if user_data and user_data.requires_premium_analysis:
            # ✅ Sequential dependency handling
            premium_analysis = await call_premium_llm_async(user_data.content)
            user_data.analysis = premium_analysis
        
        return user_data

# Usage with proper configuration:
class UserAnalysisFlow(Flow):
    def __init__(self):
        super().__init__()
        
        # Sequential processing with rate limiting
        batch_config = AsyncBatchConfig(
            delay_between_items=1.0,  # 1 second delay for rate limiting
            timeout_per_item=45,      # Longer timeout for complex operations
            stop_on_error=False       # Continue processing other users
        )
        
        self.add_node("process_users", 
                     GoodSequentialAPIBatchNode(config=batch_config))
```

### Step 6: Handle Complex Cases (40 minutes)

#### Case A: Mixed Collection and Single Item Processing

```python
# ❌ Before: Mixed processing patterns
class BadMixedProcessingNode(Node):
    def exec(self, prep_result):
        # Collection processing
        documents = prep_result['documents']
        processed_docs = []
        
        for doc in documents:
            content = process_document(doc)  # ❌ Loop in regular Node
            processed_docs.append(content)
        
        # Single item processing
        summary_data = {
            'total_docs': len(processed_docs),
            'overall_summary': call_llm_summarize_collection(processed_docs)
        }
        
        return {
            'processed_documents': processed_docs,
            'summary': summary_data
        }

# ✅ After: Separate nodes for different processing patterns
class DocumentBatchProcessor(BatchNode):
    """Handle individual document processing"""
    def exec(self, single_document):
        return process_document(single_document)

class CollectionSummarizerNode(Node):
    """Handle collection-level operations"""
    def exec(self, prep_result):
        processed_docs = prep_result['processed_documents']
        
        return {
            'total_docs': len(processed_docs),
            'overall_summary': call_llm_summarize_collection(processed_docs)
        }

class MixedProcessingFlow(Flow):
    def __init__(self):
        super().__init__()
        
        # First process collection items
        self.add_node("process_docs", DocumentBatchProcessor())
        
        # Then handle collection-level operations
        self.add_node("summarize", CollectionSummarizerNode())
        
        self.add_edge("process_docs", "summarize")
```

#### Case B: Error Handling in Batch Processing

```python
# ✅ Robust error handling in batch nodes
class RobustAsyncBatchNode(AsyncParallelBatchNode):
    """Handle errors gracefully in parallel processing"""
    
    async def exec_async(self, single_item):
        try:
            # Main processing logic
            result = await process_item_async(single_item)
            
            return {
                'item_id': single_item.id,
                'success': True,
                'result': result,
                'error': None
            }
            
        except TemporaryError as e:
            # Recoverable errors - framework can retry
            logger.warning(f"Temporary error processing {single_item.id}: {e}")
            raise  # Let framework handle retry
            
        except PermanentError as e:
            # Permanent errors - return error result
            logger.error(f"Permanent error processing {single_item.id}: {e}")
            return {
                'item_id': single_item.id,
                'success': False,
                'result': None,
                'error': str(e)
            }

# Configuration for error handling:
error_handling_config = AsyncParallelBatchConfig(
    max_concurrency=3,
    max_retries=2,          # Retry temporary failures
    retry_delay=5.0,        # Wait 5 seconds between retries
    stop_on_error=False,    # Continue processing other items
    timeout_per_item=60     # 60 seconds per item
)
```

#### Case C: Conditional Collection Processing

```python
# ✅ Conditional processing with batch nodes
class ConditionalBatchProcessor(BatchNode):
    """Process items conditionally based on their properties"""
    
    def exec(self, single_item):
        # Different processing based on item properties
        if single_item.type == 'premium':
            return self._process_premium_item(single_item)
        elif single_item.type == 'standard':
            return self._process_standard_item(single_item)
        else:
            return self._process_basic_item(single_item)
    
    def _process_premium_item(self, item):
        # Premium processing with advanced LLM
        analysis = call_llm_advanced_analysis(item.content)
        enhancement = call_llm_enhance_premium(analysis)
        return {'type': 'premium', 'analysis': analysis, 'enhancement': enhancement}
    
    def _process_standard_item(self, item):
        # Standard processing
        analysis = call_llm_standard_analysis(item.content)
        return {'type': 'standard', 'analysis': analysis}
    
    def _process_basic_item(self, item):
        # Basic processing - no LLM calls
        return {'type': 'basic', 'word_count': len(item.content.split())}

# Alternative: Separate nodes for different types
class PremiumItemProcessor(BatchNode):
    def exec(self, single_premium_item):
        analysis = call_llm_advanced_analysis(single_premium_item.content)
        enhancement = call_llm_enhance_premium(analysis)
        return {'analysis': analysis, 'enhancement': enhancement}

class StandardItemProcessor(BatchNode):
    def exec(self, single_standard_item):
        analysis = call_llm_standard_analysis(single_standard_item.content)
        return {'analysis': analysis}

class TypeBasedProcessingFlow(Flow):
    def __init__(self):
        super().__init__()
        
        # Route different types to different processors
        self.add_node("route", ItemTypeRouterNode())
        self.add_node("premium", PremiumItemProcessor())
        self.add_node("standard", StandardItemProcessor())
        
        # Conditional routing
        self.add_conditional_edge("route", "premium", 
                                lambda result: result.get('type') == 'premium')
        self.add_conditional_edge("route", "standard",
                                lambda result: result.get('type') == 'standard')
```

### Step 7: Update Tests (20 minutes)

```python
# ✅ Testing batch nodes

class TestGoodTextAnalysisBatchNode:
    def test_single_item_processing(self):
        """Test processing of single item"""
        node = GoodTextAnalysisBatchNode()
        
        # Mock single text item
        mock_text = Mock(id='text_1', content='Sample text content')
        
        with patch('your_module.call_llm_sentiment_analysis', return_value='positive'), \
             patch('your_module.call_llm_entity_extraction', return_value=['entity1']), \
             patch('your_module.call_llm_summarize', return_value='summary'):
            
            result = node.exec(mock_text)
            
            assert result['text_id'] == 'text_1'
            assert result['sentiment'] == 'positive'
            assert result['entities'] == ['entity1']
            assert result['summary'] == 'summary'


class TestGoodURLFetcherBatchNode:
    @pytest.mark.asyncio
    async def test_successful_url_fetch(self):
        """Test successful async URL fetching"""
        node = GoodURLFetcherBatchNode()
        test_url = 'https://example.com'
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.text.return_value = "Sample content"
            mock_get.return_value.__aenter__.return_value = mock_response
            
            with patch('your_module.call_llm_analyze_content', return_value='analysis'):
                result = await node.exec_async(test_url)
                
                assert result['url'] == test_url
                assert result['success'] is True
                assert result['analysis'] == 'analysis'
    
    @pytest.mark.asyncio
    async def test_failed_url_fetch(self):
        """Test error handling in async processing"""
        node = GoodURLFetcherBatchNode()
        test_url = 'https://invalid-url.com'
        
        with patch('aiohttp.ClientSession.get', side_effect=aiohttp.ClientError("Network error")):
            result = await node.exec_async(test_url)
            
            assert result['url'] == test_url
            assert result['success'] is False
            assert 'Network error' in result['error']


class TestBatchNodeIntegration:
    def test_batch_processing_flow(self):
        """Test complete flow with batch processing"""
        flow = TextAnalysisFlow()
        
        # Mock collection of texts
        input_texts = [
            Mock(id='text_1', content='First text'),
            Mock(id='text_2', content='Second text'),
            Mock(id='text_3', content='Third text')
        ]
        
        input_data = {'text_collection': input_texts}
        
        with patch('your_module.call_llm_sentiment_analysis', return_value='positive'), \
             patch('your_module.call_llm_entity_extraction', return_value=['entity']), \
             patch('your_module.call_llm_summarize', return_value='summary'):
            
            result = flow.run(input_data)
            
            # Should process all items
            assert len(result['analyses']) == 3
            
            # Each item should be processed
            for analysis in result['analyses']:
                assert analysis['sentiment'] == 'positive'
                assert analysis['entities'] == ['entity']
                assert analysis['summary'] == 'summary'
```

## Performance Comparison

### Before and After Metrics

```python
# Performance testing example
import time
import asyncio

class PerformanceTest:
    def test_sync_vs_batch_performance(self):
        """Compare sync vs batch processing performance"""
        
        # Test data
        items = [f"item_{i}" for i in range(20)]
        
        # ❌ Sync processing timing
        start_time = time.time()
        sync_results = []
        for item in items:
            result = simulate_processing(item, delay=0.1)  # 100ms per item
            sync_results.append(result)
        sync_time = time.time() - start_time
        
        # ✅ Batch processing timing
        start_time = time.time()
        batch_node = ProcessingBatchNode()
        batch_results = []
        for item in items:
            result = batch_node.exec(item)  # Framework can optimize
            batch_results.append(result)
        batch_time = time.time() - start_time
        
        print(f"Sync processing: {sync_time:.2f}s ({sync_time/len(items)*1000:.1f}ms per item)")
        print(f"Batch processing: {batch_time:.2f}s ({batch_time/len(items)*1000:.1f}ms per item)")
        
        # Batch processing should be similar for CPU-bound
        # But enables framework optimizations
    
    async def test_sync_vs_async_batch_performance(self):
        """Compare sync vs async batch processing for I/O"""
        
        # Test URLs (mock)
        urls = [f"https://example.com/page_{i}" for i in range(10)]
        
        # ❌ Sync I/O timing (sequential)
        start_time = time.time()
        sync_results = []
        for url in urls:
            result = simulate_io_operation(url, delay=0.5)  # 500ms per request
            sync_results.append(result)
        sync_time = time.time() - start_time
        
        # ✅ Async batch timing (parallel)
        start_time = time.time()
        async_batch_node = AsyncIOBatchNode()
        tasks = [async_batch_node.exec_async(url) for url in urls]
        async_results = await asyncio.gather(*tasks)
        async_time = time.time() - start_time
        
        print(f"Sync I/O: {sync_time:.2f}s (sequential)")
        print(f"Async batch I/O: {async_time:.2f}s (parallel)")
        
        # Async should be much faster for I/O operations
        assert async_time < sync_time / 2  # At least 2x faster
```

Expected performance improvements:

| Processing Type | Collection Size | Sync Time | Async Batch Time | Speedup |
|----------------|-----------------|-----------|------------------|---------|
| I/O Operations (API calls) | 10 items | 10s | 2s | 5x faster |
| I/O Operations (file downloads) | 20 items | 30s | 6s | 5x faster |
| CPU Operations (LLM calls) | 10 items | 15s | 15s | Same* |
| Mixed I/O + CPU | 15 items | 25s | 8s | 3x faster |

*CPU operations benefit from framework optimization and better error handling

## Success Criteria

✅ **Performance**
- I/O-bound operations show significant speedup (3-5x)
- CPU-bound operations maintain performance with better error handling
- Memory usage remains stable during collection processing
- No blocking operations in event loops

✅ **Code Quality**
- No loops over collections in regular Node exec() methods  
- Appropriate node types used for different processing patterns
- Clean error handling for individual items and collections
- Async operations use proper async/await patterns

✅ **Framework Compliance**
- BatchNode used for CPU-bound collection processing
- AsyncParallelBatchNode used for I/O-bound parallel operations
- AsyncBatchNode used for sequential async operations
- Configuration options properly utilized

## Time Estimates by Collection Size and Complexity

| Collection Size | Processing Complexity | Estimated Time |
|----------------|----------------------|----------------|
| Small (1-10 items) | Simple processing | 30-45 minutes |
| Medium (10-50 items) | I/O + LLM processing | 1-1.5 hours |
| Large (50+ items) | Complex mixed operations | 1.5-2 hours |

Add time for:
- Complex error handling requirements: +30 minutes
- Performance optimization and testing: +30 minutes
- Integration with existing flows: +30 minutes

## Troubleshooting

### Issue: "AsyncParallelBatchNode too aggressive"
```python
# Problem: Too many concurrent operations overwhelming resources
config = AsyncParallelBatchConfig(
    max_concurrency=1000,  # ❌ Too aggressive
    timeout_per_item=5
)

# Solution: Reasonable concurrency limits
config = AsyncParallelBatchConfig(
    max_concurrency=5,     # ✅ Conservative limit
    timeout_per_item=30,   # ✅ Realistic timeout
    rate_limit_delay=0.1   # ✅ Respect rate limits
)
```

### Issue: "Batch node needs collection-level data"
```python
# Problem: Individual items need access to collection metadata
class BadBatchNode(BatchNode):
    def exec(self, single_item):
        # ❌ Can't access total count or other collection data
        return f"Processing item {single_item.id} of {???} total"

# Solution: Add collection metadata to items during prep
class CollectionPreparationNode(Node):
    def exec(self, prep_result):
        items = prep_result['items']
        total_count = len(items)
        
        # Add collection metadata to each item
        enriched_items = []
        for i, item in enumerate(items):
            item.collection_metadata = {
                'total_count': total_count,
                'current_index': i,
                'is_first': i == 0,
                'is_last': i == total_count - 1
            }
            enriched_items.append(item)
        
        return {'enriched_items': enriched_items}

class GoodBatchNode(BatchNode):
    def exec(self, single_item):
        metadata = single_item.collection_metadata
        return f"Processing item {single_item.id} ({metadata['current_index']+1} of {metadata['total_count']})"
```

### Issue: "Need to aggregate batch results"
```python
# Problem: Need to combine individual batch results
class ResultAggregationNode(Node):
    """Aggregate results from batch processing"""
    
    def exec(self, prep_result):
        batch_results = prep_result['batch_results']  # List of individual results
        
        # Aggregate processing
        successful_items = [r for r in batch_results if r.get('success', True)]
        failed_items = [r for r in batch_results if not r.get('success', True)]
        
        # Calculate statistics
        success_rate = len(successful_items) / len(batch_results) if batch_results else 0
        
        return {
            'total_processed': len(batch_results),
            'successful': len(successful_items),
            'failed': len(failed_items),
            'success_rate': success_rate,
            'successful_results': successful_items,
            'errors': [item.get('error') for item in failed_items if item.get('error')]
        }

# Usage in flow
class ProcessAndAggregateFlow(Flow):
    def __init__(self):
        super().__init__()
        
        self.add_node("process_items", ItemBatchProcessor())
        self.add_node("aggregate", ResultAggregationNode())
        
        self.add_edge("process_items", "aggregate")
```

## Related Guides

- [Fix Lifecycle Violations](fix-lifecycle-violations.md) - For proper async method usage
- [Remove Shared Store from exec()](remove-shared-store-exec.md) - For clean data access in batch nodes
- [Monolithic to Focused Nodes](monolithic-to-focused.md) - For splitting complex collection processing