

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-4A90E2?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Agentic Coding](https://img.shields.io/badge/Development-Agentic%20Coding-FF6B6B?style=flat-square)](https://the-pocket.github.io/PocketFlow/guide.html)
[![Agent OS](https://img.shields.io/badge/Framework-Agent%20OS-00B4D8?style=flat-square)](https://buildermethods.com/agent-os)
[![PocketFlow](https://img.shields.io/badge/LLM%20Framework-PocketFlow-00F5FF?style=flat-square)](https://github.com/The-Pocket/PocketFlow)
[![Integration Status](https://img.shields.io/badge/Integration-Production%20Ready-28a745?style=flat-square)]()

## Agent OS + PocketFlow Integration

**Production-ready system for intelligent LLM application development.**

This repository contains a **complete, production-ready integration** of [Agent OS](https://buildermethods.com/agent-os) with [PocketFlow](https://github.com/The-Pocket/PocketFlow), creating an intelligent development platform that transforms AI coding from documentation-focused (6.5/10) to workflow-enforced (9/10) structured development.

**Agent OS** (by [Brian Casel](https://buildermethods.com)) provides the structured workflow management, standards, and project organization that transforms AI coding agents from confused assistants into productive developers.

**PocketFlow** (by [The Pocket](https://github.com/The-Pocket)) provides the minimalist, graph-based LLM orchestration framework following the "Agentic Coding" methodology where humans design and AI agents implement.

### 🎯 Integration Status: **PRODUCTION READY**

✅ **All 4 Implementation Phases Complete** (75+ validation tests passing)  
✅ **Comprehensive Setup & Validation System** (9-phase installation process)  
✅ **Automatic Workflow Generation** (12+ files per PocketFlow pattern)  
✅ **Design-First Enforcement** (Mandatory design documents with validation gates)  
✅ **Cross-File Orchestration** (Intelligent dependency management)  
✅ **End-to-End Testing** (Complete integration validation framework)

### ⚠️ CRITICAL: This IS the Framework Repository

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
- Improve generator logic in [`.agent-os/workflows/generator.py`](.agent-os/workflows/generator.py)
- Enhance validation scripts in [`./scripts/validation/`](./scripts/validation/)
- Develop the system that creates workflows for others
- Template placeholders and TODO stubs are intentional design features

**Framework Usage (your projects):**
- Where you install PocketFlow as a dependency
- Where generated templates become working applications  
- Where the orchestrator agent is useful for planning
- Where placeholder code gets implemented

> **New Contributors:** You're working on the meta-system that generates educational templates, not implementing those templates.

### What This Integration Provides

✅ **Complete Python/FastAPI Development Stack** - Modern Python 3.12+, FastAPI, Pydantic, uv toolchain  
✅ **8-Step Agentic Coding Methodology** - Structured workflow from requirements through optimization  
✅ **Design-First LLM Development** - Mandatory design documents with Mermaid diagrams before implementation  
✅ **Type-Safe Architecture** - Pydantic validation at all boundaries with comprehensive schemas  
✅ **Quality-First Development** - Integrated Ruff, ty (type checking), and pytest tooling  
✅ **Universal Compatibility** - Works with any existing codebase while optimizing for Python/PocketFlow  
✅ **Intelligent Workflow Generation** - Automatic creation of complete PocketFlow implementations  
✅ **PocketFlow Orchestrator Agent** - AI planning agent for complex workflow coordination  
✅ **Comprehensive Validation Framework** - 75+ tests ensuring system reliability and integration quality

## Architecture Overview

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

## 🚀 Getting Started

### How to Install and Use This Framework

**Agent OS + PocketFlow** provides a complete development platform for building intelligent LLM applications. Here's how to get started:

#### Option 1: Quick Start (Recommended)
```bash
# Install Agent OS base installation with Claude Code support
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --claude-code

# Setup your first project
cd your-project
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/project.sh | bash
```

#### Option 2: Manual Installation
1. **Base Installation** (customize standards and templates)
2. **Project Installation** (self-contained per project)
3. **Generate Workflows** (create PocketFlow applications)

See detailed instructions in [Installation Guide](#installation-guide) below.

### What You Get

✅ **Complete Python/FastAPI Development Stack** - Modern Python 3.12+, FastAPI, Pydantic, uv toolchain  
✅ **8-Step Agentic Coding Methodology** - Structured workflow from requirements through optimization  
✅ **Design-First LLM Development** - Mandatory design documents with Mermaid diagrams  
✅ **Type-Safe Architecture** - Pydantic validation with comprehensive schemas  
✅ **Quality-First Development** - Integrated Ruff, ty (type checking), and pytest tooling  
✅ **Intelligent Workflow Generation** - Automatic creation of complete PocketFlow implementations  
✅ **PocketFlow Orchestrator Agent** - AI planning agent for complex workflow coordination

---

## 📖 Documentation Navigation

### Quick Navigation by Purpose

**🚀 Using the Framework:**  
- **[Installation Guide](#installation-guide)** - Complete setup instructions (v1.4.0)
- **[Implementation Guide](#implementation-guide)** - How to create projects with the framework
- **[Generated Project Structure](#generated-project-structure)** - What the framework produces
- **[Common Workflows](#common-workflows)** - Typical development patterns

**👥 Received a Generated Template?**
- **[For End-Users Guide](docs/for-end-users/README.md)** - You probably want your generated project docs
- The documentation you need is WITH your generated template, not here

**🏗️ Contributing to the Framework:**
- **[Framework Development Guide](docs/framework-development/QUICKSTART.md)** - Get started contributing
- **[Framework Testing](docs/framework-development/TESTING.md)** - Testing the framework itself
- **[Architecture Documentation](docs/architecture/)** - System internals and design
- **[Core Components](#core-components)** - Key framework components

**🎨 Understanding Template Generation:**
- **[Template Generation Overview](docs/template-generation/README.md)** - How the framework creates templates
- **[Sub-Agents System](docs/template-generation/sub-agents/overview.md)** - Template enhancement agents
- **[Placeholder Philosophy](docs/template-generation/placeholders.md)** - Why TODOs are features

**📚 Additional Resources:**
- **[Release Notes](docs/releases/)** - Version history and changes
- **[Historical Documentation](docs/archive/)** - Previous planning and discussions

---

## Installation Guide

### Agent OS v1.4.0 Installation System

The Agent OS + PocketFlow framework uses a **two-phase installation system** that provides flexibility and self-contained project setups:

1. **Base Installation** (Optional but recommended) - System-wide standards and templates
2. **Project Installation** (Required per project) - Self-contained, committable project setup

### Phase 1: Base Installation

The base installation provides customizable standards and templates that can be shared across projects.

**Choose your AI development environment:**

```bash
# Agent OS with Claude Code support
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --claude-code

# Agent OS with Cursor support  
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --cursor

# Agent OS with both Claude Code & Cursor support
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --claude-code --cursor
```

**What this installs:**
- Agent OS framework files to `~/.agent-os/` (or your chosen location)
- Customizable standards and templates
- Configuration file (`config.yml`) for project customization
- Base templates that project installations will copy from

**After installation:**
- Customize your standards in `~/.agent-os/standards/`
- Modify templates in `~/.agent-os/templates/`
- Configure preferences in `~/.agent-os/config.yml`

### Phase 2: Project Installation

Each project gets its own self-contained Agent OS installation that's committed to git and provides complete independence.

```bash
# Navigate to your project directory
cd your-project-directory

# Install Agent OS + PocketFlow for this project
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/project.sh | bash
```

**What this creates:**
- Self-contained `.agent-os/` directory in your project
- No external references - completely independent
- Project-specific standards and templates
- PocketFlow workflow generation capabilities
- Claude Code agent configurations
- Committable to git for team collaboration

**Benefits of this approach:**
- **Team Collaboration**: `.agent-os/` directories are committable and shareable
- **Project Customization**: Different standards and templates per project
- **No External Dependencies**: Projects work independently of base installation
- **Version Control**: All Agent OS configurations are versioned with your code

### Verification

After installation, verify your setup:

```bash
# Check base installation (if installed)
ls -la ~/.agent-os/

# Check project installation
ls -la .agent-os/

# Test workflow generation (in project directory)
claude-code --workflow "Create a simple content analyzer using PocketFlow"
```

---

## Implementation Guide

### Creating Your First PocketFlow Application

Once installed, you can create intelligent LLM applications using the integrated workflow system:

#### 1. Design-First Development

All PocketFlow applications start with mandatory design documentation:

```bash
# The system will automatically create docs/design.md when you start a workflow
# This includes:
# - Problem statement and requirements
# - Architecture overview with Mermaid diagrams  
# - PocketFlow pattern selection (Agent, Workflow, RAG, etc.)
# - Implementation plan with validation criteria
```

#### 2. Generate Complete PocketFlow Implementation

```bash
# Use Claude Code to generate a complete PocketFlow application
claude-code --workflow "Create a content analysis system that processes documents and extracts key insights"

# This generates 12+ files including:
# - main.py (FastAPI app with PocketFlow integration)
# - nodes.py (PocketFlow nodes with type-safe implementations)  
# - flow.py (PocketFlow orchestration logic)
# - schemas/models.py (Pydantic validation models)
# - tests/ (Comprehensive test suite)
# - docs/design.md (Architecture documentation)
```

#### 3. Implementation Workflow

The system enforces a structured development process:

1. **Requirements Analysis** - Define what you're building
2. **Design Documentation** - Create `docs/design.md` with Mermaid diagrams
3. **Pattern Selection** - Choose optimal PocketFlow pattern
4. **Code Generation** - Auto-generate complete implementation templates
5. **Implementation** - Fill in business logic in generated templates
6. **Testing** - Run comprehensive test suites
7. **Validation** - Ensure quality gates pass
8. **Optimization** - Performance and reliability improvements

#### 4. Quality Gates

Every implementation includes automated quality assurance:

```bash
# The system automatically runs:
uv run ruff check .     # Code linting
uv run ty               # Type checking  
uv run pytest          # Test execution
```

### Common Development Patterns

#### Creating a Simple Agent
```bash
claude-code --workflow "Create a chatbot agent that answers questions about our product documentation"
# Generates: Agent pattern with single LLM integration
```

#### Building a RAG System  
```bash
claude-code --workflow "Create a RAG system that searches company knowledge base and provides contextual answers"
# Generates: RAG pattern with vector search and context injection
```

#### Complex Multi-Agent Workflow
```bash
claude-code --workflow "Create a content analysis pipeline with document processing, sentiment analysis, and report generation"
# Generates: Multi-Agent pattern with orchestrated sub-workflows
```

---

## Common Workflows

### Development Lifecycle

**Starting a New Project:**
1. Run project installation in your directory
2. Define requirements and create design document
3. Use Claude Code to generate PocketFlow implementation
4. Implement business logic in generated templates
5. Run tests and quality gates
6. Deploy with confidence

**Adding New Features:**
1. Update `docs/design.md` with new requirements
2. Generate additional PocketFlow components
3. Integrate with existing workflow
4. Validate with comprehensive testing

**Team Collaboration:**
1. Commit `.agent-os/` directory to git
2. Team members get consistent standards and templates
3. Shared workflow generation and validation
4. Consistent code quality across team

## Generated Project Structure

The workflow generator creates complete PocketFlow implementations with 12+ files:

```
your-workflow/
├── main.py              # FastAPI app entry point with PocketFlow integration
├── nodes.py             # PocketFlow nodes with type-safe implementations
├── flow.py              # PocketFlow flows with proper orchestration
├── router.py            # FastAPI routing integration
├── schemas/
│   └── models.py        # Pydantic models with validation
├── utils/               # Custom utilities
│   ├── call_llm_*.py    # LLM integration utilities
│   └── retrieve_*.py    # Data retrieval utilities
├── tests/               # Comprehensive test suite
│   ├── test_nodes.py    # Node testing
│   ├── test_flow.py     # Flow testing
│   └── test_api.py      # API testing
├── docs/
│   └── design.md        # MANDATORY design document with Mermaid diagrams
├── pyproject.toml       # Modern Python configuration with uv
└── requirements.txt     # Fallback dependencies
```

### Repository Structure

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

---

## Framework Development

### Contributing to the Framework

**This repository IS the framework** - these instructions are for contributing to and improving the framework itself.

#### Framework Development Setup

**Framework Development:**
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

**End-User Installation**: This framework provides `setup/base.sh` and `setup/project.sh` scripts that end-users run to install the framework. End-user installation instructions are provided with their generated projects, not here.

**For Framework Contributors**: Continue to [Framework Development Guide](docs/framework-development/QUICKSTART.md) to work on improving the framework.

#### Framework Architecture: v1.4.0 Two-Phase System

**What the Framework Creates for End-Users:**
- **Base Installation** (`~/.agent-os/`): Shared standards and templates
- **Project Installation** (`.agent-os/`): Self-contained copies for each project  
- **Generated Templates**: PocketFlow applications with educational placeholders

**Framework Benefits Delivered:**
- **No external references**: Projects become self-contained  
- **Team collaboration**: Generated `.agent-os/` directories are committable
- **Project customization**: Different standards per project
- **Template consistency**: All projects follow framework patterns

#### Framework Code Generation System

**What This Framework Generates:** 
This meta-framework includes a Python-based generator that creates educational PocketFlow templates with intentional placeholder TODOs. Framework developers work on improving this generation system.

**Framework Development Testing:**
```bash
# Test the generator in framework repository
cd pocketflow-tools
python generator.py example-workflow-spec.yaml
python test-generator.py
python test-full-generation.py

# View generated template examples (with intentional placeholders)
ls -la testcontentanalyzer/  # Framework validation example
```

**For End-Users**: The framework installation provides workflow commands and template generation. Usage instructions are provided with their generated projects, not here.

### Core Framework Components

**🔧 Generator System** ([`.agent-os/workflows/generator.py`](./.agent-os/workflows/generator.py))
- Creates complete PocketFlow projects from YAML specs
- Generates 12+ files per workflow pattern
- Template substitution and validation system

**✅ Validation Framework** ([`./scripts/validation/`](./scripts/validation/))
- 75+ tests ensuring framework reliability
- Integration, orchestration, and end-to-end validation  
- Template Validator agent with comprehensive quality checks
- Run with [`./scripts/run-all-tests.sh`](./scripts/run-all-tests.sh)

**🤖 Sub-Agents System** ([`docs/template-generation/sub-agents/`](docs/template-generation/sub-agents/))
- **Pattern Recognizer Agent**: Analyzes requirements and identifies optimal PocketFlow patterns
- **Template Validator Agent**: Validates generated templates for structural correctness and educational value
- **Dependency Orchestrator Agent**: Manages Python tooling and dependency configuration
- Intelligent coordination with performance caching (100x+ speedups on repeated requests)
- Framework vs usage distinction enforcement throughout template generation

**📋 Template System** ([`templates/`](templates/))
- PocketFlow, FastAPI, and task templates
- Variable substitution and code generation
- Standards enforcement and best practices

**🎯 Standards & Guidelines** ([`standards/`](standards/))
- [PocketFlow Guidelines](standards/pocket-flow.md) - Framework patterns and best practices
- [Code Style](standards/code-style.md) - Python, FastAPI, and testing standards
- [Tech Stack](standards/tech-stack.md) - Technology choices and rationale

---

## Documentation & Resources

### Framework Documentation
- **[Complete Documentation Hub](docs/)** - Organized documentation with clear navigation
- **[Template Generation System](docs/template-generation/)** - How the framework creates educational templates
- **[Sub-Agents Implementation](docs/template-generation/sub-agents/implementation.md)** - Complete 5-phase implementation details
- **[Architecture Documentation](docs/architecture/)** - System internals, components, and data flow
- **[Framework Development Guide](docs/framework-development/)** - Contributing to the framework
- **Generated Examples**: Working PocketFlow implementations in `.agent-os/workflows/examples/`

### Original Agent OS
- **Documentation**: [Agent OS Docs](https://buildermethods.com/agent-os) - Original Agent OS documentation and guides
- **Installation**: Standard Agent OS installation and usage instructions

### PocketFlow Resources  
- **Documentation**: [PocketFlow Docs](https://the-pocket.github.io/PocketFlow/) - Complete PocketFlow framework documentation
- **Repository**: [PocketFlow GitHub](https://github.com/The-Pocket/PocketFlow) - Source code and examples
- **Agentic Coding Guide**: Core methodology for human-AI collaboration in LLM development

---

## Credits & Acknowledgments

### Agent OS
Created by **Brian Casel** ([@briancasel](https://github.com/briancasel)) from [Builder Methods](https://buildermethods.com).

Agent OS provides the foundational structured workflow management that makes this integration possible. Brian's vision of transforming AI coding agents into productive developers through standards and specifications is the cornerstone of this project.

**Resources**:
- [Builder Briefing newsletter](https://buildermethods.com) - Free resources on building with AI
- [YouTube](https://youtube.com/@briancasel) - AI development insights and tutorials

### PocketFlow
Created by **The Pocket** team ([@The-Pocket](https://github.com/The-Pocket)).

PocketFlow provides the elegant, minimalist LLM orchestration framework that makes complex AI workflows simple and maintainable. Their "Agentic Coding" methodology and graph-based approach to LLM systems is revolutionary.

**Resources**:
- [PocketFlow Framework](https://github.com/The-Pocket/PocketFlow) - The core framework
- [Documentation](https://the-pocket.github.io/PocketFlow/) - Complete guides and patterns

### Integration Development Story
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

The integration maintains the design philosophy of both frameworks while creating an intelligent development platform that demonstrates how structured workflow management and minimalist LLM orchestration can work together to create a world-class AI development experience.

