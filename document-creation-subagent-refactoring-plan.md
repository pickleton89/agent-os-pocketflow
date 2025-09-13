# Document Creation Sub-Agent Refactoring Plan

> Created: 2025-09-13
> Status: Planning Phase
> Purpose: Refactor document creation from core instructions into specialized sub-agents

---

## Project Overview

### Problem Statement
Currently, document creation logic is embedded within the `instructions/core/` files. When end-users invoke these core instructions (e.g., `/plan-product`, `/create-spec`), the document creation process happens sequentially within a single Claude Code conversation. This creates a token-heavy process that consumes Claude Code's context window, leading to degraded performance and sub-optimal document generation.

### Solution Architecture
Extract document creation logic from core instructions and move it into specialized sub-agents located in `claude-code/agents/`. Each document type gets its own focused sub-agent that operates in an isolated context, preventing token bloat and improving generation quality.

### Target Installation Location
These sub-agents will be installed in end-user projects at `claude-code/agents/` when the framework is set up, allowing core instructions to delegate document creation to specialized agents.

---

## Document Creation Inventory

Based on investigation of `instructions/core/` directory, here are all documents created:

### From `plan-product.md`:
1. **mission.md** - Step 3: Product vision, users, problems, differentiators, features, architecture strategy
2. **tech-stack.md** - Step 4: Technical architecture, modern Python defaults, PocketFlow integration
3. **design.md** - Step 4.5: Initial PocketFlow design document with system architecture
4. **pre-flight.md** - Step 5.5: Pre-flight checklist based on PocketFlow best practices
5. **roadmap.md** - Step 6: 5-phase development roadmap with PocketFlow pattern tagging
6. **CLAUDE.md** - Step 7: Project instructions and workflow references (create/update)

### From `analyze-product.md`:
- **All same documents as `plan-product.md`** but with codebase analysis context
- **design.md** - Step 1.7: Assessment and creation/enhancement of existing design docs

### From `create-spec.md`:
7. **spec.md** - Step 7: Spec requirements document with overview, user stories, scope
8. **technical-spec.md** - Step 8: Technical specification with approach and dependencies
9. **database-schema.md** - Step 9: Database changes and migration specs (conditional)
10. **api-spec.md** - Step 10: API specification with FastAPI endpoints (conditional)
11. **tests.md** - Step 11: Test specifications with coverage requirements
12. **tasks.md** - Step 13: Task breakdown using PocketFlow patterns
13. **design.md** - Step 4.5: Mandatory design document creation (same as plan-product)

### Non-Document-Creating Instructions:
- `execute-tasks.md`, `execute-task.md`, `post-execution-tasks.md` - No document creation
- `documentation-discovery.md` - Processes docs but doesn't create them

---

## Required Sub-Agents

### 1. Mission Document Creator Agent
**Location**: `claude-code/agents/mission-document-creator.md`
**Extracts From**: `plan-product.md` Step 3, `analyze-product.md` Step 3
**Creates**: `.agent-os/product/mission.md`
**Responsibilities**:
- Product vision and pitch development (1-2 sentences)
- User persona development with schema requirements
- Problem statement articulation with quantifiable impact
- Competitive differentiator identification with evidence
- Key feature organization by category (8-10 features)
- Universal Architecture Strategy section with PocketFlow patterns
- Mermaid diagram generation with customization markers

### 2. Tech Stack Document Creator Agent
**Location**: `claude-code/agents/tech-stack-document-creator.md`
**Extracts From**: `plan-product.md` Step 4, `analyze-product.md` Step 4
**Creates**: `.agent-os/product/tech-stack.md`
**Responsibilities**:
- Modern Python toolchain documentation (FastAPI, Pydantic, uv, Ruff, ty)
- Interactive tech stack preference gathering through targeted questions
- Universal PocketFlow framework integration requirements
- Database and infrastructure decision documentation
- Missing items request template with numbered list format
- ChromaDB as universal requirement documentation

### 3. Design Document Creator Agent
**Location**: `claude-code/agents/design-document-creator.md` (already exists)
**Extracts From**: `plan-product.md` Step 4.5, `analyze-product.md` Step 1.7, `create-spec.md` Step 4.5
**Creates**: `docs/design.md`
**Current Status**: Already implemented as sub-agent
**Action Needed**: Verify this agent handles all design document creation patterns

