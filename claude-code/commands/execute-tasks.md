---
description: Task Execution Rules for Agent OS
globs:
alwaysApply: false
version: 2.0 # Major updates for PocketFlow integration
encoding: UTF-8
---

# Task Execution Rules

<ai_meta>
  <parsing_rules>
    - Process XML blocks first for structured data
    - Execute instructions in sequential order
    - Use templates as exact patterns
    - Request missing data rather than assuming
  </parsing_rules>
  <file_conventions>
    - encoding: UTF-8
    - line_endings: LF
    - indent: 2 spaces
    - markdown_headers: no indentation
  </file_conventions>
</ai_meta>

## Overview

<purpose>
  - Execute spec tasks systematically
  - Follow TDD development workflow
  - Ensure quality through testing and review
</purpose>

<context>
  - Part of Agent OS framework
  - Executed after spec planning is complete
  - Follows tasks defined in spec tasks.md
</context>

<prerequisites>
  - Spec documentation exists in @.agent-os/specs/
  - Tasks defined in spec's tasks.md
  - Development environment configured
  - Git repository initialized
</prerequisites>

<pre_flight_check>
  EXECUTE: @~/.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" name="task_assignment_and_understanding">

### Step 1: Task Assignment and Understanding

<step_metadata>
  <inputs>
    - spec_srd_reference: file path
    - specific_tasks: array[string] (optional)
  </inputs>
  <default>next uncompleted parent task(s)</default>
</step_metadata>

<task_selection>
  <explicit>user specifies exact task(s)</explicit>
  <implicit>find next uncompleted task(s) in tasks.md</implicit>
</task_selection>

<task_analysis>
  <read_from_tasks_md>
    - Parent task(s) description
    - All sub-task descriptions for selected tasks
    - Task dependencies and sequencing
    - Expected outcomes and deliverables
  </read_from_tasks_md>
</task_analysis>

<instructions>
  ACTION: Identify task(s) to execute and read all related sub-tasks
  DEFAULT: Select next uncompleted parent task(s) if not specified
  ANALYZE: Full scope of implementation required across selected tasks
  UNDERSTAND: Dependencies and expected deliverables
  NOTE: Test requirements for each sub-task
  CONFIRM: Task selection with user
</instructions>

</step>

<step number="2" name="context_analysis">

### Step 2: Context Analysis

<step_metadata>
  <reads>
    - spec SRD file
    - spec tasks.md
    - all files in spec sub-specs/ folder
    - @.agent-os/product/mission.md
    - @.agent-os/product/tech-stack.md # Added for LLM/AI check
  </reads>
  <purpose>complete understanding of requirements</purpose>
</step_metadata>

<context_gathering>
  <spec_level>
    - requirements from SRD
    - technical specs
    - test specifications
  </spec_level>
  <product_level>
    - overall mission alignment
    - technical standards
    - best practices
    - PocketFlow Principles (if LLM/AI involved)
  </product_level>
  <stack_specific_checks>
    - Verify Pydantic models in `schemas/` directory
    - Check existing FastAPI routes and middleware
    - Identify FastMCP tools already implemented
    - Review current utility functions in `utils/`
    - Assess PocketFlow nodes and flows (if applicable)
  </stack_specific_checks>
</context_gathering>

<instructions>
  ACTION: Read all spec documentation thoroughly
  ANALYZE: Requirements and specifications for current task
  UNDERSTAND: How task fits into overall spec goals, paying special attention to LLM/AI components and PocketFlow patterns.
</instructions>

</step>

<step number="2.5" name="design_document_validation">

### Step 2.5: Design Document Validation (LLM/AI Components Only)

<step_metadata>
  <validates>docs/design.md existence and completeness</validates>
  <blocks>implementation without proper design</blocks>
  <condition>only if LLM/AI components detected</condition>
</step_metadata>

