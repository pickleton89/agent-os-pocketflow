#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for pre-generation validation checks.
Validates Task 5.3 implementation of pre-generation checks functionality.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to the path to import from pocketflow_tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from pocketflow_tools.spec import WorkflowSpec
from pocketflow_tools.generators.workflow_composer import (
    has_collection_processing,
    uses_batch_nodes,
    has_trivial_utilities,
    pre_generation_check
)


def setup_logging():
    """Set up logging for test output."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )


def test_collection_processing_detection():
    """Test detection of collection processing patterns."""
    print("\n🧪 Testing Collection Processing Detection")
    print("=" * 50)
    
    test_cases = [
        # Positive cases - should detect collection processing
        ("Plural node names", {
            "name": "test",
            "pattern": "WORKFLOW", 
            "description": "test",
            "nodes": [
                {"name": "ProcessFiles", "type": "Node", "description": "Process multiple files"},
                {"name": "Validator", "type": "Node", "description": "Validate input"}
            ]
        }, True),
        
        ("Collection keywords", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test", 
            "nodes": [
                {"name": "DataProcessor", "type": "Node", "description": "Process documents and items"},
                {"name": "Analyzer", "type": "Node", "description": "Analyze results"}
            ]
        }, True),
        
        ("Explicit multiple mentions", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test",
            "nodes": [
                {"name": "Handler", "type": "Node", "description": "Handle multiple requests from various sources"}
            ]
        }, True),
        
        # Negative cases - should not detect collection processing
        ("No collection indicators", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test",
            "nodes": [
                {"name": "Processor", "type": "Node", "description": "Process single item"},
                {"name": "Validator", "type": "Node", "description": "Validate input"}
            ]
        }, False),
        
        ("False positive words (improved detection)", {
            "name": "test",
            "pattern": "WORKFLOW", 
            "description": "test",
            "nodes": [
                {"name": "ProcessRequest", "type": "Node", "description": "Process business request"},
                {"name": "AddressValidator", "type": "Node", "description": "Validate address format"},
                {"name": "StatusChecker", "type": "Node", "description": "Check system status"}
            ]
        }, False),
        
        ("Empty nodes", {
            "name": "test", 
            "pattern": "WORKFLOW",
            "description": "test",
            "nodes": []
        }, False)
    ]
    
    for test_name, spec_data, expected in test_cases:
        try:
            spec = WorkflowSpec(**spec_data)
            result = has_collection_processing(spec)
            status = "✅" if result == expected else "❌"
            print(f"{status} {test_name:35} | Expected: {str(expected):5} | Got: {str(result):5}")
        except Exception as e:
            print(f"❌ {test_name:35} | Error: {e}")


def test_batch_nodes_detection():
    """Test detection of BatchNode usage."""
    print("\n🧪 Testing BatchNode Usage Detection")
    print("=" * 50)
    
    test_cases = [
        # Positive cases - should detect batch nodes
        ("Has BatchNode", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test",
            "nodes": [
                {"name": "FileProcessor", "type": "BatchNode", "description": "Process files in batches"},
                {"name": "Validator", "type": "Node", "description": "Validate input"}
            ]
        }, True),
        
        ("Has AsyncBatchNode", {
            "name": "test",
            "pattern": "WORKFLOW", 
            "description": "test",
            "nodes": [
                {"name": "DataProcessor", "type": "AsyncBatchNode", "description": "Process data"},
            ]
        }, True),
        
        # Negative cases - should not detect batch nodes
        ("No batch nodes", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test", 
            "nodes": [
                {"name": "Processor", "type": "Node", "description": "Process item"},
                {"name": "AsyncProcessor", "type": "AsyncNode", "description": "Process async"}
            ]
        }, False),
        
        ("Empty nodes", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test",
            "nodes": []
        }, False)
    ]
    
    for test_name, spec_data, expected in test_cases:
        try:
            spec = WorkflowSpec(**spec_data)
            result = uses_batch_nodes(spec)
            status = "✅" if result == expected else "❌"
            print(f"{status} {test_name:25} | Expected: {str(expected):5} | Got: {str(result):5}")
        except Exception as e:
            print(f"❌ {test_name:25} | Error: {e}")


def test_trivial_utilities_detection():
    """Test detection of trivial utilities."""
    print("\n🧪 Testing Trivial Utilities Detection")
    print("=" * 50)
    
    test_cases = [
        # Positive cases - should detect predominantly trivial utilities
        ("Only simple file operations", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test",
            "utilities": [
                {"name": "read_file", "description": "Read file from disk"},
                {"name": "write_json", "description": "Write data to JSON file"}
            ]
        }, True),
        
        ("Basic I/O without complexity", {
            "name": "test", 
            "pattern": "WORKFLOW",
            "description": "test",
            "utilities": [
                {"name": "load_data", "description": "Load data from file"},
                {"name": "save_results", "description": "Save results to storage"}
            ]
        }, True),
        
        ("Mixed but trivial dominates", {
            "name": "test",
            "pattern": "WORKFLOW",
            "description": "test",
            "utilities": [
                {"name": "read_file", "description": "Read file from disk"},
                {"name": "write_json", "description": "Write data to JSON file"}, 
                {"name": "save_csv", "description": "Save data to CSV"},
                {"name": "llm_process", "description": "Apply LLM reasoning"}  # 1 complex vs 3 trivial
            ]
        }, True),
        
        # Negative cases - should not detect trivial utilities  
        ("Complex LLM utilities", {
            "name": "test",
            "pattern": "AGENT",
            "description": "test",
            "utilities": [
                {"name": "llm_reasoning", "description": "Apply LLM-based reasoning to analyze problems"},
                {"name": "process_data", "description": "Transform and analyze complex data"}
            ]
        }, False),
        
        ("Mixed but complex dominates", {
            "name": "test",
            "pattern": "AGENT",
            "description": "test",
            "utilities": [
                {"name": "read_file", "description": "Read file from disk"},
                {"name": "llm_reasoning", "description": "Apply LLM-based reasoning"},
                {"name": "ai_classify", "description": "Classify data using AI"}
            ]
        }, False),
        
        ("No utilities", {
            "name": "test",
            "pattern": "WORKFLOW", 
            "description": "test",
            "utilities": []
        }, False)
    ]
    
    for test_name, spec_data, expected in test_cases:
        try:
            spec = WorkflowSpec(**spec_data)
            result = has_trivial_utilities(spec)
            status = "✅" if result == expected else "❌"
            print(f"{status} {test_name:30} | Expected: {str(expected):5} | Got: {str(result):5}")
        except Exception as e:
            print(f"❌ {test_name:30} | Error: {e}")


def test_pre_generation_check_integration():
    """Test the complete pre-generation check system."""
    print("\n🧪 Testing Complete Pre-Generation Check System")
    print("=" * 50)
    
    test_cases = [
        # Should trigger collection processing warning
        ("Collection without BatchNode", {
            "name": "FileProcessor",
            "pattern": "WORKFLOW",
            "description": "Process multiple files",
            "nodes": [
                {"name": "ProcessFiles", "type": "Node", "description": "Process multiple documents"}
            ],
            "utilities": []
        }, ["BatchNode"], []),
        
        # Should trigger trivial utilities warning  
        ("Trivial utilities", {
            "name": "DataProcessor",
            "pattern": "WORKFLOW",
            "description": "Process data",
            "nodes": [
                {"name": "Processor", "type": "Node", "description": "Process single item"}
            ],
            "utilities": [
                {"name": "read_file", "description": "Read file from disk"}
            ]
        }, ["simple I/O"], []),
        
        # Should trigger both warnings
        ("Both issues", {
            "name": "MultiProcessor", 
            "pattern": "WORKFLOW",
            "description": "Process multiple files",
            "nodes": [
                {"name": "ProcessFiles", "type": "Node", "description": "Process documents and items"}
            ],
            "utilities": [
                {"name": "load_file", "description": "Load file data"}
            ]
        }, ["BatchNode", "simple I/O"], []),
        
        # Should trigger no warnings
        ("Clean spec", {
            "name": "SimpleProcessor",
            "pattern": "WORKFLOW", 
            "description": "Process data",
            "nodes": [
                {"name": "Processor", "type": "Node", "description": "Process single item"}
            ],
            "utilities": [
                {"name": "llm_analyze", "description": "Apply LLM analysis to complex data"}
            ]
        }, [], [])
    ]
    
    for test_name, spec_data, expected_warnings, expected_errors in test_cases:
        try:
            spec = WorkflowSpec(**spec_data)
            result = pre_generation_check(spec)
            
            warnings = result.get("warnings", [])
            errors = result.get("errors", [])
            
            warning_matches = all(any(keyword in warning for warning in warnings) for keyword in expected_warnings)
            error_matches = len(errors) == len(expected_errors)
            
            status = "✅" if warning_matches and error_matches else "❌"
            print(f"{status} {test_name:25} | Warnings: {len(warnings):2} | Errors: {len(errors):2}")
            
            # Show details for failed tests
            if not (warning_matches and error_matches):
                print(f"    Expected warning keywords: {expected_warnings}")
                print(f"    Actual warnings: {len(warnings)}")
                for warning in warnings:
                    print(f"      - {warning[:80]}...")
                    
        except Exception as e:
            print(f"❌ {test_name:25} | Error: {e}")


def main():
    """Run all pre-generation check tests."""
    setup_logging()
    
    print("🚀 Pre-Generation Validation Tests")
    print("=" * 60)
    print("Testing Task 5.3: Pre-Generation Checks Implementation")
    
    test_collection_processing_detection()
    test_batch_nodes_detection()
    test_trivial_utilities_detection() 
    test_pre_generation_check_integration()
    
    print("\n✨ Pre-Generation Check Tests Complete")


if __name__ == "__main__":
    main()