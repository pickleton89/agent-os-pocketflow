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

<step number="2" subagent="context-manager" name="context_gathering">

### Step 2: Context Gathering

<step_metadata>
  <reads>
    - @.agent-os/product/mission.md
    - @.agent-os/product/roadmap.md
    - @.agent-os/product/tech-stack.md
  </reads>
  <purpose>understand spec alignment</purpose>
  <uses>context-manager subagent</uses>
</step_metadata>

<subagent_context>
  **Context:** Product documentation analysis for spec alignment
  **Output:** Consolidated context analysis with PocketFlow pattern recommendations
  **Next Step:** Requirements clarification with informed context
</subagent_context>

<context_analysis>
  <mission>overall product vision</mission>
  <roadmap>current progress and plans</roadmap>
  <tech_stack>technical requirements</tech_stack>
  <pocketflow_pattern_analysis>determine appropriate PocketFlow pattern for all projects</pocketflow_pattern_analysis>
</context_analysis>

<instructions>
  ACTION: Use context-manager subagent for product document analysis
  REQUEST: "Analyze product documentation for spec alignment:
            - Mission: @.agent-os/product/mission.md
            - Roadmap: @.agent-os/product/roadmap.md  
            - Tech Stack: @.agent-os/product/tech-stack.md
            - Focus: PocketFlow pattern recommendations and implementation implications"
  PROCESS: Returned context analysis and pattern recommendations
  ANALYZE: Spec alignment with each document
  NOTE: Consider implications for implementation and PocketFlow architecture pattern selection.
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

<documentation_discovery>
  <pattern_detection>
    ANALYZE spec requirements for technology mentions
    IF detected_technology NOT IN current_docs_registry:
      PROMPT: "I noticed you're using [TECHNOLOGY]. 
               Would you like me to reference its documentation?
               [URL/path/skip]:"
  </pattern_detection>
  
  <feature_specific_docs>
    Based on feature type, suggest relevant documentation:
    - Payment features → Payment provider docs
    - Auth features → Auth service docs
    - Data processing → Database/queue docs
    - UI components → Component library docs
  </feature_specific_docs>
</documentation_discovery>

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
  <pocketflow_specifics>
    - **For all projects using PocketFlow architecture:**
      - Desired PocketFlow design pattern (WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE, STRUCTURED-OUTPUT)
      - Specific providers/models to use (when applicable)
      - Data sources and integrations required
      - Expected input/output formats
      - Performance requirements (latency, throughput)
      - Pattern complexity level (Simple, Enhanced, Complex)
  </pocketflow_specifics>
</clarification_areas>

<clarification_process>
  **If clarification needed:** Ask numbered questions, wait for user response
  **Otherwise:** Proceed to date determination
  
  **Question Template:**
  1. [SCOPE_QUESTION]
  2. [TECHNICAL_APPROACH_QUESTION]  
  3. [USER_EXPERIENCE_QUESTION]
  [ADD_LLM_QUESTIONS_IF_APPLICABLE]
</clarification_process>

<instructions>
  ACTION: Perform pattern detection for documentation needs
  SUGGEST: Relevant documentation based on feature type  
  EVALUATE: Need for clarification after documentation discovery
  ASK: Numbered questions if needed
  PROCEED: Only with clear requirements
  PRIORITIZE: PocketFlow pattern and architecture questions for all projects.
</instructions>

</step>

<step number="3.5" name="best_practices_precheck">

### Step 3.5: Best Practices Pre-Check

<step_metadata>
  <purpose>Early design validation to prevent downstream issues</purpose>
  <priority>critical - validates design feasibility</priority>
  <educational>provides early feedback for learning</educational>
</step_metadata>

<validation_philosophy>
  <early_detection>
    Following PocketFlow's principle: "Humans design, agents code"
    Catch design issues before implementation begins
    Provide educational feedback for better decision-making
  </early_detection>
</validation_philosophy>

