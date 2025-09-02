#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Pattern Analyzer Agent integration
"""

import logging
from pathlib import Path
from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_pattern_recognizer():
    """Test the pattern recognizer with various requirement scenarios."""
    
    # Test scenarios
    test_cases = [
        {
            "name": "DocumentSearchRAG",
            "requirements": "I need to build a document search system that can find relevant information from a knowledge base using semantic search and vector embeddings to provide accurate answers to user questions"
        },
        {
            "name": "IntelligentAgent", 
            "requirements": "Create an intelligent agent that can analyze customer requests, make autonomous decisions, and plan multi-step workflows to resolve complex business problems"
        },
        {
            "name": "APIIntegration",
            "requirements": "Build a system that integrates with multiple external APIs, processes data from different sources, and provides a unified REST API interface for clients"
        },
        {
            "name": "DataProcessingWorkflow",
            "requirements": "I want a structured workflow that processes large datasets through multiple sequential stages with validation and error handling"
        }
    ]
    
    # Initialize generator
    generator = PocketFlowGenerator(
        templates_path="templates",  # Will fail gracefully if templates don't exist
        output_path=".agent-os/workflows"
    )
    
    print("Testing Pattern Analyzer Agent Integration")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\nTest Case: {test_case['name']}")
        print("-" * 40)
        print(f"Requirements: {test_case['requirements'][:100]}...")
        
        try:
            # Test the pattern analysis
            recommendation = generator.request_pattern_analysis(test_case['requirements'])
            
            print(f"Pattern Analysis Successful:")
            print(f"   Primary Pattern: {recommendation.primary_pattern}")
            print(f"   Confidence: {recommendation.confidence_score:.2f}")
            print(f"   Secondary Patterns: {recommendation.secondary_patterns}")
            print(f"   Rationale: {recommendation.rationale}")
            
            # Test spec generation
            spec = generator.generate_spec_from_analysis(
                test_case['name'], 
                test_case['requirements'], 
                recommendation
            )
            
            print(f"Spec Generation Successful:")
            print(f"   Pattern: {spec.pattern}")
            print(f"   Nodes: {len(spec.nodes)}")
            print(f"   Utilities: {len(spec.utilities)}")
            print(f"   FastAPI: {spec.fast_api_integration}")
            
            print(f"Node Architecture:")
            for i, node in enumerate(spec.nodes, 1):
                print(f"   {i}. {node['name']} ({node['type']}) - {node['description']}")
            
            print(f"Utility Functions:")
            for utility in spec.utilities:
                print(f"   - {utility['name']}: {utility['description']}")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Pattern Analyzer Testing Complete!")

def test_full_generation():
    """Test full workflow generation from requirements."""
    
    print("\nTesting Full Workflow Generation")
    print("=" * 60)
    
    # Initialize generator
    generator = PocketFlowGenerator(
        templates_path="templates",  # Will fail gracefully if templates don't exist
        output_path=".agent-os/workflows"
    )
    
    # Test case for full generation
    test_case = {
        "name": "SmartDocumentProcessor",
        "requirements": """
        Create a document processing system that can:
        1. Accept PDF documents and extract text content
        2. Use AI to analyze and categorize the documents 
        3. Store processed documents with metadata in a vector database
        4. Provide REST API endpoints for document upload and search
        5. Return relevant documents based on semantic similarity queries
        """
    }
    
    try:
        print(f"Generating: {test_case['name']}")
        print(f"Requirements: {test_case['requirements']}")
        
        # Generate complete workflow
        workflow_files = generator.generate_workflow_from_requirements(
            test_case['name'],
            test_case['requirements']
        )
        
        print(f"\nGenerated Files ({len(workflow_files)}):")
        for file_path in sorted(workflow_files.keys()):
            file_size = len(workflow_files[file_path])
            print(f"   {file_path} ({file_size} bytes)")
        
        # Show a sample of the design document
        if "docs/design.md" in workflow_files:
            design_content = workflow_files["docs/design.md"]
            print(f"\nDesign Document Preview:")
            print("-" * 40)
            lines = design_content.split('\n')
            for line in lines[:25]:  # First 25 lines
                print(line)
            if len(lines) > 25:
                print("... (truncated)")
        
        print(f"\nFull generation successful!")
        
    except Exception as e:
        print(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pattern_recognizer()
    test_full_generation()