<validation_requirements>
  <file_existence>
    <path>docs/design.md</path>
    <required>true</required>
    <blocking>implementation cannot proceed without this file</blocking>
  </file_existence>
  <content_validation>
    - Requirements section with problem statement and success criteria
    - Flow Design with Mermaid diagram and node sequence
    - Utilities section with input/output contracts for all functions
    - Data Design with complete SharedStore schema
    - Node Design with prep/exec/post specifications for all nodes
  </content_validation>
  <quality_checks>
    - Mermaid diagram syntax validation
    - All utility functions have specified input/output types
    - SharedStore schema includes all data transformations
    - Node action strings are clearly defined
    - Error handling and retry strategies documented
  </quality_checks>
</validation_requirements>

<conditional_execution>
  <detection_criteria>
    - Check @.agent-os/product/tech-stack.md for PocketFlow or LLM framework
    - Look for LLM-related tasks in spec tasks.md
    - Identify mentions of nodes.py, flow.py, or utils/ in technical specs
    - Check for AI/ML-related dependencies or requirements
  </detection_criteria>
  <if_llm_detected>
    <action>Execute full validation process</action>
    <blocking>true - cannot proceed without complete design.md</blocking>
  </if_llm_detected>
  <if_no_llm>
    <action>Skip this step entirely</action>
    <message>Skipping design document validation - no LLM/AI components detected</message>
  </if_no_llm>
</conditional_execution>

<validation_process>
  <step1>Check if tech stack includes PocketFlow or LLM/AI components</step1>
  <step2>If LLM/AI components detected, verify docs/design.md exists</step2>
  <step3>Read and validate all required sections are present and complete</step3>
  <step4>Validate Mermaid diagram syntax if present</step4>
  <step5>Ensure all utility functions have input/output contracts</step5>
  <step6>Block progression if validation fails</step6>
</validation_process>

<blocking_message>
  ❌ **Design Document Required**
  
  This task involves LLM/AI components but `docs/design.md` is missing or incomplete.
  
  **Missing/Incomplete Sections:**
  - [LIST_MISSING_SECTIONS]
  
  **Required Actions:**
  1. Create or complete `docs/design.md` using the PocketFlow template
  2. Ensure all sections are filled with specific details
  3. Validate Mermaid diagrams are syntactically correct
  4. Specify input/output contracts for all utility functions
  
  Implementation cannot proceed without a complete design document.
  Please create the design document first or ask me to help create it.
</blocking_message>

<instructions>
  DETECT: Check multiple sources to determine if LLM/AI components involved
  CONDITIONAL: Skip entirely if no LLM/AI components detected
  VALIDATE: docs/design.md exists and is complete if LLM/AI components present
  BLOCK: Implementation progression if design document missing or incomplete
  MESSAGE: Clearly indicate whether step was executed or skipped
  GUIDE: User to create proper design documentation before proceeding
</instructions>

</step>

<step number="2.7" subagent="context-fetcher" name="best_practices_review">

### Step 2.7: Best Practices Review

<step_metadata>
  <uses>context-fetcher subagent</uses>
  <targets>@~/.agent-os/standards/best-practices.md</targets>
  <purpose>selective context loading for current tasks</purpose>
</step_metadata>

Use the context-fetcher subagent to retrieve relevant sections from @~/.agent-os/standards/best-practices.md that apply to the current task's technology stack and feature type.

<selective_reading>
  <search_best_practices>
    FIND sections relevant to:
    - Task's technology stack
    - PocketFlow patterns if applicable
    - Testing approaches needed
    - Code organization patterns
  </search_best_practices>
</selective_reading>

<instructions>
  ACTION: Use context-fetcher subagent
  REQUEST: "Find best practices sections relevant to:
            - Task's technology stack: [CURRENT_TECH]
            - Feature type: [CURRENT_FEATURE_TYPE]
            - PocketFlow patterns: [IF_APPLICABLE]
            - Testing approaches needed
            - Code organization patterns"
  PROCESS: Returned best practices
  APPLY: Relevant patterns to implementation
</instructions>

</step>

<step number="2.8" subagent="context-fetcher" name="code_style_review">

### Step 2.8: Code Style Review

<step_metadata>
  <uses>context-fetcher subagent</uses>
  <targets>@~/.agent-os/standards/code-style.md</targets>
  <purpose>selective style rules loading</purpose>
