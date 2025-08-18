# Sub-Agent Implementation Document
## Agent OS + PocketFlow Framework Enhancement

*Version: 1.0 | Date: 2025-01-18*

---

## Executive Summary

This document specifies the implementation of three new sub-agents for the Agent OS + PocketFlow framework. These agents enhance the framework's ability to generate high-quality templates and guide end-users toward successful PocketFlow implementations.

**Critical Framework Context**: This repository IS the Agent OS + PocketFlow framework itself. These sub-agents enhance template generation and framework capabilities—they do NOT implement end-user functionality.

### The Three Sub-Agents

1. **Template Validator Agent** - Validates generated templates for structural correctness
2. **Pattern Recognizer Agent** - Identifies optimal PocketFlow patterns from requirements  
3. **Dependency Orchestrator Agent** - Manages Python tooling and environment setup

---

## Framework vs. Usage Distinction

### Framework Repository (This Repo)
- **Purpose**: Generate PocketFlow templates for other projects
- **Contains**: Setup scripts, validation tools, code generators
- **Philosophy**: Template placeholders and TODO stubs are intentional design features
- **Dependencies**: Support template generation, not application runtime
- **Sub-Agent Role**: Enhance template quality and generation intelligence

### Usage Repository (End-User Projects)  
- **Purpose**: Where PocketFlow gets installed as a dependency
- **Contains**: Working applications built from generated templates
- **Philosophy**: Where generated templates become functional implementations
- **Dependencies**: Runtime dependencies for actual applications
- **Sub-Agent Role**: The orchestrator agent guides implementation

**Key Principle**: Missing implementations in generated templates are features, not bugs. This framework creates starting points for developers, not finished applications.

---

## Sub-Agent Specifications

### 1. Template Validator Agent

#### Overview
**Agent Name**: `template-validator`  
**Purpose**: Validates generated PocketFlow templates against structural best practices without completing user implementations.

#### Responsibilities
- **Structural Validation**: Ensures generated templates have correct Python syntax and imports
- **Pattern Compliance**: Validates PocketFlow node phases (prep/exec/post) are properly structured
- **Type Safety**: Checks Pydantic models for structural completeness (not implementation)
- **Error Handling**: Verifies error handling patterns are present (not implemented)
- **Workflow Connectivity**: Validates graph structures make logical sense

#### What It Does NOT Do
- Complete TODO implementations
- Add business logic to placeholder functions  
- Install runtime dependencies for end applications
- Test application functionality (tests template structure only)

#### Integration Points
- **Triggers**: Auto-invokes after `generator.py` creates templates
- **Input**: Generated template files in `.agent-os/workflows/`
- **Output**: Validation reports and structural corrections
- **Coordination**: Works with existing validation scripts in `/scripts/validation/`

#### YAML Configuration
```yaml
---
name: template-validator
description: MUST BE USED PROACTIVELY for validating generated PocketFlow templates against structural best practices. Automatically invoked after template generation.
tools: [Read, Grep, Glob, Edit, MultiEdit, Bash]
auto_invoke_triggers:
  - "generate template"
  - "create workflow"
  - "template created"
  - "generator completed"
coordination_aware: true
generates_code: false
validates_templates: true
---
```

### 2. Pattern Recognizer Agent

#### Overview
**Agent Name**: `pattern-recognizer`  
**Purpose**: Analyzes user requirements and identifies optimal PocketFlow patterns, generating appropriate template structures.

#### Responsibilities
- **Requirement Analysis**: Parse natural language requirements for pattern indicators
- **Pattern Mapping**: Map requirements to RAG, Agent, Tool, or Hybrid patterns  
- **Template Selection**: Choose appropriate PocketFlow templates for identified patterns
- **Workflow Graph Design**: Create initial node decomposition and flow structures
- **Documentation Generation**: Update design.md with pattern selection rationale

