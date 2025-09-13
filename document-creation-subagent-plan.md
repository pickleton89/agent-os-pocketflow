# Document Creation Sub-Agent Architecture Plan

> Created: 2025-09-12
> Status: Planning Phase
> Purpose: Split document creation into specialized sub-agents to improve token efficiency and maintainability

---

## Important Distinction to be kept in mind.

**These are agents for the end user projects that use the Agent OS + PocketFlow framework.**
🎯 Framework vs Usage Statement


---

## Implementation Context Clarification

These sub-agents are Claude Code agent definitions that will execute within Claude Code sessions when users invoke framework commands (like `/plan-product`, `/analyze-product`). They are specialized agents that Claude Code will use to break down complex document creation workflows into focused, efficient components that generate actual documentation files in end-user projects.

---

## Current State Analysis

### Existing Document Creation Workflow

The current Agent OS framework contains template generation instructions that create documentation **FOR** end-user projects:

1. **plan-product.md** - Framework instruction that generates initial product documentation templates for new projects
2. **analyze-product.md** - Framework instruction that analyzes existing codebases and generates Agent OS documentation templates

**Framework Context**: These are template generators in this repository that produce documentation files **FOR** end-user projects, not tools that run **IN** end-user projects.

### Document Templates Generated (5 Total)
Framework template generators create these files **IN END-USER PROJECTS**:
- `mission.md` - Product vision, users, problems, differentiators, key features, architecture strategy
- `tech-stack.md` - Complete technical stack with modern Python defaults (FastAPI, Pydantic, uv, Ruff, ty)
- `design.md` - Initial PocketFlow design document with system architecture
- `roadmap.md` - 5-phase development roadmap with PocketFlow pattern tagging
- `CLAUDE.md` - Project instructions and workflow references

**Note**: These are generated template files that end-users customize for their specific projects.

### Current Sub-Agent Usage
Three specialized sub-agents are already in use:

1. **strategic-planner** - Strategic planning, PocketFlow integration, technology stack planning
2. **pattern-analyzer** - PocketFlow pattern analysis, template selection, requirement mapping
3. **design-document-creator** - Creates comprehensive design.md files with PocketFlow patterns

### Token Usage Bottlenecks

1. **Sequential Processing**: Each document requires full context loading
2. **Large Templates**: Complex template structures for each document type
3. **Cross-Document Dependencies**: Information flows from earlier to later documents
4. **Context Duplication**: Same information passed multiple times through workflow

## Proposed Solution: Template Generation Sub-Agents

### 1. Mission Document Template Generator Agent
**Purpose**: Specialized generation of `mission.md` template files for end-user projects

**Responsibilities**:
- User persona development and market analysis
- Problem statement articulation
- Competitive differentiator identification
- Architecture strategy with PocketFlow pattern selection
- Product pitch and value proposition development

**Input Requirements**:
- User-provided product vision and key features
- Target user information
- Strategic planning output from strategic-planner

**Token Efficiency**: Focused on product vision without technical implementation details

### 2. Tech Stack Template Generator Agent  
**Purpose**: Specialized generation of `tech-stack.md` template files for end-user projects

**Responsibilities**:
- Interactive tech stack preference gathering through targeted questions
- Modern Python toolchain recommendation and validation (uv, Ruff, ty, pytest)
- PocketFlow framework integration requirements
- Database and infrastructure decision facilitation
- LLM provider selection for AI features
- Development tooling preference collection and standardization

**Interactive Approach**:
- Ask targeted questions about user preferences rather than copying from config files
- Provide options with explanations (e.g., "Do you prefer uv or poetry for package management?")
- Validate choices against project requirements and complexity
- Offer recommendations based on modern best practices
- Confirm final selections before document generation

**Input Requirements**:
- Project complexity assessment from strategic-planner
- PocketFlow pattern requirements from pattern-analyzer
- Direct user responses to tech stack questions

**Token Efficiency**: Focused on technical architecture through interactive dialogue, avoiding redundant config file parsing

### 3. Roadmap Template Generator Agent
**Purpose**: Specialized generation of `roadmap.md` template files for end-user projects  

**Responsibilities**:
- Feature prioritization and phase planning template generation (5-phase standard)
- PocketFlow pattern tagging templates for each feature
- Effort estimation and dependency mapping templates
- Development milestone definition templates
- Risk assessment templates for complex features

**Input Requirements**:
- Product features from mission.md
- Technical constraints from tech-stack.md
- PocketFlow patterns from design.md
- Strategic timeline from strategic-planner

