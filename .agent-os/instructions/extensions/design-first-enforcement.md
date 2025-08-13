# Design-First Enforcement

## Validation Gate: Design Document Required

**Purpose:** Ensure proper design before implementation

### Validation Steps:
1. Check if docs/design.md exists
2. Validate all required sections complete:
   - [ ] Requirements with pattern identification
   - [ ] Flow Design with Mermaid diagram
   - [ ] Utilities with input/output contracts  
   - [ ] Data Design with SharedStore schema
   - [ ] Node Design with prep/exec/post specs

### Enforcement Actions:
- **Missing design.md**: Invoke orchestrator to create
- **Incomplete sections**: Block progression until complete
- **Invalid Mermaid**: Request diagram correction

### Error Handling:
```bash
if [[ ! -f "docs/design.md" ]]; then
    echo "❌ BLOCKED: Implementation requires completed design document"
    echo "Please create docs/design.md using PocketFlow methodology"
    exit 1
fi
```

## Integration with Execute Tasks

This enforcement mechanism should be included in execute-tasks.md as a validation gate that:

1. **Blocks execution** if design document is missing
2. **Validates completeness** of all required sections
3. **Invokes orchestrator** to generate missing components
4. **Provides clear error messages** with resolution instructions

### Orchestrator Fallback Protocol

When design document validation fails:
1. Automatically invoke the PocketFlow Orchestrator agent
2. Provide context about the missing or incomplete design elements
3. Generate the required design document using PocketFlow templates
4. Validate the generated design meets all requirements
5. Continue with task execution only after validation passes

### Error State Handling

**design_document_missing**: 
- Action: Invoke orchestrator for creation
- Context: Feature requirements and specification
- Template: Full design document template from pocketflow-templates.md

**design_incomplete**: 
- Action: Invoke orchestrator for completion
- Context: Existing design.md and missing sections
- Template: Specific section templates for missing parts

**mermaid_diagram_missing**: 
- Action: Invoke orchestrator for diagram creation
- Context: Feature workflow and node specifications
- Template: Mermaid diagram patterns from PocketFlow templates