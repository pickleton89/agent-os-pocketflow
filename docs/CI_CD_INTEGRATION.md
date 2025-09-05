# CI/CD Integration for PocketFlow

This document explains how to set up continuous integration and deployment (CI/CD) workflows for PocketFlow projects using GitHub Actions.

## Overview

The Agent OS + PocketFlow framework provides automated quality validation tools to ensure your workflows follow best practices and avoid common antipatterns. This integration provides:

- **Continuous Quality Enforcement**: Automatic validation on every push and pull request
- **Early Feedback for Developers**: Catch issues before they reach production
- **Prevention of Regression**: Ensure code quality doesn't degrade over time
- **Documentation of Quality Standards**: Clear reporting on compliance status

## Available Workflows

### 1. Framework Repository Workflow

**File**: `.github/workflows/pocketflow-quality.yml`

This workflow tests the Agent OS + PocketFlow framework itself and includes:

- Multi-Python version testing (3.9-3.12)
- **Framework tool functionality testing** (validates that tools work, not that framework follows its own rules)
- Code linting and formatting on framework code
- Framework-specific tests (generators, setup scripts)
- Security scanning

**Critical Understanding**: This workflow does NOT run PocketFlow validation tools on the framework repository. The framework PROVIDES the validation tools - it doesn't validate itself with them. The tools are meant for END-USER projects to use on their implemented applications.

### 2. End-User Application Workflow Template

**File**: `templates/github-actions/pocketflow-validation.yml`

This template is designed for applications that USE PocketFlow as a dependency and focuses on:

- Application structure validation
- PocketFlow integration testing
- Application-specific linting and testing
- Quality reporting for implemented applications

**Important**: This template does NOT include framework validation tools (those stay in the framework repository). Instead, it validates that your application correctly uses PocketFlow as a dependency.

## Setup Instructions

### For End-User Applications

1. **Copy the template workflow**:
   ```bash
   mkdir -p .github/workflows
   cp templates/github-actions/pocketflow-validation.yml .github/workflows/
   ```

2. **Ensure PocketFlow is installed as a dependency**:
   ```bash
   # Your project should have PocketFlow in dependencies
   uv add pocketflow
   # OR
   pip install pocketflow
   ```

3. **Customize for your application** (optional):
   - Modify the trigger paths to match your source code layout (src/, workflows/, app/)
   - Adjust Python version requirements
   - Add application-specific validation steps

4. **Commit and push**:
   ```bash
   git add .github/workflows/pocketflow-validation.yml
   git commit -m "Add PocketFlow application validation workflow"
   git push
   ```

### For Framework Development

The framework repository already includes the complete workflow at `.github/workflows/pocketflow-quality.yml`.

## Validation Tools

**Important Context**: These tools are PROVIDED BY the framework repository but are designed to be USED BY end-user projects. The framework repository does not run these tools on itself.

### Best Practices Validator

**Script**: `scripts/validation/validate-best-practices.py`

**Purpose**: Tool for end-user projects to validate their implemented PocketFlow applications.

**What it validates**:
- Node lifecycle method usage in implemented applications
- Proper batch node implementation
- Utility function patterns  
- Shared store access patterns

**Who uses it**: End-user projects that have implemented PocketFlow workflows (NOT the framework repository itself)

**Usage by End-User Projects**:
```bash
# End-user projects copy this tool and run it on their implemented code
python scripts/validation/validate-best-practices.py

# Validate specific implemented workflow directory  
python scripts/validation/validate-best-practices.py --workflow src/workflows/

# Run specific checks only
python scripts/validation/validate-best-practices.py --checks lifecycle,batch
```

**Framework Repository Note**: The framework tests that this tool can be imported and is functional, but does NOT run it on framework templates (which contain intentional TODO placeholders).

### Antipattern Detector

**Script**: `pocketflow-tools/antipattern_detector.py`

**Purpose**: Tool for end-user projects to identify common implementation mistakes in their PocketFlow applications.

**What it detects in implemented applications**:
- Monolithic node syndrome
- Shared store access in exec() methods
- Lifecycle method confusion
- Business logic in utilities
- Untestable node design

**Who uses it**: End-user projects that have implemented PocketFlow workflows (NOT the framework repository itself)

**Usage by End-User Applications**:
```bash
# End-user projects copy this tool and run it on their implemented code
python pocketflow-tools/antipattern_detector.py src/

# Scan with failure on violations
python pocketflow-tools/antipattern_detector.py src/ --fail-on-violations

# Generate JSON report for implemented applications
python pocketflow-tools/antipattern_detector.py src/ --format json --output report.json
```

