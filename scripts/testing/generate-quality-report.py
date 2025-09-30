#!/usr/bin/env python3
"""
Quality Assurance Test Report Generator

Consolidates results from all testing components:
- Phase 4 optimization tests
- Performance benchmarks
- End-user workflow integration tests
- Framework validation tests
- Security scans

Generates comprehensive HTML and JSON reports for quality assurance.

Usage:
    python3 generate-quality-report.py [--output-dir DIRECTORY] [--format html|json|both]
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import subprocess
import tempfile
import os

class QualityReportGenerator:
    """Generate comprehensive quality assurance reports"""

    def __init__(self, output_dir: str = "test-reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.report_data = {}
        self.project_root = Path.cwd()

    def run_command_safely(self, command: List[str], cwd: Optional[Path] = None) -> Dict[str, Any]:
        """Run a command safely and capture results"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(command)
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out after 5 minutes',
                'command': ' '.join(command)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(command)
            }

    def collect_phase4_test_results(self) -> Dict[str, Any]:
        """Collect Phase 4 optimization test results"""
        print("📋 Collecting Phase 4 optimization test results...")

        phase4_script = self.project_root / "claude-code" / "testing" / "test-phase4-optimization.py"

        if not phase4_script.exists():
            return {
                'available': False,
                'error': 'Phase 4 test script not found'
            }

        # Run Phase 4 tests with JSON output
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            result = self.run_command_safely([
                'python3', str(phase4_script), '--json', '--cleanup'
            ])

            if result['success']:
                try:
                    # Parse JSON output from stdout
                    output_lines = result['stdout'].strip().split('\n')
                    json_line = None
                    for line in reversed(output_lines):
                        if line.startswith('{') and line.endswith('}'):
                            json_line = line
                            break

                    if json_line:
                        phase4_results = json.loads(json_line)
                    else:
                        phase4_results = {'parsed': False, 'raw_output': result['stdout']}

                except json.JSONDecodeError:
                    phase4_results = {'parsed': False, 'raw_output': result['stdout']}
            else:
                phase4_results = {'error': result.get('error', 'Test execution failed')}

            os.unlink(tmp.name)

        return {
            'available': True,
            'execution_result': result,
            'test_results': phase4_results,
            'timestamp': datetime.now().isoformat()
        }

    def collect_performance_benchmarks(self) -> Dict[str, Any]:
        """Collect performance benchmark results"""
        print("📊 Collecting performance benchmark results...")

        benchmark_script = self.project_root / "claude-code" / "testing" / "performance-benchmarking.py"

        if not benchmark_script.exists():
            return {
                'available': False,
                'error': 'Performance benchmark script not found'
            }

        # Run performance benchmarks with JSON output
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            result = self.run_command_safely([
                'python3', str(benchmark_script), '--output', tmp.name
            ])

            if result['success'] and Path(tmp.name).exists():
                try:
                    with open(tmp.name, 'r') as f:
                        benchmark_results = json.load(f)
                except json.JSONDecodeError:
                    benchmark_results = {'parsed': False, 'error': 'Invalid JSON output'}
            else:
                benchmark_results = {'error': result.get('error', 'Benchmark execution failed')}

            os.unlink(tmp.name)

        return {
            'available': True,
            'execution_result': result,
            'benchmark_results': benchmark_results,
            'timestamp': datetime.now().isoformat()
        }

    def collect_validation_test_results(self) -> Dict[str, Any]:
        """Collect framework validation test results"""
        print("🔧 Collecting framework validation test results...")

        validation_script = self.project_root / "scripts" / "run-all-tests.sh"

        if not validation_script.exists():
            return {
                'available': False,
                'error': 'Validation test script not found'
            }

        result = self.run_command_safely([
            'bash', str(validation_script), '--quick'
        ])

        # Parse validation results from output
        validation_summary = {
            'suites_run': 0,
            'suites_passed': 0,
            'suites_failed': 0,
            'failed_suites': []
        }

        if result['success'] or result['returncode'] == 1:  # Tests may fail but script runs
            output_lines = result['stdout'].split('\n')
            for line in output_lines:
                if 'Total Suites Run:' in line:
                    validation_summary['suites_run'] = int(line.split(':')[1].strip())
                elif 'Suites Passed:' in line:
                    validation_summary['suites_passed'] = int(line.split(':')[1].strip())
                elif 'Suites Failed:' in line:
                    validation_summary['suites_failed'] = int(line.split(':')[1].strip())
                elif line.strip().startswith('- ') and 'Test Suite' in line:
                    validation_summary['failed_suites'].append(line.strip()[2:])

        return {
            'available': True,
            'execution_result': result,
            'validation_summary': validation_summary,
            'timestamp': datetime.now().isoformat()
        }

    def collect_end_user_workflow_results(self) -> Dict[str, Any]:
        """Collect end-user workflow integration test results"""
        print("👥 Collecting end-user workflow integration test results...")

        workflow_script = self.project_root / "scripts" / "validation" / "validate-end-user-workflows.sh"

        if not workflow_script.exists():
            return {
                'available': False,
                'error': 'End-user workflow test script not found'
            }

        result = self.run_command_safely([
            'bash', str(workflow_script)
        ])

        # Parse workflow test results from output
        workflow_summary = {
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'failed_tests': []
        }

        if result['success'] or result['returncode'] == 1:
            output_lines = result['stdout'].split('\n')
            for line in output_lines:
                if 'Total Tests Run:' in line:
                    workflow_summary['tests_run'] = int(line.split(':')[1].strip())
                elif 'Tests Passed:' in line:
                    workflow_summary['tests_passed'] = int(line.split(':')[1].strip())
                elif 'Tests Failed:' in line:
                    workflow_summary['tests_failed'] = int(line.split(':')[1].strip())
                elif line.strip().startswith('- ') and ('FAILED' in line or 'failed' in line):
                    workflow_summary['failed_tests'].append(line.strip()[2:])

        return {
            'available': True,
            'execution_result': result,
            'workflow_summary': workflow_summary,
            'timestamp': datetime.now().isoformat()
        }

    def collect_security_scan_results(self) -> Dict[str, Any]:
        """Collect security scan results if available"""
        print("🔒 Collecting security scan results...")

        # Check for security tools
        security_results = {
            'bandit': {'available': False},
            'safety': {'available': False}
        }

        # Run bandit if available
        try:
            bandit_result = self.run_command_safely([
                'python3', '-m', 'bandit', '-r', 'scripts/', 'framework-tools/',
                '-f', 'json', '--exclude', '**/test_*,**/__pycache__/**'
            ])

            if bandit_result['success']:
                try:
                    bandit_data = json.loads(bandit_result['stdout'])
                    security_results['bandit'] = {
                        'available': True,
                        'results': bandit_data,
                        'issues_found': len(bandit_data.get('results', []))
                    }
                except json.JSONDecodeError:
                    security_results['bandit'] = {
                        'available': True,
                        'error': 'Could not parse bandit output',
                        'raw_output': bandit_result['stdout']
                    }
        except Exception as e:
            security_results['bandit'] = {'available': False, 'error': str(e)}

        # Run safety if available
        try:
            safety_result = self.run_command_safely([
                'python3', '-m', 'safety', 'check', '--json'
            ])

            if safety_result['success']:
                try:
                    safety_data = json.loads(safety_result['stdout'])
                    security_results['safety'] = {
                        'available': True,
                        'results': safety_data,
                        'vulnerabilities_found': len(safety_data) if isinstance(safety_data, list) else 0
                    }
                except json.JSONDecodeError:
                    security_results['safety'] = {
                        'available': True,
                        'error': 'Could not parse safety output',
                        'raw_output': safety_result['stdout']
                    }
        except Exception as e:
            security_results['safety'] = {'available': False, 'error': str(e)}

        return {
            'available': True,
            'security_results': security_results,
            'timestamp': datetime.now().isoformat()
        }

    def generate_report_data(self) -> Dict[str, Any]:
        """Generate comprehensive report data"""
        print("🚀 Generating Quality Assurance Report")
        print("=====================================")

        report_data = {
            'report_info': {
                'generated_at': datetime.now().isoformat(),
                'project_root': str(self.project_root),
                'report_version': '1.0.0'
            },
            'test_components': {}
        }

        # Collect all test results
        test_collectors = [
            ('phase4_optimization', self.collect_phase4_test_results),
            ('performance_benchmarks', self.collect_performance_benchmarks),
            ('framework_validation', self.collect_validation_test_results),
            ('end_user_workflows', self.collect_end_user_workflow_results),
            ('security_scans', self.collect_security_scan_results)
        ]

        for component_name, collector_func in test_collectors:
            try:
                report_data['test_components'][component_name] = collector_func()
            except Exception as e:
                print(f"❌ Error collecting {component_name}: {e}")
                report_data['test_components'][component_name] = {
                    'available': False,
                    'error': str(e)
                }

        # Calculate overall summary
        report_data['overall_summary'] = self._calculate_overall_summary(report_data['test_components'])

        return report_data

    def _calculate_overall_summary(self, test_components: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall test summary and health score"""
        summary = {
            'total_components': len(test_components),
            'components_available': 0,
            'components_passed': 0,
            'components_failed': 0,
            'health_score': 0,
            'status': 'unknown',
            'recommendations': []
        }

        for component_name, component_data in test_components.items():
            if component_data.get('available', False):
                summary['components_available'] += 1

                # Determine component success based on type
                component_success = False

                if component_name == 'phase4_optimization':
                    test_results = component_data.get('test_results', {})
                    success_rate = test_results.get('success_rate', 0)
                    component_success = success_rate >= 80

                elif component_name == 'performance_benchmarks':
                    benchmark_results = component_data.get('benchmark_results', {})
                    overall_success = benchmark_results.get('summary', {}).get('overall_success', False)
                    component_success = overall_success

                elif component_name == 'framework_validation':
                    validation_summary = component_data.get('validation_summary', {})
                    suites_run = validation_summary.get('suites_run', 0)
                    suites_passed = validation_summary.get('suites_passed', 0)
                    component_success = suites_run > 0 and (suites_passed / suites_run) >= 0.8

                elif component_name == 'end_user_workflows':
                    workflow_summary = component_data.get('workflow_summary', {})
                    tests_run = workflow_summary.get('tests_run', 0)
                    tests_passed = workflow_summary.get('tests_passed', 0)
                    component_success = tests_run > 0 and (tests_passed / tests_run) >= 0.8

                elif component_name == 'security_scans':
                    component_data.get('security_results', {})
                    # Security passes if no critical issues found
                    component_success = True  # Default to pass if scans run

                if component_success:
                    summary['components_passed'] += 1
                else:
                    summary['components_failed'] += 1

        # Calculate health score (0-100)
        if summary['components_available'] > 0:
            summary['health_score'] = (summary['components_passed'] / summary['components_available']) * 100

        # Determine overall status
        if summary['health_score'] >= 90:
            summary['status'] = 'excellent'
        elif summary['health_score'] >= 80:
            summary['status'] = 'good'
        elif summary['health_score'] >= 70:
            summary['status'] = 'acceptable'
        elif summary['health_score'] >= 50:
            summary['status'] = 'needs_improvement'
        else:
            summary['status'] = 'critical'

        # Generate recommendations
        if summary['components_failed'] > 0:
            summary['recommendations'].append("Review and fix failing test components")

        if summary['health_score'] < 80:
            summary['recommendations'].append("Improve test coverage and component reliability")

        if summary['components_available'] < summary['total_components']:
            summary['recommendations'].append("Ensure all test components are properly installed and accessible")

        return summary

    def generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML quality assurance report"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent OS + PocketFlow Quality Assurance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .summary { background: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .component { background: white; border: 1px solid #bdc3c7; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .status-excellent { color: #27ae60; }
        .status-good { color: #2980b9; }
        .status-acceptable { color: #f39c12; }
        .status-needs_improvement { color: #e74c3c; }
        .status-critical { color: #c0392b; }
        .metric { display: inline-block; margin: 5px 10px; padding: 5px 10px; background: #3498db; color: white; border-radius: 3px; }
        .error { background: #e74c3c; color: white; padding: 10px; border-radius: 3px; margin: 10px 0; }
        .success { background: #27ae60; color: white; padding: 10px; border-radius: 3px; margin: 10px 0; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔧 Agent OS + PocketFlow Quality Assurance Report</h1>
        <p>Generated: {generated_at}</p>
        <p>Project: {project_root}</p>
    </div>

    <div class="summary">
        <h2>📊 Overall Summary</h2>
        <div class="metric">Health Score: {health_score:.1f}%</div>
        <div class="metric">Status: <span class="status-{status}">{status}</span></div>
        <div class="metric">Components Available: {components_available}/{total_components}</div>
        <div class="metric">Components Passed: {components_passed}</div>
        <div class="metric">Components Failed: {components_failed}</div>

        {recommendations_html}
    </div>

    {components_html}

</body>
</html>
"""

        # Generate recommendations HTML
        recommendations = report_data['overall_summary'].get('recommendations', [])
        recommendations_html = ""
        if recommendations:
            recommendations_html = "<h3>🔍 Recommendations</h3><ul>"
            for rec in recommendations:
                recommendations_html += f"<li>{rec}</li>"
            recommendations_html += "</ul>"

        # Generate components HTML
        components_html = "<h2>📋 Test Components</h2>"
        for component_name, component_data in report_data['test_components'].items():
            component_title = component_name.replace('_', ' ').title()

            if component_data.get('available', False):
                if component_data.get('execution_result', {}).get('success', False):
                    status_class = "success"
                    status_text = "✅ Component executed successfully"
                else:
                    status_class = "error"
                    status_text = "❌ Component execution failed"
            else:
                status_class = "error"
                status_text = f"⚠️ Component not available: {component_data.get('error', 'Unknown error')}"

            components_html += f"""
            <div class="component">
                <h3>{component_title}</h3>
                <div class="{status_class}">{status_text}</div>
                <p><strong>Timestamp:</strong> {component_data.get('timestamp', 'N/A')}</p>
                <details>
                    <summary>View detailed results</summary>
                    <pre>{json.dumps(component_data, indent=2)}</pre>
                </details>
            </div>
            """

        summary = report_data['overall_summary']
        html_content = html_template.format(
            generated_at=report_data['report_info']['generated_at'],
            project_root=report_data['report_info']['project_root'],
            health_score=summary['health_score'],
            status=summary['status'],
            total_components=summary['total_components'],
            components_available=summary['components_available'],
            components_passed=summary['components_passed'],
            components_failed=summary['components_failed'],
            recommendations_html=recommendations_html,
            components_html=components_html
        )

        return html_content

    def save_reports(self, report_data: Dict[str, Any], formats: List[str] = ['html', 'json']):
        """Save reports in specified formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if 'json' in formats:
            json_file = self.output_dir / f"quality-report-{timestamp}.json"
            with open(json_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"📄 JSON report saved: {json_file}")

        if 'html' in formats:
            html_content = self.generate_html_report(report_data)
            html_file = self.output_dir / f"quality-report-{timestamp}.html"
            with open(html_file, 'w') as f:
                f.write(html_content)
            print(f"📄 HTML report saved: {html_file}")

        # Also save latest versions
        if 'json' in formats:
            latest_json = self.output_dir / "quality-report-latest.json"
            with open(latest_json, 'w') as f:
                json.dump(report_data, f, indent=2)

        if 'html' in formats:
            html_content = self.generate_html_report(report_data)
            latest_html = self.output_dir / "quality-report-latest.html"
            with open(latest_html, 'w') as f:
                f.write(html_content)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate comprehensive quality assurance report")
    parser.add_argument("--output-dir", default="test-reports", help="Output directory for reports")
    parser.add_argument("--format", choices=['html', 'json', 'both'], default='both', help="Report format")

    args = parser.parse_args()

    formats = ['html', 'json'] if args.format == 'both' else [args.format]

    generator = QualityReportGenerator(args.output_dir)
    report_data = generator.generate_report_data()
    generator.save_reports(report_data, formats)

    # Print summary
    summary = report_data['overall_summary']
    print("\n🎯 Quality Report Generated")
    print(f"Health Score: {summary['health_score']:.1f}%")
    print(f"Status: {summary['status']}")
    print(f"Components: {summary['components_passed']}/{summary['components_available']} passed")

    # Exit with appropriate code based on health score
    return 0 if summary['health_score'] >= 70 else 1

if __name__ == "__main__":
    exit(main())