</step_metadata>

Use the context-fetcher subagent to retrieve relevant code style rules from @~/.agent-os/standards/code-style.md for the languages and file types being used in this task.

<selective_reading>
  <search_code_style>
    FIND style rules for:
    - Languages used in this task
    - File types being modified
    - PocketFlow patterns being implemented
    - Testing style guidelines
  </search_code_style>
</selective_reading>

<instructions>
  ACTION: Use context-fetcher subagent
  REQUEST: "Find code style rules for:
            - Languages: [LANGUAGES_IN_TASK]
            - File types: [FILE_TYPES_BEING_MODIFIED]
            - PocketFlow patterns: [PATTERNS_BEING_IMPLEMENTED]
            - Testing style guidelines"
  PROCESS: Returned style rules
  APPLY: Relevant formatting and patterns
</instructions>

</step>

<step number="3" name="implementation_planning">

### Step 3: Implementation Planning

<step_metadata>
  <creates>execution plan</creates>
  <requires>user approval</requires>
</step_metadata>

<plan_structure>
  <format>numbered list with sub-bullets</format>
  <includes>
    - all subtasks from tasks.md
    - implementation approach following proper phase sequence
    - dependencies to install
    - test strategy with type safety validation
  </includes>
  <phase_sequence>
    - **Phase 0**: Create Pydantic schemas with validation (if needed)
    - **Phase 1**: Implement utility functions with type hints
    - **Phase 2**: Create FastAPI endpoints (if applicable)
    - **Phase 3**: Implement PocketFlow nodes (for LLM/AI)
    - **Phase 4**: Assemble PocketFlow flows (for LLM/AI)
    - **Phase 5**: Integration and testing
  </phase_sequence>
  <type_safety_planning>
    - Plan Pydantic model creation before feature implementation
    - Design FastAPI endpoint structure with proper async patterns
    - Include API → PocketFlow Flow → Response integration pattern
    - Ensure all functions have complete type hints
    - Validate schema enforcement at all boundaries
  </type_safety_planning>
  <pocketflow_specifics>
    - **If LLM/AI components are involved:**
      - Reference design.md for implementation guidance
      - Follow PocketFlow sequence: Utilities first, then Nodes, then Flows
      - Plan for SharedStore schema implementation
      - Explicit mention of PocketFlow Nodes, Flows, and Shared Store interactions
      - Outline of `prep`, `exec`, `post` logic for each relevant Node
      - Details on `utils/` function creation/usage
      - Plan for structured output (YAML/JSON) if applicable
      - Approach for handling chat history, caching, logging for LLM calls
      - Considerations for BatchNode/BatchFlow for large inputs/parallelization
  </pocketflow_specifics>
</plan_structure>

<plan_template>
  ## Implementation Plan for [TASK_NAME]

  1. **[MAJOR_STEP_1]**
     - [SPECIFIC_ACTION]
     - [SPECIFIC_ACTION]

  2. **[MAJOR_STEP_2]**
     - [SPECIFIC_ACTION]
     - [SPECIFIC_ACTION]

  **Dependencies to Install:**
  - [LIBRARY_NAME] - [PURPOSE]

  **Test Strategy:**
  - [TEST_APPROACH]
</plan_template>

<approval_request>
  I've prepared the above implementation plan.
  Please review and confirm before I proceed with execution.
</approval_request>

<instructions>
  ACTION: Create detailed execution plan following proper phase sequence
  STRUCTURE: Follow Phase 0→1→2→3→4→5 progression for implementation
  REFERENCE: design.md for LLM/AI components to guide implementation
  PLAN: Type safety validation and Pydantic model creation upfront
  DISPLAY: Plan to user for review
  WAIT: For explicit approval before proceeding
  BLOCK: Do not proceed without affirmative permission
  DETAIL: PocketFlow specifics and phase sequencing if LLM/AI components are present
</instructions>

</step>

<step number="4" name="development_server_check">

### Step 4: Check for Development Server

