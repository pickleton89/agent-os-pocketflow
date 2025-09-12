---
description: Analyze Current Product & Install Agent OS
globs:
alwaysApply: false
version: 1.1
encoding: UTF-8
---

# Analyze Current Product & Install Agent OS

<!-- Process XML blocks first, execute sequentially, analyze code before generating docs -->

## Overview

<purpose>
  - Install Agent OS into an existing codebase
  - Analyze current product state and progress
  - Generate documentation that reflects actual implementation
  - Preserve existing architectural decisions
</purpose>

<context>
  - Part of Agent OS framework
  - Used when retrofitting Agent OS to established products
  - Builds on plan-product.md with codebase analysis
</context>

<prerequisites>
  - Existing product codebase
  - Write access to project root
  - Access to @~/.agent-os/instructions/plan-product.md
</prerequisites>

<process_flow>

<step number="1" name="analyze_existing_codebase">

### Step 1: Analyze Existing Codebase

<step_metadata>
  <action>deep codebase analysis</action>
  <purpose>understand current state before documentation</purpose>
</step_metadata>

<analysis_areas>
  <project_structure>
    - Directory organization
    - File naming patterns
    - Module structure
    - Build configuration
  </project_structure>
  <technology_stack>
    - **Primary Language Detection**: Python version (3.8+), Node.js, Ruby, etc.
    - **Python Stack Specifics**: FastAPI vs Django vs Flask, Pydantic usage, uv package management
    - **Dependencies**: pyproject.toml (uv), requirements.txt (legacy), package.json, Gemfile
    - **Development Tools**: Ruff (linting/formatting), ty (type checking), pytest (testing)
    - **Database Systems**: SQLite, PostgreSQL, MongoDB, ChromaDB (vector store)
    - **Infrastructure Configuration**: Docker, deployment scripts, CI/CD
  </technology_stack>
  <implementation_progress>
    - Completed features and current functionality
    - Work in progress and incomplete implementations
    - Authentication/authorization mechanisms
    - **API Layer Analysis**: FastAPI routes, Pydantic models, middleware
    - **Database Layer**: Schema structure, ORM usage, migrations
    - **PocketFlow Component Detection**:
      - Core files: `nodes.py`, `flow.py`, `main.py` entry point
      - Utility functions: `utils/` directory structure and LLM integrations
      - **Design documentation analysis**: 
        - `docs/design.md` presence and location (absolute requirement)
        - Existing design document completeness assessment
        - Architecture sections coverage (Nodes, Flows, SharedStore, Integrations)
        - Missing sections identification for existing docs
      - Node types: AsyncNode, BatchNode, custom implementations
      - Flow patterns: Agent, RAG, Workflow, MapReduce, Multi-Agent
      - SharedStore usage: Data structure patterns and Pydantic integration
  </implementation_progress>
  <code_patterns>
    - Coding style in use
    - Naming conventions
    - File organization patterns
    - Testing approach
  </code_patterns>
</analysis_areas>

<universal_analysis>
  <python_stack_requirements>
    <required_files>
      - pyproject.toml (preferred uv format)
      - uv.lock (uv lockfile)
      - main.py with FastAPI imports (FastAPI application)
      - schemas/ directory with Pydantic models (modern structure)
      - ruff.toml or .ruff.toml (Ruff configuration)
    </required_files>
    <universal_stack>
      <enforce>
        - FastAPI for all API projects (universal requirement)
        - Pydantic for all data validation (universal requirement)
        - uv as the sole package manager (universal requirement)
        - Ruff for linting and formatting (universal requirement)
        - ty for type checking (universal requirement)
        - pytest for testing (universal requirement)
      </enforce>
    </universal_stack>
  </python_stack_requirements>
  
  <universal_pocketflow_analysis>
    <required_files>
      - nodes.py (PocketFlow nodes - universal requirement)
      - flow.py (PocketFlow flows - universal requirement)
      - docs/design.md (design-first approach - universal requirement)
      - utils/ with domain-specific functions (universal requirement)
    </required_files>
    <required_patterns>
      - Node class inheritance (AsyncNode, BatchNode)
      - SharedStore usage patterns
      - prep/exec/post lifecycle methods
      - Domain-specific utility functions
    </required_patterns>
    <universal_documentation>
      <document>
        - PocketFlow patterns implemented (Agent, RAG, Workflow, etc.)
        - All node implementations and architecture
        - SharedStore schema design
        - All integrations and utility functions
      </document>
    </universal_documentation>
  </universal_pocketflow_analysis>
