# Repository Guidelines

## Framework vs Usage
This repository is the Agent OS + PocketFlow framework — not an application using it.
- Framework (this repo): generators, setup/validation scripts, and code templates with intentional TODOs; dependencies support template generation.
- Usage (end-user projects): PocketFlow installed as a dependency; generated templates become working apps; the orchestrator runs here; TODOs are implemented.
Key principle: Missing implementations in generated templates are features, not bugs.

## Critical Reminders
1. Be completely honest — if you don’t know or made an error, say so immediately.
2. Think carefully before acting — review your approach before implementing.
3. Write high‑quality code — check for bugs, inconsistencies, and edge cases.
4. Verify your work — actually test/validate claims rather than assuming.
5. No false progress — don’t claim completion of tasks you haven’t done.

## Project Structure & Module Organization
- `framework-tools/`: Core PocketFlow tooling and tests (e.g., `generator.py`, `pattern_analyzer.py`, `test_*.py`).
- `scripts/`: Validation and orchestration scripts (e.g., `scripts/run-all-tests.sh`, `validation/*.sh`).
- `standards/`: Authoritative coding, testing, and FastAPI/PocketFlow style guides.
- `templates/` and `docs/`: Workflow templates and documentation.
- `.agent-os/` (optional): Local workspace created by setup or generators.

## Build, Test, and Development Commands
- Create venv and install deps: `uv venv && source .venv/bin/activate && uv pip install -e .`
- Run full validations: `bash scripts/run-all-tests.sh` (add `-q` for quick, `-v` for verbose).
- Run framework tests: `uv run pytest -q pocketflow_tools/`
- Generate a workflow: `uv run python -m pocketflow_tools.cli --spec framework-tools/examples/agent-workflow-spec.yaml --output /path/to/end-user-project`
- Bootstrap Agent OS locally: `bash ./setup.sh --help` (see modes `base`, `project`, `auto`).

## Coding Style & Naming Conventions
- Language: Python 3.12 (`.python-version`). Indentation: 4 spaces.
- Naming: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- Lint/format: Prefer `ruff` (target py312, line length ~88). Type hints encouraged; keep functions small and composable.
- Follow `standards/code-style.md` plus `standards/code-style/{python-style.md,fastapi-style.md,pocketflow-style.md}`.

## Testing Guidelines
- Framework: `pytest`. Tests live alongside tools in `framework-tools/` and under `framework-tools/testcontentanalyzer/tests/`.
- Naming: `test_*.py`, test functions `test_*`. Use markers only when needed.
- Run smoke or comprehensive via repo scripts (see `scripts/validation/*`). Quick check: `uv run pytest -q framework-tools`.
- Add focused unit tests for utilities and flows; include minimal fixtures and clear assertions.
 - Repo-type aware validation: the harness auto-detects framework mode and skips project-only checks.

## Repository Do/Don'ts
- Don’t install PocketFlow as a dependency in this repo; it belongs in end-user projects.
- Don’t “fix” TODO placeholders in generated templates; they are intentional teaching stubs.
- Don’t invoke the PocketFlow orchestrator agent from this repo; it runs in usage repos.
- Don’t treat import errors in generated example templates as bugs; they resolve in target projects.

## Commit & Pull Request Guidelines
- Conventional prefixes observed: `feat:`, `fix:`, `docs:`, `chore:`, `tests:` (see `git log`).
- Commits: present tense, scoped subject; small, logical changes.
- PRs: include goal summary, key changes, validation steps (e.g., output from `scripts/run-all-tests.sh`), and link issues. Add screenshots/logs for UX flows when relevant.

## Security & Configuration Tips
- Config: review `config.yml` before running scripts; avoid committing secrets.
- Isolation: use `uv` and a local `.venv`. Prefer `uv run ...` for commands.
- Generated outputs: workflows write to `.agent-os/workflows/` by default—verify before committing.
