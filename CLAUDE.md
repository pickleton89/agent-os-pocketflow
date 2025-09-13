# Agent OS + PocketFlow Framework Repository

## ⚠️ IMPORTANT: This IS the Framework
This repository contains the Agent OS + PocketFlow system itself - NOT a project using it.

### What This Repository Does
- Provides the Agent OS + PocketFlow framework following v1.4.0 architecture:
  - **Base Installation**: Framework installs to `~/.agent-os/` (or chosen location) with customizable standards
  - **Project Installation**: Self-contained `.agent-os/` copies in each end-user project
- Contains the workflow generator that creates PocketFlow templates for end-user projects
- Includes validation scripts and setup tools (`setup/base.sh`, `setup/project.sh`)
- Defines the orchestrator agent configuration for END-USER projects (not this repo)

### Framework Development Guidelines

#### ❌ DO NOT in this repository:
- Invoke the pocketflow-orchestrator agent (it's for end-user projects)
- Try to "fix" TODO placeholders in `.agent-os/workflows/generator.py` (they're intentional templates)
- Install PocketFlow as a dependency (it gets installed in target projects)
- Expect pytest to find application tests (this is a meta-framework, not an application)
- Treat import errors in generated test files as bugs (they're templates for other projects)

#### ✅ DO understand that:
- `generator.py` creates STARTER templates with TODO stubs for developers to customize
- Import errors in generated code are expected (PocketFlow is installed in target projects)  
- Missing dependencies are intentional (the generator creates templates, not working apps)
- This repository develops the framework, not uses it as an application

### Framework vs Usage Context

**Framework Development (this repository):**
- Improve the Agent OS system, generator, and validation tools
- Focus on template quality, setup scripts, and documentation
- Test the framework itself, not applications built with it

**Framework Usage (end-user repositories):**  
- Where the orchestrator agent runs and is useful
- Where PocketFlow gets installed and workflows are implemented
- Where the generated templates become working applications

### Testing the Framework
```bash
# FRAMEWORK REPOSITORY TESTING (this repo):
# Test the framework code itself
./scripts/run-all-tests.sh

# Test the generator system  
cd framework-tools
python3 test-generator.py
python3 test_full_generation_with_dependencies.py

# Test specific framework validation suites
./scripts/validation/validate-integration.sh
./scripts/validation/validate-orchestration.sh

# FRAMEWORK GENERATES installation scripts for end-users
# (The setup/base.sh and setup/project.sh files are framework output)
# End-user installation testing happens in their projects, not here
```

### Repo-Type Aware Validation

The test harness auto-detects whether it’s running in the Framework repo (this repo) or in an end‑user Project repo, and will SKIP project‑only checks when in framework mode. See the “Repo‑Type Aware Validation” section in the README for details, overrides, and examples.

Quick links:
- README: Repo-Type Aware Validation — README.md:466
- Helper script — `scripts/lib/repo-detect.sh`

### CRITICAL FRAMEWORK vs USAGE DISTINCTION

**⚠️ ALWAYS REMEMBER: This repository IS the Agent OS + PocketFlow framework itself, NOT a project using it.**

**FRAMEWORK DEVELOPMENT (this repository):**
- Contains the meta-system that generates PocketFlow templates for other projects
- Generator creates STARTER TEMPLATES with intentional TODO stubs and placeholder code
- Missing imports/functions in generated code are BY DESIGN - they're templates for developers to customize
- Focus: Improve generator logic, validation scripts, template quality, setup tools
- Test the framework itself, not applications built with it
- DO NOT: Install PocketFlow as dependency, invoke orchestrator agent, fix TODO placeholders, expect working imports in generated code

**FRAMEWORK USAGE (end-user projects):**
- Where PocketFlow gets installed as a dependency  
- Where generated templates become working applications
- Where placeholder functions get implemented
- Where the orchestrator agent runs and is useful
- Where import errors would be actual bugs to fix

**KEY PRINCIPLE:** Template generators should create meaningful placeholder code that shows intent and guides implementation, not working implementations. "Missing" dependencies and undefined functions in generated templates are features, not bugs.

**ALWAYS apply this distinction when reviewing code, identifying bugs, or making improvements. Template generation bugs (syntax errors, broken generators) are real issues. Missing implementations in generated templates are intentional design.**

### Architecture Reminders

#### v1.4.0 Architecture (Base + Project Installations)
- **Base Installation** (`~/.agent-os/`): Customizable standards, reusable across projects
- **Project Installation** (`.agent-os/` in each project): Self-contained, committable to git
- **Framework Repository** (this repo): Creates both base and project installation files
- **Migration Required**: Old single-location installations must migrate to new two-phase system

#### Framework Components
- The `.claude/agents/pocketflow-orchestrator.md` file defines an agent for END-USER projects
- The generator creates templates with intentional placeholder code
- TODO stubs in generated files are starting points, not bugs to fix
- `setup.sh` provides intelligent routing to `setup/base.sh` and `setup/project.sh` based on context
- Old `setup-claude-code.sh` and `setup-legacy.sh` have been removed (obsolete)

# Memory

## Performance Quality Standards
**CRITICAL REMINDER: MAINTAIN HIGH ACCURACY AND ATTENTION TO DETAIL**

### Quality Control Requirements:
- **Always verify counts with bash commands** - don't estimate or guess numbers
- **Double-check multi-step operations** - ensure each step actually completed
- **Use systematic verification** - confirm file changes, git status, actual vs claimed actions
- **Apply "fresh eyes" review** - catch errors before claiming completion
- **Verify assumptions with tools** - use ls, find, grep to confirm findings

### Common Error Patterns to Avoid:
- Counting errors (claimed 6 scripts, actually 7)
- Missing large file collections (.venv with 700+ files)
- Claiming completion without verification (file update ≠ git commit)
- Rushing through analysis without thorough checking
- Assuming operations completed successfully without confirmation

### Mandatory Verification Steps:
1. Use bash commands to verify all counts and file operations
2. Check git status before claiming commits are complete  
3. Apply systematic quality review to all analysis work
4. Validate findings with actual tool output, not assumptions
5. Take time for accuracy over speed

**PERFORMANCE EXPECTATION: High attention to detail and systematic verification of all work.**

- remember when working in this project 🎯 Framework vs Usage Statement

This repository IS the Agent OS + PocketFlow framework itself - NOT a project using it.

Framework Repository (this repo):
- Generates PocketFlow templates for other projects
- Contains setup scripts, validation tools, and code generators
- Template placeholders and TODO stubs are intentional design features
- Dependencies support template generation, not application runtime

Usage Repository (end-user projects):
- Where PocketFlow gets installed as a dependency
- Where generated templates become working applications
- Where the orchestrator agent runs and is useful
- Where placeholder code gets implemented

Key Principle: Missing implementations in generated templates are features, not bugs. This framework creates starting points for
developers, not finished applications.
- don't lie to the user


---
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

---
## Design-First Workflow Framework

The Agent OS + PocketFlow framework **generates templates and tools** that enforce design-first methodology in end-user projects. This section documents how the framework enables design-first development, not workflows for this repository.

### Core Principle: Humans Design, Agents Code

The framework philosophy: **Humans make architectural decisions and create designs. Agents implement code based on those designs.**

### How This Framework Enables Design-First Development

This framework repository **generates** the tools and templates that end-user projects use for design-first development:

#### 1. Framework Components for Product Planning
**Generated by this framework for end-user projects:**
```markdown
# Files this framework creates in end-user projects:
- instructions/core/plan-product.md (orchestrator instructions)
- templates/pocketflow-templates.md (design document templates)
- .claude/agents/pocketflow-orchestrator.md (agent definition)

# What end-users get after framework installation:
/plan-product command → creates docs/design.md, mission.md, roadmap.md
```

#### 2. Framework Components for Feature Specification  
**Generated by this framework for end-user projects:**
```markdown
# Files this framework creates:
- instructions/core/create-spec.md (orchestrator instructions)
- templates/* (feature design templates)

# What end-users get:
/create-spec [feature-name] → extends docs/design.md with feature designs
```

#### 3. Framework Components for Implementation
**Generated by this framework for end-user projects:**
```markdown
# Files this framework creates:
- instructions/core/execute-tasks.md (orchestrator instructions) 
- validation scripts for design-first enforcement

# What end-users get:
/execute-tasks [spec-name] → validates design exists before coding
```

### Design Document Evolution in End-User Projects

The framework **generates templates and validation logic** that ensure design continuity in end-user projects:

1. **Initial Design Templates** (created by this framework's generator):
   - Templates for `docs/design.md` with architectural foundation
   - Product architecture overview sections
   - Primary PocketFlow patterns selection guidance
   - System-wide data flow diagram templates
   - Core SharedStore schema outline templates

2. **Feature Extension Templates** (created by this framework's generator):
   - Feature-specific design section templates
   - Node type selection guidance and configurations  
   - SharedStore schema evolution templates
   - Integration and error handling strategy templates

3. **Implementation Validation Logic** (created by this framework's generator):
   - Validation scripts that verify design completeness
   - Consistency checks between initial and feature designs
   - Logic that blocks implementation without architectural foundation

### Framework Template Philosophy

**IMPORTANT**: This framework generates templates with intentional TODO placeholders:

- **Generated TODOs are features, not bugs** - they guide customization
- **Templates provide structure, humans provide logic** - business logic implementation is intentionally left to developers
- **Design documents contain blueprints** - implementation follows the architectural plan
- **Educational comments explain framework philosophy** - helping users understand the methodology

### Quality Assurance Enabled by Framework

The framework **generates templates and validation** that ensure design-first quality in end-user projects:

- ✅ **Architectural consistency** - Templates enforce consistent patterns across features
- ✅ **Pattern alignment** - Generated templates follow PocketFlow best practices  
- ✅ **Integration planning** - Templates require integration design before implementation
- ✅ **Error handling strategy** - Templates include error handling sections
- ✅ **Performance considerations** - Templates prompt for performance planning
- ✅ **Testing strategy** - Generated templates include testing strategy sections

### Anti-Patterns Framework Prevents

The framework **generates validation logic** that prevents these anti-patterns in end-user projects:

❌ **Skipping design phase** - Framework blocks `/execute-tasks` without complete design
❌ **Incomplete specifications** - Validation requires all design sections completed
❌ **Design-implementation drift** - Generated tests verify implementation matches design
❌ **Pattern mixing** - Templates guide users toward consistent architectural patterns

### Framework Validation Architecture

This framework **generates validation logic** for end-user projects at each phase:

1. **Product Planning Validation**: Generated scripts ensure foundational design completeness
2. **Feature Specification Validation**: Generated logic validates design consistency  
3. **Implementation Validation**: Generated scripts block execution without design documentation
4. **Testing Validation**: Generated tests verify implementation matches specifications

**Framework Development Note**: These validation capabilities are defined in `instructions/core/*.md` files and generated into end-user projects during setup.