</universal_analysis>

<instructions>
  ACTION: Thoroughly analyze the existing codebase with Universal PocketFlow requirements
  ENFORCE: Modern Python stack and PocketFlow architecture universally
  DOCUMENT: Current technologies, features, and patterns with Universal PocketFlow implementation
  IDENTIFY: Architectural decisions already made and gaps to fill
  REQUIRE: Modern Python/FastAPI/Pydantic stack universally
  NOTE: Development progress and PocketFlow compliance status
</instructions>

</step>

<step number="1.5" subagent="pattern-analyzer" name="pocketflow_pattern_analysis">

### Step 1.5: PocketFlow Pattern Analysis

**Uses:** pattern-analyzer subagent for PocketFlow pattern analysis

Use the pattern-analyzer subagent to analyze the existing project for optimal PocketFlow patterns and architectural recommendations.

<subagent_context>
  **Context:** Codebase analysis, tech stack, project complexity, performance needs
  **Output:** Recommended PocketFlow patterns with rationale and implementation guidance
  **Next Step:** Strategic planning and architecture recommendations
</subagent_context>

**Fallback:** Use Agent pattern if analysis inconclusive

<instructions>
  ACTION: Use pattern-analyzer subagent for comprehensive pattern analysis
  REQUEST: "Analyze existing project for optimal PocketFlow pattern recommendations:
            - Codebase analysis: [DETECTED_PROJECT_STRUCTURE_AND_FEATURES]
            - Technology stack: [CURRENT_TECH_STACK_AND_DEPENDENCIES]
            - Existing patterns: [CURRENT_ARCHITECTURE_ANALYSIS]
            - Project complexity: [FEATURE_SCOPE_AND_REQUIREMENTS]
            - Performance needs: [SCALABILITY_AND_INTEGRATION_REQUIREMENTS]
            - Pattern options: Agent, RAG, Workflow, MapReduce, Multi-Agent, Structured Output"
  PROCESS: Pattern recommendations and architectural guidance
  APPLY: Pattern analysis results to strategic planning
</instructions>

</step>

<step number="1.7" subagent="design-document-creator" name="design_document_assessment_and_creation">

### Step 1.7: Design Document Assessment and Creation

**Uses:** design-document-creator subagent for design document handling

<step_metadata>
  <purpose>Ensure all projects have complete design documentation</purpose>
  <handles>existing design.md assessment and creation for missing docs</handles>
  <preserves>existing design content while filling gaps</preserves>
</step_metadata>

<design_document_assessment>
  <check_existing_docs>
    - **Location Detection**: Check for `docs/design.md`, `DESIGN.md`, `design.md` in root, or other design document locations
    - **Content Analysis**: If design document exists, analyze completeness of standard sections:
      - Project Overview and Architecture
      - PocketFlow Patterns (Node types, Flow implementations) 
      - SharedStore schema design
      - LLM integrations and utility functions
      - API design and data models
    - **Gap Identification**: Identify missing or incomplete sections in existing docs
  </check_existing_docs>
  
  <create_or_enhance_design>
    <if_no_design_doc>
      <action>Use design-document-creator subagent to create comprehensive design.md</action>
      <location>docs/design.md (standard location)</location>
      <content>Full design document based on codebase analysis and pattern recommendations</content>
    </if_no_design_doc>
    
    <if_incomplete_design_doc>
      <action>Use design-document-creator subagent to enhance existing document</action>
      <preserve>All existing content and architectural decisions</preserve>
      <enhance>Add missing sections while maintaining existing structure and style</enhance>
    </if_incomplete_design_doc>
  </create_or_enhance_design>
</design_document_assessment>

<subagent_context>
  **Context:** Codebase analysis results, pattern recommendations, existing design content (if any)
  **Input:** Complete technical analysis and pattern recommendations from previous steps
  **Output:** Complete or enhanced design.md document
  **Preservation Rule:** Never overwrite existing architectural decisions or content
</subagent_context>

