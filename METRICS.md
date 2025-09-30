# Codebase Metrics

> Accurate baseline metrics for the Agent OS + PocketFlow framework repository
> Last Updated: 2025-09-30

## Source Code Statistics (Excluding Dependencies)

### Lines of Code
- **Python LOC**: ~24,261 lines
- **Total Source LOC**: ~74,360 lines (includes shell scripts, docs, configs)
- **File Types Included**: `.py`, `.sh`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`
- **Note**: Total LOC includes this METRICS.md file and CHANGELOG.md updates created during baseline documentation

### Test Coverage
- **Test Files**: 8 files
  - `.agent-os/workflows/cli-smoke/customeragent/tests/test_nodes.py` (15 test functions)
  - `framework-tools/complex_scenario_tests.py` (9 test functions)
  - `pocketflow_tools/generators/test_generators.py` (7 test functions)
  - `framework-tools/test_smart_features.py` (6 test functions)
  - `claude-code/testing/test-phase4-optimization.py` (6 test functions)
  - `.agent-os/workflows/cli-smoke/customeragent/tests/test_flow.py` (2 test functions)
  - `.agent-os/workflows/cli-smoke/customeragent/tests/test_api.py` (2 test functions)
  - `framework-tools/simple_pattern_test.py` (1 test function)
- **Test Functions**: 48 test functions across 8 test files
- **Test Framework**: pytest

### Validation Infrastructure
- **Validation Scripts**: 18 shell-based validation suites in `scripts/validation/`
- **Total Scripts**: 29 scripts (shell + python) in `scripts/` directory
- **Script Types**: Integration tests, orchestration validation, installer tests

## Methodology

### Exclusions
These metrics **exclude** the following directories to provide accurate codebase size:
- `.venv/` - Virtual environment dependencies (~300,000+ lines)
- `venv/` - Alternative virtual environment location
- `*/site-packages/*` - Python package installations

### Counting Commands
```bash
# Python LOC (excluding .venv)
find . -type f -name "*.py" ! -path "./.venv/*" ! -path "./venv/*" ! -path "*/site-packages/*" | xargs wc -l | tail -1

# Total Source LOC (excluding .venv)
find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" \) ! -path "./.venv/*" ! -path "./venv/*" ! -path "*/site-packages/*" | xargs wc -l | tail -1

# Test files
find . -type f \( -name "test*.py" -o -name "*test.py" \) | grep -v ".venv" | wc -l

# Test functions (includes both module-level and class-based tests, excludes template examples)
grep -r "def test_" . --include="*.py" --exclude-dir=".venv" --exclude-dir="templates" | wc -l

# Test function breakdown per file (excludes template examples)
grep -n "def test_" . --include="*.py" --exclude-dir=".venv" --exclude-dir="templates" -r | cut -d: -f1 | sort | uniq -c

# Validation scripts
ls -1 scripts/validation/*.sh | wc -l
```

## Interpretation Notes

### Framework vs Application Code
This repository is the **framework itself**, not an application built with the framework:
- Template generators with intentional TODO placeholders
- Setup and installation scripts for end-user projects
- Validation infrastructure for framework testing
- Documentation and configuration examples

### Expected Characteristics
- **Generated template code** contains intentional placeholders (not bugs)
- **Import errors in templates** are expected (dependencies installed in target projects)
- **Missing implementations** in generated files are by design
- **Test coverage** focuses on framework functionality, not application logic

### Comparison Context
**Previous inflated report**: ~300,000 LOC (included `.venv/` dependencies)
**Actual codebase**: ~74,360 LOC (source code only)
**Accuracy improvement**: 4x reduction in reported size

## Repository Structure Overview

```
agent-os-pocketflow/
├── .agent-os/              # Framework template files (installed in user projects)
├── claude-code/            # Claude Code agent definitions and testing
├── framework-tools/        # Core framework utilities and generators
├── pocketflow_tools/       # PocketFlow integration tools
├── scripts/                # Validation and testing scripts
│   ├── validation/         # 18 validation suites
│   └── lib/                # Shared script utilities
├── setup/                  # Installation scripts (base.sh, project.sh)
└── instructions/           # Agent orchestrator instructions
```

## Historical Context

This metrics baseline was created to address inflated technical debt reports that incorrectly included `.venv/` dependencies in codebase size calculations. These accurate metrics set realistic expectations for:
- Framework development scope
- Maintenance burden assessment
- Technical debt prioritization
- Contributor onboarding expectations

---

**Note**: These figures represent the framework repository itself. End-user projects using this framework will have their own separate metrics based on their application code.