### 4. Pre-Flight Checklist Creator Agent
**Location**: `claude-code/agents/pre-flight-checklist-creator.md`
**Extracts From**: `plan-product.md` Step 5.5
**Creates**: `.agent-os/checklists/pre-flight.md`
**Responsibilities**:
- Generate comprehensive checklist based on PocketFlow best practices
- Cover 9 critical areas: Requirements, Architecture, Data Flow, Node Selection, Utilities, Error Handling, Testing, Performance, Deployment
- Include actionable TODO items with guidance
- Reference relevant documentation sections

### 5. Roadmap Document Creator Agent
**Location**: `claude-code/agents/roadmap-document-creator.md`
**Extracts From**: `plan-product.md` Step 6, `analyze-product.md` Step 6
**Creates**: `.agent-os/product/roadmap.md`
**Responsibilities**:
- 5-phase development roadmap generation (3-7 features per phase)
- PocketFlow pattern tagging for all features (WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE)
- Effort estimation using standard scale (XS/S/M/L/XL)
- Universal design-first requirement enforcement
- Feature prioritization and dependency mapping
- Mark completed features as "Phase 0: Already Completed" for analyze-product

### 6. CLAUDE.md Manager Agent
**Location**: `claude-code/agents/claude-md-manager.md`
**Extracts From**: `plan-product.md` Step 7, `analyze-product.md` Step 7
**Creates/Updates**: `CLAUDE.md`
**Responsibilities**:
- Agent OS documentation section creation/replacement
- Smart merge strategy (replace section/append/create new)
- Cross-document references to all product documentation
- Workflow instruction setup
- Preserve all existing non-Agent OS content

### 7. Spec Document Creator Agent
**Location**: `claude-code/agents/spec-document-creator.md`
**Extracts From**: `create-spec.md` Step 7
**Creates**: `.agent-os/specs/YYYY-MM-DD-spec-name/spec.md`
**Responsibilities**:
- Spec requirements document with all required sections
- Overview, user stories, scope definition
- Out of scope boundary setting
- Expected deliverable specification
- API & Data Models using FastAPI templates
- Universal PocketFlow Architecture section

### 8. Technical Spec Creator Agent
**Location**: `claude-code/agents/technical-spec-creator.md`
**Extracts From**: `create-spec.md` Step 8
**Creates**: `.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/technical-spec.md`
**Responsibilities**:
- Technical specification with functionality details
- UI/UX specifications and integration requirements
- External dependencies documentation with justification
- Pydantic and FastAPI sections using templates
- Universal PocketFlow sections (utilities, SharedStore, nodes)

### 9. Database Schema Creator Agent
**Location**: `claude-code/agents/database-schema-creator.md`
**Extracts From**: `create-spec.md` Step 9
**Creates**: `.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/database-schema.md`
**Conditional**: Only when database changes needed
**Responsibilities**:
- Database changes specification (tables, columns, modifications)
- Migration syntax documentation
- Index and constraint specifications
- Foreign key relationship documentation
- Performance considerations and data integrity rules

### 10. API Spec Creator Agent
**Location**: `claude-code/agents/api-spec-creator.md`
**Extracts From**: `create-spec.md` Step 10
**Creates**: `.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/api-spec.md`
**Conditional**: Only when API changes needed
**Responsibilities**:
- Complete API specification using FastAPI templates
- Endpoint documentation with proper HTTP methods
- Pydantic model specifications
- PocketFlow integration patterns
- Status code and error handling documentation

### 11. Test Specification Creator Agent
**Location**: `claude-code/agents/test-spec-creator.md`
**Extracts From**: `create-spec.md` Step 11
**Creates**: `.agent-os/specs/YYYY-MM-DD-spec-name/sub-specs/tests.md`
**Responsibilities**:
- Comprehensive test coverage specification
- Unit, integration, and feature test planning
- Mocking requirements for external services
- Universal PocketFlow pattern tests (workflow, node execution, data flow)
- Performance and end-to-end test specifications

