# Framework vs Implementation Analysis Plan

> **Critical Project Review for Agent OS + PocketFlow Framework**  
> Created: 2025-08-16  
> Purpose: Identify and eliminate framework vs end-user implementation confusion

## Context & Problem Statement

### The Core Issue
This repository contains the **Agent OS + PocketFlow framework itself** - NOT a project using it. However, during early development stages, there may have been confusion between framework development and end-user implementation patterns that could still exist in the codebase.

### Framework vs Usage Distinction

**FRAMEWORK DEVELOPMENT (this repository):**
- Contains the meta-system that generates PocketFlow templates for other projects
- Generator creates STARTER TEMPLATES with intentional TODO stubs and placeholder code
- Missing imports/functions in generated code are BY DESIGN - they're templates for developers to customize
- Focus: Improve generator logic, validation scripts, template quality, setup tools
- Test the framework itself, not applications built with it

**FRAMEWORK USAGE (end-user projects):**
- Where PocketFlow gets installed as a dependency  
- Where generated templates become working applications
- Where placeholder functions get implemented
- Where the orchestrator agent runs and is useful
- Where import errors would be actual bugs to fix

### Red Flags to Look For
- Direct PocketFlow imports/usage outside of template generation
- Working implementations where there should be placeholder templates
- End-user project patterns (app configs, business logic, etc.)
- Orchestrator agent invocations in framework code
- Tests that validate application features instead of framework capabilities

## Analysis Phases

### Phase 1: Structural Analysis

#### 1.1 Project Structure Review
**Objective:** Identify inappropriate end-user project files  
**Action Items:**
- Check root directory for application-specific files (main.py, app.py, etc.)
- Look for business logic directories that shouldn't exist in a framework
- Identify any MVC/application architecture patterns
- Verify src/ directory contains framework code, not application code

**Expected Framework Structure:**
```
├── .agent-os/           # Templates and generator
├── scripts/             # Framework setup/validation
├── docs/               # Framework documentation
├── pyproject.toml      # Framework dependencies
├── CLAUDE.md           # Framework instructions
└── tests/              # Framework tests
```

#### 1.2 Dependency Analysis
**Objective:** Ensure PocketFlow isn't incorrectly installed as dependency  
**Action Items:**
- Review pyproject.toml dependencies section
- Check for pocketflow in requirements files
- Verify uv.lock doesn't contain PocketFlow packages
- Confirm dependencies are for framework development, not application runtime

**Framework Dependencies Should Include:**
- Development tools (ruff, ty, pytest)
- Template generation libraries
- Setup/installation utilities
- NOT: PocketFlow, application frameworks, business logic libraries

#### 1.3 Configuration Review
**Objective:** Verify configs are for framework development, not applications  
**Action Items:**
- Review .env files for application vs framework config
- Check for app-specific settings (database URLs, API keys for apps)
- Verify CI/CD configs test framework, not applications
- Ensure IDE configs support framework development

### Phase 2: Code Analysis

#### 2.1 Direct PocketFlow Usage Check
**Objective:** Find code that imports/uses PocketFlow directly  
**Action Items:**
- Search for `import pocketflow` or `from pocketflow`
- Look for direct PocketFlow class instantiations
- Check for workflow execution code outside templates
- Verify any PocketFlow references are in template strings only
- **⚠️ INVESTIGATE:** `.agent-os/workflows/testcontentanalyzer/` contains working PocketFlow code with direct imports (`from pocketflow import Flow`, `from pocketflow import Node`) - this violates framework boundaries even if used for testing

**Search Commands:**
```bash
grep -r "import pocketflow" .
grep -r "from pocketflow" .
grep -r "PocketFlow" --include="*.py" .
```

#### 2.2 Import Statement Analysis
**Objective:** Look for end-user project import patterns  
**Action Items:**
- Find imports that suggest application structure
- Check for business domain imports (users, orders, products, etc.)
- Look for framework imports being used as application dependencies
- Verify template imports are properly quoted/escaped

#### 2.3 Business Logic Check
**Objective:** Identify application-specific logic in framework code  
**Action Items:**
- Search for domain-specific functions (create_user, process_order, etc.)
- Look for database models for applications
- Check for API endpoints serving application features
- Verify any business logic is in template form only

### Phase 3: Template & Generator Analysis

#### 3.1 Generated Template Verification
**Objective:** Ensure templates contain proper placeholders vs working implementations  
**Action Items:**
- Review .agent-os/workflows/ for template quality
- Check that generator.py creates placeholders, not implementations
- Verify TODO stubs are meaningful and guide implementation
- Ensure templates show intent without working code

