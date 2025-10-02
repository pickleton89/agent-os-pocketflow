# Agent OS + PocketFlow Framework

THIS IS NOT A FINISHED PRODUCT AND STILL NEEDS WORK AND TESTING

**Enhanced Agent OS framework with integrated PocketFlow template generation.**

This is Agent OS v1.4.0 enhanced with PocketFlow capabilities. When you use Agent OS commands to develop applications, the framework automatically generates complete PocketFlow templates when needed.

## 🎯 Understanding This Repository

### This Repository (Framework Development)
- **Purpose**: Generate PocketFlow templates for OTHER projects
- **You work here if**: Building the generator, validators, setup scripts
- **What you test**: Template generation logic, validation scripts, framework tools
- **Dependencies**: Minimal (PyYAML, dev tools) - we DON'T install PocketFlow here

### End-User Projects (Framework Usage)
- **Purpose**: Build LLM applications using generated templates
- **You work here if**: Creating RAG systems, AI agents, tools with PocketFlow
- **What you test**: Your application logic, API endpoints, LLM integrations
- **Dependencies**: PocketFlow, FastAPI, pattern-specific libraries

### Common Confusion Points

❌ **"Why don't imports work in generated templates?"**
→ This repo generates templates; PocketFlow installs in end-user projects

❌ **"Why are there TODOs everywhere?"**
→ Educational placeholders for developers to customize

❌ **"Why aren't agents working?"**
→ Agent definitions are OUTPUTS for end-user projects

✅ **"How do I test the generator?"**
→ `./scripts/run-all-tests.sh`

**Key Principle**: Missing implementations in generated templates are features, not bugs. This framework creates starting points for developers, not finished applications.

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

Agent OS + PocketFlow is distributed as a uv-installable Python package. Use the `agent-os` CLI to create the base installation (`~/.agent-os/`) and then apply the project installer script inside each repository that needs PocketFlow support.

### Prerequisites
- `uv` 0.8.0 or newer (`uv --version`)
- Python 3.12+ (uv manages the runtime automatically when missing)
- Git available on your PATH (for git-based installs)

### 🎯 Quick Start (Recommended)

Install the CLI as a uv tool and bootstrap the shared base installation:
```bash
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow
agent-os init --yes
```

`agent-os init` copies the packaged resources into `~/.agent-os`. Pass `--yes` to skip the confirmation prompt.

> Working from a local clone? Replace the `--from` URL with `"$PWD"`.

> Upgrading from the legacy bash installers? Follow `docs/MIGRATION_GUIDE.md`. Contributors coordinating the uv rollout can track progress in `docs/uv-implementation-plan.md`.

### ⚡ Run Without Installing

For CI jobs or one-off machines you can execute the installer without registering the tool:
```bash
uvx --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os init --yes
```

### 🧩 Project-Local Base (uv Workspace)

When you want the base installation committed alongside a project:
```bash
uv add agent-os-pocketflow
uv run agent-os init --install-path .agent-os --yes
```

This creates the same `.agent-os/` layout inside the repository.

### 📋 Installation Architecture

```
~/.agent-os/                    # Base Installation (Framework)
├── instructions/               # Core Agent OS instructions
├── standards/                  # Your customizable coding standards
├── framework-tools/            # PocketFlow generators & validators
├── templates/                  # PocketFlow application templates
└── setup/
    ├── project.sh              # Project installation script
    └── update-project.sh       # Project update script

your-project/                   # Project Installation (Self-contained)
├── .agent-os/                  # Project-specific Agent OS files
│   ├── instructions/           # Copied from base installation
│   ├── standards/              # Copied from base installation
│   ├── framework-tools/        # PocketFlow tools for this project
│   └── config.yml              # Project configuration
├── .claude/                    # Claude Code integration (if enabled)
│   ├── commands/               # Agent OS slash commands
│   └── agents/                 # Specialized AI agents
└── [your project files]
```

### 🔧 Base Installation Options