**Token Efficiency**: Focused on project planning without repeating product/technical details

### 4. Project Configuration Template Generator Agent
**Purpose**: Specialized generation of `CLAUDE.md` template files and project setup for end-user projects

**Responsibilities**:
- Project instruction template generation
- Cross-document reference template creation
- Workflow instruction template setup
- Development standard template enforcement
- Agent OS integration configuration templates

**Input Requirements**:
- All previous document outputs
- Project-specific customizations
- Team preferences and coding standards

**Token Efficiency**: Focused on configuration without recreating content

## Implementation Strategy

### Phase 1: Create Specialized Template Generation Agents (Immediate)
1. **Create agent definitions** for each document template type in `.claude/agents/`
2. **Maintain current sequential flow** but delegate template generation to specialized agents
3. **Optimize context passing** by providing only relevant information to each agent
4. **Test with existing workflows** to ensure template output quality matches current results

### Phase 2: Optimize Coordination (Short-term)
1. **Implement smart context management** to reduce redundant information passing
2. **Enable parallel processing** where document dependencies allow
3. **Add validation layers** to ensure consistency across documents
4. **Optimize template management** with agent-specific templates

### Phase 3: Enhanced Intelligence (Medium-term)
1. **Add document quality validation** with automated consistency checking
2. **Implement adaptive templates** based on project complexity and patterns
3. **Enable incremental updates** when project requirements change
4. **Add cross-document analysis** for gap detection and recommendations

## Expected Benefits

### Token Efficiency
- **Reduced Context Size**: Each agent receives only relevant information
- **Specialized Processing**: Agents optimized for specific document types
- **Elimination of Redundancy**: No repeated processing of same information

### Parallel Processing Opportunities
- `mission.md` and `tech-stack.md` can be created in parallel after strategic planning
- `design.md` creation can happen concurrently with mission/tech-stack refinement
- `CLAUDE.md` generation can overlap with roadmap planning

### Maintainability Improvements
- **Isolated Changes**: Updates to document templates affect only one agent
- **Specialized Expertise**: Each agent can be optimized for its domain
- **Easier Testing**: Individual agents can be tested independently
- **Better Error Handling**: Problems isolated to specific document types

### Quality Enhancements
- **Focused Analysis**: Each agent provides deeper analysis within its domain
- **Consistency**: Standardized approaches for each document type
- **Customization**: Agent-specific optimizations based on document requirements

## Technical Implementation Details

### Template Generation Agent Architecture
Each template generation agent will be implemented as:
- **Independent Claude Code agent** with specific instructions for generating templates
- **Standardized input/output interface** for coordination
- **Template-based generation** with customization capabilities for end-user projects
- **Quality validation** before template finalization

### Coordination Mechanism
- **Main orchestrator** manages agent sequence and dependencies
- **Context manager** provides relevant information to each agent
- **Validation layer** ensures cross-document consistency
- **Error handling** with fallback to current sequential approach

### Migration Path
1. **Backward Compatibility**: New system works alongside current approach
2. **Performance Monitoring**: Compare token usage and quality metrics
3. **User Feedback Integration**: Adjust based on developer experience

## Success Metrics

### Token Efficiency
- **Reduce total token consumption** by 30-50% for document creation
- **Faster processing time** through parallel execution
- **Lower cost per project initialization**

### Quality Metrics
- **Maintain or improve document quality** as measured by user satisfaction
- **Reduce inconsistencies** between documents
- **Improve template customization** based on project requirements

### Developer Experience
- **Faster project setup** through optimized workflows
- **Better documentation quality** through specialized expertise
- **Easier maintenance** of Agent OS framework

## Critical Preservation Requirements for Sub-Agent Refactoring

**⚠️ ZERO FUNCTIONALITY LOSS MANDATE**: All existing logic, interactions, and data flows must be preserved exactly.

### 1. **Must Preserve Existing Sub-Agent Coordination (5 Current Sub-Agents)**
- **strategic-planner**: Strategic roadmap, architecture recommendations, PocketFlow integration
- **pattern-analyzer**: PocketFlow pattern analysis with fallback to Agent pattern
- **design-document-creator**: Comprehensive design.md creation with preservation rules
- **Documentation Discovery System**: Interactive external documentation integration
- **File Creation & Validation System**: Template engine and validation coordination

