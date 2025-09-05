# Migration Guide: Monolithic to Focused Nodes

**Antipattern**: Monolithic Node Syndrome  
**Severity**: 🔴 Critical  
**Time Estimate**: 2-4 hours  
**Risk Level**: Medium (requires architectural changes)

## Problem Description

Monolithic nodes handle multiple distinct responsibilities in a single `exec()` method, making them hard to test, debug, and reuse. Common signs include:

- `exec()` methods longer than 20 lines
- Multiple LLM calls in a single method
- Class names with multiple verbs (ProcessAndValidateNode, FetchParseStoreNode)
- Mixed concerns (validation + processing + formatting)

## Detecting the Problem

### Automated Detection
```bash
# Run antipattern detector
python pocketflow-tools/antipattern_detector.py your_code/

# Look for these violations:
# - "Method too long (X lines)"
# - "Multiple LLM calls (X) suggest multiple responsibilities"  
# - "Class name suggests multiple responsibilities"
```

### Manual Inspection
Look for these patterns in your code:

```python
# 🚨 ANTIPATTERN EXAMPLE
class ProcessAndValidateDocumentNode(Node):
    def exec(self, prep_result):
        # Multiple responsibilities in one method
        documents = prep_result['documents']
        
        # Responsibility 1: Parse documents
        parsed_docs = []
        for doc in documents:
            if doc.type == 'pdf':
                content = extract_pdf_text(doc.path)
            elif doc.type == 'docx':
                content = extract_docx_text(doc.path)
            else:
                content = doc.content
            parsed_docs.append(content)
        
        # Responsibility 2: Validate content  
        validated_docs = []
        for content in parsed_docs:
            validation_result = call_llm_validator(content)
            if validation_result.is_valid:
                validated_docs.append(content)
        
        # Responsibility 3: Process content
        processed_docs = []
        for content in validated_docs:
            summary = call_llm_summarizer(content)
            processed_docs.append(summary)
        
        # Responsibility 4: Format output
        return {
            'summaries': processed_docs,
            'total_processed': len(processed_docs),
            'success_rate': len(processed_docs) / len(documents)
        }
```

## Migration Steps

### Step 1: Identify Responsibilities (30 minutes)

Analyze your monolithic node and list distinct responsibilities:

```python
# Example analysis for ProcessAndValidateDocumentNode:
# 1. Document parsing (PDF, DOCX extraction)
# 2. Content validation (LLM validation)  
# 3. Content processing (LLM summarization)
# 4. Output formatting

# Each responsibility should become a separate node
```

### Step 2: Design the New Flow (45 minutes)

Create a flow diagram showing how responsibilities will be split:

```yaml
# New flow design:
# documents -> ParseDocumentsNode -> ValidateContentNode -> ProcessContentNode -> FormatOutputNode -> results

flow_design:
  nodes:
    - name: ParseDocumentsNode
      input: raw_documents
      output: parsed_content
      
    - name: ValidateContentNode  
      input: parsed_content
      output: valid_content
      
    - name: ProcessContentNode
      input: valid_content
      output: processed_summaries
      
    - name: FormatOutputNode
      input: processed_summaries
      output: formatted_results
```

### Step 3: Create Focused Nodes (90 minutes)

Extract each responsibility into a dedicated node:

```python
# ✅ FOCUSED NODES
class ParseDocumentsNode(Node):
    """Single responsibility: Parse different document formats"""
    
    def exec(self, prep_result):
        documents = prep_result['documents']
        parsed_docs = []
        
        for doc in documents:
            if doc.type == 'pdf':
                content = extract_pdf_text(doc.path)
            elif doc.type == 'docx':
                content = extract_docx_text(doc.path)
            else:
                content = doc.content
            parsed_docs.append(content)
        
        return {'parsed_content': parsed_docs}


class ValidateContentNode(Node):
    """Single responsibility: Validate document content"""
    
    def exec(self, prep_result):
        parsed_content = prep_result['parsed_content']
        validated_docs = []
        
        for content in parsed_content:
            validation_result = call_llm_validator(content)
            if validation_result.is_valid:
                validated_docs.append(content)
        
        return {'valid_content': validated_docs}


class ProcessContentNode(Node):
    """Single responsibility: Process and summarize content"""
    
    def exec(self, prep_result):
        valid_content = prep_result['valid_content']
        processed_docs = []
        
        for content in valid_content:
            summary = call_llm_summarizer(content)
            processed_docs.append(summary)
        
        return {'summaries': processed_docs}


class FormatOutputNode(Node):
    """Single responsibility: Format final output"""
    
    def exec(self, prep_result):
        summaries = prep_result['summaries']
        original_count = prep_result.get('original_document_count', len(summaries))
        
        return {
            'summaries': summaries,
            'total_processed': len(summaries),
            'success_rate': len(summaries) / original_count if original_count > 0 else 0
        }
```

