# Development Best Practices

> Version: 2.0.0  
> Last updated: 2025-01-10  
> Scope: Global development standards for PocketFlow + FastAPI stack

## Context

This file is part of the Agent OS standards system. These practices guide PocketFlow-based development with Python, Pydantic, FastAPI, and Fast MCP. Projects may override in `.agent-os/product/best-practices.md`.

<conditional-block context-check="core-principles">
IF core principles already in context:
  SKIP: Re-reading core principles
ELSE:
  READ: The following principles

## Core Principles

### PocketFlow Philosophy
1. **Radical Minimalism**: Keep it tiny and dependency-free
2. **Graph + Shared Store**: Every app is nodes reading/writing a common store
3. **Agentic Coding**: "Humans design, agents code" - design first, implement with AI
4. **Separation of Concerns**: Data in store, logic in nodes - never mix
5. **Loose Coupling**: Stay vendor-agnostic, swap services freely

### Development Philosophy
- **Keep It Simple**: Fewest lines possible, avoid over-engineering.
  - *Why? Simple code is more maintainable and easier for agents to reason about.*
- **Type Everything**: All data structures must be Pydantic models.
  - *Why? Strict schemas prevent data errors at boundaries and enable auto-validation.*
- **Think in Flows**: Design as graphs before writing code.
  - *Why? A clear graph design ensures modularity and testability from the start.*

### Agentic Coding Methodology

| Steps | Human | AI | Comment |
|:------|:-----:|:--:|:--------|
| 1. Requirements | ★★★ High | ★☆☆ Low | Humans understand the requirements and context |
| 2. Flow | ★★☆ Medium | ★★☆ Medium | Humans specify high-level design, AI fills details |
| 3. Utilities | ★★☆ Medium | ★★☆ Medium | Humans provide APIs, AI helps implementation |
| 4. Data | ★☆☆ Low | ★★★ High | AI designs schema, humans verify |
| 5. Node | ★☆☆ Low | ★★★ High | AI designs nodes based on flow |
| 6. Implementation | ★☆☆ Low | ★★★ High | AI implements based on design |
| 7. Optimization | ★★☆ Medium | ★★☆ Medium | Humans evaluate, AI optimizes |
| 8. Reliability | ★☆☆ Low | ★★★ High | AI writes tests and handles edge cases |
</conditional-block>

<conditional-block task-condition="agentic-workflow" context-check="agentic-steps">
IF current task involves planning PocketFlow development:
  READ: The following agentic workflow

## Agentic Development Steps

1. **Requirements**: Clarify project needs and evaluate AI system fit
   - Good for: Routine tasks, creative tasks with defined inputs
   - Not good for: Ambiguous problems requiring complex decisions
   - Keep user-centric: explain "problem" from user perspective

2. **Flow Design**: Create high-level workflow with Mermaid diagrams
   - Identify design patterns: Agent, Workflow, RAG, MapReduce
   - **Critical**: If humans can't specify the flow, AI agents can't automate it
   - Must create `docs/design.md` before any coding

3. **Utilities**: Implement external interface functions first
   - Think: AI needs a "body" to interact with the world
   - Examples: reading inputs, writing outputs, calling APIs
   - NOT LLM tasks (those are internal to AI system)
   - Avoid exception handling - let Node retry mechanisms handle failures

4. **Data Design**: Design SharedStore schema that all nodes use
   - Use in-memory dict for simple, database for complex/persistent
   - Don't repeat yourself: use references or foreign keys

5. **Node Design**: Plan how each node reads/writes data and uses utilities
   - Specify node type, prep/exec/post logic, utility functions used
   - Keep specific but high-level, no code yet

6. **Implementation**: Build nodes and flows based on design
   - FAIL FAST: leverage Node retry/fallback mechanisms
   - Add logging throughout for debugging
   - Keep it simple - avoid complex features early

7. **Optimization**: Evaluate and improve
   - Use human intuition for initial evaluation
   - Redesign flow if needed, or do micro-optimizations
   - Prompt engineering and in-context learning

8. **Reliability**: Add robustness
   - Node retries with proper max_retries and wait times
   - Logging and visualization for debugging
   - Self-evaluation nodes for uncertain results

</conditional-block>

<conditional-block task-condition="node-design" context-check="node-patterns">
IF current task involves creating PocketFlow nodes:
  READ: The following node patterns

## Node Design Patterns

### Three-Step Lifecycle
Every node follows `prep → exec → post`:
- **prep**: Data access and preparation
- **exec**: Pure computation (or exec_async for I/O)
- **post**: Side effects and routing decisions

### Node Types
- **Node**: Synchronous operations, pure computation
- **AsyncNode**: I/O operations, API calls, LLM interactions
- **BatchNode**: Process iterables, one exec per item
- **AsyncParallelBatchNode**: Concurrent processing with rate limit awareness

