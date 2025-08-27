---
description: Product Planning Rules for Agent OS
globs:
alwaysApply: false
version: 4.1
encoding: UTF-8
---

# Product Planning Rules

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
  - Generate comprehensive product documentation for new projects
  - Create structured files for AI agent consumption
  - Establish consistent project initialization
</purpose>

<context>
  - Part of Agent OS framework
  - Triggered during project initialization
  - Output used by AI agents throughout development
</context>

<prerequisites>
  - Write access to project root
  - Git initialized (recommended)
  - User has product requirements
  - Access to @~/.claude/CLAUDE.md
</prerequisites>

<process_flow>

<step number="1" name="gather_user_input">

### Step 1: Gather User Input

<step_metadata>
  <required_inputs>
    - main_idea: string
    - key_features: array[string] (minimum: 3)
    - target_users: array[string] (minimum: 1)
    - tech_stack: object
    - involves_llm_ai: boolean (new)
  </required_inputs>
  <validation>blocking</validation>
</step_metadata>

<data_sources>
  <primary>user_direct_input</primary>
  <fallback_sequence>
    1. @~/.agent-os/standards/tech-stack.md
    2. @~/.claude/CLAUDE.md
  </fallback_sequence>
</data_sources>

<error_template>
  Please provide the following missing information:
  1. Main idea for the product
  2. List of key features (minimum 3)
  3. Target users and use cases (minimum 1)
  4. Tech stack preferences (e.g., "Python with Django", "Node.js with React")
  5. Does this product involve LLMs or AI components? (yes/no)
  6. Has the new application been initialized yet and we're inside the project folder? (yes/no)
</error_template>

<instructions>
  ACTION: Collect all required inputs from user
  VALIDATION: Ensure all inputs provided before proceeding
  FALLBACK: Check configuration files for tech stack defaults
  ERROR: Use error_template if inputs missing
</instructions>

</step>

<step number="2" name="create_documentation_structure">

### Step 2: Create Documentation Structure

<step_metadata>
  <creates>
    - directory: .agent-os/product/
    - files: 4
  </creates>
</step_metadata>

<file_structure>
  .agent-os/
  └── product/
      ├── mission.md          # Product vision and purpose
      ├── tech-stack.md       # Technical architecture
      └── roadmap.md          # Development phases
</file_structure>

<git_config>
  <commit_message>Initialize Agent OS product documentation</commit_message>
  <tag>v0.1.0-planning</tag>
  <gitignore_consideration>true</gitignore_consideration>
</git_config>

<instructions>
  ACTION: Create directory structure as specified
  VALIDATION: Verify write permissions before creating
  PROTECTION: Confirm before overwriting existing files
</instructions>

</step>

<step number="3" name="create_mission_md">

### Step 3: Create mission.md

<step_metadata>
  <creates>
    - file: .agent-os/product/mission.md
  </creates>
</step_metadata>

<file_template>
  <header>
    # Product Mission

    > Last Updated: [CURRENT_DATE]
    > Version: 1.0.0
  </header>
  <required_sections>
    - Pitch
    - Users
    - The Problem
    - Differentiators
    - Key Features
    - AI/LLM Strategy (new)
  </required_sections>
</file_template>

<section name="pitch">
  <template>
    ## Pitch

    [PRODUCT_NAME] is a [PRODUCT_TYPE] that helps [TARGET_USERS] [SOLVE_PROBLEM] by providing [KEY_VALUE_PROPOSITION].
  </template>
  <constraints>
    - length: 1-2 sentences
    - style: elevator pitch
  </constraints>
</section>

<section name="users">
  <template>
    ## Users

    ### Primary Customers

    - [CUSTOMER_SEGMENT_1]: [DESCRIPTION]
    - [CUSTOMER_SEGMENT_2]: [DESCRIPTION]

    ### User Personas

    **[USER_TYPE]** ([AGE_RANGE])
    - **Role:** [JOB_TITLE]
    - **Context:** [BUSINESS_CONTEXT]
    - **Pain Points:** [PAIN_POINT_1], [PAIN_POINT_2]
    - **Goals:** [GOAL_1], [GOAL_2]
  </template>
  <schema>
    - name: string
    - age_range: "XX-XX years old"
    - role: string
    - context: string
    - pain_points: array[string]
    - goals: array[string]
  </schema>
