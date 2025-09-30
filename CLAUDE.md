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

### v1.4.0 Architecture (Base + Project Installations)
- **Base Installation** (`~/.agent-os/`): Customizable standards, reusable across projects
- **Project Installation** (`.agent-os/` in each project): Self-contained, committable to git
- **Framework Repository** (this repo): Creates both base and project installation files

### Key Components
- `.claude/agents/pocketflow-orchestrator.md` defines an agent for END-USER projects (not this repo)
- Generator creates templates with intentional placeholder code
- TODO stubs in generated files are starting points, not bugs to fix
- `setup.sh` routes to `setup/base.sh` and `setup/project.sh` based on context

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

## Quality Standards for Framework Development

### Verification-First Approach
- **Always verify counts with bash commands** - don't estimate or guess numbers
- **Double-check multi-step operations** - ensure each step actually completed
- **Use systematic verification** - confirm file changes, git status, actual vs claimed actions
- **Apply "fresh eyes" review** - catch errors before claiming completion
- **Verify assumptions with tools** - use ls, find, grep to confirm findings

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
- Always try claude_context_search before falling back to grep
- Use semantic search for conceptual queries
- Use grep only for exact string matches

### Search Commands Priority
1. `claude_context_search` - for finding related functionality
2. Traditional grep - for exact matches only

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
