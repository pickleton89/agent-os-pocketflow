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

<subagent_context>
  **Context:** Current task tech stack, feature type, testing requirements
  **Output:** Relevant best practices sections with source references
  **Next Step:** Implementation standards for Step 5
</subagent_context>

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
  ACTION: Use context-fetcher subagent for best practices retrieval
  REQUEST: "Retrieve relevant best practices from @~/.agent-os/standards/best-practices.md:
            - Task's technology stack: [TECH_STACK_FROM_TECHNICAL_SPEC]
            - Feature type: [FEATURE_TYPE_FROM_TASKS_MD]
            - Testing approaches needed
            - Code organization patterns"
  PROCESS: Returned best practices
  APPLY: Relevant patterns to implementation
</instructions>

</step>

<step number="4" subagent="context-fetcher" name="code_style_review">

### Step 4: Code Style Review

Use the context-fetcher subagent to retrieve relevant code style rules from @~/.agent-os/standards/code-style.md for the languages and file types being used in this task.

<subagent_context>
  **Context:** Task languages, file types, component patterns, testing conventions
  **Output:** Language-specific style rules and framework guidelines
  **Next Step:** Consistent implementation standards for Step 5
</subagent_context>

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
  ACTION: Use context-fetcher subagent for code style retrieval
  REQUEST: "Find code style rules for:
            - Languages: [LANGUAGES_IN_TASK]
            - File types: [FILE_TYPES_BEING_MODIFIED]
            - Component patterns: [PATTERNS_BEING_IMPLEMENTED]
            - Testing style guidelines"
  PROCESS: Returned style rules
  APPLY: Relevant formatting and patterns
</instructions>

</step>

<step number="4.5" subagent="pattern-analyzer" name="pocketflow_pattern_validation">

### Step 4.5: PocketFlow Pattern Validation

**Uses:** pattern-analyzer subagent for PocketFlow pattern validation

Use the pattern-analyzer subagent to validate that the current task aligns with appropriate PocketFlow patterns and identify any architecture optimization opportunities.

<subagent_context>
  **Context:** Task requirements, project architecture, performance needs, pattern options
  **Output:** Recommended PocketFlow pattern with rationale and implementation guidance
  **Next Step:** Architecture decisions for implementation strategy
</subagent_context>

**Fallback:** Use Agent pattern if analysis inconclusive

<instructions>
  ACTION: Use pattern-analyzer subagent for task-specific pattern validation
  REQUEST: "Analyze current task for optimal PocketFlow pattern compliance:
            - Task requirements: [CURRENT_TASK_AND_SUBTASKS]
            - Project context: [TECHNICAL_SPEC_ANALYSIS]
            - Existing patterns: [CURRENT_PROJECT_ARCHITECTURE]
            - Performance needs: [LATENCY_THROUGHPUT_SCALABILITY]
            - Pattern options: Agent, RAG, Workflow, MapReduce, Multi-Agent, Structured Output"
  PROCESS: Pattern recommendations and optimization suggestions
  APPLY: Validated patterns to implementation strategy
</instructions>

</step>

<step number="4.7" subagent="dependency-orchestrator" name="development_environment_validation">

### Step 4.7: Development Environment Validation

**Uses:** dependency-orchestrator subagent for environment validation

Use the dependency-orchestrator subagent to verify the development environment is properly configured for the current task implementation.

<subagent_context>
  **Context:** Task tech needs, toolchain requirements, PocketFlow installation
  **Output:** Environment validation results and setup commands if needed
  **Next Step:** Reliable task implementation
</subagent_context>

**Blocking:** Must resolve all environment issues before proceeding

<instructions>
  ACTION: Use dependency-orchestrator subagent for environment validation
  REQUEST: "Validate development environment for current task:
            - Task requirements: [CURRENT_TASK_TECH_NEEDS]
            - Project dependencies: [PYPROJECT_TOML_ANALYSIS]
            - Toolchain: uv, Ruff, ty, pytest configuration status
            - PocketFlow: Installation and version validation
            - Environment: Current setup vs. required setup"
  PROCESS: Environment validation results and setup recommendations
  APPLY: Any necessary environment setup before implementation
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