</section>

<section name="problem">
  <template>
    ## The Problem

    ### [PROBLEM_TITLE]

    [PROBLEM_DESCRIPTION]. [QUANTIFIABLE_IMPACT].

    **Our Solution:** [SOLUTION_DESCRIPTION]
  </template>
  <constraints>
    - problems: 2-4
    - description: 1-3 sentences
    - impact: include metrics
    - solution: 1 sentence
  </constraints>
</section>

<section name="differentiators">
  <template>
    ## Differentiators

    ### [DIFFERENTIATOR_TITLE]

    Unlike [COMPETITOR_OR_ALTERNATIVE], we provide [SPECIFIC_ADVANTAGE]. This results in [MEASURABLE_BENEFIT].
  </template>
  <constraints>
    - count: 2-3
    - focus: competitive advantages
    - evidence: required
  </constraints>
</section>

<section name="features">
  <template>
    ## Key Features

    ### Core Features

    - **[FEATURE_NAME]:** [USER_BENEFIT_DESCRIPTION]

    ### Collaboration Features

    - **[FEATURE_NAME]:** [USER_BENEFIT_DESCRIPTION]
  </template>
  <constraints>
    - total: 8-10 features
    - grouping: by category
    - description: user-benefit focused
  </constraints>
</section>

<section name="ai_llm_strategy">
  <template>
    ## AI/LLM Strategy

    **Does this product incorporate AI/LLM components?** [YES/NO]

    **If YES:**
    - **Primary LLM Framework:** PocketFlow
    - **Development Methodology:** 8-step Agentic Coding process (Design-first approach)
    - **Rationale:** Chosen for its minimalism, flexibility (Nodes, Flows, Shared Store), and suitability for Agentic Coding principles. It allows explicit graph-based design for Agents, Workflows, and RAG patterns. Follows "humans design, agents code" philosophy.
    - **Key Patterns Utilized:** [LIST_POCKETFLOW_PATTERNS_TO_BE_USED_E.G._AGENT,_RAG,_WORKFLOW,_MAPREDUCE,_MULTI_AGENT,_STRUCTURED_OUTPUT]
    - **Planned LLM Providers/Models:** [LIST_OF_LLM_PROVIDERS_AND_MODELS]
    - **Utility Philosophy:** "Examples provided, implement your own" - custom utility functions for maximum flexibility
    - **Design Requirements:** All LLM features require `docs/design.md` completion before implementation begins
    - **Integration Pattern:** FastAPI endpoints → PocketFlow Flows → Node execution → Utility functions
  </template>
  <conditional_execution>
    <detection_criteria>
      <check>involves_llm_ai boolean from Step 1</check>
      <check>user mentions LLM, AI, or machine learning in features</check>
      <check>user mentions chatbots, agents, or AI workflows</check>
    </detection_criteria>
    <if_llm_detected>
      <action>Generate complete AI/LLM Strategy section</action>
      <required_fields>
        - Primary LLM Framework: PocketFlow
        - Development Methodology: 8-step Agentic Coding
        - Key Patterns Utilized: Based on feature analysis
        - Design Requirements: Mandatory docs/design.md
      </required_fields>
    </if_llm_detected>
    <if_no_llm>
      <action>Skip this section entirely</action>
      <message>No AI/LLM components detected - skipping AI strategy section</message>
    </if_no_llm>
  </conditional_execution>
  <instructions>
    DETECT: Check multiple indicators for LLM/AI usage
    CONDITIONAL: Generate section only if LLM/AI components confirmed
    FILL: List relevant PocketFlow patterns based on initial feature ideas
    FILL: List anticipated LLM providers/models
    EMPHASIZE: Design-first methodology and utility function philosophy
    SKIP: Section entirely if no LLM/AI involvement
  </instructions>
</section>

<instructions>
  ACTION: Create mission.md using all section templates
  FILL: Use data from Step 1 user inputs
  FORMAT: Maintain exact template structure
