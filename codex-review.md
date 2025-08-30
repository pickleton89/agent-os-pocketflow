Agent OS + PocketFlow Framework — Codex Review Summary

Overview
- Purpose: This repository is the Agent OS + PocketFlow framework itself. It generates PocketFlow-based project templates, provides setup/validation/generation tooling, and ships Claude Code subagents. It is not an end-user app.
- Architecture: Two-phase install (base → ~/.agent-os; project → ./.agent-os). Base provides instructions, standards, commands, PocketFlow tools/templates, and Claude Code agents. Project install copies a self-contained set into the repository.
- Key Principle: Missing implementations and TODO placeholders in generated templates are intentional. This framework provides starting points; end-user projects implement business logic.

Framework vs Usage
- Framework (this repo):
  - Generates PocketFlow templates and supporting files
  - Installs instructions, standards, commands, and Claude Code agents
  - Provides pocketflow-tools (generator, analyzers, validators)
  - Includes validation scripts and integration test plans
- Usage (end-user repos):
  - Install PocketFlow as a dependency
  - Implement placeholder business logic in generated templates
  - Run orchestrator agents and subagents during development
  - Own runtime dependencies, configuration, and deployment

Setup Layer
- Entry router: `setup.sh` auto-detects context and routes to base/project install.
- Base install (`setup/base.sh`): Creates `~/.agent-os` with instructions, standards, commands, pocketflow-tools, templates, and Claude Code agents; writes `config.yml`; generates `setup/project.sh` and `setup/update-project.sh`.
- Project install (`setup/project.sh`): Creates `.agent-os` and `.claude`, copies or downloads instructions/standards/tools/templates; installs Claude Code commands/agents; writes project `.agent-os/config.yml`; updates `.gitignore`; validates structure.
- Update (`setup/update-project.sh`): Copies selected components from base into a project with backups.

Standards (agent-os + PocketFlow)
- best-practices.md: Design-first, PocketFlow philosophy, node lifecycle (prep/exec/post), error-as-branches, reliability and testing guidance.
- code-style.md (+ python, fastapi, pocketflow, testing sub-guides): Naming, imports, docstrings, async patterns, PocketFlow-specific conventions (class naming, action strings, SharedStore types, error patterns, flow wiring), testing patterns for nodes/flows.
- tech-stack.md: Python 3.12+, FastAPI, PocketFlow, pytest, Ruff, ty/mypy, uv; observability suggestions.
- pocket-flow.md: Agentic coding steps, design doc template, example file structure; reiterates “utilities are I/O; LLM steps live in nodes.”

Instructions and Orchestration
- Core instructions: `instructions/core/*.md` for plan-product, analyze-product, create-spec, execute-task(s), post-execution flows; designed to guide toward PocketFlow outputs and design-first.
- Extensions: `instructions/extensions/*` (design-first enforcement, PocketFlow integration) consumed by generator for enhanced TODOs/guidance.
- Orchestration: `instructions/orchestration/*` with coordination hooks, validation notes, and standards.

Claude Code Agents (claude-code/agents)
- Present: `context-fetcher`, `date-checker`, `file-creator`, `project-manager`, `test-runner`, `pattern-recognizer`, `dependency-orchestrator`, `template-validator`, `design-document-creator`, `strategic-planner`, `git-workflow`.
- Role highlights:
  - context-fetcher: selective doc/code retrieval; PocketFlow-aware
  - file-creator: applies PocketFlow templates (design.md, main.py, nodes.py, flow.py, schemas, utils, tests, pyproject)
  - test-runner: pytest/uv detection and focused analysis
  - pattern-recognizer: maps requirements to RAG/AGENT/TOOL/WORKFLOW/etc.; handoff stubs
  - design-document-creator: enforces design-first; emits complete `docs/design.md`
  - strategic-planner: product strategy aligned to PocketFlow patterns
  - dependency-orchestrator: generates tooling/deps (pyproject, uv configs)
  - template-validator: structural check of templates; enforces “templates, not apps”
  - git-workflow, project-manager: PR/branching and tracking/recaps
- Notable gap: `workflow-coordinator` is referenced by plans and code but the agent file is missing here.

PocketFlow Tools (pocketflow-tools)
- generator.py: Produces complete, self-contained PocketFlow projects with:
  - Files: `docs/design.md`, `schemas/models.py`, `utils/*.py`, `nodes.py`, `flow.py`, `main.py`, `router.py`, `tests/*`, `pyproject.toml`, `requirements*.txt`, `.gitignore`, package `__init__.py`s, `README.md`, and a `check-install.py` shim.
  - Patterns: SIMPLE_WORKFLOW/BASIC_API/SIMPLE_ETL plus RAG/AGENT/TOOL/WORKFLOW/MAPREDUCE. Adds enhanced TODOs, orchestrator hints, and “framework boundary” reminders.
  - Extensions: Reads `instructions/extensions/*` to embed guidance.
