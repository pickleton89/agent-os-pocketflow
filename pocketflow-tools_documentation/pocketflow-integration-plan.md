# PocketFlow Tools → Agents/Instructions Integration Plan

Date: 2025-09-08

- Batch ID: a711c364-a5da-4c24-8b7b-fdee9dfb401d
- Models used in parallel (read-only planning): [Claude, Gemini, Code]

This document unifies how the documentation under `pocketflow-tools_documentation/` drives correct invocation of the Python tools in `pocketflow-tools/` by sub‑agents in `claude-code/agents/` and by instruction files in `instructions/**` within an end‑user project.

## Executive Summary

- The framework offers robust analysis, orchestration, generation, and validation tools, but activation paths in end‑user flows are inconsistent.
- Add a single canonical call graph, an Invocation Matrix, and copy/paste‑ready snippets for agents and instructions.
- Close the loop with validation → feedback → (optional) override → re‑run.
- Clarify Framework vs Usage: `pocketflow_tools/` (installable package + CLI) vs. `pocketflow-tools/` (developer tools used by agents/instructions).

## Repository Map (Concise)

- `claude-code/agents/`: sub‑agent behaviors (context‑fetcher, pattern‑analyzer, file‑creator, template‑validator, dependency‑orchestrator, etc.).
- `instructions/{core,extensions,meta,orchestration}`: end‑user runnable playbooks and hooks.
- `pocketflow-tools/`: developer tools for analysis/orchestration/validation (Python scripts).
- `pocketflow_tools/`: installable package; CLI entry (`pocketflow_tools/cli.py`) that generates workflows from a YAML spec.
- `pocketflow-tools_documentation/`: component docs (e.g., `pattern_analyzer_doc.md`) + overview (`pocketflow-tools-analysis.md`).

### Directory Structure (Excerpt)

```text
claude-code/
  agents/
    context-fetcher.md
    dependency-orchestrator.md
    pattern-analyzer.md
    file-creator.md
    template-validator.md
    strategic-planner.md
instructions/
  core/ (...plan-product.md, create-spec.md, execute-task(s).md...)
  extensions/ (pocketflow-integration.md, ...)
  meta/ (pre-flight.md, post-flight-rules.md)
  orchestration/ (coordination.yaml, dependency-validation.md, template-standards.md)
pocketflow-tools/
  agent_coordination.py
  context_manager.py
  dependency_orchestrator.py
  pattern_analyzer.py
  pattern_definitions.py
  template_validator.py
  status_reporter.py
  validation_feedback.py
  workflow_graph_generator.py
pocketflow_tools/
  cli.py
  generators/{workflow_composer.py, ...}
pocketflow-tools_documentation/
  pocketflow-tools-analysis.md
  *_doc.md (per-component)
```

## Unified Call Graph

```mermaid
flowchart TD
  A[Pre‑Flight: check-pocketflow-install.py] -->|deps ok| B[Context: context_manager.py]
  B -->|context_analysis.json + spec.yaml| C[Patterns: pattern_analyzer via AgentCoordinator]
  C -->|PatternRecommendation + Handoff| D[Deps: dependency_orchestrator.py]
  D -->|pyproject.toml + uv.toml| E[Generate: pocketflow_tools/cli.py]
  E -->|.agent-os/workflows/<name>/| F[Validate: template_validator.py]
  F -->|report (text/json)| G[Feedback: validation_feedback.py]
  G -->|actions| H{Satisfactory?}
  H -- No --> I[Overrides: AgentCoordinator.handle_pattern_override_request] --> C
  H -- Yes --> J[Design Doc: design-document-creator]
  C -.-> K[Diagram: workflow_graph_generator.py] -.-> J
  E -. progress/status .- L[Status: status_reporter.py]
```

## Invocation Matrix (Summary)