<precheck_areas>
  <requirements_analysis>
    **Validate Requirements Fitness:**
    - [ ] Problem is suitable for AI automation (not better solved with traditional programming)
    - [ ] Clear input/output definitions exist
    - [ ] Task complexity appropriate (can be broken into discrete, testable steps)
    - [ ] Human oversight points identified vs. automatable tasks
    
    **Assessment Questions:**
    - Can a human manually solve this with clear, repeatable steps?
    - Are success criteria measurable and specific?
    - Is this genuinely benefited by LLM capabilities vs. deterministic logic?
  </requirements_analysis>
  
  <architecture_readiness>
    **Design Foundation Check:**
    - [ ] PocketFlow pattern selection has clear rationale
    - [ ] Flow complexity matches problem scope (not over/under-engineered)
    - [ ] Error handling and failure modes considered
    - [ ] External dependencies identified and justified
    
    **Pattern Selection Guidance:**
    - Simple data processing → WORKFLOW pattern
    - Complex decision-making → AGENT pattern  
    - Information retrieval → RAG pattern
    - Collection processing → MAPREDUCE pattern
  </architecture_readiness>
  
  <data_flow_validation>
    **Shared Store Planning:**
    - [ ] Data structure supports planned operations
    - [ ] Node responsibilities clearly separable
    - [ ] No state stored in nodes (only in shared store)
    - [ ] Data dependencies form valid flow graph
    
    **Red Flags to Catch:**
    - Circular data dependencies
    - Monolithic data structures
    - Unclear node boundaries
    - Missing error data paths
  </data_flow_validation>
</precheck_areas>

<validation_process>
  <execution_steps>
    1. **Requirements Fitness Review**: Evaluate each requirement against validation criteria
    2. **Pattern Appropriateness Check**: Confirm chosen pattern matches problem characteristics
    3. **Design Readiness Assessment**: Verify sufficient planning for next steps
    4. **Issue Documentation**: Record any concerns or recommendations
  </execution_steps>
  
  <decision_matrix>
    IF all_validations_pass:
      PROCEED to date determination
    ELIF minor_issues_identified:
      DOCUMENT recommendations and proceed with caution
      NOTE areas for extra attention during design phase
    ELSE major_issues_found:
      HALT progression and request requirement clarification
      PROVIDE specific guidance for addressing issues
  </decision_matrix>
</validation_process>

<educational_outcomes>
  <learning_objectives>
    - Understand PocketFlow pattern selection rationale
    - Recognize early warning signs of design problems
    - Appreciate importance of clear requirements before coding
    - Build intuition for appropriate complexity levels
  </learning_objectives>
  
  <feedback_format>
    **Validation Summary:**
    ✅ Requirements Analysis: [PASS/CONCERN/FAIL]
    ✅ Architecture Readiness: [PASS/CONCERN/FAIL] 
    ✅ Data Flow Planning: [PASS/CONCERN/FAIL]
    
    **Recommendations:**
    - [Specific guidance for improvement areas]
    - [Educational notes about design decisions]
    - [References to relevant best practices sections]
  </feedback_format>
</educational_outcomes>

<instructions>
  ACTION: Perform systematic pre-check validation
  EDUCATE: Explain rationale for validation decisions
  DOCUMENT: Record concerns and recommendations
  DECIDE: Proceed, proceed with caution, or halt for clarification
  REFERENCE: Link to relevant sections in @docs/POCKETFLOW_BEST_PRACTICES.md
</instructions>

</step>

<step number="4" name="date_determination">

### Step 4: Date Determination

<step_metadata>
  <purpose>Ensure accurate date for folder naming</purpose>
  <priority>high</priority>
  <uses>date-checker subagent</uses>
</step_metadata>

<date_determination_process>
  <instructions>
    ACTION: Use the date-checker subagent to determine today's date
    STORE: Date in YYYY-MM-DD format for folder naming
    NOTE: The subagent will handle all validation and fallback methods
  </instructions>
</date_determination_process>

</step>

<step number="4.5" name="mandatory_design_document_creation">

### Step 4.5: Mandatory Design Document Creation (Universal)

<step_metadata>
  <creates>
    - file: docs/design.md
  </creates>
  <condition>universal for all projects using PocketFlow architecture</condition>
  <priority>critical - blocks implementation progression</priority>
</step_metadata>

