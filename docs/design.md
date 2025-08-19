# Agent OS + PocketFlow Framework Design Document

This document outlines the design of the Agent OS + PocketFlow framework system that generates workflow templates for end-user projects.

## Requirements

### Framework Requirements
- Generate complete PocketFlow workflow templates from specifications
- Support multiple workflow patterns (RAG, WORKFLOW, etc.)
- Create project-ready structures with dependencies and tooling
- Provide validation and testing capabilities for generated templates
- Support both base and project installations (v1.4.0 architecture)

### Template Generation Requirements
- Generate placeholder implementations that guide developers
- Create comprehensive test suites for generated workflows
- Include proper dependency management (pyproject.toml, requirements.txt)
- Generate API interfaces when FastAPI integration is requested
- Include documentation and task guidance

### Validation Requirements
- Validate template structure and syntax
- Ensure generated code follows framework conventions
- Test installation processes (base and project)
- Validate integration with Claude Code and MCP systems

## Flow Design

### Template Generation Flow
1. **Specification Input**: Accept WorkflowSpec with nodes, utilities, patterns
2. **Template Processing**: Load and process Jinja2 templates
3. **Code Generation**: Generate Python files, configs, and documentation
4. **Validation**: Run structural and syntax validation
5. **Output**: Save complete project structure to target directory

### Installation Flow
1. **Base Installation**: Install framework to ~/.agent-os/ with standards
2. **Project Installation**: Copy framework files to project .agent-os/
3. **Dependency Setup**: Configure project-specific dependencies
4. **Validation**: Test installation integrity

### Testing Flow
1. **Generator Tests**: Test template generation functionality
2. **Integration Tests**: Test framework component integration
3. **Validation Tests**: Test generated template quality
4. **End-to-End Tests**: Test complete workflow generation

## Data Design

### Core Data Structures
- `WorkflowSpec`: Defines workflow specification with nodes, utilities, patterns
- `PocketFlowGenerator`: Main generator class managing templates and output
- `DependencySpec`: Manages project dependencies and tooling configuration

### Template Data
- **Jinja2 Templates**: Reusable template files for different components
- **Pattern Templates**: Specific templates for workflow patterns (RAG, etc.)
- **Configuration Templates**: Templates for pyproject.toml, requirements, etc.

### Generated Structure
```
.agent-os/workflows/{workflow_name}/
├── docs/
│   └── design.md
├── schemas/
│   ├── __init__.py
│   └── models.py
├── utils/
│   └── {utility_functions}.py
├── tests/
│   ├── test_nodes.py
│   ├── test_flow.py
│   └── test_api.py (if FastAPI)
├── nodes.py
├── flow.py
├── main.py (if FastAPI)
├── requirements.txt
├── pyproject.toml
└── tasks.md
```

## Node Design

### Generator Nodes
- **TemplateProcessor**: Processes Jinja2 templates with spec data
- **FileGenerator**: Creates individual files from templates
- **StructureBuilder**: Constructs directory hierarchy
- **Validator**: Validates generated output

### Template Categories
- **Core Templates**: nodes.py, flow.py, schemas/models.py
- **API Templates**: main.py, router.py (for FastAPI integration)
- **Testing Templates**: test_*.py files with framework-appropriate tests
- **Configuration Templates**: pyproject.toml, requirements files
- **Documentation Templates**: design.md, tasks.md, README.md

### Validation Nodes
- **SyntaxValidator**: Checks Python syntax in generated files
- **StructureValidator**: Validates directory and file structure
- **ContentValidator**: Ensures templates have appropriate placeholder content

## Implementation Plan

### Phase 1: Core Framework ✅
- [x] Implement WorkflowSpec and PocketFlowGenerator
- [x] Create Jinja2 template system
- [x] Build basic file generation functionality
- [x] Add template validation

### Phase 2: Template Enhancement ✅
- [x] Add FastAPI integration templates
- [x] Create comprehensive test templates
- [x] Implement dependency management
- [x] Add pattern-specific templates

### Phase 3: Validation System ✅
- [x] Build syntax validation
- [x] Create structure validation
- [x] Implement content validation
- [x] Add integration test framework

### Phase 4: Installation System ✅
- [x] Implement base installation (setup/base.sh)
- [x] Create project installation (setup/project.sh)
- [x] Add migration tooling
- [x] Validate installation processes

### Phase 5: Testing and Quality ✅
- [x] Create comprehensive test suite
- [x] Add generator unit tests
- [x] Implement integration testing
- [x] Validate end-to-end workflows

### Current Status: Production Ready
The framework is complete and validated, ready for end-user project generation.
All validation tests pass and the system supports the full v1.4.0 architecture.