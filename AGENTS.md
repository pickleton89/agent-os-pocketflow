# Agent OS + PocketFlow Framework Repository

## ⚠️ Critical Concept: Framework vs End-User Projects

**This repository IS the Agent OS + PocketFlow framework itself - NOT a project using it.**

| Framework Repository (this repo) | End-User Projects |
|----------------------------------|-------------------|
| Generates PocketFlow templates for other projects | Where PocketFlow gets installed as a dependency |
| Contains setup scripts, validation tools, code generators | Where generated templates become working applications |
| Develops the meta-system that creates workflows | Where the orchestrator agent runs and is useful |
| Template placeholders and TODO stubs are intentional features | Where placeholder code gets implemented |
| Missing imports/dependencies in generated code are BY DESIGN | Where import errors would be actual bugs to fix |
| Tests the framework itself, not applications built with it | Where the design-first workflow is actually used |

**Key Principle**: Template generators create meaningful placeholder code showing intent and guiding implementation, not working implementations. "Missing" dependencies and undefined functions in generated templates are features, not bugs.

### Platform & Language Scope
- Supported OS: macOS only (current focus)
- Language: Python 3.12 (managed with `uv`)
- Some agent workflows intentionally use macOS tooling (e.g., `afplay` in post‑execution tasks). Broader OS support may be added later.

### v1.4.0 Architecture (Base + Project Installations)
- **Base Installation** (`~/.agent-os/`): Customizable standards, reusable across projects
- **Project Installation** (`.agent-os/` in each project): Self-contained, committable to git
- **Framework Repository** (this repo): Creates both base and project installation files

### Key Components
- `.claude/agents/pocketflow-orchestrator.md` defines an agent for END-USER projects (not this repo)
- Generator creates templates with intentional placeholder code
- TODO stubs in generated files are starting points, not bugs to fix
- `setup.sh` routes to `setup/base.sh` and `setup/project.sh` based on context

### Instruction Resolution Order (End‑User Projects)
When instruction files are referenced, resolution occurs in this order:
1) `.agent-os/instructions/core`
2) `.agent-os/instructions`
3) `~/.agent-os/instructions/core`
4) `~/.agent-os/instructions`

Project‑local instructions take precedence over the base installation.

## Development Guidelines