<design_document_requirement>
  <philosophy>
    Following PocketFlow's methodology: **Humans design, agents code**.
    Design must be completed before any implementation begins for all projects.
  </philosophy>
  <blocking_condition>
    Implementation tasks CANNOT proceed without completed design.md
  </blocking_condition>
</design_document_requirement>

<template_reference>
  **Template:** Use appropriate design document template from @templates/pocketflow-templates.md
  **Sections Required (adapted to pattern complexity):**
  - Requirements (with PocketFlow pattern classification)
  - Flow Design (with Mermaid diagram)
  - Utilities (with input/output contracts)
  - Data Design (SharedStore schema or data structures)
  - Node Design (prep/exec/post specifications for chosen pattern)
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

<design_creation_failure_handling>
  IF design_document_creation_fails:
    - Document specific template or content generation failures
    - Attempt manual design document creation using fallback templates
    - Request user assistance for pattern selection if unclear
    - BLOCK all subsequent steps until design document is complete
  ELSE:
    - Proceed with validated design document
</design_creation_failure_handling>

<instructions>
  ACTION: Create docs/design.md using appropriate PocketFlow pattern template
  TEMPLATE: @templates/pocketflow-templates.md (Pattern-specific Design Document Template)
  BLOCK: Do not proceed to implementation steps without completed design
  VALIDATE: Ensure all sections are filled with specific details for chosen pattern
  EMPHASIZE: This is the foundation for all subsequent PocketFlow implementation
  BLOCK: Progression on design document creation failures
</instructions>

</step>

<step number="5" name="pattern_selection_validation">

### Step 5: Pattern Selection Validation

<step_metadata>
  <purpose>Validate chosen PocketFlow pattern and design document quality</purpose>
  <depends_on>completed design document from step 4.5</depends_on>
  <priority>critical - prevents antipattern implementation</priority>
  <blocks_progression>implementation cannot proceed with invalid patterns</blocks_progression>
</step_metadata>

<validation_philosophy>
  <design_quality_gate>
    The design document represents the human-designed architecture.
    This validation ensures the design follows PocketFlow best practices
    before any code generation or implementation begins.
  </design_quality_gate>
</validation_philosophy>

<pattern_validation_areas>
  <pattern_appropriateness>
    **PocketFlow Pattern Validation:**
    - [ ] **WORKFLOW**: Simple linear/conditional flows with clear data transformations
    - [ ] **TOOL**: Single-purpose utilities with defined input/output contracts
    - [ ] **AGENT**: Complex decision-making with multiple interaction patterns
    - [ ] **RAG**: Information retrieval and context-augmented generation
    - [ ] **MAPREDUCE**: Collection processing with batch operations
    - [ ] **STRUCTURED-OUTPUT**: Data extraction and formatting tasks
    
    **Pattern Selection Criteria:**
    - Does the pattern match the problem complexity?
    - Are the node types appropriate for the chosen pattern?
    - Is the pattern over/under-engineered for the use case?
  </pattern_appropriateness>
  
  <design_document_quality>
    **Required Sections Validation:**
    - [ ] Requirements section: Complete with specific PocketFlow pattern classification
    - [ ] Flow Design: Mermaid diagram showing node connections and data flow
    - [ ] Utilities: Input/output contracts for external integrations
    - [ ] Data Design: Complete SharedStore schema definition
    - [ ] Node Design: prep/exec/post specifications for chosen pattern
    - [ ] Error Handling: Failure modes and recovery paths specified
    
    **Quality Indicators:**
    - Clear separation of concerns between nodes
    - Proper node lifecycle utilization (prep/exec/post)
    - Realistic complexity assessment
    - Testable component boundaries
  </design_document_quality>
  
  <antipattern_detection>
    **Early Antipattern Warning Signs:**
    - [ ] **Monolithic Node Syndrome**: Nodes with multiple responsibilities
    - [ ] **Lifecycle Confusion**: prep/exec/post methods with wrong responsibilities
    - [ ] **SharedStore Violations**: Direct store access planned in exec() methods
    - [ ] **Business Logic in Utils**: Complex decision-making in utility functions
    - [ ] **Wrong Node Types**: Batch operations using regular Node instead of BatchNode
    
    **Red Flag Patterns:**
    - Node names with multiple verbs (ProcessAndValidateNode)
    - exec() methods planned to exceed 20 lines
    - Utilities that contain LLM calls or business logic
    - Direct external service calls in node methods
  </antipattern_detection>