<instructions>
  ACTION: Use design-document-creator subagent for design document handling
  REQUEST: "Handle design document for existing project:
            - Codebase analysis: [COMPLETE_TECHNICAL_ANALYSIS_FROM_STEP_1]
            - Pattern recommendations: [POCKETFLOW_PATTERNS_FROM_STEP_1_5]
            - Existing design doc: [DETECTED_DESIGN_DOC_LOCATION_AND_CONTENT]
            - Missing sections: [GAP_ANALYSIS_FROM_DESIGN_DOC_ASSESSMENT]
            - Action needed: [CREATE_NEW_OR_ENHANCE_EXISTING]
            - Preservation requirements: [MAINTAIN_EXISTING_DECISIONS_AND_CONTENT]"
  ENSURE: Design document reflects actual codebase state and includes pattern analysis
  PRESERVE: All existing architectural decisions and content in current design docs
  OUTPUT: Complete design.md in standard location with all required sections
</instructions>

</step>

<step number="2" name="gather_product_context">

### Step 2: Gather Product Context

<step_metadata>
  <supplements>codebase analysis</supplements>
  <gathers>business context and future plans</gathers>
</step_metadata>

<context_questions>
  Based on my analysis of your codebase, I can see you're building [OBSERVED_PRODUCT_TYPE].

  To properly set up Agent OS, I need to understand:

  1. **Product Vision**: What problem does this solve? Who are the target users?

  2. **Current State**: Are there features I should know about that aren't obvious from the code?
     - Describe all PocketFlow patterns implemented, underlying integrations, and specific architectural designs used.

  3. **Roadmap**: What features are planned next? Any major refactoring planned?
     - For planned features, specify desired PocketFlow patterns (Agent, Workflow, RAG, MapReduce, etc.).

  4. **Decisions**: Are there important technical or product decisions I should document?
     - Include any strategic decisions related to framework choices and PocketFlow pattern selection.

  5. **Team Preferences**: Any coding standards or practices the team follows that I should capture?
     - Emphasize PocketFlow-specific best practices for all development.
</context_questions>

<instructions>
  ACTION: Ask user for product context
  COMBINE: Merge user input with codebase analysis
  PREPARE: Information for plan-product.md execution
</instructions>

</step>

<step number="2.5" subagent="strategic-planner" name="strategic_analysis_and_recommendations">

### Step 2.5: Strategic Analysis and PocketFlow Integration Recommendations

**Uses:** strategic-planner subagent for strategic analysis and PocketFlow integration

Use the strategic-planner subagent to create strategic analysis and comprehensive PocketFlow integration recommendations based on the codebase analysis and user context.

<subagent_context>
  **Context:** Codebase analysis, pattern recommendations, user vision, development state
  **Output:** Strategic roadmap, migration strategy, and development phase recommendations
  **Next Step:** Plan-product execution and documentation generation
</subagent_context>

**Strategic Focus:**
- Agent OS installation approach and PocketFlow pattern adoption
- Phase-by-phase implementation with priority matrix
- Team training and capability development

**Blocking:** Must achieve strategic clarity before plan-product execution

<instructions>
  ACTION: Use strategic-planner subagent for comprehensive strategic analysis
  REQUEST: "Create strategic analysis and PocketFlow integration recommendations:
            - Codebase state: [COMPLETE_ANALYSIS_FROM_STEP_1]
            - Pattern analysis: [POCKETFLOW_RECOMMENDATIONS_FROM_STEP_1_5]
            - Product context: [USER_VISION_AND_REQUIREMENTS_FROM_STEP_2]
            - Current priorities: [EXISTING_ROADMAP_AND_DEVELOPMENT_STATE]
            - Integration approach: [RETROFIT_AGENT_OS_WITH_POCKETFLOW_PATTERNS]
            - Strategic focus: [OPTIMAL_MIGRATION_AND_IMPLEMENTATION_STRATEGY]"
  PROCESS: Strategic recommendations and implementation roadmap
  APPLY: Strategic analysis to plan-product execution parameters
</instructions>

</step>

<step number="3" name="execute_plan_product">

### Step 3: Execute Plan-Product with Context

<step_metadata>
  <uses>@~/.agent-os/instructions/plan-product.md</uses>
  <modifies>standard flow for existing products</modifies>
</step_metadata>

