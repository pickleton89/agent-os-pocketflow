# LLM/AI Workflow Extension

## Design Document Requirement (LLM/AI Features Only)

@include orchestration/orchestrator-hooks.md hook="design_document_validation"

**Blocking Condition:** Implementation CANNOT proceed without completed docs/design.md

## PocketFlow Pattern Selection

When LLM/AI components detected:
1. Analyze feature complexity
2. Select appropriate PocketFlow pattern:
   - **Agent**: Dynamic decision making
   - **Workflow**: Sequential processing  
   - **RAG**: Knowledge-enhanced responses
   - **MapReduce**: Large data processing
   - **Multi-Agent**: Collaborative systems

## Code Generation Requirements

Generate complete PocketFlow implementation:
- [ ] Pydantic models for all data structures
- [ ] Node implementations with proper lifecycle
- [ ] Flow assembly with error handling
- [ ] Utility functions with standalone tests

## LLM-Specific Clarification Areas

<llm_specifics>
  - **For LLM/AI components:**
    - Desired PocketFlow design pattern (Agent, Workflow, RAG, MapReduce, Multi-Agent, Structured Output)
    - Specific LLM models/providers to use (if not already in tech stack)
    - Data sources for RAG or knowledge base
    - Expected input/output formats (structured output considerations)
    - Latency or throughput requirements
</llm_specifics>

## Integration with Step 4.5: Mandatory Design Document Creation

This extension specifically handles the LLM/AI workflow requirements for step 4.5 in create-spec.md:

### Template Reference
**Template:** Use complete design document template from @templates/pocketflow-templates.md
**Sections Required:**
- Requirements (with design pattern classification)
- Flow Design (with Mermaid diagram)
- Utilities (with input/output contracts)
- Data Design (SharedStore schema)
- Node Design (prep/exec/post specifications)

### Validation Requirements
<must_complete>
  - [ ] Requirements section filled with specific details
  - [ ] Mermaid diagram created and validated
  - [ ] All utility functions specified with input/output contracts
  - [ ] SharedStore schema defined completely
  - [ ] Each node's prep/exec/post logic detailed
  - [ ] Error handling and retry strategies specified
  - [ ] Integration points identified
</must_complete>