Use `agent-os init` flags to customise the base installation:
```bash
# Specify a custom install location
agent-os init --install-path ~/company/.agent-os --yes

# Disable PocketFlow templates
agent-os init --no-pocketflow --yes

# Skip Claude Code integration assets
agent-os init --no-claude-code --yes

# Overwrite an existing installation
agent-os init --force --yes

# Show verbose logging with full path details
agent-os init --verbose --show-paths --yes
```

### 📖 CLI Flags Reference

#### `agent-os init`
| Flag | Description | Example |
|------|-------------|---------|
| `--install-path PATH` | Custom base installation location | `agent-os init --install-path ~/my-agent-os --yes` |
| `--no-pocketflow` | Skip PocketFlow templates and toolkit | `agent-os init --no-pocketflow --yes` |
| `--no-claude-code` | Skip Claude Code integration assets | `agent-os init --no-claude-code --yes` |
| `--force` | Overwrite an existing installation | `agent-os init --force --yes` |
| `--toolkit-source PATH` | Use a custom toolkit source directory | `agent-os init --toolkit-source ~/agent-os/framework-tools --yes` |
| `--verbose` | Enable verbose logging output | `agent-os init --verbose --yes` |
| `--show-paths` | Print every created/overwritten path | `agent-os init --show-paths --yes` |
| `--prompt` | Require confirmation before running (default) | `agent-os init --prompt` |
| `--yes` | Skip confirmation prompts | `agent-os init --yes` |

#### Project Installation Flags (`setup/project.sh`)
| Flag | Description | Example |
|------|-------------|---------|
| `--claude-code` | Enable Claude Code integration | `--claude-code` |
| `--no-pocketflow` | Install standard Agent OS only | `--no-pocketflow` |
| `--no-base` | Standalone mode (no base required) | `--no-base --claude-code` |
| `--base-path PATH` | Custom base installation path | `--base-path ~/my-agent-os` |
| `--project-type TYPE` | Set project type | `--project-type fastapi-pocketflow` |
| `--force` | Overwrite existing `.agent-os` | `--force` |

#### Project Types Available
- `pocketflow-enhanced` (default) - Full Agent OS + PocketFlow
- `standard-agent-os` - Standard Agent OS only
- `python-pocketflow` - Python-optimized PocketFlow setup
- `fastapi-pocketflow` - FastAPI + PocketFlow setup

### 🔄 Updating Your Installation

#### Update the CLI Tool
```bash
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow
```

Re-running the install command refreshes the cached tool. Use `uv tool uninstall agent-os-pocketflow` to remove it.

#### Refresh Base Installation Resources
```bash
agent-os init --force --yes
```

Passing `--force` ensures the base directory is replaced with the latest packaged assets.

#### Update Project Installation
```bash
# Update all project components from base
~/.agent-os/setup/update-project.sh --update-all

# Update specific components
~/.agent-os/setup/update-project.sh --update-instructions
~/.agent-os/setup/update-project.sh --update-standards
~/.agent-os/setup/update-project.sh --update-framework-tools

# Update without backing up existing files
~/.agent-os/setup/update-project.sh --update-all --no-backup

# Force update even if no changes detected
~/.agent-os/setup/update-project.sh --update-all --force
```

### 🛠️ Common Installation Scenarios

#### First-time Setup
```bash
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow
agent-os init --yes
cd /path/to/project
~/.agent-os/setup/project.sh --claude-code
```

#### Adding to Existing Project
```bash
agent-os init --yes
cd existing-project
~/.agent-os/setup/project.sh --claude-code
```

#### Multiple Projects
```bash
# Base installation (once)
agent-os init --yes

# Each project
cd project-1 && ~/.agent-os/setup/project.sh --claude-code
cd project-2 && ~/.agent-os/setup/project.sh --claude-code
```

#### Standalone Project (No Shared Base)
```bash
cd my-project
uvx --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os init --install-path .agent-os --yes
./.agent-os/setup/project.sh --no-base --claude-code
```

**Installation complete!** Your system now has Agent OS + PocketFlow ready to use.

---

## 📋 How to Use

### Pattern Analyzer — Phase 4 Summary

The Pattern Analyzer automatically detects which PocketFlow pattern best fits your requirements and can identify meaningful pattern combinations.

