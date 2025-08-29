# Agent OS + PocketFlow Execution Utilities

## Overview

Shared utilities and patterns used by both execute-tasks.md and execute-task.md to prevent code duplication and ensure consistency.

## PocketFlow Detection Patterns

### LLM/AI Component Detection
```yaml
detection_criteria:
  design_document: Check if docs/design.md exists
  pocketflow_files: Look for nodes.py, flow.py files
  llm_utilities: Identify utils/ directory with LLM-related functions
  imports: Check for PocketFlow imports in codebase
  schema_patterns: Look for SharedStore schema definitions
```

### Project Type Classification
```yaml
project_types:
  pocketflow: LLM/AI components with PocketFlow patterns
  standard: Traditional software development tasks
  graphrag: Graph-based RAG implementations (future)
  multi_agent: Multi-agent coordination (future)
```

## PocketFlow Phase Definitions

### Phase 0: Schema Design & Validation
```yaml
phase_0_schema:
  purpose: Create Pydantic schemas with comprehensive validation
  deliverables:
    - SharedStore schema using Pydantic models
    - Data transformation schemas
    - Schema validation tests
    - Edge case testing
  validation:
    - All schemas have proper type hints
    - Validation rules are comprehensive
    - Test coverage includes edge cases
```

### Phase 1: Utility Functions Development
```yaml
phase_1_utilities:
  purpose: Implement utility functions with input/output contracts
  deliverables:
    - LLM integration utilities (call_llm_*.py)
    - Data retrieval utilities (retrieve_*.py)
    - Standalone tests with type hints
    - Modular, testable functions
  validation:
    - All functions match design.md contracts
    - Complete type annotations
    - Comprehensive test coverage
```

### Phase 2: FastAPI Integration
```yaml
phase_2_api:
  purpose: Create FastAPI endpoints with proper async patterns
  deliverables:
    - Pydantic request/response models
    - Async endpoint implementations
    - Middleware and error handling
    - WebSocket support (if needed)
  validation:
    - API documentation auto-generated
    - All endpoints properly tested
    - Error handling comprehensive
```

### Phase 3: PocketFlow Node Implementation
```yaml
phase_3_nodes:
  purpose: Implement nodes.py following lifecycle patterns
  deliverables:
    - prep/exec/post method implementations
    - Clear separation of responsibilities
    - Action string definitions
    - Error handling as action routing
  validation:
    - Node lifecycle properly implemented
    - Action strings match design
    - Error handling converts to actions
```

### Phase 4: Flow Assembly & Orchestration
```yaml
phase_4_flows:
  purpose: Assemble flow.py connecting nodes
  deliverables:
    - Action-based node transitions
    - Mermaid diagram implementation
    - Error handling and retry strategies
    - Integration point validation
  validation:
    - Flow matches design.md diagram
    - All transitions properly implemented
    - Error recovery functional
```

### Phase 5: Integration Testing & Quality
```yaml
phase_5_integration:
  purpose: Comprehensive testing and quality validation
  deliverables:
    - Integration test suite
    - ruff format/check compliance
    - ty type checking validation
    - Design adherence verification
  validation:
    - All quality gates pass
    - Implementation matches design
    - Error scenarios tested
```

## Standard TDD Workflow

### Traditional Task Execution
```yaml
standard_tdd:
  purpose: Non-PocketFlow task implementation
  approach:
    - Write failing tests first
    - Implement minimal code to pass
    - Refactor while keeping tests green
    - Repeat for each subtask
  validation:
    - Test coverage adequate
    - Code quality maintained
    - No regressions introduced
```

## Quality Enforcement Patterns

### Type Safety Requirements
```yaml
type_safety:
  requirements:
    - All functions have complete type hints
    - Pydantic models validate at boundaries
    - FastAPI documentation auto-generated
    - SharedStore schema enforced
    - No Any types without justification
```

### Code Quality Standards
```yaml
quality_standards:
  toolchain:
    - ruff format: Code formatting
    - ruff check: Linting and style
    - ty: Type checking
    - pytest: Testing framework
  principles:
    - Modular file organization
    - Clear error messages
    - Consistent coding patterns
    - Fail fast approach
```

## Context Management Strategies

### Token Efficiency Patterns
```yaml
context_efficiency:
  orchestrated_mode:
    - Receive minimal task context
    - Skip redundant context loading
    - Use provided execution state
  direct_mode:
    - Load full task context
    - Interactive task selection
    - Complete context gathering
```

