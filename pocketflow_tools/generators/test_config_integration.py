#!/usr/bin/env python3
"""
Integration test for config_generators with dependency orchestrator
"""

import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pocketflow_tools.spec import WorkflowSpec
from pocketflow_tools.generators.config_generators import (
    generate_dependency_files,
    generate_basic_pyproject,
)


def create_test_spec(pattern: str) -> WorkflowSpec:
    """Create a test WorkflowSpec for the given pattern."""
    return WorkflowSpec(
        name=f"Test{pattern}Workflow",
        description=f"Test {pattern} pattern workflow",
        pattern=pattern,
        nodes=[{"name": "TestNode", "type": "Node", "description": "Test node"}],
        utilities=[{"name": "test_utility", "description": "Test utility function"}],
        shared_store_schema={},
        api_endpoints=[],
    )


def test_generate_dependency_files_with_patterns():
    """Test that generate_dependency_files works with all patterns."""
    print("=== Testing generate_dependency_files Integration ===\n")

    patterns = ["RAG", "AGENT", "TOOL", "WORKFLOW", "MAPREDUCE"]

    for pattern in patterns:
        print(f"Testing {pattern} pattern...")

        spec = create_test_spec(pattern)
        files = generate_dependency_files(spec)

        # Verify all expected files are generated
        expected_files = [
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            ".gitignore",
            "README.md",
            "uv.toml",
            ".python-version",
        ]

        for file_name in expected_files:
            assert file_name in files, f"Missing {file_name} for {pattern}"
            assert len(files[file_name]) > 0, f"Empty {file_name} for {pattern}"

        # Verify pattern-specific dependencies are included
        requirements = files["requirements.txt"]

        # All patterns should have base dependencies
        assert "pocketflow" in requirements, f"{pattern} should have pocketflow"
        assert "pydantic" in requirements, f"{pattern} should have pydantic"
        assert "fastapi" in requirements, f"{pattern} should have fastapi"

        # Check pattern-specific dependencies
        if pattern == "RAG":
            assert "chromadb" in requirements, "RAG should have chromadb"
            print(f"  ✓ {pattern}: chromadb included")
        elif pattern == "AGENT":
            assert "openai" in requirements, "AGENT should have openai"
            print(f"  ✓ {pattern}: openai included")
        elif pattern == "TOOL":
            has_http = "requests" in requirements or "aiohttp" in requirements
            assert has_http, "TOOL should have HTTP client"
            print(f"  ✓ {pattern}: HTTP client included")
        elif pattern == "MAPREDUCE":
            assert "celery" in requirements, "MAPREDUCE should have celery"
            print(f"  ✓ {pattern}: celery included")
        else:
            print(f"  ✓ {pattern}: base dependencies included")

        # Verify pyproject.toml structure
        pyproject = files["pyproject.toml"]
        assert "[build-system]" in pyproject, (
            f"{pattern} pyproject.toml should have build-system"
        )
        assert "[project]" in pyproject, (
            f"{pattern} pyproject.toml should have project section"
        )
        assert "[tool.ruff]" in pyproject, (
            f"{pattern} pyproject.toml should have ruff config"
        )
        assert "[tool.pytest.ini_options]" in pyproject, (
            f"{pattern} pyproject.toml should have pytest config"
        )

        # Verify requirements-dev.txt has dev dependencies
        requirements_dev = files["requirements-dev.txt"]
        assert "pytest" in requirements_dev, f"{pattern} should have pytest in dev deps"
        assert "ruff" in requirements_dev, f"{pattern} should have ruff in dev deps"
        assert "ty" in requirements_dev, f"{pattern} should have ty in dev deps"

        # Verify UV configuration
        assert ".python-version" in files, f"{pattern} should have .python-version"
        assert "3.12" in files[".python-version"], (
            f"{pattern} should specify Python 3.12"
        )

        uv_toml = files["uv.toml"]
        assert "[tool.uv]" in uv_toml, f"{pattern} should have [tool.uv] section"
        assert "dev-dependencies" in uv_toml, (
            f"{pattern} should have dev-dependencies in uv.toml"
        )

        # Verify README
        readme = files["README.md"]
        assert pattern in readme, f"{pattern} README should mention pattern"
        assert "PocketFlow" in readme, f"{pattern} README should mention PocketFlow"
        assert "uv run" in readme, f"{pattern} README should include UV commands"

        print(f"  ✓ All files generated correctly for {pattern}\n")

    return True