- Configurable thresholds: `PatternAnalyzer` exposes combination detection thresholds at the class level via `DEFAULT_COMBINATION_RULES` and at the instance level via `combination_rules`. Tune per combo using normalized `min_norm` values (relative to the max score in a run).
- Rationale prefix: When a valid combination is detected (e.g., RAG + AGENT), the analyzer prepends a brief line like: "Detected composite scenario: RAG + AGENT. Top patterns: TOOL (1.00), RAG (0.85)."
- Confidence bump: For robust combos where all member patterns have normalized scores ≥ 0.8, the analyzer adds a small confidence bump (+0.05, capped at 1.0).
- HYBRID remains metadata-first: The analyzer only sets `template_customizations.hybrid_candidate` and `combination_info`; primary pattern stays an enum. The generator can optionally promote hybrid behavior when configured.

To customize thresholds:
```python
from pocketflow_tools.pattern_analyzer import PatternAnalyzer, PatternType

custom = {
    "intelligent_rag": {"patterns": [PatternType.RAG, PatternType.AGENT], "min_norm": 0.6},
}
analyzer = PatternAnalyzer(combination_rules=custom)
```


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

### Optional: HYBRID Composition (Opt-in)

- Enable hybrid node/graph composition when the analyzer detects meaningful combinations (e.g., RAG + AGENT).
- Default is off to avoid churn. Turn it on per-generator instance:

```python
# If running inside a project repo, adjust sys.path to the tools directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.agent-os/framework-tools')))  # project tools directory
import generator as gen

# Opt-in to compose nodes and graph when combinations are detected
g = gen.PocketFlowGenerator(enable_hybrid_promotion=True)

# Given requirements text `req`, this will:
# - Keep the strongest primary pattern for classification
# - Compose nodes from both base patterns (e.g., RAG + AGENT)
# - Render a composed Mermaid graph in docs/design.md
files = g.generate_workflow_from_requirements("HybridExample", req)
```

Notes:
- If the analyzer recommends a simple structure (SIMPLE_WORKFLOW, BASIC_API, SIMPLE_ETL), that takes precedence over hybrid composition.
- Hybrid remains metadata-driven; the analyzer does not set HYBRID as primary.

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
- **[Repository Guidelines](AGENTS.md)** - Contributor guide for structure, commands, style, and tests

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Installation Issues

**"No base installation found"**
```bash
# Solution: Install the CLI (if needed) and create the base before running the project script
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow
agent-os init --yes
cd your-project
~/.agent-os/setup/project.sh --claude-code
```

**"Existing .agent-os directory found"**
```bash
# Solution: Use --force to overwrite or backup manually
~/.agent-os/setup/project.sh --force --claude-code
```

**"Permission denied" errors**
```bash
# Solution: Ensure write permissions
chmod +w ~/.agent-os
chmod +w .
```

#### Update Issues

**"Failed to copy instructions from base installation"**
```bash
# Solution: Verify base installation and re-update
ls -la ~/.agent-os/instructions/
~/.agent-os/setup/update-project.sh --update-instructions --force
```

**Custom standards got overwritten**
```bash
# Solution: Restore from backup (created automatically)
ls -la .agent-os-backup-*
cp .agent-os-backup-*/standards/* .agent-os/standards/
```

#### Usage Issues

**Commands not found (/plan-product, etc.)**
```bash
# For Claude Code: Ensure .claude directory exists and restart Claude Code
ls -la .claude/commands/
# Re-install if missing:
~/.agent-os/setup/project.sh --claude-code --force
```

**PocketFlow generation not working**
```bash
# Verify PocketFlow tools are installed
ls -la .agent-os/framework-tools/
# Update if missing:
~/.agent-os/setup/update-project.sh --update-framework-tools
```

### Checking Your Installation

#### Verify Base Installation
```bash
# Check base installation structure
ls -la ~/.agent-os/
cat ~/.agent-os/config.yml

# Expected directories:
# ~/.agent-os/instructions/
# ~/.agent-os/standards/
# ~/.agent-os/framework-tools/
# ~/.agent-os/setup/
```

#### Verify Project Installation
```bash
# Check project installation structure  
ls -la .agent-os/
cat .agent-os/config.yml

# Expected directories:
# .agent-os/instructions/
# .agent-os/standards/
# .agent-os/framework-tools/ (if PocketFlow enabled)
# .claude/commands/ (if Claude Code enabled)
```

