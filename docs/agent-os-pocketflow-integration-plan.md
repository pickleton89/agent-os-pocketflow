# Document Plan: Updating Agent OS Instructions for PocketFlow Methodology

## Overview
Update the three core Agent OS instruction files to fully integrate the PocketFlow Guidelines methodology along with the modern Python stack (FastAPI, Pydantic, FastMCP), ensuring AI agents follow the proper 8-step Agentic Coding process with proper type safety and API integration.

## Files to Update

### 1. `plan-product.md` (Minor Updates)
**Current Focus**: Product documentation generation  
**PocketFlow Integration Needed**:

- **Step 3 (mission.md)**: Enhance "AI/LLM Strategy" section template
  - Add reference to 8-step Agentic Coding methodology
  - Include design-first philosophy statement
  - Specify utility function approach ("examples provided, implement your own")

- **Step 5 (roadmap.md)**: Update phase template
  - Add requirement for `docs/design.md` creation before any LLM feature implementation
  - Tag features with specific PocketFlow design patterns (Agent, RAG, Workflow, etc.)

**Python Stack Integration Needed**:

- **Step 4 (tech-stack.md)**: Update default technology selections
  - Set Python 3.12+ as default language
  - FastAPI as primary web framework (serves MCP endpoints)
  - Pydantic for data validation
  - uv as package manager
  - Ruff for linting/formatting, mypy for type checking

- **Project Structure Template**: Define standard layout
  - Include `schemas/` directory for Pydantic models
  - FastAPI `main.py` as entry point
  - Standard `utils/` organization

### 2. `create-spec.md` (Major Updates Required)
**Current Focus**: Feature specification creation  
**Critical PocketFlow Additions Needed**:

- **New Step 4.5**: **Mandatory Design Document Creation**
  - Create `docs/design.md` using PocketFlow template structure
  - Include Requirements, Flow Design (with Mermaid), Utilities, Node Design sections
  - Block progression to implementation without completed design doc

- **Step 6 (spec.md)**: Enhance "LLM Workflow" section
  - Replace current template with comprehensive PocketFlow flow design
  - Require identification of design patterns (Agent/RAG/Workflow/MapReduce)
  - Mandate Mermaid diagram creation

- **Step 7 (technical-spec.md)**: Add PocketFlow-specific sections
  - Utility function specifications with input/output contracts
  - SharedStore schema design
  - Node type selections and retry strategies

- **Step 12 (tasks.md)**: Restructure task breakdown
  - Follow 8-step methodology: Design → Utilities → Data → Nodes → Implementation
  - Add specific tasks for `docs/design.md` creation and validation
  - Include utility function implementation before node development

**Python Stack Integration Needed**:

- **Step 6 (spec.md)**: Enhance API and Schema sections
  - Require Pydantic models for all data structures
  - FastAPI endpoint specifications with request/response models
  - Type hints mandatory for all functions

- **Step 7 (technical-spec.md)**: Add Stack-specific sections
  - Pydantic schema definitions with validation rules
  - FastAPI route organization and middleware
  - FastMCP tool specifications for multi-agent scenarios
  - Error response models using Pydantic

- **Step 9 (api-spec.md)**: Update API specification template
  - FastAPI route decorators and async patterns
  - Pydantic request/response model examples
  - Status code standards (200, 201, 204, 404, 422)
  - Dependency injection patterns

- **Step 12 (tasks.md)**: Add stack-specific tasks
  - Create Pydantic schemas before implementation
  - Implement FastAPI endpoints with proper typing
  - Add FastMCP tool creation for agent coordination

### 3. `execute-tasks.md` (Major Updates Required)  
**Current Focus**: Task implementation execution  
**Critical PocketFlow Integration**:

- **New Step 2.5**: **Design Document Validation**
  - Verify `docs/design.md` exists and is complete
  - Block implementation without proper design documentation
  - Validate Mermaid diagrams and utility specifications

- **Step 3 (implementation_planning)**: Restructure planning approach
  - Follow PocketFlow sequence: Utilities first, then Nodes, then Flows
  - Reference design.md for implementation guidance
  - Plan for SharedStore schema implementation

- **Step 6 (development_execution)**: Update execution standards
  - **Phase 1**: Implement utility functions with standalone tests
  - **Phase 2**: Create nodes.py following lifecycle patterns
  - **Phase 3**: Assemble flow.py connecting nodes
  - **Phase 4**: Create main.py as entry point
  - Enforce "fail fast" approach - avoid try/except in utilities
  - Use Node retry mechanisms for error handling

- **New Step 6.5**: **Design Document Adherence Check**
  - Validate implementation matches design.md specifications
  - Ensure utility functions match documented input/output contracts
  - Verify SharedStore schema implementation

**Python Stack Integration Needed**:

- **Step 2 (context_analysis)**: Add stack-specific checks
  - Verify Pydantic models in `schemas/` directory
  - Check existing FastAPI routes and middleware
  - Identify FastMCP tools already implemented