### Step 4: Update Flow Configuration (30 minutes)

Create a new flow that connects your focused nodes:

```python
# flows/document_processing_flow.py
from pocketflow import Flow
from .nodes import (
    ParseDocumentsNode,
    ValidateContentNode, 
    ProcessContentNode,
    FormatOutputNode
)

class DocumentProcessingFlow(Flow):
    def __init__(self):
        super().__init__()
        
        # Add nodes
        self.add_node("parse", ParseDocumentsNode())
        self.add_node("validate", ValidateContentNode())
        self.add_node("process", ProcessContentNode())
        self.add_node("format", FormatOutputNode())
        
        # Define flow
        self.add_edge("parse", "validate")
        self.add_edge("validate", "process")  
        self.add_edge("process", "format")
        
        # Pass through original count for success rate calculation
        self.add_data_flow("parse", "format", 
                          lambda result: {"original_document_count": len(result.get("documents", []))})
```

### Step 5: Update Shared Store Schema (15 minutes)

Ensure your shared store schema supports the new data flow:

```python
# schemas/document_processing_schema.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DocumentProcessingSharedStore(BaseModel):
    # Input data
    documents: List[Dict[str, Any]]
    
    # Intermediate results
    parsed_content: Optional[List[str]] = None
    valid_content: Optional[List[str]] = None
    summaries: Optional[List[str]] = None
    
    # Final results
    total_processed: Optional[int] = None
    success_rate: Optional[float] = None
    original_document_count: Optional[int] = None
```

### Step 6: Test Individual Nodes (45 minutes)

Create focused tests for each node:

```python
# tests/test_focused_nodes.py
import pytest
from unittest.mock import Mock, patch
from nodes.document_processing import (
    ParseDocumentsNode,
    ValidateContentNode,
    ProcessContentNode,
    FormatOutputNode
)

class TestParseDocumentsNode:
    def test_parse_mixed_documents(self):
        node = ParseDocumentsNode()
        
        # Mock documents
        documents = [
            Mock(type='pdf', path='/path/to/doc.pdf'),
            Mock(type='docx', path='/path/to/doc.docx'),
            Mock(type='txt', content='Plain text content')
        ]
        
        prep_result = {'documents': documents}
        
        with patch('nodes.document_processing.extract_pdf_text', return_value='PDF content'), \
             patch('nodes.document_processing.extract_docx_text', return_value='DOCX content'):
            
            result = node.exec(prep_result)
            
            assert result['parsed_content'] == [
                'PDF content',
                'DOCX content', 
                'Plain text content'
            ]
    
    def test_parse_empty_documents(self):
        node = ParseDocumentsNode()
        prep_result = {'documents': []}
        
        result = node.exec(prep_result)
        assert result['parsed_content'] == []


class TestValidateContentNode:
    def test_validate_mixed_content(self):
        node = ValidateContentNode()
        prep_result = {'parsed_content': ['good content', 'bad content', 'ok content']}
        
        with patch('nodes.document_processing.call_llm_validator') as mock_validator:
            mock_validator.side_effect = [
                Mock(is_valid=True),   # good content
                Mock(is_valid=False),  # bad content  
                Mock(is_valid=True),   # ok content
            ]
            
            result = node.exec(prep_result)
            assert result['valid_content'] == ['good content', 'ok content']


class TestProcessContentNode:
    def test_process_content(self):
        node = ProcessContentNode()
        prep_result = {'valid_content': ['content 1', 'content 2']}
        
        with patch('nodes.document_processing.call_llm_summarizer') as mock_summarizer:
            mock_summarizer.side_effect = ['summary 1', 'summary 2']
            
            result = node.exec(prep_result)
            assert result['summaries'] == ['summary 1', 'summary 2']


class TestFormatOutputNode:
    def test_format_output_with_success_rate(self):
        node = FormatOutputNode()
        prep_result = {
            'summaries': ['summary 1', 'summary 2'],
            'original_document_count': 3
        }
        
        result = node.exec(prep_result)
        
        assert result['summaries'] == ['summary 1', 'summary 2']
        assert result['total_processed'] == 2
        assert result['success_rate'] == pytest.approx(0.6667, abs=0.001)
```