### Shared State Management
```yaml
shared_state:
  workflow_level:
    - Project configuration
    - Git branch state
    - Progress tracking
    - Error recovery info
  task_level:
    - Task specifications
    - Implementation context
    - Quality metrics
    - Completion status
```

## Error Handling Patterns

### PocketFlow Error Handling
```yaml
pocketflow_errors:
  strategy: Action string routing (not try/catch inline)
  implementation:
    - Convert errors to action strings
    - Use Node retry mechanisms
    - Implement graceful degradation
    - Log errors for debugging
```

### Standard Error Handling
```yaml
standard_errors:
  strategy: Traditional exception handling
  implementation:
    - Appropriate try/catch blocks
    - Clear error messages
    - Recovery strategies
    - User-friendly feedback
```

## Subagent Context Flow Specifications

### Context Isolation Architecture

**⚠️ CRITICAL**: Subagents do not share memory or conversation history with the primary agent. Each subagent call is stateless and context-isolated, requiring explicit context passing and structured output formats.

### Enhanced Context Flow Template (Phase 2 Pattern)

**Standard Pattern**:
```xml
<step number="X.Y" subagent="agent-name" name="descriptive_name">
### Step X.Y: Descriptive Step Title

<step_metadata>
  <uses>agent-name subagent</uses>
  <validates>specific validation purpose</validates>
  <purpose>clear explanation of why this subagent is needed</purpose>
</step_metadata>

Use the agent-name subagent to [specific task] with comprehensive context provision.

<context_block_name_context>
  <context_to_provide>
    - Specific input requirement 1
    - Specific input requirement 2
    - Previous step outputs: [VARIABLE_NAME_FROM_STEP_X]
    - User requirements and constraints
    - Technical context and decisions
  </context_to_provide>
  
  <expected_output>
    - Specific output requirement 1
    - Specific output requirement 2
    - Structured data for next step integration
    - Validation results or recommendations
  </expected_output>
  
  <required_for_next_step>
    Clear explanation of how this output integrates into subsequent steps
  </required_for_next_step>
</context_block_name_context>

<failure_handling>
  IF agent-name reports [specific failure conditions]:
    - Specific recovery action 1
    - Specific recovery action 2
    - Fallback strategy (e.g., default Agent pattern)
  ELSE:
    - Proceed with successful execution path
</failure_handling>

<instructions>
  ACTION: Use agent-name subagent for [specific purpose]
  REQUEST: "Detailed request with all context variables populated"
  PROCESS: Returned output and integrate into workflow
  APPLY: Results to subsequent steps
</instructions>
</step>
```

### Agent-Specific Context Requirements

**context-fetcher**:
- Input: Specific file paths, sections to extract, filtering criteria
- Output: Extracted content with source attribution, context status
- Integration: Parsed content available for use in subsequent steps
- Context Pattern: `<[purpose]_retrieval_context>` (e.g., `<best_practices_retrieval_context>`, `<code_style_retrieval_context>`)

**pattern-recognizer**:
- Input: Complete requirements, existing project context, constraints
- Output: Identified patterns with confidence scores, template recommendations
- Integration: Pattern selection drives subsequent template and architecture decisions
- Context Pattern: `<pattern_validation_context>` for architectural analysis

**strategic-planner**:
- Input: Product vision, feature requirements, technical constraints
- Output: Strategic recommendations with rationale, implementation priorities
- Integration: Strategic decisions inform roadmap and architectural choices
- Context Pattern: `<strategic_analysis_context>` for high-level planning

**dependency-orchestrator**:
- Input: Project requirements, current environment state, tool preferences
- Output: Environment setup commands, dependency specifications, validation results
- Integration: Environment readiness enables implementation phases
- Context Pattern: `<environment_validation_context>` for environment setup

**template-validator**:
- Input: Generated code/templates, quality criteria, framework standards
- Output: Validation results with specific issues and recommendations
- Integration: Quality approval gates prevent progression of flawed implementations
- Context Pattern: `<quality_validation_context>` for quality assurance

**test-runner**:
- Input: Test commands, scope specifications, failure analysis requirements
- Output: Test results, failure analysis, quality metrics
- Integration: Testing results inform implementation validation and next steps
- Context Pattern: `<test_verification_context>` for testing validation

### Context Flow Usage Examples

