# Task Templates

> Version: 2.0  
> Last Updated: 2025-01-08  
> Purpose: Templates for 8-step Agentic Coding methodology task breakdowns

## Overview

This file contains task breakdown templates following PocketFlow's 8-step Agentic Coding methodology. These templates ensure proper sequencing from design through implementation to optimization.

## 8-Step Methodology Overview

Following PocketFlow's "Agentic Coding" methodology:
1. **Requirements** (human-led)
2. **Flow Design** (collaborative)
3. **Utilities** (collaborative)
4. **Data Design** (AI-led)
5. **Node Design** (AI-led)
6. **Implementation** (AI-led)
7. **Optimization** (collaborative)
8. **Reliability** (AI-led)

## Cross-Reference Navigation

### Related Documents (Created in End-User Projects)
- **Design Document**: @docs/design.md - Complete feature design (must exist before tasks)
- **PocketFlow Templates**: @templates/pocketflow-templates.md - Design and spec templates (from framework)
- **Spec Document**: @.agent-os/specs/[spec-name]/spec.md - Feature specification (created by end-user)
- **Mission Document**: @docs/mission.md - Product goals and context (created by end-user)
- **Roadmap Document**: @docs/roadmap.md - Feature prioritization (created by end-user)

### Template Cross-References
- **Design Template**: Line 211 in @templates/pocketflow-templates.md
- **LLM Workflow Template**: Line 408 in @templates/pocketflow-templates.md
- **FastAPI Templates**: @templates/fastapi-templates.md

### Documentation Standards
- **Design Document Required**: Phase 0 must be completed before any implementation
- **Cross-Link Format**: Use @-notation for internal references
- **Validation Links**: Include documentation URLs for external dependencies

### Version Compatibility Warnings
⚠️ **IMPORTANT**: Verify all dependency versions before starting implementation

#### Critical Version Checks (For End-User Projects)
- **Python**: 3.8+ required for modern async patterns
- **Agent OS + PocketFlow Framework**: Requires framework installation (this repository provides templates)
- **FastAPI**: 0.100.0+ for proper async/await support
- **Pydantic**: v2.x only (v1.x is incompatible with templates)

#### Pre-Implementation Validation Tasks
- [ ] **Check LLM Provider Status**: Verify API endpoints and model availability
- [ ] **Validate API Documentation**: Ensure all referenced APIs are current
- [ ] **Version Compatibility Matrix**: Create compatibility matrix in design.md
- [ ] **Deprecation Warnings**: Document any deprecated dependencies

## Task Organization Phases

- **Phase 0:** Design Document Creation (mandatory for LLM/AI)
- **Phase 1:** Pydantic Schemas & Data Models
- **Phase 2:** Utility Functions Implementation
- **Phase 3:** FastAPI Endpoints (if applicable)
- **Phase 4:** PocketFlow Nodes (for LLM/AI)
- **Phase 5:** PocketFlow Flow Assembly (for LLM/AI)
- **Phase 6:** Integration & Testing
- **Phase 7:** Optimization & Reliability

## Complete Task Template

### For tasks.md File