| Tool (pocketflow-tools) | Primary Callers | Typical Trigger | Inputs | Outputs | Invocation | Failure Handling |
|---|---|---|---|---|---|---|
| agent_coordination.py | Agents: pattern-analyzer → design-document-creator / strategic-planner / file-creator / template-validator | After pattern analysis; before each specialized step | project_name, requirements, user_overrides | HandoffPackage, updated CoordinationContext | Programmatic import | Default route to file-creator if no recommendation; ignore invalid override with warning |
| context_manager.py | Agent: context-fetcher; Instruction: core/create-spec.md | Before planning/generation | `--project-root`, `--workflow-name`, `--output`, `--spec` | context_analysis.json, optional spec YAML | CLI | Missing docs → minimal context + warnings |
| pattern_analyzer.py | Agent: pattern-analyzer | Planning/spec stage | requirements text | PatternRecommendation (pattern(s), confidence, rationale) | Programmatic (preferred); add thin CLI | Low confidence → allow override via AgentCoordinator |
| dependency_orchestrator.py | Agent: dependency-orchestrator; Instruction: orchestration/dependency-validation.md | After recommendation, before generation | pattern, project_name | pyproject.toml, uv.toml/.python-version (content) | CLI or import | Validate and report conflicts; non-destructive (caller writes files) |
| workflow_graph_generator.py | Agents: design-document-creator, pattern-analyzer | During design doc creation | PatternType, complexity | Mermaid, graph object | Import | Safe defaults to WORKFLOW |
| template_validator.py | Agent: template-validator; Instruction: orchestration/template-standards.md | After generation, before commit | template dir path | Printed report + exit code; ValidationResult | CLI | Categorized errors/warnings; guides next action |
| validation_feedback.py | Agents: template-validator (post), project-manager | After validation | validator output; optional `--context` | feedback.json, feedback.md | CLI | Tolerant of partial/unknown inputs |
| status_reporter.py | Agents: project-manager, file-creator | Around long steps | workflow_name, operation, action | status JSON + logs in /tmp | CLI | No-fail logging |
| check-pocketflow-install.py | Agent: project-manager; Instruction: meta/pre-flight.md | First-run setup | `--install` optional | printed status / exit code | CLI | Graceful hints for non-PocketFlow dirs |

## End‑to‑End Lifecycle (Happy Path)

1) Pre‑flight
```bash
python3 ~/.agent-os/pocketflow-tools/check-pocketflow-install.py --install
```

2) Extract context and spec
```bash
python3 pocketflow-tools/context_manager.py \
  --project-root . \
  --workflow-name "MyFeature" \
  --output context_analysis.json \
  --spec workflow.yaml
```

3) Analyze patterns and create handoff
```python
from pocketflow-tools.agent_coordination import (
    coordinate_pattern_analysis, create_subagent_handoff
)

ctx = coordinate_pattern_analysis("MyProject", open("requirements.txt").read())
handoff = create_subagent_handoff(ctx)  # routes to design/strategy/file-creator
print(handoff.target_agent, ctx.pattern_recommendation.primary_pattern)
```

4) Orchestrate dependencies
```bash
python3 pocketflow-tools/dependency_orchestrator.py \
  --pattern RAG \
  --project-name my-app \
  --output-pyproject > pyproject.toml
```

5) Generate workflow (installable CLI)
```bash
uv run python -m pocketflow_tools.cli --spec workflow.yaml --output .agent-os/workflows
```

6) Validate templates
```bash
python3 pocketflow-tools/template_validator.py .agent-os/workflows/MyFeature | tee validation.txt
```

7) Feedback and iteration
```bash
python3 pocketflow-tools/validation_feedback.py validation.txt \
  --context context_analysis.json \
  --markdown feedback.md
```
If needed, apply an override and loop:
```python
from pocketflow-tools.agent_coordination import AgentCoordinator
coordinator = AgentCoordinator()
ctx = coordinator.handle_pattern_override_request(ctx, {
  "force_pattern": "WORKFLOW", "complexity_preference": "simple"
})
```

8) Design doc with diagram
```python
from pocketflow_tools.workflow_graph_generator import WorkflowGraphGenerator
from pocketflow_tools.pattern_analyzer import PatternType

gen = WorkflowGraphGenerator()
graph = gen.generate_workflow_graph(PatternType.RAG, complexity_level="medium")
mermaid = gen.generate_mermaid_diagram(graph)
# Embed 'mermaid' in docs/design.md under "## Flow Design"
```

9) Status tracking (optional)
```bash
python3 pocketflow-tools/status_reporter.py "MyFeature" generation init
python3 pocketflow-tools/status_reporter.py "MyFeature" generation step 1 "Analyzing patterns"
```

## Agent & Instruction Snippets (Ready to Paste)

### claude-code/agents/pattern-analyzer.md
```python
from pocketflow-tools.agent_coordination import coordinate_pattern_analysis, create_subagent_handoff

def run_pattern_analysis(project_name: str, requirements: str):
    ctx = coordinate_pattern_analysis(project_name, requirements)
    handoff = create_subagent_handoff(ctx)
    return {
        "pattern": ctx.pattern_recommendation.primary_pattern.value,
        "confidence": ctx.pattern_recommendation.confidence_score,
        "handoff": handoff.payload,
        "target_agent": handoff.target_agent,
    }
```

### claude-code/agents/dependency-orchestrator.md
```python
from pocketflow_tools.dependency_orchestrator import DependencyOrchestrator

def generate_configs(project_name: str, pattern: str):
    orch = DependencyOrchestrator()
    pyproject = orch.generate_pyproject_toml(project_name, pattern)
    uv_files = orch.generate_uv_config(project_name, pattern)
    issues = orch.validate_configuration(pyproject, "pyproject.toml")
    return {"pyproject": pyproject, "uv": uv_files, "issues": issues}
```

