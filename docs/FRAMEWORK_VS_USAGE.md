# 🎯 Framework vs Usage Statement

This repository IS the Agent OS + PocketFlow framework itself — NOT a project using it.

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

Key Principle: Missing implementations in generated templates are features, not bugs. This framework creates starting points for developers, not finished applications.

## Canonical Validator & Ownership
- Source of truth for template validation lives in `pocketflow-tools/template_validator.py` (framework repo).
- Wrapper entry points: `scripts/validation/validate-generation.py` and `scripts/validation/validate-template-structure.sh` both delegate to the canonical validator.
- Usage repositories consume generated templates; they do not duplicate validator logic. Validation rules change in one place (this framework) and propagate via the wrappers.