```markdown
# Spec Tasks

These are the tasks to be completed for the spec detailed in @.agent-os/specs/YYYY-MM-DD-spec-name/spec.md

> Created: [CURRENT_DATE]
> Status: Ready for Implementation

## Tasks

Following PocketFlow's 8-step Agentic Coding methodology:

### Phase 0: Design Document (LLM/AI Components Only)
- [ ] 0.1 Create `docs/design.md` with complete PocketFlow design
- [ ] 0.2 Define Requirements section with problem statement and success criteria
- [ ] 0.3 Create Flow Design with Mermaid diagram and node sequence
- [ ] 0.4 Specify all Utility functions with input/output contracts
- [ ] 0.5 Define SharedStore schema with complete data structure
- [ ] 0.6 Detail Node Design with prep/exec/post specifications
- [ ] 0.7 Add External Documentation References section with:
  - [ ] Framework documentation links and version compatibility
  - [ ] API integration documentation and rate limits
  - [ ] Compliance requirements and validation criteria
- [ ] 0.8 Validate design completeness before proceeding
- [ ] 0.9 Verify all documentation links are accessible and current

### Phase 1: Pydantic Schemas & Data Models
- [ ] 1.1 Write tests for Pydantic model validation
- [ ] 1.2 Create request/response models in `schemas/requests.py` and `schemas/responses.py`
- [ ] 1.3 Implement core entity models with validation rules
- [ ] 1.4 Create SharedStore transformation models
- [ ] 1.5 Add custom validators and field constraints
- [ ] 1.6 Create error response models with standardized format
- [ ] 1.7 Verify all Pydantic models pass validation tests

### Phase 2: Utility Functions Implementation
- [ ] 2.1 Write tests for utility functions (with mocked external dependencies)
- [ ] 2.2 Implement utility functions in `utils/` directory (one file per function)
- [ ] 2.3 Add proper type hints and docstrings for all utilities
- [ ] 2.4 Implement LLM integration utilities (if applicable)
  - [ ] Validate API documentation links and endpoint specifications
  - [ ] Verify authentication methods against provider documentation
  - [ ] Check rate limits and implement according to documentation
- [ ] 2.5 Add error handling without try/catch (fail fast approach)
- [ ] 2.6 Create standalone main() functions for utility testing
- [ ] 2.7 Verify all utility tests pass with mocked dependencies
- [ ] 2.8 Cross-reference implementation against design.md documentation sections

### Phase 3: FastAPI Endpoints (If Applicable)
- [ ] 3.1 Write tests for FastAPI endpoints (with mocked flows)
- [ ] 3.2 Create FastAPI application structure in `main.py`
- [ ] 3.3 Implement route handlers with proper async patterns
- [ ] 3.4 Add request/response model integration
- [ ] 3.5 Implement error handling and status code mapping
- [ ] 3.6 Add authentication and middleware (if required)
- [ ] 3.7 Verify all FastAPI endpoint tests pass

### Phase 4: PocketFlow Nodes (LLM/AI Components)
- [ ] 4.1 Write tests for individual node lifecycle methods
- [ ] 4.2 Implement nodes in `nodes.py` following design.md specifications
- [ ] 4.3 Create prep() methods for data access and validation
- [ ] 4.4 Implement exec() methods with utility function calls
- [ ] 4.5 Add post() methods for result storage and action determination
- [ ] 4.6 Implement error handling as action string routing
- [ ] 4.7 Verify all node tests pass in isolation

### Phase 5: PocketFlow Flow Assembly (LLM/AI Components)
- [ ] 5.1 Write tests for complete flow execution scenarios
- [ ] 5.2 Create flow assembly in `flow.py`
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
- [ ] 6.7 Validate integration against documented API specifications
  - [ ] Test all documented endpoints and parameters
  - [ ] Verify error responses match API documentation
  - [ ] Validate rate limiting implementation against documentation
- [ ] 6.8 Create cross-reference validation between implementation and design.md
- [ ] 6.9 Run complete test suite and ensure 100% pass rate

### Phase 7: Optimization & Reliability
- [ ] 7.1 Add comprehensive logging throughout the system
- [ ] 7.2 Implement caching strategies (if applicable)
- [ ] 7.3 Add monitoring and observability hooks
- [ ] 7.4 Optimize async operations and batch processing
- [ ] 7.5 Add retry mechanisms and circuit breakers
- [ ] 7.6 Create health check endpoints
- [ ] 7.7 Verify system reliability under various conditions

**Development Toolchain Validation (Every Phase):**
- Run `ruff check --fix .` for linting
- Run `ruff format .` for code formatting  
- Run `uvx ty check` for type checking
- Run `pytest` for all tests
- Verify all checks pass before proceeding to next phase

**Version Compatibility Validation (Every Phase):**
- ⚠️ Check for dependency updates before each phase
- ⚠️ Validate API endpoints are still accessible
- ⚠️ Verify model/service availability (for LLM integrations)
- ⚠️ Review breaking changes in dependency changelogs
```

## Phase Dependencies

### Dependency Chain
- Phase 0 (Design) → blocks all implementation phases
- Phase 1 (Data Models) → required for Phases 2-7
- Phase 2 (Utilities) → required for Phase 4 (Nodes)
- Phase 3 (FastAPI) → can run parallel with Phase 4-5
- Phase 4 (Nodes) → required for Phase 5 (Flow)
- Phase 5 (Flow) → required for Phase 6 (Integration)
- Phase 6 (Integration) → required for Phase 7 (Optimization)