<execution_parameters>
  <main_idea>[DERIVED_FROM_ANALYSIS_AND_USER_INPUT]</main_idea>
  <key_features>[IDENTIFIED_IMPLEMENTED_AND_PLANNED_FEATURES]</key_features>
  <target_users>[FROM_USER_CONTEXT]</target_users>
  <tech_stack>[DETECTED_FROM_CODEBASE_WITH_MODERN_PYTHON_PRIORITY]</tech_stack>
  <uses_pocketflow_architecture>[TRUE_UNIVERSAL_REQUIREMENT_ALL_PROJECTS]</uses_pocketflow_architecture>
</execution_parameters>

<tech_stack_resolution>
  <priority_order>
    1. **If Python detected**: Prioritize uv/Ruff/ty stack (FastAPI, Pydantic, uv, Ruff, ty)
    2. **Universal PocketFlow**: Document all existing patterns, implement missing components
    3. **If legacy Python tools**: Document current state but suggest migration to uv/Ruff/ty
    4. **If other frameworks**: Document but suggest migration path to modern Python stack
  </priority_order>
  <detection_logic>
    <python_indicators>
      - pyproject.toml (preferred) or requirements.txt presence
      - uv.lock file (modern uv usage)
      - Python import statements in main files
      - FastAPI, Django, or Flask usage
      - Ruff configuration files
    </python_indicators>
    <pocketflow_indicators>
      - nodes.py and flow.py files
      - SharedStore usage patterns
      - docs/design.md existence
      - LLM utility functions in utils/
    </pocketflow_indicators>
  </detection_logic>
</tech_stack_resolution>

<execution_prompt>
  @~/.agent-os/instructions/plan-product.md

  I'm installing Agent OS into an existing product. Here's what I've gathered:

  **Main Idea**: [SUMMARY_FROM_ANALYSIS_AND_CONTEXT]

  **Key Features**:
  - Already Implemented: [LIST_FROM_ANALYSIS]
  - Planned: [LIST_FROM_USER]

  **Target Users**: [FROM_USER_RESPONSE]

  **Tech Stack**: [DETECTED_STACK_WITH_VERSIONS_AND_MODERN_PYTHON_PRIORITY]

  **Uses PocketFlow Architecture**: [TRUE_UNIVERSAL_REQUIREMENT]
  
  **Detected Patterns**: [POCKETFLOW_PATTERNS_IF_APPLICABLE]
</execution_prompt>

<instructions>
  ACTION: Execute plan-product.md with gathered information
  PROVIDE: All context as structured input
  ALLOW: plan-product.md to create .agent-os/product/ structure
</instructions>

</step>

<step number="4" name="customize_generated_files">

### Step 4: Customize Generated Documentation

<step_metadata>
  <refines>generated documentation</refines>
  <ensures>accuracy for existing product</ensures>
</step_metadata>

<customization_tasks>
  <roadmap_adjustment>
    - Mark completed features as done
    - Move implemented items to "Phase 0: Already Completed"
    - Adjust future phases based on actual progress
    - **For LLM/AI features:** Ensure they are tagged with the correct PocketFlow pattern.
  </roadmap_adjustment>
  <tech_stack_verification>
    - Verify detected versions are correct
    - Add any missing infrastructure details
    - Document actual deployment setup
    - **For LLM/AI:** Explicitly state PocketFlow as the LLM framework if present.
  </tech_stack_verification>
  <decisions_documentation>
    - Add historical decisions that shaped current architecture
    - Document why certain technologies were chosen
    - Capture any pivots or major changes
    - **For PocketFlow:** Document decisions related to pattern selection, architectural choices, or major implementations.
  </decisions_documentation>
  <llm_strategy_refinement>
    - If LLM/AI components are present, refine the "AI/LLM Strategy" section in `mission.md` based on the analysis.
    - Document currently utilized PocketFlow patterns and LLM providers.
    - Include existing design.md analysis if present
    - Map current node implementations to standard PocketFlow patterns
  </llm_strategy_refinement>
  <design_document_integration>
    - **Preserve Existing Design**: Ensure any pre-existing design.md content is preserved and integrated into Agent OS documentation
    - **Cross-Reference Design**: Link design document findings in mission.md and tech-stack.md for consistency
    - **Update Product Documentation**: Ensure .agent-os/product/ documentation reflects design decisions from existing design.md
    - **Architecture Alignment**: Verify generated roadmap aligns with architectural decisions in existing design documents
    - **Design Document Maintenance**: If design.md was created or enhanced in Step 1.7, ensure it's referenced in Agent OS documentation structure
  </design_document_integration>
