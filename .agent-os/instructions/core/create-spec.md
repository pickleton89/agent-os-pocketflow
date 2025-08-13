---
description: Spec Creation Rules for Agent OS
globs:
alwaysApply: false
version: 2.0
encoding: UTF-8
---

# Spec Creation Rules

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
  - Create detailed spec plans for specific features
  - Generate structured documentation for implementation
  - Ensure alignment with product roadmap and mission
</purpose>

<context>
  - Part of Agent OS framework
  - Executed when implementing roadmap items
  - Creates spec-specific documentation
</context>

<prerequisites>
  - Product documentation exists in .agent-os/product/
  - Access to:
    - @.agent-os/product/mission.md,
    - @.agent-os/product/roadmap.md,
    - @.agent-os/product/tech-stack.md
  - User has spec idea or roadmap reference
</prerequisites>

## Template References

This instruction file uses modular templates from:
- **PocketFlow Templates:** @templates/pocketflow-templates.md
- **FastAPI Templates:** @templates/fastapi-templates.md  
- **Task Templates:** @templates/task-templates.md

<process_flow>

<step number="1" name="spec_initiation">

### Step 1: Spec Initiation

<step_metadata>
  <trigger_options>
    - option_a: user_asks_whats_next
    - option_b: user_provides_specific_spec
  </trigger_options>
</step_metadata>

<option_a_flow>
  <trigger_phrases>
    - "what's next?"
    - "what should we work on next?"
  </trigger_phrases>
  <actions>
    1. CHECK @.agent-os/product/roadmap.md
    2. FIND next uncompleted item
    3. SUGGEST item to user
    4. WAIT for approval
  </actions>
</option_a_flow>

<option_b_flow>
  <trigger>user describes specific spec idea</trigger>
  <accept>any format, length, or detail level</accept>
  <proceed>to context gathering</proceed>
</option_b_flow>

<instructions>
  ACTION: Identify spec initiation method
  ROUTE: Follow appropriate flow based on trigger
  WAIT: Ensure user agreement before proceeding
</instructions>

</step>

<step number="2" name="context_gathering">

### Step 2: Context Gathering

<step_metadata>
  <reads>
    - @.agent-os/product/mission.md
    - @.agent-os/product/roadmap.md
    - @.agent-os/product/tech-stack.md
  </reads>
  <purpose>understand spec alignment</purpose>
</step_metadata>

<context_analysis>
  <mission>overall product vision</mission>
  <roadmap>current progress and plans</roadmap>
  <tech_stack>technical requirements</tech_stack>
  <llm_integration_check>determine if spec involves LLM/AI components</llm_integration_check>
</context_analysis>

<instructions>
  ACTION: Read all three product documents
  ANALYZE: Spec alignment with each document
  NOTE: Consider implications for implementation, especially LLM integration.
</instructions>

</step>

<step number="3" name="requirements_clarification">

### Step 3: Requirements Clarification

<step_metadata>
  <required_clarifications>
    - scope_boundaries: string
    - technical_considerations: array[string]
  </required_clarifications>
</step_metadata>

<clarification_areas>
  <scope>
    - in_scope: what is included
    - out_of_scope: what is excluded (optional)
  </scope>
  <technical>
    - functionality specifics
    - UI/UX requirements
    - integration points
  </technical>
  <llm_specifics>
    - **For LLM/AI components:**
      - Desired PocketFlow design pattern (Agent, Workflow, RAG, MapReduce, Multi-Agent, Structured Output)
      - Specific LLM models/providers to use (if not already in tech stack)
      - Data sources for RAG or knowledge base
      - Expected input/output formats (structured output considerations)
      - Latency or throughput requirements
  </llm_specifics>
</clarification_areas>

<decision_tree>
  IF clarification_needed:
    ASK numbered_questions
    WAIT for_user_response
  ELSE:
    PROCEED to_date_determination
</decision_tree>

<question_template>
  Based on the spec description, I need clarification on:

  1. [SPECIFIC_QUESTION_ABOUT_SCOPE]
  2. [SPECIFIC_QUESTION_ABOUT_TECHNICAL_APPROACH]
  3. [SPECIFIC_QUESTION_ABOUT_USER_EXPERIENCE]
  [ADD_LLM_QUESTIONS_IF_APPLICABLE]
</question_template>

<instructions>
  ACTION: Evaluate need for clarification
  ASK: Numbered questions if needed
  PROCEED: Only with clear requirements
  PRIORITIZE: LLM-specific questions if the spec involves AI/LLM components.
</instructions>

