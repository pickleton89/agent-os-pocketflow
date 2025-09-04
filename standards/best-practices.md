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

## Node Lifecycle Rules

### Strict Separation of Concerns

**prep() Method - Data Access Only:**
```python
def prep(self, shared):
    # ✅ CORRECT: Read from SharedStore
    data = shared.get("input_data")
    config = shared.get("processing_config", {})
    return {"data": data, "config": config}
    
    # ❌ WRONG: External API calls
    # response = requests.get("https://api.example.com")
    
    # ❌ WRONG: Complex computation
    # processed = expensive_calculation(data)
```

**exec() Method - Pure Logic Only:**
```python
def exec(self, prep_result):
    # ✅ CORRECT: Use only prep_result
    data = prep_result["data"]
    result = process_data(data)
    return result
    
    # ❌ WRONG: Access SharedStore directly
    # config = self.shared["config"]
    
    # ❌ WRONG: Side effects
    # save_to_file(result)
```

**post() Method - Side Effects and Routing:**
```python
def post(self, shared, prep_result, exec_result):
    # ✅ CORRECT: Update SharedStore
    shared["processed_data"] = exec_result
    shared["processing_complete"] = True
    
    # ✅ CORRECT: Routing logic
    if exec_result.get("needs_review"):
        return "review_required"
    return "success"
    
    # ❌ WRONG: Complex computation
    # final_result = expensive_post_processing(exec_result)
```

### Lifecycle Violations to Avoid

1. **Monolithic exec() Methods**
   - Don't perform multiple distinct operations in exec()
   - Split into separate nodes for different responsibilities

2. **SharedStore Access in exec()**
   - Never access `shared` directly in exec()
   - All data must come through prep_result

3. **Side Effects in prep()**
   - Don't write to files, databases, or external systems
   - Keep prep() read-only for data preparation

4. **Complex Logic in post()**
   - Post should focus on storing results and routing
   - Avoid heavy computation or complex business logic

## Batch Node Selection Criteria

### When to Use BatchNode vs Regular Node

**Use BatchNode When:**
- Processing collections of similar items
- Each item can be processed independently
- Input is naturally iterable (lists, files, records)
- Want to leverage parallel processing capabilities

**Use Regular Node When:**
- Processing single items or unified datasets
- Operations require coordination between items
- Input is not naturally divisible
- Sequential processing is required

### Collection Processing Patterns

**✅ CORRECT - BatchNode for File Processing:**
```python
class ProcessMultipleFiles(BatchNode):
    def prep(self, shared):
        # Return list of file paths
        return shared["file_paths"]
    
    def exec(self, filepath):
        # Process one file at a time
        content = read_file(filepath)
        return process_content(content)
    
    def post(self, shared, prep_result, exec_res_list):
        # Aggregate all results
        shared["processed_files"] = dict(zip(prep_result, exec_res_list))
        return "success"
```

**❌ WRONG - Regular Node with Loop:**
```python
class ProcessMultipleFilesWrong(Node):
    def exec(self, prep_result):
        results = []
        for filepath in prep_result["file_paths"]:  # Don't loop in exec!
            content = read_file(filepath)
            results.append(process_content(content))
        return results
```

### BatchNode Decision Tree

```
Is your input a collection of items?
├─ No → Use Regular Node
└─ Yes → Can items be processed independently?
    ├─ No → Use Regular Node (with proper data flow)
    └─ Yes → Are there more than ~10 items?
        ├─ No → Regular Node acceptable, BatchNode preferred
        └─ Yes → Use BatchNode (required for performance)
```

### Batch Processing Anti-Patterns

1. **Single Item in BatchNode**
   - Don't use BatchNode for single items
   - Use regular Node for single document processing

2. **Dependent Item Processing**
   - Don't use BatchNode when items depend on each other
   - Use regular Node with proper sequencing

3. **Mixed Processing Types**
   - Don't mix file processing and API calls in one BatchNode
   - Split into separate nodes for different operations