</pattern_validation_areas>

<validation_execution>
  <systematic_review>
    1. **Pattern Appropriateness Analysis**: Review chosen pattern against problem requirements
    2. **Design Document Completeness Check**: Verify all required sections are detailed
    3. **Node Architecture Validation**: Confirm proper single responsibility and lifecycle usage
    4. **Data Flow Analysis**: Validate SharedStore schema and node interactions
    5. **Antipattern Detection**: Scan for common design mistakes
  </systematic_review>
  
  <validation_decision_matrix>
    IF pattern_validated AND design_complete AND no_antipatterns:
      APPROVE design and proceed to spec folder creation
      LOG successful validation for reference
    ELIF minor_issues_identified:
      DOCUMENT specific improvement recommendations
      REQUEST targeted design document updates
      RETRY validation after corrections
    ELSE major_issues_found:
      HALT progression and require design revision
      PROVIDE specific guidance for pattern/design fixes
      REFERENCE relevant sections of best practices documentation
  </validation_decision_matrix>
</validation_execution>

<validation_feedback>
  <comprehensive_report>
    **Pattern Selection Validation Results:**
    
    ✅ **Pattern Appropriateness**: [APPROVED/NEEDS_REVISION/REJECTED]
    - Chosen Pattern: [PATTERN_NAME]
    - Complexity Match: [APPROPRIATE/OVER_ENGINEERED/UNDER_ENGINEERED]
    - Node Types: [CORRECT/NEEDS_ADJUSTMENT]
    
    ✅ **Design Document Quality**: [COMPLETE/NEEDS_WORK/INSUFFICIENT]
    - Required Sections: [X/7] complete
    - Mermaid Diagram: [VALID/NEEDS_REVISION/MISSING]
    - SharedStore Schema: [COMPLETE/INCOMPLETE/UNCLEAR]
    
    ✅ **Antipattern Check**: [CLEAN/MINOR_CONCERNS/MAJOR_ISSUES]
    - Single Responsibility: [PASS/FAIL]
    - Lifecycle Usage: [CORRECT/CONFUSED/UNCLEAR]
    - Node Type Selection: [APPROPRIATE/INCORRECT]
    
    **Specific Recommendations:**
    [Detailed guidance for any identified issues]
    
    **Next Steps:**
    [PROCEED/REVISE_AND_RETRY/MAJOR_REDESIGN_NEEDED]
  </comprehensive_report>
  
  <educational_value>
    **Learning Outcomes:**
    - Understanding of chosen pattern strengths and limitations
    - Recognition of proper node architecture principles
    - Appreciation for design-first methodology benefits
    - Familiarity with common antipatterns to avoid
  </educational_value>
</validation_feedback>

<design_revision_support>
  <common_fixes>
    **Pattern Selection Issues:**
    - WORKFLOW → AGENT: When decision complexity is underestimated
    - AGENT → WORKFLOW: When complexity is overestimated
    - Regular Node → BatchNode: When collection processing is identified
    - Monolithic → Decomposed: When single nodes have multiple responsibilities
    
    **Design Document Improvements:**
    - Add missing Mermaid diagram with proper flow notation
    - Expand SharedStore schema with complete key definitions
    - Separate monolithic nodes into single-responsibility components
    - Add error handling branches to flow diagram
  </common_fixes>
  
  <retry_process>
    AFTER design_document_updates:
      RE_RUN pattern selection validation
      COMPARE improvements against previous validation
      DOCUMENT lessons learned for future reference
  </retry_process>
</design_revision_support>

<instructions>
  ACTION: Perform comprehensive pattern and design validation
  ANALYZE: @docs/design.md against best practices criteria
  DETECT: Early warning signs of implementation antipatterns
  EDUCATE: Provide specific improvement guidance when needed
  BLOCK: Progression on major validation failures until resolved
  REFERENCE: @docs/POCKETFLOW_BEST_PRACTICES.md for detailed guidance