</step>

<step number="4" name="date_determination">

### Step 4: Date Determination

<step_metadata>
  <purpose>Ensure accurate date for folder naming</purpose>
  <priority>high</priority>
  <creates>temporary file for timestamp</creates>
</step_metadata>

<date_determination_process>
  <primary_method>
    <name>File System Timestamp</name>
    <process>
      1. CREATE directory if not exists: .agent-os/specs/
      2. CREATE temporary file: .agent-os/specs/.date-check
      3. READ file creation timestamp from filesystem
      4. EXTRACT date in YYYY-MM-DD format
      5. DELETE temporary file
      6. STORE date in variable for folder naming
    </process>
  </primary_method>

  <fallback_method>
    <trigger>if file system method fails</trigger>
    <name>User Confirmation</name>
    <process>
      1. STATE: "I need to confirm today's date for the spec folder"
      2. ASK: "What is today's date? (YYYY-MM-DD format)"
      3. WAIT for user response
      4. VALIDATE format matches YYYY-MM-DD
      5. STORE date for folder naming
    </process>
  </fallback_method>
</date_determination_process>

<validation>
  <format_check>^\d{4}-\d{2}-\d{2}$</format_check>
  <reasonableness_check>
    - year: 2024-2030
    - month: 01-12
    - day: 01-31
  </reasonableness_check>
</validation>

<error_handling>
  IF date_invalid:
    USE fallback_method
  IF both_methods_fail:
    ERROR "Unable to determine current date"
</error_handling>

<instructions>
  ACTION: Determine accurate date using file system
  FALLBACK: Ask user if file system method fails
  VALIDATE: Ensure YYYY-MM-DD format
  STORE: Date for immediate use in next step
</instructions>

</step>

<step number="4.5" name="mandatory_design_document_creation">

### Step 4.5: Mandatory Design Document Creation (LLM/AI Features Only)

<step_metadata>
  <creates>
    - file: docs/design.md
  </creates>
  <condition>only if spec involves LLM/AI components</condition>
  <priority>critical - blocks implementation progression</priority>
</step_metadata>

<design_document_requirement>
  <philosophy>
    Following PocketFlow's "Agentic Coding" methodology: **Humans design, agents code**.
    Design must be completed before any implementation begins.
  </philosophy>
  <blocking_condition>
    Implementation tasks CANNOT proceed without completed design.md
  </blocking_condition>
</design_document_requirement>

<template_reference>
  **Template:** Use complete design document template from @templates/pocketflow-templates.md
  **Sections Required:**
  - Requirements (with design pattern classification)
  - Flow Design (with Mermaid diagram)
  - Utilities (with input/output contracts)
  - Data Design (SharedStore schema)
  - Node Design (prep/exec/post specifications)
</template_reference>

<validation_requirements>
  <must_complete>
    - [ ] Requirements section filled with specific details
    - [ ] Mermaid diagram created and validated
    - [ ] All utility functions specified with input/output contracts
    - [ ] SharedStore schema defined completely
    - [ ] Each node's prep/exec/post logic detailed
    - [ ] Error handling and retry strategies specified
    - [ ] Integration points identified
  </must_complete>
</validation_requirements>

<instructions>
  ACTION: Create docs/design.md using PocketFlow template
  TEMPLATE: @templates/pocketflow-templates.md (Design Document Template)
  BLOCK: Do not proceed to implementation steps without completed design
  VALIDATE: Ensure all sections are filled with specific details
  EMPHASIZE: This is the foundation for all subsequent implementation
</instructions>

</step>

<step number="5" name="spec_folder_creation">

### Step 5: Spec Folder Creation

<step_metadata>
  <creates>
    - directory: .agent-os/specs/YYYY-MM-DD-spec-name/
  </creates>
  <uses>date from step 4</uses>
</step_metadata>

<folder_naming>
  <format>YYYY-MM-DD-spec-name</format>
  <date>use stored date from step 4</date>
  <name_constraints>
    - max_words: 5
    - style: kebab-case
    - descriptive: true
  </name_constraints>
</folder_naming>

<example_names>
  - 2025-03-15-password-reset-flow
  - 2025-03-16-user-profile-dashboard
  - 2025-03-17-api-rate-limiting
</example_names>

<instructions>
  ACTION: Create spec folder using stored date
  FORMAT: Use kebab-case for spec name
  LIMIT: Maximum 5 words in name
  VERIFY: Folder created successfully
</instructions>

</step>

<step number="6" name="create_spec_md">

### Step 6: Create spec.md

