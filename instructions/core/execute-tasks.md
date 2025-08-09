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

<process_flow>

<step number="1" name="task_assignment">

### Step 1: Task Assignment

<step_metadata>
  <inputs>
    - spec_srd_reference: file path
    - specific_tasks: array[string] (optional)
  </inputs>
  <default>next uncompleted parent task</default>
</step_metadata>

<task_selection>
  <explicit>user specifies exact task(s)</explicit>
  <implicit>find next uncompleted task in tasks.md</implicit>
</task_selection>

<instructions>
  ACTION: Identify task(s) to execute
  DEFAULT: Select next uncompleted parent task if not specified
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

<step number="6" name="development_execution">

### Step 6: Development Execution

<step_metadata>
  <follows>approved implementation plan</follows>
  <adheres_to>all spec standards</adheres_to>
</step_metadata>

<execution_standards>
  <follow_exactly>
    - approved implementation plan
    - spec specifications
    - @.agent-os/product/code-style.md
    - @.agent-os/product/dev-best-practices.md
  </follow_exactly>
  <approach>test-driven development (TDD)</approach>
  <phase_based_execution>
    - **Phase 0**: Create Pydantic schemas with validation tests
    - **Phase 1**: Implement utility functions with standalone tests and type hints
    - **Phase 2**: Create FastAPI endpoints with proper async patterns (if applicable)
    - **Phase 3**: Implement PocketFlow nodes following lifecycle patterns
    - **Phase 4**: Assemble flow.py connecting nodes with action-based transitions
    - **Phase 5**: Integration testing and validation
  </phase_based_execution>
  <type_safety_enforcement>
    - All functions must have complete type hints
    - Pydantic models validate at all boundaries
    - FastAPI automatic documentation generation validated
    - SharedStore schema enforced with Pydantic models
    - No Any types without explicit justification
  </type_safety_enforcement>
  <pocketflow_coding_principles>
    - **For LLM/AI components:**
      - Follow design.md specifications exactly
      - Generate `utils/` functions first with input/output contracts
      - Implement `nodes.py` with `prep`, `exec`, `post` methods clearly separated
      - Define `shared` store schema using Pydantic models consistently
      - Assemble `flow.py` by connecting nodes with clear action-based transitions
      - **Apply comprehensive toolchain:** Use `ruff format`, `ruff check`, and `uvx ty check`
      - Implement error handling as action string routing (not try/catch inline)
      - Use Node retry mechanisms for error handling
      - Consider BatchNode/BatchFlow for iterative/parallel processing
      - Use provided LLM wrappers or create new ones in `utils/`
      - Add logging to LLM calls and node execution for debugging
      - Emphasize "Fail Fast" by avoiding excessive `try`/`except` during initial implementation
  </pocketflow_coding_principles>
</execution_standards>

<tdd_workflow>
  1. Write failing tests first
  2. Implement minimal code to pass
  3. Refactor while keeping tests green
  4. Repeat for each feature
</tdd_workflow>

<instructions>
  ACTION: Execute development plan systematically
  FOLLOW: All coding standards and specifications, including PocketFlow-specific principles for LLM components and explicit use of Ruff for code quality.
  IMPLEMENT: TDD approach throughout
  MAINTAIN: Code quality at every step
  Keep files modular and organized. No large monolithic files.
</instructions>

</step>

<step number="6.5" name="design_document_adherence_check">

### Step 6.5: Design Document Adherence Check (LLM/AI Components Only)

<step_metadata>
  <validates>implementation matches design.md specifications</validates>
  <ensures>design-implementation consistency</ensures>
  <condition>only if LLM/AI components implemented</condition>
</step_metadata>

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