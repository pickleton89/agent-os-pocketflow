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
  5. Has the new application been initialized yet and we're inside the project folder? (yes/no)
</error_template>

<instructions>
  ACTION: Collect all required inputs from user
  VALIDATION: Ensure all inputs provided before proceeding
  FALLBACK: Check configuration files for tech stack defaults
  ERROR: Use error_template if inputs missing
</instructions>

</step>

<step number="1.5" subagent="strategic-planner" name="comprehensive_strategic_planning">

### Step 1.5: Comprehensive Strategic Planning and Implementation Roadmap

<step_metadata>
  <uses>strategic-planner subagent</uses>
  <creates>comprehensive strategic plan and implementation roadmap</creates>
  <purpose>develop strategic foundation for product planning</purpose>
</step_metadata>

Use the strategic-planner subagent to create a comprehensive strategic plan and implementation roadmap based on user input and product requirements.

<strategic_planning_context>
  <context_to_provide>
    - User input from Step 1: main idea, key features, target users, tech stack
    - Product vision and market positioning requirements
    - Technical architecture decisions and constraints
    - Development timeline and resource considerations
    - Competitive landscape and differentiation strategy
    - Team capabilities and development preferences
  </context_to_provide>
  
  <expected_output>
    - Strategic product roadmap with phase-by-phase implementation plan
    - Technical architecture recommendations with rationale
    - PocketFlow pattern integration strategy
    - Risk assessment and mitigation strategies
    - Resource allocation and timeline recommendations
    - Market positioning and competitive differentiation strategy
  </expected_output>
  
  <required_for_next_step>
    Strategic plan informs all subsequent documentation generation and roadmap creation
  </required_for_next_step>
</strategic_planning_context>

<comprehensive_planning_scope>
  <strategic_dimensions>
    - Product vision and market fit analysis
    - Technical architecture and PocketFlow pattern selection
    - Development methodology and team organization
    - Timeline and milestone planning
    - Risk management and contingency planning
    - Competitive positioning and differentiation
  </strategic_dimensions>
  
  <pocketflow_integration_strategy>
    - Optimal pattern selection based on product requirements
    - Implementation sequence for complex vs. simple patterns
    - Integration with existing technology choices
    - Scalability and performance considerations
    - Team training and capability development
  </pocketflow_integration_strategy>
</comprehensive_planning_scope>

<instructions>
  ACTION: Use strategic-planner subagent for comprehensive strategic planning
  REQUEST: "Create comprehensive strategic plan and implementation roadmap:
            - Product vision: [MAIN_IDEA_AND_TARGET_USERS]
            - Key features: [FEATURE_LIST_AND_PRIORITIES]
            - Technical foundation: [TECH_STACK_AND_ARCHITECTURE_PREFERENCES]
            - Market context: [COMPETITIVE_LANDSCAPE_AND_POSITIONING]
            - PocketFlow integration: [OPTIMAL_PATTERN_SELECTION_AND_IMPLEMENTATION]
            - Strategic priorities: [DEVELOPMENT_PHASES_AND_RESOURCE_ALLOCATION]"
  PROCESS: Strategic recommendations and implementation roadmap
  APPLY: Strategic plan to documentation structure and content generation
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
    - Architecture Strategy
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