- pattern_analyzer.py: Requirement → pattern scoring with expanded support for non-LLM (CRUD/API/workflow). Returns a PatternRecommendation with customizations and workflow suggestions.
- workflow_graph_generator.py: Builds workflow graph + Mermaid diagram by pattern; optional complexity add-ons (monitoring, cache, retry).
- template_validator.py: AST-based template validation — syntax/imports, Node/Flow patterns (prep/exec/post, Flow edges), Pydantic structure, utility/test checks, placeholder quality, and framework-vs-usage enforcement.
- dependency_orchestrator.py: Pattern-specific runtime/optional/dev deps and tool configs; emits `pyproject.toml`, uv configs, and requirements files.
- context_manager.py: Extracts planning context from docs and infers patterns/constraints for handoff to implementation.
- status_reporter.py: Tracks progress/status in /tmp with simple console progress.
- testcontentanalyzer/: Intentionally generated example template used by tests/docs to validate generator output; contains PocketFlow imports and TODOs by design.

Validation & Test Artifacts (docs)
- Unified mission and integration plans drive “universal PocketFlow” (design-first, always generate PocketFlow structure).
- Integration test plans and results show subagent context isolation, information flow integrity, and blocking gates for environment/quality/design validation.
- End-to-end validation reports confirm most enhancements; one earlier report flagged a missing `strategic-planner` agent (the agent now exists in this repo).

How It’s Supposed To Work (Happy Path)
1. Install base via `setup.sh` or `setup/base.sh` (adds instructions, standards, pocketflow-tools, templates, Claude Code agents; creates project installer and updater).
2. In a project, run `~/.agent-os/setup/project.sh` to create `.agent-os` + `.claude` and copy components.
3. Use Agent OS commands: `/plan-product` → `/create-spec` → `/execute-tasks`. Subagents assist planning, ensure design-first, select patterns, configure deps, generate templates, and validate structure.
4. The generator creates a complete PocketFlow scaffold with intentional TODOs; the template validator checks structure and philosophy; tests run via test-runner.
5. End-users then implement placeholders in their own repo; the framework repo remains template-focused.

Recommended Improvements & Fixes
- Add missing agent file: `claude-code/agents/workflow-coordinator.md` (referenced by pattern-recognizer and agent_coordination, and listed in setup installers).
- Fix check-install path in generator:
  - `generator.py` references `~/.agent-os/workflows/check-pocketflow-install.py`; the checker actually lives under `pocketflow-tools/check-pocketflow-install.py` (deployed to `.agent-os/pocketflow-tools/`). Update the path or make it configurable via `config.yml`.
- Enforce design doc presence in validation:
  - Extend `template_validator.py` to assert `docs/design.md` exists in generated outputs and contains at least one Mermaid block and required sections (Requirements, Flow Design, Node Specifications). This complements design-first behavior beyond Python-only checks.
- Align Python tool versions:
  - Standards specify Python 3.12+; some tool configs (dependency_orchestrator ruff target-version py39) could be aligned to py312 for consistency across emitted templates.
- Import robustness in pocketflow-tools:
  - Consider package-relative imports for internal modules (`from .pattern_analyzer import ...`) to reduce path sensitivity if tools are executed as a package. Current structure works inside `pocketflow-tools`, but relative imports are safer.
- Confirm installer agent lists:
  - `setup/base.sh` and `setup/project.sh` list PocketFlow agents including `workflow-coordinator`. Ensure the file is present to avoid download failures when offline installs are used.
- Optional: Add a minimal smoke validation script in `scripts/validation/` to check that generated projects include `docs/design.md` with Mermaid, and that `template_validator.py` passes with 0 errors before proceeding.

Key Reminders
- Do not “fix” TODO placeholders in templates in this framework repo — they are features for end-users to fill in.
- Do not install runtime app dependencies here; only framework/tooling dependencies belong.
- Do not run the orchestrator against this repo; orchestrators are for end-user projects.

Quick File Index
- Setup: `setup.sh`, `setup/base.sh`, `setup/project.sh`, `setup/update-project.sh`
- Standards: `standards/*` and `standards/code-style/*`
- Instructions: `instructions/core/*`, `instructions/extensions/*`, `instructions/orchestration/*`
- Agents: `claude-code/agents/*.md`
- Tools: `pocketflow-tools/*` (generator, analyzers, validator, deps, graphs, tests)
- Docs: Validation plans/reports under `docs/*`

Conclusion
This repo cleanly implements a meta-framework: Agent OS for process + PocketFlow for execution architecture. It installs itself into base and projects, generates complete PocketFlow scaffolds, and validates structure while preserving the framework vs usage boundary. Addressing the few gaps above will further harden design-first enforcement and round out subagent coverage.

