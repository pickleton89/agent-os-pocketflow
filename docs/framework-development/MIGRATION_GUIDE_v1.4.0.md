# Agent OS v1.4.0 Framework Architecture Changes

**Document Created:** 2025-08-19  
**Status:** ACTIVE - Framework Development Documentation  
**Version:** Agent OS + PocketFlow v1.4.0

## Overview

⚠️ **Framework Development Context**: This document describes the architectural changes made to the framework itself in v1.4.0. It's for framework contributors who need to understand the new architecture.

**Framework vs Usage**: This repository IS the framework. End-user migration instructions are provided with their framework installations, not here. This documents the framework's internal changes.

## Framework Architecture Changes in v1.4.0

### Framework Output Changed
**Pre-v1.4.0**: Framework generated single installation system
```
Framework created: Single installation to ~/.agent-os/
```

**v1.4.0**: Framework generates two-phase installation system
```
Framework creates:
1. setup/base.sh    -> Installs to ~/.agent-os/ with customizable standards
2. setup/project.sh -> Creates .agent-os/ in each project (self-contained)
```

### Framework Development Impact
- **Framework testing**: Must test both base.sh and project.sh scripts
- **Template generation**: Templates now support project-specific standards
- **Validation scripts**: Must validate both installation types
- **Documentation generation**: Framework creates docs for both phases

## Framework Development Changes Required

### Updated Framework Components
**New files framework developers need to understand:**

```bash
# Framework repository structure (what contributors work on)
setup/base.sh         # Script that installs framework for base usage
setup/project.sh      # Script that installs framework for project usage  
setup/validate-migration.sh  # Validates installation scripts work

# Framework testing must cover both installation types
./scripts/validation/validate-integration.sh  # Tests framework components
./scripts/validation/validate-orchestration.sh # Tests orchestration logic
```

### Framework Testing Changes
Framework contributors must now test both installation paths:

```bash
# Test framework itself (always required)
./scripts/run-all-tests.sh

# Test generator system (core framework functionality)  
cd pocketflow-tools
python test-generator.py
python test-full-generation.py

# Validate that framework creates working installation scripts
./setup/base.sh --test-mode
./setup/project.sh --test-mode
```

### Template System Changes
Framework templates now support:
- **Base installation templates**: Shared standards and configurations
- **Project installation templates**: Self-contained project configurations
- **Config generation**: Creates config.yml for both installation types

### Framework Architecture Benefits
v1.4.0 framework architecture provides:

1. **Better template isolation**: Projects become self-contained
2. **Improved testing**: Can test framework components independently
3. **Enhanced validation**: Separate validation for base vs project installations
4. **Cleaner separation**: Framework vs usage distinction is enforced

## Framework Contributors: Next Steps

For framework development with v1.4.0 architecture:

1. **Test both installation scripts**: Ensure base.sh and project.sh work correctly
2. **Update generator templates**: Support project-specific customization
3. **Validate framework output**: Templates work in both base and project contexts  
4. **Maintain distinction**: Framework code vs generated templates remain separate

**End-user migration instructions**: Provided with their framework installations, not in this repository.

---

**Framework Development**: This repository creates the v1.4.0 installation system that end-users will use. Framework contributors work on improving the generator, templates, and validation systems - not on using the framework in projects.