**Coordination Requirements**:
- Current sub-agent integration patterns must be maintained
- All handoff protocols and context passing must be preserved
- Pattern analysis fallback logic must remain functional
- **Note**: Verify existence of coordination classes in framework codebase before implementation

### 2. **Must Preserve Data Flow Chain Integrity**
```
User Input → Strategic Planning → Pattern Analysis → Documentation Discovery → Document Creation → CLAUDE.md Integration
```

**Data Resolution Hierarchy** (must remain exactly as-is):
1. User Input (primary)
2. `~/.agent-os/standards/tech-stack.md` (fallback)
3. `~/.claude/CLAUDE.md` (secondary fallback) 
4. Universal Python defaults (final fallback: Python 3.12+, FastAPI, Pydantic, uv, Ruff, ty)

**Cross-Document Dependencies**:
- mission.md → tech-stack.md (tech decisions inform mission architecture)
- tech-stack.md → design.md (technical foundation informs design)
- design.md → roadmap.md (design patterns inform roadmap features)
- roadmap.md → CLAUDE.md (roadmap references in project instructions)

### 3. **Must Preserve All Template Logic & Conditional Rules**

**Mission.md Template Requirements**:
- Required sections with exact constraint specifications (pitch: 1-2 sentences, users with schema)
- Universal Architecture Strategy section generation for ALL products
- PocketFlow pattern mapping and complexity level assessment
- Mermaid diagram generation with TODO customization markers

**Tech-Stack.md Resolution Logic**:
- Universal requirements enforcement (PocketFlow, FastAPI, Pydantic, uv, Ruff, ty)
- Modern Python stack detection and migration recommendations
- Missing items request template with numbered list format
- ChromaDB as universal requirement for data storage

**Design.md Creation Rules**:
- Universal creation for all PocketFlow projects (critical priority)
- Design-first foundation establishment
- Preservation rule: Never overwrite existing architectural decisions
- Standard location: `docs/design.md`

**Roadmap.md Structure**:
- 5-phase standard with 3-7 features per phase
- PocketFlow pattern tagging for all features
- docs/design.md extension requirement before implementation

### 4. **Must Preserve Error Handling & Validation**

**Error Scenarios** (all must be preserved):
- no_clear_structure → Ask user for project clarification
- conflicting_patterns → Ask user which pattern to document
- missing_dependencies → List detected, request missing pieces
- unclear_llm_usage → Ask for PocketFlow pattern clarification
- mixed_python_tooling → Recommend uv/Ruff/ty migration
- incomplete_pocketflow → Ask to complete PocketFlow implementation

**Validation Requirements**:
- Document completeness checklists for both plan-product and analyze-product
- Cross-document consistency validation
- Universal PocketFlow architecture enforcement

### 5. **Must Preserve File Management & Integration Logic**

**CLAUDE.md Integration Strategy** (exact preservation required):
```python
if_exists_with_agent_os_section: replace_section
if_exists_without_section: append_to_end
if_not_exists: create_new_file
preservation_rule: keep_all_other_existing_content
```

**File Structure Creation**:
- `.agent-os/product/` directory with mission.md, tech-stack.md, roadmap.md
- `docs/design.md` as universal PocketFlow requirement
- Pre-flight checklist generation
- Directory structure validation before creation

### 6. **Must Preserve Modern Python Toolchain Detection**

**Detection Logic** (analyze-product.md):
- Python indicators: pyproject.toml, uv.lock, Python imports, FastAPI/Django/Flask
- Preferred toolchain: uv (exclusively), Ruff (unified linting), ty (mypy wrapper), pytest
- Legacy migration recommendations with specific guidance
- PocketFlow component detection: nodes.py, flow.py, design.md presence

### 7. **Must Preserve Interactive Documentation Discovery**

**Documentation Categories & Processing**:
- Tech Stack Documentation, External APIs, Internal Standards, Compliance
- Interactive prompts with skip options
- Content fetching, pattern extraction, storage in docs-registry.yaml
- Planning context enrichment with external constraints

## Next Steps

1. **Review and approve this plan** with stakeholders
2. **Create detailed agent specifications** for each document type that preserve ALL existing logic
3. **Implement proof-of-concept** with mission document agent, validating preservation
4. **Test integration** with existing plan-product.md workflow for zero regression
5. **Iterate based on results** before full implementation

---

*This plan provides the foundation for a more efficient, scalable document creation system that maintains the high-quality standards of Agent OS while significantly improving token efficiency and developer experience. **Critical**: All existing functionality must be preserved exactly during refactoring.*