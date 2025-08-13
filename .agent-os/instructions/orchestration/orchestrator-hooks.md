# Orchestration Hooks System

## Hook: design_document_validation
**Purpose:** Ensure design.md exists and is complete
**Usage:** @include orchestration/orchestrator-hooks.md hook="design_document_validation"

### Implementation Logic:
1. Check if docs/design.md exists
2. Validate all required sections complete
3. If incomplete: Invoke orchestrator to complete
4. If missing: Block progression with error

### Error States:
- `design_document_missing`: Invoke orchestrator for creation
- `design_incomplete`: Invoke orchestrator for completion  
- `mermaid_diagram_missing`: Invoke orchestrator for diagram

## Hook: validate_workflow_implementation
**Purpose:** Ensure PocketFlow workflow exists and matches spec
**Usage:** @include orchestration/orchestrator-hooks.md hook="validate_workflow_implementation"

### Implementation Logic:
1. Look for .agent-os/workflows/[feature-name].py
2. Validate workflow structure matches design
3. Check Pydantic models are defined
4. Verify flow connections match Mermaid diagram

## Hook: orchestrator_fallback
**Purpose:** Automatically invoke orchestrator when needed
**Usage:** @include orchestration/orchestrator-hooks.md hook="orchestrator_fallback"

### Implementation Logic:
1. Detect if current task requires orchestration
2. Check if orchestrator outputs exist
3. If missing: Invoke pocketflow-orchestrator with context
4. Wait for completion and validate outputs