<step_metadata>
  <creates>
    - file: .agent-os/specs/YYYY-MM-DD-spec-name/spec.md
  </creates>
</step_metadata>

<file_template>
  <header>
    # Spec Requirements Document

    > Spec: [SPEC_NAME]
    > Created: [CURRENT_DATE]
    > Status: Planning
  </header>
  <required_sections>
    - Overview
    - User Stories  
    - Spec Scope
    - Out of Scope
    - Expected Deliverable
    - API & Data Models
    - LLM Workflow (if applicable)
  </required_sections>
</file_template>

<section_templates>
  <overview>
    ## Overview
    [1-2_SENTENCE_GOAL_AND_OBJECTIVE]
  </overview>
  
  <user_stories>
    ## User Stories
    ### [STORY_TITLE]
    As a [USER_TYPE], I want to [ACTION], so that [BENEFIT].
    [DETAILED_WORKFLOW_DESCRIPTION]
  </user_stories>

  <spec_scope>
    ## Spec Scope
    1. **[FEATURE_NAME]** - [ONE_SENTENCE_DESCRIPTION]
    2. **[FEATURE_NAME]** - [ONE_SENTENCE_DESCRIPTION]
  </spec_scope>

  <out_of_scope>
    ## Out of Scope
    - [EXCLUDED_FUNCTIONALITY_1]
    - [EXCLUDED_FUNCTIONALITY_2]
  </out_of_scope>

  <expected_deliverable>
    ## Expected Deliverable
    1. [TESTABLE_OUTCOME_1]
    2. [TESTABLE_OUTCOME_2]
  </expected_deliverable>

  <api_data_models>
    **Template:** Use API & Data Models template from @templates/fastapi-templates.md
    **Include:** FastAPI endpoints, Pydantic models, error handling, PocketFlow integration
  </api_data_models>

  <llm_workflow>
    **Template:** Use LLM Workflow template from @templates/pocketflow-templates.md  
    **Condition:** Only if spec involves LLM/AI components
    **Include:** PocketFlow architecture, node specifications, design patterns
  </llm_workflow>
</section_templates>

<instructions>
  ACTION: Create spec.md with all sections
  TEMPLATES: Use referenced templates for complex sections
  FILL: Use spec details from steps 1-3
  MAINTAIN: Clear, concise descriptions
</instructions>

</step>

<step number="7" name="create_technical_spec">

### Step 7: Create Technical Specification

<step_metadata>
  <creates>
    - directory: sub-specs/
    - file: sub-specs/technical-spec.md
  </creates>
</step_metadata>

<file_template>
  <header>
    # Technical Specification

    This is the technical specification for the spec detailed in @.agent-os/specs/YYYY-MM-DD-spec-name/spec.md

    > Created: [CURRENT_DATE]
    > Version: 1.0.0
  </header>
</file_template>

<spec_sections>
  <technical_requirements>
    - functionality details
    - UI/UX specifications
    - integration requirements
    - performance criteria
  </technical_requirements>
  <approach_options>
    - multiple approaches (if applicable)
    - selected approach
    - rationale for selection
  </approach_options>
  <external_dependencies>
    - new libraries/packages
    - justification for each
    - version requirements
  </external_dependencies>
  <pydantic_fastapi_sections>
    **Templates:** Use Pydantic and FastAPI templates from @templates/fastapi-templates.md
    **Include:** Schema specifications, route organization, error handling
  </pydantic_fastapi_sections>
  <pocketflow_sections>
    **Templates:** Use utility, SharedStore, and node templates from @templates/pocketflow-templates.md
    **Condition:** Only if spec involves LLM/AI components
    **Include:** Utility specifications, SharedStore schema, node implementations
  </pocketflow_sections>
</spec_sections>

<instructions>
  ACTION: Create sub-specs folder and technical-spec.md
  TEMPLATES: Use referenced templates for detailed sections
  DOCUMENT: All technical decisions and requirements
  JUSTIFY: Any new dependencies
</instructions>

</step>

<step number="8" name="create_database_schema">

### Step 8: Create Database Schema (Conditional)

<step_metadata>
  <creates>
    - file: sub-specs/database-schema.md
  </creates>
  <condition>only if database changes needed</condition>
</step_metadata>

<decision_tree>
  IF spec_requires_database_changes:
    CREATE sub-specs/database-schema.md
  ELSE:
    SKIP this_step
</decision_tree>

