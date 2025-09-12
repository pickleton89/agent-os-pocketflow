# Design-First Implementation Plan: Closing the Gap

> **Project**: Agent OS + PocketFlow Framework Enhancement  
> **Created**: 2025-01-15  
> **Status**: Ready for Implementation  
> **Priority**: Critical - Framework Consistency

## Executive Summary

The agent-os-pocketflow framework preaches design-first methodology but only enforces it during feature development (create-spec/execute-tasks), not during initial product setup (plan-product). This creates a fundamental disconnect where end-users receive excellent design guidance during implementation but lack foundational design structure during product planning.

## Problem Statement

### Current State Issues:
1. **plan-product.md** creates mission.md, tech-stack.md, roadmap.md but NO design.md
2. **No visual architecture** in initial product documentation despite having graph generation capabilities
3. **Missing pre-flight checklist** generation during product setup
4. **Inconsistent design enforcement** - strict during features, absent during planning
5. **Pattern guidance only appears** during spec creation, not roadmap planning

### Impact:
- End-users lack design foundation from day one
- Framework appears to violate its own best practices
- Design-first methodology only partially implemented
- Users may develop without proper architectural planning

## Solution Overview

Enhance the framework to apply design-first methodology consistently from initial product planning through implementation, while preserving the "templates with TODOs" philosophy.

## Implementation Phases

### Phase 1: Core Infrastructure (Priority: Critical)

**Estimated Time**: 1-2 days  
**Goal**: Establish design-first foundation in plan-product.md

#### Task 1.1: Add Initial Design Document Generation to plan-product.md
**Files Modified**: `instructions/core/plan-product.md`

Add new Step 4.5: "Generate Initial Product Design Document"

```markdown
<step number="4.5" name="generate_initial_design_document">
### Step 4.5: Generate Initial Product Design Document

<step_metadata>
  <creates>
    - file: docs/design.md
  </creates>
  <condition>universal for all projects using PocketFlow architecture</condition>
  <priority>critical - establishes design-first foundation</priority>
</step_metadata>

<design_document_requirement>
  <philosophy>
    Following PocketFlow's methodology: **Humans design, agents code**.
    Initial product design establishes architectural foundation before feature development.
  </philosophy>
</design_document_requirement>

<template_content>
  **Template:** Use Initial Product Design template from @templates/pocketflow-templates.md
  **Sections Required:**
  - Product Architecture Overview
  - Primary PocketFlow Patterns (based on feature analysis)
  - System-Wide Data Flow (high-level Mermaid diagram)
  - Core Shared Store Schema (outline)
  - Major System Utilities (identification)
  - Integration Points (external systems)
  - Implementation Phases Alignment (links to roadmap)
</template_content>
```

**Acceptance Criteria**:
- [ ] Step 4.5 added after tech-stack.md creation
- [ ] Generates docs/design.md with TODO templates
- [ ] Includes high-level Mermaid diagram placeholder
- [ ] Links to roadmap phases for implementation planning
- [ ] Validates against PocketFlow Universal Framework requirements

#### Task 1.2: Enhance pocketflow-templates.md with Product Design Template
**Files Modified**: `templates/pocketflow-templates.md`

Add new section: "Initial Product Design Template"