4. **State Sharing Between Items**
   - BatchNode exec() should not share state between items
   - Use prep() to set up shared resources if needed

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

## Error Handling Patterns

### Convert Exceptions to Branches
Use try-catch to determine routing, not to handle errors inline:
```python
# ✅ CORRECT: Let exceptions propagate, handle in post()
def exec(self, prep_result):
    # Pure logic - let exceptions propagate naturally
    result = process(prep_result["data"])
    return result

def post(self, shared, prep_result, exec_result):
    # Handle successful result
    shared["result"] = exec_result
    return "success"

# Handle exceptions via exec_fallback
def exec_fallback(self, prep_result, exc):
    # Classify the exception for routing
    if isinstance(exc, ValidationError):
        return {"error_type": "validation", "message": str(exc)}
    elif isinstance(exc, APIError):
        return {"error_type": "api_failure", "retry": True}
    else:
        return {"error_type": "unknown", "message": str(exc)}

def post(self, shared, prep_result, exec_result):
    # Check if result is an error from fallback
    if isinstance(exec_result, dict) and "error_type" in exec_result:
        shared["error"] = exec_result
        if exec_result.get("retry"):
            return "retry"  # Routes to retry node
        return f"{exec_result['error_type']}_handler"
    
    shared["result"] = exec_result
    return "success"

# ❌ WRONG: Handling errors inline
def exec(self, prep_result):
    try:
        result = process(prep_result["data"])
    except Exception:
        result = fallback_process()  # Don't handle inline!
    return result
```

### Comprehensive Error Flow Design

**Error Classification System:**
```python
class ProcessingNode(Node):
    def exec(self, prep_result):
        # Pure logic - let exceptions propagate
        return complex_processing(prep_result)
    
    def exec_fallback(self, prep_result, exc):
        # Classify exceptions for routing
        if isinstance(exc, ValidationError):
            return {"error_type": "validation", "recoverable": True}
        elif isinstance(exc, NetworkError):
            return {"error_type": "network", "recoverable": True}
        elif isinstance(exc, AuthenticationError):
            return {"error_type": "auth", "recoverable": False}
        elif isinstance(exc, ResourceExhaustedError):
            return {"error_type": "quota", "recoverable": True, "wait_time": 300}
        else:
            return {"error_type": "unknown", "recoverable": False}
    
    def post(self, shared, prep_result, exec_result):
        if isinstance(exec_result, dict) and "error_type" in exec_result:
            error = exec_result
            shared["last_error"] = error
            
            if not error["recoverable"]:
                return "fatal_error"
            if error["error_type"] == "quota":
                shared["wait_time"] = error.get("wait_time", 60)
                return "wait_and_retry"
            return f"{error['error_type']}_handler"
        
        shared["result"] = exec_result
        return "success"
```

### Advanced Error Patterns

**Progressive Retry Strategy:**
```python
class RetryWithBackoff(Node):
    def prep(self, shared):
        retry_count = shared.get("retry_count", 0)
        return {"data": shared["data"], "attempt": retry_count}
    
    def post(self, shared, prep_result, exec_result):
        if exec_result.get("success"):
            # Reset retry counter on success
            shared.pop("retry_count", None)
            return "complete"
        
        retry_count = shared.get("retry_count", 0) + 1
        shared["retry_count"] = retry_count
        
        if retry_count >= 3:
            return "max_retries_exceeded"
        
        # Exponential backoff
        wait_time = 2 ** retry_count
        shared["wait_time"] = wait_time
        return "wait_and_retry"
```