**Framework Repository Note**: The framework tests that this tool can be imported and is functional. The framework does NOT run antipattern detection on itself because framework templates intentionally contain placeholder patterns that would be flagged as "antipatterns" but are actually design features.

## Workflow Features

### Quality Reporting

Both workflows generate comprehensive quality reports that include:

- **Best Practices Compliance**: Detailed analysis of adherence to PocketFlow patterns
- **Antipattern Detection Results**: List of detected issues with severity levels
- **Recommendations**: Specific suggestions for fixing identified problems
- **Workflow Structure Analysis**: Validation of overall project organization

### PR Integration

When running on pull requests, the workflows:

- **Post Quality Reports**: Add comments to PRs with validation results
- **Fail on Critical Issues**: Prevent merging when critical antipatterns are detected
- **Upload Artifacts**: Save detailed reports for later analysis

### Flexible Configuration

The workflows support:

- **Severity Filtering**: Only show issues above a certain severity level
- **Custom File Patterns**: Include/exclude specific files or directories
- **Multiple Output Formats**: Console, JSON, or Markdown reporting
- **Parallel Execution**: Run multiple validation checks simultaneously

## Integration with Development Workflow

### Pre-commit Hooks

For immediate feedback, consider setting up pre-commit hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pocketflow-best-practices
        name: PocketFlow Best Practices
        entry: python scripts/validation/validate-best-practices.py
        language: system
        files: \.py$
      
      - id: pocketflow-antipatterns
        name: PocketFlow Antipattern Detection
        entry: python pocketflow-tools/antipattern_detector.py
        language: system
        files: \.py$
        args: [--fail-on-violations, --severity, high]
```

### IDE Integration

The validation tools can be integrated into IDEs:

```bash
# VS Code task.json example
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate PocketFlow",
      "type": "shell",
      "command": "python",
      "args": ["scripts/validation/validate-best-practices.py", "--verbose"],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always"
      }
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### For End-User Applications:

1. **"PocketFlow not found - ensure it's in dependencies"**
   - Add PocketFlow to your project dependencies: `uv add pocketflow`
   - Ensure your pyproject.toml or requirements.txt includes PocketFlow

2. **"No standard source directory found"**
   - Create a `src/`, `workflows/`, or `app/` directory for your application code
   - Update the workflow triggers to match your project structure

3. **"No workflow files found in application"**
   - Create Python files with your PocketFlow Node implementations
   - Ensure your implemented workflows are in the expected directories

#### For Framework Development:

4. **"Best practices validator not found"**
   - This error should only occur in the framework repository
   - Check that `scripts/validation/validate-best-practices.py` exists

5. **Python version compatibility issues**
   - Update the workflow to use your required Python version
   - Check that all dependencies support the Python version

### Debug Mode

Enable verbose output for detailed troubleshooting:

```bash
# Verbose best practices validation
python scripts/validation/validate-best-practices.py --verbose

# Verbose antipattern detection
python pocketflow-tools/antipattern_detector.py --verbose
```

## Customization

### Adding Custom Checks

You can extend the validation by:

1. **Creating custom validators** in the `scripts/validation/` directory
2. **Adding new antipattern rules** to the detector configuration
3. **Modifying workflow triggers** to run on specific file changes
4. **Adding notification integrations** (Slack, email, etc.)

### Organization-Specific Standards

For organization-wide standards:

1. Fork the Agent OS + PocketFlow framework
2. Modify the validation rules to match your standards
3. Distribute your customized framework to development teams
4. Update workflows to use your custom validation rules

## Best Practices for CI/CD

1. **Run validation on every PR**: Catch issues early in the development process
2. **Use appropriate severity levels**: Don't let minor issues block critical fixes
3. **Review reports regularly**: Use quality trends to improve development practices
4. **Automate fixes when possible**: Use formatters and auto-fixers for common issues
5. **Educate the team**: Share validation results and best practices with developers

## Performance Considerations

- **Parallel execution**: The workflows run multiple checks simultaneously
- **Incremental validation**: Only validate changed files when possible
- **Artifact caching**: Cache dependencies between workflow runs
- **Smart triggers**: Only run on relevant file changes

## Security

The workflows include security scanning features:

- **Dependency vulnerability scanning** with Safety
- **Code security analysis** with Bandit
- **Secure credential handling** in CI/CD environment
- **Artifact encryption** for sensitive reports

---

For more information about PocketFlow best practices, see:
- [PocketFlow Best Practices Guide](POCKETFLOW_BEST_PRACTICES.md)
- [Common Antipatterns Documentation](COMMON_ANTIPATTERNS.md)
- [Agent OS Setup Instructions](README.md)