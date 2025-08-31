# Pocketflow-Orchestrator Refactoring Update Plan

## Overview
The `pocketflow-orchestrator` has been split into three focused sub-agents. This plan outlines updates needed across the framework repository to reflect this architectural change.

## New Sub-Agent Structure
Based on the refactoring commit, the three new sub-agents are:
- `design-document-creator` → PocketFlow design document creation specialist
- `strategic-planner` → Product strategy and PocketFlow integration planning  
- `workflow-coordinator` → Template generation and workflow orchestration

## Update Categories

### 1. Documentation Files (Selected Updates Only)
**Target**: `INTEGRATION_GAP.md`

**Updates Needed**:
- Line 15: Update agent file reference from single orchestrator to three agents
- Lines 64, 75, 117: Replace orchestrator references with appropriate sub-agent based on context
  - Design-related gaps → `design-document-creator`
  - Planning/strategy gaps → `strategic-planner`  
  - Workflow/coordination gaps → `workflow-coordinator`

### 2. Code Files (All Updates Required)
**Target**: `pocketflow-tools/agent_coordination.py`, `pocketflow-tools/generator.py`

#### agent_coordination.py Updates:
- **Lines 5, 138**: Update class documentation to reference three sub-agents
- **Lines 145, 147**: Update handoff creation methods for multiple target agents
- **Line 175**: Update target_agent field to use appropriate sub-agent
- **Lines 187, 334**: Update coordination methods for multi-agent handoffs

**Replacement Strategy**:
- Pattern recognition → workflow coordination: Use `workflow-coordinator`
- Strategic decisions: Use `strategic-planner`
- Design validation: Use `design-document-creator`

#### generator.py Updates:
- **Line 352**: Update orchestrator guidance example to use appropriate sub-agent
  - For validation tasks: `workflow-coordinator`
  - Template example: `claude-code agent invoke workflow-coordinator --task validate-node --node [name]`

### 3. Validation Scripts (All Updates Required)
**Targets**: `scripts/validation/validate-integration.sh`, `scripts/validation/validate-orchestration.sh`, `scripts/validation/validate-orchestration.py`, `scripts/validation/validate-end-to-end.sh`

#### validate-integration.sh:
- **Line 18**: Update to check for three agent files instead of one
- Add checks for: `design-document-creator.md`, `strategic-planner.md`, `workflow-coordinator.md`

#### validate-orchestration.sh & validate-orchestration.py:
- **Filename consideration**: May need to be renamed to `validate-workflow-coordination.*`
- Update internal logic to validate workflow coordination specifically
- Remove strategic planning and design document validation (now separate agents)

#### validate-end-to-end.sh:
- **Lines 222, 225**: Update agent configuration tests for three agents
- Test each agent file exists and has proper YAML frontmatter
- Update grep patterns to match new agent names

### 4. Agent Definition Files (All Updates Required)
**Target**: `claude-code/agents/pattern-analyzer.md`

**Updates Needed**:
- Review any references to `pocketflow-orchestrator` in handoff instructions
- Update coordination protocols to work with three target agents
- Specify which sub-agent should be invoked based on pattern type:
  - Design patterns → `design-document-creator`
  - Strategy patterns → `strategic-planner`
  - Workflow patterns → `workflow-coordinator`

## Framework vs Usage Considerations

### Framework Context (This Repository)
- These updates modify the **template generation system** that creates agent configurations for end-user projects
- The validation scripts test the framework's ability to generate proper agent structures
- Agent coordination code supports the framework's pattern recognition and handoff capabilities

### Generated Template Context (End-User Projects)
- End-user projects will receive the new three-agent structure via the updated generator
- Each end-user project will get all three agents to handle their specific needs
- The framework generates starting templates - end-users implement the actual functionality

## Implementation Priority

1. **High Priority**: Validation scripts (functional impact)
2. **High Priority**: Agent coordination code (system integration)
3. **Medium Priority**: Generator templates (affects new project creation)
4. **Medium Priority**: Documentation updates (reference accuracy)

## Validation Strategy

After updates:
1. Run `./scripts/run-all-tests.sh` to ensure framework integrity
2. Test generator with `python pocketflow-tools/test-generator.py`
3. Validate that new agent files are properly created in generated projects
4. Confirm handoff protocols work with multiple target agents
