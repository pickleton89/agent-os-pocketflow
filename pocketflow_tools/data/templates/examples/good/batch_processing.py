"""
Good Example: Batch Processing with PocketFlow

This example demonstrates the correct way to implement batch processing
using BatchNode and AsyncParallelBatchNode for efficient collection handling.
"""

from typing import Dict, Any, Optional
from pocketflow import SharedStore, BatchNode, AsyncParallelBatchNode
import asyncio


class DocumentBatchProcessor(BatchNode):
    """
    ✅ CORRECT: BatchNode for processing collections efficiently
    
    This node demonstrates proper batch processing patterns:
    - Single responsibility: only processes documents
    - Uses BatchNode for collection operations
    - Proper error handling with partial failure support
    - Clear batch statistics tracking
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare batch processing parameters and validate input."""
        documents = shared.get('documents', [])
        batch_size = shared.get('batch_size', 5)
        
        if not documents:
            raise ValueError("No documents provided for processing")
        
        # Validate batch size
        if batch_size <= 0:
            batch_size = 5
            
        return {
            'documents': documents,
            'batch_size': batch_size,
            'total_documents': len(documents)
        }
    
    def exec(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process documents in batches with proper error handling."""
        documents = prep_result['documents']
        batch_size = prep_result['batch_size']
        
        # Split into batches
        batches = [
            documents[i:i + batch_size] 
            for i in range(0, len(documents), batch_size)
        ]
        
        processed_results = []
        failed_batches = []
        
        for i, batch in enumerate(batches):
            try:
                self.logger.info(f"Processing batch {i+1}/{len(batches)}")
                
                # Process each document in the batch
                batch_results = []
                for doc in batch:
                    processed_doc = self._process_single_document(doc)
                    batch_results.append(processed_doc)
                
                processed_results.extend(batch_results)
                
                # Small delay to avoid overwhelming downstream systems
                if i < len(batches) - 1:
                    asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(
                    f"Batch {i+1} failed: {str(e)}",
                    extra={'batch_size': len(batch), 'batch_index': i}
                )
                failed_batches.append(i)
        
        return {
            'processed_results': processed_results,
            'batch_stats': {
                'total_batches': len(batches),
                'successful_batches': len(batches) - len(failed_batches),
                'failed_batches': failed_batches,
                'success_rate': len(processed_results) / len(documents)
            }
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Store results and determine next action based on success rate."""
        shared['processed_documents'] = exec_result['processed_results']
        shared['batch_statistics'] = exec_result['batch_stats']
        
        success_rate = exec_result['batch_stats']['success_rate']
        
        # Route based on success rate
        if success_rate < 0.5:  # Less than 50% success
            return "critical_failure"
        elif success_rate < 0.9:  # Less than 90% success
            return "partial_failure"
        
        return None  # Complete success
    
    def _process_single_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single document. This is a pure function with no side effects."""
        # Example processing: extract metadata and content
        processed = {
            'id': document.get('id', 'unknown'),
            'processed_content': self._clean_content(document.get('content', '')),
            'metadata': {
                'word_count': len(document.get('content', '').split()),
                'processed_at': 'timestamp_placeholder'
            }
        }
        return processed
    
    def _clean_content(self, content: str) -> str:
        """Clean document content."""
        # Simple cleaning logic
        return content.strip().replace('\n\n', '\n')


class AsyncDocumentProcessor(AsyncParallelBatchNode):
    """
    ✅ CORRECT: AsyncParallelBatchNode for concurrent I/O operations
    
    This demonstrates parallel processing of items that require I/O operations
    like API calls, file operations, or database queries.
    """
    
    def prep(self, shared: SharedStore) -> Dict[str, Any]:
        """Prepare async processing parameters."""
        documents = shared.get('documents', [])
        max_concurrent = shared.get('max_concurrent', 3)
        
        return {
            'documents': documents,
            'max_concurrent': max_concurrent,
            'total_count': len(documents)
        }
    
    async def exec_async(self, prep_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process documents concurrently with controlled parallelism."""
        documents = prep_result['documents']
        max_concurrent = prep_result['max_concurrent']
        
        # Use semaphore to control concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(doc):
            async with semaphore:
                return await self._process_document_async(doc)
        
        # Process all documents concurrently
        tasks = [process_with_semaphore(doc) for doc in documents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Separate successful results from exceptions
        successful_results = []
        failed_count = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Document {i} failed: {str(result)}")
                failed_count += 1
            else:
                successful_results.append(result)
        
        return {
            'processed_documents': successful_results,
            'success_count': len(successful_results),
            'failure_count': failed_count,
            'total_count': len(documents)
        }
    
    def post(self, shared: SharedStore, prep_result: Dict[str, Any], exec_result: Dict[str, Any]) -> Optional[str]:
        """Store results and route based on success rate."""
        shared['async_processed_documents'] = exec_result['processed_documents']
        shared['processing_stats'] = {
            'success_count': exec_result['success_count'],
            'failure_count': exec_result['failure_count'],
            'success_rate': exec_result['success_count'] / exec_result['total_count']
        }
        
        success_rate = shared['processing_stats']['success_rate']
        
        if success_rate < 0.8:
            return "review_failures"
        
        return None
    
    async def _process_document_async(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Async processing of a single document (simulating I/O operations)."""
        # Simulate async I/O operation
        await asyncio.sleep(0.1)
        
        # Example: fetch additional data or call external API
        enhanced_doc = {
            'original_id': document.get('id'),
            'processed_content': document.get('content', '').upper(),
            'async_metadata': {
                'processing_time': '0.1s',
                'enhanced': True
            }
        }
        
        return enhanced_doc


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    # Example documents
    sample_documents = [
        {'id': 'doc1', 'content': 'First document content'},
        {'id': 'doc2', 'content': 'Second document content'},
        {'id': 'doc3', 'content': 'Third document content'},
        {'id': 'doc4', 'content': 'Fourth document content'},
        {'id': 'doc5', 'content': 'Fifth document content'},
    ]
    
    # Test synchronous batch processing
    print("=== Synchronous Batch Processing ===")
    shared = SharedStore({
        'documents': sample_documents,
        'batch_size': 2
    })
    
    processor = DocumentBatchProcessor()
    prep_result = processor.prep(shared)
    exec_result = processor.exec(prep_result)
    action = processor.post(shared, prep_result, exec_result)
    
    print(f"Processed {len(shared['processed_documents'])} documents")
    print(f"Batch statistics: {shared['batch_statistics']}")
    print(f"Next action: {action}")
    
    # Test asynchronous parallel processing
    async def test_async():
        print("\n=== Async Parallel Processing ===")
        shared_async = SharedStore({
            'documents': sample_documents,
            'max_concurrent': 3
        })
        
        async_processor = AsyncDocumentProcessor()
        prep_result = async_processor.prep(shared_async)
        exec_result = await async_processor.exec_async(prep_result)
        action = async_processor.post(shared_async, prep_result, exec_result)
        
        print(f"Async processed {len(shared_async['async_processed_documents'])} documents")
        print(f"Processing stats: {shared_async['processing_stats']}")
        print(f"Next action: {action}")
    
    asyncio.run(test_async())