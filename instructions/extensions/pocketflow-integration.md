# PocketFlow Integration Extension

## Auto-Detection and Orchestration
This extension automatically detects when PocketFlow patterns are needed and invokes the orchestrator.

### Detection Triggers:
- Complex data processing requirements
- Multi-step workflows
- AI/LLM integration needs
- Async processing patterns

### Integration Points:
1. **Planning Phase**: Identify PocketFlow patterns during product planning
2. **Specification Phase**: Generate PocketFlow-compatible specs
3. **Implementation Phase**: Create actual PocketFlow workflows

### Generated Artifacts:
- `.agent-os/workflows/[feature].py` - Complete PocketFlow implementation
- `src/schemas/[feature]_schema.py` - Pydantic models
- `src/nodes/[feature]_nodes.py` - Node implementations
- `src/flows/[feature]_flow.py` - Flow assembly