</customization_tasks>

<conditional_documentation>
  <python_stack_detected>
    <if_modern_python>
      <apply>
        - Emphasize uv/Ruff/ty stack in tech-stack.md (FastAPI, Pydantic, uv, Ruff, ty)
        - Document existing Pydantic models and schemas/ structure
        - Note modern toolchain usage (specifically uv, Ruff, ty, pytest)
      </apply>
    </if_modern_python>
    <if_legacy_python>
      <apply>
        - Document current stack (Django/Flask/pip/poetry/black/mypy)
        - Suggest migration path to uv/Ruff/ty stack in roadmap.md notes
        - Note specific differences from preferred uv/Ruff/ty defaults
      </apply>
    </if_legacy_python>
  </python_stack_detected>
  
  <pocketflow_detected>
    <if_complete_implementation>
      <apply>
        - Document all existing PocketFlow patterns
        - Map current nodes to design patterns (Agent, RAG, etc.)
        - Include design.md analysis in mission.md
        - Mark LLM features as "Phase 0: Already Completed"
      </apply>
    </if_complete_implementation>
    <if_partial_implementation>
      <apply>
        - Document what exists vs. what's missing
        - Suggest completion roadmap for partial PocketFlow adoption
        - Flag missing design.md as high priority
      </apply>
    </if_partial_implementation>
  </pocketflow_detected>
</conditional_documentation>

<roadmap_template>
  ## Phase 0: Already Completed

  The following features have been implemented:

  - [x] [FEATURE_1] - [DESCRIPTION_FROM_CODE]
      - **LLM Pattern:** [POCKETFLOW_PATTERN] (if applicable)

  ## Phase 1: Current Development

  - [ ] [IN_PROGRESS_FEATURE] - [DESCRIPTION]

  [CONTINUE_WITH_STANDARD_PHASES]
</roadmap_template>

<instructions>
  ACTION: Update generated files to reflect reality
  MODIFY: Roadmap to show completed work
  VERIFY: Tech stack matches actual implementation
  ADD: Historical context notes to roadmap.md
  REFINE: LLM/AI specific documentation based on analysis
  INTEGRATE: Design document content and architectural decisions from existing design.md
  PRESERVE: All existing design decisions while ensuring consistency across Agent OS documentation
</instructions>

</step>

<step number="5" name="final_verification">

### Step 5: Final Verification and Summary

<step_metadata>
  <verifies>installation completeness</verifies>
  <provides>next steps for user</provides>
</step_metadata>

<verification_checklist>
  - [ ] .agent-os/product/ directory created
  - [ ] All product documentation reflects actual codebase
  - [ ] Roadmap shows completed and planned features accurately
  - [ ] Tech stack matches installed dependencies
  - [ ] CLAUDE.md configured (if applicable)
</verification_checklist>

<summary_template>
  ## ✅ Agent OS Successfully Installed

  I've analyzed your [PRODUCT_TYPE] codebase and set up Agent OS with documentation that reflects your actual implementation.

  ### What I Found

  - **Tech Stack**: [SUMMARY_OF_DETECTED_STACK]
  - **Completed Features**: [COUNT] features already implemented
  - **Code Style**: [DETECTED_PATTERNS]
  - **Current Phase**: [IDENTIFIED_DEVELOPMENT_STAGE]
  - **LLM/AI Components**: [PRESENCE_AND_SUMMARY_OF_POCKETFLOW_USAGE]
  - **Modern Python Stack**: [FASTAPI_PYDANTIC_UV_USAGE_STATUS]
  - **Development Toolchain**: [UV_RUFF_TY_PYTEST_USAGE_STATUS]

  ### What Was Created

  - ✓ Product documentation in `.agent-os/product/`
  - ✓ Roadmap with completed work in Phase 0
  - ✓ Tech stack reflecting actual dependencies
  - ✓ Updated LLM Strategy in mission.md (if applicable)

  ### Next Steps

  1. Review the generated documentation in `.agent-os/product/`
  2. Make any necessary adjustments to reflect your vision
  3. See the Agent OS README for usage instructions: https://github.com/pickleton89/agent-os-pocketflow
  4. Start using Agent OS for your next feature:
     ```
     @~/.agent-os/instructions/create-spec.md
     ```

  Your codebase is now Agent OS-enabled! 🚀