### Design Rules
- Single responsibility per node
- Clear action strings ("success", "retry", not "1", "2")
- Never store state in nodes - use SharedStore only
- Mock external dependencies via node injection
</conditional-block>

<conditional-block task-condition="fastapi-integration" context-check="api-patterns">
IF current task involves API endpoints:
  READ: The following FastAPI patterns

## FastAPI + PocketFlow Integration

### Flows as Endpoints
```python
@app.post("/process", response_model=ProcessResponse)
async def process_endpoint(request: ProcessRequest):
    flow = ProcessingWorkflow()
    shared = SharedStore({"request": request.dict()})
    await flow.run_async(shared)
    return ProcessResponse(**shared["result"])
```

### Pydantic Schemas
- Define SharedStore schemas upfront
- Validate at every boundary
- Return Pydantic models from endpoints

### Fast MCP Integration
- Wrap MCP servers in AsyncNode
- Handle tool errors via branching
- Use AsyncFlow for MCP workflows
</conditional-block>

<conditional-block task-condition="error-handling" context-check="error-patterns">
IF current task involves error handling:
  READ: The following error patterns

## Error Handling

### Convert Exceptions to Branches
Use try-catch to determine routing, not to handle errors inline:
```python
# ✅ CORRECT: Exceptions determine flow branching
def exec(self, shared):
    try:
        result = process(shared["data"])
        shared["result"] = result
        return "success"
    except ValidationError as e:
        shared["error"] = str(e)
        return "validation_error"  # Routes to validation handler node
    except APIError:
        return "retry"  # Routes to retry node

# ❌ WRONG: Handling errors inline
def exec(self, shared):
    try:
        result = process(shared["data"])
    except Exception:
        result = fallback_process()  # Don't handle inline!
    return "default"
```

### Error Flow Design
- **Make error paths visible**: Errors should appear in your flow graph
- **Dedicated error nodes**: Handle each error type in its own node
- **FAIL FAST during development**: Avoid try/except in utilities and early stages
- **Let Node retry mechanisms handle failures**: Don't catch exceptions in utilities
- **Add retry nodes**: For transient failures
- **Never expose internals**: Generic messages in production
</conditional-block>

<conditional-block task-condition="testing" context-check="test-philosophy">
IF current task involves testing:
  READ: The following testing principles

## Testing Philosophy

### Test Priorities
1. **Node isolation**: Test nodes independently first
2. **Mock externals**: Never call real APIs in tests
3. **Happy path first**: Then edge cases, then errors
4. **Behavior over implementation**: Test outcomes, not internals

### PocketFlow Testing
```python
def test_node():
    node = MyNode()
    shared = SharedStore({"input": test_data})
    result = node.exec(shared)
    assert result == "expected_action"
    assert shared["output"] == expected_value
```
</conditional-block>

## Anti-Patterns to Avoid

### PocketFlow Anti-Patterns
- **State in Nodes**: Always use SharedStore for state
- **Sync I/O in AsyncNode**: Don't block the event loop
- **Giant Nodes**: Split nodes doing multiple things
- **Deep Nesting**: Refactor beyond 3 levels
- **Premature Optimization**: Profile first

### API Anti-Patterns
- **Business logic in endpoints**: Delegate to flows
- **Inconsistent responses**: Use Pydantic models
- **Silent failures**: Return proper error codes

## Code Organization

### Required PocketFlow Structure
```
project/
├── main.py         # Entry point
├── nodes.py        # All node definitions
├── flow.py         # Flow assembly functions
├── utils/          # Custom utility functions
│   ├── __init__.py
│   ├── call_llm.py
│   └── [other_utils].py
├── requirements.txt
└── docs/
    └── design.md   # MANDATORY: High-level no-code design
```

### Documentation Requirements
- **docs/design.md is MANDATORY** - create before any coding
- Every flow needs a Mermaid diagram in design.md
- Document utility functions with input/output specs
- Keep design.md high-level and code-free

## Performance Guidelines

- Use AsyncNode for all I/O operations
- Batch process with AsyncParallelBatchNode
- Cache expensive LLM calls at node level
- Profile before optimizing

## Security Principles

- Validate all inputs with Pydantic
- Sanitize data crossing boundaries
- Never commit secrets
- Log security events
- Use environment variables

---

## Utility Function Philosophy

**PocketFlow provides ZERO built-in utilities.** You implement your own for maximum flexibility:
- **Why?** API volatility, vendor lock-in avoidance, custom optimizations
- **Examples provided, not built-in**: LLM wrappers, embeddings, search, chunking
- **One file per API call**: `utils/call_llm.py`, `utils/search_web.py`
- **Include main() for testing**: Each utility should be testable standalone

---

*Remember: Every feature starts with docs/design.md, then utilities, then nodes, then flows.*
