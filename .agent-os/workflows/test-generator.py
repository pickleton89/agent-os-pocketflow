#!/usr/bin/env python3
"""
Test script for the workflow generator without external dependencies.
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from generator import WorkflowSpec, PocketFlowGenerator
    print("✓ Generator module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import generator: {e}")
    sys.exit(1)

def test_workflow_spec():
    """Test WorkflowSpec creation."""
    print("\nTesting WorkflowSpec...")
    
    spec = WorkflowSpec(
        name="TestWorkflow",
        pattern="WORKFLOW",
        description="Test workflow for validation",
        nodes=[
            {
                "name": "TestNode",
                "type": "Node",
                "description": "Test node"
            }
        ],
        utilities=[
            {
                "name": "test_utility",
                "description": "Test utility function",
                "parameters": [{"name": "input", "type": "str", "optional": False}],
                "return_type": "str"
            }
        ],
        shared_store_schema={
            "input_data": "str",
            "output_data": "str"
        },
        fast_api_integration=False
    )
    
    print(f"✓ Created WorkflowSpec: {spec.name}")
    print(f"  Pattern: {spec.pattern}")
    print(f"  Nodes: {len(spec.nodes)}")
    print(f"  Utilities: {len(spec.utilities)}")
    
    return spec

def test_generator():
    """Test PocketFlowGenerator."""
    print("\nTesting PocketFlowGenerator...")
    
    try:
        generator = PocketFlowGenerator()
        print("✓ Generator created successfully")
        
        # Check if templates are loaded
        print(f"  Templates loaded: {list(generator.templates.keys())}")
        
        return generator
    except Exception as e:
        print(f"✗ Generator creation failed: {e}")
        return None

def test_generation():
    """Test workflow generation."""
    print("\nTesting workflow generation...")
    
    spec = test_workflow_spec()
    generator = test_generator()
    
    if not generator:
        return False
    
    try:
        # Test individual generation methods
        print("  Testing design doc generation...")
        design_doc = generator._generate_design_doc(spec)
        print(f"    ✓ Design doc generated ({len(design_doc)} chars)")
        
        print("  Testing Pydantic models generation...")
        models = generator._generate_pydantic_models(spec)
        print(f"    ✓ Models generated ({len(models)} chars)")
        
        print("  Testing nodes generation...")
        nodes = generator._generate_nodes(spec)
        print(f"    ✓ Nodes generated ({len(nodes)} chars)")
        
        print("  Testing flow generation...")
        flow = generator._generate_flow(spec)
        print(f"    ✓ Flow generated ({len(flow)} chars)")
        
        print("  Testing utility generation...")
        utility = generator._generate_utility(spec.utilities[0])
        print(f"    ✓ Utility generated ({len(utility)} chars)")
        
        print("✓ All generation methods working")
        return True
        
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_workflow():
    """Test complete workflow generation."""
    print("\nTesting complete workflow generation...")
    
    spec = test_workflow_spec()
    generator = test_generator()
    
    if not generator:
        return False
    
    try:
        output_files = generator.generate_workflow(spec)
        
        print("✓ Complete workflow generated")
        print(f"  Generated files: {len(output_files)}")
        
        for file_path in sorted(output_files.keys()):
            print(f"    - {file_path}")
        
        # Test a few key files
        key_files = ["docs/design.md", "nodes.py", "flow.py", "schemas/models.py"]
        for key_file in key_files:
            if key_file in output_files:
                content = output_files[key_file]
                print(f"    ✓ {key_file} ({len(content)} chars)")
            else:
                print(f"    ✗ Missing {key_file}")
        
        return True
        
    except Exception as e:
        print(f"✗ Complete workflow generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Testing PocketFlow Workflow Generator")
    print("=" * 40)
    
    tests = [
        test_workflow_spec,
        test_generator,
        test_generation,
        test_full_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())