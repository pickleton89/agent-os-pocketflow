---
description: Task Execution Rules for Agent OS
globs:
alwaysApply: false
version: 2.1 # Updated to use 3-phase execution model from v1.4.1
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
    - PocketFlow Principles (universal architecture)
  </product_level>
  <stack_specific_checks>
    - Verify Pydantic models in `schemas/` directory
    - Check existing FastAPI routes and middleware
    - Identify FastMCP tools already implemented
    - Review current utility functions in `utils/`
    - Assess PocketFlow nodes and flows (universal architecture)
  </stack_specific_checks>
</context_gathering>

<instructions>
  ACTION: Read all spec documentation thoroughly
  ANALYZE: Requirements and specifications for current task
  UNDERSTAND: How task fits into overall spec goals and PocketFlow architecture patterns.
</instructions>

</step>

<step number="2.5" name="design_document_validation">

### Step 2.5: Design Document Validation (Universal)

<step_metadata>
  <validates>docs/design.md existence and completeness</validates>
  <blocks>implementation without proper design</blocks>
  <condition>universal for all projects</condition>
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

<universal_execution>
  <action>Execute full validation process for all projects</action>
  <blocking>true - cannot proceed without complete design.md</blocking>
  <rationale>All projects use PocketFlow architecture with appropriate patterns</rationale>
</universal_execution>

<validation_process>
  <step1>Verify docs/design.md exists for all projects</step1>
  <step2>Read and validate all required sections are present and complete</step2>
  <step3>Validate Mermaid diagram syntax if present</step3>
  <step4>Ensure all utility functions have input/output contracts</step4>
  <step5>Verify PocketFlow pattern selection and implementation plan</step5>
  <step6>Block progression if validation fails</step6>
</validation_process>

<blocking_message>
  ❌ **Design Document Required**
  
  This project uses PocketFlow architecture but `docs/design.md` is missing or incomplete.
  
  **Missing/Incomplete Sections:**
  - [LIST_MISSING_SECTIONS]
  
  **Required Actions:**
  1. Create or complete `docs/design.md` using the appropriate PocketFlow pattern template
  2. Ensure all sections are filled with specific details
  3. Validate Mermaid diagrams are syntactically correct
  4. Specify input/output contracts for all utility functions
  5. Define the PocketFlow pattern (WORKFLOW, TOOL, AGENT, RAG, etc.)
  
  Implementation cannot proceed without a complete design document.
  Please create the design document first or ask me to help create it.
</blocking_message>

<instructions>
  VALIDATE: docs/design.md exists and is complete for all projects
  BLOCK: Implementation progression if design document missing or incomplete
  VERIFY: PocketFlow pattern selection is appropriate for project type
  ENSURE: All required sections are present and detailed
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

<best_practices_retrieval_context>
  <context_to_provide>
    - Target file: @~/.agent-os/standards/best-practices.md
    - Current task technology stack and feature type
    - Testing and code organization requirements
    - PocketFlow patterns if applicable to project
  </context_to_provide>
  
  <expected_output>
    - Relevant best practices sections with source references
    - Technology-specific guidelines and testing approaches
    - Framework-specific best practices (if PocketFlow project)
  </expected_output>
  
  <required_for_next_step>
    Best practices inform implementation standards and quality requirements in Step 3
  </required_for_next_step>
</best_practices_retrieval_context>

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
  ACTION: Use context-fetcher subagent with complete context specification
  PROCESS: Returned best practices sections and guidelines
  APPLY: Relevant patterns and standards to implementation approach
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

<code_style_retrieval_context>
  <context_to_provide>
    - Target file: @~/.agent-os/standards/code-style.md
    - Programming languages and file types for current task
    - Component and testing conventions
    - PocketFlow patterns being implemented
  </context_to_provide>
  
  <expected_output>
    - Language-specific style rules and conventions
    - Component structure and testing style guidelines
    - Framework-specific styles (FastAPI, PocketFlow patterns)
  </expected_output>
  
  <required_for_next_step>
    Code style rules ensure consistent implementation in Step 3
  </required_for_next_step>
</code_style_retrieval_context>

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
  ACTION: Use context-fetcher subagent with complete context specification
  PROCESS: Returned style rules and conventions
  APPLY: Relevant formatting patterns and guidelines to implementation
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
    - **Phase 3**: Implement PocketFlow nodes (universal architecture)
    - **Phase 4**: Assemble PocketFlow flows (universal architecture)
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
    - **For all projects using PocketFlow architecture:**
      - Reference design.md for implementation guidance
      - Follow PocketFlow sequence: Utilities first, then Nodes, then Flows
      - Plan for SharedStore schema implementation
      - Explicit mention of PocketFlow Nodes, Flows, and Shared Store interactions
      - Outline of `prep`, `exec`, `post` logic for each relevant Node
      - Details on `utils/` function creation/usage
      - Plan for structured output (YAML/JSON) if applicable
      - Pattern-specific considerations (WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE)
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
  REFERENCE: design.md for all PocketFlow components to guide implementation
  PLAN: Type safety validation and Pydantic model creation upfront
  DISPLAY: Plan to user for review
  WAIT: For explicit approval before proceeding
  BLOCK: Do not proceed without affirmative permission
  DETAIL: PocketFlow specifics and phase sequencing for universal architecture
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

