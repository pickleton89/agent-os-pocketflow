---
description: Product Planning Rules for Agent OS
globs:
alwaysApply: false
version: 4.1
encoding: UTF-8
---

# Product Planning Rules

<!-- Process XML blocks first, execute sequentially, use templates exactly -->

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

**Uses:** strategic-planner subagent for comprehensive strategic planning

Use the strategic-planner subagent to create a comprehensive strategic plan and implementation roadmap based on user input and product requirements.

<subagent_context>
  **Context:** User input, product vision, technical decisions, development timeline
  **Output:** Strategic roadmap, architecture recommendations, PocketFlow integration strategy
  **Next Step:** Documentation generation and roadmap creation
</subagent_context>

**Planning Scope:** Product vision, technical architecture, development methodology, PocketFlow pattern selection

**Blocking:** Must have clear requirements before documentation creation

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

<step number="1.6" name="documentation_discovery">
### Step 1.6: Documentation Discovery and Integration

<step_metadata>
  <purpose>Gather external documentation for accurate technical context</purpose>
  <optional>true - user can skip</optional>
  <timing>after strategic planning, before documentation creation</timing>
</step_metadata>

<interactive_prompts>
  "I can reference external documentation to ensure accurate technical implementation.
   Would you like me to incorporate any of the following?
   
   1. **Tech Stack Documentation** 
      Examples: FastAPI docs, Next.js guides, Django documentation
      
   2. **External API Documentation**
      Examples: Stripe API, Auth0, AWS services, custom APIs
      
   3. **Internal Standards & Architecture**
      Examples: Company style guides, architecture decisions, design systems
      
   4. **Compliance & Security Requirements**
      Examples: HIPAA, SOC2, GDPR, security policies
   
   For each category you want to include:
   - Provide a URL to fetch documentation from, OR
   - Provide a local file path (starting with / or ~), OR
   - Type 'skip' to proceed without
   
   Format: [category_number]: [url_or_path_or_skip]"
</interactive_prompts>

<documentation_processing>
  FOR each provided documentation:
    1. Validate source accessibility
    2. Fetch content using appropriate handler
    3. Extract relevant patterns and constraints
    4. Store in docs-registry.yaml
    5. Include in planning context
</documentation_processing>

<instructions>
  ACTION: Present interactive documentation prompts to user
  PROCESS: Each provided documentation source using appropriate handlers
  VALIDATE: Source accessibility before processing
  STORE: Processed documentation in .agent-os/docs-registry.yaml
  ENRICH: Planning context with extracted patterns and constraints
  CONTINUE: Proceed to next step regardless of user response (skip allowed)
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

<step number="3" subagent="mission-document-creator" name="create_mission_md">

### Step 3: Create mission.md

**Uses:** mission-document-creator subagent for comprehensive mission document creation

Use the mission-document-creator subagent to create the comprehensive `.agent-os/product/mission.md` file that establishes product vision, user personas, competitive positioning, and architecture strategy.

<subagent_context>
  **Context:** User input from Step 1, strategic planning recommendations, product requirements
  **Output:** Complete mission.md file with all required sections
  **Next Step:** Tech stack documentation creation
</subagent_context>

**Mission Foundation:** Product vision, user personas, problems, differentiators, key features, PocketFlow architecture strategy

**Blocking:** Must complete mission document before technical documentation

<instructions>
  ACTION: Use mission-document-creator subagent for mission document creation
  REQUEST: "Create comprehensive mission document with context:
            - Main idea: [MAIN_IDEA_FROM_USER_INPUT]
            - Key features: [KEY_FEATURES_FROM_USER_INPUT]
            - Target users: [TARGET_USERS_FROM_USER_INPUT]
            - Strategic planning: [STRATEGIC_RECOMMENDATIONS_FROM_STEP_1_5]
            - Product requirements: [ALL_GATHERED_REQUIREMENTS]
            - PocketFlow integration: [UNIVERSAL_ARCHITECTURE_STRATEGY]"
  PROCESS: Mission document creation with all required sections
  APPLY: Complete mission.md file creation in .agent-os/product/
</instructions>

</step>

<step number="4" subagent="tech-stack-document-creator" name="create_tech_stack_md">

### Step 4: Create tech-stack.md

**Uses:** tech-stack-document-creator subagent for comprehensive tech stack documentation

Use the tech-stack-document-creator subagent to create the comprehensive `.agent-os/product/tech-stack.md` file with modern Python defaults and universal PocketFlow framework integration.

<subagent_context>
  **Context:** User input, strategic planning, mission requirements, technical preferences
  **Output:** Complete tech-stack.md file with all required sections and modern defaults
  **Next Step:** Initial design document generation
</subagent_context>

**Tech Stack Focus:** Modern Python toolchain, PocketFlow integration, interactive preference gathering, missing items identification