<schema_template>
  # Database Schema
  
  ## Changes
  - new tables
  - new columns
  - modifications
  - migrations

  ## Specifications
  - exact SQL or migration syntax
  - indexes and constraints
  - foreign key relationships

  ## Rationale
  - reason for each change
  - performance considerations
  - data integrity rules
</schema_template>

<instructions>
  ACTION: Check if database changes needed
  CREATE: database-schema.md only if required
  INCLUDE: Complete SQL/migration specifications
</instructions>

</step>

<step number="9" name="create_api_spec">

### Step 9: Create API Specification (Conditional)

<step_metadata>
  <creates>
    - file: sub-specs/api-spec.md
  </creates>
  <condition>only if API changes needed</condition>
</step_metadata>

<decision_tree>
  IF spec_requires_api_changes:
    CREATE sub-specs/api-spec.md using FastAPI template
  ELSE:
    SKIP this_step
</decision_tree>

<template_reference>
  **Template:** Use complete API specification template from @templates/fastapi-templates.md
  **Include:** FastAPI endpoints, Pydantic models, PocketFlow integration, status codes
</template_reference>

<instructions>
  ACTION: Check if API changes needed
  CREATE: api-spec.md only if required using FastAPI template
  DOCUMENT: All endpoints and controllers with proper patterns
</instructions>

</step>

<step number="10" name="create_tests_spec">

### Step 10: Create Tests Specification

<step_metadata>
  <creates>
    - file: sub-specs/tests.md
  </creates>
</step_metadata>

<test_template>
  # Tests Specification
  
  ## Test Coverage
  ### Unit Tests
  - model tests
  - service tests
  - helper tests
  
  ### Integration Tests
  - controller tests
  - API tests
  - workflow tests
  
  ### Feature Tests
  - end-to-end scenarios
  - user workflows
  
  ### Mocking Requirements
  - external services
  - API responses
  - time-based tests
  
  ### LLM-Specific Tests (if applicable)
  - Prompt robustness tests
  - Context retrieval accuracy tests
  - Output format validation tests
  - Performance tests (latency, throughput)
  - Token usage tests
  - End-to-end LLM workflow tests
</test_template>

<instructions>
  ACTION: Create comprehensive test specification
  ENSURE: All new functionality has test coverage
  SPECIFY: Mock requirements for external services
  INCLUDE: LLM-specific tests if applicable
</instructions>

</step>

<step number="11" name="user_review">

### Step 11: User Review

<step_metadata>
  <action>request user review</action>
  <reviews>
    - spec.md
    - all sub-specs files
  </reviews>
</step_metadata>

<review_request>
  I've created the spec documentation:

  - Spec Requirements: @.agent-os/specs/YYYY-MM-DD-spec-name/spec.md
  - Technical Spec: @.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/technical-spec.md
  [LIST_OTHER_CREATED_SPECS]

  Please review and let me know if any changes are needed before I create the task breakdown.
</review_request>

<instructions>
  ACTION: Request user review of all documents
  WAIT: For approval or revision requests
  REVISE: Make requested changes if any
</instructions>

</step>

<step number="12" name="create_tasks">

### Step 12: Create tasks.md

<step_metadata>
  <creates>
    - file: tasks.md
  </creates>
  <depends_on>user approval from step 11</depends_on>
</step_metadata>

<template_selection>
  <llm_ai_components>
    **Template:** Use complete 8-phase template from @templates/task-templates.md
    **Phases:** Design → Pydantic Schemas → Utilities → FastAPI → Nodes → Flow → Integration → Optimization
  </llm_ai_components>
  <traditional_features>
    **Template:** Use simplified template from @templates/task-templates.md  
    **Phases:** Data Models → Business Logic → FastAPI → Integration & Testing
  </traditional_features>
</template_selection>

<instructions>
  ACTION: Create task breakdown using appropriate template
  TEMPLATE: Select from @templates/task-templates.md based on feature type
  STRUCTURE: Follow 8-step methodology for LLM/AI or simplified for traditional features
  ORDER: Ensure proper phase dependencies
  VALIDATE: Include toolchain validation at every phase
</instructions>

</step>

<step number="13" name="update_cross_references">

### Step 13: Documentation Cross-References

<step_metadata>
  <updates>
    - file: spec.md
  </updates>
  <adds>references to all spec files</adds>
</step_metadata>

<reference_template>
  ## Spec Documentation

  - Tasks: @.agent-os/specs/YYYY-MM-DD-spec-name/tasks.md
  - Technical Specification: @.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/technical-spec.md
  - API Specification: @.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/api-spec.md
  - Database Schema: @.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/database-schema.md
  - Tests Specification: @.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/tests.md
