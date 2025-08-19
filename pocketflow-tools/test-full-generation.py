#!/usr/bin/env python3
"""
Comprehensive test of the workflow generation system.
Generates a complete workflow and validates its structure.
"""

import sys
import shutil
from pathlib import Path

# Add the current directory to the path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

# If running from project root, adjust path to find pocketflow-tools
if not Path("generator.py").exists() and Path("pocketflow-tools/generator.py").exists():
    sys.path.insert(0, str(Path("pocketflow-tools")))

from generator import WorkflowSpec, PocketFlowGenerator


def create_test_spec() -> WorkflowSpec:
    """Create a comprehensive test specification."""
    return WorkflowSpec(
        name="TestContentAnalyzer",
        pattern="RAG",
        description="Test content analyzer using RAG pattern for validation",
        fast_api_integration=True,
        nodes=[
            {
                "name": "DocumentRetrieverNode",
                "type": "AsyncNode",
                "description": "Retrieve relevant documents from vector store",
            },
            {
                "name": "ContextBuilderNode",
                "type": "Node",
                "description": "Build context from retrieved documents",
            },
            {
                "name": "LLMAnalyzerNode",
                "type": "AsyncNode",
                "description": "Analyze content using LLM with context",
            },
            {
                "name": "ResponseFormatterNode",
                "type": "Node",
                "description": "Format analysis results for response",
            },
        ],
        utilities=[
            {
                "name": "retrieve_documents",
                "description": "Retrieve documents from vector database",
                "parameters": [
                    {"name": "query", "type": "str", "optional": False},
                    {"name": "limit", "type": "int", "optional": True},
                ],
                "return_type": "List[Dict[str, Any]]",
            },
            {
                "name": "call_llm_analyzer",
                "description": "Call LLM for content analysis",
                "parameters": [
                    {"name": "context", "type": "str", "optional": False},
                    {"name": "query", "type": "str", "optional": False},
                ],
                "return_type": "str",
            },
        ],
        shared_store_schema={
            "input_query": "str",
            "retrieved_docs": "List[Dict[str, Any]]",
            "context": "str",
            "llm_response": "str",
            "analysis_result": "Dict[str, Any]",
            "timestamp": "datetime",
        },
        api_endpoints=[
            {
                "name": "AnalyzeContent",
                "method": "post",
                "path": "/analyze",
                "description": "Analyze content using RAG pattern",
                "request_fields": [
                    {"name": "query", "type": "str"},
                    {"name": "options", "type": "Optional[Dict[str, Any]]"},
                ],
                "response_fields": [
                    {"name": "analysis", "type": "Dict[str, Any]"},
                    {"name": "confidence", "type": "float"},
                    {"name": "sources", "type": "List[str]"},
                ],
            }
        ],
    )


def test_generation_and_save():
    """Test complete workflow generation and save to disk."""
    print("Testing complete workflow generation...")

    # Create test specification
    spec = create_test_spec()
    print(f"✓ Created test spec: {spec.name}")

    # Generate workflow
    generator = PocketFlowGenerator()
    print("✓ Created generator")

    output_files = generator.generate_workflow(spec)
    print(f"✓ Generated {len(output_files)} files")

    # Print file list
    print("\nGenerated files:")
    for file_path in sorted(output_files.keys()):
        content_length = len(output_files[file_path])
        print(f"  - {file_path} ({content_length} chars)")

    # Save to disk
    generator.save_workflow(spec, output_files)
    print("✓ Saved workflow to disk")

    # Validate saved files
    workflow_dir = Path(".agent-os/workflows") / spec.name.lower().replace(" ", "_")
    print(f"\nValidating saved files in: {workflow_dir}")

    expected_files = [
        "docs/design.md",
        "schemas/models.py",
        "utils/retrieve_documents.py",
        "utils/call_llm_analyzer.py",
        "nodes.py",
        "flow.py",
        "main.py",
        "router.py",
        "tests/test_nodes.py",
        "tests/test_flow.py",
        "tests/test_api.py",
        "tasks.md",
    ]

    missing_files = []
    for expected_file in expected_files:
        file_path = workflow_dir / expected_file
        if file_path.exists():
            print(f"  ✓ {expected_file}")
        else:
            print(f"  ✗ {expected_file}")
            missing_files.append(expected_file)

    if missing_files:
        print(f"\nMissing files: {missing_files}")
        return False
    else:
        print(f"\n✓ All {len(expected_files)} expected files created")
        return True


def test_file_contents():
    """Test that generated files have reasonable content."""
    print("\nTesting file contents...")

    workflow_dir = Path(".agent-os/workflows/testcontentanalyzer")

    # Test design document
    design_file = workflow_dir / "docs/design.md"
    if design_file.exists():
        content = design_file.read_text()
        if "# Design Document" in content and "TestContentAnalyzer" in content:
            print("  ✓ Design document has expected structure")
        else:
            print("  ✗ Design document missing expected content")
            return False

    # Test nodes file
    nodes_file = workflow_dir / "nodes.py"
    if nodes_file.exists():
        content = nodes_file.read_text()
        expected_classes = [
            "DocumentRetrieverNode",
            "ContextBuilderNode",
            "LLMAnalyzerNode",
            "ResponseFormatterNode",
        ]
        found_classes = [cls for cls in expected_classes if f"class {cls}" in content]

        if len(found_classes) == len(expected_classes):
            print(f"  ✓ All {len(expected_classes)} node classes found")
        else:
            print(
                f"  ✗ Missing node classes: {set(expected_classes) - set(found_classes)}"
            )
            return False

    # Test flow file
    flow_file = workflow_dir / "flow.py"
    if flow_file.exists():
        content = flow_file.read_text()
        if "class TestContentAnalyzerFlow" in content and "nodes = {" in content:
            print("  ✓ Flow file has expected structure")
        else:
            print("  ✗ Flow file missing expected content")
            return False

    # Test API files
    main_file = workflow_dir / "main.py"
    if main_file.exists():
        content = main_file.read_text()
        if "FastAPI" in content and "TestContentAnalyzer API" in content:
            print("  ✓ FastAPI main file has expected structure")
        else:
            print("  ✗ FastAPI main file missing expected content")
            return False

    return True


def cleanup():
    """Clean up generated test files."""
    workflow_dir = Path(".agent-os/workflows/testcontentanalyzer")
    if workflow_dir.exists():
        shutil.rmtree(workflow_dir)
        print(f"✓ Cleaned up test workflow: {workflow_dir}")


def main():
    """Run comprehensive generation test."""
    print("Comprehensive PocketFlow Generation Test")
    print("=" * 45)

    try:
        # Test generation and saving
        if not test_generation_and_save():
            print("\n✗ Generation test failed")
            return 1

        # Test file contents
        if not test_file_contents():
            print("\n✗ Content validation failed")
            return 1

        print("\n" + "=" * 45)
        print("✓ All tests passed!")
        print("\nGenerated workflow can be found at:")
        print("  .agent-os/workflows/testcontentanalyzer/")
        print("\nTo clean up, run:")
        print("  rm -rf .agent-os/workflows/testcontentanalyzer/")

        return 0

    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
