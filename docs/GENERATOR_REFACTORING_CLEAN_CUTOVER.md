# Generator Refactoring — Clean Cutover Plan

## Executive Summary

- Objective: Replace the monolithic `pocketflow-tools/generator.py` with a modular Python package `pocketflow_tools` while preserving CLI behavior, generated outputs, and framework philosophy.
- Approach: Clean cutover (no facade). Update all internal imports, scripts, and docs to the new package and CLI, then remove the old file.
- Non‑Goals: Do not change generated file contents, layout, or the “templates, not finished apps” contract.

## Framework vs Usage Principles

- Framework repo (this repo): Generates PocketFlow templates, contains setup/validation tools, uses TODO placeholders intentionally, and keeps runtime deps minimal.
- Usage repos (end‑user projects): Install PocketFlow, host generated templates, implement TODOs, and run orchestrator agents.
- Key principle: Missing implementations in generated templates are features, not bugs.

## Outcomes

- New import surface: `from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator` and `from pocketflow_tools.spec import WorkflowSpec`.
- New CLI: `python -m pocketflow_tools.cli --spec <file> --output <dir>` with identical flags, messages, and exit codes.
- Generated outputs remain byte‑for‑byte identical across supported patterns.

## Package Layout

- pocketflow_tools/
  - `__init__.py`
  - `spec.py` — `WorkflowSpec`
  - `cli.py` — CLI entrypoint (parity with current `main()`)
  - generators/
    - `__init__.py`
    - `template_engine.py` — template + extension loading/parsing
    - `code_generators.py` — nodes/flow/models/utilities/FastAPI code
    - `doc_generators.py` — design docs, tasks
    - `config_generators.py` — pyproject, gitignore, dependency files, README
    - `workflow_composer.py` — `PocketFlowGenerator` orchestration

Notes
- `pocketflow-tools/` (hyphen) remains a tools folder; `pocketflow_tools/` (underscore) is the importable package.
- Mirror current defensive import patterns where needed to avoid path brittleness.

## Phases

### Phase 0 — Baseline & Snapshots

- Run tests and record outputs for comparison.
  - `./scripts/run-all-tests.sh > baseline_test_results.txt`
  - `python pocketflow-tools/test-generator.py > baseline_generator_output.txt`
  - `python pocketflow-tools/test_full_generation_with_dependencies.py > baseline_full_generation.txt`
- Snapshot generated files by spec into `baseline_out/` and hash them for deterministic diffing.
  - Normalize whitespace and newlines during comparison.
- Gate: If baseline tests fail, pause and fix before proceeding.

### Phase 1 — Package Skeleton & Module Split

- Create `pocketflow_tools/` with the layout above.
- Move `WorkflowSpec` to `pocketflow_tools/spec.py` (no behavior changes).
- Implement `pocketflow_tools/cli.py` that replicates current flags/messages/exit codes of `main()`.
- Extract modules:
  - `template_engine.py`: `_load_templates`, enhanced extensions parsing; keep current path fallbacks for `instructions/extensions`.
  - `code_generators.py`: `_generate_pydantic_models`, `_generate_nodes`, `_generate_flow`, `_generate_utility`, `_generate_fastapi_main`, `_generate_fastapi_router`.
  - `doc_generators.py`, `config_generators.py`: low‑risk generators.
  - `workflow_composer.py`: orchestration that delegates to the above modules.
- Keep method names/signatures intact; if shared state is needed, pass a small `GenerationContext` object internally (no external API change).

#### TODOs — Phase 1 Cutover

- Code extraction (remaining):
  - Implement `code_generators.generate_pydantic_models` and override legacy `_generate_pydantic_models`. (Implemented)
  - Implement `code_generators.generate_nodes` and override legacy `_generate_nodes` (preserve enhanced TODO/orchestrator guidance behavior and extension fallbacks). (Implemented)
  - Implement `code_generators.generate_flow` and override legacy `_generate_flow`. (Implemented)
  - Add `doc_generators.py` with:
    - `generate_design_doc` (port `_generate_design_doc`, `_generate_basic_mermaid`, `_format_customizations_for_doc`). (Implemented)
    - `generate_tasks` (port `_generate_tasks`). (Implemented)
  - Confirm current overrides are active: utilities, FastAPI (`main.py`, `router.py`), and config/deps (`pyproject`, requirements, `.gitignore`, README). (Implemented)
  - Additional generators for parity: tests (`tests/test_*.py`), `__init__.py` variants, `check-install.py`. (Implemented)

