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

<conditional-block task-condition="python" context-check="python-style">
IF current task involves writing or updating Python:
  IF python-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using Python style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get Python style rules from code-style/python-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @~/.agent-os/standards/code-style/python-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: Python style guide not relevant to current task
</conditional-block>

<conditional-block task-condition="pocketflow" context-check="pocketflow-style">
IF current task involves PocketFlow nodes or flows:
  IF pocketflow-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using PocketFlow style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get PocketFlow conventions from code-style/pocketflow-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @~/.agent-os/standards/code-style/pocketflow-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: PocketFlow style guide not relevant to current task
</conditional-block>

<conditional-block task-condition="fastapi" context-check="fastapi-style">
IF current task involves FastAPI routes or models:
  IF fastapi-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using FastAPI style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get FastAPI conventions from code-style/fastapi-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @~/.agent-os/standards/code-style/fastapi-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: FastAPI style guide not relevant to current task
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

<conditional-block task-condition="testing" context-check="testing-style">
IF current task involves writing or updating tests:
  IF testing-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using testing style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get testing conventions from code-style/testing-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @~/.agent-os/standards/code-style/testing-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: Testing style guide not relevant to current task
</conditional-block>