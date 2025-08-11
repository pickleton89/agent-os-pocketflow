# PocketFlow Style Guide

> Version: 1.0.0
> Last Updated: 2025-01-11

## PocketFlow-Specific Patterns

This file contains detailed PocketFlow conventions that extend the base code-style.md rules for LLM workflow development.

## Node Design Patterns

### Node Naming Standards
```python
# Node classes: PascalCase + "Node" suffix
class FetchDataNode(Node):
    """Fetches data from external API."""

class ProcessTextNode(Node):  
    """Processes text using LLM."""

class ValidateOutputNode(Node):
    """Validates LLM output format."""

# Async variants
class AsyncFetchNode(Node):
    """Async version of data fetching."""

# Batch processing
class BatchProcessNode(Node):
    """Processes multiple items in batch."""
```

### Lifecycle Method Implementation
```python
from pocketflow import Node, SharedStore
from typing import Dict, Any, Optional

class DataProcessingNode(Node):
    """Example node with all lifecycle methods."""
    
    def prep(self, shared_store: SharedStore) -> Optional[str]:
        """Prepare node execution - validate inputs."""
        
        # Validate required inputs
        if 'input_data' not in shared_store:
            self.logger.error("Missing required input_data")
            return "error"
        
        # Set up processing parameters
        shared_store['processing_started'] = True
        shared_store['node_config'] = {
            'batch_size': 10,
            'timeout': 30
        }
        
        self.logger.info("Node preparation completed")
        return None  # Continue to exec
    
    def exec(self, shared_store: SharedStore) -> Optional[str]:
        """Execute main node logic."""
        
        input_data = shared_store['input_data']
        config = shared_store['node_config']
        
        try:
            # Process data
            results = self.process_data(input_data, config)
            
            # Store results with timestamp
            shared_store['processed_results'] = results
            shared_store['processed_timestamp'] = datetime.utcnow().isoformat()
            
            self.logger.info(
                "Processing completed",
                items_processed=len(results)
            )
            
            return None  # Success - continue flow
            
        except Exception as e:
            self.logger.error(
                "Processing failed", 
                error=str(e),
                input_size=len(input_data)
            )
            shared_store['error_details'] = {
                'node': self.__class__.__name__,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
            return "error"
    
    def post(self, shared_store: SharedStore) -> Optional[str]:
        """Post-execution cleanup and logging."""
        
        # Cleanup temporary data
        if 'temp_processing_data' in shared_store:
            del shared_store['temp_processing_data']
        
        # Log completion stats
        if 'processed_results' in shared_store:
            results = shared_store['processed_results']
            self.logger.info(
                "Node execution completed",
                results_count=len(results),
                success=True
            )
        else:
            self.logger.warning("Node completed without results")
        
        return None  # Continue flow

    def process_data(self, data: list, config: dict) -> list:
        """Custom processing logic."""
        # Implementation here
        pass
```

### Async Node Patterns
```python
class AsyncLLMNode(Node):
    """Async LLM processing node."""
    
    async def prep_async(self, shared_store: SharedStore) -> Optional[str]:
        """Async preparation - validate API keys, test connections."""
        
        # Validate LLM configuration
        if not await self.validate_llm_connection():
            self.logger.error("LLM connection failed")
            return "error"
        
        return None
    
    async def exec_async(self, shared_store: SharedStore) -> Optional[str]:
        """Execute LLM processing asynchronously."""
        
        prompts = shared_store['prompts']
        
        # Process prompts concurrently
        tasks = [self.process_prompt(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle partial failures
        successful_results = []
        failed_count = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(
                    "Prompt processing failed",
                    prompt_index=i,
                    error=str(result)
                )
                failed_count += 1
            else:
                successful_results.append(result)
        
        # Store results and metadata
        shared_store['llm_results'] = successful_results
        shared_store['processing_stats'] = {
            'total': len(prompts),
            'successful': len(successful_results),
            'failed': failed_count
        }
        
        # Decide next action based on success rate
        success_rate = len(successful_results) / len(prompts)
        if success_rate < 0.5:
            return "retry"  # Retry if less than 50% success
        elif failed_count > 0:
            return "partial_success"  # Handle partial failures
        
        return None  # Complete success
    
    async def process_prompt(self, prompt: str) -> dict:
        """Process individual prompt with LLM."""
        # Implementation here
        pass
```