<step_metadata>
  <checks>running development server</checks>
  <prevents>port conflicts</prevents>
</step_metadata>

<server_check_flow>
  <if_running>
    ASK user to shut down
    WAIT for response
  </if_running>
  <if_not_running>
    PROCEED immediately
  </if_not_running>
</server_check_flow>

<user_prompt>
  A development server is currently running.
  Should I shut it down before proceeding? (yes/no)
</user_prompt>

<instructions>
  ACTION: Check for running local development server
  CONDITIONAL: Ask permission only if server is running
  PROCEED: Immediately if no server detected
</instructions>

</step>

<step number="5" name="git_branch_management">

### Step 5: Git Branch Management

<step_metadata>
  <manages>git branches</manages>
  <ensures>proper isolation</ensures>
</step_metadata>

<branch_naming>
  <source>spec folder name</source>
  <format>exclude date prefix</format>
  <example>
    - folder: 2025-03-15-password-reset
    - branch: password-reset
  </example>
</branch_naming>

<branch_logic>
  <case_a>
    <condition>current branch matches spec name</condition>
    <action>PROCEED immediately</action>
  </case_a>
  <case_b>
    <condition>current branch is main/staging/review</condition>
    <action>CREATE new branch and PROCEED</action>
  </case_b>
  <case_c>
    <condition>current branch is different feature</condition>
    <action>ASK permission to create new branch</action>
  </case_c>
</branch_logic>

<case_c_prompt>
  Current branch: [CURRENT_BRANCH]
  This spec needs branch: [SPEC_BRANCH]

  May I create a new branch for this spec? (yes/no)
</case_c_prompt>

<instructions>
  ACTION: Check current git branch
  EVALUATE: Which case applies
  EXECUTE: Appropriate branch action
  WAIT: Only for case C approval
</instructions>

</step>

<step number="5" name="task_execution_loop">

### Step 5: Task Execution Loop

<step_metadata>
  <purpose>Execute all parent tasks using individual task processor</purpose>
  <delegates>execute-task.md for actual implementation</delegates>
  <manages>task orchestration and progress tracking</manages>
  <references>@~/.agent-os/shared/execution_utils.md for shared patterns</references>
</step_metadata>

<task_execution_workflow>
  <preparation>
    LOAD: @~/.agent-os/instructions/core/execute-task.md instructions ONCE
    IDENTIFY: All parent tasks selected for execution
    PREPARE: Shared execution context for consistency
  </preparation>
  
  <execution_loop>
    FOR each parent_task in selected_tasks:
      <task_invocation>
        CONTEXT: {
          parent_task_number: "Task X",
          parent_task_description: "task description from tasks.md", 
          subtasks: ["X.1", "X.2", "X.3", ...],
          project_type: "pocketflow|standard|graphrag",
          shared_context: minimal_project_state,
          execution_mode: "orchestrated"
        }
        
        INVOKE: execute-task.md with task_context
        METHOD: Use Task tool to delegate execution
        WAIT: For task completion confirmation
      </task_invocation>
      
      <progress_tracking>
        UPDATE: tasks.md with completion status
        VALIDATE: Task completion meets acceptance criteria
        REPORT: Progress to user with clear status
      </progress_tracking>
      
      <error_handling>
        IF task_fails:
          CAPTURE: Detailed error context from execute-task.md
          OFFER: Options to retry, skip, or abort workflow
          PRESERVE: Progress of completed tasks
        END_IF
      </error_handling>
    END_FOR
  </execution_loop>
</task_execution_workflow>

<context_management>
  <efficiency_strategy>
    - Load execute-task.md context once, reuse for all tasks
    - Pass minimal context per task to reduce token usage
    - Clear task-specific context after each completion
    - Maintain only essential workflow state between tasks
  </efficiency_strategy>
  
  <shared_state>
    - Project configuration (tech stack, standards)
    - Current branch and git state
    - Overall progress tracking
    - Error recovery information
  </shared_state>
</context_management>

