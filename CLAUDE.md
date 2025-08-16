# Agent OS + PocketFlow Framework Repository

## ⚠️ IMPORTANT: This IS the Framework
This repository contains the Agent OS + PocketFlow system itself - NOT a project using it.

### What This Repository Does
- Provides the Agent OS system that gets installed to `~/.agent-os/`
- Contains the workflow generator that creates PocketFlow templates for end-user projects
- Includes validation scripts and setup tools for system installation
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
# Run framework validation tests
./scripts/run-all-tests.sh

# Test the generator system  
cd .agent-os/workflows
python test-generator.py

# Test specific validation suites
./scripts/validation/validate-integration.sh
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
- The `.claude/agents/pocketflow-orchestrator.md` file defines an agent for END-USER projects
- The generator creates templates with intentional placeholder code
- TODO stubs in generated files are starting points, not bugs to fix

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