## Flow Design Patterns

### Flow Naming Standards
```python
# Flow classes: PascalCase + "Flow" suffix
class DataProcessingFlow(Flow):
    """Main data processing workflow."""

class LLMChainFlow(Flow):
    """Multi-step LLM processing chain."""

class ValidationFlow(Flow):
    """Output validation workflow."""
```

### Flow Configuration
```python
from pocketflow import Flow
from typing import Dict, List

class DocumentProcessingFlow(Flow):
    """Document processing with LLM enhancement."""
    
    def __init__(self):
        super().__init__()
        
        # Define action constants for clarity
        self.ACTION_SUCCESS = "success"
        self.ACTION_ERROR = "error"
        self.ACTION_RETRY = "retry"
        self.ACTION_VALIDATE = "validate"
        self.ACTION_ENHANCE = "enhance"
        self.ACTION_FINALIZE = "finalize"
    
    def setup_flow(self) -> Dict[str, any]:
        """Configure the flow nodes and routing."""
        
        return {
            # Node definitions
            'fetch_documents': FetchDocumentsNode(),
            'validate_input': ValidateInputNode(), 
            'process_llm': ProcessWithLLMNode(),
            'validate_output': ValidateOutputNode(),
            'enhance_results': EnhanceResultsNode(),
            'finalize_output': FinalizeOutputNode(),
            'handle_error': ErrorHandlerNode(),
            
            # Flow routing
            'flow': {
                'start': 'fetch_documents',
                'fetch_documents': {
                    None: 'validate_input',
                    self.ACTION_ERROR: 'handle_error'
                },
                'validate_input': {
                    None: 'process_llm',
                    'invalid': 'handle_error'
                },
                'process_llm': {
                    None: 'validate_output',
                    self.ACTION_RETRY: 'process_llm',  # Retry same node
                    self.ACTION_ERROR: 'handle_error'
                },
                'validate_output': {
                    None: 'enhance_results',
                    'invalid': 'process_llm',  # Go back and retry
                    self.ACTION_ERROR: 'handle_error'
                },
                'enhance_results': {
                    None: 'finalize_output',
                    'skip': 'finalize_output',
                    self.ACTION_ERROR: 'handle_error'
                },
                'finalize_output': {
                    None: 'end'
                },
                'handle_error': {
                    None: 'end'
                }
            }
        }
```

## Shared Store Conventions

### Key Naming Patterns
```python
# Use consistent key naming patterns
shared_store = {
    # Input data (raw_prefix)
    'raw_documents': [...],
    'raw_user_input': "...",
    'raw_api_response': {...},
    
    # Processed data (processed_prefix)
    'processed_documents': [...],
    'processed_chunks': [...],
    'processed_embeddings': [...],
    
    # Final outputs (final_prefix)
    'final_results': [...],
    'final_summary': "...",
    'final_metadata': {...},
    
    # Temporary data (temp_prefix)
    'temp_processing_state': {...},
    'temp_llm_context': "...",
    
    # Node-specific namespacing
    'fetcher_status': 'completed',
    'fetcher_results': [...],
    'processor_config': {...},
    'validator_errors': [...],
    
    # Timestamps
    'started_timestamp': '2025-01-11T10:00:00Z',
    'processed_timestamp': '2025-01-11T10:05:00Z',
    'completed_timestamp': '2025-01-11T10:10:00Z',
    
    # Status tracking
    'processing_status': 'in_progress',
    'current_step': 'llm_processing',
    'steps_completed': ['fetch', 'validate'],
    
    # Error handling
    'error_count': 0,
    'last_error': None,
    'retry_count': 0,
    'max_retries': 3,
}
```