</instructions>

</step>

<step number="6" name="spec_folder_creation">

### Step 6: Spec Folder Creation

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

<folder_creation_failure_handling>
  IF spec_folder_creation_fails:
    - Document file system errors or permission issues
    - Attempt folder creation with alternative naming
    - Check for existing folder conflicts and resolve
    - BLOCK progression until folder successfully created
  ELSE:
    - Proceed with successfully created spec folder
</folder_creation_failure_handling>

<instructions>
  ACTION: Create spec folder using stored date
  FORMAT: Use kebab-case for spec name
  LIMIT: Maximum 5 words in name
  VERIFY: Folder created successfully
  BLOCK: Progression on folder creation failures
</instructions>

</step>

<step number="7" subagent="spec-document-creator" name="create_spec_md">

### Step 7: Create spec.md

**Uses:** spec-document-creator subagent for comprehensive spec requirements document creation

Use the spec-document-creator subagent to create the comprehensive `.agent-os/specs/YYYY-MM-DD-spec-name/spec.md` file that establishes spec overview, user stories, scope definitions, and PocketFlow architecture integration.

<subagent_context>
  **Context:** Requirements clarification from steps 1-3.5, pattern validation, design document foundation
  **Output:** Complete spec.md file with all required sections
  **Next Step:** Technical specification creation
</subagent_context>

**Spec Foundation:** Overview, user stories, scope, expected deliverables, API & data models, PocketFlow architecture

**Blocking:** Must complete spec document before technical specifications

<spec_file_creation_failure_handling>
  IF spec_file_creation_fails:
    - Document subagent errors or context preparation failures
    - Attempt fallback spec.md creation using embedded templates
    - Verify spec folder exists and is accessible
    - BLOCK progression until spec.md is successfully created
  ELSE:
    - Proceed with successfully created spec.md
</spec_file_creation_failure_handling>

<instructions>
  ACTION: Use spec-document-creator subagent for spec requirements document creation
  REQUEST: "Create comprehensive spec requirements document with context:
            - Spec name: [SPEC_NAME_FROM_FOLDER_CREATION]
            - Requirements clarification: [CLARIFIED_REQUIREMENTS_FROM_STEP_3]
            - Pattern validation: [VALIDATION_RESULTS_FROM_STEP_5]
            - Design document: [DESIGN_DOCUMENT_FROM_STEP_4_5]
            - Project context: [PRODUCT_CONTEXT_FROM_STEP_2]
            - PocketFlow patterns: [PATTERN_RECOMMENDATIONS_AND_VALIDATION]"
  PROCESS: Spec document creation with all required sections
  APPLY: Complete spec.md file creation in .agent-os/specs/[YYYY-MM-DD-spec-name]/
  BLOCK: Progression on spec file creation failures
</instructions>

</step>

<step number="8" subagent="technical-spec-creator" name="create_technical_spec">

### Step 8: Create Technical Specification

**Uses:** technical-spec-creator subagent for comprehensive technical specification creation

Use the technical-spec-creator subagent to create the comprehensive `sub-specs/technical-spec.md` file that establishes functionality details, UI/UX specifications, integration requirements, and PocketFlow architecture implementation.

<subagent_context>
  **Context:** Spec requirements document from Step 7, pattern validation, design foundation
  **Output:** Complete technical-spec.md file with detailed implementation specifications
  **Next Step:** Database schema creation (conditional)
</subagent_context>

**Technical Foundation:** Functionality details, approach selection, dependencies, Pydantic/FastAPI sections, PocketFlow implementation specifications

**Blocking:** Must complete technical specification before database and API specifications

<technical_spec_creation_failure_handling>
  IF technical_spec_creation_fails:
    - Document subagent errors or context preparation failures
    - Attempt fallback technical-spec.md creation using embedded templates
    - Verify sub-specs folder exists and is accessible
    - BLOCK progression until technical-spec.md is successfully created
  ELSE:
    - Proceed with successfully created technical-spec.md
