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

### Phase 1: Update Framework Command Templates ✅ COMPLETED

#### [x] Update `/instructions/core/plan-product.md`
- [x] Step 1: Add `subagent="context-fetcher"` for gathering user input
- [x] Step 1a: Add `subagent="pocketflow-orchestrator"` for LLM/AI project planning (conditional)
- [x] Step 2: Add `subagent="file-creator"` for creating documentation structure  
- [x] Step 3: Add `subagent="file-creator"` for mission.md creation
- [x] Step 4: Add `subagent="file-creator"` for tech-stack.md creation
- [x] Step 6: Add `subagent="file-creator"` for CLAUDE.md creation (updated from roadmap.md)

#### [x] Update `/instructions/core/execute-tasks.md`
- [x] Step 2: Add `subagent="context-fetcher"` for context analysis
- [x] Step 5: Add `subagent="git-workflow"` for branch management
- [x] Step 6: Add `subagent="test-runner"` for test verification
- [x] Step 7: Add `subagent="project-manager"` for post-execution workflow

#### [x] Update `/instructions/core/execute-task.md`
- [x] Step 3: Add `subagent="context-fetcher"` for best practices review
- [x] Step 4: Add `subagent="context-fetcher"` for code style review
- [x] Step 6: Add `subagent="test-runner"` for task test verification

#### [x] Update `/instructions/core/create-spec.md`
- [x] Step 1: Add `subagent="context-fetcher"` for requirement gathering
- [x] Step 2: Add `subagent="context-fetcher"` for context analysis
- [x] Step 5: Add `subagent="file-creator"` for spec folder creation
- [x] Steps 6-12: Add `subagent="file-creator"` for each spec file creation

#### [x] Update `/instructions/core/analyze-product.md`
- [x] Step 1: Add `subagent="context-fetcher"` for existing project analysis
- [x] Step 4: Add `subagent="file-creator"` for documentation updates

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

**Current Issues Found:**
- **Non-standard YAML fields**: Files contain `auto_invoke_triggers`, `coordination_aware`, `generates_code`, `color` which aren't recognized by Claude Code
- **Inconsistent tools format**: Some use arrays `[Tool1, Tool2]`, others use comma-separated strings
- **Missing PocketFlow invocation**: `pocketflow-orchestrator` should be invoked for LLM/AI projects during planning

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

## Detailed Sub-Agent File Issues

### Files Requiring YAML Header Standardization

#### 1. **pocketflow-orchestrator.md**
**Current Issues:**
- Contains `auto_invoke_triggers`, `coordination_aware`, `generates_code` (non-standard fields)
- Tools format: `[Read, Write, Grep, Glob, Bash, Edit, MultiEdit, TodoWrite, Task]` (array format)

**Required Fix:**
```yaml
---
name: pocketflow-orchestrator
description: MUST BE USED PROACTIVELY for planning, designing, and orchestrating complex Agent OS workflows using PocketFlow's graph-based architecture. Automatically invoked for LLM/AI features and complex planning tasks.
tools: Read, Write, Grep, Glob, Bash, Edit, MultiEdit, TodoWrite, Task
---
```

#### 2. **context-fetcher.md**
**Current Issues:**
- Contains `color: blue` (non-standard field)
- Tools format: `Read, Grep, Glob` (correct format)

#### 3. **dependency-orchestrator.md**
**Current Issues:**
- Likely contains non-standard fields (needs verification)

#### 4. **template-validator.md**
**Current Issues:**
- Likely contains non-standard fields (needs verification)

#### 5. **pattern-recognizer.md** 
**Current Issues:**
- Likely contains non-standard fields (needs verification)

### Required Actions
1. **Audit all 10 sub-agent files** for non-standard YAML fields
2. **Remove non-standard fields**: `auto_invoke_triggers`, `coordination_aware`, `generates_code`, `color`
3. **Standardize tools format**: Use comma-separated strings, not arrays
4. **Preserve functionality**: Move important triggers into descriptions using "MUST BE USED PROACTIVELY"

## Status
- Created: 2025-08-26
- Status: Phase 1 Complete ✅ - Ready for Phase 2 (Sub-Agent YAML Standardization)
- Phase 1 Completed: 2025-08-26
- Last Updated: 2025-08-26

## Phase 1 Completion Summary
✅ **Framework Templates Updated**: All 5 core instruction templates now include proper sub-agent invocation syntax
✅ **Sub-Agent Integration**: context-fetcher, file-creator, git-workflow, test-runner, project-manager, pocketflow-orchestrator
✅ **Pattern Compliance**: Follows buildermethods/agent-os XML syntax with ACTION/REQUEST/WAIT/PROCESS blocks
✅ **Conditional Logic**: pocketflow-orchestrator only invoked for LLM/AI projects
✅ **Changes Committed**: All modifications committed to git (commit: f7b3ed9)

**Next Step**: Proceed to Phase 2 - Standardize sub-agent YAML headers for Claude Code compatibility