#### Pattern Recognition Logic
- **RAG Indicators**: "search", "knowledge base", "documentation", "retrieval"
- **Agent Indicators**: "decision", "planning", "reasoning", "autonomous"  
- **Tool Indicators**: "integration", "API", "external service", "automation"
- **Hybrid Indicators**: Complex combinations of the above

#### Integration Points
- **Triggers**: Auto-invokes during spec creation and planning phases
- **Input**: User requirements from `.agent-os/specs/` and `.agent-os/product/`
- **Output**: Pattern recommendations and initial template structures  
- **Coordination**: Works closely with pocketflow-orchestrator

#### YAML Configuration
```yaml
---
name: pattern-recognizer  
description: MUST BE USED PROACTIVELY for analyzing requirements and identifying optimal PocketFlow patterns. Automatically invoked during planning and spec creation.
tools: [Read, Write, Grep, Glob, Edit, MultiEdit, mcp__graphiti__search_memory_nodes]
auto_invoke_triggers:
  - "analyze requirements"
  - "identify patterns"
  - "choose architecture"
  - "plan implementation"
coordination_aware: true
generates_code: true
pattern_specialist: true
---
```

### 3. Dependency Orchestrator Agent

#### Overview
**Agent Name**: `dependency-orchestrator`  
**Purpose**: Manages Python tooling configuration and dependency specifications for generated PocketFlow templates.

#### Responsibilities
- **Environment Configuration**: Generate UV environment configs for templates
- **Tool Setup**: Configure Ruff, type checking, and other Python tools
- **Dependency Analysis**: Determine required packages based on PocketFlow patterns
- **Configuration Generation**: Create pyproject.toml templates with proper dependencies
- **Validation Setup**: Ensure testing infrastructure is properly configured

#### Framework-Specific Focus
- **Template Dependencies**: Packages needed for template structure, not runtime
- **Development Tools**: Ruff, ty, pytest configurations for generated projects
- **Pattern-Specific Needs**: Different dependencies for RAG vs Agent vs Tool patterns
- **Version Management**: Maintain compatibility matrices for Python tooling

#### Integration Points
- **Triggers**: Auto-invokes when new patterns are generated
- **Input**: Pattern specifications and tech-stack.md standards
- **Output**: pyproject.toml templates and tool configurations
- **Coordination**: Works with file-creator for batch configuration generation

#### YAML Configuration
```yaml
---
name: dependency-orchestrator
description: MUST BE USED PROACTIVELY for managing Python tooling and dependency configuration in generated PocketFlow templates. Automatically invoked during template generation.
tools: [Read, Write, Edit, MultiEdit, Bash, Glob]
auto_invoke_triggers:
  - "setup dependencies"
  - "configure environment"  
  - "create project structure"
  - "generate template"
coordination_aware: true
generates_code: true  
dependency_specialist: true
---
```

---

## Implementation Roadmap

### Phase 1: Foundation Setup (Week 1) ✅ COMPLETED

#### Step 1.1: Agent File Creation ✅
- [x] Create `.claude/agents/template-validator.md`
- [x] Create `.claude/agents/pattern-recognizer.md`  
- [x] Create `.claude/agents/dependency-orchestrator.md`
- [x] Validate YAML frontmatter syntax

#### Step 1.2: Integration Configuration ✅
- [x] Update `.agent-os/instructions/orchestration/coordination.yaml`
- [x] Add new agents to coordination map
- [x] Define trigger conditions and dependencies
- [x] Configure validation gates

#### Step 1.3: Framework Integration ✅
- [x] Update `setup-claude-code.sh` to include new agents
- [x] Modify generator coordination logic
- [x] Add agent detection to validation scripts

### Phase 2: Template Validator Implementation (Week 2)

#### Step 2.1: Validation Logic
- [ ] Implement Python syntax validation
- [ ] Add PocketFlow pattern structure checks
- [ ] Create Pydantic model validation
- [ ] Build workflow graph validation

#### Step 2.2: Integration Testing
- [ ] Test with existing generator.py templates
- [ ] Validate against known good/bad template examples
- [ ] Ensure proper error reporting
- [ ] Verify coordination with validation scripts