def test_generate_basic_pyproject():
    """Test that generate_basic_pyproject uses the orchestrator."""
    print("=== Testing generate_basic_pyproject Integration ===\n")

    patterns = ["RAG", "AGENT", "TOOL"]

    for pattern in patterns:
        spec = create_test_spec(pattern)
        pyproject = generate_basic_pyproject(spec)

        # Verify basic structure
        assert "[build-system]" in pyproject, f"{pattern} should have build-system"
        assert "[project]" in pyproject, f"{pattern} should have project section"
        assert f'name = "test{pattern.lower()}workflow"' in pyproject, (
            f"{pattern} should have correct name"
        )

        # Verify pattern name appears in description
        assert pattern in pyproject or pattern.lower() in pyproject, (
            f"{pattern} should be in description"
        )

        # Verify tool configurations
        assert "[tool.ruff]" in pyproject, f"{pattern} should have ruff config"
        assert "[tool.pytest.ini_options]" in pyproject, (
            f"{pattern} should have pytest config"
        )

        print(f"  ✓ {pattern}: generate_basic_pyproject works correctly")

    print()
    return True


def test_pattern_specific_dependencies():
    """Test that different patterns generate different dependencies."""
    print("=== Testing Pattern-Specific Dependencies ===\n")

    # Create specs for different patterns
    rag_spec = create_test_spec("RAG")
    agent_spec = create_test_spec("AGENT")
    workflow_spec = create_test_spec("WORKFLOW")

    rag_files = generate_dependency_files(rag_spec)
    agent_files = generate_dependency_files(agent_spec)
    workflow_files = generate_dependency_files(workflow_spec)

    # RAG should have chromadb, others shouldn't
    assert "chromadb" in rag_files["requirements.txt"], "RAG should have chromadb"
    assert "chromadb" not in agent_files["requirements.txt"], (
        "AGENT shouldn't have chromadb"
    )
    assert "chromadb" not in workflow_files["requirements.txt"], (
        "WORKFLOW shouldn't have chromadb"
    )
    print("  ✓ RAG has unique dependencies (chromadb)")

    # AGENT should have openai, others shouldn't necessarily
    assert "openai" in agent_files["requirements.txt"], "AGENT should have openai"
    print("  ✓ AGENT has unique dependencies (openai)")

    # WORKFLOW should have minimal dependencies
    workflow_deps = workflow_files["requirements.txt"].split("\n")
    rag_deps = rag_files["requirements.txt"].split("\n")
    assert len(workflow_deps) < len(rag_deps), (
        "WORKFLOW should have fewer deps than RAG"
    )
    print("  ✓ WORKFLOW has minimal dependencies")

    print()
    return True


def main():
    """Run all integration tests."""
    print("Config Generators Integration Test Suite")
    print("=" * 70)
    print()

    tests = [
        (
            "generate_dependency_files with all patterns",
            test_generate_dependency_files_with_patterns,
        ),
        ("generate_basic_pyproject integration", test_generate_basic_pyproject),
        ("Pattern-specific dependencies", test_pattern_specific_dependencies),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED\n")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED\n")
                failed += 1
        except AssertionError as e:
            print(f"❌ {test_name}: ASSERTION FAILED - {str(e)}\n")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}\n")
            import traceback

            traceback.print_exc()
            failed += 1

    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print(f"⚠️  {failed} tests failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
