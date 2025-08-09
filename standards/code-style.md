# Code Style Guide

> Version: 1.3.0
> Last Updated: 2025-01-31

## Context

This file is part of the Agent OS standards system. These global code style rules are referenced by all product codebases and provide default formatting guidelines. Individual projects may extend or override these rules in their `.agent-os/product/code-style.md` file.

<conditional-block context-check="general-formatting">
IF this General Formatting section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using General Formatting rules already in context"
ELSE:
  READ: The following formatting rules

## General Formatting

### Python Standards
- **Indentation**: 4 spaces (never tabs)
- **Line Length**: 88 characters max (Ruff default)
- **File Length**: Keep under 500 lines
- **Blank Lines**: Two around top-level definitions, one around methods

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Methods/Variables | snake_case | `user_profile` |
| Classes | PascalCase | `UserProfile` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private Methods | _prefix | `_validate_input()` |
| Environment Vars | UPPER_SNAKE_CASE | `API_KEY` |

### String Formatting
- Prefer f-strings: `f"Hello {name}"`
- Single quotes for simple strings, triple double for docstrings
- Define constants at module level after imports

### Code Principles
- **DRY**: Extract common logic into utilities
- **Whitespace**: No extra spaces inside brackets/parens
- **Trailing Commas**: Use in multi-line collections

</conditional-block>

<conditional-block task-condition="pocketflow" context-check="pocketflow-patterns">
IF current task involves PocketFlow nodes or flows:
  READ: The following PocketFlow conventions

## PocketFlow Patterns

### Naming Standards
- **Nodes**: `PascalCase` + "Node" suffix (e.g., `FetchDataNode`)
- **Flows**: `PascalCase` + "Flow" suffix (e.g., `ProcessingFlow`)
- **Batch/Async**: Include in name (e.g., `BatchProcessNode`, `AsyncFetchNode`)

### Lifecycle Methods
- Standard: `prep()`, `exec()`, `post()`
- Async variants: `prep_async()`, `exec_async()`, `post_async()`
- Keep each method focused and single-purpose

### Shared Store Conventions
- **Key Format**: snake_case (e.g., `processed_chunks`)
- **Namespacing**: Prefix by node (e.g., `fetcher_results`)
- **Timestamps**: Use `<key>_timestamp` format
- **Prefixes**: `raw_`, `processed_`, `final_`, `temp_`

### Flow Control Actions
| Purpose | Action String |
|---------|--------------|
| Default/Success | `None` or `"success"` |
| Error States | `"error"`, `"retry"`, `"skip"` |
| Flow Control | `"continue"`, `"end"`, `"batch"` |
| Branching | Custom descriptive strings |

**Best Practice**: For complex flows with many branches, define action strings as constants at the top of your `flow.py` file to avoid typos and improve readability (e.g., `ACTION_APPROVE = "approved"`).

</conditional-block>

<conditional-block task-condition="fastapi" context-check="fastapi-conventions">
IF current task involves FastAPI routes or models:
  READ: The following FastAPI conventions

## FastAPI Conventions

### Routes & Models
- **Route Functions**: verb_noun pattern (e.g., `get_items`, `create_user`)
- **Base Models**: Simple names (e.g., `User`, `Item`)
- **Request Models**: Action suffix (e.g., `UserCreate`, `ItemUpdate`)
- **Response Models**: "Response" suffix when different from base
- **Always use** `async def` for route functions

### Status Codes
- 200: Success (GET/PUT)
- 201: Created (POST)
- 204: No Content (DELETE)
- 404: Not Found
- 422: Validation Error

### Project Structure
```
src/
├── auth/
│   ├── router.py
│   ├── schemas.py
│   └── service.py
├── items/
│   ├── router.py
│   ├── schemas.py
│   └── service.py
```

</conditional-block>

<conditional-block task-condition="mcp" context-check="mcp-conventions">
IF current task involves Fast MCP tools:
  READ: The following MCP conventions

## Fast MCP Conventions

### Tool Standards
- **Function Names**: snake_case (e.g., `search_documents`)
- **Descriptions**: Concise, action-oriented
- **Return Types**: JSON-serializable only
- **Parameters**: Use type hints with defaults
- **Error Handling**: Return structured error objects

</conditional-block>

<conditional-block task-condition="async" context-check="async-patterns">
IF current task involves async/await:
  READ: The following async patterns

## Async/Await Patterns

### Best Practices
- No `_async` suffix unless disambiguating from sync version
- Use `async with` for context managers
- Use `asyncio.gather()` for parallel operations
- Wrap await statements in try/except for error handling

</conditional-block>

## Universal Standards

### Imports
1. Standard library
2. Core frameworks (FastAPI, PocketFlow)
3. Third-party packages
4. Local application

### Type Hints
- **Required** for all function parameters and returns
- Use `Optional[T]` or `T | None` (Python 3.10+)
- Use `Protocol` for duck typing interfaces

### Documentation
- Follow PEP 257 for docstrings
- Comment the "why", not the "what"
- Update comments when code changes

## Logging
- Use `structlog` for all application logging.
- Log levels: Use `info` for routine events, `warning` for recoverable issues, and `error` or `exception` for critical failures.
- Context: Bind relevant context (e.g., `user_id`, `request_id`) to the logger for better traceability.

### Testing
- Files: `test_*.py` pattern
- Classes: `Test` prefix (e.g., `TestUserAPI`)
- Methods: `test_` prefix (e.g., `test_create_user`)
- Use pytest fixtures for common data