#### Step 2.3: Documentation
- [ ] Add validation criteria documentation
- [ ] Update framework setup instructions
- [ ] Create troubleshooting guide

### Phase 3: Pattern Recognizer Implementation (Week 3)

#### Step 3.1: Pattern Analysis Engine
- [ ] Implement requirement parsing logic
- [ ] Build pattern indicator recognition
- [ ] Create pattern confidence scoring
- [ ] Add template selection logic

#### Step 3.2: Template Generation
- [ ] Integrate with existing PocketFlow templates
- [ ] Add workflow graph generation
- [ ] Implement design document updates
- [ ] Create pattern justification logic

#### Step 3.3: Orchestrator Integration
- [ ] Coordinate with pocketflow-orchestrator
- [ ] Implement handoff protocols
- [ ] Add pattern override capabilities
- [ ] Test complex requirement scenarios

### Phase 4: Dependency Orchestrator Implementation (Week 4)

#### Step 4.1: Configuration Generation
- [ ] Implement pyproject.toml template generation
- [ ] Add UV environment configuration
- [ ] Create tool configuration templates
- [ ] Build dependency analysis logic

#### Step 4.2: Pattern-Specific Dependencies
- [ ] Map PocketFlow patterns to dependency sets
- [ ] Implement version compatibility checking
- [ ] Add development vs runtime dependency separation
- [ ] Create configuration validation

#### Step 4.3: Integration and Testing
- [ ] Test with all PocketFlow pattern types
- [ ] Validate generated configurations
- [ ] Ensure proper tool chain setup
- [ ] Verify framework vs usage separation

### Phase 5: System Integration and Validation (Week 5)

#### Step 5.1: End-to-End Testing
- [ ] Test complete agent coordination
- [ ] Validate template generation pipeline
- [ ] Ensure proper framework/usage distinction
- [ ] Test edge cases and error conditions

#### Step 5.2: Performance Optimization
- [ ] Optimize agent coordination overhead
- [ ] Implement caching where appropriate
- [ ] Reduce template generation time
- [ ] Minimize resource usage

#### Step 5.3: Documentation and Release
- [ ] Complete implementation documentation
- [ ] Update framework setup guides
- [ ] Create migration guide for existing users
- [ ] Prepare release notes

---

## Integration Points

### Existing Framework Components

#### Coordination System
- **File**: `.agent-os/instructions/orchestration/coordination.yaml`
- **Updates**: Add new agents to coordination map
- **New Sections**:
  ```yaml
  template-validator:
    triggers_on: ["template_generation_complete"]
    validates: ["structural_integrity", "pattern_compliance"]
    outputs: ["validation_reports"]
    
  pattern-recognizer:
    triggers_on: ["requirements_analysis", "spec_creation"]
    analyzes: ["user_requirements", "pattern_indicators"]
    outputs: ["pattern_recommendations", "template_selections"]
    
  dependency-orchestrator:
    triggers_on: ["pattern_selected", "template_generated"]
    configures: ["python_environment", "development_tools"]
    outputs: ["pyproject_templates", "tool_configs"]
  ```

#### Generator System
- **File**: `.agent-os/workflows/generator.py`
- **Integration**: Add agent coordination hooks
- **New Functions**:
  ```python
  def coordinate_template_validation(template_path: str) -> ValidationResult
  def request_pattern_analysis(requirements: str) -> PatternRecommendation
  def generate_dependency_config(pattern: str) -> DependencyConfig
  ```

#### Validation Scripts
- **Directory**: `scripts/validation/`
- **New Scripts**:
  - `validate-template-structure.sh`
  - `validate-pattern-recognition.sh`
  - `validate-dependency-config.sh`

### New Framework Components

#### Agent Coordination Hub
- **File**: `.agent-os/instructions/orchestration/agent-coordination.md`
- **Purpose**: Define how new agents work together
- **Content**: Coordination protocols and handoff procedures