</reference_template>

<reference_format>
  - Use @ prefix for clickable paths
  - Include full path from project root
  - Only list files that were created
</reference_format>

<instructions>
  ACTION: Update spec.md with references
  FORMAT: Use @ prefix for all paths
  INCLUDE: Only files actually created
</instructions>

</step>

<step number="14" name="decision_documentation">

### Step 14: Decision Documentation

<step_metadata>
  <evaluates>strategic impact</evaluates>
  <updates>decisions.md if needed</updates>
</step_metadata>

<decision_analysis>
  <review_against>
    - @.agent-os/product/mission.md
    - @.agent-os/product/decisions.md
  </review_against>
  <criteria>
    - changes product direction
    - impacts roadmap priorities
    - introduces new technical patterns
    - affects user experience significantly
    - **For LLM/AI components:** Introduces new LLM models/providers, changes core LLM patterns, or has significant cost/performance implications
  </criteria>
</decision_analysis>

<decision_tree>
  IF spec_impacts_mission_or_roadmap:
    IDENTIFY key_decisions (max 3)
    DOCUMENT decision_details
    ASK user_for_approval
    IF approved:
      UPDATE decisions.md
  ELSE:
    STATE "This spec is inline with the current mission and roadmap, so no need to post anything to our decisions log at this time."
</decision_tree>

<instructions>
  ACTION: Analyze spec for strategic decisions
  IDENTIFY: Up to 3 key decisions if any
  REQUEST: User approval before updating
  UPDATE: Add to decisions.md if approved
  TAG: Decisions related to LLM/AI with 'llm-ai' category
</instructions>

</step>

<step number="15" name="execution_readiness">

### Step 15: Execution Readiness Check

<step_metadata>
  <evaluates>readiness to begin implementation</evaluates>
  <depends_on>completion of all previous steps</depends_on>
</step_metadata>

<readiness_summary>
  <present_to_user>
    - Spec name and description
    - First task summary from tasks.md
    - Estimated complexity/scope
    - Key deliverables for task 1
  </present_to_user>
</readiness_summary>

<execution_prompt>
  PROMPT: "The spec planning is complete. The first task is:

  **Task 1:** [FIRST_TASK_TITLE]
  [BRIEF_DESCRIPTION_OF_TASK_1_AND_SUBTASKS]

  Would you like me to proceed with implementing Task 1? I will follow the execution guidelines in @~/.agent-os/instructions/execute-tasks.md and focus only on this first task and its subtasks unless you specify otherwise.

  Type 'yes' to proceed with Task 1, or let me know if you'd like to review or modify the plan first."
</execution_prompt>

<execution_flow>
  IF user_confirms_yes:
    REFERENCE: @~/.agent-os/instructions/execute-tasks.md
    FOCUS: Only Task 1 and its subtasks
    CONSTRAINT: Do not proceed to additional tasks without explicit user request
  ELSE:
    WAIT: For user clarification or modifications
</execution_flow>

<instructions>
  ACTION: Summarize first task and request user confirmation
  REFERENCE: Use execute-tasks.md for implementation
  SCOPE: Limit to Task 1 only unless user specifies otherwise
</instructions>

</step>

</process_flow>

## Execution Standards

<standards>
  <follow>
    - @.agent-os/product/code-style.md
    - @.agent-os/product/dev-best-practices.md
    - @.agent-os/product/tech-stack.md
  </follow>
  <maintain>
    - Consistency with product mission
    - Alignment with roadmap
    - Technical coherence
  </maintain>
  <create>
    - Comprehensive documentation
    - Clear implementation path
    - Testable outcomes
  </create>
</standards>

<template_usage>
  <pocketflow_templates>@templates/pocketflow-templates.md</pocketflow_templates>
  <fastapi_templates>@templates/fastapi-templates.md</fastapi_templates>
  <task_templates>@templates/task-templates.md</task_templates>
</template_usage>

<final_checklist>
  <verify>
    - [ ] Accurate date determined via file system
    - [ ] Spec folder created with correct date prefix
    - [ ] spec.md contains all required sections
    - [ ] All applicable sub-specs created using templates
    - [ ] User approved documentation
    - [ ] tasks.md created using appropriate template
    - [ ] Cross-references added to spec.md
    - [ ] Strategic decisions evaluated
  </verify>
</final_checklist>

<!-- Orchestration Integration -->
@include extensions/llm-workflow-extension.md if involves_llm_ai
@include extensions/pocketflow-integration.md
@include orchestration/orchestrator-hooks.md