<instructions>
  ACTION: Load execute-task.md instructions once for efficiency
  LOOP: Through each parent task systematically
  DELEGATE: All actual implementation to execute-task.md
  COORDINATE: Task sequence and dependencies
  TRACK: Progress and handle failures gracefully
  MAINTAIN: Clean separation between orchestration and execution
</instructions>

</step>

<step number="6" name="final_validation">

### Step 6: Final Validation & Workflow Completion

<step_metadata>
  <validates>overall workflow completion</validates>
  <confirms>all tasks completed successfully</confirms>
  <purpose>workflow finalization and cleanup</purpose>
</step_metadata>

<workflow_validation>
  <task_completion_check>
    VERIFY: All selected parent tasks marked as [COMPLETED] in tasks.md
    CONFIRM: No tasks remain in [IN_PROGRESS] or [FAILED] status
    VALIDATE: Each completed task meets acceptance criteria
  </task_completion_check>
  
  <integration_verification>
    RUN: Full test suite to ensure all components work together
    CHECK: All PocketFlow integrations function correctly (if applicable)
    VALIDATE: Code quality standards met (ruff, ty checks pass)
    CONFIRM: No critical errors or warnings remain
  </integration_verification>
  
  <documentation_check>
    VERIFY: All implementation matches specifications
    UPDATE: Documentation reflects any implementation decisions
    CONFIRM: Design documents align with final implementation (if LLM/AI components)
  </documentation_check>
</workflow_validation>

<completion_reporting>
  <progress_summary>
    REPORT: Total tasks completed vs planned
    HIGHLIGHT: Key features implemented
    DOCUMENT: Any deviations from original plan
    NOTE: Performance metrics and quality indicators
  </progress_summary>
  
  <next_steps_guidance>
    SUGGEST: Appropriate next actions for user
    RECOMMEND: Testing procedures or deployment steps
    IDENTIFY: Any follow-up tasks or improvements
  </next_steps_guidance>
</completion_reporting>

<instructions>
  ACTION: Validate overall workflow completion
  CONFIRM: All tasks executed successfully via execute-task.md
  VERIFY: Integration and quality standards met
  REPORT: Comprehensive completion summary to user
  GUIDE: User on appropriate next steps
</instructions>

</step>

<conditional_execution>
  <detection_criteria>
    - Check if docs/design.md exists (indicates LLM/AI implementation)
    - Look for implemented nodes.py or flow.py files
    - Identify utils/ directory with LLM-related functions
    - Check for PocketFlow imports or usage in codebase
  </detection_criteria>
  <if_llm_implemented>
    <action>Execute full adherence validation</action>
    <blocking>true for major deviations from design</blocking>
  </if_llm_implemented>
  <if_no_llm_implementation>
    <action>Skip this step entirely</action>
    <message>Skipping design adherence check - no LLM/AI components implemented</message>
  </if_no_llm_implementation>
</conditional_execution>

<adherence_validation>
  <utility_functions>
    - Verify all utility functions match documented input/output contracts
    - Check function signatures align with design.md specifications
    - Validate error handling matches documented patterns
    - Ensure all promised utility functions are implemented
  </utility_functions>
  <shared_store_schema>
    - Validate SharedStore schema implementation matches design
    - Check all data transformations are properly defined
    - Verify Pydantic models align with schema specifications
    - Ensure consistent key naming throughout implementation
  </shared_store_schema>
  <node_implementation>
    - Verify each node's prep/exec/post logic matches design specifications
    - Check action strings match documented flow transitions
    - Validate node responsibilities align with design document
    - Ensure error handling converts to proper action strings
  </node_implementation>
  <flow_assembly>
    - Validate flow connections match Mermaid diagram
    - Check node transitions follow documented action strings
    - Verify error handling and retry strategies are implemented
    - Ensure integration points work as designed
  </flow_assembly>
</adherence_validation>

<validation_checklist>
  - [ ] All utility functions implemented with documented signatures
  - [ ] SharedStore schema matches design document
  - [ ] Node prep/exec/post methods follow design specifications
  - [ ] Flow assembly matches Mermaid diagram
  - [ ] Action strings and transitions implemented correctly
  - [ ] Error handling follows design patterns
  - [ ] Integration points work as documented
