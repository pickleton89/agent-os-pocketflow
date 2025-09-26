# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

**CRITICAL**: This IS the Agent OS + PocketFlow framework itself — NOT a project using it.

This repository:
- Generates PocketFlow templates for other projects
- Contains setup scripts, validation tools, and code generators  
- Template placeholders and TODO stubs are intentional design features
- Dependencies support template generation, not application runtime

**Key Principle**: Missing implementations in generated templates are features, not bugs. This framework creates starting points for developers, not finished applications.

## Quick Development Setup

### Environment Setup
```bash
# Initialize virtual environment with user preferences
uv init --python 3.13
uv add --dev pytest ruff
uv add pyyaml

# Or using existing pyproject.toml
uv sync --dev
```

### Framework Development Verification
```bash
# Test the framework itself (essential tests only)
./scripts/run-all-tests.sh --quick

# Full validation suite (75+ tests)
./scripts/run-all-tests.sh

# Test specific components
./scripts/validation/validate-integration.sh
./scripts/validation/validate-pocketflow.sh
```

### Generator Testing
```bash
cd framework-tools
python3 run_end_to_end_tests.py
python3 simple_pattern_test.py
python3 complex_scenario_tests.py

# View generated examples (with intentional placeholders)
ls -la testcontentanalyzer/
```

## Architecture Overview

### Two-Phase Installation System
The framework creates a two-phase installation architecture for end-users:

```
~/.agent-os/                    # Base Installation (Framework)
├── instructions/               # Core Agent OS instructions
├── standards/                  # Customizable coding standards
├── framework-tools/           # PocketFlow generators & validators
├── templates/                 # PocketFlow application templates
└── setup/
    ├── project.sh            # Project installation script
    └── update-project.sh     # Project update script

your-project/                   # Project Installation (Self-contained)
├── .agent-os/                 # Project-specific Agent OS files
│   ├── instructions/          # Copied from base installation
│   ├── standards/             # Copied from base installation
│   ├── framework-tools/      # PocketFlow tools for this project
│   └── config.yml            # Project configuration
├── .claude/                   # Claude Code integration (if enabled)
│   ├── commands/              # Agent OS slash commands
│   └── agents/               # Specialized AI agents
└── [your project files]
```

### Core Components

#### Framework Directory Structure
- `framework-tools/` - Python generators, validators, and tools
- `scripts/validation/` - Comprehensive test suites (75+ tests)
- `setup/` - Installation scripts for end-users
- `templates/` - Template systems for code generation
- `standards/` - Development standards and guidelines
- `instructions/` - Agent OS instruction files
- `.claude/agents/` - AI agents for end-user projects

#### Key Generator Files
- `framework-tools/pattern_analyzer.py` - PocketFlow pattern detection
- `framework-tools/template_validator.py` - Generated code validation
- `framework-tools/dependency_orchestrator.py` - Dependency management
- `framework-tools/smart_cli.py` - CLI interface for generators

## Common Development Tasks

### Running Tests
```bash
# Quick framework validation (3 essential tests)
./scripts/run-all-tests.sh --quick

# Full test suite with verbose output
./scripts/run-all-tests.sh --verbose

# Continue on errors for debugging
./scripts/run-all-tests.sh --continue

# Test individual suites
./scripts/validation/validate-configuration.sh
./scripts/validation/validate-integration.sh
./scripts/validation/validate-orchestration.sh
```

### Linting and Code Quality
```bash
# The framework uses ruff for linting (configured in pyproject.toml)
ruff check .
ruff format .

# Run Python tests in framework-tools
cd framework-tools
python3 -m pytest test_*.py -v
```

### Generator Development
```bash
# Test pattern analysis and smart features
cd framework-tools
python3 pattern_analyzer.py --help
python3 test_smart_features.py

# Validate generated templates
python3 template_validator.py

# Test CLI interface
python3 smart_cli.py --help
```

### Template Validation
```bash
# Comprehensive template validation
./scripts/validation/validate-pocketflow.sh

# Test specific patterns
cd framework-tools
python3 simple_pattern_test.py
python3 complex_scenario_tests.py
```

## Installation Commands

### For Framework Development
```bash
# Clone and setup for framework development
git clone https://github.com/pickleton89/agent-os-pocketflow.git
cd agent-os-pocketflow
uv sync --dev

# Test framework components
./scripts/run-all-tests.sh
```

### For End-User Installation (what the framework provides)
```bash
# Auto-detect installation
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash

# Manual two-phase installation
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash -s -- --claude-code
cd your-project
~/.agent-os/setup/project.sh --claude-code
```

## PocketFlow Integration

### Supported Patterns
The framework automatically generates templates for:
- **Agent Pattern** - Single LLM agent for conversational interfaces
- **Workflow Pattern** - Multi-step processing pipelines  
- **RAG Pattern** - Retrieval-augmented generation systems
- **Multi-Agent Pattern** - Coordinated teams of specialized agents
- **MapReduce Pattern** - Parallel processing workflows
- **Structured Output** - Type-safe data extraction

