# Context Rot Remediation Plan

Purpose: Eliminate duplicate concepts, unify canonical components, and reduce drift across the PocketFlow framework without changing the framework vs usage contract.

Scope: Framework repo only. Generated template placeholders remain intentional (no business logic implementations in templates).

## Objectives
- Single source of truth for shared data models and pattern definitions
- One canonical validation pathway with consistent rules
- Remove/clarify duplicate tests and utilities
- Fix identified defects and reduce confusion-prone naming

## Workstreams

### 1) Consolidate Data Models (Canonicalize types)
- [x] Replace `generator.PatternRecommendation` with `pattern_analyzer.PatternRecommendation` (enum-based)
  - Update `PocketFlowGenerator.request_pattern_analysis` to return analyzer types directly.
  - If a shape change is needed for generator output, add a small adapter function (do not re-declare a same-named class).
- [x] Replace `generator.DependencyConfig` with `dependency_orchestrator.DependencyConfig`
  - Update generator fallback `_generate_basic_dependency_config` to either import the canonical type or use a clearly named `BasicDependencyConfig` (no name collision).
- [x] Remove `generator.ValidationResult` in favor of `template_validator.ValidationResult`
  - Update `coordinate_template_validation` to return the validator object (or a minimal dict), not a same-named class.

Files to touch:
- `pocketflow-tools/generator.py`
- `pocketflow-tools/pattern_analyzer.py` (only imports/typing if needed)
- `pocketflow-tools/dependency_orchestrator.py` (no change expected)
- Affected tests under `pocketflow-tools/`

Acceptance:
- No duplicate class names across modules for the three types
- All generator paths compile and tests pass

---

### 2) Centralize Pattern Definitions
- [x] Create `pocketflow-tools/pattern_definitions.py` as the single source of truth for pattern node templates (names, descriptions, node types).
- [x] Make `generator._generate_nodes_from_pattern` import from the shared module.
- [x] Make `workflow_graph_generator._load_pattern_flows` import from the same source (convert to graph structures without re-encoding nodes).

Files to touch:
- `pocketflow-tools/pattern_definitions.py` (new)
- `pocketflow-tools/generator.py`
- `pocketflow-tools/workflow_graph_generator.py`
- Affected tests under `pocketflow-tools/`

Acceptance:
- Generated nodes and Mermaid diagrams stay in sync for all patterns
- No hardcoded duplicate node lists remain in the two modules

---

### 3) Canonical Validator Adoption
- [x] Treat `pocketflow-tools/template_validator.py` as source of truth.
- [x] Update `scripts/validation/validate-generation.py` to delegate design/nodes/flow checks to the Python validator for consistency (keep script as a CLI wrapper and for type/ruff calls).
- [x] Simplify `scripts/validation/validate-template-structure.sh` by shelling out to the Python validator instead of embedding AST logic; retain basic structural checks only.
- [x] Align required design sections with the module’s rules (prefer module flexibility: “## Requirements”, “## Flow Design”, and either “## Node Design” or “## Node Specifications”).

Files to touch:
- `scripts/validation/validate-generation.py`
- `scripts/validation/validate-template-structure.sh`
- (No change) `pocketflow-tools/template_validator.py` unless we choose to expand sections there instead

Acceptance:
- Running any of the validation entry points yields consistent results on the same template
- Reduced duplicate logic; one place to change rules

---

### 4) Fix StatusReporter defect
- [x] `complete_operation()` returns a defined value (loads persisted status).
  - Also improved: avoid reinit on read; compute summary from persisted state; correct elapsed calculation; improved CLI `complete` parsing.

Files to touch:
- `pocketflow-tools/status_reporter.py`

Acceptance:
- No NameError on return; basic call path works under a tiny smoke test

---

### 5) Test Suite Rationalization
- [x] Keep `test_dependency_orchestrator.py` as the comprehensive suite; mark `test_dependency_orchestrator_simple.py` as “smoke” or remove if redundant.
- [x] De-duplicate generator tests: maintain a fast smoke test (`test-generator.py`) and a comprehensive end-to-end (`test_full_generation_with_dependencies.py`). Remove or merge `test-full-generation.py` if redundant.
- [x] Ensure CI only runs one “comprehensive” suite per area, plus a smoke pass.

Files to touch:
- `pocketflow-tools/test_dependency_orchestrator.py`
- `pocketflow-tools/test_dependency_orchestrator_simple.py`
- `pocketflow-tools/test-generator.py`
- `pocketflow-tools/test_full_generation_with_dependencies.py`
- CI/test runner scripts if present

Acceptance:
- Test runtime reduced; overlapping tests consolidated; coverage of critical paths preserved

---

### 6) Unify Pattern Analysis Entrypoint
- [ ] Prefer `agent_coordination.coordinate_pattern_analysis` as the high-level pathway from UX flows.
- [ ] Deprecate `PocketFlowGenerator.request_pattern_analysis` or make it a thin wrapper that returns the canonical analyzer type; avoid defining duplicate dataclasses.

Files to touch:
- `pocketflow-tools/generator.py`
- `pocketflow-tools/agent_coordination.py`

Acceptance:
- Single canonical recommendation type propagates across generation and coordination

---

### 7) Naming/Docs to Reduce Confusion
- [ ] Add short module docstrings clarifying roles:
  - `ContextManager` (extracts project context from docs) vs `CoordinationContext` (runtime coordination state).
- [ ] Add a brief note in `docs/FRAMEWORK_VS_USAGE.md` referencing the canonical validator and model ownership.

Files to touch:
- `pocketflow-tools/context_manager.py` (doc comment only)
- `pocketflow-tools/agent_coordination.py` (doc comment only)
- `docs/FRAMEWORK_VS_USAGE.md`

Acceptance:
- Clear ownership and purpose for similarly named concepts

---

## Tracking Checklist

- [x] 1. Data models consolidated (no duplicate class names across modules)
- [x] 2. Pattern definitions centralized and imported by generator + graph generator
- [x] 3. Validators aligned (scripts call module; unified section rules)
- [x] 4. StatusReporter return fixed and smoke-tested
- [x] 5. Tests rationalized (smoke vs comprehensive), CI updated
- [ ] 6. Single pattern analysis entrypoint adopted
- [ ] 7. Docstring and documentation updates

## Verification
- Run: `scripts/run-all-tests.sh`
- Run validator wrapper: `python scripts/validation/validate-generation.py --all` (after it delegates to module)
- Run end-to-end: `python pocketflow-tools/run_end_to_end_tests.py`

## Risks & Mitigations
- Type/enum vs string mismatches after consolidation → add small adapters at module boundaries; do not re-declare types.
- Pattern template centralization causing small diagram/layout changes → update tests to assert by structure, not string equality where possible.
- Script invocations in different environments → prefer module calls with clear error messages; keep minimal shell fallbacks.