</validation_checklist>

<deviation_handling>
  <minor_deviations>
    - Document in implementation notes
    - Update design.md if improvement discovered
    - Ensure consistency across codebase
  </minor_deviations>
  <major_deviations>
    - Stop implementation
    - Discuss with user before proceeding
    - Update design.md first if changes needed
    - Re-validate entire approach
  </major_deviations>
</deviation_handling>

<instructions>
  DETECT: Check for LLM/AI implementation artifacts before executing
  CONDITIONAL: Skip entirely if no LLM/AI components were implemented
  VALIDATE: Implementation adheres to design.md specifications if LLM/AI present
  CHECK: All documented components are implemented correctly
  DOCUMENT: Any deviations from original design
  BLOCK: Major changes without design document updates
  MESSAGE: Clearly indicate whether step was executed or skipped
  ENSURE: Implementation consistency with documented design
</instructions>

</step>

<step number="7" name="task_status_updates">

### Step 7: Task Status Updates

<step_metadata>
  <updates>tasks.md file</updates>
  <timing>immediately after completion</timing>
</step_metadata>

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

<step number="7.5" subagent="test-runner" name="task_specific_test_verification">

### Step 7.5: Task-Specific Test Verification

<step_metadata>
  <uses>test-runner subagent</uses>
  <purpose>focused testing before full suite</purpose>
  <runs>only tests related to current tasks</runs>
</step_metadata>

Use the test-runner subagent to run and verify only the tests specific to the current tasks being worked on (not the full test suite) to ensure the features are working correctly.

<focused_test_execution>
  <run_only>
    - All new tests written for current tasks
    - All tests updated during these tasks
    - Tests directly related to implemented features
  </run_only>
  <skip>
    - Full test suite (done later in Step 8)
    - Unrelated test files
  </skip>
</focused_test_execution>

<final_verification>
  IF any test failures:
    - Debug and fix the specific issue
    - Re-run only the failed tests
  ELSE:
    - Confirm all task tests passing
    - Ready to proceed to full test suite
</final_verification>

<instructions>
  ACTION: Use test-runner subagent
  REQUEST: "Run tests for [current tasks' test files]"
  WAIT: For test-runner analysis
  PROCESS: Returned failure information
  VERIFY: 100% pass rate for task-specific tests
  CONFIRM: These features' tests are complete before full suite
</instructions>

</step>

<step number="8" name="test_suite_verification">

### Step 8: Run All Tests

<step_metadata>
  <runs>entire test suite</runs>
  <ensures>no regressions</ensures>
</step_metadata>

<test_execution>
  <order>
    1. Run Ruff for linting and formatting: `ruff check --fix . && ruff format .`
    2. Run ty for type checking: `uvx ty check`
    3. Verify new tests pass (using Pytest as specified in tech stack)
    4. Run entire test suite (using Pytest as specified in tech stack)
    5. Fix any failures
  </order>
  <requirement>100% pass rate for all checks</requirement>
</test_execution>

<failure_handling>
  <action>troubleshoot and fix</action>
  <priority>before proceeding</priority>
</failure_handling>

<instructions>
  ACTION: Run complete test suite, including linting, formatting, and type checking.
  VERIFY: All checks pass, including new tests.
  FIX: Any failures before continuing.
  BLOCK: Do not proceed with failing checks or tests.
</instructions>

</step>

<step number="8.5" name="type_safety_validation">

### Step 8.5: Type Safety Validation

<step_metadata>
  <validates>comprehensive type safety across codebase</validates>
  <ensures>Pydantic model enforcement</ensures>
  <checks>FastAPI documentation generation</checks>
  <condition>Python projects with modern type safety stack</condition>
</step_metadata>

