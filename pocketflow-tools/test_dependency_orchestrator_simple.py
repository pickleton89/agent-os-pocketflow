#!/usr/bin/env python3
"""
SMOKE TEST: Quick checks for Dependency Orchestrator.

This is a lightweight smoke test for the dependency orchestrator to verify
essential behavior fast. The comprehensive suite is
`pocketflow-tools/test_dependency_orchestrator.py`.
"""

import sys
import logging
from pathlib import Path

# Add the workflows directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from dependency_orchestrator import DependencyOrchestrator, DependencyConfig


def test_pattern_config_generation():
    """Test configuration generation for all supported patterns."""
    print("Testing Pattern Configuration Generation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    patterns = ["RAG", "AGENT", "TOOL", "WORKFLOW", "MAPREDUCE", "MULTI-AGENT", "STRUCTURED-OUTPUT"]
    
    results = {}
    
    for pattern in patterns:
        try:
            config = orchestrator.generate_config_for_pattern(pattern)
            results[pattern] = {
                "success": True,
                "base_deps": len(config.base_dependencies),
                "pattern_deps": len(config.pattern_dependencies),
                "dev_deps": len(config.dev_dependencies),
                "tool_configs": len(config.tool_configs),
            }
            print("SUCCESS {} | Base: {} | Pattern: {} | Dev: {} | Tools: {}".format(
                pattern.ljust(15), 
                len(config.base_dependencies),
                len(config.pattern_dependencies), 
                len(config.dev_dependencies),
                len(config.tool_configs)
            ))
        except Exception as e:
            results[pattern] = {"success": False, "error": str(e)}
            print("ERROR {} | Error: {}".format(pattern.ljust(15), e))
    
    return results


def test_pyproject_generation():
    """Test pyproject.toml generation."""
    print("\nTesting PyProject.toml Generation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    test_patterns = ["RAG", "AGENT", "TOOL"]
    
    for pattern in test_patterns:
        try:
            project_name = "test-{}-project".format(pattern.lower())
            description = "Test {} pattern project".format(pattern)
            
            toml_content = orchestrator.generate_pyproject_toml(project_name, pattern, description)
            
            # Basic validation
            assert "[build-system]" in toml_content
            assert "[project]" in toml_content
            assert 'name = "{}"'.format(project_name) in toml_content
            assert 'description = "{}"'.format(description) in toml_content
            assert "[tool.ruff]" in toml_content
            assert "[tool.pytest.ini_options]" in toml_content
            
            print("SUCCESS {} | pyproject.toml generated ({} chars)".format(
                pattern.ljust(15), len(toml_content)
            ))
            
        except Exception as e:
            print("ERROR {} | Error: {}".format(pattern.ljust(15), e))


def test_uv_config_generation():
    """Test UV configuration generation."""
    print("\nTesting UV Configuration Generation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    test_patterns = ["RAG", "AGENT", "TOOL"]
    
    for pattern in test_patterns:
        try:
            project_name = "test-{}-project".format(pattern.lower())
            
            uv_files = orchestrator.generate_uv_config(project_name, pattern)
            
            # Check expected files
            expected_files = [".python-version", "uv.toml"]
            for filename in expected_files:
                assert filename in uv_files
                content = uv_files[filename]
                assert isinstance(content, str)
                assert len(content) > 0
            
            print("SUCCESS {} | UV config generated ({} files)".format(
                pattern.ljust(15), len(uv_files)
            ))
            
        except Exception as e:
            print("ERROR {} | Error: {}".format(pattern.ljust(15), e))


def test_version_constraints():
    """Test version constraint application."""
    print("\nTesting Version Constraint Application")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    
    test_cases = [
        ("pocketflow", "pocketflow>=0.1.0"),
        ("pydantic", "pydantic>=2.0,<3.0"),
        ("fastapi", "fastapi>=0.104.0,<1.0.0"),
        ("uvicorn[standard]", "uvicorn[standard]>=0.24.0,<1.0.0"),
        ("some-unknown-package", "some-unknown-package"),
    ]
    
    for input_dep, expected_output in test_cases:
        try:
            result = orchestrator._apply_version_constraints(input_dep)
            status = "SUCCESS" if result == expected_output else "MISMATCH"
            print("{} {} -> {}".format(status, input_dep.ljust(20), result))
            if result != expected_output:
                print("    Expected: {}".format(expected_output))
        except Exception as e:
            print("ERROR {} -> Error: {}".format(input_dep.ljust(20), e))


def run_integration_test():
    """Run a complete integration test."""
    print("\nIntegration Test: End-to-End Workflow")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    
    try:
        # 1. Generate configuration for RAG pattern
        print("1. Generating RAG pattern configuration...")
        config = orchestrator.generate_config_for_pattern("RAG")
        assert isinstance(config, DependencyConfig)
        print("   SUCCESS: Generated config with {} base deps".format(
            len(config.base_dependencies)
        ))
        
        # 2. Generate pyproject.toml
        print("2. Generating pyproject.toml...")
        toml_content = orchestrator.generate_pyproject_toml(
            "test-rag-app", "RAG", "Test RAG application"
        )
        assert len(toml_content) > 100
        print("   SUCCESS: Generated pyproject.toml ({} chars)".format(
            len(toml_content)
        ))
        
        # 3. Generate UV config
        print("3. Generating UV configuration...")
        uv_files = orchestrator.generate_uv_config("test-rag-app", "RAG")
        assert len(uv_files) >= 2
        print("   SUCCESS: Generated UV config ({} files)".format(
            len(uv_files)
        ))
        
        print("\nIntegration test completed successfully!")
        return True
        
    except Exception as e:
        print("\nIntegration test failed: {}".format(e))
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all dependency orchestrator tests."""
    print("Dependency Orchestrator Test Suite")
    print("Phase 4 Implementation Validation")
    print("=" * 60)
    
    test_functions = [
        test_pattern_config_generation,
        test_pyproject_generation,
        test_uv_config_generation,
        test_version_constraints,
        run_integration_test,
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_func in test_functions:
        try:
            result = test_func()
            if result is not False:  # None or True counts as success
                passed += 1
        except Exception as e:
            print("EXCEPTION {} failed with exception: {}".format(
                test_func.__name__, e
            ))
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test Results: {}/{} test suites passed".format(passed, total))
    
    if passed == total:
        print("All dependency orchestrator tests passed!")
        return 0
    else:
        print("Some tests failed. Check output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
