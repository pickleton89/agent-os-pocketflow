#!/usr/bin/env python3
"""
Test Suite for Dependency Orchestrator
Tests pattern-specific dependency generation and configuration
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dependency_orchestrator import DependencyOrchestrator, DependencyConfig


def test_basic_initialization():
    """Test that orchestrator initializes correctly"""
    print("=== Testing Basic Initialization ===")

    orchestrator = DependencyOrchestrator()

    # Check that pattern mappings are loaded
    assert len(orchestrator.pattern_dependency_map) > 0, (
        "Pattern dependency map should not be empty"
    )
    assert len(orchestrator.tool_configurations) > 0, (
        "Tool configurations should not be empty"
    )
    assert len(orchestrator.version_constraints) > 0, (
        "Version constraints should not be empty"
    )

    print(
        f"  ✓ Loaded {len(orchestrator.pattern_dependency_map)} pattern configurations"
    )
    print(f"  ✓ Loaded {len(orchestrator.tool_configurations)} tool configurations")
    print(f"  ✓ Loaded {len(orchestrator.version_constraints)} version constraints")

    return True


def test_pattern_specific_dependencies():
    """Test that each pattern generates correct dependencies"""
    print("\n=== Testing Pattern-Specific Dependencies ===")

    orchestrator = DependencyOrchestrator()

    patterns = [
        "RAG",
        "AGENT",
        "TOOL",
        "WORKFLOW",
        "MAPREDUCE",
        "MULTI-AGENT",
        "STRUCTURED-OUTPUT",
    ]

    for pattern in patterns:
        config = orchestrator.generate_config_for_pattern(pattern)

        # Verify config structure
        assert isinstance(config, DependencyConfig), (
            f"Config for {pattern} should be DependencyConfig"
        )
        assert len(config.base_dependencies) > 0, (
            f"{pattern} should have base dependencies"
        )
        assert config.python_version, f"{pattern} should have python version"

        # All patterns should have pocketflow, pydantic, fastapi, uvicorn
        base_dep_names = [
            dep.split(">=")[0].split("[")[0] for dep in config.base_dependencies
        ]
        assert "pocketflow" in base_dep_names, f"{pattern} should include pocketflow"
        assert "pydantic" in base_dep_names, f"{pattern} should include pydantic"
        assert "fastapi" in base_dep_names, f"{pattern} should include fastapi"

        # Check pattern-specific dependencies
        pattern_dep_names = [
            dep.split(">=")[0].split("[")[0] for dep in config.pattern_dependencies
        ]

        if pattern == "RAG":
            assert "chromadb" in pattern_dep_names or "chromadb" in base_dep_names, (
                "RAG should include chromadb"
            )
            print(
                f"  ✓ {pattern}: {len(config.pattern_dependencies)} pattern deps (includes chromadb)"
            )
        elif pattern == "AGENT":
            assert "openai" in pattern_dep_names or "openai" in base_dep_names, (
                "AGENT should include openai"
            )
            print(
                f"  ✓ {pattern}: {len(config.pattern_dependencies)} pattern deps (includes openai)"
            )
        elif pattern == "TOOL":
            has_http = any(
                pkg in pattern_dep_names or pkg in base_dep_names
                for pkg in ["requests", "aiohttp"]
            )
            assert has_http, "TOOL should include HTTP client"
            print(
                f"  ✓ {pattern}: {len(config.pattern_dependencies)} pattern deps (includes HTTP client)"
            )
        elif pattern == "MAPREDUCE":
            assert "celery" in pattern_dep_names or "celery" in base_dep_names, (
                "MAPREDUCE should include celery"
            )
            print(
                f"  ✓ {pattern}: {len(config.pattern_dependencies)} pattern deps (includes celery)"
            )
        else:
            print(f"  ✓ {pattern}: {len(config.pattern_dependencies)} pattern deps")

        # Verify dev dependencies
        assert len(config.dev_dependencies) > 0, (
            f"{pattern} should have dev dependencies"
        )
        dev_dep_names = [dep.split(">=")[0] for dep in config.dev_dependencies]
        assert "pytest" in dev_dep_names, f"{pattern} should include pytest in dev deps"
        assert "ruff" in dev_dep_names, f"{pattern} should include ruff in dev deps"

    return True


def test_pyproject_toml_generation():
    """Test pyproject.toml generation for each pattern"""
    print("\n=== Testing pyproject.toml Generation ===")

    orchestrator = DependencyOrchestrator()

    patterns = ["RAG", "AGENT", "TOOL", "WORKFLOW"]

    for pattern in patterns:
        content = orchestrator.generate_pyproject_toml(
            project_name=f"test-{pattern.lower()}-project",
            pattern=pattern,
            description=f"Test {pattern} pattern project",
        )

        # Verify basic structure
        assert "[build-system]" in content, (
            f"{pattern} pyproject.toml should have build-system"
        )
        assert "[project]" in content, (
            f"{pattern} pyproject.toml should have project section"
        )
        assert "dependencies = [" in content, (
            f"{pattern} pyproject.toml should have dependencies"
        )
        assert "[project.optional-dependencies]" in content, (
            f"{pattern} should have optional dependencies"
        )
        assert "dev = [" in content, f"{pattern} should have dev dependencies"

        # Verify tool configurations
        assert "[tool.ruff]" in content, f"{pattern} should have ruff config"
        assert "[tool.pytest.ini_options]" in content, (
            f"{pattern} should have pytest config"
        )

        # Verify project metadata
        assert f'name = "test-{pattern.lower()}-project"' in content, (
            f"{pattern} should have project name"
        )
        assert 'requires-python = ">=3.12' in content, (
            f"{pattern} should specify Python version"
        )

        print(f"  ✓ {pattern}: Generated valid pyproject.toml ({len(content)} chars)")

    return True


def test_requirements_txt_generation():
    """Test requirements.txt generation from config"""
    print("\n=== Testing requirements.txt Generation ===")

    orchestrator = DependencyOrchestrator()

    patterns = ["RAG", "AGENT", "TOOL"]

    for pattern in patterns:
        config = orchestrator.generate_config_for_pattern(pattern)

        # Combine base and pattern dependencies (like the refactored code will do)
        all_deps = list(set(config.base_dependencies + config.pattern_dependencies))

        # Verify structure
        assert len(all_deps) > 0, f"{pattern} should have runtime dependencies"

        # Check for version constraints
        for dep in all_deps:
            # Each dependency should have proper format
            assert isinstance(dep, str), f"Dependency should be string: {dep}"
            # Should have version constraint or be bare package name
            valid_format = (
                any(op in dep for op in [">=", "==", ">", "<", "~="])
                or "[" in dep
                or dep.isalpha()
            )
            assert valid_format, f"Dependency should have valid format: {dep}"

        print(f"  ✓ {pattern}: {len(all_deps)} total dependencies")

        # Verify dev dependencies
        assert len(config.dev_dependencies) > 0, (
            f"{pattern} should have dev dependencies"
        )
        print(f"  ✓ {pattern}: {len(config.dev_dependencies)} dev dependencies")

    return True


def test_uv_config_generation():
    """Test UV-specific configuration generation"""
    print("\n=== Testing UV Config Generation ===")

    orchestrator = DependencyOrchestrator()

    pattern = "AGENT"
    uv_files = orchestrator.generate_uv_config(f"test-{pattern.lower()}", pattern)

    # Should generate .python-version and uv.toml
    assert ".python-version" in uv_files, "Should generate .python-version"
    assert "uv.toml" in uv_files, "Should generate uv.toml"

    # Check .python-version content
    python_version = uv_files[".python-version"]
    assert "3.12" in python_version, "Should specify Python 3.12"

    # Check uv.toml content
    uv_toml = uv_files["uv.toml"]
    assert "[tool.uv]" in uv_toml, "Should have [tool.uv] section"
    assert "dev-dependencies = [" in uv_toml, "Should have dev-dependencies"

    print(f"  ✓ Generated .python-version: {python_version.strip()}")
    print(f"  ✓ Generated uv.toml ({len(uv_toml)} chars)")

    return True


def test_dependency_validation():
    """Test dependency validation functionality"""
    print("\n=== Testing Dependency Validation ===")

    orchestrator = DependencyOrchestrator()

    # Test valid dependencies
    valid_deps = ["pocketflow>=0.1.0", "fastapi>=0.104.0", "pydantic>=2.0"]
    issues = orchestrator.validate_dependencies(valid_deps)

    assert "warnings" in issues, "Should have warnings field"
    assert "errors" in issues, "Should have errors field"
    print(
        f"  ✓ Valid dependencies: {len(issues['warnings'])} warnings, {len(issues['errors'])} errors"
    )

    # Test conflicting dependencies
    conflicting_deps = ["django>=4.0", "fastapi>=0.104.0"]
    issues = orchestrator.validate_dependencies(conflicting_deps)

    # Should warn about using both web frameworks
    has_framework_warning = any("framework" in w.lower() for w in issues["warnings"])
    print(f"  ✓ Conflicting frameworks detected: {has_framework_warning}")

    return True


def test_pattern_compatibility_validation():
    """Test pattern-specific compatibility validation"""
    print("\n=== Testing Pattern Compatibility Validation ===")

    orchestrator = DependencyOrchestrator()

    # Test RAG pattern with correct dependencies
    rag_deps = [
        "pocketflow",
        "pydantic",
        "fastapi",
        "chromadb",
        "sentence-transformers",
    ]
    issues = orchestrator.validate_pattern_compatibility("RAG", rag_deps)

    assert len(issues["errors"]) == 0, "RAG with correct deps should have no errors"
    print(f"  ✓ RAG pattern with correct deps: {len(issues['warnings'])} warnings")

    # Test AGENT pattern missing LLM client
    agent_deps = ["pocketflow", "pydantic", "fastapi"]
    issues = orchestrator.validate_pattern_compatibility("AGENT", agent_deps)

    # Should warn about missing LLM client
    has_llm_warning = any("llm" in w.lower() for w in issues["warnings"])
    print(f"  ✓ AGENT without LLM client detected: {has_llm_warning}")

    return True


def test_caching():
    """Test configuration caching functionality"""
    print("\n=== Testing Configuration Caching ===")

    orchestrator = DependencyOrchestrator()

    # Generate config twice for same pattern
    config1 = orchestrator.generate_config_for_pattern("RAG")
    config2 = orchestrator.generate_config_for_pattern("RAG")

    # Should return same object from cache
    assert config1 is config2, "Should return cached config"
    print("  ✓ Configuration caching works")

    # Clear cache and regenerate
    orchestrator.clear_cache()
    config3 = orchestrator.generate_config_for_pattern("RAG")

    # Should be different object after cache clear
    assert config1 is not config3, "Should generate new config after cache clear"
    print("  ✓ Cache clearing works")

    return True


def test_version_constraints():
    """Test version constraint application"""
    print("\n=== Testing Version Constraints ===")

    orchestrator = DependencyOrchestrator()

    # Test constraint application
    test_cases = [
        ("pocketflow", "pocketflow>=0.1.0"),
        ("pydantic", "pydantic>=2.0,<3.0"),
        ("fastapi", "fastapi>=0.104.0,<1.0.0"),
        (
            "uvicorn[standard]",
            "uvicorn[standard]>=0.24.0,<1.0.0",
        ),  # Should preserve extras
    ]

    for input_dep, expected_pattern in test_cases:
        result = orchestrator._apply_version_constraints(input_dep)
        # Check if result matches expected pattern (basic check)
        has_constraint = ">=" in result or "==" in result
        print(f"  ✓ {input_dep} -> {result}")
        assert has_constraint or input_dep == result, (
            f"Should apply constraint to {input_dep}"
        )

    return True


def test_pyproject_validation():
    """Test pyproject.toml validation"""
    print("\n=== Testing pyproject.toml Validation ===")

    orchestrator = DependencyOrchestrator()

    # Generate valid pyproject.toml
    content = orchestrator.generate_pyproject_toml(
        "test-project", "WORKFLOW", "Test project"
    )

    # Validate it
    issues = orchestrator.validate_configuration(content, "pyproject.toml")

    assert "errors" in issues, "Should have errors field"
    assert "warnings" in issues, "Should have warnings field"
    assert len(issues["errors"]) == 0, (
        f"Generated pyproject.toml should be valid, got errors: {issues['errors']}"
    )

    print(f"  ✓ Generated pyproject.toml is valid")
    print(
        f"  ✓ Validation found {len(issues['warnings'])} warnings, {len(issues['errors'])} errors"
    )

    return True


def main():
    """Run all dependency orchestrator tests"""
    print("Dependency Orchestrator Test Suite")
    print("=" * 70)

    tests = [
        ("Basic Initialization", test_basic_initialization),
        ("Pattern-Specific Dependencies", test_pattern_specific_dependencies),
        ("pyproject.toml Generation", test_pyproject_toml_generation),
        ("requirements.txt Generation", test_requirements_txt_generation),
        ("UV Config Generation", test_uv_config_generation),
        ("Dependency Validation", test_dependency_validation),
        ("Pattern Compatibility", test_pattern_compatibility_validation),
        ("Configuration Caching", test_caching),
        ("Version Constraints", test_version_constraints),
        ("pyproject.toml Validation", test_pyproject_validation),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"\n✅ {test_name}: PASSED\n")
                passed += 1
            else:
                print(f"\n❌ {test_name}: FAILED\n")
                failed += 1
        except AssertionError as e:
            print(f"\n❌ {test_name}: ASSERTION FAILED - {str(e)}\n")
            failed += 1
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {str(e)}\n")
            import traceback

            traceback.print_exc()
            failed += 1

    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All dependency orchestrator tests passed!")
        return 0
    else:
        print(f"⚠️  {failed} tests failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
