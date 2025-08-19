# Agent OS v1.4.0 Migration Plan for agent-os-pocketflow

**Document Created:** 2025-08-19  
**Status:** CRITICAL - Major Architectural Overhaul Required  
**Author:** Claude Code Analysis  

## Executive Summary

This document outlines a critical architectural overhaul required for the agent-os-pocketflow framework due to fundamental changes in Agent OS v1.4.0. The base Agent OS maintainer has completely restructured the installation and architecture system, requiring us to realign our enhanced framework.

## Background: Critical Bug Discovery

### Original Bug Found
During initial setup testing, we discovered that our `setup.sh` script had a fundamental flaw:
- `setup.sh` installed Agent OS files to the local project directory (`.agent-os/`)
- `setup-claude-code.sh` expected files in the home directory (`~/.agent-os/`)
- This mismatch caused installation failures

### Initial Fix Applied
We modified `setup.sh` to install Agent OS files to `$HOME/.agent-os/` instead of the local directory, which resolved the immediate installation issue.

### Discovery of v1.4.0 Changes
During our architectural review, we learned that Agent OS v1.4.0 has completely restructured its installation system, making our initial fix insufficient.

## Agent OS v1.4.0 Architectural Changes

### Previous Architecture (pre-v1.4.0)
- Single installation process
- Mixed global/local file references
- Simple setup scripts

### New v1.4.0 Architecture
Agent OS now uses a two-tier installation system:

#### 1. Base Installation
**Location:** User's choice (typically `~/.agent-os/`)  
**Purpose:** System-wide defaults and templates  
**Contents:**
```
~/.agent-os/
├── config.yml                 # Version and settings tracking
├── standards/                 # Default standards templates
├── instructions/              # Core Agent OS instructions
├── commands/                  # Commands for Claude Code/Cursor
├── claude-code/agents/        # Claude Code agent templates
└── setup/                     # Installation scripts
    ├── base.sh
    └── project.sh
```

#### 2. Project Installation
**Location:** Each project's root directory  
**Purpose:** Self-contained, customizable per-project  
**Contents:**
```
project/
├── .agent-os/                 # Project's own Agent OS copy
│   ├── instructions/          # Copied from base
│   ├── standards/             # Copied from base
│   ├── product/               # Created by plan-product
│   └── specs/                 # Created by create-spec
├── .claude/commands/          # If using Claude Code
└── .cursor/rules/             # If using Cursor
```

### Key v1.4.0 Features
- **Self-contained projects:** No external references
- **Project types:** Different configurations for different project types
- **Configuration tracking:** `config.yml` manages versions and settings
- **Improved reliability:** No broken references to external files

## Impact on agent-os-pocketflow Framework

### Current State Analysis
Our framework currently has:
- Single `setup.sh` (incorrectly mixing base and project setup)
- Enhanced Agent OS instructions with PocketFlow integration
- PocketFlow tools in `.agent-os/workflows/`
- Additional templates and standards
- Framework-specific validation scripts

### Required Changes
To align with v1.4.0, we need a complete restructuring:

## Major Overhaul Plan

### Phase 1: Directory Restructuring

#### New Target Structure
```
agent-os-pocketflow/
├── setup/                     # NEW: v1.4.0 installation scripts
│   ├── base.sh                # Enhanced Agent OS base installation
│   └── project.sh             # Enhanced project installation
├── config.yml                 # NEW: Configuration template
├── commands/                  # NEW: Move from instructions/core/
├── pocketflow-tools/          # RENAME: from .agent-os/workflows/
│   ├── generator.py           # PocketFlow workflow generator
│   ├── pattern_analyzer.py    # Pattern analysis tools
│   ├── template_validator.py  # Validation tools
│   └── dependency_orchestrator.py # Orchestration tools
├── instructions/              # ENHANCED: Agent OS + PocketFlow
│   ├── core/                  # Enhanced core instructions
│   └── meta/                  # Meta instructions
├── standards/                 # ENHANCED: Includes PocketFlow standards
│   ├── tech-stack.md
│   ├── code-style.md
│   ├── best-practices.md
│   ├── pocket-flow.md         # PocketFlow-specific standards
│   └── code-style/
├── templates/                 # KEEP: PocketFlow templates
├── claude-code/               # KEEP: Enhanced Claude Code agents
│   └── agents/
├── docs/                      # KEEP: Documentation
└── README.md                  # UPDATE: New installation instructions
```

