# Contributing to Agent OS + PocketFlow Framework

## ⚠️ IMPORTANT: This IS the Framework Repository

**You are viewing the Agent OS + PocketFlow framework itself - NOT a project using it.**

| Framework Repository (This Repo) | Usage Repository (End-User Projects) |
|----------------------------------|-------------------------------------|
| 🏗️ **We BUILD** the generator | 🚀 **They USE** generated templates |
| 🔧 **We CREATE** template systems | ✅ **They IMPLEMENT** business logic |
| 📝 **We WRITE** placeholder TODOs | 💻 **They COMPLETE** placeholder TODOs |
| 🧪 **We TEST** the framework itself | ✅ **They TEST** their applications |
| 📦 **Dependencies**: Template generation tools | 📦 **Dependencies**: PocketFlow + runtime libs |

**Key Principle**: Missing implementations in generated templates are **features, not bugs**. This framework creates starting points for developers, not finished applications.

**Framework Development (this repo):**
- Improve generator logic in [`.agent-os/workflows/generator.py`](./.agent-os/workflows/generator.py)
- Enhance validation scripts in [`./scripts/validation/`](./scripts/validation/)
- Develop the system that creates workflows for others
- Template placeholders and TODO stubs are intentional design features

**Framework Usage (your projects):**
- Where you install PocketFlow as a dependency
- Where generated templates become working applications  
- Where the orchestrator agent is useful for planning
- Where placeholder code gets implemented

> **New Contributors:** You're working on the meta-system that generates educational templates, not implementing those templates.

## Framework Development Setup

**This repository IS the framework** - these instructions are for contributing to and improving the framework itself.

### Getting Started with Framework Development

```bash
# Clone the framework repository for development
git clone https://github.com/pickleton89/agent-os-pocketflow.git
cd agent-os-pocketflow

# Install framework development dependencies
uv init
uv add --dev pytest ruff ty

# Test the framework itself
./scripts/run-all-tests.sh

# Verify framework components
ls -la setup/  # Contains base.sh and project.sh for end-users
ls -la pocketflow-tools/  # Contains generator and validation tools
```

**End-User Installation**: This framework provides `setup/base.sh` and `setup/project.sh` scripts that end-users run to install the framework. End-user installation instructions are in the main [README.md](README.md).

### Framework Architecture: v1.4.0 Two-Phase System

**What the Framework Creates for End-Users:**
- **Base Installation** (`~/.agent-os/`): Shared standards and templates
- **Project Installation** (`.agent-os/`): Self-contained copies for each project  
- **Generated Templates**: PocketFlow applications with educational placeholders

**Framework Benefits Delivered:**
- **No external references**: Projects become self-contained  
- **Team collaboration**: Generated `.agent-os/` directories are committable
- **Project customization**: Different standards per project
- **Template consistency**: All projects follow framework patterns

### Framework Code Generation System

**What This Framework Generates:** 
This meta-framework includes a Python-based generator that creates educational PocketFlow templates with intentional placeholder TODOs. Framework developers work on improving this generation system.

**Framework Development Testing:**
```bash
# Test the generator in framework repository
cd pocketflow-tools
python3 generator.py example-workflow-spec.yaml
python3 test-generator.py  # smoke
python3 test_full_generation_with_dependencies.py  # comprehensive

# View generated template examples (with intentional placeholders)
ls -la testcontentanalyzer/  # Framework validation example
```

## Core Framework Components

### 🔧 Generator System ([`.agent-os/workflows/generator.py`](./.agent-os/workflows/generator.py))
- Creates complete PocketFlow projects from YAML specs
- Generates 12+ files per workflow pattern
- Template substitution and validation system

### ✅ Validation Framework ([`./scripts/validation/`](./scripts/validation/))
- 75+ tests ensuring framework reliability
- Integration, orchestration, and end-to-end validation  
- Template Validator agent with comprehensive quality checks
- Run with [`./scripts/run-all-tests.sh`](./scripts/run-all-tests.sh)

### 🤖 Sub-Agents System ([`docs/template-generation/sub-agents/`](docs/template-generation/sub-agents/))
- **Pattern Analyzer Agent**: Analyzes requirements and identifies optimal PocketFlow patterns
- **Template Validator Agent**: Validates generated templates for structural correctness and educational value
- **Dependency Orchestrator Agent**: Manages Python tooling and dependency configuration
- Intelligent coordination with performance caching (100x+ speedups on repeated requests)
- Framework vs usage distinction enforcement throughout template generation

