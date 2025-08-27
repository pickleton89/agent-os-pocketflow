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