- **Step 3 (implementation_planning)**: Enhance planning with type safety
  - Plan Pydantic model creation before feature implementation
  - Design FastAPI endpoint structure with proper async patterns
  - Include API → PocketFlow Flow → Response integration pattern

- **Step 6 (development_execution)**: Update execution phases
  - **Phase 0**: Create Pydantic schemas with validation
  - **Phase 1**: Implement utility functions with type hints
  - **Phase 2**: Create FastAPI endpoints (if needed)
  - **Phase 3**: Implement PocketFlow nodes
  - **Phase 4**: Integrate API endpoints with Flows
  - **Phase 5**: Add FastMCP tools for agent coordination (if needed)

- **Step 8 (test_suite_verification)**: Comprehensive toolchain
  - Run `ruff check --fix . && ruff format .` for linting/formatting
  - Run `uvx ty check` for type checking
  - Run pytest for all tests
  - Validate Pydantic schema enforcement
  - Test FastAPI endpoints with proper status codes

- **New Step 8.5**: **Type Safety Validation**
  - Verify all functions have proper type hints
  - Ensure Pydantic models validate at boundaries
  - Check FastAPI automatic documentation generation

## Implementation Priorities

### High Priority (Essential for Complete Integration)
1. **Design-first enforcement** in both `create-spec.md` and `execute-tasks.md`
2. **8-step methodology integration** across all instruction files
3. **Utility function philosophy** (implement your own, not built-in)
4. **File structure compliance** (main.py, nodes.py, flow.py, utils/, schemas/, docs/design.md)
5. **Type safety enforcement** with Pydantic models for all data structures
6. **Development toolchain** integration (Ruff, ty, pytest, uv)

### Medium Priority (Important for Best Practices)
1. **Error handling patterns** (exceptions as flow branches, not inline handling)
2. **SharedStore schema design** using Pydantic models
3. **Node lifecycle enforcement** (prep→exec→post separation)
4. **FastAPI integration pattern** (endpoint → Flow → response)
5. **FastMCP tool specifications** for multi-agent scenarios

### Low Priority (Nice to Have)
1. **Design pattern identification** helpers
2. **Utility function templates** and examples
3. **Testing strategy enhancements**
4. **API documentation** auto-generation with FastAPI

## Key Integration Patterns to Include

### FastAPI + PocketFlow Pattern
The instruction files should include this standard pattern for API endpoints:
```python
@app.post("/process", response_model=ProcessResponse)
async def process_endpoint(request: ProcessRequest):
    flow = ProcessingWorkflow()
    shared = SharedStore({"request": request.dict()})
    await flow.run_async(shared)
    return ProcessResponse(**shared["result"])
```

### Pydantic Schema Pattern
All data structures must use Pydantic models:
```python
class ProcessRequest(BaseModel):
    data: str
    options: dict[str, Any] = {}
    
class ProcessResponse(BaseModel):
    result: str
    metadata: dict[str, Any]
```

### Standard Project Structure
```
project/
├── main.py           # FastAPI app entry point
├── nodes.py          # PocketFlow nodes
├── flow.py           # PocketFlow flows
├── schemas/          # Pydantic models
│   ├── __init__.py
│   ├── requests.py   # API request models
│   └── responses.py  # API response models
├── utils/            # Custom utilities
│   ├── __init__.py
│   ├── call_llm.py
│   └── [other_utils].py
├── docs/
│   └── design.md     # MANDATORY design document
└── requirements.txt

```

## Integrated Architecture Pattern

The updated Agent OS instructions will guide agents to build applications following this architecture:

```
FastAPI (main.py)
    ↓ receives requests
Pydantic Models (schemas/)
    ↓ validates data
PocketFlow Flows (flow.py)
    ↓ orchestrates logic
PocketFlow Nodes (nodes.py)
    ↓ executes tasks
Utility Functions (utils/)
    ↓ interfaces with external services
FastMCP Tools (when multi-agent coordination needed)
```

This ensures:
- **Type safety** at every boundary with Pydantic
- **Clear separation** between API layer and business logic
- **Modular design** with reusable nodes and utilities
- **Agent coordination** through FastMCP when needed

## Execution Approach

### Phase 1: `create-spec.md` Updates
- Add mandatory design document creation step
- Enhance LLM workflow specifications with Pydantic schemas
- Include FastAPI endpoint specifications
- Update task breakdown to follow 8-step methodology

### Phase 2: `execute-tasks.md` Updates  
- Add design document validation
- Restructure implementation phases (schemas→utilities→APIs→nodes→flows)
- Integrate comprehensive development toolchain
- Add type safety validation steps

### Phase 3: `plan-product.md` Updates
- Update tech stack defaults to Python/FastAPI/Pydantic
- Enhance mission and roadmap templates
- Add standard project structure template

This plan ensures AI agents will be properly guided through the complete PocketFlow development methodology with modern Python type safety and API standards, while maintaining the existing Agent OS workflow structure.