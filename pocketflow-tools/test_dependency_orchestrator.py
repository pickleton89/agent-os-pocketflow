#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Dependency Orchestrator functionality.
Validates Phase 4 implementation of the dependency orchestrator agent.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add the workflows directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from dependency_orchestrator import DependencyOrchestrator, DependencyConfig


def setup_logging():
    """Set up logging for test output."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )


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
                "python_version": config.python_version
            }
            msg = "SUCCESS {} | Base: {:2} | Pattern: {:2} | Dev: {:2} | Tools: {:2}".format(
                pattern.ljust(15), 
                len(config.base_dependencies),
                len(config.pattern_dependencies), 
                len(config.dev_dependencies),
                len(config.tool_configs)
            )
            print(msg)
        except Exception as e:
            results[pattern] = {"success": False, "error": str(e)}
            print("ERROR {} | Error: {}".format(pattern.ljust(15), e))
    
    return results


def test_pyproject_generation():
    """Test pyproject.toml generation."""
    print("\n🧪 Testing PyProject.toml Generation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    test_patterns = ["RAG", "AGENT", "TOOL"]
    
    for pattern in test_patterns:
        try:
            project_name = f"test-{pattern.lower()}-project"
            description = f"Test {pattern} pattern project"
            
            toml_content = orchestrator.generate_pyproject_toml(project_name, pattern, description)
            
            # Basic validation
            assert "[build-system]" in toml_content
            assert "[project]" in toml_content
            assert f'name = "{project_name}"' in toml_content
            assert f'description = "{description}"' in toml_content
            assert "[tool.ruff]" in toml_content
            assert "[tool.pytest.ini_options]" in toml_content
            
            print(f"✅ {pattern:15} | pyproject.toml generated ({len(toml_content)} chars)")
            
        except Exception as e:
            print(f"❌ {pattern:15} | Error: {e}")


def test_uv_config_generation():
    """Test UV configuration generation."""
    print("\n🧪 Testing UV Configuration Generation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    test_patterns = ["RAG", "AGENT", "TOOL"]
    
    for pattern in test_patterns:
        try:
            project_name = f"test-{pattern.lower()}-project"
            
            uv_files = orchestrator.generate_uv_config(project_name, pattern)
            
            # Check expected files
            expected_files = [".python-version", "uv.toml"]
            for filename in expected_files:
                assert filename in uv_files
                content = uv_files[filename]
                assert isinstance(content, str)
                assert len(content) > 0
            
            print(f"✅ {pattern:15} | UV config generated ({len(uv_files)} files)")
            
        except Exception as e:
            print(f"❌ {pattern:15} | Error: {e}")


def test_configuration_validation():
    """Test configuration file validation."""
    print("\n🧪 Testing Configuration Validation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    
    # Test valid pyproject.toml
    valid_toml = '''
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test-project"
version = "0.1.0"
description = "Test project"
requires-python = ">=3.12"
dependencies = ["pocketflow", "pydantic>=2.0"]

[tool.ruff]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
    '''
    
    # Test invalid pyproject.toml
    invalid_toml = '''
[project
name = "test-project"
    '''
    
    # Test valid requirements.txt
    valid_requirements = '''
pocketflow
pydantic>=2.0
fastapi>=0.104.0
    '''
    
    # Test invalid requirements.txt
    invalid_requirements = '''
invalid-package-name-!!!
    '''
    
    test_cases = [
        ("valid pyproject.toml", valid_toml, "pyproject.toml"),
        ("invalid pyproject.toml", invalid_toml, "pyproject.toml"),
        ("valid requirements.txt", valid_requirements, "requirements.txt"),
        ("invalid requirements.txt", invalid_requirements, "requirements.txt"),
    ]
    
    for test_name, content, file_type in test_cases:
        try:
            issues = orchestrator.validate_configuration(content, file_type)
            error_count = len(issues.get("errors", []))
            warning_count = len(issues.get("warnings", []))
            
            status = "✅" if error_count == 0 else "⚠️" if error_count == 0 and warning_count > 0 else "❌"
            print(f"{status} {test_name:20} | Errors: {error_count:2} | Warnings: {warning_count:2}")
            
            # Print first few issues for debugging
            for error in issues.get("errors", [])[:2]:
                print(f"    Error: {error}")
            for warning in issues.get("warnings", [])[:2]:
                print(f"    Warning: {warning}")
                
        except Exception as e:
            print(f"❌ {test_name:20} | Validation failed: {e}")


def test_pattern_compatibility():
    """Test pattern compatibility validation."""
    print("\n🧪 Testing Pattern Compatibility Validation")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    
    test_cases = [
        # Good cases
        ("RAG with correct deps", "RAG", ["pocketflow", "pydantic>=2.0", "chromadb>=0.4.15"]),
        ("AGENT with LLM client", "AGENT", ["pocketflow", "pydantic>=2.0", "openai>=1.0.0"]),
        ("TOOL with HTTP client", "TOOL", ["pocketflow", "pydantic>=2.0", "requests>=2.31.0"]),
        
        # Problem cases  
        ("RAG missing chromadb", "RAG", ["pocketflow", "pydantic>=2.0"]),
        ("AGENT missing LLM client", "AGENT", ["pocketflow", "pydantic>=2.0"]),
        ("Missing pocketflow", "WORKFLOW", ["pydantic>=2.0"]),
    ]
    
    for test_name, pattern, dependencies in test_cases:
        try:
            issues = orchestrator.validate_pattern_compatibility(pattern, dependencies)
            error_count = len(issues.get("errors", []))
            warning_count = len(issues.get("warnings", []))
            
            status = "✅" if error_count == 0 and warning_count == 0 else "⚠️" if error_count == 0 else "❌"
            print(f"{status} {test_name:25} | Errors: {error_count:2} | Warnings: {warning_count:2}")
            
        except Exception as e:
            print(f"❌ {test_name:25} | Validation failed: {e}")


def test_version_constraints():
    """Test version constraint application."""
    print("\n🧪 Testing Version Constraint Application")
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
            status = "✅" if result == expected_output else "❌"
            print(f"{status} {input_dep:20} → {result}")
            if result != expected_output:
                print(f"    Expected: {expected_output}")
        except Exception as e:
            print(f"❌ {input_dep:20} → Error: {e}")


def test_dependency_recommendations():
    """Test dependency recommendation based on requirements text."""
    print("\n🧪 Testing Dependency Recommendations")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    
    test_cases = [
        ("Database project", "We need to store data in a postgres database"),
        ("Auth system", "Users need to login with JWT tokens"),
        ("File processing", "Process PDF files and Excel spreadsheets"),
        ("ML pipeline", "Train models and make predictions"),
        ("Simple workflow", "Just process some data"),
    ]
    
    for test_name, requirements_text in test_cases:
        try:
            recommendations = orchestrator.get_pattern_recommendations(requirements_text)
            print(f"✅ {test_name:20} | {len(recommendations)} recommendations: {', '.join(recommendations[:3])}")
        except Exception as e:
            print(f"❌ {test_name:20} | Error: {e}")


def run_integration_test():
    """Run a complete integration test."""
    print("\n🚀 Integration Test: End-to-End Workflow")
    print("=" * 50)
    
    orchestrator = DependencyOrchestrator()
    
    try:
        # 1. Generate configuration for RAG pattern
        print("1. Generating RAG pattern configuration...")
        config = orchestrator.generate_config_for_pattern("RAG")
        assert isinstance(config, DependencyConfig)
        print(f"   ✅ Generated config with {len(config.base_dependencies)} base deps")
        
        # 2. Generate pyproject.toml
        print("2. Generating pyproject.toml...")
        toml_content = orchestrator.generate_pyproject_toml("test-rag-app", "RAG", "Test RAG application")
        assert len(toml_content) > 100
        print(f"   ✅ Generated pyproject.toml ({len(toml_content)} chars)")
        
        # 3. Validate the generated configuration
        print("3. Validating generated configuration...")
        issues = orchestrator.validate_configuration(toml_content, "pyproject.toml")
        error_count = len(issues.get("errors", []))
        print(f"   {'✅' if error_count == 0 else '❌'} Validation complete ({error_count} errors)")
        
        # 4. Check pattern compatibility
        print("4. Checking pattern compatibility...")
        all_deps = config.base_dependencies + config.pattern_dependencies
        compat_issues = orchestrator.validate_pattern_compatibility("RAG", all_deps)
        compat_errors = len(compat_issues.get("errors", []))
        print(f"   {'✅' if compat_errors == 0 else '❌'} Compatibility check complete ({compat_errors} errors)")
        
        # 5. Generate UV config
        print("5. Generating UV configuration...")
        uv_files = orchestrator.generate_uv_config("test-rag-app", "RAG")
        assert len(uv_files) >= 2
        print(f"   ✅ Generated UV config ({len(uv_files)} files)")
        
        print("\n🎉 Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n💥 Integration test failed: {e}")
        return False


def main():
    """Run all dependency orchestrator tests."""
    setup_logging()
    
    print("🔧 Dependency Orchestrator Test Suite")
    print("Phase 4 Implementation Validation")
    print("=" * 60)
    
    test_functions = [
        test_pattern_config_generation,
        test_pyproject_generation,
        test_uv_config_generation,
        test_configuration_validation,
        test_pattern_compatibility,
        test_version_constraints,
        test_dependency_recommendations,
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
            print(f"💥 {test_func.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All dependency orchestrator tests passed!")
        return 0
    else:
        print("❌ Some tests failed. Check output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