<pattern_integration>
  <validated_pattern_application>
    APPLY: Pattern validation results from Step 4.5 pattern-analyzer analysis:
    - Use recommended PocketFlow pattern with confidence score and rationale
    - Apply validation results and optimization suggestions  
    - Follow specific node and flow recommendations for implementation
    - Consider integration requirements with existing patterns
    - Implementation guided by: [PATTERN_VALIDATION_FROM_STEP_4_5]
  </validated_pattern_application>
  
  <pattern_compliance_execution>
    INTEGRATE: Validated pattern recommendations into implementation phases
    OPTIMIZE: Task execution using pattern-specific best practices
    VALIDATE: Implementation follows recommended PocketFlow patterns
    ENSURE: Architecture decisions align with pattern validation results
  </pattern_compliance_execution>
</pattern_integration>

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
      **Phase 0: Schema Design** - Create Pydantic schemas and SharedStore validation
      **Phase 1: Utilities** - Implement utility functions with contracts from design.md  
      **Phase 2: FastAPI** - Create endpoints and middleware (if applicable)
      **Phase 3: PocketFlow Nodes** - Implement prep/exec/post lifecycle patterns
      **Phase 4: Flow Assembly** - Connect nodes matching design.md Mermaid diagram
      **Phase 5: Integration Testing** - Validate complete system and apply toolchain
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

<step number="5.5" subagent="template-validator" name="implementation_quality_validation">

### Step 5.5: Implementation Quality Validation

**Uses:** template-validator subagent for code quality validation

Use the template-validator subagent to validate the quality of implemented code, templates, and architecture compliance before proceeding to testing.

<subagent_context>
  **Context:** Implemented code, pattern compliance, framework standards, acceptance criteria
  **Output:** Quality validation results and improvement recommendations
  **Next Step:** Reliable test execution
</subagent_context>

**Blocking:** Must fix all quality issues before testing

<instructions>
  ACTION: Use template-validator subagent for implementation quality validation
  REQUEST: "Validate implementation quality for current task:
            - Code changes: [IMPLEMENTED_FILES_AND_CHANGES]
            - PocketFlow compliance: [PATTERN_ADHERENCE_CHECK]
            - Framework standards: [BEST_PRACTICES_COMPLIANCE]
            - Task requirements: [ACCEPTANCE_CRITERIA_VALIDATION]
            - Template quality: [STRUCTURE_AND_PLACEHOLDER_QUALITY]"
  PROCESS: Quality validation results and improvement recommendations
  BLOCK: Progression until quality standards are met
  APPLY: Required improvements before testing phase
</instructions>

</step>

<step number="6.5" subagent="test-runner" name="task_test_verification">

### Step 6.5: Task-Specific Test Verification

Use the test-runner subagent to run and verify only the tests specific to this parent task (not the full test suite) to ensure the feature is working correctly.

<subagent_context>
  **Context:** Task-specific test files and acceptance criteria
  **Output:** Test results, failure details, and remediation recommendations
  **Next Step:** Task completion in Step 8
</subagent_context>

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
  ACTION: Use test-runner subagent for task-specific test verification
  REQUEST: "Run tests for [this parent task's test files]"
  WAIT: For test-runner analysis
  PROCESS: Returned failure information
  VERIFY: 100% pass rate for task-specific tests
  CONFIRM: This feature's tests are complete
</instructions>

</step>

<step number="8" subagent="project-manager" name="task_status_updates">

### Step 8: Task Status Updates

**Uses:** project-manager subagent for comprehensive task tracking

Use the project-manager subagent to update task status and provide comprehensive progress reporting.

<subagent_context>
  **Context:** Task completion status, progress tracking, blocking issues
  **Output:** Updated tasks.md file and progress summary
  **Next Step:** Task completion notification
</subagent_context>

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
  ACTION: Use project-manager subagent for task status updates
  REQUEST: "Update task status and progress tracking:
            - Parent task: [CURRENT_TASK_NUMBER_AND_DESCRIPTION]
            - Subtasks completed: [LIST_OF_COMPLETED_SUBTASKS]
            - Implementation files: [FILES_CREATED_OR_MODIFIED]
            - Test results: [TASK_SPECIFIC_TEST_OUTCOMES]
            - Blocking issues: [ANY_UNRESOLVED_ISSUES]"
  PROCESS: Returned status update and progress analysis
  UPDATE: tasks.md after each task completion
  MARK: [x] for completed items immediately
  DOCUMENT: Blocking issues with ⚠️ emoji
  LIMIT: 3 attempts before marking as blocked
</instructions>

</step>

</process_flow>
