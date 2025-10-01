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
- `design_document_missing`: Invoke design-document-creator for creation
- `design_incomplete`: Invoke design-document-creator for completion  
- `mermaid_diagram_missing`: Invoke design-document-creator for diagram

## validate_design_document
**Template for End-User Projects:** This section provides example validation logic that gets deployed to end-user projects.

```bash
#!/bin/bash
# Template validation script for end-user projects
# TODO: Customize this validation logic for your specific requirements

validate_design_document() {
    local design_file="docs/design.md"
    
    # TODO: Implement design document existence check
    if [[ ! -f "$design_file" ]]; then
        echo "❌ Design document missing: $design_file"
        echo "💡 Run: claude-code agent invoke design-document-creator"
        return 1
    fi
    
    # TODO: Implement section validation
    local required_sections=("Requirements" "Flow Design" "Data Design" "Node Design")
    for section in "${required_sections[@]}"; do
        if ! grep -q "^## $section" "$design_file"; then
            echo "❌ Missing section: $section"
            echo "💡 Run: claude-code agent invoke design-document-creator"
            return 2
        fi
    done
    
    # TODO: Implement Mermaid diagram validation  
    if ! grep -q "```mermaid" "$design_file"; then
        echo "❌ Missing Mermaid diagram"
        echo "💡 Add flow diagram to design document"
        return 3
    fi
    
    echo "✅ Design document validation passed"
    return 0
}

# TODO: Add this function call to your project's validation workflow
# validate_design_document
```

## Hook: validate_workflow_implementation
**Purpose:** Ensure PocketFlow workflow exists and matches spec
**Usage:** @include orchestration/orchestrator-hooks.md hook="validate_workflow_implementation"

### Implementation Logic:
1. Look for .agent-os/workflows/[feature-name].py
2. Validate workflow structure matches design
3. Check Pydantic models are defined
4. Verify flow connections match Mermaid diagram

## validate_workflow_implementation
**Template for End-User Projects:** This section provides example workflow validation that gets deployed to end-user projects.

```bash
#!/bin/bash
# Template workflow validation script for end-user projects  
# TODO: Customize this validation logic for your PocketFlow workflows

validate_workflow_implementation() {
    local feature_name="$1"
    local workflow_file=".agent-os/workflows/${feature_name}.py"
    
    # TODO: Implement workflow file existence check
    if [[ ! -f "$workflow_file" ]]; then
        echo "❌ Workflow missing: $workflow_file"
        echo "💡 Run: claude-code agent invoke file-creator --feature $feature_name (uses framework-tools/generator)"
        return 1
    fi
    
    # TODO: Implement Python syntax validation
    if ! python3 -m py_compile "$workflow_file" 2>/dev/null; then
        echo "❌ Workflow syntax error: $workflow_file"  
        echo "💡 Check Python syntax and imports"
        return 2
    fi
    
    # TODO: Implement Pydantic model validation
    local schema_file="src/schemas/${feature_name}_schema.py"
    if [[ ! -f "$schema_file" ]]; then
        echo "❌ Schema missing: $schema_file"
        echo "💡 Ensure Pydantic models are defined"
        return 3
    fi
    
    # TODO: Implement node validation
    local nodes_file="src/nodes/${feature_name}_nodes.py"
    if [[ ! -f "$nodes_file" ]]; then
        echo "❌ Nodes missing: $nodes_file"
        echo "💡 Implement workflow node classes"
        return 4
    fi
    
    # TODO: Validate workflow structure matches design.md
    local design_file="docs/design.md"
    if [[ -f "$design_file" ]]; then
        echo "💡 TODO: Implement design-workflow consistency check"
        # Add logic to compare Mermaid diagram with workflow structure
    fi
    
    echo "✅ Workflow implementation validation passed"
    return 0
}

# TODO: Add this function call to your project's CI/CD pipeline
# validate_workflow_implementation "your_feature_name"
```

## Hook: orchestrator_fallback
**Purpose:** Automatically invoke orchestrator when needed
**Usage:** @include orchestration/orchestrator-hooks.md hook="orchestrator_fallback"

### Implementation Logic:
1. Detect if current task requires orchestration
2. Check if orchestrator outputs exist
3. If missing: Invoke file-creator with context (uses generator)
4. Wait for completion and validate outputs