**Example 1: Pattern Recognition Integration** (from execute-task.md):
```xml
<pattern_validation_context>
  <context_to_provide>
    - Current task description and requirements from tasks.md
    - Existing project context from technical-spec.md analysis
    - PocketFlow pattern options: Agent, RAG, Workflow, MapReduce, Multi-Agent, Structured Output
    - Performance requirements: latency, throughput, scalability needs
    - Current architecture decisions and constraints
  </context_to_provide>
  
  <expected_output>
    - Recommended PocketFlow pattern with confidence score and rationale
    - Validation of current approach or suggested optimizations
    - Specific node and flow recommendations for implementation
    - Integration considerations with existing patterns
  </expected_output>
  
  <required_for_next_step>
    Pattern validation informs implementation approach and architecture decisions
  </required_for_next_step>
</pattern_validation_context>
```

**Example 2: Strategic Planning Integration** (from analyze-product.md):
```xml
<strategic_analysis_context>
  <context_to_provide>
    - Complete codebase analysis from Step 1
    - PocketFlow pattern recommendations from Step 1.5
    - User-provided product context and vision from Step 2
    - Current development state and roadmap priorities
    - Technical constraints and integration opportunities
    - Team capabilities and development preferences
  </context_to_provide>
  
  <expected_output>
    - Strategic roadmap for Agent OS integration
    - PocketFlow pattern implementation priority matrix
    - Migration strategy for existing architecture
    - Risk assessment and mitigation recommendations
    - Timeline estimates and resource requirements
  </expected_output>
  
  <required_for_next_step>
    Strategic analysis provides foundation for plan-product execution and strategic approach validation
  </required_for_next_step>
</strategic_analysis_context>
```

**Example 3: Environment Validation Integration** (from execute-task.md):
```xml
<environment_validation_context>
  <context_to_provide>
    - Current task requirements and technology stack needs
    - Project pyproject.toml and dependency requirements
    - Required toolchain: uv, Ruff, ty, pytest configuration
    - PocketFlow installation and version requirements
    - Pattern-specific dependencies from Step 4.5: [PATTERN_VALIDATION_FROM_STEP_4_5]
    - Any task-specific dependencies or tools needed
  </context_to_provide>
  
  <expected_output>
    - Environment setup validation results
    - Missing dependencies or configuration issues
    - Toolchain validation status (uv/Ruff/ty/pytest)
    - Environment setup commands if needed
    - PocketFlow readiness confirmation
  </expected_output>
  
  <required_for_next_step>
    Environment readiness enables reliable task implementation
  </required_for_next_step>
</environment_validation_context>

<blocking_validation>
  IF dependency-orchestrator identifies critical environment issues:
    - Execute recommended setup commands immediately
    - Install missing dependencies via uv add
    - Configure toolchain settings as specified
    - Re-validate environment until all requirements met
    - BLOCK progression until environment fully ready
  ELSE:
    - Proceed to implementation with validated environment
</blocking_validation>
```

### Information Flow Validation Checklist

Before implementing any subagent call, validate:
- [ ] **Complete Context**: All necessary information explicitly provided to subagent
- [ ] **Self-Contained**: Subagent has everything needed without external context
- [ ] **Structured Output**: Output format enables proper integration back to workflow
- [ ] **No Information Loss**: Critical workflow data preserved through subagent handoff
- [ ] **Error Recovery**: Fallback behavior defined for subagent failures
- [ ] **Integration Path**: Clear process for using subagent output in next steps
- [ ] **Variable Consistency**: Output variables properly referenced in subsequent steps

### Quality Standards for Context Blocks

**Required Elements**:
1. `<context_to_provide>`: Explicit list of all inputs needed
2. `<expected_output>`: Structured specification of required outputs
3. `<required_for_next_step>`: Integration explanation for workflow continuation
4. `<failure_handling>`: Error recovery and fallback strategies (where applicable)
5. `<blocking_validation>`: Critical validation gates (for essential subagents)

**Naming Conventions**:
- Context blocks: `<[purpose]_context>` (e.g., `<pattern_validation_context>`)
- Variable references: `[DESCRIPTIVE_NAME_FROM_STEP_X_Y]` (e.g., `[PATTERN_VALIDATION_FROM_STEP_4_5]`)
- Step metadata: Always include `<uses>`, `<validates>`, `<purpose>` elements

## Integration Validation

### Cross-File Coordination
```yaml
coordination_validation:
  execute_tasks_to_execute_task:
    - Task context properly passed
    - Execution state maintained
    - Progress tracking functional
    - Error reporting accurate
  
  execute_task_to_execute_tasks:
    - Completion status returned
    - Error context preserved
    - Quality metrics reported
    - Next steps identified
```

### Design Document Adherence
```yaml
design_adherence:
  validation_points:
    - Utility function contracts match
    - SharedStore schema implementation correct
    - Node responsibilities align with design
    - Flow assembly matches Mermaid diagram
    - Integration points work as designed
```