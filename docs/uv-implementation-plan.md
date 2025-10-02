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
- **Related Docs**:
  - `README.md` — Updated installation commands (see the "Installation" section).
  - `docs/MIGRATION_GUIDE.md` — Step-by-step instructions for upgrading legacy installs.


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
| | 1.6 | Develop `pocketflow_tools/installer_cli.py` (Click-based) sourcing version from package metadata | - [x] | | 2025-10-01 Implemented Click CLI with init command sourcing package version via importlib.metadata |
| | 1.7 | Run smoke import tests for installer module and CLI (`uv run python -c ...`) | - [x] | | 2025-10-07 `uv run python -c "import pocketflow_tools.installer"` + CLI import succeeded |
| 2. Testing & QA | 2.1 | Install package in editable mode (`uv pip install -e .`), verify `agent-os` and `pocketflow-generate` commands | - [x] | | 2025-10-01 `uv pip install -e .`; `uv run agent-os --help`; `uv run pocketflow-generate --help` |
| | 2.2 | Add automated tests for installer + toolkit modules; achieve >80% coverage | - [x] | | 2025-10-08 Added tests/test_installer.py covering installer + toolkit flows; coverage 87% via `UV_CACHE_DIR=.uv-cache uv run pytest --cov=pocketflow_tools.installer tests/test_installer.py` |
| | 2.3 | Execute mock project install (base, `--claude-code`, `--force`); confirm configs, directories, `.gitignore` | - [x] | | 2025-10-01 Mock base install via `agent-os init` + project setup from packaged script; verified config, directories, `.gitignore` in temp workspace |
| | 2.4 | Validate toolkit install and atomic overwrite behaviour (temp directory + atomic rename) | - [x] | | 2025-10-01 Verified atomic toolkit install uses temp dir + rename via pytest (test_install_toolkit_atomic_overwrite_uses_temp_directory) |
| | 2.5 | Exercise error handling (non-project directory, invalid path, pre-existing toolkit) | - [x] | | 2025-10-01 CLI tests cover root/home safeguards, invalid toolkit path, existing install guard via pytest |
| | 2.6 | Re-run regression tests and linting (`uv run pytest`, `uv run ruff check`) | - [x] | | 2025-10-02 `uv run pytest` → 30 passed (legacy CLI suites emit return-value warnings); `uv run ruff check` now clean after adding pytest/ruff config and fixing stray lint hits |
| | 2.7 | Confirm backward compatibility for legacy scripts and root directories | - [x] | | 2025-10-02 Synced framework-tools duplicates with packaged data; diff parity confirmed; setup scripts smoke checks passed |
| 3. Distribution Scenarios | 3.1 | `uvx --from "$REPO_ROOT" agent-os init` smoke test | - [x] | | 2025-10-02 Ran `uvx` smoke install into temp dir with `--yes` + custom install path; report showed 19 created items, no warnings |
| | 3.2 | Test `uv tool install --from "$REPO_ROOT" agent-os-pocketflow`, `uv tool install .`, and uninstall | - [x] | | 2025-10-02 Verified `uv tool install --from "$PWD"` + `uv tool install .` with local XDG dirs; executables linked; `uv tool uninstall agent-os-pocketflow` leaves `uv tool list` empty |
| | 3.3 | Validate project-local install via `uv add agent-os-pocketflow` + `uv run agent-os init` | - [x] | | 2025-10-02 uv add agent-os-pocketflow in temp workspace + agent-os init --install-path .agent-os created 19 paths |
| | 3.4 | Run Docker-based CI simulation (build + run) | - [~] | | 2025-10-02 Added Dockerfile + runner script; blocked from executing due to Docker daemon access in current env · 2025-10-02 Reran via `./scripts/ci/run-docker-ci.sh` with Docker Desktop — image builds and ruff lint now runs, but pipeline stops at `uv run ruff format --check .` reporting 60 files needing formatting (see container log) |
| | 3.5 | Perform Windows (native or WSL) install check; note any platform-specific guidance | - [ ] | | |
| 4. Documentation & Release | 4.1 | Update README installation instructions | - [x] | | 2025-10-02 README install section converted to uv tool + agent-os CLI workflow; updated troubleshooting and migration commands |
| | 4.2 | Author `docs/MIGRATION_GUIDE.md` | - [x] | | 2025-10-09 Migration guide drafted with uv CLI workflow, project update steps, and rollback instructions |
| | 4.3 | Update CHANGELOG with 2.0.0 entry | - [x] | | 2025-10-09 Added 2.0.0 release notes summarizing uv CLI packaging and docs updates |
| | 4.4 | Crosslink plan + docs; ensure commands accurate | - [x] | | 2025-10-09 Linked README + migration guide references in plan and README; corrected migration command block |
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