</instructions>

</step>

<step number="4" name="create_tech_stack_md">

### Step 4: Create tech-stack.md

<step_metadata>
  <creates>
    - file: .agent-os/product/tech-stack.md
  </creates>
</step_metadata>

<file_template>
  <header>
    # Technical Stack

    > Last Updated: [CURRENT_DATE]
    > Version: 1.0.0
  </header>
</file_template>

<required_items>
  - programming_language: string + version (defaults to Python 3.12+)
  - application_framework: string + version (defaults to FastAPI)
  - data_validation: string + version (defaults to Pydantic)
  - package_manager: string (defaults to uv)
  - linting_formatting: string (defaults to Ruff)
  - type_checking: string (defaults to mypy/ty)
  - testing_framework: string (defaults to pytest)
  - database_system: string (defaults to SQLite)
  - vector_store: string (defaults to ChromaDB, if LLM/AI)
  - frontend_framework: string (defaults to "None - API only")
  - application_hosting: string
  - database_hosting: string
  - deployment_solution: string
  - code_repository_url: string
  - llm_framework: string + version (defaults to PocketFlow, if LLM/AI)
  - llm_providers: array[string] (if LLM/AI)
</required_items>

<data_resolution>
  <for_each item="required_items">
    <if_not_in>user_input</if_not_in>
    <then_check>
      1. @~/.agent-os/standards/tech-stack.md
      2. @~/.claude/CLAUDE.md
    </then_check>
    <else>add_to_missing_list</else>
  </for_each>
</data_resolution>

<conditional_tech_stack>
  <llm_ai_detection>
    <if_involves_llm_ai>true</if_involves_llm_ai>
    <then_apply>
      - llm_framework: "PocketFlow (latest)"
      - vector_store: "ChromaDB" 
      - programming_language: "Python 3.12+"
      - application_framework: "FastAPI"
      - data_validation: "Pydantic"
    </then_apply>
    <else_apply>
      - llm_framework: "n/a"
      - vector_store: "n/a"
      - programming_language: "Python 3.12+" (default, user can override)
      - application_framework: "FastAPI" (default, user can override)
      - data_validation: "Pydantic" (default, user can override)
    </else_apply>
  </llm_ai_detection>
  
  <project_structure_selection>
    <if_involves_llm_ai>true</if_involves_llm_ai>
    <then_include>
      - nodes.py file for PocketFlow nodes
      - flow.py file for PocketFlow flows
      - docs/design.md (MANDATORY before implementation)
      - utils/ directory with LLM utility functions
    </then_include>
    <else_include>
      - Standard FastAPI structure only
      - utils/ directory for business logic
      - No PocketFlow-specific files required
    </else_include>
  </project_structure_selection>
</conditional_tech_stack>

<missing_items_template>
  Please provide the following technical stack details:
  [NUMBERED_LIST_OF_MISSING_ITEMS]

  You can respond with the technology choice or "n/a" for each item.
</missing_items_template>

<instructions>
  ACTION: Document all tech stack choices with modern Python defaults
  RESOLUTION: Check user input first, then config files, then apply defaults
  DEFAULTS: Use Python 3.12+ with FastAPI, Pydantic, uv, Ruff, and pytest unless user specifies otherwise
  REQUEST: Ask for any missing items using template
  PRIORITIZE: PocketFlow for llm_framework if product involves AI/LLM
  EMPHASIZE: Modern type-safe Python development stack as foundation
</instructions>

</step>

<step number="5" name="create_roadmap_md">

### Step 5: Create roadmap.md

<step_metadata>
  <creates>
    - file: .agent-os/product/roadmap.md
  </creates>
</step_metadata>

<file_template>
  <header>
    # Product Roadmap

    > Last Updated: [CURRENT_DATE]
    > Version: 1.0.0
    > Status: Planning
  </header>
</file_template>