#### Verify Installation Health
```bash
# Test base installation
~/.agent-os/setup/project.sh --help

# Test update mechanism
~/.agent-os/setup/update-project.sh --help

# Check PocketFlow tools
python -m pocketflow_tools.cli --help
```

### Getting Clean State

#### Reset Base Installation
```bash
# Backup customizations first
cp -r ~/.agent-os/standards/ ~/agent-os-standards-backup/

# Clean reinstall
agent-os init --force --yes

# Restore customizations
cp -r ~/agent-os-standards-backup/* ~/.agent-os/standards/
```

#### Reset Project Installation
```bash
# Backup project-specific customizations
cp -r .agent-os/ .agent-os-backup-manual/

# Clean reinstall
rm -rf .agent-os .claude
~/.agent-os/setup/project.sh --claude-code

# Restore specific customizations as needed
```

### Migration from Older Versions

#### From v1.3.x or earlier Agent OS
```bash
# Install or refresh the CLI
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow

# Replace the base installation with the packaged resources
agent-os init --force --yes

# Reinstall in each project
cd each-project
~/.agent-os/setup/project.sh --claude-code
```

#### From Single-directory Installation
```bash
# If you have old single .agent-os installation, migrate to v1.4.0 architecture
# Backup old installation
cp -r .agent-os/ .agent-os-old-backup/

# Install new base + project setup
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow
agent-os init --yes
~/.agent-os/setup/project.sh --claude-code
```

---

## ✅ Repo-Type Aware Validation

The validation harness auto-detects whether it is running in the Framework repository (this repo) or in an end‑user Project repository, and adapts checks to avoid false failures.

### Detection

- Override with env var: `REPO_TYPE=framework` or `REPO_TYPE=project`
- Heuristics when not set:
  - Framework if `pocketflow_tools/` package exists or `CLAUDE.md` contains "This IS the Framework"
  - Project if `.agent-os/workflows/` has subdirectories, or `docs/design.md` or `tests/` exists
  - Defaults to framework

Helper script: `scripts/lib/repo-detect.sh`

```
detect_repo_type        # echoes "framework" or "project"
is_framework && ...     # run only in framework
is_project && ...       # run only in project
skip_if_framework "reason"  # print SKIP and return success
skip_if_project  "reason"  # print SKIP and return success
```

### Affected Scripts

- `scripts/run-all-tests.sh` — prints repo type and selects suites accordingly
- `scripts/validation/validate-integration.sh` — in framework mode runs light sanity checks and skips project‑only checks
- `scripts/validation/validate-orchestration.sh` — skipped in framework mode
- `scripts/validation/validate-end-to-end.sh` — skipped in framework mode
- `scripts/validation/validate-design.sh` — skipped in framework mode
- `scripts/validation/validate-pocketflow.sh` — skipped in framework mode

Project‑only checks still run unchanged in project mode.

### Usage Examples

Run full suite (auto‑detect):

```bash
bash scripts/run-all-tests.sh
```

Run quick suite:

```bash
bash scripts/run-all-tests.sh -q
```

Force project mode (e.g., when testing against a sample project):

```bash
REPO_TYPE=project bash scripts/run-all-tests.sh -v
```

### CI Recommendation

Use a single job that runs `scripts/run-all-tests.sh`. It adapts to framework or project contexts automatically. Pin `REPO_TYPE` for deterministic behavior if needed.  
In framework CI, SKIP messages will appear for project‑only checks, keeping signal clean.

## 🤝 Support

- **Issues:** [GitHub Issues](https://github.com/pickleton89/agent-os-pocketflow/issues)
- **Agent OS Community:** [Builder Methods](https://buildermethods.com)
- **Installation Help:** Check troubleshooting section above

---

## Credits

**Agent OS** by [Brian Casel](https://buildermethods.com) - Structured workflow management  
**PocketFlow** by [The Pocket](https://github.com/The-Pocket) - LLM orchestration framework  
**Integration** - Seamless combination of both systems for enhanced AI development
