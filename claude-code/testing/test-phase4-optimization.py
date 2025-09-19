#!/usr/bin/env python3
"""
Phase 4 Optimization Testing Suite

Tests the Phase 4 optimization components for document creation subagent refactoring.
Validates parallel processing, context optimization, validation layers, error handling,
and performance monitoring.

Usage:
    python3 test-phase4-optimization.py [--component COMPONENT] [--verbose]
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any
import tempfile

# Add current directory to path for importing our modules
sys.path.append(str(Path(__file__).parent.parent))

try:
    from validation.document_consistency_validator import DocumentConsistencyValidator
    from monitoring.document_creation_metrics import DocumentCreationMetrics
    from optimization.context_optimization_framework import ContextOptimizer
except ImportError:
    print("⚠️  Some optimization modules not available - testing will be limited")


class Phase4OptimizationTester:
    """Test suite for Phase 4 optimization components"""

    def __init__(self, project_root: Path = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.test_results = {}
        self.verbose = False

    def log(self, message: str, level: str = "INFO") -> None:
        """Log message if verbose mode is enabled"""
        if self.verbose or level in ["ERROR", "SUCCESS"]:
            icon = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
            print(f"{icon.get(level, '📝')} {message}")

    def create_test_documents(self) -> Path:
        """Create test documents for validation testing"""
        test_dir = self.project_root / "test-documents"
        test_dir.mkdir(exist_ok=True)

        # Create .agent-os structure
        (test_dir / ".agent-os" / "product").mkdir(parents=True, exist_ok=True)
        (test_dir / ".agent-os" / "checklists").mkdir(parents=True, exist_ok=True)
        (test_dir / "docs").mkdir(exist_ok=True)

        # Create sample mission document
        mission_content = """# Product Mission

> Last Updated: 2025-01-15
> Version: 1.0.0

## Pitch

TestApp is a productivity tool that helps small business owners manage their daily tasks by providing intelligent automation and insights.

## Users

- **Primary User**: 25-40 year old small business owners who struggle with time management
- **Secondary User**: 30-50 year old operations managers who need workflow optimization

## Problems

1. **Time Management**: Small business owners waste 3+ hours daily on repetitive tasks - *Impact*: 30% productivity loss
2. **Task Prioritization**: Poor task organization leads to missed deadlines - *Impact*: 20% revenue loss

## Key Features

### Core Functionality
- **Task Automation**: Intelligent task scheduling and delegation
- **Priority Management**: AI-powered task prioritization

### Advanced Features
- **Analytics Dashboard**: Performance insights and trend analysis
- **Team Collaboration**: Shared workspaces and communication tools

## Differentiators

1. **AI-First Approach**: Built-in machine learning for task optimization
2. **Small Business Focus**: Designed specifically for teams under 20 people

## Architecture Strategy

**Framework**: PocketFlow
**Patterns**: WORKFLOW, TOOL, AGENT
**Complexity**: ENHANCED_WORKFLOW
**Rationale**: Chosen for workflow automation capabilities and scalability
"""

        (test_dir / ".agent-os" / "product" / "mission.md").write_text(mission_content)

        # Create sample tech stack document
        tech_stack_content = """# Tech Stack

> Last Updated: 2025-01-15

## Programming Language
- **Python 3.12**: Modern Python with type hints and async support

## Framework
- **FastAPI**: High-performance web framework for APIs
- **PocketFlow**: Workflow automation framework

## Database
- **PostgreSQL**: Reliable relational database for structured data
- **Redis**: Caching and session storage

## Frontend
- **React 18**: Modern frontend framework
- **TypeScript**: Type-safe JavaScript development

## Deployment
- **Docker**: Containerized deployment
- **Railway**: Cloud hosting platform
"""

        (test_dir / ".agent-os" / "product" / "tech-stack.md").write_text(tech_stack_content)

        # Create sample roadmap document
        roadmap_content = """# Development Roadmap

> Last Updated: 2025-01-15