<phase_structure>
  <phase_count>5</phase_count>
  <features_per_phase>3-7</features_per_phase>
  <phase_template>
    ## Phase [NUMBER]: [NAME] ([DURATION])

    **Goal:** [PHASE_GOAL]
    **Success Criteria:** [MEASURABLE_CRITERIA]

    ### Must-Have Features

    - [ ] [FEATURE] - [DESCRIPTION] `[EFFORT]`
        - **LLM Pattern:** [POCKETFLOW_PATTERN] (if applicable, e.g., Agent, RAG, Workflow)
        - **Design Requirement:** `docs/design.md` must be completed before implementation (if LLM/AI)

    ### Should-Have Features

    - [ ] [FEATURE] - [DESCRIPTION] `[EFFORT]`
        - **LLM Pattern:** [POCKETFLOW_PATTERN] (if applicable)
        - **Design Requirement:** `docs/design.md` must be completed before implementation (if LLM/AI)

    ### Dependencies

    - [DEPENDENCY]
    - Complete design documentation for any LLM/AI features before implementation begins
  </phase_template>
</phase_structure>

<phase_guidelines>
  - Phase 1: Core MVP functionality
  - Phase 2: Key differentiators
  - Phase 3: Scale and polish
  - Phase 4: Advanced features
  - Phase 5: Enterprise features
</phase_guidelines>

<effort_scale>
  - XS: 1 day
  - S: 2-3 days
  - M: 1 week
  - L: 2 weeks
  - XL: 3+ weeks
</effort_scale>

<conditional_roadmap>
  <llm_ai_features>
    <if_involves_llm_ai>true</if_involves_llm_ai>
    <then_apply>
      - Add "Design Document Creation" as prerequisite for LLM features
      - Tag features with PocketFlow patterns (Agent, RAG, Workflow, etc.)
      - Include design.md requirement in dependencies
      - Enforce 8-step methodology progression
    </then_apply>
    <else_apply>
      - Standard feature progression without PocketFlow requirements
      - No design document prerequisites
      - Standard FastAPI development phases
    </else_apply>
  </llm_ai_features>
</conditional_roadmap>

<instructions>
  ACTION: Create 5 development phases
  PRIORITIZE: Based on dependencies and mission importance
  ESTIMATE: Use effort_scale for all features
  VALIDATE: Ensure logical progression between phases
  CONDITIONAL: Apply LLM/AI-specific requirements only if detected
  TAG: Features with relevant PocketFlow patterns if they involve LLMs/AI
  ENFORCE: Design-first requirement for all LLM/AI features (docs/design.md)
  EMPHASIZE: No implementation begins without completed design documentation for LLM features
  FALLBACK: Standard FastAPI roadmap if no LLM/AI components
</instructions>

</step>


<step number="6" name="create_or_update_claude_md">

### Step 6: Create or Update CLAUDE.md

<step_metadata>
  <creates>
    - file: CLAUDE.md
  </creates>
  <updates>
    - file: CLAUDE.md (if exists)
  </updates>
  <merge_strategy>append_or_replace_section</merge_strategy>
</step_metadata>

<file_location>
  <path>./CLAUDE.md</path>
  <description>Project root directory</description>
</file_location>

<content_template>
## Agent OS Documentation

### Product Context
- **Mission & Vision:** @.agent-os/product/mission.md
- **Technical Architecture:** @.agent-os/product/tech-stack.md
- **Development Roadmap:** @.agent-os/product/roadmap.md

### Development Standards
- **Code Style:** @~/.agent-os/standards/code-style.md
- **Best Practices:** @~/.agent-os/standards/best-practices.md
- **PocketFlow Principles:** @~/.agent-os/standards/best-practices.md (specifically for LLM components) (new)

### Project Management
- **Active Specs:** @.agent-os/specs/
- **Spec Planning:** Use `@~/.agent-os/instructions/create-spec.md`
- **Tasks Execution:** Use `@~/.agent-os/instructions/execute-tasks.md`

## Workflow Instructions

When asked to work on this codebase:

1. **First**, check @.agent-os/product/roadmap.md for current priorities
2. **Then**, follow the appropriate instruction file:
   - For new features: @.agent-os/instructions/create-spec.md
   - For tasks execution: @.agent-os/instructions/execute-tasks.md
3. **Always**, adhere to the standards in the files listed above, including PocketFlow principles for LLM-related tasks.

