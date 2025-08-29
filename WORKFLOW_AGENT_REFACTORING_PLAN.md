# Workflow Agent Refactoring Plan

> **Objective**: Replace the massive workflow-coordinator.md (2400+ lines) with 4 focused, maintainable agents
> 
> **Status**: Planning Phase  
> **Created**: 2025-01-29  
> **Estimated Timeline**: 1-2 days implementation

## Current State Analysis

### Problems with Current Architecture
- **workflow-coordinator.md**: 2400+ lines, unmaintainable
- **Redundancy**: Duplicates functionality of existing agents
- **Monolithic**: 7 different commands in one agent
- **Poor separation of concerns**: Multiple responsibilities mixed

### Existing Agent Redundancies Identified
| Workflow Command | Existing Agent | Overlap Level |
|------------------|----------------|---------------|
| `/analyze-pattern` | `pattern-recognizer.md` | 🔴 **100% REDUNDANT** |
| `/validate-workflow` | `template-validator.md` | 🔴 **100% REDUNDANT** |
| `/generate-pocketflow` | `dependency-orchestrator.md` | 🟡 **PARTIAL OVERLAP** |

## Proposed Solution

### Phase 1: Create 4 Focused Agents

#### 1. `workflow-implementer.md` 
**Purpose**: Main orchestration agent that coordinates existing specialists
- **Primary Command**: `/implement-workflow <name>`
- **Size**: ~400-500 lines
- **Responsibility**: Orchestrate pattern-recognizer → generator → dependency-orchestrator → template-validator
- **Value**: Saves users 2-3 hours of manual coordination

#### 2. `workflow-helper.md`
**Purpose**: Complete user guidance and documentation system
- **Primary Command**: `/help-workflow`  
- **Size**: ~200-300 lines
- **Responsibility**: Provide comprehensive workflow guidance and troubleshooting
- **Value**: Prevents user confusion, provides complete workflow clarity

#### 3. `workflow-status.md`
**Purpose**: Implementation progress tracking and analysis
- **Primary Command**: `/status-workflow <name>`
- **Size**: ~300-400 lines  
- **Responsibility**: Analyze implementation state, track TODO progress, report next steps
- **Value**: Saves 15 minutes per check, eliminates guessing what's left to do

#### 4. `workflow-documenter.md`
**Purpose**: Comprehensive documentation generation for workflows  
- **Primary Command**: `/document-workflow <name>`
- **Size**: ~300-400 lines
- **Responsibility**: Generate README, CODE.md, EXAMPLES.md, and navigation docs
- **Value**: Saves 1-2 hours of documentation writing

### Phase 2: Handle Existing workflow-coordinator.md

#### Migration Strategy
1. **Extract unique logic** from workflow-coordinator.md to new agents
2. **Remove redundant functionality** that duplicates existing agents
3. **Archive original file** for reference during transition
4. **Update references** in documentation and setup scripts

## Implementation Plan

### Pre-Implementation Steps

#### Step 1: Backup and Analysis
```bash
# Backup current state
cp claude-code/agents/workflow-coordinator.md claude-code/agents/workflow-coordinator.md.backup

# Analyze current file structure
grep -n "### \`/" claude-code/agents/workflow-coordinator.md > workflow_commands_analysis.txt
```

#### Step 2: Extract Code Sections
- **Map each command implementation** to target agent
- **Identify shared utility functions** that need extraction
- **Document dependencies** between commands

### Implementation Phase 1: Create New Agents

#### Agent 1: workflow-implementer.md
```yaml
Priority: HIGH (main orchestrator)
Size: ~400 lines
Key Features:
  - Context-aware planning-to-implementation handoff
  - Orchestrates existing agents in sequence
  - Progress tracking with visual indicators
  - Error recovery and fallback strategies
  - Handoff documentation generation
Dependencies:
  - pattern-recognizer.md
  - template-validator.md  
  - dependency-orchestrator.md
  - Framework tools: generator.py, context_manager.py
```

**Implementation Steps:**
1. Create agent definition with orchestration focus
2. Extract `/implement-workflow` logic from workflow-coordinator.md
3. Simplify to focus on coordination, not implementation
4. Add error handling and progress reporting
5. Test orchestration with existing agents

#### Agent 2: workflow-helper.md
```yaml
Priority: MEDIUM (user experience)
Size: ~200 lines
Key Features:
  - Complete user guide for all workflow commands
  - Troubleshooting guide with common issues
  - Framework vs usage context explanation
  - Command examples and usage patterns
  - Integration guidance
Dependencies:
  - Documentation templates
  - Command reference data
```

**Implementation Steps:**
1. Extract `/help-workflow` content from workflow-coordinator.md
2. Organize into logical help sections
3. Add dynamic help based on project state
4. Include troubleshooting patterns
5. Test help system completeness

#### Agent 3: workflow-status.md  
```yaml
Priority: MEDIUM (progress tracking)
Size: ~300 lines
Key Features:
  - File structure analysis and completeness
  - TODO placeholder counting and categorization
  - Validation status reporting
  - Dependency status checking
  - Implementation progress calculation
Dependencies:
  - File system analysis tools
  - Validation result parsing
  - Progress calculation algorithms
```