```markdown
## Initial Product Design Template

### Complete docs/design.md Structure for New Products

\`\`\`markdown
# [PRODUCT_NAME] Design Document

> Product: [PRODUCT_NAME]
> Created: [CURRENT_DATE]
> Status: Initial Architecture Planning
> Framework: PocketFlow

**FOUNDATION**: This initial design document establishes the architectural foundation. 
Feature-specific designs will be created during spec development.

## Product Architecture Overview

### System Purpose
[PRODUCT_MISSION_SUMMARY_FROM_MISSION_MD]

### Primary PocketFlow Patterns
Based on planned features, this product will primarily use:
- **[PRIMARY_PATTERN]**: [JUSTIFICATION_FROM_FEATURE_ANALYSIS]
- **[SECONDARY_PATTERN]**: [JUSTIFICATION_IF_APPLICABLE]

### Complexity Assessment
- **Overall Complexity**: [SIMPLE_WORKFLOW/ENHANCED_WORKFLOW/COMPLEX_APPLICATION/LLM_APPLICATION]
- **Rationale**: [BASED_ON_FEATURE_COUNT_AND_INTEGRATION_REQUIREMENTS]

## System-Wide Data Flow

### High-Level Architecture
\`\`\`mermaid
graph TD
    A[User Input] --> B[API Layer]
    B --> C{Processing Required?}
    C -->|Simple| D[Direct Processing]
    C -->|Complex| E[PocketFlow Pipeline]
    E --> F[SharedStore]
    F --> G[Business Logic Nodes]
    G --> H[Output Processing]
    D --> I[Response]
    H --> I
    
    %% TODO: Replace with actual system flow based on your features
\`\`\`

### Major Data Transformations
- **Input**: [TYPICAL_USER_INPUT_FORMATS]
- **Processing**: [CORE_BUSINESS_LOGIC_TRANSFORMATIONS]
- **Output**: [EXPECTED_RESULT_FORMATS]

## Core Shared Store Schema (Outline)

### Initial Schema Planning
\`\`\`python
# TODO: Define based on feature requirements from roadmap
SharedStore = {
    "user_context": "Dict[str, Any]",  # User session and preferences
    "processing_state": "Dict[str, Any]",  # Current operation state
    "results": "Dict[str, Any]",  # Processed outputs
    # Additional keys will be defined during feature spec creation
}
\`\`\`

## Major System Utilities (Identification)

### External Integration Points
- **[UTILITY_CATEGORY_1]**: [EXTERNAL_SERVICES_OR_APIS]
  - TODO: Define input/output contracts during spec creation
- **[UTILITY_CATEGORY_2]**: [FILE_PROCESSING_OR_DATA_HANDLING]
  - TODO: Implement following PocketFlow utility philosophy

### Development Phases Alignment

This design document will evolve through roadmap phases:
- **Phase 1**: [CORE_FEATURES] → Detailed design in specs
- **Phase 2**: [ENHANCEMENT_FEATURES] → Extended design sections
- **Phase 3+**: [ADVANCED_FEATURES] → Additional pattern integration

**Next Steps**: 
1. Use `/create-spec` for each roadmap feature
2. Each spec will extend this foundational design
3. Implementation follows feature-specific design documents
\`\`\`
```

**Acceptance Criteria**:
- [ ] Initial Product Design Template added to templates file
- [ ] Includes TODO placeholders for customization
- [ ] References roadmap phases for implementation planning
- [ ] Follows PocketFlow architectural principles
- [ ] Provides Mermaid diagram template

#### Task 1.3: Update analyze-product.md for Existing Products
**Files Modified**: `instructions/core/analyze-product.md`

Add step to handle existing products that may already have design documents or need them created.

**Acceptance Criteria**:
- [ ] Detects existing docs/design.md files
- [ ] Creates design document for products that lack them
- [ ] Preserves existing design content while adding missing sections

### Phase 2: Visual Enhancement (Priority: High)

**Estimated Time**: 1 day  
**Goal**: Add visual architecture to initial product documentation

#### Task 2.1: Add Mermaid Diagram to mission.md Architecture Strategy
**Files Modified**: `instructions/core/plan-product.md` (mission.md template section)

Enhance the Architecture Strategy section to include a system overview diagram.

```markdown
<section name="architecture_strategy">
  <template>
    ## Architecture Strategy

    **Application Architecture:** PocketFlow-based design

    ### System Overview
    \`\`\`mermaid
    graph TD
        A[Users] --> B[API Endpoints]
        B --> C[PocketFlow Orchestration]
        C --> D[Business Logic Nodes]
        D --> E[SharedStore]
        E --> F[Utility Functions]
        F --> G[External Services]
        
        %% TODO: Customize based on your specific architecture
    \`\`\`

    ### Architecture Details
    - **Primary Framework:** PocketFlow
    - **Development Methodology:** Design-first approach with structured workflow patterns
    - **Key Patterns Utilized:** [LIST_POCKETFLOW_PATTERNS]
    - **Integration Pattern:** FastAPI endpoints → PocketFlow Flows → Node execution → Utility functions
  </template>
</section>
```