### Pattern Analysis
```bash
# Analyze requirements for optimal pattern
cd framework-tools
python3 pattern_analyzer.py analyze "your requirements text"

# Test end-to-end scenarios
python3 end_to_end_test_scenarios.py
```

### Template Generation
```bash
# Generate complete PocketFlow application (12+ files)
cd framework-tools
# Use smart CLI for generation
python3 smart_cli.py generate --pattern workflow --name your-app

# Run comprehensive tests
python3 run_end_to_end_tests.py

# What gets generated:
# - main.py (FastAPI application)
# - nodes.py (PocketFlow nodes with TODO placeholders)
# - flow.py (Orchestration logic)  
# - router.py (API endpoints)
# - schemas/models.py (Pydantic models)
# - tests/ (Comprehensive test suite)
# - docs/design.md (Architecture documentation)
```

## Claude Code Integration

### Enabling Claude Code
End-users enable Claude Code integration with the `--claude-code` flag during installation.

### Generated Slash Commands
The framework generates these slash commands for end-user projects:
- `/plan-product` - Define product vision and roadmap
- `/analyze-product` - Add Agent OS to existing projects
- `/create-spec` - Detail feature requirements  
- `/execute-tasks` - Create and implement features systematically

### Agent Configuration
- `.claude/agents/pocketflow-orchestrator.md` - Main orchestration agent for end-users
- `.claude/commands/` - Generated slash command implementations

## Maintenance and Updates

### Updating Framework Components
```bash
# Update base installation (preserves customizations)
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash -s -- --overwrite-instructions --claude-code

# Update PocketFlow tools only
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash -s -- --update-framework-tools

# Update project installations
~/.agent-os/setup/update-project.sh --update-all
```

### Framework Version Management
```bash
# Check current version
cat pyproject.toml | grep version

# Update version and changelog
# Edit pyproject.toml version
# Update CHANGELOG.md

# Tag release
git tag -a v1.4.1 -m "Release v1.4.1"
git push origin v1.4.1
```

## Testing and Validation

### Repo-Type Aware Testing
The framework auto-detects whether it's running in framework mode or project mode:

```bash
# Framework mode (this repo) - runs framework-focused tests
./scripts/run-all-tests.sh

# Force project mode for testing
REPO_TYPE=project ./scripts/run-all-tests.sh

# Check repo detection
./scripts/lib/repo-detect.sh
```

### Validation Suites
- **Configuration**: Framework configuration validation
- **Integration**: Core integration validation with light sanity checks in framework mode
- **PocketFlow Tools**: Framework tool component validation
- **CLI Smoke**: CLI smoke tests (help/invalid YAML/valid run)
- **Python Tests**: Framework Python smoke and comprehensive tests

### End-to-End Testing
```bash
# Test complete workflow generation
./scripts/validation/validate-end-to-end-scenarios.sh

# Test user experience flows
./scripts/validation/validate-user-experience.sh

# Validate generated templates
./scripts/validation/validate-design-docs.sh
```

## Common Issues and Solutions

### Framework Development Issues

**Import errors in generated code**
- This is expected! Generated templates have placeholder imports for PocketFlow
- These are resolved when templates are deployed to end-user projects

**"TODO placeholders should be implemented"**
- TODOs in generated templates are intentional design features
- They guide developers on what to customize in their projects

**Tests failing for generated applications**
- Framework tests validate the generation process, not the generated applications
- Generated apps are templates with intentional placeholders

### Installation Issues
```bash
# Permission denied errors
chmod +w ~/.agent-os
chmod +w .

# Missing base installation
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash -s -- --claude-code

# Clean reinstall
rm -rf ~/.agent-os
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash -s -- --claude-code
```

## Framework vs Usage Distinction

### Framework Development (This Repository)
- ✅ Improve generator logic, validation scripts, template quality
- ✅ Test framework components and generation process
- ✅ Template placeholders and TODO stubs are intentional features
- ❌ Don't install PocketFlow as dependency (it's for generated projects)
- ❌ Don't try to "fix" TODO placeholders (they're educational templates)
- ❌ Don't expect working imports in generated templates

### Framework Usage (End-User Projects)
- Where PocketFlow gets installed as a dependency
- Where generated templates become working applications
- Where the orchestrator agent runs and is useful
- Where placeholder code gets implemented

## Documentation Links

- [README.md](README.md) - Complete framework documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Framework development guide
- [CLAUDE.md](CLAUDE.md) - Framework vs usage distinction
- [docs/](docs/) - Detailed architecture and implementation docs
- [Agent OS Docs](https://buildermethods.com/agent-os) - Original Agent OS documentation
- [PocketFlow Docs](https://the-pocket.github.io/PocketFlow/) - PocketFlow framework documentation