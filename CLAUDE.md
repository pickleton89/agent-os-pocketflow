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

### Architecture Reminders
- The `.claude/agents/pocketflow-orchestrator.md` file defines an agent for END-USER projects
- The generator creates templates with intentional placeholder code
- TODO stubs in generated files are starting points, not bugs to fix