- Composer wiring:
  - Introduce `GenerationContext` to pass shared data (templates, extensions, flags) between modules. (Implemented)
  - In `workflow_composer`, route generation through new modules first; use legacy adapter only for not‑yet‑migrated parts. (Implemented via adapter overrides)
  - Once all generators are migrated, update composer to construct the full `output_files` dict without the adapter (adapter remains available until Phase 4 removal). (Pending)

- Parity checkpoints (Phase 1 local smoke checks):
  - Use `python -m pocketflow_tools.cli --spec <spec> --output <dir>` (or `scripts/validation/validate-cli-smoke.sh`) to smoke‑generate a workflow and verify:
    - File set includes: `docs/design.md`, `schemas/models.py`, `nodes.py`, `flow.py`, `main.py`, `router.py`, `utils/*.py`, tests, `pyproject.toml`, requirements, `.gitignore`, `README.md`.
    - Messages and exit codes match legacy CLI for invalid/missing YAML and success.
  - Do not run full baseline diffs yet (that’s Phase 3), but spot‑check a couple outputs for obvious drift (imports, headings, TODOs).

- Documentation alignment:
  - Decision: keep README generation in `config_generators.py` for Phase 1 (parity with dependency config); Package Layout updated to reflect this.
  - Ensure extension path fallback behavior is documented in `template_engine.py` notes. (Documented in module docstring)

- Exit criteria for Phase 1:
  - New modules provide all generation functions; composer can generate a complete workflow using only new modules. (Met via overrides; direct composition without adapter is deferred to Phase 2/3)
  - CLI parity preserved (`python -m pocketflow_tools.cli ...`).
  - Legacy adapter still present but only as a safety net (to be removed in later phases).

### Phase 2 — Repo‑Wide Updates

- Update imports (internal only):
  - Before: `from generator import PocketFlowGenerator, WorkflowSpec`
  - After: `from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator` and `from pocketflow_tools.spec import WorkflowSpec`
- Update CLI invocations:
  - Before: `python pocketflow-tools/generator.py --spec ... --output ...`
  - After: `python -m pocketflow_tools.cli --spec ... --output ...`
- Update scripts that check for the existence of `pocketflow-tools/generator.py` to instead detect the package or CLI.
  - `scripts/lib/repo-detect.sh`
  - `scripts/validation/validate-*.sh`
- Update docs and configs referencing the old path:
  - `README.md`, `CONTRIBUTING.md`, `docs/IMPLEMENTATION_PLAN.md`, extension docs, `config.yml`.

### Phase 2 — Implementation Status & Next Steps

#### ✅ Completed
- **Phase 1**: Full modular package structure implemented (`pocketflow_tools/`)
- **Internal imports updated**: Test files and scripts now use `from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator` and `from pocketflow_tools.spec import WorkflowSpec` (commit: 788c5de)
- **CLI functional**: `python -m pocketflow_tools.cli` working with identical behavior to legacy version

#### 🔄 Phase 2 Remaining Tasks

**Task 1: Update CLI Invocations in Scripts**
- **Status**: 12+ files found with `python pocketflow-tools/generator.py` references
- **Target files**:
  - `scripts/validation/validate-end-to-end.sh`
  - `scripts/validation/validate-orchestration.sh`
  - `scripts/validation/validate-integration.sh`
  - `scripts/validation/validate-user-experience.sh`
  - `setup/base.sh`
  - Other validation and setup scripts
- **Change**: Replace `python pocketflow-tools/generator.py --spec ... --output ...` with `python -m pocketflow_tools.cli --spec ... --output ...`
- **Verification**: Each script must pass its validation checks

**Task 2: Update Documentation References**
- **Target files**:
  - `README.md` - CLI usage examples and installation instructions
  - `AGENTS.md` - agent configuration examples  
  - Other documentation with generator references
- **Change**: Update command examples and references to use new CLI
- **Verification**: Documentation examples must be accurate and testable