### Type-Safe Store Access
```python
from typing import TypedDict, Optional, List, Dict, Any

class DocumentProcessingStore(TypedDict, total=False):
    """Type hints for shared store structure."""
    
    # Inputs
    raw_documents: List[str]
    processing_config: Dict[str, Any]
    
    # Processing state
    processed_chunks: List[Dict[str, Any]]
    llm_results: List[str]
    validation_errors: List[str]
    
    # Outputs
    final_results: List[Dict[str, Any]]
    final_summary: str
    
    # Metadata
    started_timestamp: str
    completed_timestamp: str
    processing_stats: Dict[str, int]

# Use in node implementations
def exec(self, shared_store: DocumentProcessingStore) -> Optional[str]:
    """Execute with type safety."""
    documents = shared_store.get('raw_documents', [])
    # Processing logic here
```

## Error Handling Patterns

### Node-Level Error Handling
```python
class RobustProcessingNode(Node):
    """Node with comprehensive error handling."""
    
    def exec(self, shared_store: SharedStore) -> Optional[str]:
        """Execute with proper error handling."""
        
        try:
            # Main processing logic
            result = self.process_data(shared_store['input'])
            shared_store['result'] = result
            return None
            
        except ValidationError as e:
            # Handle validation errors - usually retry with fixes
            self.logger.warning(
                "Validation failed - will retry", 
                error=str(e),
                retry_count=shared_store.get('retry_count', 0)
            )
            
            # Increment retry counter
            retry_count = shared_store.get('retry_count', 0) + 1
            shared_store['retry_count'] = retry_count
            
            if retry_count >= 3:
                shared_store['final_error'] = f"Max retries exceeded: {e}"
                return "error"
            
            return "retry"
            
        except ConnectionError as e:
            # Handle connection errors - often temporary
            self.logger.error("Connection failed", error=str(e))
            shared_store['connection_error'] = str(e)
            return "retry"
            
        except Exception as e:
            # Handle unexpected errors
            self.logger.exception("Unexpected error occurred")
            shared_store['unexpected_error'] = {
                'error': str(e),
                'type': type(e).__name__,
                'node': self.__class__.__name__
            }
            return "error"
```

### Flow-Level Error Recovery
```python
class ErrorRecoveryFlow(Flow):
    """Flow with built-in error recovery."""
    
    def setup_flow(self) -> Dict[str, any]:
        return {
            'main_processor': MainProcessingNode(),
            'backup_processor': BackupProcessingNode(),
            'error_analyzer': ErrorAnalyzerNode(),
            'recovery_handler': RecoveryHandlerNode(),
            
            'flow': {
                'start': 'main_processor',
                'main_processor': {
                    None: 'end',  # Success path
                    'error': 'error_analyzer'
                },
                'error_analyzer': {
                    'recoverable': 'backup_processor',
                    'use_fallback': 'recovery_handler',
                    'fatal': 'end'
                },
                'backup_processor': {
                    None: 'end',  # Success with backup
                    'error': 'recovery_handler'
                },
                'recovery_handler': {
                    None: 'end'  # Always end after recovery
                }
            }
        }
```

## LLM Integration Patterns

