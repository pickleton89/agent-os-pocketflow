# PocketFlow Tools Documentation Index

Date: 2025-09-08

This is the starting point for using the PocketFlow tools, agents, and instructions together. It provides a unified call graph, quickstart, and links to all component docs and the comprehensive integration plan.

## Start Here

- Integration plan: see `pocketflow-integration-plan.md` (how everything fits together, with Invocation Matrix and step-by-step flow).
- Overview of tools: `pocketflow-tools-analysis.md` (what each non-test file does).

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

## Quickstart (Happy Path)

1) Pre‑flight
```bash
python3 ~/.agent-os/pocketflow-tools/check-pocketflow-install.py --install
```

2) Extract context + spec
```bash
python3 pocketflow-tools/context_manager.py \
  --project-root . \
  --workflow-name "MyFeature" \
  --output context_analysis.json \
  --spec workflow.yaml
```

3) Analyze patterns (programmatic handoff)
```python
from pocketflow-tools.agent_coordination import coordinate_pattern_analysis, create_subagent_handoff
ctx = coordinate_pattern_analysis("MyProject", open("requirements.txt").read())
handoff = create_subagent_handoff(ctx)
print(handoff.target_agent, ctx.pattern_recommendation.primary_pattern)
```

4) Orchestrate dependencies
```bash
python3 pocketflow-tools/dependency_orchestrator.py --pattern RAG --project-name my-app --output-pyproject > pyproject.toml
```

5) Generate workflow (installable CLI)
```bash
uv run python -m pocketflow_tools.cli --spec workflow.yaml --output .agent-os/workflows
```

6) Validate and feed back
```bash
python3 pocketflow-tools/template_validator.py .agent-os/workflows/MyFeature | tee validation.txt
python3 pocketflow-tools/validation_feedback.py validation.txt --context context_analysis.json --markdown feedback.md
```

## Component Docs

- Agent coordination: `agent_coordination_doc.md`
- Context extraction: `context_manager_doc.md`
- Pattern analysis: `pattern_analyzer_doc.md`
- Pattern definitions: `pattern_definitions_doc.md`
- Dependency orchestration: `dependency_orchestrator_doc.md`
- Workflow graph + Mermaid: `workflow_graph_generator_doc.md`
- Template validation: `template_validator_doc.md`
- Validation feedback: `validation_feedback_doc.md`
- Status reporting: `status_reporter_doc.md`
- Install check: `check-pocketflow-install_doc.md`
- Antipattern demo: `antipattern_demo_doc.md`
- Test generator: `test-generator_doc.md`

## Agents and Instructions (for cross-reference)

- Agents (sub‑agents invoked by flows):
  - `../claude-code/agents/pattern-analyzer.md`
  - `../claude-code/agents/dependency-orchestrator.md`
  - `../claude-code/agents/file-creator.md`
  - `../claude-code/agents/template-validator.md`
  - `../claude-code/agents/strategic-planner.md`
  - `../claude-code/agents/context-fetcher.md`

- Instructions (end‑user playbooks):
  - `../instructions/core/create-spec.md`
  - `../instructions/core/execute-task.md`
  - `../instructions/orchestration/dependency-validation.md`
  - `../instructions/orchestration/template-standards.md`
  - `../instructions/extensions/pocketflow-integration.md`
  - `../instructions/meta/pre-flight.md`

## Framework vs Usage

- Framework (this repo) houses both developer tools (`pocketflow-tools/`) and the installable package (`pocketflow_tools/`).
- End‑users primarily invoke the CLI in `pocketflow_tools/` and rely on agents/instructions that call into `pocketflow-tools/` capabilities as shown above.

## Next Steps

- Read `pocketflow-integration-plan.md` for the Invocation Matrix and detailed mapping.
- Paste the ready‑made snippets from the plan into the corresponding agent and instruction files as needed.
- Use the Quickstart to validate your environment on a sample feature.