### 📋 Template System ([`templates/`](templates/))
- PocketFlow, FastAPI, and task templates
- Variable substitution and code generation
- Standards enforcement and best practices

### 🎯 Standards & Guidelines ([`standards/`](standards/))
- [PocketFlow Guidelines](standards/pocket-flow.md) - Framework patterns and best practices
- [Code Style](standards/code-style.md) - Python, FastAPI, and testing standards
- [Tech Stack](standards/tech-stack.md) - Technology choices and rationale

## Framework Architecture Overview

This integration combines the best of both frameworks in a **4-phase implementation** that creates an intelligent, self-orchestrating development platform:

```
Agent OS (Workflow Management) + PocketFlow (LLM Orchestration) = Intelligent Development Platform
```

### Implementation Architecture

**Phase 1: Modular Foundation** ✅ Complete
- Modular `.agent-os/instructions/{core,extensions,orchestration}` architecture
- Extension system for conditional feature logic
- Cross-file coordination framework with dependency management

**Phase 2: Orchestration System** ✅ Complete  
- PocketFlow Orchestrator Agent with intelligent planning capabilities
- Automatic orchestrator invocation for LLM/AI features and complex tasks
- Cross-file coordination with validation gates and error handling

**Phase 3: Templates & Code Generation** ✅ Complete
- Comprehensive workflow generator creating 12+ files per PocketFlow pattern
- Support for all PocketFlow patterns (Agent, Workflow, RAG, MapReduce, Multi-Agent, Structured Output)
- Complete template system with auto-generation and variable substitution

**Phase 4: Integration Testing & Setup** ✅ Complete
- Production-ready setup script with 9-phase installation process
- Comprehensive validation framework with 75+ tests across 5 test suites
- End-to-end testing with 100% pass rate and quality assurance

### Key Integration Components

- **Streamlined Repository Structure**: Single source of truth eliminating 5x duplication
- **PocketFlow Orchestrator**: AI agent for strategic planning and workflow coordination  
- **Workflow Generator**: Python system creating complete PocketFlow implementations from YAML specs
- **Validation Framework**: 5 comprehensive test suites ensuring system reliability
- **Design-First Enforcement**: Mandatory design documents with blocking mechanisms
- **Quality Gates**: Ruff linting, ty type checking, and pytest integration
- **Template System**: Auto-generation of working PocketFlow, FastAPI, and task templates

## Repository Structure

This integrated repository contains:

```
agent-os-pocketflow/
├── .agent-os/                    # Core Agent OS integration
│   ├── instructions/             # Modular instruction system
│   │   ├── core/                 # Core workflow instructions
│   │   ├── extensions/           # PocketFlow-specific extensions
│   │   └── orchestration/        # Cross-file coordination
│   ├── templates/                # Template system
│   │   ├── pocketflow-templates.md
│   │   ├── fastapi-templates.md
│   │   └── task-templates.md
│   ├── workflows/                # Generated workflows
│   │   ├── generator.py          # Workflow generation engine
│   │   └── examples/             # Example implementations
│   └── scripts/                  # Validation and testing
├── .claude/                      # Claude Code integration
│   └── agents/
│       └── pocketflow-orchestrator.md  # AI planning agent
├── scripts/                      # Setup and validation scripts
│   ├── run-all-tests.sh         # Master test runner
│   ├── validate-integration.sh   # Integration validation
│   └── validation/               # 5 comprehensive test suites
├── docs/                         # Documentation
├── templates/                    # Global templates
├── standards/                    # Development standards
└── instructions/                 # Core instruction files
```

## Integration Features & Capabilities

### 🎯 Intelligent Orchestration
- **PocketFlow Orchestrator Agent**: AI planning agent automatically invoked for complex tasks
- **Design-First Enforcement**: Mandatory `docs/design.md` with blocking mechanisms before implementation
- **Cross-File Coordination**: Robust dependency management preventing execution without prerequisites
- **Quality Gates**: Pre-commit validation with ruff linting, ty type checking, and pytest testing

### 🔧 Workflow Generation System
- **Comprehensive Generator**: Creates 12+ files per workflow from YAML specifications
- **All PocketFlow Patterns**: Support for Agent, Workflow, RAG, MapReduce, Multi-Agent, Structured Output
- **Template System**: Auto-generation with variable substitution and proper file structure
- **Validation Framework**: Generated code quality assurance with comprehensive error reporting