**Task 3: Update Repository Detection Logic**
- **Target files**:
  - `scripts/lib/repo-detect.sh`
  - Any scripts that check for `pocketflow-tools/generator.py` existence
- **Change**: Detect `pocketflow_tools/` package or `python -m pocketflow_tools.cli` availability instead
- **Verification**: Repo-type detection must work correctly for framework vs usage distinction

**Task 4: Update Configuration Files**
- **Target files**:
  - `config.yml`
  - Any other configs referencing the old generator path
- **Change**: Update path references to use new CLI or package structure
- **Verification**: All configs must load and function correctly

#### Phase 2 Systematic Approach

1. **CLI Script Updates**:
   ```bash
   # Find all references
   grep -r "python pocketflow-tools/generator.py" . --include="*.sh" --include="*.yml" --include="*.md"
   
   # Update each file systematically
   # Test each script after update
   ```

2. **Documentation Updates**:
   ```bash
   # Update README examples
   # Update AGENTS.md examples
   # Verify all examples work
   ```

3. **Verification Protocol**:
   ```bash
   # After each category of changes:
   ./scripts/run-all-tests.sh
   python -m pocketflow_tools.cli --help
   # Test representative validation scripts
   ```

#### Phase 2 Exit Criteria
- ✅ All scripts use `python -m pocketflow_tools.cli` instead of old generator path
- ✅ All documentation examples updated and verified functional
- ✅ Repository detection logic works correctly  
- ✅ No remaining references to `pocketflow-tools/generator.py` except in rollback plans
- ✅ All validation scripts pass with new invocations
- ✅ CLI behavior identical to legacy version (flags, messages, exit codes)

**Ready for Phase 3**: When all Phase 2 tasks completed and exit criteria met.

### Phase 3 — Validation

- Unit and integration tests:
  - `./scripts/run-all-tests.sh`
  - `python -m pocketflow_tools.cli --spec <spec> --output <dir>` smoke tests (help/invalid YAML/valid run).
- Template integrity checks:
  - Assert TODO placeholders exist in `nodes.py`, `flow.py`, `router.py`.
  - Assert no unintended vendor SDK imports appear in generated code.
  - Assert generated file set and relative paths unchanged: `schemas/models.py`, `nodes.py`, `flow.py`, `main.py`, `router.py`.
- Determinism:
  - Provide `POCKETFLOW_TEST_MODE=1` to disable any non‑deterministic behaviors if present.
  - Normalize diffs (whitespace/newlines) and compare hashes against `baseline_out/`.

### Phase 4 — Removal & Cleanup

- Delete `pocketflow-tools/generator.py` and any references to it.
- Update `config.yml` and any scripts that referenced the old path.
- Run code quality tools on the new package (do not change messages/output semantics in ways that break tests).
  - `uv run ruff check pocketflow_tools/`
  - `uv run ruff check --fix pocketflow_tools/`
  - `uv run mypy pocketflow_tools/` (if configured)

## Risks & Mitigations

- Import path changes: Mitigate with a single, clear new entrypoint and comprehensive search‑and‑replace across repo.
- Hyphen vs underscore: Keep tools under `pocketflow-tools/`, imports under `pocketflow_tools/`.
- Path resolution for extensions: Preserve current fallback logic in `template_engine.py`.
- Output drift: Use baseline snapshots, normalized diffs, and file set assertions as hard gates.

## Rollback Strategy

- Keep a branch/tag: `pre-cutover` for immediate rollback.
- If partial rollback needed, restore the monolithic file and update scripts back to previous invocations.

## Acceptance Criteria

- Tests and validation scripts pass as before.
- Generated outputs are identical to baseline (content and file set).
- CLI parity confirmed for flags, messages, and exit codes.
- No references remain to `pocketflow-tools/generator.py`.

## Checklists

- Imports updated across tests and scripts.
- CLI invocations updated in scripts and docs.
- Template integrity checks in place (TODOs preserved).
- Baseline vs current outputs matched.
- Old file deleted; configs updated.

## Notes

- This clean cutover is internal to the framework repo (not public release dependent). We optimize for clarity and maintainability while honoring the framework’s “starter templates with TODOs” philosophy.
