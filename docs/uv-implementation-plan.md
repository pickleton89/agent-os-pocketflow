# Agent OS + PocketFlow — uv Installation Implementation Plan (v2.1)

_This plan expands the v2.1 strategy into trackable tasks. Update checkboxes, status notes, and timestamps as work progresses._

## Overview
- **Goal**: Replace bash-driven installation with a uv-powered Python package while keeping workflow generation intact and legacy scripts compatible.
- **Scope**: Package metadata, data layout, installer module + CLI, documentation, regression testing, distribution verification.
- **Non-Goals**: Changing generated templates, modifying workflow generator behaviour, or deprecating legacy scripts during this release.
- **Success Criteria**:
  - `agent-os` CLI works via editable install, `uvx`, and `uv tool install`.
  - Backward compatibility validated (`pocketflow-generate`, legacy bash scripts, existing projects).
  - Automated tests cover installer logic (>80% module coverage).
  - Documentation updated (README, migration guide, changelog) with accurate commands.

## Tracking Legend
- `- [ ]` Not started · `- [~]` In progress · `- [x]` Complete
- Update the **Status / Notes** column with date + short summary when a box changes state.

| Phase | Step | Task | Status | Owner | Status / Notes |
|-------|------|------|--------|-------|----------------|
| 0. Preparation | 0.1 | Capture repo root (`REPO_ROOT=$(git rev-parse --show-toplevel)`) for reuse | - [x] | | 2025-10-01 Captured repo root `/Users/jeffkiefer/Documents/projects/agent-os-pocketflow` via git |
| | 0.2 | Verify environment (`uv --version`, `python --version`, `git status`; run `uv run pytest -q framework-tools`) | - [x] | | 2025-10-01 `uv 0.8.8`, `python 2.7.18`, clean git status, `uv run pytest -q framework-tools` passed (warnings only) |
| 1. Package Structure | 1.1 | Add dependencies `click`, `rich` via `uv add` | - [x] | | 2025-10-01 Added `click`, `rich` with `uv add`; pyproject and uv.lock updated |
| | 1.2 | Update `pyproject.toml` metadata (version 2.0.0, classifiers, URLs, dependencies, scripts) and validate TOML | - [x] | | 2025-10-01 Updated metadata, added classifiers/URLs/scripts, refreshed uv.lock, validated TOML with uv |
| | 1.3 | Copy repository data into `pocketflow_tools/data/` (keep root copies), update packaging config, append `.gitignore` note with leading newline | - [x] | | 2025-10-01 Mirrored instructions/standards/templates/claude-code/shared/setup/config.yml into package data; updated pyproject + .gitignore note · 2025-10-06 Marked complete in plan |
| | 1.4 | Implement `pocketflow_tools/data/__init__.py` exposing data directory constants | - [x] | | 2025-10-06 Added resource helpers + constants for packaged data |
| | 1.5 | Develop `pocketflow_tools/installer.py` with safe force install (pre-remove targets via `shutil.rmtree`) + toolkit logic | - [x] | | 2025-10-07 Implemented AgentOsInstaller module with force-safe copy helpers |
| | 1.5.2 | Package PocketFlow toolkit resources so installer deployments include framework tools | - [x] | | 2025-10-01 Mirrored framework-tools into packaged data + added lookup helper |
| | 1.6 | Develop `pocketflow_tools/installer_cli.py` (Click-based) sourcing version from package metadata | - [ ] | | |
| | 1.7 | Run smoke import tests for installer module and CLI (`uv run python -c ...`) | - [ ] | | |
| 2. Testing & QA | 2.1 | Install package in editable mode (`uv pip install -e .`), verify `agent-os` and `pocketflow-generate` commands | - [ ] | | |
| | 2.2 | Add automated tests for installer + toolkit modules; achieve >80% coverage | - [ ] | | |
| | 2.3 | Execute mock project install (base, `--claude-code`, `--force`); confirm configs, directories, `.gitignore` | - [ ] | | |
| | 2.4 | Validate toolkit install and atomic overwrite behaviour (temp directory + atomic rename) | - [ ] | | |
| | 2.5 | Exercise error handling (non-project directory, invalid path, pre-existing toolkit) | - [ ] | | |
| | 2.6 | Re-run regression tests and linting (`uv run pytest`, `uv run ruff check`) | - [ ] | | |
| | 2.7 | Confirm backward compatibility for legacy scripts and root directories | - [ ] | | |
| 3. Distribution Scenarios | 3.1 | `uvx --from "$REPO_ROOT" agent-os init` smoke test | - [ ] | | |
| | 3.2 | Test `uv tool install --from "$REPO_ROOT" agent-os-pocketflow`, `uv tool install .`, and uninstall | - [ ] | | |
| | 3.3 | Validate project-local install via `uv add agent-os-pocketflow` + `uv run agent-os init` | - [ ] | | |
| | 3.4 | Run Docker-based CI simulation (build + run) | - [ ] | | |
| | 3.5 | Perform Windows (native or WSL) install check; note any platform-specific guidance | - [ ] | | |
| 4. Documentation & Release | 4.1 | Update README installation instructions | - [ ] | | |
| | 4.2 | Author `docs/MIGRATION_GUIDE.md` | - [ ] | | |
| | 4.3 | Update CHANGELOG with 2.0.0 entry | - [ ] | | |
| | 4.4 | Crosslink plan + docs; ensure commands accurate | - [ ] | | |
| Wrap-up | W.1 | Final validation pass (spot-check commands, re-run key tests) | - [ ] | | |
| | W.2 | Review against success criteria; capture lessons learned | - [ ] | | |

## Status Log
_Use this table to append notable events (branch merges, issues, decisions)._ 

| Date | Author | Summary |
|------|--------|---------|
| | | |

## Notes & Decisions
- Document any deviations from plan, blockers encountered, or follow-up items here.
- CLI version sourcing **must** use `importlib.metadata.version("agent-os-pocketflow")`; no hardcoded literals.
- Capture `REPO_ROOT=$(git rev-parse --show-toplevel)` during Phase 0 and reuse that variable in every off-repo scenario (e.g., Phase 3 uvx smoke tests).
- Force reinstall flows remove existing targets with `shutil.rmtree` before copying new files.
- Toolkit installs write into a temporary directory and atomically rename into place to prevent partial state.
- When appending to `.gitignore`, ensure the existing file ends with `\n` before writing new entries.

## Rollback Checklist
- Keep prior release tag (`v0.1.0`) accessible.
- If rollback needed: revert implementation commits, restore documentation, ensure legacy scripts remain functional.

---

**Next Action**: Begin Phase 0 once the team approves this tracking plan.