### Quality Gates
- Every phase ends with toolchain validation
- No phase progression without 100% test pass rate
- Type safety enforced at every step
- Design adherence validated continuously

## Ordering Principles

### Agentic Methodology
- **Design First:** Complete design.md before any implementation
- **TDD Throughout:** Write tests before implementation in every phase
- **Utility Foundation:** Build utility functions before nodes
- **Data Models Early:** Pydantic schemas provide type safety foundation
- **Flow Assembly Last:** Connect nodes only after individual validation
- **Fail Fast:** Avoid try/catch in early phases, let errors surface
- **Type Safety:** Enforce at every boundary with proper toolchain

## Simplified Task Template (Non-LLM Features)

### For Traditional Features Without AI/LLM Components

```markdown
# Spec Tasks

These are the tasks to be completed for the spec detailed in @.agent-os/specs/YYYY-MM-DD-spec-name/spec.md

> Created: [CURRENT_DATE]
> Status: Ready for Implementation

## Tasks

Following modern Python development practices:

### Phase 1: Data Models & Validation
- [ ] 1.1 Write tests for Pydantic model validation
- [ ] 1.2 Create request/response models in `schemas/`
- [ ] 1.3 Implement core entity models with validation rules
- [ ] 1.4 Create error response models with standardized format
- [ ] 1.5 Verify all Pydantic models pass validation tests

### Phase 2: Business Logic Implementation
- [ ] 2.1 Write tests for core business logic functions
- [ ] 2.2 Implement utility functions in `utils/` directory
- [ ] 2.3 Add proper type hints and docstrings
- [ ] 2.4 Implement database operations (if applicable)
- [ ] 2.5 Verify all utility tests pass

### Phase 3: FastAPI Integration
- [ ] 3.1 Write tests for FastAPI endpoints
- [ ] 3.2 Create FastAPI application structure in `main.py`
- [ ] 3.3 Implement route handlers with proper async patterns
- [ ] 3.4 Add request/response model integration
- [ ] 3.5 Implement error handling and status code mapping
- [ ] 3.6 Add authentication and middleware (if required)
- [ ] 3.7 Verify all FastAPI endpoint tests pass

### Phase 4: Integration & Testing
- [ ] 4.1 Write end-to-end integration tests
- [ ] 4.2 Test complete request→response cycle
- [ ] 4.3 Validate error handling and edge cases
- [ ] 4.4 Test performance under expected load
- [ ] 4.5 Verify type safety across all boundaries
- [ ] 4.6 Run complete test suite and ensure 100% pass rate

**Development Toolchain Validation (Every Phase):**
- Run `ruff check --fix .` for linting
- Run `ruff format .` for code formatting  
- Run `uvx ty check` for type checking
- Run `pytest` for all tests
- Verify all checks pass before proceeding to next phase

**Version Compatibility Validation (Every Phase):**
- ⚠️ Check for dependency updates before each phase
- ⚠️ Validate API endpoints are still accessible
- ⚠️ Verify model/service availability (for LLM integrations)
- ⚠️ Review breaking changes in dependency changelogs
```

## Task Customization Guidelines

### When to Use Which Template

**Use Complete 8-Phase Template When:**
- Spec involves LLM/AI components
- Using PocketFlow for workflow orchestration
- Complex multi-step processing required
- Need SharedStore data management

**Use Simplified Template When:**
- Traditional CRUD operations
- Simple API endpoints
- No LLM/AI processing
- Straightforward business logic

### Template Customization

**Always Include:**
- Development toolchain validation at every phase
- TDD approach with tests before implementation
- Type safety enforcement with Pydantic
- Proper error handling and status codes

**Customize Based On:**
- Specific tech stack requirements
- Database integration needs
- Authentication/authorization requirements
- Performance and scalability needs
- Third-party service integrations

## Testing Strategy

### Test Organization
- **Unit Tests:** Individual functions and classes
- **Integration Tests:** API endpoints and workflows
- **End-to-End Tests:** Complete user scenarios
- **Performance Tests:** Load and stress testing

### Mock Strategy
- Mock external dependencies in unit tests
- Use test databases for integration tests
- Mock LLM calls for deterministic testing
- Test error scenarios and edge cases

### Quality Metrics
- 100% test pass rate required for phase progression
- Type checking must pass without errors
- Linting must pass with no violations
- Code formatting must be consistent