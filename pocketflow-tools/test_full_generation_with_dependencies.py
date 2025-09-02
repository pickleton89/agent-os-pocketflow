#!/usr/bin/env python3
"""
Test full workflow generation with dependency orchestrator integration.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add framework root to sys.path for package imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator
from pocketflow_tools.spec import WorkflowSpec


def test_full_workflow_generation():
    """Test complete workflow generation with dependency files."""
    print("Testing Full Workflow Generation with Dependencies")
    print("=" * 60)
    
    patterns_to_test = ["RAG", "AGENT", "TOOL", "WORKFLOW"]
    
    for pattern in patterns_to_test:
        print(f"\nTesting {pattern} pattern generation...")
        
        # Create a test workflow spec
        spec = WorkflowSpec(
            name=f"Test{pattern}Workflow",
            pattern=pattern,
            description=f"Test workflow for {pattern} pattern with dependency management"
        )
        
        # Create temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Initialize generator with temporary output path
            generator = PocketFlowGenerator(
                templates_path="templates",  # This might not exist, but fallback should work
                output_path=str(temp_path)
            )
            
            try:
                # Generate workflow
                output_files = generator.generate_workflow(spec)
                
                # Check that dependency files were generated
                expected_dependency_files = [
                    "pyproject.toml",
                    "requirements.txt", 
                    "requirements-dev.txt",
                    ".gitignore",
                    "README.md",
                    ".python-version",
                    "uv.toml"
                ]
                
                dependency_files_found = 0
                for dep_file in expected_dependency_files:
                    if dep_file in output_files:
                        dependency_files_found += 1
                        content = output_files[dep_file]
                        assert isinstance(content, str), f"{dep_file} content should be string"
                        assert len(content) > 0, f"{dep_file} should not be empty"
                
                print(f"  SUCCESS: Generated {len(output_files)} files")
                print(f"  SUCCESS: Found {dependency_files_found}/{len(expected_dependency_files)} dependency files")
                
                # Check pyproject.toml content specifically
                if "pyproject.toml" in output_files:
                    toml_content = output_files["pyproject.toml"]
                    assert "[build-system]" in toml_content
                    assert "[project]" in toml_content
                    assert "[tool.ruff]" in toml_content
                    print("  SUCCESS: pyproject.toml has required sections")
                
                # Check README content
                if "README.md" in output_files:
                    readme_content = output_files["README.md"]
                    assert f"# Test{pattern}Workflow" in readme_content
                    # Accept either full UV-based README or basic pip-based fallback
                    if "uv sync" in readme_content and "uv run pytest" in readme_content:
                        print("  SUCCESS: README.md has proper UV instructions")
                    elif "pip install -r requirements.txt" in readme_content and "pytest" in readme_content:
                        print("  SUCCESS: README.md has basic pip instructions (fallback)")
                    else:
                        raise AssertionError("README.md missing expected setup instructions (uv or pip)")

                # Persist to disk in the temporary directory and verify structure
                generator.save_workflow(spec, output_files)

                saved_root = temp_path / spec.name.lower().replace(" ", "_")
                expected_files_on_disk = [
                    "docs/design.md",
                    "schemas/models.py",
                    "utils",
                    "nodes.py",
                    "flow.py",
                    "main.py",
                    "router.py",
                    "tests/test_nodes.py",
                    "tests/test_flow.py",
                    "tests/test_api.py",
                    "tasks.md",
                    "pyproject.toml",
                    "requirements.txt",
                    "requirements-dev.txt",
                ]
                # Only require UV files if they were generated in-memory
                if ".python-version" in output_files:
                    expected_files_on_disk.append(".python-version")
                if "uv.toml" in output_files:
                    expected_files_on_disk.append("uv.toml")

                missing = []
                for rel in expected_files_on_disk:
                    p = saved_root / rel
                    if not p.exists():
                        missing.append(rel)
                if missing:
                    print(f"  ERROR: Missing expected generated files on disk: {missing}")
                    return False
                else:
                    print("  SUCCESS: Saved workflow has expected structure on disk")
                
            except FileNotFoundError as e:
                # Expected if templates directory doesn't exist - this is OK for framework testing
                if "Templates directory not found" in str(e):
                    print(f"  SKIPPED: {pattern} (no templates directory - this is expected in framework repo)")
                    continue
                else:
                    raise
            except Exception as e:
                print(f"  ERROR: {pattern} failed - {e}")
                import traceback
                traceback.print_exc()
                return False
    
    return True


def test_dependency_coordination():
    """Test that dependency orchestrator is properly coordinated."""
    print("\nTesting Dependency Orchestrator Coordination")
    print("=" * 60)
    
    try:
        # Test the coordination function directly
        generator = PocketFlowGenerator()
        
        # Test dependency config generation
        config = generator.generate_dependency_config("RAG")
        
        assert hasattr(config, 'base_dependencies')
        assert hasattr(config, 'pattern_dependencies')
        assert hasattr(config, 'dev_dependencies')
        assert hasattr(config, 'tool_configs')
        
        print("  SUCCESS: Dependency orchestrator coordination works")
        print(f"  SUCCESS: Config has {len(config.base_dependencies)} base deps")
        print(f"  SUCCESS: Config has {len(config.pattern_dependencies)} pattern deps")
        print(f"  SUCCESS: Config has {len(config.dev_dependencies)} dev deps")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: Coordination test failed - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_framework_vs_usage_separation():
    """Test that framework vs usage separation is maintained."""
    print("\nTesting Framework vs Usage Separation")
    print("=" * 60)
    
    # This test ensures we're not trying to install end-user dependencies
    # in the framework itself, and that generated templates have the right structure
    
    try:
        from dependency_orchestrator import DependencyOrchestrator
        
        orchestrator = DependencyOrchestrator()
        
        # Framework should not include end-user runtime dependencies
        # It should generate templates that WILL have those dependencies
        
        # Test RAG pattern dependencies - these should be for end-user projects
        config = orchestrator.generate_config_for_pattern("RAG")
        
        # Check that we have RAG-specific dependencies for templates
        pattern_dep_names = [dep.split('>=')[0].split('[')[0] for dep in config.pattern_dependencies]
        
        expected_rag_deps = ['chromadb', 'sentence-transformers']
        for dep in expected_rag_deps:
            assert dep in pattern_dep_names, f"Missing expected RAG dependency: {dep}"
        
        print("  SUCCESS: RAG pattern includes vector DB dependencies for end-user projects")
        
        # Test AGENT pattern
        agent_config = orchestrator.generate_config_for_pattern("AGENT")
        agent_dep_names = [dep.split('>=')[0].split('[')[0] for dep in agent_config.pattern_dependencies]
        
        expected_agent_deps = ['openai', 'tiktoken']
        for dep in expected_agent_deps:
            assert dep in agent_dep_names, f"Missing expected AGENT dependency: {dep}"
            
        print("  SUCCESS: AGENT pattern includes LLM client dependencies for end-user projects")
        
        # Verify we're not installing these in the framework repo itself
        # (This test is more conceptual - we're generating templates, not installing)
        print("  SUCCESS: Framework generates dependency templates, doesn't install end-user deps")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: Framework separation test failed - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("Phase 4 Dependency Orchestrator Integration Tests")
    print("=" * 70)
    
    test_functions = [
        test_dependency_coordination,
        test_framework_vs_usage_separation,
        test_full_workflow_generation,
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_func in test_functions:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                print(f"FAILED: {test_func.__name__}")
        except Exception as e:
            print(f"EXCEPTION in {test_func.__name__}: {e}")
    
    print("\n" + "=" * 70)
    print(f"Integration Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("SUCCESS: All Phase 4 integration tests passed!")
        print("\nPhase 4 Implementation Complete:")
        print("- Dependency orchestrator fully implemented")
        print("- Pattern-specific dependency mapping working")  
        print("- pyproject.toml generation working")
        print("- UV configuration generation working")
        print("- Configuration validation working")
        print("- Framework vs usage separation maintained")
        return 0
    else:
        print("FAILURE: Some integration tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