</summary_template>

<instructions>
  ACTION: Verify all files created correctly
  SUMMARIZE: What was found and created
  PROVIDE: Clear next steps for user
</instructions>

</step>

</process_flow>

## Error Handling

<error_scenarios>
  <scenario name="no_clear_structure">
    <condition>Cannot determine project type or structure</condition>
    <action>Ask user for clarification about project</action>
  </scenario>
  <scenario name="conflicting_patterns">
    <condition>Multiple coding styles detected</condition>
    <action>Ask user which pattern to document</action>
  </scenario>
  <scenario name="missing_dependencies">
    <condition>Cannot determine full tech stack</condition>
    <action>List detected technologies and ask for missing pieces</action>
  </scenario>
  <scenario name="unclear_llm_usage">
    <condition>LLM/AI components detected but their purpose or pattern is unclear</condition>
    <action>Ask user for clarification on PocketFlow patterns (e.g., "Is this a RAG system, Agent workflow, or MapReduce pattern?") or specific architectural decisions.</action>
  </scenario>
  <scenario name="mixed_python_tooling">
    <condition>Multiple Python package managers or linting tools detected (e.g., poetry + pip, black + Ruff)</condition>
    <action>Recommend migration to uv/Ruff/ty stack for consistency with Agent OS preferences.</action>
  </scenario>
  <scenario name="incomplete_pocketflow">
    <condition>Some PocketFlow files present but missing key components (e.g., design.md)</condition>
    <action>Ask user if they want to complete PocketFlow implementation or document current partial state.</action>
  </scenario>
</error_scenarios>

## Modern Python Toolchain Detection

<preferred_toolchain_detection>
  <package_managers>
    <detect_files>uv.lock (preferred), pyproject.toml (uv format), requirements.txt (legacy), Pipfile (pipenv), poetry.lock (poetry)</detect_files>
    <preferred>uv (exclusively)</preferred>
    <legacy_migration>Suggest migration from poetry/pipenv/pip to uv</legacy_migration>
  </package_managers>
  
  <linting_formatting>
    <detect_files>ruff.toml, .ruff.toml (preferred), setup.cfg, tox.ini (flake8), pyproject.toml (black), .flake8</detect_files>
    <preferred>Ruff (exclusively - replaces black, flake8, isort, etc.)</preferred>
    <legacy_migration>Suggest migration from black+flake8+isort to unified Ruff</legacy_migration>
  </linting_formatting>
  
  <type_checking>
    <detect_files>pyproject.toml (ty/mypy config), mypy.ini, .mypy.ini, pyrightconfig.json</detect_files>
    <detect_usage>ty command wrapper (preferred), mypy direct usage</detect_usage>
    <preferred>ty (mypy wrapper with better UX)</preferred>
    <legacy_migration>Suggest using ty instead of direct mypy calls</legacy_migration>
  </type_checking>
  
  <testing>
    <detect_files>pytest.ini, pyproject.toml (pytest), setup.cfg, tox.ini</detect_files>
    <detect_patterns>test_*.py files, tests/ directory structure</detect_patterns>
    <preferred>pytest (already the standard)</preferred>
    <legacy_migration>Migrate from unittest to pytest if needed</legacy_migration>
  </testing>
  
  <optimal_stack_summary>
    **Preferred Stack:** uv + Ruff + ty + pytest
    **Migration Path:** Any detected legacy tools → Recommend uv/Ruff/ty adoption
    **Detection Priority:** Look for uv.lock and Ruff config as indicators of modern stack
  </optimal_stack_summary>
</preferred_toolchain_detection>

## Execution Summary

<final_checklist>
  <verify>
    - [ ] Codebase analyzed thoroughly
    - [ ] User context gathered
    - [ ] plan-product.md executed with proper context
    - [ ] Documentation customized for existing product
    - [ ] Team can adopt Agent OS workflow
  </verify>
</final_checklist>
