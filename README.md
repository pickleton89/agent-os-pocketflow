<img width="1280" height="640" alt="agent-os-og" src="https://github.com/user-attachments/assets/e897628e-7063-4bab-a69a-7bb6d7ac8403" />

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-4A90E2?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Agentic Coding](https://img.shields.io/badge/Development-Agentic%20Coding-FF6B6B?style=flat-square)](https://the-pocket.github.io/PocketFlow/guide.html)
[![Agent OS](https://img.shields.io/badge/Framework-Agent%20OS-00B4D8?style=flat-square)](https://buildermethods.com/agent-os)
[![PocketFlow](https://img.shields.io/badge/LLM%20Framework-PocketFlow-00F5FF?style=flat-square)](https://github.com/The-Pocket/PocketFlow)

## Agent OS + PocketFlow Integration

**Your system for structured LLM application development.**

This repository contains a comprehensive integration of [Agent OS](https://buildermethods.com/agent-os) with [PocketFlow](https://github.com/The-Pocket/PocketFlow), creating a powerful framework for building modern LLM applications with structured, standards-driven workflows.

**Agent OS** (by [Brian Casel](https://buildermethods.com)) provides the structured workflow management, standards, and project organization that transforms AI coding agents from confused assistants into productive developers.

**PocketFlow** (by [The Pocket](https://github.com/The-Pocket)) provides the minimalist, graph-based LLM orchestration framework following the "Agentic Coding" methodology where humans design and AI agents implement.

### What This Integration Provides

✅ **Complete Python/FastAPI Development Stack** - Modern Python 3.12+, FastAPI, Pydantic, uv toolchain

✅ **8-Step Agentic Coding Methodology** - Structured workflow from requirements through optimization

✅ **Design-First LLM Development** - Mandatory design documents with Mermaid diagrams before implementation

✅ **Type-Safe Architecture** - Pydantic validation at all boundaries with comprehensive schemas

✅ **Quality-First Development** - Integrated Ruff, ty (type checking), and pytest tooling

✅ **Universal Compatibility** - Works with any existing codebase while optimizing for Python/PocketFlow

## Architecture Overview

This integration combines the best of both frameworks:

```
FastAPI (main.py) → Pydantic Models (schemas/) → PocketFlow Flows (flow.py) → PocketFlow Nodes (nodes.py) → Utility Functions (utils/)
```

### Key Components

- **Standards & Instructions**: Global development standards and workflow instructions optimized for Python/PocketFlow
- **Templates**: Comprehensive templates for design documents, FastAPI endpoints, and PocketFlow components  
- **Claude Code Agents**: Specialized agents for file creation, context fetching, git workflows, and testing
- **8-Step Methodology**: Requirements → Flow Design → Utilities → Data Design → Node Design → Implementation → Optimization → Reliability

## Quick Start

### Installation

```bash
# Clone this integrated repository
git clone https://github.com/your-repo/agent-os.git
cd agent-os

# Run the setup script to install globally
./setup.sh

# Setup Claude Code integration (optional)
./setup-claude-code.sh
```

### Usage

For **new Python/PocketFlow projects**:
```bash
# Plan a new product
/plan-product

# Create feature specifications
/create-spec

# Execute implementation tasks
/execute-tasks
```

For **existing codebases** (any language):
```bash
# Analyze and add Agent OS to existing code
/analyze-product
```

## Project Structure

When you create a new PocketFlow project, you'll get:

```
project/
├── main.py           # FastAPI app entry point
├── nodes.py          # PocketFlow nodes  
├── flow.py           # PocketFlow flows
├── schemas/          # Pydantic models
│   ├── requests.py   # API request models
│   └── responses.py  # API response models
├── utils/            # Custom utilities (call_llm.py, etc.)
├── docs/
│   └── design.md     # MANDATORY design document
└── requirements.txt  # or pyproject.toml for uv
```

## Documentation & Resources

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

### Integration Development
This integration was created to demonstrate how structured workflow management (Agent OS) and minimalist LLM orchestration (PocketFlow) can work together to create a world-class development experience for building AI applications.

**Built with Agentic Coding**: This entire integration was developed using the Agentic Coding methodology with [Claude Code](https://claude.ai/code) as the AI development partner. The project exemplifies the "humans design, agents code" philosophy:

- **Human-led Design**: Strategic decisions, architecture planning, and integration approach
- **AI-assisted Implementation**: Standards files, templates, documentation, and workflow instructions
- **Collaborative Refinement**: Iterative improvement and validation of all components

The integration maintains the design philosophy of both frameworks while creating something greater than the sum of its parts. This project serves as a real-world example of how Agentic Coding can be used to build complex, production-ready developer tools and frameworks.