<step number="5.5" name="task_execution_loop">

### Step 5.5: Task Execution Loop

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
          LOG: Task failure with specific error details
          PRESERVE: Progress of completed tasks in tasks.md
          OFFER: Options to retry with enhanced context, skip task, or abort workflow
          DOCUMENT: Failure reason and attempted solutions
          IF retry_selected:
            - Re-run with additional debugging context
            - Limit to maximum 2 retry attempts per task
          ELSE_IF skip_selected:
            - Mark task as blocked with specific reason
            - Continue to next task if dependencies allow
          ELSE_IF abort_selected:
            - Terminate workflow with progress summary
            - Document incomplete tasks for future continuation
          END_IF
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

<step number="6" name="post_execution_workflow">

### Step 6: Post-Execution Workflow

<step_metadata>
  <delegates>post-execution-tasks.md for completion workflow</delegates>
  <handles>testing, git operations, documentation, and reporting</handles>
  <implements>3-phase execution model from Agent OS v1.4.1</implements>
</step_metadata>

After all tasks in tasks.md have been implemented, use @.agent-os/instructions/core/post-execution-tasks.md to run the complete series of steps we always execute when finishing and delivering a new feature.

<post_execution_workflow>
  <phase_model>
    **3-Phase Execution Model:**
    - **Pre-execution**: Context gathering and planning (Steps 1-5)
    - **Execution**: Task implementation (Step 5.5 loop)
    - **Post-execution**: Testing, validation, and delivery (this step)
  </phase_model>
  
  <delegated_responsibilities>
    The post-execution-tasks.md workflow handles:
    - PocketFlow implementation validation (universal requirement for all projects)
    - Full test suite execution
    - Git workflow and PR creation
    - Task completion verification
    - Roadmap progress updates
    - Enhanced recap document generation
    - Completion summary and notification
  </delegated_responsibilities>
</post_execution_workflow>

<enhanced_features>
  <pocketflow_validation>
    - Validates design.md compliance for all PocketFlow features
    - Checks PocketFlow pattern implementation
    - Verifies utility function contracts
    - Ensures Node/Flow structure correctness
  </pocketflow_validation>
  
  <enhanced_documentation>
    - Creates recaps with PocketFlow pattern details
    - Documents providers and models used (when applicable)
    - Includes design compliance status
    - Captures technical implementation details
  </enhanced_documentation>
</enhanced_features>

<instructions>
  ACTION: Delegate complete post-execution workflow
  EXECUTE: @.agent-os/instructions/core/post-execution-tasks.md
  WAIT: For full completion before concluding
  TRUST: Post-execution workflow to handle all finalization steps
  REPORT: Only final summary once post-execution completes
</instructions>

</step>

</process_flow>

<execution_summary>
  <workflow_phases>
    1. **Pre-execution** (Steps 1-5): Context gathering, validation, and preparation
    2. **Execution** (Step 5): Task implementation loop via execute-task.md  
    3. **Post-execution** (Step 6): Testing, validation, and delivery via post-execution-tasks.md
  </workflow_phases>
  
  <pocketflow_integration>
    - Design document validation ensures all features are properly planned
    - PocketFlow patterns are recognized and implemented correctly
    - Enhanced validation and documentation capture all implementation details
  </pocketflow_integration>
  
  <quality_assurance>
    - 3-phase model ensures systematic completion
    - Post-execution validation catches integration issues
    - Enhanced recap system provides better project tracking
  </quality_assurance>
</execution_summary>

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
    - Document in tasks.md with specific failure context
    - Mark with ⚠️ emoji and detailed error description
    - Include in summary with attempted solutions
    - Track resolution status for future attempts
  </blocking_issues>
  <test_failures>
    - Fix before proceeding to avoid broken state
    - Never commit failing tests to repository
    - Document test failure patterns for debugging
    - Retry test execution after fixes with full context
  </test_failures>
  <technical_roadblocks>
    - Attempt maximum 3 different approaches per issue
    - Document each approach and failure reason
    - Seek user input with specific technical questions
    - Preserve implementation context for manual resolution
  </technical_roadblocks>
  <subagent_failures>
    - Capture subagent error output and context
    - Attempt manual execution as fallback when possible
    - Document subagent availability issues
    - Continue workflow with degraded capability if non-critical
  </subagent_failures>
  <environment_issues>
    - Validate development environment setup
    - Document dependency or configuration problems
    - Attempt automatic fixes for common issues
    - Block progression on critical environment failures
  </environment_issues>
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