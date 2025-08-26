# Sub-Agent Invocation Implementation Plan

## Overview
The Enhanced Agent OS + PocketFlow fork removed the sub-agent invocation syntax from the original buildermethods/agent-os. This plan details how to restore sub-agent invocation so they appear visually in Claude Code like shown in Jake's demo video.

## Problem Statement
- Current state: Sub-agents are installed but not being invoked
- Desired state: Sub-agents appear with color-coded output when commands run
- Root cause: Missing invocation syntax in command templates

## Sub-Agent Invocation Patterns from buildermethods/agent-os

### Pattern 1: Step-Level Delegation
```xml
<step number="X" subagent="agent-name" name="step_name">
  <instructions>
    ACTION: Use agent-name subagent
    REQUEST: "Specific request details"
    WAIT: For subagent completion
    PROCESS: Returned information
  </instructions>
</step>
```

### Pattern 2: Inline Invocation
```
USE: @agent:agent-name
REQUEST: "Find [ITEM_NAME] from file"
```

## Implementation Checklist

### Phase 1: Update Framework Command Templates

#### [ ] Update `/instructions/core/plan-product.md`
- [ ] Step 1: Add `subagent="context-fetcher"` for gathering user input
- [ ] Step 2: Add `subagent="file-creator"` for creating documentation structure  
- [ ] Step 3: Add `subagent="file-creator"` for mission.md creation
- [ ] Step 4: Add `subagent="file-creator"` for tech-stack.md creation
- [ ] Step 5: Add `subagent="file-creator"` for mission-lite.md creation
- [ ] Step 6: Add `subagent="file-creator"` for roadmap.md creation

#### [ ] Update `/instructions/core/execute-tasks.md`
- [ ] Step 2: Add `subagent="context-fetcher"` for context analysis
- [ ] Step 3: Add `subagent="git-workflow"` for branch management
- [ ] After each task: Add `subagent="test-runner"` for test verification
- [ ] Final step: Add `subagent="project-manager"` for recap creation

#### [ ] Update `/instructions/core/execute-task.md`
- [ ] Step 3: Add `subagent="context-fetcher"` for best practices review
- [ ] Step 4: Add `subagent="context-fetcher"` for code style review
- [ ] Step 6: Add `subagent="test-runner"` for task test verification

#### [ ] Update `/instructions/core/create-spec.md`
- [ ] Step 1: Add `subagent="context-fetcher"` for requirement gathering
- [ ] Step 2: Add `subagent="file-creator"` for spec structure creation
- [ ] Steps 3-6: Add `subagent="file-creator"` for each spec file

#### [ ] Update `/instructions/core/analyze-product.md`
- [ ] Add `subagent="context-fetcher"` for existing project analysis
- [ ] Add `subagent="file-creator"` for documentation updates

### Phase 2: Verify Sub-Agent Files

#### [ ] Check all files in `/claude-code/agents/` have proper YAML frontmatter:
- [ ] context-fetcher.md
- [ ] date-checker.md
- [ ] dependency-orchestrator.md
- [ ] file-creator.md
- [ ] git-workflow.md
- [ ] pattern-recognizer.md
- [ ] pocketflow-orchestrator.md
- [ ] project-manager.md
- [ ] template-validator.md
- [ ] test-runner.md

Required frontmatter format:
```yaml
---
name: agent-name
description: When this agent should be invoked
tools: Tool1, Tool2, Tool3  # Optional - inherits all if omitted
---
```

### Phase 3: Update Setup Scripts

#### [ ] Verify `/setup/base.sh`
- [ ] Downloads correct instruction files with sub-agent syntax
- [ ] Copies agent files to base installation

#### [ ] Verify `/setup/project.sh`
- [ ] Copies updated instruction files to project
- [ ] Copies agent files to `.claude/agents/`
- [ ] Maintains proper file structure

### Phase 4: Testing

#### [ ] Framework Repository Testing
- [ ] Run validation scripts to ensure templates are valid
- [ ] Check that sub-agent syntax doesn't break template generation

#### [ ] TestingProject Integration Testing
- [ ] Re-run project installation: `~/.agent-os/setup/project.sh --claude-code`
- [ ] Start Claude Code in TestingProject
- [ ] Test `/plan-product` command
  - [ ] Verify context-fetcher appears
  - [ ] Verify file-creator appears
  - [ ] Verify color-coded output
- [ ] Test `/create-spec` command
  - [ ] Verify context-fetcher appears
  - [ ] Verify file-creator appears
- [ ] Test `/execute-tasks` command
  - [ ] Verify git-workflow appears
  - [ ] Verify test-runner appears
  - [ ] Verify project-manager appears

### Phase 5: Documentation

#### [ ] Update README.md
- [ ] Document sub-agent feature
- [ ] Add troubleshooting section for sub-agents

#### [ ] Update CHANGELOG.md
- [ ] Document sub-agent invocation restoration
- [ ] Note compatibility with Claude Code visual features

## Success Criteria

1. **Visual Confirmation**: Sub-agents appear with color-coded names in Claude Code UI
2. **Functional Verification**: Commands properly delegate to sub-agents
3. **Framework Integrity**: Changes only affect template generation, not runtime
4. **User Experience**: Matches demo video behavior

## Notes

### Framework vs Usage Principle
- We're updating templates that get installed in end-user projects
- Not implementing application logic
- Missing implementations in generated templates remain intentional

### Compatibility
- Must work with Claude Code's latest sub-agent system (July 2025)
- Should maintain compatibility with cursor where possible
- Enhanced PocketFlow features should not interfere

## References
- Demo Video: https://www.youtube.com/watch?v=4PlVnrliN3Q
- Original Repo: https://github.com/buildermethods/agent-os
- Enhanced Fork: https://github.com/pickleton89/agent-os-pocketflow

## Status
- Created: 2025-08-26
- Status: Planning Phase
- Last Updated: 2025-08-26