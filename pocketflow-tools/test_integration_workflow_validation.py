#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test to verify pre-generation checks work in actual workflow generation.
"""

import sys
import logging
from pathlib import Path
from io import StringIO

# Add the parent directory to the path to import from pocketflow_tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from pocketflow_tools.spec import WorkflowSpec
from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator


def test_workflow_generation_with_warnings():
    """Test that warnings are logged during actual workflow generation."""
    print("\n🧪 Testing Integration: Pre-Generation Checks in Workflow Generation")
    print("=" * 70)
    
    # Create a spec that should trigger both warnings
    spec_data = {
        "name": "TestWorkflow",
        "pattern": "WORKFLOW",
        "description": "Test workflow with potential issues",
        "nodes": [
            {"name": "ProcessFiles", "type": "Node", "description": "Process multiple documents and files"}
        ],
        "utilities": [
            {"name": "read_file", "description": "Read file from disk"},
            {"name": "save_csv", "description": "Save data to CSV file"}
        ]
    }
    
    spec = WorkflowSpec(**spec_data)
    
    # Set up logging capture
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.WARNING)
    
    logger = logging.getLogger('pocketflow_tools.generators.workflow_composer')
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    
    try:
        # Generate workflow (which should trigger our pre-generation checks)
        generator = PocketFlowGenerator()
        output_files = generator.generate_workflow(spec)
        
        # Check that files were generated
        print(f"✅ Generated {len(output_files)} workflow files")
        
        # Check logged warnings
        log_output = log_capture.getvalue()
        
        if "Pre-generation validation found potential issues" in log_output:
            print("✅ Pre-generation validation warnings were logged")
            
            if "BatchNode for collection processing" in log_output:
                print("✅ Collection processing warning detected")
            else:
                print("❌ Collection processing warning NOT detected")
                
            if "simple I/O operations to node prep()" in log_output:
                print("✅ Trivial utilities warning detected")
            else:
                print("❌ Trivial utilities warning NOT detected")
                
        else:
            print("❌ No pre-generation validation warnings found in logs")
            print("Log output:")
            print(log_output)
            
    except Exception as e:
        print(f"❌ Workflow generation failed: {e}")
    finally:
        logger.removeHandler(handler)


if __name__ == "__main__":
    test_workflow_generation_with_warnings()
    print("\n✨ Integration Test Complete")