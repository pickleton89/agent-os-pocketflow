# Agent OS + PocketFlow Framework

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-4A90E2?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Agentic Coding](https://img.shields.io/badge/Development-Agentic%20Coding-FF6B6B?style=flat-square)](https://the-pocket.github.io/PocketFlow/guide.html)
[![Agent OS](https://img.shields.io/badge/Framework-Agent%20OS-00B4D8?style=flat-square)](https://buildermethods.com/agent-os)
[![PocketFlow](https://img.shields.io/badge/LLM%20Framework-PocketFlow-00F5FF?style=flat-square)](https://github.com/The-Pocket/PocketFlow)
[![Integration Status](https://img.shields.io/badge/Integration-Production%20Ready-28a745?style=flat-square)]()

**Enhanced Agent OS framework with integrated PocketFlow template generation.**

This is Agent OS v1.4.0 enhanced with PocketFlow capabilities. When you use Agent OS commands to develop applications, the framework automatically generates complete PocketFlow templates when needed.

## What This Framework Provides

### ✅ Full Agent OS v1.4.0 Workflow
- `/plan-product` - Define product vision and roadmap
- `/analyze-product` - Add Agent OS to existing projects  
- `/create-spec` - Detail feature requirements
- `/execute-tasks` - Create and implement features systematically

### ✅ Automatic PocketFlow Generation
When your tasks involve creating LLM applications, the framework automatically:
- Generates complete PocketFlow applications (12+ files)
- Creates proper FastAPI + Pydantic architecture
- Includes comprehensive test suites
- Provides educational TODO placeholders for business logic
- Supports all PocketFlow patterns (Agent, Workflow, RAG, Multi-Agent)

---

## 🚀 Installation

**Simple one-command setup with automatic context detection:**

### Quick Start (Recommended)

```bash
# Auto-detect context and install appropriately
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash
```

The setup script intelligently detects your context and guides you through the appropriate installation:
- **Base Installation**: Installs framework to `~/.agent-os/` 
- **Project Setup**: Installs into your current project directory

### Manual Installation (Advanced)

```bash
# Step 1: Install base framework to ~/.agent-os/
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash -s base --claude-code

# Step 2: Setup your project (run from project directory)
cd /path/to/your-project
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash -s project
```

### Installation Options

The setup script supports various options:

**Base Installation Options:**
```bash
# Custom installation path
curl -sSL .../setup.sh | bash -s base --claude-code --path ~/my-agent-os

# Force installation (overwrite existing)
curl -sSL .../setup.sh | bash -s base --claude-code --force
```

**Project Installation Options:**
```bash
# Specify project type
curl -sSL .../setup.sh | bash -s project --type python-pocketflow

# Skip base installation check
curl -sSL .../setup.sh | bash -s project --no-base-install --claude-code
```

**That's it! Installation complete.**

---

## 📋 How to Use

Use standard Agent OS workflow. PocketFlow generation happens automatically when needed.

### 1. Start Your Product

```bash
# For new products:
/plan-product

# For existing codebases:
/analyze-product
```

### 2. Develop Features

```bash
# Create detailed specification:
/create-spec

# Create and implement tasks (PocketFlow templates generated automatically when needed):
/execute-tasks
```

### 3. Customize Standards

Edit files in `~/.agent-os/standards/` to define your preferences. The framework will follow these when generating code.

---

## 🎯 What Gets Generated

When your tasks involve PocketFlow applications, the framework automatically creates:

```
your-app/
├── main.py                 # FastAPI application entry point
├── nodes.py                # PocketFlow nodes (with TODO placeholders)
├── flow.py                 # Orchestration logic
├── router.py               # API endpoints
├── schemas/
│   └── models.py          # Pydantic models
├── utils/                  # Utility functions
├── tests/                  # Comprehensive test suite
├── docs/
│   └── design.md          # Architecture documentation
├── pyproject.toml         # Python project configuration
└── requirements.txt       # Dependencies
```

**Note:** TODO placeholders in generated code are intentional - they mark where you implement your specific business logic.

---

## 🔧 PocketFlow Patterns Supported

The framework automatically selects the appropriate pattern based on your specifications:

- **Agent Pattern** - Single LLM agent for conversational interfaces
- **Workflow Pattern** - Multi-step processing pipelines
- **RAG Pattern** - Retrieval-augmented generation systems
- **Multi-Agent Pattern** - Coordinated teams of specialized agents
- **MapReduce Pattern** - Parallel processing workflows
- **Structured Output** - Type-safe data extraction

---

## 🤔 Understanding This Framework

**This Repository:**
- Enhanced Agent OS with PocketFlow integration
- Provides slash commands that work with AI coding agents
- Contains the PocketFlow generator used during `/execute-tasks`
- Creates setup scripts for end-user projects

**Your Projects:**
- Use Agent OS commands to develop features
- Automatically receive PocketFlow templates when needed
- Implement business logic in generated TODO placeholders
- Everything works seamlessly through the Agent OS workflow

---

## 📚 Documentation

- **[Agent OS Docs](https://buildermethods.com/agent-os)** - Original Agent OS documentation
- **[PocketFlow Docs](https://the-pocket.github.io/PocketFlow/)** - PocketFlow framework
- **[Contributing](CONTRIBUTING.md)** - Improve this framework

---

## 🤝 Support

- **Issues:** [GitHub Issues](https://github.com/pickleton89/agent-os-pocketflow/issues)
- **Agent OS Community:** [Builder Methods](https://buildermethods.com)

---

## Credits

**Agent OS** by [Brian Casel](https://buildermethods.com) - Structured workflow management  
**PocketFlow** by [The Pocket](https://github.com/The-Pocket) - LLM orchestration framework  
**Integration** - Seamless combination of both systems for enhanced AI development