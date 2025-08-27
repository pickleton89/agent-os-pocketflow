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