## Important Notes

- Product-specific files in `.agent-os/product/` override any global standards
- User's specific instructions override (or amend) instructions found in `.agent-os/specs/...`
- Always adhere to established patterns, code style, and best practices documented above.
</content_template>

<merge_behavior>
  <if_file_exists>
    <check_for_section>"## Agent OS Documentation"</check_for_section>
    <if_section_exists>
      <action>replace_section</action>
      <start_marker>"## Agent OS Documentation"</start_marker>
      <end_marker>next_h2_heading_or_end_of_file</end_marker>
    </if_section_exists>
    <if_section_not_exists>
      <action>append_to_file</action>
      <separator>"\n\n"</separator>
    </if_section_not_exists>
  </if_file_exists>
  <if_file_not_exists>
    <action>create_new_file</action>
    <content>content_template</content>
  </if_file_not_exists>
</merge_behavior>

<instructions>
  ACTION: Check if CLAUDE.md exists in project root
  MERGE: Replace "Agent OS Documentation" section if it exists
  APPEND: Add section to end if file exists but section doesn't
  CREATE: Create new file with template content if file doesn't exist
  PRESERVE: Keep all other existing content in the file
</instructions>

</step>

</process_flow>

## Execution Summary

<final_checklist>
  <verify>
    - [ ] All 3 files created in .agent-os/product/
    - [ ] User inputs incorporated throughout
    - [ ] Missing tech stack items requested
    - [ ] CLAUDE.md created or updated with Agent OS documentation
  </verify>
</final_checklist>

<execution_order>
  1. Gather and validate all inputs
  2. Create directory structure
  3. Generate each file sequentially
  4. Request any missing information
  5. Create or update project CLAUDE.md file
  6. Validate complete documentation set
</execution_order>

## Standard Project Structure

<project_structure>
  <conditional_structure>
    <base_structure>
      All projects get this foundation:
      ```
      project/
      ├── main.py           # FastAPI app entry point
      ├── schemas/          # Pydantic models
      │   ├── __init__.py
      │   ├── requests.py   # API request models
      │   └── responses.py  # API response models
      ├── utils/            # Custom utilities
      │   ├── __init__.py
      │   └── [business_utils].py
      ├── tests/
      │   ├── __init__.py
      │   ├── test_models.py
      │   └── test_endpoints.py
      ├── pyproject.toml    # uv package management (preferred)
      ├── uv.lock           # uv lockfile
      ├── .gitignore
      └── README.md
      ```
    </base_structure>
    
    <llm_ai_additions>
      If LLM/AI components detected, add:
      ```
      project/
      ├── nodes.py          # PocketFlow nodes
      ├── flow.py           # PocketFlow flows  
      ├── utils/
      │   ├── call_llm.py   # LLM utility functions
      │   └── [llm_utils].py
      ├── docs/
      │   └── design.md     # MANDATORY before implementation
      └── tests/
          └── test_flows.py # PocketFlow flow tests
      ```
    </llm_ai_additions>
  </conditional_structure>
  
  <structure_selection>
    <if_involves_llm_ai>true</if_involves_llm_ai>
    <then_create>base_structure + llm_ai_additions</then_create>
    <else_create>base_structure only</else_create>
  </structure_selection>
</project_structure>

<architecture_pattern>
  This structure supports the integrated architecture:
  
  ```
  FastAPI (main.py)
      ↓ receives requests
  Pydantic Models (schemas/)
      ↓ validates data  
  PocketFlow Flows (flow.py)
      ↓ orchestrates logic
  PocketFlow Nodes (nodes.py)
      ↓ executes tasks
  Utility Functions (utils/)
      ↓ interfaces with external services
  FastMCP Tools (when multi-agent coordination needed)
  ```
  
  This ensures:
  - **Type safety** at every boundary with Pydantic
  - **Clear separation** between API layer and business logic
  - **Modular design** with reusable nodes and utilities
  - **Agent coordination** through FastMCP when needed
</architecture_pattern>

## Orchestration Integration

@include orchestration/orchestrator-hooks.md

This instruction integrates with the orchestrator system for coordinated planning and execution.