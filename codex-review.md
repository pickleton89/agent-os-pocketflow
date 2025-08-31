Agent OS + PocketFlow Framework — Codex Review Summary

Update — 2025-08-30 (docs ignored)
- Scope: Re-audit focusing on code, setup scripts, standards, and pocketflow-tools; intentionally ignoring the ./docs directory.
- Mission fit: The repo correctly behaves as a framework that generates PocketFlow templates and ships installers/validators; no usage-repo behavior detected.
- Key confirmations and deltas:
  1) Workflow-coordinator split acknowledged (no agent file needed)
     - Functionality now lives in `pocketflow-tools/generator.py`, `pocketflow-tools/template_validator.py`, and `pocketflow-tools/pattern_analyzer.py`.
     - Adjust references: remove `workflow-coordinator.md` from setup download lists and validation expectations; update agent docs and hooks to point to file-creator/generator and template-validator.
     - Implemented: setup scripts and validation updated; pattern-analyzer agent doc and generator guidance updated.
  2) Generator’s install-check path corrected
     - Generated shim now points to `~/.agent-os/pocketflow-tools/check-pocketflow-install.py` to match deployed checker location.
  3) Python version alignment (completed)
     - Standards: Python 3.12+ (standards/tech-stack.md)
     - Framework root: `requires-python >=3.12` (pyproject.toml)
     - Tooling targets: ruff `py312`, ty/mypy `3.12`
     - Base installer prerequisite: Python 3.12+
     - Outcome: Consistent 3.12 target across framework and generated templates
  4) Validation scripts assume usage-repo context
     - Scripts require `.agent-os/workflows` or `.claude/agents` in the current repo.
     - Evidence: `scripts/validation/validate-pocketflow.sh:14`, `scripts/validation/validate-sub-agents.sh:48` and master runner includes them.
     - Impact: Running `scripts/run-all-tests.sh` from framework root may fail despite framework being correct.
     - Recommendation: Gate tests by repository type: detect framework context (presence of `pocketflow-tools/generator.py`) and skip usage-only checks, or add a `--framework` mode.
  5) Import stability in pocketflow-tools
     - Mixed import styles: generator uses package-relative imports with fallback handling, while `agent_coordination.py` uses absolute (`from pattern_analyzer import ...`).
     - Evidence: `pocketflow-tools/agent_coordination.py:13`
     - Recommendation: Use a try/except pattern for relative-then-absolute imports for robustness when running as a script vs. package.
  6) Base installer Python prerequisite too lax vs. emitted environments
     - Base checks 3.8+, while emitted configs and checker expect 3.11+.
     - Recommendation: Raise base prerequisite to 3.11+ (or 3.12+) to match emitted templates and `check-pocketflow-install.py`.
  7) Claude Code agent download vs. local copy skew
     - Remote download list updated to remove workflow-coordinator; copy branch continues to mirror local agents.
     - Follow-up: Optional post-copy verification for the active agent set (pattern-analyzer, template-validator, dependency-orchestrator, design-document-creator, strategic-planner).
  8) Optionally add non-interactive install mode
     - `setup.sh` prompts for confirmation during auto detection.
     - Recommendation: Add `--yes` flag to bypass prompts to aid CI or scripted bootstrap.
  9) FastAPI as a framework dependency
     - Root `pyproject.toml` includes FastAPI; it appears used for template tests (`testcontentanalyzer`) rather than runtime.
     - Recommendation: If desired, move to dev dependencies in framework context; not required for template generation.

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
- Present: `context-fetcher`, `date-checker`, `file-creator`, `project-manager`, `test-runner`, `pattern-analyzer`, `dependency-orchestrator`, `template-validator`, `design-document-creator`, `strategic-planner`, `git-workflow`.
- Role highlights:
  - context-fetcher: selective doc/code retrieval; PocketFlow-aware
  - file-creator: applies PocketFlow templates (design.md, main.py, nodes.py, flow.py, schemas, utils, tests, pyproject)
  - test-runner: pytest/uv detection and focused analysis
  - pattern-analyzer: maps requirements to RAG/AGENT/TOOL/WORKFLOW/etc.; handoff stubs
  - design-document-creator: enforces design-first; emits complete `docs/design.md`
  - strategic-planner: product strategy aligned to PocketFlow patterns
  - dependency-orchestrator: generates tooling/deps (pyproject, uv configs)
  - template-validator: structural check of templates; enforces “templates, not apps”
  - git-workflow, project-manager: PR/branching and tracking/recaps
    - Note: workflow-coordinator responsibilities moved into pocketflow-tools (generator/template_validator/pattern_analyzer); agent reference removed in setup/validation/docs.

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



Quick File Index
- Setup: `setup.sh`, `setup/base.sh`, `setup/project.sh`, `setup/update-project.sh`
- Standards: `standards/*` and `standards/code-style/*`
- Instructions: `instructions/core/*`, `instructions/extensions/*`, `instructions/orchestration/*`
- Agents: `claude-code/agents/*.md`
- Tools: `pocketflow-tools/*` (generator, analyzers, validator, deps, graphs, tests)
- Docs: Validation plans/reports under `docs/*`

Conclusion
This repo cleanly implements a meta-framework: Agent OS for process + PocketFlow for execution architecture. It installs itself into base and projects, generates complete PocketFlow scaffolds, and validates structure while preserving the framework vs usage boundary. Addressing the few gaps above will further harden design-first enforcement and round out subagent coverage.