**Blocking:** Must complete tech stack documentation before design document creation

<instructions>
  ACTION: Use tech-stack-document-creator subagent for tech stack documentation
  REQUEST: "Create comprehensive tech stack document with context:
            - User input: [TECH_STACK_PREFERENCES_FROM_USER_INPUT]
            - Mission context: [PRODUCT_REQUIREMENTS_FROM_MISSION]
            - Strategic planning: [TECHNICAL_RECOMMENDATIONS_FROM_STEP_1_5]
            - Modern defaults: [PYTHON_3_12_FASTAPI_PYDANTIC_UV_RUFF_PYTEST]
            - Universal requirements: [POCKETFLOW_CHROMADB_INTEGRATION]
            - Missing items handling: [INTERACTIVE_PREFERENCE_GATHERING]"
  PROCESS: Tech stack documentation with modern Python defaults and PocketFlow integration
  APPLY: Complete tech-stack.md file creation in .agent-os/product/
</instructions>

</step>

<step number="4.5" subagent="design-document-creator" name="generate_initial_design_document">

### Step 4.5: Generate Initial Product Design Document

**Uses:** design-document-creator subagent for comprehensive design document creation

Use the design-document-creator subagent to create the initial `docs/design.md` file that establishes the architectural foundation following PocketFlow's design-first methodology.

<subagent_context>
  **Context:** Mission document, tech stack, strategic planning, pattern validation, product requirements
  **Output:** Complete docs/design.md file with architectural foundation
  **Next Step:** Pre-flight checklist generation
</subagent_context>

**Design Foundation:** PocketFlow architecture, system purpose, pattern selection, data flow, SharedStore schema, utilities identification

**Critical Priority:** Establishes design-first foundation for all future feature development

<instructions>
  ACTION: Use design-document-creator subagent for initial design document creation
  REQUEST: "Create comprehensive initial design document with context:
            - Mission context: [PRODUCT_MISSION_AND_ARCHITECTURE_FROM_MISSION_MD]
            - Tech stack: [TECHNICAL_STACK_FROM_TECH_STACK_MD]
            - Strategic planning: [STRATEGIC_RECOMMENDATIONS_FROM_STEP_1_5]
            - Pattern validation: [PATTERN_RECOMMENDATIONS_FROM_STEP_4_6]
            - Product requirements: [ALL_GATHERED_REQUIREMENTS]
            - Design philosophy: [HUMANS_DESIGN_AGENTS_CODE_METHODOLOGY]"
  PROCESS: Initial design document creation with PocketFlow architectural foundation
  APPLY: Complete docs/design.md file creation with TODO templates for future expansion
</instructions>

</step>

<step number="4.6" subagent="pattern-analyzer" name="technical_pattern_validation">

### Step 4.6: Technical Pattern Validation

**Uses:** pattern-analyzer subagent for technical pattern validation

Use the pattern-analyzer subagent to validate the recommended technical patterns and architecture decisions before finalizing the roadmap.

<subagent_context>
  **Context:** Strategic recommendations, technical architecture, product requirements, pattern options
  **Output:** Pattern validation results and optimization recommendations
  **Next Step:** Roadmap features with optimal PocketFlow patterns
</subagent_context>

**Validation Focus:** PocketFlow pattern suitability, technical compatibility, team capability alignment

**Fallback:** Use Agent pattern for complex or unclear cases

<instructions>
  ACTION: Use pattern-analyzer subagent for technical pattern validation
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

<step number="5.5" subagent="pre-flight-checklist-creator" name="generate_prelight_checklist">

### Step 5.5: Generate Pre-flight Checklist

**Uses:** pre-flight-checklist-creator subagent for comprehensive pre-flight checklist creation

Use the pre-flight-checklist-creator subagent to create the comprehensive `.agent-os/checklists/pre-flight.md` file based on PocketFlow best practices.

<subagent_context>
  **Context:** Design document, tech stack, mission requirements, PocketFlow best practices
  **Output:** Complete pre-flight checklist with 9 critical areas and actionable TODO items
  **Next Step:** Roadmap document creation
</subagent_context>

**Checklist Coverage:** Requirements analysis, architecture planning, data flow design, node selection, utility strategy, error handling, testing, performance, deployment

**Validation Focus:** Ensure all critical PocketFlow best practices are covered with actionable guidance

<instructions>
  ACTION: Use pre-flight-checklist-creator subagent for pre-flight checklist creation
  REQUEST: "Create comprehensive pre-flight checklist with context:
            - Design foundation: [ARCHITECTURAL_FOUNDATION_FROM_DESIGN_MD]
            - Tech stack: [TECHNICAL_REQUIREMENTS_FROM_TECH_STACK_MD]
            - Mission requirements: [PRODUCT_REQUIREMENTS_FROM_MISSION_MD]
            - PocketFlow best practices: [REFERENCE_POCKETFLOW_BEST_PRACTICES_MD]
            - Checklist areas: [9_CRITICAL_AREAS_WITH_ACTIONABLE_TODOS]
            - Documentation links: [RELEVANT_DOCUMENTATION_REFERENCES]"
  PROCESS: Pre-flight checklist creation with PocketFlow best practices integration
  APPLY: Complete pre-flight checklist creation in .agent-os/checklists/