#### Template Quality Standards
- **File**: `.agent-os/instructions/orchestration/template-standards.md`
- **Purpose**: Define validation criteria for generated templates
- **Content**: Structural requirements and quality gates

#### Pattern Library
- **Directory**: `.agent-os/patterns/`
- **Files**:
  - `rag-patterns.yaml` - RAG pattern definitions
  - `agent-patterns.yaml` - Agent pattern definitions  
  - `tool-patterns.yaml` - Tool pattern definitions
  - `hybrid-patterns.yaml` - Hybrid pattern definitions

---

## Testing & Validation Requirements

### Unit Testing
- **Template Validator**: Test validation logic against known template structures
- **Pattern Recognizer**: Test pattern identification with various requirement examples
- **Dependency Orchestrator**: Test configuration generation for all pattern types

### Integration Testing
- **Agent Coordination**: Test proper handoffs between agents
- **Template Generation**: Test complete pipeline from requirements to validated templates
- **Framework Preservation**: Ensure framework vs usage distinction is maintained

### Validation Criteria
- **Framework Integrity**: New agents enhance framework without breaking existing functionality
- **Template Quality**: Generated templates maintain proper structure and placeholder philosophy
- **Performance Impact**: Agent coordination doesn't significantly slow template generation
- **Documentation Accuracy**: All new functionality is properly documented

### Test Environment Setup
```bash
# Framework testing (this repository)
./scripts/run-all-tests.sh
./scripts/validation/validate-integration.sh
./scripts/validation/validate-orchestration.sh
./scripts/validation/validate-end-to-end.sh

# Agent-specific testing
./scripts/test-template-validator.sh
./scripts/test-pattern-recognizer.sh  
./scripts/test-dependency-orchestrator.sh
```

---

## Success Metrics

### Framework Enhancement Metrics
- **Template Quality**: 95% of generated templates pass structural validation
- **Pattern Accuracy**: 90% of pattern recommendations align with user requirements
- **Configuration Correctness**: 100% of generated pyproject.toml files are syntactically valid

### User Experience Metrics
- **Template Generation Speed**: No more than 10% slowdown from agent coordination
- **Setup Success Rate**: 95% of users successfully implement generated templates
- **Framework Adoption**: Increased usage of PocketFlow patterns in end-user projects

### Framework Integrity Metrics
- **Separation Maintenance**: 100% adherence to framework vs usage distinction
- **Backward Compatibility**: 100% compatibility with existing framework installations
- **Documentation Accuracy**: All new functionality fully documented and validated

---

## Risk Assessment and Mitigation

### Technical Risks
- **Risk**: Agent coordination overhead slows template generation
- **Mitigation**: Implement asynchronous coordination and caching

- **Risk**: Template validation becomes too restrictive  
- **Mitigation**: Configurable validation levels and override mechanisms

- **Risk**: Pattern recognition generates incorrect recommendations
- **Mitigation**: Confidence scoring and human override capabilities

### Framework Risks  
- **Risk**: Agents blur framework vs usage distinction
- **Mitigation**: Clear agent scope definitions and validation gates

- **Risk**: Over-automation reduces user learning
- **Mitigation**: Maintain educational documentation and transparent decision-making

### Implementation Risks
- **Risk**: Complex coordination logic introduces bugs
- **Mitigation**: Comprehensive testing and gradual rollout

- **Risk**: New agents conflict with existing framework components
- **Mitigation**: Thorough integration testing and backward compatibility validation

---

## Conclusion

These three sub-agents will significantly enhance the Agent OS + PocketFlow framework's ability to generate high-quality templates and guide users toward successful implementations. By maintaining strict adherence to the framework vs usage distinction, they enhance the meta-framework's capabilities without compromising its design philosophy.

The implementation roadmap provides clear, actionable steps for adding these agents to the framework while preserving all existing functionality and maintaining the intentional design of template placeholders as learning tools rather than completed implementations.