## Phase 1: Foundation (Weeks 1-4)
- **Task Management Core** [WORKFLOW] - Core task CRUD operations (M)
- **User Authentication** [TOOL] - Login and user management (S)
- **Basic Dashboard** [TOOL] - Simple task overview interface (M)

## Phase 2: Automation (Weeks 5-8)
- **Task Automation** [AGENT] - AI-powered task scheduling (L)
- **Priority Management** [WORKFLOW] - Smart task prioritization (M)
- **Analytics Dashboard** [TOOL] - Performance insights (M)

## Phase 3: Collaboration (Weeks 9-12)
- **Team Collaboration** [WORKFLOW] - Shared workspaces (L)
- **Communication Tools** [TOOL] - In-app messaging (M)
- **Advanced Analytics** [AGENT] - Predictive insights (XL)
"""

        (test_dir / ".agent-os" / "product" / "roadmap.md").write_text(roadmap_content)

        # Create CLAUDE.md
        claude_content = """# Project Instructions

## Agent OS Integration
- Mission document: .agent-os/product/mission.md
- Tech stack: .agent-os/product/tech-stack.md
- Development roadmap: .agent-os/product/roadmap.md

## Workflow Commands
- `/plan-product`: Initialize product planning
- `/create-spec`: Create feature specifications
"""

        (test_dir / "CLAUDE.md").write_text(claude_content)

        self.log(f"Created test documents in {test_dir}")
        return test_dir

    def test_validation_framework(self) -> bool:
        """Test document consistency validation"""
        self.log("Testing document consistency validation framework")

        try:
            test_dir = self.create_test_documents()
            validator = DocumentConsistencyValidator(test_dir)
            validator.run_all_validations()

            report = validator.generate_report()
            self.log(f"Validation completed with {len(validator.issues)} issues found")

            # Test should find some consistency patterns
            success = True
            if not validator.documents:
                success = False
                self.log("No documents were loaded for validation", "ERROR")

            self.test_results['validation_framework'] = {
                'success': success,
                'documents_loaded': len(validator.documents),
                'issues_found': len(validator.issues),
                'report_generated': len(report) > 100
            }

            return success

        except Exception as e:
            self.log(f"Validation framework test failed: {e}", "ERROR")
            self.test_results['validation_framework'] = {'success': False, 'error': str(e)}
            return False

    def test_performance_monitoring(self) -> bool:
        """Test performance monitoring and metrics collection"""
        self.log("Testing performance monitoring framework")

        try:
            # Create temporary metrics database
            with tempfile.TemporaryDirectory() as temp_dir:
                metrics_db = Path(temp_dir) / "test_metrics.db"
                metrics = DocumentCreationMetrics(metrics_db_path=metrics_db)

                # Simulate a document creation session
                metrics.start_session("test_session")

                # Simulate agent executions
                start1 = metrics.record_agent_start("mission-document-creator")
                time.sleep(0.1)  # Simulate work
                metrics.record_agent_completion("mission-document-creator", start1, success=True, token_usage=1500)

                start2 = metrics.record_agent_start("tech-stack-document-creator")
                time.sleep(0.05)  # Simulate work
                metrics.record_agent_completion("tech-stack-document-creator", start2, success=True, token_usage=1200)

                # Finish session
                orchestration_metric = metrics.finish_session(parallel_groups=1)

                # Verify metrics were recorded
                analysis = metrics.analyze_performance(days=1)

                success = True
                if analysis.get('total_sessions', 0) == 0:
                    success = False
                    self.log("No sessions were recorded in metrics", "ERROR")

                if not analysis.get('agent_performance'):
                    success = False
                    self.log("No agent performance data recorded", "ERROR")

                self.test_results['performance_monitoring'] = {
                    'success': success,
                    'sessions_recorded': analysis.get('total_sessions', 0),
                    'agents_tracked': len(analysis.get('agent_performance', {})),
                    'metrics_database_created': metrics_db.exists()
                }

                return success

        except Exception as e:
            self.log(f"Performance monitoring test failed: {e}", "ERROR")
            self.test_results['performance_monitoring'] = {'success': False, 'error': str(e)}
            return False

    def test_context_optimization(self) -> bool:
        """Test context optimization framework"""
        self.log("Testing context optimization framework")

        try:
            optimizer = ContextOptimizer()

            # Create test context data
            test_context = {
                "main_idea": "AI-powered task management for small businesses",
                "key_features": [
                    "Task automation",
                    "Priority management",
                    "Analytics dashboard",
                    "Team collaboration"
                ],
                "target_users": [
                    {"role": "Business owner", "age": "25-40", "context": "Time management struggles"},
                    {"role": "Operations manager", "age": "30-50", "context": "Workflow optimization needs"}
                ],
                "tech_stack": {
                    "backend": "Python FastAPI",
                    "frontend": "React",
                    "database": "PostgreSQL"
                },
                "competitive_analysis": "Detailed competitive analysis text..." * 50,  # Large field
                "business_model": "SaaS subscription model with tiered pricing"
            }

            # Test context analysis
            target_agents = ["mission-document-creator", "tech-stack-document-creator", "roadmap-document-creator"]
            analysis = optimizer.analyze_context_usage(test_context, target_agents)

            # Test optimization
            optimized_contexts = optimizer.create_parallel_contexts(test_context, target_agents)

            success = True
            if not analysis.get('field_usage'):
                success = False
                self.log("Context analysis produced no field usage data", "ERROR")

            if len(optimized_contexts) != len(target_agents):
                success = False
                self.log(f"Expected {len(target_agents)} optimized contexts, got {len(optimized_contexts)}", "ERROR")

            # Check token reduction
            original_size = sum(optimizer._estimate_token_cost(v) for v in test_context.values())
            total_optimized = sum(
                sum(optimizer._estimate_token_cost(v) for v in ctx.values() if not str(v).startswith('_'))
                for ctx in optimized_contexts.values()
            )

            reduction_achieved = total_optimized < (original_size * len(target_agents))

            self.test_results['context_optimization'] = {
                'success': success and reduction_achieved,
                'analysis_completed': bool(analysis.get('field_usage')),
                'contexts_generated': len(optimized_contexts),
                'original_tokens': original_size,
                'optimized_tokens': total_optimized,
                'reduction_achieved': reduction_achieved
            }

            if reduction_achieved:
                reduction_pct = ((original_size * len(target_agents) - total_optimized) /
                               (original_size * len(target_agents))) * 100
                self.log(f"Context optimization achieved {reduction_pct:.1f}% token reduction")

            return success and reduction_achieved

        except Exception as e:
            self.log(f"Context optimization test failed: {e}", "ERROR")
            self.test_results['context_optimization'] = {'success': False, 'error': str(e)}
            return False

    def test_agent_definitions(self) -> bool:
        """Test that all Phase 4 agents are properly defined"""
        self.log("Testing Phase 4 agent definitions")

        expected_agents = [
            "document-orchestration-coordinator.md",
            "document-creation-error-handler.md"
        ]

        success = True
        agents_found = {}

        agents_dir = self.project_root / "claude-code" / "agents"
        for agent_file in expected_agents:
            agent_path = agents_dir / agent_file
            exists = agent_path.exists()
            agents_found[agent_file] = exists

            if not exists:
                success = False
                self.log(f"Agent definition missing: {agent_file}", "ERROR")
            else:
                # Check basic structure
                content = agent_path.read_text()
                required_sections = ["Core Responsibilities", "Output Format", "Context Requirements"]

                missing_sections = []
                for section in required_sections:
                    if section not in content:
                        missing_sections.append(section)

                if missing_sections:
                    self.log(f"Agent {agent_file} missing sections: {missing_sections}", "WARNING")

        self.test_results['agent_definitions'] = {
            'success': success,
            'agents_found': agents_found,
            'total_expected': len(expected_agents),
            'total_found': sum(agents_found.values())
        }

        return success

    def test_optimization_scripts(self) -> bool:
        """Test that optimization scripts are executable"""
        self.log("Testing optimization script functionality")

        scripts = [
            "validation/document-consistency-validator.py",
            "monitoring/document-creation-metrics.py",
            "optimization/context-optimization-framework.py"
        ]

        success = True
        scripts_tested = {}

        for script_path in scripts:
            full_path = self.project_root / "claude-code" / script_path
            exists = full_path.exists()
            scripts_tested[script_path] = {'exists': exists, 'executable': False}

            if not exists:
                success = False
                self.log(f"Optimization script missing: {script_path}", "ERROR")
                continue

            # Test if script is executable (has main function and proper structure)
            try:
                content = full_path.read_text()
                has_main = 'def main()' in content or 'if __name__ == "__main__"' in content
                has_imports = 'import ' in content
                has_classes = 'class ' in content

                executable = has_main and has_imports and has_classes
                scripts_tested[script_path]['executable'] = executable

                if not executable:
                    self.log(f"Script {script_path} may not be properly structured", "WARNING")

            except Exception as e:
                self.log(f"Error checking script {script_path}: {e}", "WARNING")

        self.test_results['optimization_scripts'] = {
            'success': success,
            'scripts_tested': scripts_tested,
            'total_expected': len(scripts),
            'total_found': sum(1 for s in scripts_tested.values() if s['exists'])
        }

        return success

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 4 optimization tests"""
        self.log("🚀 Starting Phase 4 Optimization Test Suite", "SUCCESS")

        test_methods = [
            ('agent_definitions', self.test_agent_definitions),
            ('optimization_scripts', self.test_optimization_scripts),
            ('validation_framework', self.test_validation_framework),
            ('performance_monitoring', self.test_performance_monitoring),
            ('context_optimization', self.test_context_optimization)
        ]

        passed_tests = 0
        total_tests = len(test_methods)

        for test_name, test_method in test_methods:
            self.log(f"\n📋 Running {test_name}...")
            try:
                success = test_method()
                if success:
                    passed_tests += 1
                    self.log(f"✅ {test_name} PASSED", "SUCCESS")
                else:
                    self.log(f"❌ {test_name} FAILED", "ERROR")

            except Exception as e:
                self.log(f"❌ {test_name} CRASHED: {e}", "ERROR")
                self.test_results[test_name] = {'success': False, 'error': str(e)}

        # Final summary
        success_rate = (passed_tests / total_tests) * 100
        self.log(f"\n🎯 Phase 4 Testing Complete: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)", "SUCCESS")

        summary = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': success_rate,
            'individual_results': self.test_results
        }

        return summary

    def cleanup_test_files(self) -> None:
        """Clean up test files and directories"""
        test_dir = self.project_root / "test-documents"
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
            self.log("Cleaned up test documents")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Test Phase 4 optimization components")
    parser.add_argument("--component", help="Test specific component only",
                       choices=['validation', 'monitoring', 'optimization', 'agents', 'scripts'])
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--cleanup", action="store_true", help="Clean up test files after run")
    parser.add_argument("--json", action="store_true", help="Output JSON results")

    args = parser.parse_args()

    tester = Phase4OptimizationTester()
    tester.verbose = args.verbose

    if args.component:
        # Run specific component test
        component_map = {
            'validation': tester.test_validation_framework,
            'monitoring': tester.test_performance_monitoring,
            'optimization': tester.test_context_optimization,
            'agents': tester.test_agent_definitions,
            'scripts': tester.test_optimization_scripts
        }

        if args.component in component_map:
            success = component_map[args.component]()
            result = {'component': args.component, 'success': success, 'details': tester.test_results}
        else:
            print(f"❌ Unknown component: {args.component}")
            return 1
    else:
        # Run all tests
        result = tester.run_all_tests()

    if args.cleanup:
        tester.cleanup_test_files()

    if args.json:
        print(json.dumps(result, indent=2))

    return 0 if result.get('success', result.get('success_rate', 0) > 80) else 1


if __name__ == "__main__":
    exit(main())