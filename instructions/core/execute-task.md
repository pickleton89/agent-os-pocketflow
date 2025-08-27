---
description: Rules to execute a task and its sub-tasks using Agent OS
globs:
alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Task Execution Rules

## Overview

Execute a specific task along with its sub-tasks systematically following a TDD development workflow. This instruction can be invoked directly by users (`/execute-task`) or called from execute-tasks.md in orchestrated mode.

**Shared Resources**: See @~/.agent-os/shared/execution_utils.md for common patterns, phase definitions, and quality standards used by both execute-tasks.md and execute-task.md.

<invocation_modes>
  <direct_invocation>
    USER: "/execute-task" or "/execute-task Task 3.2"
    CONTEXT: User wants to work on a specific task independently
    BEHAVIOR: Interactive task selection and full context loading
  </direct_invocation>
  
  <orchestrated_invocation>  
    CALLER: execute-tasks.md via Task tool
    CONTEXT: Part of full workflow orchestration
    BEHAVIOR: Use provided task context, minimal additional loading
  </orchestrated_invocation>
</invocation_modes>

<pre_flight_check>
  EXECUTE: @~/.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>


<process_flow>

<step number="1" name="task_understanding">

### Step 1: Task Understanding & Context Determination

Determine invocation mode and establish task context appropriately.

<invocation_detection>
  <check_for_orchestrated_context>
    IF task_context provided from execute-tasks.md:
      MODE: orchestrated
      CONTEXT: Use provided task information
      TASK: task_context.parent_task_number and subtasks
    ELSE:
      MODE: direct
      CONTEXT: Load from user input and tasks.md
      TASK: User-specified or interactive selection
    END_IF
  </check_for_orchestrated_context>
</invocation_detection>

<task_selection_and_analysis>
  <orchestrated_mode>
    IF MODE == orchestrated:
      RECEIVE: Task context from execute-tasks.md
      EXTRACT: parent_task_number, parent_task_description, subtasks
      VALIDATE: Context completeness and consistency
      PROCEED: With provided task information
    END_IF
  </orchestrated_mode>
  
  <direct_mode>
    IF MODE == direct:
      <user_task_specification>
        IF user specified task (e.g., "/execute-task Task 3.2"):
          PARSE: Task number from user input
          VALIDATE: Task exists in tasks.md
        ELSE:
          DISPLAY: Available tasks from tasks.md
          PROMPT: User to select specific task
        END_IF
      </user_task_specification>
      
      <task_analysis_direct>
        READ: Specified task and all subtasks from tasks.md
        ANALYZE: Task dependencies and prerequisites
        UNDERSTAND: Full scope of implementation required
        NOTE: Test requirements for each sub-task
      </task_analysis_direct>
    END_IF
  </direct_mode>
</task_selection_and_analysis>

<context_validation>
  CONFIRM: Task selection is clear and unambiguous
  VERIFY: All subtasks are identified and understood
  CHECK: Prerequisites and dependencies are noted
  ENSURE: Ready to proceed with implementation
</context_validation>

<instructions>
  DETECT: Invocation mode (orchestrated vs direct)
  HANDLE: Task selection based on mode
  LOAD: Appropriate context for selected task
  VALIDATE: Task understanding is complete
  PREPARE: For systematic implementation
</instructions>

</step>

<step number="2" name="technical_spec_review">

### Step 2: Technical Specification Review

Search and extract relevant sections from technical-spec.md to understand the technical implementation approach for this task.

<selective_reading>
  <search_technical_spec>
    FIND sections in technical-spec.md related to:
    - Current task functionality
    - Implementation approach for this feature
    - Integration requirements
    - Performance criteria
  </search_technical_spec>
</selective_reading>

<instructions>
  ACTION: Search technical-spec.md for task-relevant sections
  EXTRACT: Only implementation details for current task
  SKIP: Unrelated technical specifications
  FOCUS: Technical approach for this specific feature
</instructions>

</step>

<step number="3" subagent="context-fetcher" name="best_practices_review">

### Step 3: Best Practices Review

Use the context-fetcher subagent to retrieve relevant sections from @~/.agent-os/standards/best-practices.md that apply to the current task's technology stack and feature type.