<conditional_execution>
  <detection_criteria>
    - Check @.agent-os/product/tech-stack.md for Python 3.8+
    - Look for Pydantic usage in dependencies or code
    - Identify FastAPI framework usage
    - Check for type hints and mypy/ty configuration
    - Look for schemas/ directory with Pydantic models
  </detection_criteria>
  <if_modern_python_stack>
    <action>Execute comprehensive type safety validation</action>
    <blocking>true for type errors or validation failures</blocking>
  </if_modern_python_stack>
  <if_basic_python_or_other_lang>
    <action>Skip advanced validation, run basic type checking only</action>
    <message>Skipping comprehensive type safety validation - not using modern Python stack</message>
    <fallback>Run basic linting and available type checking</fallback>
  </if_basic_python_or_other_lang>
</conditional_execution>

<type_safety_checks>
  <function_type_hints>
    - Verify all functions have complete type hints for parameters and returns
    - Check no usage of bare `Any` types without justification
    - Validate Optional vs required parameter declarations
    - Ensure async functions properly typed with return types
  </function_type_hints>
  <pydantic_validation>
    - Test all Pydantic models validate correctly at boundaries
    - Verify validation rules work as expected with invalid data
    - Check custom validators function properly
    - Ensure model inheritance and composition work correctly
  </pydantic_validation>
  <fastapi_integration>
    - Validate automatic documentation generation works
    - Check request/response model integration
    - Test error response models return proper status codes
    - Verify dependency injection typing is correct
  </fastapi_integration>
  <shared_store_schema>
    - Validate SharedStore schema enforcement with Pydantic
    - Test data transformations maintain type consistency
    - Check no untyped dictionary access patterns
    - Ensure SharedStore keys follow naming conventions
  </shared_store_schema>
</type_safety_checks>

<validation_commands>
  <type_checking>
    <command>uvx ty check</command>
    <requirement>zero type errors</requirement>
    <fixes>address all type inconsistencies before proceeding</fixes>
  </type_checking>
  <pydantic_testing>
    <command>pytest -k "test_model" -v</command>
    <requirement>all model validation tests pass</requirement>
    <coverage>test both valid and invalid data scenarios</coverage>
  </pydantic_testing>
  <fastapi_docs>
    <validation>check /docs and /redoc endpoints load properly</validation>
    <schema>validate OpenAPI schema generation is complete</schema>
  </fastapi_docs>
</validation_commands>

<blocking_issues>
  <type_errors>
    - Any mypy/ty errors must be resolved
    - No bare Any types without explicit justification
    - All function signatures must be complete
  </type_errors>
  <model_failures>
    - Pydantic validation must work correctly
    - Custom validators must handle edge cases
    - Error messages must be user-friendly
  </model_failures>
  <api_documentation>
    - FastAPI docs must generate without errors
    - Request/response models must appear correctly
    - Example values must be meaningful
  </api_documentation>
</blocking_issues>

<instructions>
  DETECT: Check tech stack and dependencies for modern Python usage
  CONDITIONAL: Execute full validation for modern Python stack, basic checking otherwise
  VALIDATE: Comprehensive type safety if Pydantic/FastAPI detected
  RUN: All appropriate type checking and validation commands
  VERIFY: Pydantic models enforce boundaries correctly (if applicable)
  CHECK: FastAPI documentation generation works properly (if applicable)
  FALLBACK: Run basic linting and available type checking for non-modern stacks
  MESSAGE: Clearly indicate level of validation performed
  BLOCK: Progression if any applicable type safety issues detected
  FIX: All type errors before continuing to next step
</instructions>

</step>

<step number="9" name="git_workflow">

### Step 9: Git Workflow

<step_metadata>
  <creates>
    - git commit
    - github push
    - pull request
  </creates>
</step_metadata>

<commit_process>
  <commit>
    <message>descriptive summary of changes</message>
    <format>conventional commits if applicable</format>
  </commit>
  <push>
    <target>spec branch</target>
    <remote>origin</remote>
  </push>
  <pull_request>
    <title>descriptive PR title</title>
    <description>functionality recap</description>
  </pull_request>
</commit_process>

<pr_template>
  ## Summary

  [BRIEF_DESCRIPTION_OF_CHANGES]

  ## Changes Made

  - [CHANGE_1]
  - [CHANGE_2]

  ## Testing

  - [TEST_COVERAGE]
  - All tests passing ✓
