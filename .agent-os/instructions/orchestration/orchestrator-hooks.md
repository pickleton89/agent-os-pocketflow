# Orchestration Hooks System

## Hook: validate_design_document
**Purpose:** Ensure design.md exists and is complete before implementation
**Used by:** create-spec.md, execute-tasks.md

**Implementation:**
1. Check if docs/design.md exists
2. Validate required sections:
   - [ ] Requirements (with PocketFlow pattern identification)
   - [ ] Flow Design (with Mermaid diagram)  
   - [ ] Utilities (with input/output contracts)
   - [ ] Data Design (SharedStore schema)
   - [ ] Node Design (prep/exec/post specifications)
3. If incomplete: Invoke orchestrator to complete
4. If missing: Block progression with error

**Error States:**
- `design_document_missing`: Invoke orchestrator for creation
- `design_incomplete`: Invoke orchestrator for completion
- `mermaid_diagram_missing`: Invoke orchestrator for diagram creation

## Hook: validate_workflow_implementation  
**Purpose:** Ensure PocketFlow workflow exists and matches spec
**Used by:** execute-tasks.md

**Implementation:**
1. Look for .agent-os/workflows/[feature-name].py
2. Validate workflow structure:
   - [ ] Proper Node definitions with prep/exec/post
   - [ ] SharedStore schema matches design
   - [ ] Flow connections match Mermaid diagram
   - [ ] Pydantic models for data validation
3. If missing: Invoke orchestrator to generate
4. If mismatched: Invoke orchestrator to fix

## Hook: orchestrator_fallback
**Purpose:** Automatically invoke orchestrator when needed
**Used by:** All instruction files

**Implementation:**
1. Detect if current task requires orchestration
2. Check if orchestrator outputs exist
3. If missing: Invoke pocketflow-orchestrator with context
4. Wait for completion and validate outputs
5. Continue with enhanced workflow

**Coordination Protocol:**
```python
def invoke_orchestrator_hook(context: dict, hook_type: str):
    """Standard orchestrator invocation protocol"""
    
    # 1. Prepare context for orchestrator
    orchestrator_context = {
        "instruction_file": context["current_file"],
        "step": context["current_step"], 
        "hook_type": hook_type,
        "feature_context": context.get("feature", {}),
        "validation_requirements": get_requirements(hook_type)
    }
    
    # 2. Invoke orchestrator with context
    result = invoke_agent("pocketflow-orchestrator", orchestrator_context)
    
    # 3. Validate orchestrator outputs
    validation = validate_orchestrator_outputs(result, hook_type)
    
    # 4. Update coordination state
    update_coordination_state(context["current_file"], result)
    
    return validation
```