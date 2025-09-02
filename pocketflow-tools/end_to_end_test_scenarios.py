#!/usr/bin/env python3
"""
End-to-End Test Scenarios for Universal PocketFlow Integration (Task 5.1)

Tests that validate the universal PocketFlow architecture works for all project types,
ensuring the framework generates PocketFlow-structured code for every workflow.

This validates the implementation of Tasks 1-4 (Universal PocketFlow Integration).
"""

import logging
import os
import sys
import tempfile
import shutil
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import subprocess
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class TestScenario:
    """Test scenario definition."""
    name: str
    description: str
    requirements: str
    expected_pattern: str
    expected_files: List[str]
    validation_criteria: Dict[str, Any]


@dataclass
class TestResult:
    """Test execution result."""
    scenario_name: str
    success: bool
    pattern_detected: Optional[str]
    files_generated: List[str]
    errors: List[str]
    validation_results: Dict[str, bool]


class EndToEndTestRunner:
    """Runner for end-to-end test scenarios validating universal PocketFlow integration."""
    
    def __init__(self, test_workspace_dir: Optional[str] = None):
        """Initialize test runner."""
        self.test_workspace = test_workspace_dir or tempfile.mkdtemp(prefix="e2e_test_")
        self.results = []
        self.framework_root = Path(__file__).parent.parent
        
        # Ensure we have access to the framework tools and package
        sys.path.insert(0, str(self.framework_root))
        sys.path.insert(0, str(self.framework_root / "pocketflow-tools"))
        
        # Change to framework root so generator can find templates
        self.original_cwd = os.getcwd()
        os.chdir(str(self.framework_root))
        
        logger.info(f"Test workspace: {self.test_workspace}")
        logger.info(f"Framework root: {self.framework_root}")
    
    def cleanup(self):
        """Clean up test workspace."""
        # Restore original working directory
        if hasattr(self, 'original_cwd'):
            os.chdir(self.original_cwd)
            
        if os.path.exists(self.test_workspace):
            shutil.rmtree(self.test_workspace)
            logger.info(f"Cleaned up test workspace: {self.test_workspace}")
    
    def run_all_scenarios(self) -> List[TestResult]:
        """Run all test scenarios."""
        scenarios = self._get_test_scenarios()
        
        logger.info("="*80)
        logger.info("END-TO-END TEST SCENARIOS - UNIVERSAL POCKETFLOW VALIDATION")
        logger.info("="*80)
        logger.info(f"Running {len(scenarios)} test scenarios...")
        
        for scenario in scenarios:
            logger.info(f"\n{'-'*60}")
            logger.info(f"Running: {scenario.name}")
            logger.info(f"{'-'*60}")
            
            result = self._run_scenario(scenario)
            self.results.append(result)
            
            if result.success:
                logger.info("✅ PASSED")
            else:
                logger.error(f"❌ FAILED: {', '.join(result.errors)}")
        
        self._print_summary()
        return self.results
    
    def _get_test_scenarios(self) -> List[TestScenario]:
        """Define all test scenarios according to Task 5.1 requirements."""
        
        return [
            # Scenario 1: Simple CRUD Application (WORKFLOW pattern)
            TestScenario(
                name="Simple CRUD Application",
                description="Basic CRUD operations that should use WORKFLOW pattern",
                requirements="""
                Build a simple user management system with these features:
                1. Create new users with name, email, and role
                2. Read user information from a database
                3. Update user profiles and settings
                4. Delete users from the system
                5. Validate input data before processing
                6. Return standardized API responses
                
                This is a straightforward CRUD application with no AI/LLM components.
                """,
                expected_pattern="WORKFLOW",
                expected_files=[
                    "nodes.py",
                    "flow.py",
                    "schemas/models.py",
                    "tests/test_flow.py",
                    "tests/test_nodes.py",
                    "main.py",
                    "router.py"
                ],
                validation_criteria={
                    "pocketflow_structure": True,
                    "workflow_pattern": True,
                    "no_ai_dependencies": True,
                    "crud_operations": True,
                    "proper_nodes": True
                }
            ),
            
            # Scenario 2: REST API Service (TOOL pattern)
            TestScenario(
                name="REST API Service",
                description="External API integration that should use TOOL pattern",
                requirements="""
                Create a payment processing API integration service that:
                1. Connects to Stripe API for payment processing
                2. Handles webhook notifications from payment providers
                3. Transforms payment data between different formats
                4. Implements retry logic for failed API calls
                5. Manages API rate limiting and error handling
                6. Logs all API interactions for audit purposes
                7. Provides standardized payment status responses
                
                This focuses on external service integration, not AI.
                """,
                expected_pattern="TOOL",
                expected_files=[
                    "nodes.py",
                    "flow.py", 
                    "schemas/models.py",
                    "utils/__init__.py",
                    "tests/test_flow.py",
                    "main.py",
                    "router.py"
                ],
                validation_criteria={
                    "pocketflow_structure": True,
                    "tool_pattern": True,
                    "api_integration": True,
                    "error_handling": True,
                    "no_ai_dependencies": True
                }
            ),
            
            # Scenario 3: Data Processing Job (MAPREDUCE pattern)
            TestScenario(
                name="Data Processing Job", 
                description="Large-scale data processing that should use MAPREDUCE pattern",
                requirements="""
                Build a sales data processing pipeline that:
                1. Reads sales data from multiple CSV files (10GB+ datasets)
                2. Cleans and validates data records in parallel
                3. Aggregates sales metrics by region, product, and time period
                4. Calculates derived metrics like growth rates and trends
                5. Generates summary reports in multiple formats
                6. Handles data processing errors gracefully
                7. Processes data in chunks for memory efficiency
                8. Outputs results to database and file storage
                
                This is traditional ETL processing without AI components.
                """,
                expected_pattern="MAPREDUCE",
                expected_files=[
                    "nodes.py",
                    "flow.py", 
                    "schemas/models.py",
                    "utils/__init__.py",
                    "tests/test_flow.py",
                    "tests/test_nodes.py",
                    "main.py",
                    "router.py"
                ],
                validation_criteria={
                    "pocketflow_structure": True,
                    "mapreduce_pattern": True,
                    "parallel_processing": True,
                    "data_pipeline": True,
                    "no_ai_dependencies": True
                }
            ),
            
            # Scenario 4: Complex Business Workflow (AGENT pattern)
            TestScenario(
                name="Complex Business Workflow",
                description="Multi-step business logic that should use AGENT pattern",
                requirements="""
                Develop an order fulfillment automation system that:
                1. Receives customer orders and validates inventory availability
                2. Makes intelligent decisions about shipping methods based on multiple factors
                3. Coordinates with warehouse management systems
                4. Handles exception scenarios like backorders and cancellations
                5. Makes autonomous decisions about order prioritization
                6. Adapts workflow based on business rules and constraints
                7. Manages complex state transitions through order lifecycle
                8. Provides intelligent recommendations for order optimization
                
                This requires decision-making and workflow adaptation, but not LLMs.
                """,
                expected_pattern="AGENT", 
                expected_files=[
                    "nodes.py",
                    "flow.py",
                    "schemas/models.py",
                    "utils/__init__.py",
                    "tests/test_flow.py",
                    "tests/test_nodes.py",
                    "main.py",
                    "router.py"
                ],
                validation_criteria={
                    "pocketflow_structure": True,
                    "agent_pattern": True,
                    "decision_making": True,
                    "complex_workflow": True,
                    "state_management": True
                }
            ),
            
            # Scenario 5: Search/Query System (RAG pattern)
            TestScenario(
                name="Search/Query System",
                description="Knowledge search system that should use RAG pattern", 
                requirements="""
                Build a product catalog search system that:
                1. Indexes product information from multiple data sources
                2. Processes search queries and finds relevant products
                3. Uses semantic similarity for intelligent matching
                4. Retrieves product details and specifications
                5. Ranks results based on relevance and business rules
                6. Provides augmented search results with recommendations
                7. Handles complex queries with multiple filters
                8. Uses vector embeddings for semantic search capabilities
                
                This uses AI/embedding models for search, demonstrating RAG pattern.
                """,
                expected_pattern="RAG",
                expected_files=[
                    "nodes.py",
                    "flow.py",
                    "schemas/models.py",
                    "utils/__init__.py",
                    "tests/test_flow.py",
                    "tests/test_nodes.py",
                    "main.py",
                    "router.py"
                ],
                validation_criteria={
                    "pocketflow_structure": True,
                    "rag_pattern": True,
                    "search_functionality": True,
                    "vector_operations": True,
                    "ai_components": True
                }
            )
        ]
    
    def _run_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a single test scenario."""
        logger.info(f"Requirements: {scenario.requirements[:100]}...")
        
        result = TestResult(
            scenario_name=scenario.name,
            success=False,
            pattern_detected=None,
            files_generated=[],
            errors=[],
            validation_results={}
        )
        
        try:
            # Create test directory for this scenario
            scenario_dir = Path(self.test_workspace) / scenario.name.lower().replace(" ", "_")
            scenario_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. Test Pattern Recognition
            pattern_detected = self._test_pattern_recognition(scenario)
            result.pattern_detected = pattern_detected
            
            if pattern_detected != scenario.expected_pattern:
                result.errors.append(f"Expected {scenario.expected_pattern}, got {pattern_detected}")
            
            # 2. Test Template Generation
            files_generated = self._test_template_generation(scenario, scenario_dir)
            result.files_generated = files_generated
            
            # 3. Validate Generated Structure
            validation_results = self._validate_generated_structure(scenario, scenario_dir)
            result.validation_results = validation_results
            
            # 4. Check Framework vs Usage Distinction
            framework_distinction_valid = self._validate_framework_distinction(scenario_dir)
            result.validation_results["framework_distinction"] = framework_distinction_valid
            
            # Overall success criteria
            pattern_correct = pattern_detected == scenario.expected_pattern
            structure_valid = all(validation_results.values())
            files_present = len([f for f in scenario.expected_files if self._file_exists(scenario_dir, f)]) > 0
            
            result.success = pattern_correct and structure_valid and files_present and framework_distinction_valid
            
            if not result.success:
                if not pattern_correct:
                    result.errors.append(f"Pattern mismatch: expected {scenario.expected_pattern}, got {pattern_detected}")
                if not structure_valid:
                    failed_validations = [k for k, v in validation_results.items() if not v]
                    result.errors.append(f"Structure validation failed: {failed_validations}")
                if not files_present:
                    result.errors.append("Expected files not generated")
                if not framework_distinction_valid:
                    result.errors.append("Framework vs usage distinction not maintained")
        
        except Exception as e:
            result.errors.append(f"Test execution error: {str(e)}")
            logger.exception(f"Error running scenario {scenario.name}")
        
        return result
    
    def _test_pattern_recognition(self, scenario: TestScenario) -> Optional[str]:
        """Test pattern recognition for the scenario."""
        try:
            # Import and use the pattern analyzer
            from pattern_analyzer import PatternAnalyzer
            
            analyzer = PatternAnalyzer()
            recommendation = analyzer.analyze_and_recommend(scenario.requirements)
            
            logger.info(f"Pattern detected: {recommendation.primary_pattern.value}")
            logger.info(f"Confidence: {recommendation.confidence_score:.2f}")
            
            return recommendation.primary_pattern.value
        except Exception as e:
            logger.error(f"Pattern recognition failed: {e}")
            return None
    
    def _test_template_generation(self, scenario: TestScenario, output_dir: Path) -> List[str]:
        """Test template generation for the scenario."""
        try:
            # Import and use the generator
            from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator
            
            generator = PocketFlowGenerator()
            
            # Generate templates using the proper method
            name = scenario.name.lower().replace(" ", "_")
            file_contents = generator.generate_workflow_from_requirements(name, scenario.requirements)
            
            # Write the generated files to the output directory
            generated_files = []
            for file_path, content in file_contents.items():
                full_path = output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                generated_files.append(file_path)
            
            logger.info(f"Generated {len(generated_files)} files")
            return generated_files
            
        except Exception as e:
            logger.error(f"Template generation failed: {e}")
            return []
    
    def _validate_generated_structure(self, scenario: TestScenario, output_dir: Path) -> Dict[str, bool]:
        """Validate the generated project structure."""
        results = {}
        
        try:
            # Check PocketFlow structure
            results["pocketflow_structure"] = self._has_pocketflow_structure(output_dir)
            
            # Check pattern-specific structure
            results[f"{scenario.expected_pattern.lower()}_pattern"] = self._has_pattern_structure(
                output_dir, scenario.expected_pattern
            )
            
            # Check for proper Node structure
            results["proper_nodes"] = self._has_proper_node_structure(output_dir)
            
            # Check for no AI dependencies (except for RAG pattern)
            if scenario.expected_pattern != "RAG":
                results["no_ai_dependencies"] = self._has_no_ai_dependencies(output_dir)
            else:
                results["ai_components"] = self._has_ai_components(output_dir)
            
            # Pattern-specific validations
            if scenario.expected_pattern == "WORKFLOW":
                results["crud_operations"] = self._has_crud_operations(output_dir)
            elif scenario.expected_pattern == "TOOL": 
                results["api_integration"] = self._has_api_integration(output_dir)
                results["error_handling"] = self._has_error_handling(output_dir)
            elif scenario.expected_pattern == "MAPREDUCE":
                results["parallel_processing"] = self._has_parallel_processing(output_dir)
                results["data_pipeline"] = self._has_data_pipeline(output_dir)
            elif scenario.expected_pattern == "AGENT":
                results["decision_making"] = self._has_decision_making(output_dir)
                results["complex_workflow"] = self._has_complex_workflow(output_dir)
                results["state_management"] = self._has_state_management(output_dir)
            elif scenario.expected_pattern == "RAG":
                results["search_functionality"] = self._has_search_functionality(output_dir)
                results["vector_operations"] = self._has_vector_operations(output_dir)
            
        except Exception as e:
            logger.error(f"Structure validation error: {e}")
            # Set all to False on error
            for key in scenario.validation_criteria:
                results[key] = False
        
        return results
    
    def _validate_framework_distinction(self, output_dir: Path) -> bool:
        """Validate that framework vs usage distinction is maintained."""
        try:
            # Check that generated files have TODO placeholders (framework templates)
            # and not working implementations (usage code)
            
            python_files = list(output_dir.rglob("*.py"))
            if not python_files:
                return False
            
            has_todos = False
            has_placeholders = False
            
            for file_path in python_files:
                if file_path.name.startswith("test_"):
                    continue
                if file_path.name in ["__init__.py", "check-install.py"]:
                    continue
                    
                try:
                    content = file_path.read_text()
                    # Look for various TODO patterns
                    if "# TODO:" in content or "TODO:" in content or "# TODO " in content:
                        has_todos = True
                    # Look for placeholder patterns indicating template nature
                    if ("Customize this" in content or 
                        "Implement your" in content or
                        "Add your logic here" in content or
                        "raise NotImplementedError" in content):
                        has_placeholders = True
                except Exception:
                    continue
            
            # Framework templates should have TODOs or placeholders
            return has_todos or has_placeholders
            
        except Exception as e:
            logger.error(f"Framework distinction validation error: {e}")
            return False
    
    def _file_exists(self, base_dir: Path, file_path: str) -> bool:
        """Check if a file exists in the generated structure."""
        return (base_dir / file_path).exists()
    
    def _has_pocketflow_structure(self, output_dir: Path) -> bool:
        """Check if output has proper PocketFlow structure."""
        # Check for core PocketFlow files
        required_files = ["nodes.py", "flow.py", "schemas/models.py", "tests/test_flow.py"]
        return all((output_dir / f).exists() for f in required_files)
    
    def _has_pattern_structure(self, output_dir: Path, pattern: str) -> bool:
        """Check pattern-specific structure requirements."""
        # All patterns should have flow and nodes files
        return (output_dir / "flow.py").exists() and (output_dir / "nodes.py").exists()
    
    def _has_proper_node_structure(self, output_dir: Path) -> bool:
        """Check if nodes follow PocketFlow structure."""
        nodes_file = output_dir / "nodes.py"
        if not nodes_file.exists():
            return False
        
        try:
            content = nodes_file.read_text()
            # Look for Node class structure patterns
            return "prep(" in content and "exec(" in content and "post(" in content
        except Exception:
            return False
    
    def _has_no_ai_dependencies(self, output_dir: Path) -> bool:
        """Check that non-AI patterns don't include AI dependencies."""
        python_files = list(output_dir.rglob("*.py"))
        
        # Look for actual AI library imports/usage, not just mentions in comments
        ai_imports = ["import openai", "from openai", "import anthropic", "from anthropic", 
                     "import langchain", "from langchain", "import transformers", "from transformers"]
        ai_usage = ["OpenAI(", "anthropic.", "langchain.", "embedding_model", "transformer_model"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text()
                
                # Check for actual AI imports
                if any(ai_import in content for ai_import in ai_imports):
                    return False
                    
                # Check for actual AI usage (not just mentions in docstrings/comments)
                for line in content.split('\n'):
                    # Skip comments and docstrings
                    if line.strip().startswith('#') or line.strip().startswith('"""') or line.strip().startswith("'''"):
                        continue
                    if any(usage in line for usage in ai_usage):
                        return False
                        
            except Exception:
                continue
        
        return True
    
    def _has_ai_components(self, output_dir: Path) -> bool:
        """Check that AI patterns include AI components."""
        python_files = list(output_dir.rglob("*.py"))
        
        ai_keywords = ["embedding", "vector", "similarity", "search", "retrieval"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in ai_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_crud_operations(self, output_dir: Path) -> bool:
        """Check for CRUD operation indicators."""
        python_files = list(output_dir.rglob("*.py"))
        
        crud_keywords = ["create", "read", "update", "delete", "insert", "select"]
        
        found_operations = 0
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                for keyword in crud_keywords:
                    if keyword in content:
                        found_operations += 1
                        break
            except Exception:
                continue
        
        return found_operations >= 2  # At least 2 CRUD operations mentioned
    
    def _has_api_integration(self, output_dir: Path) -> bool:
        """Check for API integration patterns."""
        python_files = list(output_dir.rglob("*.py"))
        
        api_keywords = ["requests", "api", "http", "client", "webhook", "endpoint"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in api_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_error_handling(self, output_dir: Path) -> bool:
        """Check for error handling patterns."""
        python_files = list(output_dir.rglob("*.py"))
        
        error_keywords = ["try:", "except", "raise", "error", "exception"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in error_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_parallel_processing(self, output_dir: Path) -> bool:
        """Check for parallel processing indicators."""
        python_files = list(output_dir.rglob("*.py"))
        
        parallel_keywords = ["map", "reduce", "parallel", "chunk", "batch", "concurrent"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in parallel_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_data_pipeline(self, output_dir: Path) -> bool:
        """Check for data pipeline patterns."""
        python_files = list(output_dir.rglob("*.py"))
        
        pipeline_keywords = ["pipeline", "etl", "transform", "process", "data"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in pipeline_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_decision_making(self, output_dir: Path) -> bool:
        """Check for decision making patterns."""
        python_files = list(output_dir.rglob("*.py"))
        
        decision_keywords = ["decision", "rule", "condition", "logic", "choose", "select"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in decision_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_complex_workflow(self, output_dir: Path) -> bool:
        """Check for complex workflow patterns."""
        # Check for flow file and that it has substantial content
        flow_file = output_dir / "flow.py"
        if not flow_file.exists():
            return False
        
        try:
            content = flow_file.read_text()
            # Look for multiple steps or complex logic indicators
            return len(content.split('\n')) > 20  # Substantial flow file
        except Exception:
            return False
    
    def _has_state_management(self, output_dir: Path) -> bool:
        """Check for state management patterns."""
        python_files = list(output_dir.rglob("*.py"))
        
        state_keywords = ["state", "status", "transition", "lifecycle", "stage"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in state_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_search_functionality(self, output_dir: Path) -> bool:
        """Check for search functionality."""
        python_files = list(output_dir.rglob("*.py"))
        
        search_keywords = ["search", "query", "find", "retrieve", "index"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in search_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _has_vector_operations(self, output_dir: Path) -> bool:
        """Check for vector operations."""
        python_files = list(output_dir.rglob("*.py"))
        
        vector_keywords = ["vector", "embedding", "similarity", "distance", "semantic"]
        
        for file_path in python_files:
            try:
                content = file_path.read_text().lower()
                if any(keyword in content for keyword in vector_keywords):
                    return True
            except Exception:
                continue
        
        return False
    
    def _print_summary(self):
        """Print test execution summary."""
        logger.info("\n" + "="*80)
        logger.info("END-TO-END TEST SCENARIOS SUMMARY")
        logger.info("="*80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Scenarios: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            logger.info("\nFAILED SCENARIOS:")
            for result in self.results:
                if not result.success:
                    logger.info(f"  - {result.scenario_name}:")
                    for error in result.errors:
                        logger.info(f"    * {error}")
        
        logger.info("\nDETAILED RESULTS:")
        for result in self.results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            logger.info(f"  {result.scenario_name}: {status}")
            logger.info(f"    Pattern: {result.pattern_detected or 'N/A'}")
            logger.info(f"    Files: {len(result.files_generated)}")
            
            # Show validation breakdown
            passed_validations = sum(1 for v in result.validation_results.values() if v)
            total_validations = len(result.validation_results)
            logger.info(f"    Validations: {passed_validations}/{total_validations}")
        
        logger.info("\n" + "="*80)


def main():
    """Main entry point for running end-to-end test scenarios."""
    runner = EndToEndTestRunner()
    
    try:
        results = runner.run_all_scenarios()
        
        # Exit with error code if any tests failed
        failed_count = sum(1 for r in results if not r.success)
        if failed_count > 0:
            logger.error(f"❌ {failed_count} test scenarios failed")
            sys.exit(1)
        else:
            logger.info("🎉 All test scenarios passed!")
            sys.exit(0)
            
    except Exception as e:
        logger.exception("Test runner failed")
        sys.exit(1)
    finally:
        runner.cleanup()


if __name__ == "__main__":
    main()