### 📊 Validation & Testing
- **75+ Comprehensive Tests**: 5 test suites covering integration, orchestration, design, PocketFlow, and end-to-end
- **Master Test Runner**: Quick mode (3 essential tests) and full mode (5 comprehensive suites)
- **Production Readiness**: 100% pass rate validation ensuring system reliability
- **Quality Assurance**: Integration with development toolchain for comprehensive validation

### 🚀 Production-Ready Setup
- **Setup Script v2.0.0**: 9-phase installation process with comprehensive validation
- **Repository Streamlining**: Eliminated 5x duplication with single source of truth architecture
- **Comprehensive Error Handling**: Detailed feedback and validation throughout installation
- **Integration Validation**: Complete system health checks and dependency verification

## Framework Documentation

### Development Resources
- **[Framework Development Guide](docs/framework-development/QUICKSTART.md)** - Get started contributing
- **[Framework Testing](docs/framework-development/TESTING.md)** - Testing the framework itself
- **[Architecture Documentation](docs/architecture/)** - System internals and design
- **[Template Generation Overview](docs/template-generation/README.md)** - How the framework creates templates
- **[Sub-Agents System](docs/template-generation/sub-agents/overview.md)** - Template enhancement agents
- **[Placeholder Philosophy](docs/template-generation/placeholders.md)** - Why TODOs are features
- **[Complete Documentation Hub](docs/)** - Organized documentation with clear navigation
- **Generated Examples**: Working PocketFlow implementations in `.agent-os/workflows/examples/`

### External Resources
- **[Agent OS Docs](https://buildermethods.com/agent-os)** - Original Agent OS documentation and guides
- **[PocketFlow Docs](https://the-pocket.github.io/PocketFlow/)** - Complete PocketFlow framework documentation
- **[PocketFlow GitHub](https://github.com/The-Pocket/PocketFlow)** - Source code and examples

## Testing the Framework

### Quick Test (Framework Validation)
```bash
./scripts/run-all-tests.sh --quick
```

### Full Test Suite (All 75+ Tests)
```bash
./scripts/run-all-tests.sh
```

### Individual Test Suites
```bash
# Integration tests
./scripts/validation/validate-integration.sh

# Orchestration tests  
./scripts/validation/validate-orchestration.sh

# Design validation
./scripts/validation/validate-design.sh

# PocketFlow validation
./scripts/validation/validate-pocketflow.sh

# End-to-end tests
./scripts/validation/validate-end-to-end.sh
```

### Generator Testing
```bash
cd pocketflow-tools
python3 test-generator.py
python3 test_full_generation_with_dependencies.py
```

## Development Workflow

1. **Fork and Clone**: Fork this repository and clone your fork
2. **Install Dependencies**: Run `uv init && uv add --dev pytest ruff ty`
3. **Run Tests**: Ensure all tests pass with `./scripts/run-all-tests.sh`
4. **Make Changes**: Improve generator logic, templates, or validation
5. **Test Changes**: Run relevant test suites to validate your changes
6. **Document**: Update documentation if needed
7. **Submit PR**: Create a pull request with clear description

## Getting Help

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/pickleton89/agent-os-pocketflow/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/pickleton89/agent-os-pocketflow/discussions)
- **Documentation**: Check the [docs/](docs/) directory for detailed guides

## Integration Development Story

This integration represents a **real-world demonstration** of the Agentic Coding methodology in action - transforming AI coding from documentation-focused (6.5/10) to workflow-enforced (9/10) intelligent development.

**Built with Agentic Coding**: This entire 4-phase integration was developed using the Agentic Coding methodology with [Claude Code](https://claude.ai/code) as the AI development partner. The project exemplifies the "humans design, agents code" philosophy:

**Phase-by-Phase Development**:
- **Human-led Strategic Design**: 4-phase implementation plan, architecture decisions, integration requirements
- **AI-assisted Implementation**: 75+ validation tests, workflow generation system, orchestration framework
- **Collaborative Quality Assurance**: Comprehensive validation framework ensuring production readiness
- **Iterative Integration**: Cross-file coordination, design-first enforcement, and quality gates

**Production Results**:
- **Complete System Integration**: All 4 phases implemented with 100% validation success
- **Intelligent Orchestration**: Automatic PocketFlow orchestrator invocation for complex tasks
- **Quality-First Development**: Mandatory design documents, validation gates, and comprehensive testing
- **Production-Ready Framework**: 9-phase setup system with 75+ tests ensuring reliability
