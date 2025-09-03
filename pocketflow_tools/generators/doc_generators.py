from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def _generate_basic_mermaid(spec) -> str:
    """Generate a basic Mermaid diagram as fallback (legacy parity)."""
    lines: List[str] = [
        "```mermaid",
        "graph TD",
        "    A[Start] --> B[Input Validation]",
    ]
    prev_node = "B"
    for i, node in enumerate(spec.nodes):
        node_id = chr(ord("C") + i)
        lines.append(f"    {prev_node} --> {node_id}[{node['name']}]")
        prev_node = node_id
    lines.append(f"    {prev_node} --> Z[End]")
    lines.append("```")
    return "\n".join(lines)


def _format_customizations_for_doc(customizations: Dict[str, Any]) -> str:
    """Format customizations for documentation (legacy parity)."""
    if not customizations:
        return "- No specific customizations applied"
    formatted: List[str] = []
    for key, value in customizations.items():
        formatted.append(f"- **{key.replace('_', ' ').title()}:** {value}")
    return "\n".join(formatted)


def generate_design_doc(spec) -> str:
    """Generate design document from template (legacy base implementation)."""
    design_doc = f"""# Design Document

> Spec: {spec.name}
> Created: {datetime.now().isoformat()[:10]}
> Status: Design Phase
> Framework: PocketFlow

**CRITICAL**: This design document MUST be completed before any code implementation begins.

## Requirements

### Problem Statement
{spec.description}

### Success Criteria
- Successful implementation of {spec.pattern} pattern
- All nodes execute correctly in sequence
- Proper error handling and validation
- Complete test coverage

### Design Pattern Classification
**Primary Pattern:** {spec.pattern}
**Secondary Patterns:** FastAPI Integration (Universal)

### Input/Output Specification
- **Input Format:** Request data from API or direct invocation
- **Output Format:** Processed results with metadata
- **Error Conditions:** Validation errors, processing failures, timeout errors

## Flow Design

### High-Level Architecture
{_generate_basic_mermaid(spec)}
"""

    # Node sequence
    design_doc += "\n### Node Sequence\n"
    for i, node in enumerate(spec.nodes, 1):
        design_doc += f"{i}. **{node['name']}** - {node['description']}\n"

    # Utilities
    design_doc += "\n## Utilities\n\n"
    design_doc += 'Following PocketFlow\'s "implement your own" philosophy, specify all utility functions needed.\n\n'
    design_doc += "### Required Utility Functions\n\n"
    for utility in spec.utilities:
        design_doc += f"#### {utility['name']}\n"
        design_doc += f"- **Purpose:** {utility['description']}\n"
        params_str = ", ".join(
            [f"{p['name']}: {p['type']}" for p in utility.get("parameters", [])]
        )
        design_doc += f"- **Input:** {params_str}\n"
        design_doc += f"- **Output:** {utility.get('return_type', 'Any')}\n\n"

    # Shared store schema
    design_doc += "\n## Data Design\n\n"
    design_doc += "### SharedStore Schema\n"
    design_doc += "Following PocketFlow's shared store pattern, all data flows through a common dictionary.\n\n"
    design_doc += "```python\n"
    design_doc += "SharedStore = {\n"
    for key, value_type in spec.shared_store_schema.items():
        design_doc += f'    "{key}": {value_type},\n'
    design_doc += "}\n```\n"

    # Node design
    design_doc += "\n## Node Design\n\n"
    design_doc += "Following PocketFlow's node-based architecture, each processing step is implemented as a discrete node.\n\n"
    for i, node in enumerate(spec.nodes, 1):
        design_doc += f"### {i}. {node['name']}\n"
        design_doc += f"**Purpose:** {node['description']}\n\n"
        inputs_str = ", ".join(node.get("inputs", []) or []) or "SharedStore"
        outputs_str = ", ".join(node.get("outputs", []) or []) or "Updates SharedStore"
        design_doc += f"**Inputs:** {inputs_str}\n"
        design_doc += f"**Outputs:** {outputs_str}\n\n"

    # Implementation notes
    design_doc += "\n## Implementation Notes\n\n"
    design_doc += f"- Pattern: {spec.pattern}\n"
    design_doc += f"- Nodes: {len(spec.nodes)}\n"
    design_doc += f"- Utilities: {len(spec.utilities)}\n"
    design_doc += "- FastAPI Integration: Enabled (Universal)\n"
    design_doc += "\nThis design document was generated automatically. Please review and complete with specific implementation details."

    return design_doc


