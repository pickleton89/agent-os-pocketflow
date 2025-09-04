#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the workflow generator without external dependencies.
"""

import sys
from pathlib import Path

# Ensure repository root is on sys.path so the package is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from pocketflow_tools.spec import WorkflowSpec
    from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator

    print("+ Generator module imported successfully")
except ImportError as e:
    print(f"- Failed to import pocketflow_tools: {e}")
    sys.exit(1)


def test_workflow_spec():
    """Test WorkflowSpec creation."""
    print("\nTesting WorkflowSpec...")

    spec = WorkflowSpec(
        name="TestWorkflow",
        pattern="WORKFLOW",
        description="Test workflow for validation",
        nodes=[{"name": "TestNode", "type": "Node", "description": "Test node"}],
        utilities=[
            {
                "name": "test_utility",
                "description": "Test utility function",
                "parameters": [{"name": "input", "type": "str", "optional": False}],
                "return_type": "str",
            }
        ],
        shared_store_schema={"input_data": "str", "output_data": "str"},
        fast_api_integration=False,
    )

    print(f"+ Created WorkflowSpec: {spec.name}")
    print(f"  Pattern: {spec.pattern}")
    print(f"  Nodes: {len(spec.nodes)}")
    print(f"  Utilities: {len(spec.utilities)}")

    return spec


def test_smart_pattern_detection():
    """Test smart pattern detection for batch processing suggestions."""
    print("\nTesting Smart Pattern Detection...")

    # Create test specs with different batch processing indicators
    test_cases = [
        {
            "name": "ProcessFiles", 
            "description": "Process multiple files from input directory",
            "expected_indicators": ["plural noun in name", "collection-related keywords", "explicit multiple item mentions"]
        },
        {
            "name": "DataAnalyzer",
            "description": "Analyze datasets and generate reports", 
            "expected_indicators": ["collection-related keywords"]
        },
        {
            "name": "DocumentLoader",
            "description": "Load and parse each document in the collection",
            "expected_indicators": ["collection-related keywords", "explicit multiple item mentions"]
        },
        {
            "name": "SimpleProcessor", 
            "description": "Process single input",
            "expected_indicators": []  # Should not trigger batch suggestions
        },
        # Additional edge cases
        {
            "name": "ProcessSuccess",  # Should NOT be detected as plural (false positive test)
            "description": "Handle successful completion",
            "expected_indicators": []
        },
        {
            "name": "DataSources",  # Should be detected as plural
            "description": "Connect to various data sources",
            "expected_indicators": ["plural noun in name", "collection-related keywords", "explicit multiple item mentions"]
        }
    ]

    generator = PocketFlowGenerator(output_path="/tmp/test_pattern_detection")
    all_tests_passed = True
    
    for i, test_case in enumerate(test_cases):
        print(f"\n  Test case {i+1}: {test_case['name']}")
        print(f"    Description: '{test_case['description']}'")
        
        spec = WorkflowSpec(
            name=f"TestWorkflow{i+1}",
            pattern="WORKFLOW", 
            description="Test workflow for pattern detection",
            nodes=[{
                "name": test_case["name"],
                "type": "Node", 
                "description": test_case["description"]
            }],
            utilities=[],
            shared_store_schema={},
            fast_api_integration=False,
        )
        
        # Apply pattern detection
        detected_spec = generator._detect_batch_patterns(spec)
        
        # Check if framework_reminders were added correctly
        node = detected_spec.nodes[0]
        framework_reminders = node.get('framework_reminders', [])
        has_batch_guidance = any("SMART PATTERN DETECTION" in reminder for reminder in framework_reminders)
        
        expected_batch_guidance = len(test_case['expected_indicators']) > 0
        
        # Verify overall detection
        if has_batch_guidance == expected_batch_guidance:
            print(f"    ✓ Pattern detection {'detected' if has_batch_guidance else 'correctly ignored'} batch indicators")
        else:
            print(f"    ✗ Expected batch guidance: {expected_batch_guidance}, Got: {has_batch_guidance}")
            all_tests_passed = False
            continue
            
        # If we expected indicators, verify the specific ones
        if has_batch_guidance and test_case['expected_indicators']:
            indicators_comment = next(
                (r for r in framework_reminders if 'Detected indicators:' in r), 
                None
            )
            
            if indicators_comment:
                detected_indicators = indicators_comment.split('Detected indicators: ')[1]
                print(f"    ✓ {indicators_comment}")
                
                # Verify each expected indicator is present
                missing_indicators = []
                for expected_indicator in test_case['expected_indicators']:
                    if expected_indicator not in detected_indicators:
                        missing_indicators.append(expected_indicator)
                
                if missing_indicators:
                    print(f"    ✗ Missing expected indicators: {', '.join(missing_indicators)}")
                    all_tests_passed = False
                else:
                    print("    ✓ All expected indicators found")
            else:
                print("    ✗ Expected indicators comment not found in framework_reminders")
                all_tests_passed = False

    # Test edge cases for robustness
    print("\n  Testing edge cases...")
    
    # Test with empty spec
    empty_spec = WorkflowSpec(name="Empty", pattern="WORKFLOW", description="", nodes=[], utilities=[], shared_store_schema={}, fast_api_integration=False)
    result = generator._detect_batch_patterns(empty_spec)
    if result == empty_spec:
        print("    ✓ Handles empty spec correctly")
    else:
        print("    ✗ Failed to handle empty spec")
        all_tests_passed = False
    
    # Test with malformed node
    malformed_spec = WorkflowSpec(
        name="Malformed", pattern="WORKFLOW", description="", 
        nodes=[{"name": "", "description": None}],  # Missing/invalid data
        utilities=[], shared_store_schema={}, fast_api_integration=False
    )
    try:
        result = generator._detect_batch_patterns(malformed_spec)
        print("    ✓ Handles malformed nodes gracefully")
    except Exception as e:
        print(f"    ✗ Failed on malformed nodes: {e}")
        all_tests_passed = False

    print(f"\n+ Smart pattern detection test {'completed successfully' if all_tests_passed else 'completed with failures'}")
    return all_tests_passed


def test_generator():
    """Test PocketFlowGenerator."""
    print("\nTesting PocketFlowGenerator...")

    try:
        generator = PocketFlowGenerator()
        print("+ Generator created successfully")

        # Check if templates are loaded
        print(f"  Templates loaded: {list(generator.templates.keys())}")

        return generator
    except Exception as e:
        print(f"- Generator creation failed: {e}")
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
        print(f"    + Design doc generated ({len(design_doc)} chars)")

        print("  Testing Pydantic models generation...")
        models = generator._generate_pydantic_models(spec)
        print(f"    + Models generated ({len(models)} chars)")

        print("  Testing nodes generation...")
        nodes = generator._generate_nodes(spec)
        print(f"    + Nodes generated ({len(nodes)} chars)")

        print("  Testing flow generation...")
        flow = generator._generate_flow(spec)
        print(f"    + Flow generated ({len(flow)} chars)")

        print("  Testing utility generation...")
        utility = generator._generate_utility(spec.utilities[0])
        print(f"    + Utility generated ({len(utility)} chars)")

        print("+ All generation methods working")
        return True

    except Exception as e:
        print(f"- Generation failed: {e}")
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

        print("+ Complete workflow generated")
        print(f"  Generated files: {len(output_files)}")

        for file_path in sorted(output_files.keys()):
            print(f"    - {file_path}")

        # Test a few key files
        key_files = ["docs/design.md", "nodes.py", "flow.py", "schemas/models.py"]
        for key_file in key_files:
            if key_file in output_files:
                content = output_files[key_file]
                print(f"    + {key_file} ({len(content)} chars)")
            else:
                print(f"    - Missing {key_file}")

        return True

    except Exception as e:
        print(f"- Complete workflow generation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Testing PocketFlow Workflow Generator")
    print("=" * 40)

    tests = [test_workflow_spec, test_generator, test_smart_pattern_detection, test_generation, test_full_workflow]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"- Test {test.__name__} failed with exception: {e}")

    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("+ All tests passed!")
        return 0
    else:
        print("- Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