**Acceptance Criteria**:
- [ ] mission.md includes system overview Mermaid diagram
- [ ] Diagram shows typical PocketFlow application flow
- [ ] TODO comments guide customization
- [ ] Integrates with existing Architecture Strategy content

#### Task 2.2: Enhance Roadmap Features with Pattern Guidance
**Files Modified**: `instructions/core/plan-product.md` (roadmap.md template section)

Add pattern-specific guidance to roadmap feature template.

```markdown
<phase_template>
    ## Phase [NUMBER]: [NAME] ([DURATION])

    **Goal:** [PHASE_GOAL]
    **Success Criteria:** [MEASURABLE_CRITERIA]

    ### Must-Have Features

    - [ ] [FEATURE] - [DESCRIPTION] `[EFFORT]`
        - **PocketFlow Pattern:** [POCKETFLOW_PATTERN]
        - **Node Types**: [SUGGESTED_NODE_TYPES] (Node/AsyncNode/BatchNode)
        - **SharedStore Updates**: [DATA_CHANGES_REQUIRED]
        - **Error Handling**: [ERROR_STRATEGY_APPROACH]
        - **Design Requirement:** `docs/design.md` extension required for implementation

    ### Dependencies
    - [DEPENDENCY]
    - Feature-specific design document sections
    - SharedStore schema updates in docs/design.md
</phase_template>
```

**Acceptance Criteria**:
- [ ] Roadmap features include node type suggestions
- [ ] Error handling strategy identified per feature
- [ ] SharedStore updates planned upfront
- [ ] Links to design document requirements

### Phase 3: Guidance Enhancement (Priority: Medium)

**Estimated Time**: 1 day  
**Goal**: Provide comprehensive guidance and validation

#### Task 3.1: Generate Pre-flight Checklist
**Files Modified**: `instructions/core/plan-product.md`

Add Step 5.5: "Generate Pre-flight Checklist"

```markdown
<step number="5.5" name="generate_prelight_checklist">
### Step 5.5: Generate Pre-flight Checklist

<step_metadata>
  <creates>
    - file: .agent-os/checklists/pre-flight.md
  </creates>
</step_metadata>

<checklist_content>
  Based on @docs/POCKETFLOW_BEST_PRACTICES.md, generate comprehensive checklist covering:
  1. Requirements Analysis
  2. Architecture Planning
  3. Data Flow Design
  4. Node Selection and Design
  5. Utility Function Strategy
  6. Error Handling and Resilience
  7. Testing Strategy
  8. Performance Considerations
  9. Deployment Planning
</checklist_content>
```

**Acceptance Criteria**:
- [ ] Pre-flight checklist generated during plan-product
- [ ] Covers all 9 critical areas from best practices
- [ ] Includes TODO items with guidance
- [ ] Links to relevant documentation

#### Task 3.2: Add Framework Self-Awareness Comments
**Files Modified**: Multiple template files

Add explanatory comments to generated templates explaining the framework's philosophy.

```python
# TODO: Implement your business logic here
# 
# FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
# framework provides templates and structure, but YOU implement the specific
# business logic for your use case.
#
# Why? This ensures maximum flexibility and prevents vendor lock-in.
# 
# Next Steps:
# 1. Review docs/design.md for your specific requirements
# 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
# 3. See @~/.agent-os/standards/best-practices.md for patterns
```

**Acceptance Criteria**:
- [ ] Templates include educational comments
- [ ] Explain why TODOs are intentional
- [ ] Reference relevant documentation
- [ ] Maintain framework philosophy