</instructions>

</step>

<step number="6" subagent="roadmap-document-creator" name="create_roadmap_md">

### Step 6: Create roadmap.md

**Uses:** roadmap-document-creator subagent for comprehensive roadmap document creation

Use the roadmap-document-creator subagent to create the comprehensive `.agent-os/product/roadmap.md` file with 5-phase development roadmap and PocketFlow pattern tagging.

<subagent_context>
  **Context:** Mission document, design document, tech stack, pattern validation, strategic planning
  **Output:** Complete roadmap.md file with 5 phases, PocketFlow patterns, and effort estimates
  **Next Step:** CLAUDE.md project documentation creation
</subagent_context>

**Roadmap Structure:** 5 development phases, 3-7 features per phase, PocketFlow pattern tagging, effort estimates, design-first enforcement

**Universal Requirements:** Design document prerequisites, PocketFlow pattern compliance, logical phase progression

<instructions>
  ACTION: Use roadmap-document-creator subagent for roadmap document creation
  REQUEST: "Create comprehensive development roadmap with context:
            - Mission features: [KEY_FEATURES_FROM_MISSION_MD]
            - Design foundation: [ARCHITECTURAL_REQUIREMENTS_FROM_DESIGN_MD]
            - Tech stack: [IMPLEMENTATION_CONSTRAINTS_FROM_TECH_STACK_MD]
            - Pattern validation: [RECOMMENDED_PATTERNS_FROM_STEP_4_6]
            - Strategic priorities: [DEVELOPMENT_PHASES_FROM_STRATEGIC_PLANNING]
            - Universal requirements: [DESIGN_FIRST_POCKETFLOW_PATTERN_TAGGING]"
  PROCESS: Roadmap creation with 5 phases, pattern tagging, and effort estimation
  APPLY: Complete roadmap.md file creation in .agent-os/product/
</instructions>

</step>


<step number="7" subagent="claude-md-manager" name="create_or_update_claude_md">

### Step 7: Create or Update CLAUDE.md

**Uses:** claude-md-manager subagent for CLAUDE.md project documentation management

Use the claude-md-manager subagent to create or update the `CLAUDE.md` file in the project root with Agent OS documentation and workflow references.

<subagent_context>
  **Context:** All created product documents, Agent OS standards, workflow instructions, project structure
  **Output:** Complete or updated CLAUDE.md file with Agent OS documentation section
  **Next Step:** Process completion and validation
</subagent_context>

**Documentation Scope:** Product context references, development standards, project management workflows, merge strategy handling

**File Management:** Smart merge strategy, preserve existing content, cross-document references

<instructions>
  ACTION: Use claude-md-manager subagent for CLAUDE.md documentation management
  REQUEST: "Create or update CLAUDE.md file with Agent OS documentation:
            - Product references: [REFERENCES_TO_MISSION_TECH_STACK_ROADMAP]
            - Generated documents: [ALL_CREATED_PRODUCT_DOCUMENTATION]
            - Workflow instructions: [AGENT_OS_WORKFLOW_COMMANDS_AND_REFERENCES]
            - Development standards: [POCKETFLOW_PRINCIPLES_AND_BEST_PRACTICES]
            - Merge strategy: [INTELLIGENT_SECTION_REPLACEMENT_OR_APPEND]
            - Content preservation: [MAINTAIN_ALL_EXISTING_NON_AGENT_OS_CONTENT]"
  PROCESS: CLAUDE.md creation or update with smart merge strategy
  APPLY: Complete CLAUDE.md file management in project root
</instructions>

</step>

</process_flow>

## Execution Summary

<final_checklist>
  <verify>
    - [ ] All 3 files created in .agent-os/product/
    - [ ] docs/design.md created with architectural foundation
    - [ ] Pre-flight checklist generated in .agent-os/checklists/pre-flight.md
    - [ ] User inputs incorporated throughout
    - [ ] Missing tech stack items requested
    - [ ] CLAUDE.md created or updated with Agent OS documentation
  </verify>
</final_checklist>

<execution_order>
  1. Gather and validate all inputs
  2. Create directory structure
  3. Generate each file sequentially
  4. Generate initial design document (docs/design.md)
  5. Generate pre-flight checklist (.agent-os/checklists/pre-flight.md)
  6. Request any missing information
  7. Create or update project CLAUDE.md file
  8. Validate complete documentation set
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