### claude-code/agents/template-validator.md
```bash
python3 pocketflow-tools/template_validator.py .agent-os/workflows/$WORKFLOW | tee validation.txt
```

### instructions/orchestration/orchestrator-hooks.md (post-generation)
```bash
python3 pocketflow-tools/template_validator.py ".agent-os/workflows/${feature}" > validation.txt || true
python3 pocketflow-tools/validation_feedback.py validation.txt --context context_analysis.json --markdown feedback.md
```

### instructions/core/create-spec.md (context gathering)
```bash
python3 pocketflow-tools/context_manager.py --project-root . --workflow-name "$FEATURE" --output context_analysis.json --spec workflow.yaml
```

### instructions/orchestration/dependency-validation.md
```bash
python3 pocketflow-tools/dependency_orchestrator.py --pattern "$PATTERN" --project-name "$PROJECT" --output-pyproject > pyproject.toml
```

## Documentation Changes (By File)

- `pocketflow-tools-analysis.md`
  - Add sections: “Invocation Matrix” and “Unified Call Graph” (link to this plan).
  - Add banner clarifying Framework vs Usage contexts.

- `agent_coordination_doc.md`
  - Add “Agent Handoff Protocol” with JSON schema for `HandoffPackage` and response expectations.
  - Add “Override Flow” examples (`force_pattern`, `complexity_preference`).

- `pattern_analyzer_doc.md`
  - Add “Programmatic API” import path and structured return example.
  - Cross‑link to `workflow_graph_generator_doc.md` for diagram embedding.

- `dependency_orchestrator_doc.md`
  - Clarify when to consume orchestrator output vs. minimal generators.
  - Provide `validate_configuration(...)` examples; common warnings/errors table.

- `template_validator_doc.md`
  - Add “Required Sections” for `docs/design.md` and return codes with next actions.

- `validation_feedback_doc.md`
  - Map validator categories → remediation actions; show loop back to overrides.

- `status_reporter_doc.md`
  - Minimal integration snippets and recommended event names.

- New `pocketflow-tools_documentation/index.md`
  - Landing page with the call graph and Invocation Matrix; links to all components.

## Errors & Edge Cases (Playbook)

- Missing `pyproject.toml` before generation → use orchestrator to emit content; write file; re‑validate.
- Invalid spec YAML → `pocketflow_tools/cli.py` surfaces error; route to design‑document‑creator to fix spec; re‑run.
- Pattern mismatch/low confidence → apply overrides via AgentCoordinator; regenerate deps/templates.
- Missing/invalid design sections → template_validator emits errors; design‑document‑creator fills sections and embeds Mermaid.
- Import/dependency failures → classify as dependency issues; rerun orchestrator; surface `uv add`/install guidance.
- CI/network limits → prefer guidance over auto‑install; status_reporter records partial success + warnings.

## Acceptance Criteria

- Documentation
  - Each component doc shows activation (CLI + import), inputs/outputs, return codes, error remediation, and cross‑links to at least one agent + one instruction.
  - Overview includes Invocation Matrix and Call Graph.

- End‑to‑End Flow (example repo)
  - Pre‑flight passes or provides actionable guidance.
  - `context_analysis.json` and `workflow.yaml` created.
  - Pattern analysis returns a recommendation and handoff target.
  - Orchestrator outputs valid `pyproject.toml`/`uv.toml` (validation clean).
  - CLI generation produces files under `.agent-os/workflows/<name>/`.
  - Validator emits categorized report; feedback produces JSON + Markdown.
  - Optional: design doc includes Mermaid diagram.

- Tests
  - Unit: CLI arg parsing happy paths; validator/orchestrator minimal cases; feedback parsing.
  - Integration: temp project → context → spec → deps → generate → validate → feedback; assert artifacts.
  - Smoke script: runs the full sequence locally and passes.

## Rollout Plan

- V1 (1–2 days): Invocation Matrix + call graph; add snippets to component docs; update key instructions for happy path.
- V2 (3–5 days): Formalize AgentCoordinator contracts and override protocol; cross‑link agents ↔ tools ↔ instructions; add “Edge Cases & Recovery”.
- V3 (1–2 weeks): Example end‑user repo + smoke script; advanced/hybrid patterns guide; expanded troubleshooting matrices.

## Optional Enhancements

- Thin CLI wrappers where missing (e.g., `pattern_analyzer.py`, `agent_coordination.py`) for reproducible instruction examples.
- “Orchestrator Bridge” module (thin facade) to encapsulate the sequence for agents; keeps instruction scripts simple.
- Standardize `uv run` in all examples.

## Appendix: Constraints Placeholder

Integrate previously provided policies/constraints here (reference: “Pasted Content 1246 chars”) once available, and thread them through the Invocation Matrix and error playbook.