<selective_reading>
  <search_best_practices>
    FIND sections relevant to:
    - Task's technology stack
    - Feature type being implemented
    - Testing approaches needed
    - Code organization patterns
  </search_best_practices>
</selective_reading>

<instructions>
  ACTION: Use context-fetcher subagent
  REQUEST: "Find best practices sections relevant to:
            - Task's technology stack: [CURRENT_TECH]
            - Feature type: [CURRENT_FEATURE_TYPE]
            - Testing approaches needed
            - Code organization patterns"
  PROCESS: Returned best practices
  APPLY: Relevant patterns to implementation
</instructions>

</step>

<step number="4" subagent="context-fetcher" name="code_style_review">

### Step 4: Code Style Review

Use the context-fetcher subagent to retrieve relevant code style rules from @~/.agent-os/standards/code-style.md for the languages and file types being used in this task.

<selective_reading>
  <search_code_style>
    FIND style rules for:
    - Languages used in this task
    - File types being modified
    - Component patterns being implemented
    - Testing style guidelines
  </search_code_style>
</selective_reading>

<instructions>
  ACTION: Use context-fetcher subagent
  REQUEST: "Find code style rules for:
            - Languages: [LANGUAGES_IN_TASK]
            - File types: [FILE_TYPES_BEING_MODIFIED]
            - Component patterns: [PATTERNS_BEING_IMPLEMENTED]
            - Testing style guidelines"
  PROCESS: Returned style rules
  APPLY: Relevant formatting and patterns
</instructions>

</step>

<step number="5" name="task_execution">

### Step 5: Task and Sub-task Execution

Execute the parent task and all sub-tasks systematically following TDD approach and PocketFlow-specific patterns when applicable.

<execution_context_detection>
  <project_type_detection>
    REQUIRE: docs/design.md exists (universal design-first methodology)
    VERIFY: PocketFlow imports and architecture in codebase  
    CONFIRM: utils/ directory with domain-specific functions
    EXECUTE: Universal PocketFlow task implementation
  </project_type_detection>
</execution_context_detection>

<design_document_validation>
  <universal_requirement>
    <mandatory_execution>
      VALIDATE: docs/design.md exists and is complete for all projects
      REQUIRE: All sections filled with specific details
      VERIFY: Mermaid diagrams are syntactically correct
      CONFIRM: Input/output contracts for all utility functions specified
      BLOCK: Implementation if design document incomplete
    </mandatory_execution>
  </universal_requirement>
</design_document_validation>

<execution_standards>
  <follow_exactly>
    - Task specifications from tasks.md
    - Technical specifications from technical-spec.md
    - @~/.agent-os/standards/code-style.md patterns
    - @~/.agent-os/standards/best-practices.md guidelines
  </follow_exactly>
  
  <tdd_approach>Test-driven development throughout</tdd_approach>
  
  <pocketflow_phase_execution>
    <universal_pocketflow_phases>
      EXECUTE: Universal PocketFlow 6-phase implementation for all projects:
        
        **Phase 0: Schema Design & Validation**
        - Create Pydantic schemas with comprehensive validation tests
        - Define SharedStore schema using Pydantic models
        - Implement data transformation schemas
        - Test schema validation edge cases
        
        **Phase 1: Utility Functions Development**
        - Implement utility functions with input/output contracts from design.md
        - Create standalone tests with type hints
        - Build LLM integration utilities (call_llm_*.py functions)
        - Develop data retrieval utilities (retrieve_*.py functions)
        - Ensure all utility functions are testable and modular
        
        **Phase 2: FastAPI Integration (if applicable)**
        - Create FastAPI endpoints with proper async patterns
        - Implement Pydantic request/response models
        - Add middleware and error handling
        - Build WebSocket support if needed
        - Test API endpoints thoroughly
        
        **Phase 3: PocketFlow Node Implementation**  
        - Implement nodes.py following lifecycle patterns (prep/exec/post)
        - Ensure clear separation of node responsibilities
        - Define action strings for flow transitions
        - Implement error handling as action string routing (not try/catch inline)
        - Add logging for debugging and monitoring
        - Use Node retry mechanisms for error handling
        
        **Phase 4: Flow Assembly & Orchestration**
        - Assemble flow.py connecting nodes with action-based transitions
        - Match Mermaid diagram from design.md exactly
        - Implement error handling and retry strategies
        - Consider BatchNode/BatchFlow for iterative/parallel processing
        - Validate integration points work as designed
        
        **Phase 5: Integration Testing & Quality Validation**
        - Run comprehensive integration tests
        - Apply toolchain: `ruff format`, `ruff check`, `uvx ty check`
        - Validate against design.md specifications
        - Test error scenarios and recovery paths
        - Ensure logging and monitoring work correctly
    </universal_pocketflow_phases>
  </pocketflow_phase_execution>
  
  <type_safety_enforcement>
    - All functions must have complete type hints
    - Pydantic models validate at all boundaries  
    - FastAPI automatic documentation generation validated
    - SharedStore schema enforced with Pydantic models
    - No Any types without explicit justification
  </type_safety_enforcement>
  
  <quality_principles>
    - Keep files modular and organized (no large monolithic files)
    - Follow "Fail Fast" by avoiding excessive try/except during initial implementation
    - Emphasize clear error messages and debugging information
    - Maintain consistent coding patterns throughout implementation
  </quality_principles>