</technical_spec_creation_failure_handling>

<instructions>
  ACTION: Use technical-spec-creator subagent for technical specification creation
  REQUEST: "Create comprehensive technical specification with context:
            - Spec document: [COMPLETE_SPEC_MD_FROM_STEP_7]
            - Design document: [DESIGN_DOCUMENT_FROM_STEP_4_5]
            - Pattern validation: [VALIDATION_RESULTS_FROM_STEP_5]
            - Requirements clarification: [CLARIFIED_REQUIREMENTS_FROM_STEP_3]
            - Project context: [PRODUCT_CONTEXT_FROM_STEP_2]
            - PocketFlow architecture: [PATTERN_SPECIFICATIONS_AND_IMPLEMENTATION_GUIDANCE]"
  PROCESS: Technical specification creation with all required sections
  APPLY: Complete technical-spec.md file creation in sub-specs/ directory
  BLOCK: Progression on technical specification creation failures
</instructions>

</step>

<step number="9" name="create_database_schema">

### Step 9: Create Database Schema (Conditional)

<step_metadata>
  <creates>
    - file: sub-specs/database-schema.md
  </creates>
  <condition>only if database changes needed</condition>
  <uses>database-schema-creator subagent</uses>
</step_metadata>

<decision_tree>
  IF spec_requires_database_changes:
    USE database-schema-creator subagent to create sub-specs/database-schema.md
  ELSE:
    SKIP this_step
</decision_tree>

<subagent_context>
  **Context:** Database schema creation for PocketFlow project specification
  **Input:** Technical requirements, existing schema structure, data model specifications
  **Output:** Complete database-schema.md with migration procedures and performance optimizations
  **Conditional Activation:** Only when database changes are identified in technical specification
</subagent_context>

<database_change_detection>
  <analyze_requirements>
    - New data models requiring table creation
    - Existing table modifications for new functionality
    - Database relationship changes (foreign keys, constraints)
    - Performance optimization requirements (indexes, queries)
    - Migration complexity assessment
  </analyze_requirements>

  <decision_criteria>
    DATABASE_CHANGES_NEEDED IF:
    - New tables required for spec functionality
    - Existing table schema modifications needed
    - New relationships or constraints required
    - Performance optimizations or indexing changes needed
    - Data migration procedures required
  </decision_criteria>
</database_change_detection>

<database_schema_creation_failure_handling>
  IF database_schema_creation_fails:
    - Document subagent errors or context preparation failures
    - Attempt fallback database schema creation using embedded templates
    - Verify technical specification contains sufficient database requirements
    - BLOCK progression until database-schema.md is successfully created
  ELSE:
    - Proceed with successfully created database schema specification
</database_schema_creation_failure_handling>

<instructions>
  ACTION: Analyze technical specification for database change requirements
  DETECT: New tables, schema modifications, relationships, and performance needs
  INVOKE: database-schema-creator subagent only if database changes required
  CONTEXT: "Create database schema specification for spec: [SPEC_NAME]
            - Technical Requirements: @.agent-os/specs/[YYYY-MM-DD-spec-name]/sub-specs/technical-spec.md
            - Spec Context: @.agent-os/specs/[YYYY-MM-DD-spec-name]/spec.md
            - Focus: Migration procedures, constraints, indexing strategy, and performance optimization"
  SKIP: If no database changes needed for the specification
  BLOCK: Progression on database schema creation failures
</instructions>

</step>

<step number="10" name="create_api_spec">

### Step 10: Create API Specification (Conditional)

<step_metadata>
  <creates>
    - file: sub-specs/api-spec.md
  </creates>
  <condition>only if API changes needed</condition>
  <uses>api-spec-creator subagent</uses>
</step_metadata>

<decision_tree>
  IF spec_requires_api_changes:
    USE api-spec-creator subagent to create sub-specs/api-spec.md
  ELSE:
    SKIP this_step
</decision_tree>

<subagent_context>
  **Context:** API specification creation for PocketFlow project specification
  **Input:** Technical requirements, existing API structure, endpoint specifications
  **Output:** Complete api-spec.md with FastAPI endpoints, Pydantic models, and PocketFlow integration
  **Conditional Activation:** Only when API changes are identified in technical specification