### 12. Task Breakdown Creator Agent
**Location**: `claude-code/agents/task-breakdown-creator.md`
**Extracts From**: `create-spec.md` Step 13
**Creates**: `.agent-os/specs/YYYY-MM-DD-spec-name/tasks.md`
**Responsibilities**:
- Task breakdown using appropriate PocketFlow templates
- Complex patterns: Full 8-phase template (Design → Pydantic → Utilities → FastAPI → Nodes → Flow → Integration → Optimization)
- Simple patterns: Streamlined template (Design → Data Models → Utilities → Nodes → Flow → Integration & Testing)
- Proper phase dependencies and toolchain validation

---

## Implementation Plan

### Phase 1: Core Document Agents (Priority 1)
**Timeline**: Immediate implementation
**Agents**: 1, 2, 4, 5, 6 (mission, tech-stack, pre-flight, roadmap, CLAUDE.md)
**Rationale**: These handle the primary product documentation from plan-product/analyze-product

**Tasks**:
1. Create agent definitions for each document type
2. Extract document creation logic from core instructions
3. Implement context passing interfaces
4. Update core instructions to call sub-agents instead of inline creation
5. Test with existing plan-product workflow

### Phase 2: Spec Creation Agents (Priority 2)
**Timeline**: After Phase 1 completion
**Agents**: 7, 8, 11, 12 (spec, technical-spec, tests, tasks)
**Rationale**: Handle the core spec documentation from create-spec

**Tasks**:
1. Create spec-focused agent definitions
2. Extract complex template logic from create-spec
3. Implement conditional creation logic
4. Update create-spec to use sub-agents
5. Test complete spec creation workflow

### Phase 3: Conditional Document Agents (Priority 3)
**Timeline**: After Phase 2 completion
**Agents**: 9, 10 (database-schema, api-spec)
**Rationale**: Handle conditional document creation

**Tasks**:
1. Create conditional agent definitions
2. Implement decision tree logic for when to invoke
3. Update create-spec conditional steps
4. Test conditional creation scenarios

### Phase 4: Optimization and Integration (Priority 4)
**Timeline**: After core functionality complete
**Focus**: Performance optimization and coordination

**Tasks**:
1. Implement parallel processing where possible
2. Optimize context passing between agents
3. Add validation layers for consistency
4. Enhanced error handling and fallbacks
5. Performance monitoring and metrics

---

## Sub-Agent Design and Implementation Standards

### Core Architecture Principles

#### Isolated Context & Single Responsibility
Each sub-agent operates independently with a singular focus, preventing context pollution while maintaining specialized expertise. This architecture ensures that each document creation sub-agent concentrates exclusively on one document type, avoiding the pitfalls of monolithic designs that attempt to handle multiple responsibilities.

#### Structure Requirements
Every sub-agent follows a consistent structure:
- **YAML frontmatter** defining name, description, tools, color, and optional flags
- **Clear purpose statement** immediately following frontmatter
- **Core Responsibilities section** listing 4-5 main duties
- **Detailed methodology sections** specific to the agent's domain
- **Workflow Process** with step-by-step procedures
- **Output Format section** with structured Success/Error response templates
- **Context Requirements** explicitly defining input/output expectations
- **Integration Points** documenting coordination with other agents
- **TODO placeholders** for future ToolCoordinator integration

### Critical Success Factors

1. **Single Responsibility Principle** - The most critical factor. Each agent must focus on ONE specific task only.
2. **Tool Restrictions** - Apply principle of least privilege. Document creation agents typically need only Read, Write, and Edit tools.
3. **Proactive Usage Pattern** - Use strong keywords "MUST BE USED PROACTIVELY" rather than weak "Use proactively" to ensure automatic invocation by Claude Code.
4. **Structured Output Format** - Predictable, consistent outputs with clear success/error formats enable proper integration back into the main workflow.
5. **Explicit Context Management** - Clearly defined input/output context requirements ensure proper information flow between main conversation and sub-agent.

### Implementation Standards

#### Documentation Style
- Structured markdown with clear hierarchies
- Template sections for reusable content generation
- Code examples demonstrating integration patterns
- Explicit constraints and quality standards
- Clear success indicators and comprehensive error handling

#### Key Architectural Features
- Self-contained agents with precisely defined tool access
- Clear handoff protocols between agents
- Template-driven outputs ensuring consistency
- Focused domain expertise without scope creep
- Integration guidance maintaining loose coupling

