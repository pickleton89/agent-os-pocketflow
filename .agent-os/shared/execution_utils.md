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