### Phase 4: Validation and Integration (Priority: Medium)

**Estimated Time**: 1 day  
**Goal**: Ensure consistency and validation

#### Task 4.1: Create Design Evolution Validation
**Files Modified**: `instructions/core/execute-tasks.md`

Enhance design document validation to check for evolution from initial design.

```markdown
<design_evolution_validation>
  <initial_design>docs/design.md (product-level)</initial_design>
  <feature_designs>specs/*/design.md sections</feature_designs>
  <validation_checks>
    - Initial design exists and is complete
    - Feature designs reference and extend initial design
    - No conflicts between initial and feature-specific designs
    - SharedStore schema evolution is consistent
  </validation_checks>
</design_evolution_validation>
```

**Acceptance Criteria**:
- [ ] Validates relationship between initial and feature designs
- [ ] Checks for consistency in SharedStore evolution
- [ ] Ensures no architectural conflicts




## Testing Strategy

### Validation Approach:
1. **Template Generation Testing**: Verify new templates generate correctly
2. **Content Validation**: Ensure generated content follows PocketFlow principles
3. **Integration Testing**: Test full plan-product → create-spec → execute-tasks flow
4. **Framework Consistency**: Verify framework practices what it preaches

### Test Cases:
1. **New Product Setup**: Run plan-product and verify all files created including design.md
2. **Existing Product Analysis**: Run analyze-product on project with/without existing design.md
3. **Design Evolution**: Create spec and verify it properly extends initial design
4. **Validation Blocking**: Ensure execute-tasks blocks without complete design

## Acceptance Criteria Summary

### Phase 1 (Critical):
- [ ] plan-product.md generates docs/design.md with architectural foundation
- [ ] Initial design template created in pocketflow-templates.md
- [ ] analyze-product.md handles existing products with design documents

### Phase 2 (High):
- [ ] mission.md includes system overview Mermaid diagram
- [ ] roadmap.md features include pattern guidance and node suggestions
- [ ] Visual architecture aids understanding

### Phase 3 (Medium):
- [ ] Pre-flight checklist generated during product setup
- [ ] Templates include educational comments explaining framework philosophy
- [ ] Comprehensive guidance provided

### Phase 4 (Medium):
- [ ] Design evolution validation ensures consistency
- [ ] CLAUDE.md updated with design-first workflow
- [ ] End-to-end integration validated

## Success Metrics

### Framework Consistency:
- [ ] Framework enforces design-first from initial product setup through implementation
- [ ] All generated projects have foundational design documents
- [ ] No gaps between stated best practices and actual framework behavior

### User Experience:
- [ ] End-users receive design guidance from day one
- [ ] Clear progression from product planning → feature specs → implementation
- [ ] Educational comments help users understand framework philosophy

### Quality:
- [ ] Generated templates maintain "TODO for customization" approach
- [ ] PocketFlow best practices consistently applied
- [ ] Visual aids improve architectural understanding

## Implementation Notes

### Preserve Framework Philosophy:
- **Templates, not implementations**: Continue providing TODO-filled starting points
- **"Humans design, agents code"**: Enhance human design tools, don't automate decisions
- **Framework awareness**: Remember this IS the framework, generating templates for end-users

### Technical Considerations:
- **Backward compatibility**: Existing projects shouldn't break
- **Template consistency**: Maintain existing patterns and conventions
- **Validation integration**: Work with existing orchestration and validation systems

### Risk Mitigation:
- **Incremental rollout**: Implement phases gradually
- **Testing at each phase**: Validate before moving to next phase
- **Framework testing**: Use existing test-generator.py for validation

## Conclusion

This implementation plan addresses the critical gap in the agent-os-pocketflow framework where design-first methodology was only partially implemented. By adding initial design document generation during product planning, we ensure consistent application of the framework's own best practices and provide end-users with proper architectural foundation from day one.

The phased approach allows for incremental improvement while maintaining the framework's core philosophy of providing flexible templates rather than rigid implementations.