**Template Quality Criteria:**
- Contains `# TODO:` comments with clear instructions
- Has placeholder functions with docstrings
- Shows expected structure without implementation
- Includes import statements that would work in target projects

#### 3.2 Agent Invocation Check
**Objective:** Find inappropriate orchestrator agent usage in framework code  
**Action Items:**
- Search for pocketflow-orchestrator agent calls
- Check for Task tool usage with orchestrator agent
- Verify orchestrator is only referenced in templates/docs
- Ensure no direct agent execution in framework scripts

**Search Commands:**
```bash
grep -r "pocketflow-orchestrator" .
grep -r "Task.*orchestrator" .
```

#### 3.3 Workflow Analysis
**Objective:** Review workflow files for implementation vs template confusion  
**Action Items:**
- Examine .agent-os/workflows/ directory structure
- Verify workflow files are templates, not working implementations
- Check for hardcoded values instead of placeholders
- Ensure workflows demonstrate patterns, not specific solutions

### Phase 4: Testing & Validation

#### 4.1 Test File Review
**Objective:** Ensure tests validate framework capabilities, not application features  
**Action Items:**
- Review test/ directory for application vs framework tests
- Check test naming conventions (test_generator vs test_user_login)
- Verify tests exercise template generation, not template usage
- Ensure no end-user feature testing

**Framework Test Categories:**
- Generator functionality tests
- Template quality validation
- Setup script testing
- Documentation accuracy checks

#### 4.2 Validation Script Analysis
**Objective:** Verify scripts test framework, not app functionality  
**Action Items:**
- Review scripts/ directory purpose and scope
- Check validation scripts test framework installation
- Verify scripts don't test application features
- Ensure scripts validate template generation quality

#### 4.3 .agent-os Directory Review
**Objective:** Confirm it contains only generator templates  
**Action Items:**
- Verify all files are templates or generators
- Check for working implementations instead of placeholders
- Ensure no application-specific configurations
- Validate template structure follows framework patterns

### Phase 5: Documentation & Scripts

#### 5.1 Script Purpose Verification
**Objective:** Ensure scripts are for framework development  
**Action Items:**
- Review all shell scripts for appropriate scope
- Check Python scripts serve framework needs
- Verify no application deployment scripts
- Ensure scripts support framework development workflow

#### 5.2 Documentation Clarity
**Objective:** Check docs maintain framework vs usage distinction  
**Action Items:**
- Review README for clear framework positioning
- Check documentation doesn't mix framework and usage instructions
- Verify examples show template generation, not template usage
- Ensure architectural docs focus on framework design

### Phase 6: Synthesis & Reporting

#### 6.1 Comprehensive Analysis
**Objective:** Compile findings with specific recommendations  
**Action Items:**
- Categorize all findings by severity and impact
- Provide specific file/line references for issues
- Recommend concrete remediation steps
- Prioritize changes by architectural importance

## Analysis Checklist

### Pre-Analysis Setup
- [ ] Clone fresh copy of repository
- [ ] Review current branch and recent commits
- [ ] Understand latest framework architecture
- [ ] Set up analysis tools and search commands

### Execution Tracking
- [ ] Phase 1: Structural Analysis Complete
- [ ] Phase 2: Code Analysis Complete  
- [ ] Phase 3: Template & Generator Analysis Complete
- [ ] Phase 4: Testing & Validation Complete
- [ ] Phase 5: Documentation & Scripts Complete
- [ ] Phase 6: Synthesis & Reporting Complete

### Deliverables
- [ ] Detailed findings report with file references
- [ ] Prioritized remediation plan
- [ ] Updated architectural guidelines
- [ ] Verification that framework maintains proper boundaries

## Key Success Criteria

1. **Zero Direct PocketFlow Usage** - Framework code never imports/uses PocketFlow directly
2. **Proper Template Structure** - All generated code contains meaningful placeholders
3. **Framework-Focused Tests** - Tests validate framework capabilities, not applications
4. **Clear Architectural Boundaries** - No confusion between framework and end-user patterns
5. **Generator Quality** - Templates guide implementation without providing working code

## Future Reference

This document serves as a repeatable analysis framework for maintaining architectural integrity. Use this checklist whenever:
- Adding new framework features
- Reviewing contributions
- Conducting periodic architectural reviews
- Onboarding new framework developers

**Remember:** Template generators should create meaningful placeholder code that shows intent and guides implementation, not working implementations. "Missing" dependencies and undefined functions in generated templates are features, not bugs.