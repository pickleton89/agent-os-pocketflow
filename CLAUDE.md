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
cd pocketflow-tools
python test-generator.py
python test-full-generation.py

# Test specific framework validation suites
./scripts/validation/validate-integration.sh
./scripts/validation/validate-orchestration.sh

# FRAMEWORK GENERATES installation scripts for end-users
# (The setup/base.sh and setup/project.sh files are framework output)
# End-user installation testing happens in their projects, not here
```

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