<section name="architecture_strategy">
  <template>
    ## Architecture Strategy

    **Application Architecture:** PocketFlow-based design

    - **Primary Framework:** PocketFlow
    - **Development Methodology:** Design-first approach with structured workflow patterns
    - **Rationale:** Chosen for its minimalism, flexibility (Nodes, Flows, Shared Store), and scalability from simple workflows to complex multi-agent systems. It provides explicit graph-based design for all application patterns.
    - **Key Patterns Utilized:** [LIST_POCKETFLOW_PATTERNS_TO_BE_USED_E.G._WORKFLOW,_TOOL,_AGENT,_RAG,_MAPREDUCE,_STRUCTURED_OUTPUT]
    - **Complexity Level:** [SIMPLE_WORKFLOW/ENHANCED_WORKFLOW/COMPLEX_APPLICATION/LLM_APPLICATION]
    - **Utility Philosophy:** "Examples provided, implement your own" - custom utility functions for maximum flexibility
    - **Design Requirements:** All projects require `docs/design.md` completion before implementation begins
    - **Integration Pattern:** FastAPI endpoints → PocketFlow Flows → Node execution → Utility functions
    - **LLM Providers/Models:** [LIST_IF_APPLICABLE, OTHERWISE_N/A]
  </template>
  <instructions>
    UNIVERSAL: Generate this section for ALL products
    PATTERN_MAPPING: Map project features to appropriate PocketFlow patterns
    COMPLEXITY: Assess and assign appropriate complexity level
    PATTERNS: Select patterns based on feature analysis (WORKFLOW for simple, TOOL for APIs, AGENT for complex logic, etc.)
    DESIGN_FIRST: Emphasize mandatory docs/design.md for all projects
    UNIVERSAL_REQUIREMENT: Include appropriate providers and integrations for all PocketFlow projects
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
  - workflow_framework: string + version (defaults to PocketFlow)
  - vector_store: string (defaults to ChromaDB, if needed)
  - frontend_framework: string (defaults to "None - API only")
  - application_hosting: string
  - database_hosting: string
  - deployment_solution: string
  - code_repository_url: string
  - llm_providers: array[string] (if applicable)
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

<universal_tech_stack>
  <default_stack>
    - workflow_framework: "PocketFlow (latest)"
    - programming_language: "Python 3.12+"
    - application_framework: "FastAPI"
    - data_validation: "Pydantic"
    - vector_store: "ChromaDB" (universal requirement for data storage and retrieval)
  </default_stack>
  
  <project_structure_inclusion>
    <always_include>
      - nodes.py file for PocketFlow nodes
      - flow.py file for PocketFlow flows
      - docs/design.md (MANDATORY before implementation)
      - utils/ directory for application-specific utility functions
    </always_include>
  </project_structure_inclusion>
</universal_tech_stack>

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
  UNIVERSAL: PocketFlow for workflow_framework for all projects
  EMPHASIZE: Modern type-safe Python development stack with PocketFlow architecture as foundation
</instructions>

</step>

<step number="4.5" subagent="pattern-recognizer" name="technical_pattern_validation">

### Step 4.5: Technical Pattern Validation

<step_metadata>
  <uses>pattern-recognizer subagent</uses>
  <validates>recommended technical patterns and architecture decisions</validates>
  <purpose>ensure optimal PocketFlow pattern alignment with product requirements</purpose>
</step_metadata>

Use the pattern-recognizer subagent to validate the recommended technical patterns and architecture decisions before finalizing the roadmap.

<pattern_validation_context>
  <context_to_provide>
    - Strategic plan recommendations from Step 1.5
    - Technical architecture decisions from tech-stack.md creation
    - Product requirements and feature complexity from mission.md
    - Performance, scalability, and integration requirements
    - Team capabilities and development constraints
    - PocketFlow pattern options: Agent, RAG, Workflow, MapReduce, Multi-Agent, Structured Output
  </context_to_provide>
  
  <expected_output>
    - Validation of recommended PocketFlow patterns with confidence scores
    - Technical architecture compliance assessment
    - Pattern optimization recommendations for specific features
    - Implementation complexity analysis and warnings
    - Alternative pattern suggestions if misalignment detected
    - Integration and migration strategy validation
  </expected_output>
  
  <required_for_next_step>
    Pattern validation ensures roadmap features use optimal PocketFlow patterns
  </required_for_next_step>
</pattern_validation_context>

<technical_validation_scope>
  <architecture_validation>
    - PocketFlow pattern suitability for each major feature
    - Technical stack compatibility with chosen patterns
    - Scalability and performance implications
    - Integration complexity and dependencies
  </architecture_validation>
  
  <implementation_validation>
    - Team capability alignment with pattern complexity
    - Development timeline feasibility
    - Resource requirements for pattern implementation
    - Risk assessment for technical choices
  </implementation_validation>
</technical_validation_scope>

