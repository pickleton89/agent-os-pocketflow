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

<step number="4.6" subagent="pattern-analyzer" name="technical_pattern_validation">

### Step 4.6: Technical Pattern Validation

**Uses:** pattern-analyzer subagent for technical pattern validation

Use the pattern-analyzer subagent to validate the recommended technical patterns and architecture decisions before finalizing the roadmap.

<subagent_context>
  **Context:** Strategic recommendations, technical architecture, product requirements, pattern options
  **Output:** Pattern validation results and optimization recommendations
  **Next Step:** Coordinated parallel document creation
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

<step number="3-7" subagent="document-orchestration-coordinator" name="parallel_document_creation">

### Steps 3-7: Coordinated Parallel Document Creation

**Uses:** document-orchestration-coordinator subagent for optimized parallel document generation

Use the document-orchestration-coordinator subagent to create all product documents in parallel groups based on dependency analysis, achieving 20%+ performance improvement over sequential execution.

<subagent_context>
  **Context:** User input, strategic planning, documentation requirements, parallel execution patterns
  **Output:** Complete set of product documents with consistency validation
  **Performance Target:** >20% improvement over sequential execution
</subagent_context>

**Parallel Groups:**
- **Group A (Independent)**: mission, tech-stack, design, pre-flight checklist
- **Group B (Dependent)**: roadmap, CLAUDE.md

**Quality Assurance:** Cross-document consistency validation and PocketFlow compliance

<instructions>
  ACTION: Use document-orchestration-coordinator subagent for parallel document creation
  REQUEST: "Coordinate parallel document creation for product planning:
            - User context: [COMPLETE_USER_INPUT_FROM_STEP_1]
            - Strategic planning: [STRATEGIC_RECOMMENDATIONS_FROM_STEP_1_5]
            - Documentation discovery: [EXTERNAL_DOCS_FROM_STEP_1_6]
            - Pattern validation: [VALIDATED_PATTERNS_FROM_STEP_4_6]
            - Target documents: [mission.md, tech-stack.md, design.md, pre-flight.md, roadmap.md, CLAUDE.md]
            - Parallel groups: [GROUP_A_INDEPENDENT, GROUP_B_DEPENDENT]
            - Quality requirements: [CONSISTENCY_VALIDATION, POCKETFLOW_COMPLIANCE]"
  PROCESS: Parallel document creation with dependency management
  VALIDATE: Cross-document consistency and architectural coherence
  REPORT: Performance metrics and completion status
</instructions>

</step>

</process_flow>

## Execution Summary

<final_checklist>
  <verify>
    - [ ] All product documents created in .agent-os/product/ (mission.md, tech-stack.md, roadmap.md)
    - [ ] docs/design.md created with architectural foundation
    - [ ] Pre-flight checklist generated in .agent-os/checklists/pre-flight.md
    - [ ] User inputs incorporated throughout all documents
    - [ ] Missing tech stack items requested and resolved
    - [ ] CLAUDE.md created or updated with Agent OS documentation
    - [ ] Cross-document consistency validation passed
    - [ ] Performance improvement >20% achieved through parallel execution
  </verify>
</final_checklist>

<execution_order>
  1. Gather and validate all inputs
  2. Execute strategic planning and pattern validation
  3. Create directory structure
  4. **Coordinated parallel document creation** using document-orchestration-coordinator
     - Group A (parallel): mission.md, tech-stack.md, design.md, pre-flight.md
     - Group B (dependent): roadmap.md, CLAUDE.md
  5. Cross-document consistency validation
  6. Performance metrics collection and reporting
  7. Request any missing information resolution
  8. Final documentation set validation
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

This instruction integrates with the orchestrator system for coordinated planning and execution. The parallel document creation process is handled by the document-orchestration-coordinator agent as defined in step 3-7 above.

For additional orchestration details, see: [orchestration/orchestrator-hooks.md](../../orchestration/orchestrator-hooks.md)