</subagent_context>

<api_change_detection>
  <analyze_requirements>
    - New API endpoints required for spec functionality
    - Existing endpoint modifications or extensions
    - New data models requiring API exposure
    - Authentication and authorization changes
    - PocketFlow workflow integration endpoints
  </analyze_requirements>

  <decision_criteria>
    API_CHANGES_NEEDED IF:
    - New REST endpoints required for functionality
    - Existing API endpoints need modification or extension
    - New Pydantic models require API exposure
    - Authentication/authorization patterns need updates
    - PocketFlow workflow integration requires API access
    - External service integrations need API wrappers
  </decision_criteria>
</api_change_detection>

<api_spec_creation_failure_handling>
  IF api_spec_creation_fails:
    - Document subagent errors or context preparation failures
    - Attempt fallback API specification creation using embedded templates
    - Verify technical specification contains sufficient API requirements
    - BLOCK progression until api-spec.md is successfully created
  ELSE:
    - Proceed with successfully created API specification
</api_spec_creation_failure_handling>

<instructions>
  ACTION: Analyze technical specification for API change requirements
  DETECT: New endpoints, model modifications, authentication changes, and PocketFlow integrations
  INVOKE: api-spec-creator subagent only if API changes required
  CONTEXT: "Create API specification for spec: [SPEC_NAME]
            - Technical Requirements: @.agent-os/specs/[YYYY-MM-DD-spec-name]/sub-specs/technical-spec.md
            - Spec Context: @.agent-os/specs/[YYYY-MM-DD-spec-name]/spec.md
            - Focus: FastAPI endpoints, Pydantic models, authentication patterns, and PocketFlow integration"
  SKIP: If no API changes needed for the specification
  BLOCK: Progression on API specification creation failures
</instructions>

</step>

<step number="11" subagent="test-spec-creator" name="create_tests_spec">

### Step 11: Create Tests Specification

**Uses:** test-spec-creator subagent for comprehensive test specification creation

Use the test-spec-creator subagent to create the comprehensive `sub-specs/tests.md` file that establishes complete test coverage, mocking requirements, and universal PocketFlow pattern tests.

<subagent_context>
  **Context:** Technical specification from Step 8, spec requirements from Step 7, PocketFlow pattern implementation
  **Output:** Complete tests.md file with comprehensive test coverage specifications
  **Next Step:** User review of all documentation
</subagent_context>

**Test Foundation:** Unit tests, integration tests, feature tests, mocking requirements, PocketFlow pattern-specific tests

**Blocking:** Must complete test specification before user review phase

<test_spec_creation_failure_handling>
  IF test_spec_creation_fails:
    - Document subagent errors or context preparation failures
    - Attempt fallback tests.md creation using embedded templates
    - Verify sub-specs folder exists and is accessible
    - BLOCK progression until tests.md is successfully created
  ELSE:
    - Proceed with successfully created tests.md
</test_spec_creation_failure_handling>

<instructions>
  ACTION: Use test-spec-creator subagent for test specification creation
  REQUEST: "Create comprehensive test specification with context:
            - Technical specification: [TECHNICAL_SPEC_FROM_STEP_8]
            - Spec requirements: [SPEC_DOCUMENT_FROM_STEP_7]
            - Design document: [DESIGN_DOCUMENT_FROM_STEP_4_5]
            - PocketFlow patterns: [PATTERN_SPECIFICATIONS_AND_TESTING_REQUIREMENTS]
            - Database changes: [DATABASE_SCHEMA_IF_CREATED_IN_STEP_9]
            - API changes: [API_SPECIFICATION_IF_CREATED_IN_STEP_10]"
  PROCESS: Test specification creation with all required coverage areas
  APPLY: Complete tests.md file creation in sub-specs/ directory
  BLOCK: Progression on test specification creation failures
</instructions>

</step>

<step number="12" name="user_review">

### Step 12: User Review

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

<step number="13" subagent="task-breakdown-creator" name="create_tasks">

### Step 13: Create tasks.md