**Error Recovery Patterns:**
```python
# Error handler nodes for different error types
class ValidationErrorHandler(Node):
    def exec(self, prep_result):
        error_info = prep_result["error"]
        # Attempt to clean/fix the data
        cleaned_data = sanitize_input(prep_result["original_data"])
        return cleaned_data
    
    def post(self, shared, prep_result, exec_result):
        shared["cleaned_data"] = exec_result
        return "retry_processing"

class NetworkErrorHandler(Node):
    def exec(self, prep_result):
        # Switch to backup endpoint
        return {"use_backup": True, "endpoint": "https://backup-api.com"}
    
    def post(self, shared, prep_result, exec_result):
        shared["api_config"] = exec_result
        return "retry_with_backup"
```

### Error Flow Architecture

**Complete Error Flow Example:**
```python
# Main processing node
process_node = ProcessingNode()
validation_handler = ValidationErrorHandler()
network_handler = NetworkErrorHandler()
fatal_handler = FatalErrorHandler()
retry_node = RetryWithBackoff()
wait_node = WaitNode()

# Connect error paths
process_node - "success" >> next_step
process_node - "validation_handler" >> validation_handler
process_node - "network_handler" >> network_handler  
process_node - "fatal_error" >> fatal_handler
process_node - "wait_and_retry" >> wait_node

# Recovery paths
validation_handler - "retry_processing" >> process_node
network_handler - "retry_with_backup" >> process_node
wait_node - "continue" >> process_node
```

### Error Handling Anti-Patterns

1. **Silent Failures**
   - Always log and route errors explicitly
   - Never swallow exceptions without handling

2. **Generic Error Handling**
   - Handle specific error types differently
   - Don't treat all errors the same way

3. **Inline Error Recovery**
   - Don't fix errors within the same node that detected them
   - Use dedicated error handler nodes

4. **Infinite Retry Loops**
   - Always have maximum retry limits
   - Include circuit breaker patterns for persistent failures

### Best Practices Summary

- **Make error paths visible**: Errors should appear in your flow graph
- **Dedicated error nodes**: Handle each error type in its own node
- **Fail fast during development**: Avoid try/except in utilities and early stages
- **Let Node retry mechanisms handle failures**: Don't catch exceptions in utilities
- **Add retry nodes**: For transient failures with exponential backoff
- **Never expose internals**: Generic messages in production
- **Circuit breaker pattern**: Stop trying after persistent failures
- **Error context preservation**: Keep error details for debugging
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
    shared = {"input": test_data}
    
    # Test the full node lifecycle
    action = node.run(shared)
    assert action == "expected_action"
    assert shared["output"] == expected_value
    
    # Or test individual methods
    prep_result = node.prep(shared)
    exec_result = node.exec(prep_result)
    assert exec_result == expected_exec_result
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

### Expanded Utility Guidelines

**What Belongs in Utilities:**
- External API calls (LLM, web search, databases)
- File I/O operations
- Data format conversions (JSON, XML, CSV)
- Simple data transformations
- Authentication and credential management

**What Does NOT Belong in Utilities:**
- Complex business logic or decision-making
- Multi-step workflows (use nodes instead)
- LLM reasoning or prompt construction
- State management (use SharedStore)
- Flow control or branching logic

### Utility Design Patterns

**✅ CORRECT - Simple, Focused Utility:**
```python
# utils/call_llm.py
from openai import OpenAI

def call_llm(prompt: str, model: str = "gpt-4") -> str:
    """Simple LLM wrapper - no complex reasoning."""
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    result = call_llm("Hello world")
    print(result)
```

**❌ WRONG - Hidden Logic in Utility:**
```python
# utils/complex_llm.py  # DON'T DO THIS
from utils.call_llm import call_llm

def analyze_and_decide(data):
    """This hides too much decision logic!"""
    if len(data) > 1000:
        summary = call_llm(f"Summarize: {data}")
        if "urgent" in summary.lower():
            return call_llm(f"Create urgent response for: {summary}")
    return call_llm(f"Standard analysis: {data}")
```

### Utility Anti-Patterns

1. **Hidden LLM Logic**
   - Don't hide complex prompts or reasoning chains
   - Keep utilities transparent and simple

