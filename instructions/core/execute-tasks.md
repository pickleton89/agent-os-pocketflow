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
    - **Execution**: Task implementation (Step 5 loop)
    - **Post-execution**: Testing, validation, and delivery (this step)
  </phase_model>
  
  <delegated_responsibilities>
    The post-execution-tasks.md workflow handles:
    - PocketFlow implementation validation (if LLM/AI components)
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
    - Validates design.md compliance for LLM/AI features
    - Checks PocketFlow pattern implementation
    - Verifies utility function contracts
    - Ensures Node/Flow structure correctness
  </pocketflow_validation>
  
  <enhanced_documentation>
    - Creates recaps with PocketFlow pattern details
    - Documents LLM providers and models used
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
    - Design document validation ensures LLM/AI features are properly planned
    - PocketFlow patterns are recognized and implemented correctly
    - Enhanced validation and documentation capture LLM/AI implementation details
  </pocketflow_integration>
  
  <quality_assurance>
    - 3-phase model ensures systematic completion
    - Post-execution validation catches integration issues
    - Enhanced recap system provides better project tracking
  </quality_assurance>
</execution_summary>