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

---
## Actual Changelog: Agent OS v1.4.0

### Changelog
All notable changes to Agent OS will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

#### 1.4.0 - 2025-08-17
BIG updates in this one! Thanks for all the feedback, requests and support 🙏

#### All New Installation Process
The way Agent OS gets installed is structured differently from prior versions. The new system works as follows:

There are 2 installation processes:
- Your "Base installation" (now optional, but still recommended!)
- Your "Project installation"

##### "Base installation"

- Installs all of the Agent OS files to a location of your choosing on your system where they can be customized (especially your standards) and maintained.
- Project installations copy files from your base installation, so they can be customized and self-contained within each individual project.
- Your base installation now has a config.yml

To install the Agent OS base installation,

1. cd to a location of your choice (your system's home folder is a good choice).

2. Run one of these commands:

- Agent OS with Claude Code support: curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --claude-code
- Agent OS with Cursor support: curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --cursor
- Agent OS with Claude Code & Cursor support: curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --claude-code --cursor
3. Customize your /standards (just like earlier versions)

##### Project installation

- Now each project codebase gets it's own self-contained installation of Agent OS. It no longer references instructions or standards that reside elsewhere on your system. These all get installed directly into your project's .agent-os folder, which brings several benefits:
  - No external references = more reliable Agent OS commands & workflows.
  - You can commit your instructions, standards, Claude Code commands and agents to your project's github repo for team access.

  - You can customize standards differently per project than what's in your base installation.
Your project installation command will be based on where you installed the Agent OS base installation.

  - If you've installed it to your system's home folder, then your project installation command will be ~/.agent-os/setup/project.sh.
  - If you've installed it elsewhere, your command will be /path/to/agent-os/setup/project.sh (after your base installation, it will show you your project installation command. It's a good idea to save it or make an alias if you work on many projects.)
  - If (for whatever reason) you didn't install the base installation, you can still install Agent OS directly into a project, by pulling it directly off of the public github repo using the following command.

    - Note: This means your standards folder won't inherit your defaults from a base installation. You'd need to customize the files in the standards folder for this project. curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/project.sh | bash -s -- --no-base --claude-code --cursor

#### Agent OS config.yml
When you install the Agent OS base installation, that now includes a config.yml file. Currently this file is used for:

- Tracking the Agent OS version you have installed
- Which coding agents (Claude Code, Cursor) you're using
- Project Types (new! read on...)

#### Project Types
If you work on different types of projects, you can define different sets of standards, code style, and instructions for each!

  - By default, a new installation of Agent OS into a project will copy its instructions and standards from your base installation's /instructions and /standards.
  - You can define additional project types by doing the following:
    - Setup a folder (typically inside your base installation's .agent-os folder, but it can be anywhere on your system) which contains /instructions and /standards folders (copy these from your base install, then customize).
    - Define the project type's folder location on your system in your base install's config.yml
  - Using project types:
    - If you've named a project type, 'ruby-on-rails', when running your project install command, add the flag --project-type=ruby-on-rails.
    - To make a project type your default for new projects, set it's name as the value for default_project_type in config.yml

#### Removed or changed in version 1.4.0:
This update does away with the old installation script files:

- setup.sh (replaced by /setup/base.sh and /setup/project.sh)
- setup-claude-code.sh (now you add --claude-code flag to the install commands or enable it in your Agent OS config.yml)
- setup-cursor.sh (now you add --cursor flag to the install commands or enable it in your Agent OS config.yml)
Claude Code Agent OS commands now should not be installed in the ~/.agent-os/.claude/commands folder. Now, these are copied from ~/.agent-os/commands into each project's ~/.claude/commands folder (this prevents duplicate commands showing in in Claude Code's commands list). The same approach applies to Claude Code subagents files.

#### Upgrading to version 1.4.0
Follow these steps to update a previous version to 1.4.0:

1. If you've customized any files in /instructions, back those up now. They will be overwritten.

2. Navigate to your home directory (or whichever location you want to have your Agent OS base installation)

3. Run the following to command, which includes flags to overwrite your /instructions (remove the --cursor flag if not using Cursor): curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup/base.sh | bash -s -- --overwrite-instructions --claude-code --cursor

4. If your ~/.claude/commands contain Agent OS commands, remove those and copy the versions that are now in your base installation's commands folder into your project's .claude/commands folder.

5. Navigate to your project. Run your project installation command to install Agent OS instructions and standards into your project's installation. If your Agent OS base installation is in your system's home folder (like previous versions), then your project installation will be: ~/.agent-os/setup/project.sh

---

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

#### Step 1: Create New Directory Structure ✅ COMPLETED (2025-08-19)
- [x] Create `setup/` directory
- [x] Create `commands/` directory
- [x] Rename `.agent-os/workflows/` to `pocketflow-tools/`
- [x] Create enhanced `config.yml` template

#### Step 2: Develop setup/base.sh ✅ COMPLETED (2025-08-19)
- [x] Base installation logic
- [x] Enhanced instructions installation
- [x] PocketFlow tools installation
- [x] Configuration file creation
- [x] Project script generation

#### Step 3: Develop setup/project.sh ✅ COMPLETED (2025-08-19)
- [x] Project installation logic
- [x] Base installation detection
- [x] Tool integration setup
- [x] PocketFlow orchestration enablement

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