### Step 7: Integration Testing (30 minutes)

Test the complete flow:

```python
# tests/test_document_processing_flow.py
import pytest
from unittest.mock import Mock, patch
from flows.document_processing_flow import DocumentProcessingFlow

class TestDocumentProcessingFlow:
    def test_complete_flow(self):
        flow = DocumentProcessingFlow()
        
        # Mock input data
        input_data = {
            'documents': [
                Mock(type='txt', content='Document 1 content'),
                Mock(type='txt', content='Document 2 content'),
            ]
        }
        
        with patch('nodes.document_processing.call_llm_validator') as mock_validator, \
             patch('nodes.document_processing.call_llm_summarizer') as mock_summarizer:
            
            mock_validator.return_value = Mock(is_valid=True)
            mock_summarizer.side_effect = ['Summary 1', 'Summary 2']
            
            result = flow.run(input_data)
            
            assert 'summaries' in result
            assert result['total_processed'] == 2
            assert result['success_rate'] == 1.0
```

## Risk Mitigation

### Common Issues and Solutions

**Issue**: Data flow between nodes breaks
```python
# Problem: Missing data in prep_result
def exec(self, prep_result):
    # KeyError: 'expected_key'
    data = prep_result['expected_key']

# Solution: Check data availability and add error handling
def exec(self, prep_result):
    if 'expected_key' not in prep_result:
        raise ValueError(f"Missing required data: expected_key. Available keys: {list(prep_result.keys())}")
    data = prep_result['expected_key']
```

**Issue**: Performance degradation from multiple nodes
```python
# Monitor execution time
import time

def exec(self, prep_result):
    start_time = time.time()
    result = process_data(prep_result)
    execution_time = time.time() - start_time
    
    # Log slow operations
    if execution_time > 1.0:
        logger.warning(f"Slow execution in {self.__class__.__name__}: {execution_time:.2f}s")
    
    return result
```

**Issue**: Shared state between nodes
```python
# Problem: Nodes accidentally sharing mutable state
class BadNode(Node):
    cache = {}  # ❌ Shared class variable
    
    def exec(self, prep_result):
        self.cache[key] = value  # Affects other instances

# Solution: Use instance variables or shared store
class GoodNode(Node):
    def __init__(self):
        super().__init__()
        self.cache = {}  # ✅ Instance variable
```

### Rollback Plan

If issues arise during migration:

1. **Immediate rollback**: `git checkout pre-migration-backup`
2. **Partial rollback**: Keep working nodes, revert problematic ones
3. **Hybrid approach**: Use new nodes alongside old monolithic node temporarily

### Monitoring After Migration

```python
# Add monitoring to new nodes
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MonitoredNode(Node):
    def exec(self, prep_result):
        start_time = datetime.now()
        
        try:
            result = self._do_exec(prep_result)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"{self.__class__.__name__} completed in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"{self.__class__.__name__} failed after {execution_time:.2f}s: {e}")
            raise
    
    def _do_exec(self, prep_result):
        # Override this method with your logic
        raise NotImplementedError
```

## Success Criteria

✅ **Code Quality**
- Each node has a single, clear responsibility
- `exec()` methods are under 15 lines
- No multiple LLM calls in single methods
- Clear, descriptive class names

✅ **Testing**
- Each node is independently testable
- 90%+ test coverage on focused nodes
- Integration tests pass
- Performance is maintained or improved

✅ **Maintainability**  
- New features can be added as new nodes
- Changes to one responsibility don't affect others
- Code is easier to debug and understand
- Documentation is clear

## Time Estimates by Complexity

| Original Node Complexity | Responsibilities | Estimated Time |
|--------------------------|------------------|----------------|
| Simple (2-3 responsibilities) | 2-3 nodes | 2-3 hours |
| Medium (4-5 responsibilities) | 4-5 nodes | 3-4 hours |  
| Complex (6+ responsibilities) | 6+ nodes | 4+ hours |

Add 50% buffer time for:
- Complex data flows
- Extensive test suites  
- Integration issues
- Performance optimization

## Related Guides

After completing this migration, you may also need:

- [Remove Shared Store from exec()](remove-shared-store-exec.md) - If nodes still access shared store directly
- [Fix Lifecycle Violations](fix-lifecycle-violations.md) - If prep/post methods need cleanup
- [Async Collection Processing](async-collection-processing.md) - If any nodes process collections