### LLM Utility Integration
```python
from utils.call_llm import call_llm
from pydantic import BaseModel

class LLMProcessingNode(Node):
    """Node that integrates with LLM utilities."""
    
    def exec(self, shared_store: SharedStore) -> Optional[str]:
        """Process data using LLM."""
        
        # Get input data and configuration
        input_text = shared_store['raw_text']
        llm_config = shared_store.get('llm_config', {})
        
        # Prepare prompt
        prompt = self.build_prompt(input_text)
        
        try:
            # Call LLM utility function
            response = call_llm(
                prompt=prompt,
                model=llm_config.get('model', 'gpt-4'),
                temperature=llm_config.get('temperature', 0.7),
                max_tokens=llm_config.get('max_tokens', 1000)
            )
            
            # Store raw response
            shared_store['llm_raw_response'] = response
            
            # Parse structured response if needed
            if 'output_schema' in shared_store:
                schema = shared_store['output_schema']
                parsed = self.parse_llm_response(response, schema)
                shared_store['llm_parsed_response'] = parsed
            
            self.logger.info("LLM processing completed successfully")
            return None
            
        except Exception as e:
            self.logger.error("LLM processing failed", error=str(e))
            shared_store['llm_error'] = str(e)
            return "retry"  # Let flow decide retry logic
    
    def build_prompt(self, input_text: str) -> str:
        """Build LLM prompt from input."""
        return f"""
        Please analyze the following text and provide insights:
        
        Text: {input_text}
        
        Please provide your analysis in a structured format.
        """
    
    def parse_llm_response(self, response: str, schema: BaseModel) -> dict:
        """Parse LLM response using Pydantic schema."""
        try:
            # Attempt to parse JSON response
            import json
            response_data = json.loads(response)
            return schema(**response_data).dict()
        except (json.JSONDecodeError, ValidationError) as e:
            self.logger.warning("Failed to parse structured response", error=str(e))
            return {"raw_response": response}
```

## Batch Processing Patterns

### Batch Node Implementation
```python
class BatchLLMNode(Node):
    """Process multiple items in batches."""
    
    def exec(self, shared_store: SharedStore) -> Optional[str]:
        """Process items in batches for efficiency."""
        
        items = shared_store['items_to_process']
        batch_size = shared_store.get('batch_size', 5)
        
        # Split into batches
        batches = [
            items[i:i + batch_size] 
            for i in range(0, len(items), batch_size)
        ]
        
        processed_results = []
        failed_batches = []
        
        for i, batch in enumerate(batches):
            try:
                self.logger.info(f"Processing batch {i+1}/{len(batches)}")
                
                # Process batch
                batch_results = self.process_batch(batch)
                processed_results.extend(batch_results)
                
                # Add small delay between batches to avoid rate limits
                if i < len(batches) - 1:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                self.logger.error(
                    f"Batch {i+1} failed", 
                    error=str(e),
                    batch_size=len(batch)
                )
                failed_batches.append(i)
        
        # Store results and statistics
        shared_store['processed_results'] = processed_results
        shared_store['batch_stats'] = {
            'total_batches': len(batches),
            'successful_batches': len(batches) - len(failed_batches),
            'failed_batches': failed_batches,
            'total_items': len(items),
            'processed_items': len(processed_results)
        }
        
        # Determine next action based on success rate
        success_rate = len(processed_results) / len(items)
        if success_rate < 0.7:  # Less than 70% success
            return "partial_failure"
        elif failed_batches:
            return "partial_success"
        
        return None  # Complete success
    
    def process_batch(self, batch: List[Any]) -> List[Any]:
        """Process a single batch of items."""
        # Implementation here
        pass
```

## Testing Patterns

### Node Testing
```python
import pytest
from unittest.mock import patch, MagicMock
from pocketflow import SharedStore

class TestDataProcessingNode:
    """Test suite for DataProcessingNode."""
    
    @pytest.fixture
    def node(self):
        """Create node instance for testing."""
        return DataProcessingNode()
    
    @pytest.fixture
    def shared_store(self):
        """Create shared store with test data."""
        return SharedStore({
            'input_data': ['item1', 'item2', 'item3'],
            'node_config': {'batch_size': 10, 'timeout': 30}
        })
    
    def test_prep_success(self, node, shared_store):
        """Test successful preparation."""
        result = node.prep(shared_store)
        
        assert result is None  # Should continue to exec
        assert shared_store['processing_started'] is True
        assert 'node_config' in shared_store
    
    def test_prep_missing_input(self, node):
        """Test preparation with missing input."""
        empty_store = SharedStore({})
        
        result = node.prep(empty_store)
        
        assert result == "error"
    
    @patch.object(DataProcessingNode, 'process_data')
    def test_exec_success(self, mock_process, node, shared_store):
        """Test successful execution."""
        # Mock the processing method
        mock_process.return_value = ['result1', 'result2']
        
        result = node.exec(shared_store)
        
        assert result is None  # Success
        assert 'processed_results' in shared_store
        assert shared_store['processed_results'] == ['result1', 'result2']
        assert 'processed_timestamp' in shared_store
    
    @patch.object(DataProcessingNode, 'process_data')
    def test_exec_failure(self, mock_process, node, shared_store):
        """Test execution with processing failure."""
        # Mock processing to raise exception
        mock_process.side_effect = Exception("Processing failed")
        
        result = node.exec(shared_store)
        
        assert result == "error"
        assert 'error_details' in shared_store
        assert shared_store['error_details']['error'] == "Processing failed"
```