2. **Utility State Management**
   - Don't store state in utility functions
   - Use SharedStore for all persistent data

3. **Multi-Step Utilities**
   - Don't chain multiple API calls in one utility
   - Break into separate utilities or use nodes

4. **Trivial I/O Wrappers**
   - Don't create utilities for simple file operations
   - Direct file I/O in nodes is acceptable

### Framework-Specific Guidance

**For Template Generation:**
- Generated utilities should include TODO comments
- Mark complex logic boundaries clearly
- Provide placeholder implementations, not full solutions

## Context Management Guidelines

### SharedStore Design Principles

**Hierarchical Structure:**
```python
# ✅ CORRECT - Well-organized SharedStore
shared = {
    "input": {
        "user_query": "How do I use PocketFlow?",
        "context": {"session_id": "123", "user_preferences": {...}}
    },
    "processing": {
        "step1_result": {...},
        "step2_result": {...},
        "current_stage": "analysis"
    },
    "output": {
        "final_answer": None,  # To be populated
        "confidence_score": None,
        "sources": []
    },
    "metadata": {
        "start_time": "2025-01-04T10:00:00",
        "processing_nodes": [],
        "error_log": []
    }
}
```

**❌ WRONG - Flat, Disorganized Structure:**
```python
shared = {
    "query": "How do I use PocketFlow?",
    "result1": {...},
    "temp_data": {...},
    "final": None,
    "user_id": "123",
    "error": None,
    "time": "2025-01-04T10:00:00"
}
```

### Data Flow Patterns

**Read-Modify-Write Pattern:**
```python
def post(self, shared, prep_result, exec_result):
    # ✅ CORRECT: Clear data flow
    # 1. Read existing state
    processing_state = shared.get("processing", {})
    
    # 2. Modify based on results
    processing_state.update({
        "analysis_complete": True,
        "result": exec_result,
        "next_action": "review" if exec_result.needs_review else "complete"
    })
    
    # 3. Write back to SharedStore
    shared["processing"] = processing_state
    
    return processing_state["next_action"]
```

### Context Size Management

**Progressive Context Building:**
```python
# ✅ CORRECT - Build context incrementally
class GatherContext(Node):
    def post(self, shared, prep_result, exec_result):
        context = shared.setdefault("context", {"sources": []})
        context["sources"].append({
            "type": "search_result",
            "content": exec_result,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 5 sources to manage size
        context["sources"] = context["sources"][-5:]
        return "continue"
```

**❌ WRONG - Unbounded Context Growth:**
```python
def post(self, shared, prep_result, exec_result):
    # This will grow indefinitely!
    all_results = shared.setdefault("all_results", [])
    all_results.append(exec_result)
    return "continue"
```

### Context Anti-Patterns

1. **Deep Nesting**
   - Avoid more than 3 levels of nesting
   - Use references or foreign keys for complex relationships

2. **Duplicate Data**
   - Don't store the same data in multiple places
   - Use references to single source of truth

3. **Untyped Context**
   - Define clear schemas for SharedStore sections
   - Document expected data types and structures

4. **Context Leakage**
   - Don't let temporary processing data persist
   - Clean up intermediate results when no longer needed

### Best Practices for Large Contexts

**Chunking and References:**
```python
# Store large content separately, reference by ID
shared = {
    "documents": {
        "doc_001": {"content": "large text...", "metadata": {...}},
        "doc_002": {"content": "more text...", "metadata": {...}}
    },
    "processing": {
        "current_doc_id": "doc_001",
        "doc_queue": ["doc_002", "doc_003"]
    }
}
```

**Context Cleanup:**
```python
def post(self, shared, prep_result, exec_result):
    # Clean up temporary data after processing
    if "temp_processing" in shared:
        del shared["temp_processing"]
    
    # Move final results to permanent location
    shared["final_results"] = exec_result
    return "complete"
```

---

*Remember: Every feature starts with docs/design.md, then utilities, then nodes, then flows.*