</pr_template>

<instructions>
  ACTION: Commit all changes with descriptive message
  PUSH: To GitHub on spec branch
  CREATE: Pull request with detailed description
</instructions>

</step>

<step number="10" name="roadmap_progress_check">

### Step 10: Roadmap Progress Check

<step_metadata>
  <checks>@.agent-os/product/roadmap.md</checks>
  <updates>if spec completes roadmap item</updates>
</step_metadata>

<roadmap_criteria>
  <update_when>
    - spec fully implements roadmap feature
    - all related tasks completed
    - tests passing
  </update_when>
  <caution>only mark complete if absolutely certain</caution>
</roadmap_criteria>

<instructions>
  ACTION: Review roadmap.md for related items
  EVALUATE: If current spec completes roadmap goals
  UPDATE: Mark roadmap items complete if applicable
  VERIFY: Certainty before marking complete
</instructions>

</step>

<step number="11" name="completion_notification">

### Step 11: Task Completion Notification

<step_metadata>
  <plays>system sound</plays>
  <alerts>user of completion</alerts>
</step_metadata>

<notification_command>
  afplay /System/Library/Sounds/Glass.aiff
</notification_command>

<instructions>
  ACTION: Play completion sound
  PURPOSE: Alert user that task is complete
</instructions>

</step>

<step number="12" name="completion_summary">

### Step 12: Completion Summary

<step_metadata>
  <creates>summary message</creates>
  <format>structured with emojis</format>
</step_metadata>

<summary_template>
  ## ✅ What's been done

  1. **[FEATURE_1]** - [ONE_SENTENCE_DESCRIPTION]
  2. **[FEATURE_2]** - [ONE_SENTENCE_DESCRIPTION]

  ## ⚠️ Issues encountered

  [ONLY_IF_APPLICABLE]
  - **[ISSUE_1]** - [DESCRIPTION_AND_REASON]

  ## 👀 Ready to test in browser

  [ONLY_IF_APPLICABLE]
  1. [STEP_1_TO_TEST]
  2. [STEP_2_TO_TEST]

  ## 📦 Pull Request

  View PR: [GITHUB_PR_URL]
</summary_template>

<summary_sections>
  <required>
    - functionality recap
    - pull request info
  </required>
  <conditional>
    - issues encountered (if any)
    - testing instructions (if testable in browser)
  </conditional>
</summary_sections>

<instructions>
  ACTION: Create comprehensive summary
  INCLUDE: All required sections
  ADD: Conditional sections if applicable
  FORMAT: Use emoji headers for scannability
</instructions>

</step>

</process_flow>

## Development Standards

<standards>
  <code_style>
    <follow>@.agent-os/product/code-style.md</follow>
    <enforce>strictly</enforce>
  </code_style>
  <best_practices>
    <follow>@.agent-os/product/dev-best-practices.md</follow>
    <apply>all directives</apply>
  </best_practices>
  <testing>
    <coverage>comprehensive</coverage>
    <approach>test-driven development</approach>
  </testing>
  <documentation>
    <commits>clear and descriptive</commits>
    <pull_requests>detailed descriptions</pull_requests>
  </documentation>
</standards>

## Error Handling

<error_protocols>
  <blocking_issues>
    - document in tasks.md
    - mark with ⚠️ emoji
    - include in summary
  </blocking_issues>
  <test_failures>
    - fix before proceeding
    - never commit broken tests
  </test_failures>
  <technical_roadblocks>
    - attempt 3 approaches
    - document if unresolved
    - seek user input
  </technical_roadblocks>
</error_protocols>

<final_checklist>
  <verify>
    - [ ] Task implementation complete
    - [ ] All tests passing
    - [ ] tasks.md updated
    - [ ] Code committed and pushed
    - [ ] Pull request created
    - [ ] Roadmap checked/updated
    - [ ] Summary provided to user
  </verify>
</final_checklist>

## Orchestration Integration

@include orchestration/orchestrator-hooks.md

This instruction integrates with the orchestrator system for coordinated task execution.