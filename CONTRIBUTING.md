# PocketFlow Implementation Guidelines

## Quick PR Review Checklist

Use this checklist when reviewing AI-generated PocketFlow designs and code:

### Flow Design ✓
- [ ] Flow is linear unless truly an agent; trivial I/O not modeled as nodes
- [ ] Batch used anywhere we iterate per item (files/anomalies/issues/insights)
- [ ] No over-branching of simple workflows - reserve branching for agent patterns
- [ ] Nodes have single responsibilities (not monolithic)

### Utilities ✓
- [ ] Utilities = external I/O; **no LLM prompts** inside utilities
- [ ] LLM calls stay in node `exec()` methods for transparency
- [ ] Utilities are narrow and focused (not over-ambitious)

### Shared Store Schema ✓
- [ ] Shared store schema is concrete, minimal, and every field is consumed
- [ ] No vague schemas ("anomalies", "engagement score")
- [ ] No bloat fields without consumers

### Node Contract & Execution ✓
- [ ] Node contract honored: `prep()` reads, `exec()` is pure (no shared/self), `post()` writes & routes
- [ ] **No `try/except` in `exec()` or utilities** for flow control; use retries/fallbacks
- [ ] No accessing shared store from `exec()`
- [ ] No stashing state on `self`

### Context & Scaling ✓
- [ ] No arbitrary context truncation; chunk if needed
- [ ] Modern LLMs handle large contexts - avoid "sample first 10 lines" patterns

### Analysis & Business Logic ✓
- [ ] Reports are deterministic; LLMs used only where judgment/context is needed
- [ ] Action spaces (for agents) are small, explicit, and testable
- [ ] Metrics and outputs map to business context
- [ ] No string concatenation where LLM calls would add value

### Deliverables & Outputs ✓
- [ ] No redundant nodes duplicating work
- [ ] Single artifact per purpose; reuse intermediate products
- [ ] Only create assets if consumers need them

## Detailed Guidelines

### 1. Flow Design Patterns

#### ✅ DO: Use BatchNode for List Processing
```python
class ParallelProcessorNode(BatchNode):
    """Process multiple items in parallel"""
    # Use when exec operates on "for each item" pattern
```

#### ❌ DON'T: Include Trivial I/O as Nodes
```python
# Wrong - inflates graph
class LoadCSVNode(Node): pass
class SaveOutputNode(Node): pass

# Right - keep in main.py/post steps
```

### 2. Utility Function Patterns

#### ✅ DO: Keep Utilities for Real I/O
```python
async def fetch_api_data(url: str) -> dict:
    """Utility for external API calls"""
    # Real-world I/O operation
```

#### ❌ DON'T: Hide LLM Calls in Utilities
```python
# Wrong - breaks transparency
def analyze_with_llm(data):
    return llm_client.chat(prompt)

# Right - LLM prompts in node exec()
class AnalyzeNode(AsyncNode):
    async def exec_async(self, prep_result):
        prompt = f"Analyze this data: {prep_result}"
        return await llm_client.chat(prompt)
```

### 3. Error Handling Patterns

#### ✅ DO: Use PocketFlow's Built-in Error Handling
```python
class MyNode(AsyncNode):
    max_retries = 3
    wait = 2.0
    
    async def exec_async(self, prep_result):
        # Let exceptions bubble up
        return await risky_operation(prep_result)
    
    async def exec_fallback(self, prep_result, error):
        return "fallback_result"
```

#### ❌ DON'T: Use Try/Except in exec() or Utilities
```python
# Wrong - fights PocketFlow's retry system
async def exec_async(self, prep_result):
    try:
        return await operation()
    except Exception:
        return "error"  # This breaks retries!
```

### 4. Node Contract Patterns

#### ✅ DO: Follow prep/exec/post Separation
```python
class MyNode(AsyncNode):
    def prep(self, shared: Dict[str, Any]) -> Any:
        """Read everything needed from shared store"""
        return {
            'input_data': shared['input_data'],
            'config': shared.get('config', {})
        }
    
    async def exec_async(self, prep_result: Any) -> Any:
        """Pure function - only uses prep_result"""
        return process_data(prep_result['input_data'])
    
    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:
        """Write results and choose next action"""
        shared['processed_data'] = exec_result
```

#### ❌ DON'T: Access Shared Store in exec()
```python
# Wrong - breaks separation of concerns
async def exec_async(self, prep_result):
    data = self.shared['input_data']  # Should be in prep()
    result = process(data)
    self.shared['result'] = result    # Should be in post()
```

### 5. FastAPI Integration Patterns

#### ✅ DO: Let PocketFlow Handle Errors
```python
@router.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    shared = {"request_data": request.dict()}
    
    # Let PocketFlow handle retries and errors
    flow = MyFlow()
    await flow.run_async(shared)
    
    if "error" in shared:
        raise HTTPException(status_code=422, detail=shared["error_message"])
    
    return AnalyzeResponse(**shared["result"])
```

#### ❌ DON'T: Wrap Flow Execution in Try/Catch
```python
# Wrong - prevents PocketFlow error handling
try:
    await flow.run_async(shared)
    return response
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

## Validation Commands

Before submitting PRs, run these commands:

```bash
# Lint and format
uv run ruff check --fix .
uv run ruff format .

# Type checking
uv run ty check

# Run tests
uv run pytest

# Validate PocketFlow patterns
uv run python .agent-os/scripts/validate-generation.py <workflow-path>
```

## Common Anti-Patterns to Avoid

1. **Magic Numbers**: Use configuration instead of hardcoded values
2. **Premature Optimization**: Start simple, optimize when needed  
3. **Over-Engineering**: Keep utilities narrow and focused
4. **Hidden Dependencies**: Make all external calls explicit
5. **Context Truncation**: Use chunking strategies instead of arbitrary limits

## Resources

- [PocketFlow Documentation](docs/)
- [Agent OS Standards](standards/)
- [Workflow Templates](templates/)

---

*This checklist is derived from PocketFlow best practices and should be used for all code reviews.*