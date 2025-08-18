# Configuration Guidelines

> **Framework Repository Configuration Standards**  
> Last Updated: 2025-08-16

## Overview

This document outlines the configuration approach for the Agent OS + PocketFlow framework repository. As a meta-framework that generates templates for end-user projects, this repository maintains minimal configurations focused solely on framework development needs.

## Framework vs Application Configuration

### ✅ Appropriate Framework Configurations

**Development Tools:**
- `pyproject.toml` - Framework dependencies and metadata
- `.python-version` - Python version specification for framework development
- `.gitignore` - Standard ignores for framework development
- `uv.lock` - Dependency lock file for reproducible framework builds

**Claude Code Integration:**
- `.claude/config.json` - MCP server configurations for framework development
- `.claude/settings.local.json` - Permissions for framework development tools
- `.claude/agents/` - Agent definitions for END-USER projects (not this repo)

**Framework Templates:**
- `.agent-os/workflows/*.yaml` - Workflow specification templates
- `.agent-os/instructions/` - Template generation instructions

### ❌ Inappropriate Application Configurations

**Environment Files:**
- `.env` files with application secrets/settings
- Database connection strings
- API keys for specific applications
- Application-specific environment variables

**CI/CD for Applications:**
- Deployment pipelines for end-user applications
- Application testing workflows (vs framework testing)
- Production environment configurations

**Application Dependencies:**
- PocketFlow as a runtime dependency (it's installed in target projects)
- Business logic libraries
- Application-specific frameworks beyond template generation needs

**IDE Configurations:**
- Application-specific debugger configurations
- Runtime configurations for end-user applications
- Project-specific settings that aren't framework development related

## Current Configuration Status

### Existing Configurations

1. **pyproject.toml**
   - Purpose: Framework metadata and development dependencies
   - Dependencies: FastAPI (to generate FastAPI templates), pytest, PyYAML
   - Status: ✅ Appropriate for framework

2. **.python-version**
   - Purpose: Specify Python version for framework development
   - Value: 3.11
   - Status: ✅ Appropriate

3. **.claude/config.json**
   - Purpose: MCP server configuration for documentation access
   - Contains: Git documentation server for this repository
   - Status: ✅ Appropriate for framework development

4. **.claude/settings.local.json**
   - Purpose: Permissions for framework development tools
   - Contains: Allowed bash commands, MCP tools, etc.
   - Status: ✅ Appropriate for framework development

### What's Missing (Intentionally)

- **No .env files** - Framework doesn't need environment-specific configs
- **No CI/CD pipelines** - Framework testing is handled through validation scripts
- **No application configs** - This generates templates; doesn't run applications
- **No PocketFlow runtime configs** - PocketFlow is installed in target projects

## Configuration Validation

### Red Flags to Watch For

1. **Application-Specific Environment Variables:**
   ```bash
   # BAD - Application configs in framework
   DATABASE_URL=postgres://...
   API_KEY=sk-...
   REDIS_URL=redis://...
   ```

2. **PocketFlow Runtime Dependencies:**
   ```toml
   # BAD - PocketFlow as framework dependency
   dependencies = [
       "pocketflow>=1.0.0",  # Should not be here
   ]
   ```

3. **Application CI/CD:**
   ```yaml
   # BAD - Deploying applications from framework repo
   - name: Deploy to Production
     run: deploy-app.sh
   ```

### Validation Commands

```bash
# Check for inappropriate environment files
find . -name "*.env*" -not -path "./.venv/*" -not -path "./.git/*"

# Check for PocketFlow dependencies (runtime deps, not project name)
grep '"pocketflow' pyproject.toml uv.lock 2>/dev/null | grep -v 'name.*agent-os-pocketflow' || echo "Good - no PocketFlow deps"

# Check for application-specific configs
find . -name "docker-compose.yml" -o -name "Dockerfile" -o -name "kubernetes.yaml"
```

## Best Practices

### When Adding New Configurations

1. **Ask: "Is this for framework development or application usage?"**
   - Framework development: ✅ Add it
   - Application usage: ❌ Don't add it

2. **Prefer minimal configurations**
   - Only add what's absolutely necessary
   - Document why each config is needed

3. **Use template patterns for end-user configs**
   - Instead of adding app configs here, create templates that generate them
   - Store templates in `.agent-os/workflows/` or similar

### Configuration Documentation

- Document the purpose of each configuration file
- Explain why certain configs are intentionally absent
- Provide examples of what NOT to add

## Troubleshooting

### "Why don't I see [application config] in this repository?"

This repository IS the framework, not a project using it. Application configurations belong in the projects that the framework generates, not in the framework itself.

### "How do I configure [application feature]?"

Create a template that generates the configuration in target projects. The framework creates starting points for developers to customize.

### "Why can't I find PocketFlow configurations?"

PocketFlow gets installed and configured in end-user projects. This framework repository generates the templates and setup for those projects.

## Framework Boundaries

Remember: This repository generates templates and tools for other projects. It should not contain the configurations that those projects will use - instead, it should contain the generators that create those configurations.

**Key Principle:** If a configuration would be used by an end-user application, it belongs in the generated templates, not in this framework repository.