**Uses:** task-breakdown-creator subagent for comprehensive task breakdown creation

Use the task-breakdown-creator subagent to create the comprehensive `tasks.md` file with appropriate pattern-specific templates, proper phase dependencies, and toolchain validation.

<subagent_context>
  **Context:** All specification documents from Steps 7-11, user approval from Step 12, PocketFlow pattern complexity
  **Output:** Complete tasks.md file with appropriate phase breakdown and dependencies
  **Next Step:** Documentation cross-references update
</subagent_context>

**Task Foundation:** Pattern-specific templates, phase dependencies, toolchain validation, proper complexity matching

**Blocking:** Must complete task breakdown after user approval and before cross-references

<task_breakdown_creation_failure_handling>
  IF task_breakdown_creation_fails:
    - Document subagent errors or context preparation failures
    - Attempt fallback tasks.md creation using embedded templates
    - Verify pattern complexity assessment and template selection
    - BLOCK progression until tasks.md is successfully created
  ELSE:
    - Proceed with successfully created tasks.md
</task_breakdown_creation_failure_handling>

<instructions>
  ACTION: Use task-breakdown-creator subagent for task breakdown creation
  REQUEST: "Create comprehensive task breakdown with context:
            - Spec requirements: [SPEC_DOCUMENT_FROM_STEP_7]
            - Technical specification: [TECHNICAL_SPEC_FROM_STEP_8]
            - Database schema: [DATABASE_SCHEMA_IF_CREATED_IN_STEP_9]
            - API specification: [API_SPEC_IF_CREATED_IN_STEP_10]
            - Test specification: [TEST_SPEC_FROM_STEP_11]
            - Design document: [DESIGN_DOCUMENT_FROM_STEP_4_5]
            - PocketFlow pattern: [PATTERN_COMPLEXITY_AND_TEMPLATE_SELECTION]
            - User approval: [CONFIRMED_FROM_STEP_12]"
  PROCESS: Task breakdown creation with appropriate pattern-specific templates
  APPLY: Complete tasks.md file creation in spec root directory
  BLOCK: Progression on task breakdown creation failures
</instructions>

</step>

<step number="14" name="update_cross_references">

### Step 14: Documentation Cross-References

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

<step number="15" name="decision_documentation">

### Step 15: Decision Documentation

<step_metadata>
  <evaluates>strategic impact</evaluates>
</step_metadata>

<decision_analysis>
  <review_against>
    - @.agent-os/product/mission.md
  </review_against>
  <criteria>
    - changes product direction
    - impacts roadmap priorities
    - introduces new technical patterns
    - affects user experience significantly
    - **For PocketFlow components:** Introduces new patterns/providers, changes core architecture patterns, or has significant cost/performance implications
  </criteria>
</decision_analysis>

<decision_tree>
  IF spec_impacts_mission_or_roadmap:
    IDENTIFY key_decisions (max 3)
    DOCUMENT decision_details
    ASK user_for_approval
    IF approved:
      UPDATE roadmap.md with notes if needed
  ELSE:
    STATE "This spec is inline with the current mission and roadmap, so no changes needed to product documentation at this time."
</decision_tree>

<instructions>
  ACTION: Analyze spec for strategic decisions
  IDENTIFY: Up to 3 key strategic considerations if any
  REQUEST: User approval before updating product documentation
  UPDATE: Add notes to roadmap.md if approved
  NOTE: Strategic considerations related to PocketFlow patterns should be documented
</instructions>

</step>

<step number="16" name="execution_readiness">

### Step 16: Execution Readiness Check

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

  Would you like me to proceed with implementing Task 1? I will follow the execution guidelines in @.agent-os/instructions/core/execute-tasks.md and focus only on this first task and its subtasks unless you specify otherwise.

  Type 'yes' to proceed with Task 1, or let me know if you'd like to review or modify the plan first."
</execution_prompt>

<execution_flow>
  IF user_confirms_yes:
    REFERENCE: @.agent-os/instructions/core/execute-tasks.md
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

## Orchestration Integration

@include orchestration/orchestrator-hooks.md

This instruction integrates with the orchestrator system for coordinated specification creation.