### Common Pitfalls to Avoid

- **Single Responsibility Violations** - Never combine multiple document types in one agent
- **Missing Output Specifications** - Always define structured output formats
- **Excessive Tool Access** - Restrict tools to minimum necessary for the task
- **Weak Invocation Keywords** - Use "MUST BE USED PROACTIVELY" for reliable automation
- **Absent Context Documentation** - Always specify required input context and expected outputs

This architecture ensures each document creation process operates in its own context window, preventing token accumulation while maintaining optimal quality through specialized, focused sub-agents.

---

## Technical Implementation Details

### Agent Architecture
Each document creation agent will:
- **Independent Operation**: Run in isolated Claude Code context
- **Standardized Interface**: Accept structured input, return document content
- **Template Integration**: Use existing templates from `templates/` directory
- **Error Handling**: Graceful degradation with fallback to current approach
- **Validation**: Ensure output meets quality standards before returning

### Context Management
- **Input Specification**: Each agent receives only relevant data for its document type
- **Structured Parameters**: Consistent input format across all agents
- **Output Validation**: Verify document completeness before handoff
- **Dependency Handling**: Manage cross-document references and dependencies

### Core Instruction Modifications
Each core instruction will be modified to:
- **Agent Invocation**: Replace inline document creation with agent calls
- **Context Preparation**: Prepare and pass relevant context to each agent
- **Result Integration**: Receive and process agent outputs
- **Error Handling**: Fallback to current approach if agent fails
- **Orchestration**: Manage agent sequence and dependencies

### Backward Compatibility
- **Parallel Operation**: New system runs alongside current approach initially
- **Fallback Mechanism**: Automatic fallback if agent system fails
- **Gradual Migration**: Phase-by-phase rollout with testing at each stage
- **Performance Monitoring**: Compare token usage and quality metrics

---

## Success Metrics

### Token Efficiency Goals
- **30-50% reduction** in total token consumption for document creation
- **Faster processing** through context isolation and potential parallel execution
- **Lower cost** per project initialization and spec creation

### Quality Preservation
- **Zero functionality loss**: All existing document creation logic preserved
- **Maintain consistency**: Cross-document references and dependencies intact
- **Template compliance**: All existing templates and validation preserved
- **User experience**: Same or better quality documentation output

### Development Experience
- **Faster project setup** through optimized workflows
- **Better maintainability** with isolated document creation logic
- **Easier testing** of individual document creation components
- **Clearer debugging** when document creation issues occur

---

## Risk Mitigation

### Technical Risks
- **Agent coordination complexity**: Start with sequential execution, add parallelization later
- **Context passing errors**: Implement comprehensive validation and fallback mechanisms
- **Template integration issues**: Thorough testing with existing template system
- **Performance degradation**: Monitor and compare with current system

### Implementation Risks
- **Breaking existing workflows**: Comprehensive testing before deployment
- **User adoption resistance**: Maintain backward compatibility during transition
- **Maintenance overhead**: Document agent interfaces and dependencies clearly
- **Debugging complexity**: Implement clear error reporting and logging

---

## Next Steps

### Immediate Actions (Week 1)
1. **Create Phase 1 agents** - mission, tech-stack, pre-flight, roadmap, CLAUDE.md creators
2. **Extract document creation logic** from plan-product.md and analyze-product.md
3. **Implement basic context passing** between core instructions and agents
4. **Test mission document creation** as proof of concept

### Short Term (Week 2-3)
1. **Complete Phase 1 agent implementation** and testing
2. **Update plan-product.md and analyze-product.md** to use sub-agents
3. **Validate zero functionality loss** through comprehensive testing
4. **Begin Phase 2 implementation** for spec creation agents

### Medium Term (Month 2)
1. **Complete all agent implementations** through Phase 3
2. **Optimize coordination mechanisms** and context management
3. **Implement parallel processing** where document dependencies allow
4. **Performance testing and optimization**

### Long Term (Month 3+)
1. **Advanced coordination features** and smart context management
2. **Quality validation automation** and consistency checking
3. **Adaptive templates** based on project complexity
4. **Cross-document analysis** and recommendation systems

---

*This plan provides a systematic approach to refactoring document creation into specialized sub-agents while preserving all existing functionality and improving token efficiency and maintainability.*