</execution_standards>

<subtask_execution_loop>
  FOR each subtask in parent_task:
    <subtask_implementation>
      READ: Subtask description and requirements
      PLAN: Implementation approach based on subtask type
      IMPLEMENT: Following appropriate phase patterns above
      TEST: Verify subtask completion meets acceptance criteria
      UPDATE: Mark subtask as [COMPLETED] in tasks.md
    </subtask_implementation>
    
    <quality_validation>
      RUN: Relevant tests for implemented functionality
      CHECK: Code quality with ruff and ty (if PocketFlow)
      VALIDATE: Implementation matches specifications
      ENSURE: No regressions in existing functionality
    </quality_validation>
  END_FOR
</subtask_execution_loop>

<instructions>
  ACTION: Validate universal PocketFlow execution context
  VALIDATE: Design document for all projects (universal requirement)
  EXECUTE: Universal PocketFlow phase-based implementation
  FOLLOW: All coding standards and quality requirements
  IMPLEMENT: Each subtask systematically with proper testing
  MAINTAIN: Code quality and architectural consistency throughout
  UPDATE: Progress tracking for each completed subtask
</instructions>

</step>

<step number="6" subagent="test-runner" name="task_test_verification">

### Step 6: Task-Specific Test Verification

Use the test-runner subagent to run and verify only the tests specific to this parent task (not the full test suite) to ensure the feature is working correctly.

<focused_test_execution>
  <run_only>
    - All new tests written for this parent task
    - All tests updated during this task
    - Tests directly related to this feature
  </run_only>
  <skip>
    - Full test suite (done later in execute-tasks.md)
    - Unrelated test files
  </skip>
</focused_test_execution>

<final_verification>
  IF any test failures:
    - Debug and fix the specific issue
    - Re-run only the failed tests
  ELSE:
    - Confirm all task tests passing
    - Ready to proceed
</final_verification>

<instructions>
  ACTION: Use test-runner subagent
  REQUEST: "Run tests for [this parent task's test files]"
  WAIT: For test-runner analysis
  PROCESS: Returned failure information
  VERIFY: 100% pass rate for task-specific tests
  CONFIRM: This feature's tests are complete
</instructions>

</step>

<step number="7" name="task_status_updates">

### Step 7: Task Status Updates

Update the tasks.md file immediately after completing each task to track progress.

<update_format>
  <completed>- [x] Task description</completed>
  <incomplete>- [ ] Task description</incomplete>
  <blocked>
    - [ ] Task description
    ⚠️ Blocking issue: [DESCRIPTION]
  </blocked>
</update_format>

<blocking_criteria>
  <attempts>maximum 3 different approaches</attempts>
  <action>document blocking issue</action>
  <emoji>⚠️</emoji>
</blocking_criteria>

<instructions>
  ACTION: Update tasks.md after each task completion
  MARK: [x] for completed items immediately
  DOCUMENT: Blocking issues with ⚠️ emoji
  LIMIT: 3 attempts before marking as blocked
</instructions>

</step>

</process_flow>