def generate_tasks(spec) -> str:
    """Generate tasks.md content (legacy parity)."""
    current_date = datetime.now().isoformat()[:10]

    tasks = f"""# Implementation Tasks for {spec.name}

This document outlines the tasks required to complete the implementation of the {spec.name} workflow.

## Overview

### Project Summary
- **Workflow Name:** {spec.name}
- **Pattern:** {spec.pattern}
- **Description:** {spec.description}
- **FastAPI Integration:** Enabled (Universal)
- **Generated On:** {current_date}

## Task Breakdown

### Phase 1: Data Modeling (Pydantic)
- [ ] 1.1 Define Pydantic models for request/response
- [ ] 1.2 Create SharedStore Pydantic model
- [ ] 1.3 Implement core entity models with validation rules
- [ ] 1.4 Create SharedStore transformation models
- [ ] 1.5 Add custom validators and field constraints
- [ ] 1.6 Create error response models with standardized format
- [ ] 1.7 Verify all Pydantic models pass validation tests

### Phase 2: Utility Functions Implementation
- [ ] 2.1 Write tests for utility functions (with mocked external dependencies)
- [x] 2.2 Implement utility functions in `utils/` directory ✓ (Generated templates)
"""

    for utility in spec.utilities:
        tasks += f"\n- [ ] 2.2.{utility['name']}: Complete implementation of `utils/{utility['name']}.py`"

    tasks += """
- [ ] 2.3 Add proper type hints and docstrings for all utilities
- [ ] 2.4 Implement LLM integration utilities (if applicable)
- [ ] 2.5 Add error handling without try/catch (fail fast approach)
- [ ] 2.6 Create standalone main() functions for utility testing
- [ ] 2.7 Verify all utility tests pass with mocked dependencies

### Phase 3: FastAPI Endpoints (Universal Architecture)
- [ ] 3.1 Write tests for FastAPI endpoints (with mocked flows)
- [x] 3.2 Create FastAPI application structure in `main.py` ✓ (Generated)
- [x] 3.3 Implement route handlers with proper async patterns ✓ (Generated)
- [x] 3.4 Add request/response model integration ✓ (Generated)
- [ ] 3.5 Implement error handling and status code mapping
- [ ] 3.6 Add authentication and middleware (if required)
- [ ] 3.7 Verify all FastAPI endpoint tests pass

### Phase 4: PocketFlow Nodes (LLM/AI Components)
- [ ] 4.1 Write tests for individual node lifecycle methods
- [x] 4.2 Implement nodes in `nodes.py` following design.md specifications ✓ (Generated templates)
"""

    for node in spec.nodes:
        tasks += f"\n- [ ] 4.2.{node['name']}: Complete implementation of {node['name']}"

    tasks += """
- [ ] 4.3 Create prep() methods for data access and validation
- [ ] 4.4 Implement exec() methods with utility function calls
- [ ] 4.5 Add post() methods for result storage and action determination
- [ ] 4.6 Implement error handling as action string routing
- [ ] 4.7 Verify all node tests pass in isolation

### Phase 5: PocketFlow Flow Assembly (LLM/AI Components)
- [ ] 5.1 Write tests for complete flow execution scenarios
- [x] 5.2 Create flow assembly in `flow.py` ✓ (Generated)
- [ ] 5.3 Connect nodes with proper action string routing
- [ ] 5.4 Implement error handling and retry strategies
- [ ] 5.5 Add flow-level logging and monitoring
- [ ] 5.6 Test all flow paths including error scenarios
- [ ] 5.7 Verify flow integration with SharedStore schema

### Phase 6: Integration & Testing
- [ ] 6.1 Write end-to-end integration tests
- [ ] 6.2 Integrate FastAPI endpoints with PocketFlow workflows
- [ ] 6.3 Test complete request→flow→response cycle
- [ ] 6.4 Validate error propagation from flow to API responses
- [ ] 6.5 Test performance under expected load
- [ ] 6.6 Verify type safety across all boundaries
- [ ] 6.7 Run complete test suite and ensure 100% pass rate

### Phase 7: Optimization & Reliability
- [ ] 7.1 Add comprehensive logging throughout the system
- [ ] 7.2 Implement caching strategies (if applicable)
- [ ] 7.3 Add monitoring and observability hooks
- [ ] 7.4 Optimize async operations and batch processing
- [ ] 7.5 Add retry mechanisms and circuit breakers
- [ ] 7.6 Create health check endpoints
- [ ] 7.7 Verify system reliability under various conditions

**Development Toolchain Validation (Every Phase):**
- Run `uv run ruff check --fix .` for linting
- Run `uv run ruff format .` for code formatting
- Run `uv run ty check` for type checking
- Run `pytest` for all tests
- Verify all checks pass before proceeding to next phase

## Generated Files Summary

The following files have been generated and need completion:

### Core Files ✓
- `docs/design.md` - Design document (review and complete)
- `schemas/models.py` - Pydantic models (review and extend)
- `nodes.py` - PocketFlow nodes (implement logic)
- `flow.py` - Flow assembly (review connections)

### Utility Files ✓
"""

    for utility in spec.utilities:
        tasks += f"\n- `utils/{utility['name']}.py` - {utility['description']}"

    tasks += """

### FastAPI Files ✓
- `main.py` - FastAPI application
- `router.py` - API routes and handlers

### Test Files ✓
- `tests/test_nodes.py` - Node unit tests
- `tests/test_flow.py` - Flow integration tests
- `tests/test_api.py` - API endpoint tests

### Next Steps
1. Review the design document and complete any missing sections
2. Implement the utility functions with actual logic
3. Complete the node implementations with proper business logic
4. Test the complete workflow end-to-end
5. Deploy and validate in staging environment

Generated on: {current_date}
Workflow Pattern: {spec.pattern}
FastAPI Integration: Enabled (Universal)
"""

    return tasks