#### Files to Remove/Archive
- `setup.sh` → Archive as `setup-legacy.sh`
- `setup-claude-code.sh` → Functionality integrated into new scripts
- `src/`, `tests/` → Remove (shouldn't exist in framework)
- `.agent-os/` → Rename to `pocketflow-tools/`

### Phase 2: New Installation Scripts

#### setup/base.sh
**Purpose:** Install enhanced Agent OS to user's chosen location  
**Functionality:**
- Install to `~/.agent-os/` (or user-specified location)
- Copy enhanced instructions with PocketFlow additions
- Copy enhanced standards including PocketFlow guide
- Install PocketFlow tools (generators, validators, orchestrators)
- Set up commands for Claude Code/Cursor integration
- Create config.yml with PocketFlow settings
- Install project.sh for future project installations

#### setup/project.sh
**Purpose:** Install Agent OS + PocketFlow into specific projects  
**Functionality:**
- Copy instructions from base installation
- Copy standards from base installation
- Create project-specific directories (product/, specs/)
- Set up tool-specific integrations (.claude/, .cursor/)
- Enable PocketFlow orchestration for the project

### Phase 3: Configuration System

#### Enhanced config.yml
```yaml
# Agent OS + PocketFlow Enhanced Configuration
version: "2.0.0"              # Our enhanced version
base_agent_os_version: "1.4.0" # Underlying Agent OS compatibility
created: "2025-08-19"
tools:
  claude_code: true
  cursor: true
  pocketflow: true            # Our enhancement
pocketflow:
  generator_path: "~/.agent-os/pocketflow-tools/generator.py"
  templates_path: "~/.agent-os/templates/"
  orchestrator_enabled: true
  pattern_analyzer_enabled: true
project_types:
  default: "pocketflow-enhanced"
  available:
    - pocketflow-enhanced      # Our default project type
    - standard-agent-os        # Standard Agent OS projects
    - python-pocketflow        # Python-specific PocketFlow
    - fastapi-pocketflow       # FastAPI + PocketFlow
```

### Phase 4: Migration Strategy

#### For New Users
```bash
# Install enhanced Agent OS base
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash

# Install into a project
~/.agent-os/setup/project.sh --pocketflow
```

#### For Existing Users
1. **Backup current installation**
   ```bash
   mv ~/.agent-os ~/.agent-os-backup-$(date +%Y%m%d)
   ```

2. **Run migration script** (to be created)
   ```bash
   ./migrate-to-v2.sh
   ```

3. **Preserve customizations**
   - Standards files customizations
   - Local instruction modifications
   - Project-specific configurations

### Phase 5: Implementation Steps

#### Step 1: Create New Directory Structure
- [ ] Create `setup/` directory
- [ ] Create `commands/` directory
- [ ] Rename `.agent-os/workflows/` to `pocketflow-tools/`
- [ ] Create enhanced `config.yml` template

#### Step 2: Develop setup/base.sh
- [ ] Base installation logic
- [ ] Enhanced instructions installation
- [ ] PocketFlow tools installation
- [ ] Configuration file creation
- [ ] Project script generation

#### Step 3: Develop setup/project.sh
- [ ] Project installation logic
- [ ] Base installation detection
- [ ] Tool integration setup
- [ ] PocketFlow orchestration enablement

#### Step 4: Create Migration Tools
- [ ] Migration script for existing users
- [ ] Backup and restore functionality
- [ ] Validation of successful migration

#### Step 5: Update Documentation
- [ ] Update README with new installation process
- [ ] Update CLAUDE.md with new architecture
- [ ] Create migration guide for users
- [ ] Update all framework documentation

#### Step 6: Testing and Validation
- [ ] Test base installation process
- [ ] Test project installation process
- [ ] Test PocketFlow tools functionality
- [ ] Test backward compatibility
- [ ] Test migration process
- [ ] Integration testing with Claude Code

## Critical Success Factors

### 1. Maintain v1.4.0 Compatibility
Our enhanced version must work exactly like standard Agent OS v1.4.0 while adding PocketFlow capabilities.

### 2. Preserve PocketFlow Features
All existing PocketFlow functionality must continue working:
- Workflow generators
- Pattern analyzers
- Template validators
- Dependency orchestrators

### 3. Clear Framework vs Usage Separation
The framework repository must clearly separate:
- **Framework development:** Tools for building the framework itself
- **End-user functionality:** Tools that get installed for project use

### 4. Smooth Migration Path
Existing users must be able to upgrade without losing:
- Custom standards
- Existing projects
- Tool configurations

## Risk Assessment

### High Risks
- **Breaking existing installations:** Users could lose customizations
- **Tool incompatibility:** PocketFlow tools might not work with new structure
- **Documentation gaps:** Users might not understand new architecture

### Mitigation Strategies
- **Comprehensive backup process:** Automatic backup before migration
- **Staged rollout:** Test with select users before general release
- **Fallback mechanism:** Ability to revert to previous version
- **Extensive testing:** All functionality tested before release

## Timeline and Priorities

### Immediate (Next 1-2 days)
1. Create new directory structure
2. Develop setup/base.sh script
3. Test basic installation flow

### Short-term (Next week)
1. Complete setup/project.sh
2. Create migration tooling
3. Update core documentation

### Medium-term (Next 2 weeks)
1. Comprehensive testing
2. Migration guide creation
3. User communication and rollout

## Success Metrics

### Technical Metrics
- [ ] Installation success rate: 100%
- [ ] All PocketFlow tools functional: 100%
- [ ] Migration success rate: >95%
- [ ] Backward compatibility maintained

### User Experience Metrics
- [ ] Installation time: <2 minutes
- [ ] Clear documentation: User feedback positive
- [ ] Migration confusion: <5% of users need support

## Conclusion

This v1.4.0 migration represents a fundamental architectural shift that, while significant work, will position our agent-os-pocketflow framework for long-term compatibility with the Agent OS ecosystem. The restructuring will improve reliability, maintainability, and user experience while preserving all PocketFlow enhancements.

The key to success is careful planning, comprehensive testing, and clear communication with users throughout the migration process.

---

**Next Actions:**
1. Review and approve this migration plan
2. Begin Phase 1 implementation
3. Coordinate with any existing users for migration timing
4. Execute implementation steps systematically

**Document Status:** Ready for review and implementation approval