### ❌ DO NOT
- Invoke the pocketflow-orchestrator agent (it's for end-user projects)
- Try to "fix" TODO placeholders in generated templates (they're intentional)
- Install PocketFlow as a dependency (it gets installed in target projects)
- Expect pytest to find application tests (this is a meta-framework, not an application)
- Treat import errors in generated test files as bugs (they're templates for other projects)

### ✅ DO
- Improve the Agent OS system, generator, and validation tools
- Focus on template quality, setup scripts, and documentation
- Test the framework itself, not applications built with it
- Understand that `generator.py` creates STARTER templates with TODO stubs for customization
- Remember that missing imports/dependencies in generated code are intentional design

### Testing Framework Code

```bash
# Test the framework code itself
./scripts/run-all-tests.sh

# Test the generator system
cd framework-tools
python3 test-generator.py
python3 test_full_generation_with_dependencies.py

# Test specific validation suites
./scripts/validation/validate-integration.sh
./scripts/validation/validate-orchestration.sh
```

**Repo-Type Aware Validation**: The test harness auto-detects framework vs project repos and skips project-only checks in framework mode. See README.md:466 or `scripts/lib/repo-detect.sh` for details.

## 🚨 Critical Distinction: Framework vs Usage

**BEFORE suggesting fixes, ask: "Is this framework code or generated template code?"**

### Framework Code (Fix bugs immediately)
- **Location**: Files in `framework-tools/`, `pocketflow_tools/`, `scripts/`, `setup/`
- **Purpose**: Generator logic, validation scripts, setup tools, CLI utilities
- **Quality Standard**: Should have zero F821 errors (except educational demos)
- **Import Errors**: Are actual bugs - must be fixed
- **TODO Comments**: Indicate incomplete framework features - should be implemented

**Examples**:
- `pocketflow_tools/generators/` - Template generation engines
- `framework-tools/check-pocketflow-install.py` - Validation utility
- `setup/base.sh` - Installation script

### Generated Template Code (TODOs are features)
- **Location**: Files in `templates/`, generated output examples, documentation examples
- **Purpose**: Starter code for end-user projects with placeholder functions
- **Quality Standard**: Placeholder functions, educational comments, TODO stubs expected
- **Import Errors**: Are BY DESIGN - templates show structure, not working code
- **TODO Comments**: Guide developers on what to customize - are intentional features

**Examples**:
- `templates/pocketflow-templates.md` - Template definitions (framework file)
- `nodes.py`, `flow.py` in end-user projects - Generated files with `# TODO` placeholders
- Generated test files in end-user projects - Show testing structure with missing fixtures

### Educational Demo Code (Errors are intentional)
- **Location**: Files like `antipattern_demo.py`, `templates/examples/bad/`
- **Purpose**: Demonstrates what NOT to do for detector validation
- **Quality Standard**: Linting errors are EXPECTED and DOCUMENTED
- **Import Errors**: Part of the demonstration - validate detector catches them
- **TODO Comments**: May indicate areas for expanding demo coverage

**Examples**:
- `framework-tools/antipattern_demo.py` - Intentionally violates best practices

### Decision Tree for Contributors

```
Found an issue? Ask these questions:

1. Where is the file located?
   ├─ framework-tools/, pocketflow_tools/, scripts/ → Framework code
   ├─ templates/, docs/examples/ → Template code
   └─ *_demo.py, examples/bad/ → Educational demo

2. What's the issue?
   ├─ Import error in framework code → BUG - fix immediately
   ├─ Import error in template → FEATURE - it's a placeholder
   ├─ TODO in framework code → INCOMPLETE - should implement
   ├─ TODO in template → FEATURE - guides customization
   └─ Error in demo code → Check if intentional for detector

3. Is this file executed by the framework?
   ├─ Yes → Must work correctly, fix all errors
   └─ No (it's a template) → Errors are design features
```

### Common Scenarios

**Scenario 1**: Found undefined function in generated `nodes.py` file (in end-user project)
- ✅ **Correct**: This is generated template code - placeholder is intentional
- ❌ **Incorrect**: "Let me implement this function in the framework"

**Scenario 2**: Found import error in `pocketflow_tools/generators/code_generators.py`
- ✅ **Correct**: This is framework code - must fix immediately
- ❌ **Incorrect**: "This is just a template, it's fine"

**Scenario 3**: Found TODO in `framework-tools/validate-setup.sh`
- ✅ **Correct**: Framework feature incomplete - should implement
- ❌ **Incorrect**: "TODOs are features here"

**Scenario 4**: Found linting error in `antipattern_demo.py`
- ✅ **Correct**: Check if it's documented as intentional for testing
- ❌ **Incorrect**: "Let me fix all these linting errors"

## Quality Standards for Framework Development

### Verification-First Approach
- Always verify counts with bash commands — don't estimate or guess numbers
- Double-check multi-step operations — ensure each step actually completed
- Use systematic verification — confirm file changes, git status, actual vs claimed actions
- Apply "fresh eyes" review — catch errors before claiming completion
- Verify assumptions with tools — use `ls`, `find`, `grep` to confirm findings

### Common Error Patterns to Avoid
- Counting errors (claimed 6 scripts, actually 7)
- Missing large file collections (.venv with 700+ files)
- Claiming completion without verification (file update ≠ git commit)
- Rushing through analysis without thorough checking
- Assuming operations completed successfully without confirmation

### Mandatory Verification Steps
1. Use bash commands to verify all counts and file operations
2. Check git status before claiming commits are complete
3. Apply systematic quality review to all analysis work
4. Validate findings with actual tool output, not assumptions
5. Take time for accuracy over speed

**Performance Expectation**: High attention to detail and systematic verification of all work.

## Search Strategy Preferences

### Semantic Search First
- Always try `claude_context_search` before falling back to grep
- Use semantic search for conceptual queries
- Use grep only for exact string matches

### Search Commands Priority
1. `claude_context_search` — for finding related functionality
2. Traditional grep — for exact matches only

### Example Queries
- "Use claude_context_search to find statistical analysis code"
- "Search semantically for file parsing utilities"

## Design-First Philosophy (What Framework Generates)

The Agent OS + PocketFlow framework **generates templates and tools** that enforce design-first methodology in end-user projects.

### Core Principle: Humans Design, Agents Code

**Framework philosophy**: Humans make architectural decisions and create designs. Agents implement code based on those designs.

### Generated Design-First Workflow

This framework generates for end-user projects:

1. **Product Planning** (`/plan-product`):
   - Creates `docs/design.md`, `mission.md`, `roadmap.md`
   - Templates for architectural foundation, pattern selection, data flow diagrams
   - Orchestrator instructions: `instructions/core/plan-product.md`

2. **Feature Specification** (`/create-spec [feature-name]`):
   - Extends `docs/design.md` with feature-specific designs
   - Templates for node types, SharedStore schema evolution, integration strategies
   - Orchestrator instructions: `instructions/core/create-spec.md`

3. **Implementation** (`/execute-tasks [spec-name]`):
   - Validates design documentation exists before allowing code changes
   - Generated validation scripts block execution without complete design
   - Orchestrator instructions: `instructions/core/execute-tasks.md`

### Framework Template Philosophy

**Generated templates include intentional TODO placeholders**:
- TODOs guide customization (features, not bugs)
- Templates provide structure, humans provide business logic
- Design documents contain blueprints, implementation follows the plan
- Educational comments explain framework methodology

### Quality Assurance Through Generated Validation

Framework-generated templates and validation ensure in end-user projects:
- ✅ Architectural consistency across features
- ✅ PocketFlow pattern alignment
- ✅ Integration planning before implementation
- ✅ Error handling and performance strategy sections
- ✅ Testing strategy included in all specs

Framework-generated validation prevents:
- ❌ Skipping design phase (blocks `/execute-tasks` without complete design)
- ❌ Incomplete specifications (validates all design sections completed)
- ❌ Design-implementation drift (tests verify implementation matches design)
- ❌ Pattern mixing (guides toward consistent architectural patterns)

**Framework Development Note**: Validation capabilities are defined in `instructions/core/*.md` files and generated into end-user projects during setup.

## Additional Repository Reference

### Project Structure & Module Organization
- `framework-tools/`: Core PocketFlow tooling and tests (e.g., `generator.py`, `pattern_analyzer.py`, `test_*.py`)
- `scripts/`: Validation and orchestration scripts (e.g., `scripts/run-all-tests.sh`, `validation/*.sh`)
- `standards/`: Authoritative coding, testing, and FastAPI/PocketFlow style guides
- `templates/` and `docs/`: Workflow templates and documentation
- `.agent-os/` (optional): Local workspace created by setup or generators

### Build, Test, and Development Commands
- Create venv and install deps: `uv venv && source .venv/bin/activate && uv pip install -e .`
- Run full validations: `bash scripts/run-all-tests.sh` (add `-q` for quick, `-v` for verbose)
- Run framework tests: `uv run pytest -q pocketflow_tools/`
- Generate a workflow: `uv run python -m pocketflow_tools.cli --spec framework-tools/examples/agent-workflow-spec.yaml --output /path/to/end-user-project`
- Bootstrap Agent OS locally: `bash ./setup.sh --help` (see modes `base`, `project`, `auto`)

### Coding Style & Naming Conventions
- Language: Python 3.12 (`.python-version`), indentation 4 spaces
- Naming: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`
- Lint/format: Prefer `ruff` (target py312, line length ~88); type hints encouraged; keep functions small and composable
- Follow `standards/code-style.md` plus `standards/code-style/{python-style.md,fastapi-style.md,pocketflow-style.md}`

### Testing Guidelines
- Framework: `pytest`; tests live alongside tools in `framework-tools/` and under `framework-tools/testcontentanalyzer/tests/`
- Naming: `test_*.py`, test functions `test_*`; use markers only when needed
- Run smoke or comprehensive via repo scripts (see `scripts/validation/*`); quick check: `uv run pytest -q framework-tools`
- Add focused unit tests for utilities and flows; include minimal fixtures and clear assertions
- Repo-type aware validation: the harness auto-detects framework mode and skips project-only checks

### Repository Do/Don'ts
- Don't install PocketFlow as a dependency in this repo; it belongs in end-user projects
- Don't "fix" TODO placeholders in generated templates; they are intentional teaching stubs
- Don't invoke the PocketFlow orchestrator agent from this repo; it runs in usage repos
- Don't treat import errors in generated example templates as bugs; they resolve in target projects

### Commit & Pull Request Guidelines
- Conventional prefixes observed: `feat:`, `fix:`, `docs:`, `chore:`, `tests:` (see `git log`)
- Commits: present tense, scoped subject; small, logical changes
- PRs: include goal summary, key changes, validation steps (e.g., output from `scripts/run-all-tests.sh`), and link issues; add screenshots/logs for UX flows when relevant

### Security & Configuration Tips
- Config: review `config.yml` before running scripts; avoid committing secrets
- Isolation: use `uv` and a local `.venv`; prefer `uv run ...` for commands
- Generated outputs: workflows write to `.agent-os/workflows/` by default — verify before committing

### Critical Reminders for Agent Behavior
1. Be completely honest — if you don’t know or made an error, say so immediately
2. Think carefully before acting — review your approach before implementing
3. Write high-quality code — check for bugs, inconsistencies, and edge cases
4. Verify your work — actually test/validate claims rather than assuming
5. No false progress — don’t claim completion of tasks you haven’t done