### Flow Testing
```python
class TestDocumentProcessingFlow:
    """Test suite for DocumentProcessingFlow."""
    
    @pytest.fixture
    def flow(self):
        """Create flow instance for testing."""
        return DocumentProcessingFlow()
    
    def test_flow_setup(self, flow):
        """Test flow configuration."""
        config = flow.setup_flow()
        
        # Check node definitions
        assert 'fetch_documents' in config
        assert isinstance(config['fetch_documents'], FetchDocumentsNode)
        
        # Check flow routing
        assert 'flow' in config
        assert config['flow']['start'] == 'fetch_documents'
    
    @pytest.mark.asyncio
    async def test_flow_execution_success(self, flow):
        """Test successful flow execution."""
        initial_store = SharedStore({
            'document_urls': ['http://example.com/doc1.pdf'],
            'processing_config': {'batch_size': 5}
        })
        
        final_store = await flow.run(initial_store)
        
        assert 'final_results' in final_store
        assert final_store['processing_status'] == 'completed'
    
    @pytest.mark.asyncio
    async def test_flow_execution_with_errors(self, flow):
        """Test flow execution with error handling."""
        initial_store = SharedStore({
            # Missing required data to trigger error path
        })
        
        final_store = await flow.run(initial_store)
        
        assert 'error_details' in final_store
        assert final_store.get('processing_status') == 'failed'
```

## Performance Optimization

### Memory Management
```python
class EfficientProcessingNode(Node):
    """Node optimized for memory usage."""
    
    def exec(self, shared_store: SharedStore) -> Optional[str]:
        """Process data with memory optimization."""
        
        # Process data in chunks to avoid memory issues
        chunk_size = 1000
        input_data = shared_store['large_dataset']
        results = []
        
        for i in range(0, len(input_data), chunk_size):
            chunk = input_data[i:i + chunk_size]
            
            # Process chunk
            chunk_results = self.process_chunk(chunk)
            results.extend(chunk_results)
            
            # Clean up chunk data to free memory
            del chunk, chunk_results
            
            # Yield control periodically
            if i % (chunk_size * 10) == 0:
                await asyncio.sleep(0.01)
        
        shared_store['processed_results'] = results
        
        # Clean up input data if no longer needed
        if shared_store.get('cleanup_input', True):
            del shared_store['large_dataset']
        
        return None
```

### Async Optimization
```python
class OptimizedAsyncNode(Node):
    """Node with async optimizations."""
    
    async def exec_async(self, shared_store: SharedStore) -> Optional[str]:
        """Execute with async optimizations."""
        
        items = shared_store['items']
        
        # Use semaphore to limit concurrent operations
        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent
        
        async def process_with_semaphore(item):
            async with semaphore:
                return await self.process_item(item)
        
        # Process all items concurrently but controlled
        tasks = [process_with_semaphore(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results and exceptions
        successful_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error("Item processing failed", error=str(result))
            else:
                successful_results.append(result)
        
        shared_store['processed_results'] = successful_results
        return None
    
    async def process_item(self, item):
        """Process individual item asynchronously."""
        # Implementation here
        pass
```