**Implementation Steps:**
1. Extract `/status-workflow` logic from workflow-coordinator.md
2. Create file analysis utilities
3. Add progress calculation algorithms
4. Implement status reporting templates
5. Test with various workflow states

#### Agent 4: workflow-documenter.md
```yaml
Priority: LOW (nice to have)
Size: ~300 lines  
Key Features:
  - README.md generation with project overview
  - CODE.md technical documentation
  - EXAMPLES.md usage patterns
  - Documentation index and navigation
  - Pattern-specific documentation
Dependencies:
  - Documentation templates
  - Code analysis utilities
  - Markdown generation tools
```

**Implementation Steps:**
1. Extract `/document-workflow` logic from workflow-coordinator.md
2. Create documentation templates
3. Add dynamic content generation
4. Implement pattern-specific documentation
5. Test documentation quality and completeness

### Implementation Phase 2: Handle workflow-coordinator.md

#### Step 1: Verification
```bash
# Verify new agents handle all functionality
./scripts/test-workflow-commands.sh

# Check that no functionality is lost
diff workflow_commands_analysis.txt new_agents_commands.txt
```

#### Step 2: Safe Removal Process
1. **Rename original file** to `workflow-coordinator.md.deprecated`
2. **Add deprecation notice** pointing to new agents
3. **Update any references** in documentation
4. **Test all workflow commands** work with new agents
5. **Monitor for issues** over 1-2 weeks
6. **Remove deprecated file** after verification period

#### Step 3: Documentation Updates
- Update `claude-code-sub-agents-guide.md` with new agent descriptions
- Update `CLAUDE.md` with new workflow command structure  
- Update any integration documentation
- Create migration guide for existing users

### Implementation Phase 3: Testing and Validation

#### Integration Testing
```bash
# Test complete workflow from start to finish
/implement-workflow TestProject
/status-workflow TestProject  
/help-workflow
/document-workflow TestProject

# Verify orchestration works correctly
# Check error handling and recovery
# Validate documentation generation
```

#### Performance Testing
- **File size verification**: Each new agent < 500 lines
- **Response time**: Commands complete within reasonable time
- **Memory usage**: No significant overhead from multiple agents
- **Error handling**: Graceful failures and recovery

## Success Criteria

### Technical Success
- [ ] 4 new agents created, each < 500 lines
- [ ] All original functionality preserved
- [ ] No performance degradation
- [ ] Comprehensive test coverage
- [ ] Documentation updated

### User Experience Success  
- [ ] Commands work identically from user perspective
- [ ] Improved error messages and guidance
- [ ] Better progress tracking and feedback
- [ ] Comprehensive help system
- [ ] Professional documentation generation

### Maintainability Success
- [ ] Each agent has single, clear responsibility
- [ ] Code duplication eliminated
- [ ] Dependencies clearly defined
- [ ] Easy to modify individual agents
- [ ] Clear separation of concerns

## Risk Mitigation

### Risk 1: Functionality Loss
**Mitigation**: 
- Comprehensive mapping of all existing functionality
- Side-by-side testing during implementation
- Keep backup file until fully verified

### Risk 2: Integration Issues
**Mitigation**:
- Test with existing agents early and often  
- Implement rollback plan
- Gradual migration with verification steps

### Risk 3: User Disruption
**Mitigation**:
- Commands work identically from user perspective
- Provide clear migration guidance
- Monitor for issues and respond quickly

## Timeline

### Week 1
- **Days 1-2**: Create workflow-implementer.md and workflow-helper.md
- **Days 3-4**: Create workflow-status.md and workflow-documenter.md  
- **Day 5**: Integration testing and refinement

### Week 2  
- **Days 1-2**: Handle workflow-coordinator.md deprecation
- **Days 3-4**: Documentation updates and final testing
- **Day 5**: Monitoring and issue resolution

## File Structure Changes

### Before
```
claude-code/agents/
└── workflow-coordinator.md (2400+ lines)
```

### After  
```
claude-code/agents/
├── workflow-implementer.md    (~400 lines)
├── workflow-helper.md         (~200 lines)
├── workflow-status.md         (~300 lines)
├── workflow-documenter.md     (~300 lines)
└── workflow-coordinator.md.deprecated
```

### Benefits
- **Maintainability**: 4 focused agents vs 1 massive file
- **Separation of Concerns**: Each agent has single responsibility
- **Reduced Complexity**: Easier to modify individual features
- **Better Testing**: Can test each agent independently
- **Improved Documentation**: Each agent self-documents its purpose

## Implementation Notes

### Code Reuse Strategy
- **Shared utilities**: Extract common bash functions to shared utilities
- **Template patterns**: Standardize output formatting across agents
- **Error handling**: Consistent error reporting and recovery patterns
- **Progress indicators**: Reusable progress bar and status functions

### Quality Standards
- **Code style**: Follow existing agent patterns and conventions
- **Documentation**: Comprehensive inline documentation
- **Error messages**: Clear, actionable error messages
- **User feedback**: Consistent, helpful user communication
- **Testing**: Unit tests for key functionality where applicable

---

**Next Steps**: Review and approve this plan, then begin implementation with workflow-implementer.md as the highest priority agent.