<instructions>
  ACTION: Use pattern-recognizer subagent for technical pattern validation
  REQUEST: "Validate recommended technical patterns and architecture decisions:
            - Strategic recommendations: [STRATEGIC_PLAN_FROM_STEP_1_5]
            - Technical architecture: [TECH_STACK_DECISIONS_AND_FRAMEWORK_CHOICES]
            - Product requirements: [FEATURE_COMPLEXITY_AND_PERFORMANCE_NEEDS]
            - Pattern candidates: [PROPOSED_POCKETFLOW_PATTERNS_FOR_FEATURES]
            - Validation focus: [OPTIMAL_PATTERN_ALIGNMENT_AND_IMPLEMENTATION_FEASIBILITY]
            - Alternative analysis: [PATTERN_OPTIMIZATION_AND_RISK_MITIGATION]"
  PROCESS: Pattern validation results and optimization recommendations
  APPLY: Validated patterns to roadmap feature tagging and implementation planning
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
        - **PocketFlow Pattern:** [POCKETFLOW_PATTERN] (e.g., WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE)
        - **Design Requirement:** `docs/design.md` must be completed before implementation

    ### Should-Have Features

    - [ ] [FEATURE] - [DESCRIPTION] `[EFFORT]`
        - **PocketFlow Pattern:** [POCKETFLOW_PATTERN]
        - **Design Requirement:** `docs/design.md` must be completed before implementation

    ### Dependencies

    - [DEPENDENCY]
    - Complete design documentation for all features before implementation begins
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

<universal_roadmap>
  <pocketflow_features>
    <always_apply>
      - Add "Design Document Creation" as prerequisite for all features
      - Tag all features with appropriate PocketFlow patterns (WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE, etc.)
      - Include design.md requirement in dependencies
      - Enforce design-first methodology progression
      - Map complexity from simple workflows to complex multi-agent systems
    </always_apply>
  </pocketflow_features>
</universal_roadmap>

<instructions>
  ACTION: Create 5 development phases
  PRIORITIZE: Based on dependencies and mission importance
  ESTIMATE: Use effort_scale for all features
  VALIDATE: Ensure logical progression between phases
  UNIVERSAL: Apply PocketFlow requirements to all projects
  TAG: All features with relevant PocketFlow patterns (WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE, etc.)
  ENFORCE: Design-first requirement for all features (docs/design.md)
  EMPHASIZE: No implementation begins without completed design documentation
  PATTERN_MAP: Map project complexity to appropriate PocketFlow patterns
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
- **PocketFlow Principles:** @~/.agent-os/standards/best-practices.md (universal architecture standards)

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
3. **Always**, adhere to the standards in the files listed above, including PocketFlow principles for all development tasks.

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
  <universal_structure>
    All projects get this complete PocketFlow foundation:
    ```
    project/
    ├── main.py           # FastAPI app entry point
    ├── nodes.py          # PocketFlow nodes
    ├── flow.py           # PocketFlow flows
    ├── schemas/          # Pydantic models
    │   ├── __init__.py
    │   ├── requests.py   # API request models
    │   └── responses.py  # API response models
    ├── utils/            # Custom utilities
    │   ├── __init__.py
    │   └── [application_utils].py
    ├── docs/
    │   └── design.md     # MANDATORY before implementation
    ├── tests/
    │   ├── __init__.py
    │   ├── test_models.py
    │   ├── test_endpoints.py
    │   └── test_flows.py # PocketFlow flow tests
    ├── pyproject.toml    # uv package management (preferred)
    ├── uv.lock           # uv lockfile
    ├── .gitignore
    └── README.md
    ```
  </universal_structure>
</project_structure>

<architecture_pattern>
  This structure supports the universal PocketFlow architecture:
  
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
  Design Document (docs/design.md)
      ↓ guides implementation
  ```
  
  This ensures:
  - **Type safety** at every boundary with Pydantic
  - **Clear separation** between API layer and business logic
  - **Modular design** with reusable nodes and utilities
  - **Design-first approach** for all features
  - **Scalable patterns** from simple workflows to complex multi-agent systems
</architecture_pattern>

## Orchestration Integration

@include orchestration/orchestrator-hooks.md

This instruction integrates with the orchestrator system for coordinated planning and execution.