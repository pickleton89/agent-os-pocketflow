# Template Quality Standards

> Agent OS + PocketFlow Framework - Template Validation Criteria
> Last Updated: 2025-01-18
> 
> **Framework Context**: This defines quality standards for GENERATED templates, not end-user implementations.

---

## Overview

This document defines the quality standards and validation criteria used by the Template Validator agent to ensure generated PocketFlow templates maintain educational value while following framework patterns.

**Critical Distinction**: These standards validate template structure and educational quality, NOT functional completeness. Missing implementations and TODO stubs are intentional design features.

---

## Validation Categories

### 1. Python Syntax Validation

#### Requirements
- All generated Python files must have valid syntax
- AST parsing must succeed without errors
- Import statements must be syntactically correct
- Function and class definitions must be well-formed

#### Common Issues
- Escaped newline characters in string literals (`\\n` instead of `\n`)
- Malformed f-string expressions
- Incorrect indentation in generated code blocks
- Missing or extra quotation marks

#### Framework Perspective
- Syntax errors prevent templates from being educational starting points
- Users should not encounter parsing errors when beginning implementation
- Template syntax correctness validates framework generator quality

### 2. PocketFlow Pattern Compliance

#### Node Class Requirements
- **Inheritance**: All node classes must inherit from `Node`, `AsyncNode`, or `BatchNode`
- **Required Methods**: 
  - `prep(self, shared: Dict[str, Any]) -> Any`
  - `exec(self, prep_result: Any) -> Any` OR `async def exec_async(self, prep_result: Any) -> Any`
  - `post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None`
- **Method Signatures**: Parameter types and names must follow PocketFlow conventions
- **Async Consistency**: AsyncNode classes must use `exec_async`, Node classes use `exec`

#### Flow Class Requirements
- **Inheritance**: Must inherit from `Flow`
- **Structure**: Must define `nodes` and `edges` dictionaries in `__init__`
- **Connectivity**: Edge definitions must reference existing nodes
- **Entry/Exit Points**: Flow must have clear start and end conditions

#### Import Requirements
- PocketFlow base classes must be imported from `pocketflow`
- Type annotations must import from `typing`
- No runtime-specific imports (framework generates templates, not applications)

### 3. Pydantic Model Structure

#### BaseModel Requirements
- All data models must inherit from `pydantic.BaseModel`
- Field annotations must be present and valid
- Optional fields should use `Optional[Type]` or `Type | None`
- Model names should follow PascalCase convention

#### Field Validation
- Type annotations must be syntactically valid
- Field definitions should include helpful defaults where appropriate
- Custom validators may be stubbed but not implemented
- Model docstrings should explain purpose and usage

#### Framework Context
- Models define data contracts for templates, not working validation logic
- Validation rules can be stubbed to show intent without implementation
- Focus on structure and educational value over functional completeness

### 4. Workflow Graph Validation

#### Connectivity Requirements
- All nodes referenced in edges must exist in the nodes dictionary
- No orphaned nodes (nodes not referenced in any edge)
- No circular dependencies without proper exit conditions
- Error handling paths must be defined

#### Graph Structure
- Clear entry point (typically first node in sequence)
- Defined exit conditions (success and error paths)
- Logical flow progression that matches design intent
- Proper error routing to error handlers

#### Educational Value
- Graph structure should demonstrate PocketFlow patterns
- Edge definitions show how to handle different execution outcomes
- Templates provide clear examples of workflow design

### 5. Educational Placeholder Quality

#### TODO Comment Standards
- **Descriptive**: TODO comments must explain WHAT needs to be implemented
- **Educational**: Should guide users toward correct implementation approach
- **Specific**: Avoid generic "TODO: implement" - be specific about the task
- **Context**: Include relevant parameters, return values, or business logic hints

#### Good Examples:
```python
# TODO: Implement document retrieval from your vector database
# Parameters: query (str) - user search query
# Returns: List[Document] - relevant documents with similarity scores
def retrieve_documents(query: str) -> List[Document]:
    raise NotImplementedError("Connect to your vector database (ChromaDB, Pinecone, etc.)")
```

#### Poor Examples:
```python
# TODO: implement this
def process_data(data):
    pass
```

#### NotImplementedError Usage
- Utility functions should raise `NotImplementedError` with descriptive messages
- Error messages should suggest implementation approaches
- Include relevant context about expected functionality
- Point users toward appropriate libraries or patterns

### 6. Framework vs Usage Distinction

#### Template Characteristics
- **Placeholders**: Functions contain meaningful stubs, not working implementations
- **Educational**: Code structure demonstrates patterns without completing business logic
- **Flexible**: Templates adapt to different use cases through customization
- **Guided**: Clear TODO items direct users toward proper implementation

#### Validation Criteria
- No completed business logic implementations
- All utility functions raise NotImplementedError
- Test files use mocks and fixtures, not real implementations
- Dependencies focus on framework needs, not runtime requirements

#### Red Flags
- Working API calls or database connections
- Completed algorithms or business logic
- Hardcoded business-specific values
- Production-ready error handling

---

## Quality Levels

### ERROR Level Issues
- Python syntax errors
- Missing required PocketFlow methods
- Broken import statements
- Invalid class inheritance
- Malformed workflow graphs

### WARNING Level Issues
- Generic TODO comments
- Missing NotImplementedError in utilities
- Potential completed implementations
- Test files without pytest imports
- Models without field annotations

### INFO Level Issues
- Files without TODO comments (acceptable for simple files)
- Stylistic improvements
- Additional documentation opportunities
- Enhancement suggestions

---

## Validation Process

### Automatic Validation
1. **Generation**: Templates automatically validated after creation
2. **Integration**: Validation results displayed during generation process
3. **Reporting**: Comprehensive feedback with specific line numbers and suggestions

### Manual Validation
1. **Script**: Use `scripts/validation/validate-template-structure.sh <template_dir>`
2. **Python Module**: Use `.agent-os/workflows/template_validator.py <template_dir>`
3. **Agent Integration**: Template-validator agent automatically invoked

### Validation Reports
- **Summary**: Error, warning, and info counts
- **Categories**: Issues grouped by validation type
- **Details**: Specific file locations and suggested fixes
- **Educational**: Each issue includes learning guidance

---

## Best Practices for Framework Developers

### Generating Quality Templates
1. Use smart defaults that show implementation intent
2. Include descriptive TODO comments with context
3. Ensure proper PocketFlow pattern adherence
4. Validate templates before committing generator changes

### Improving Template Quality
1. Regular validation of existing templates
2. User feedback integration for template improvements
3. Pattern updates based on PocketFlow evolution
4. Educational value assessment and enhancement

### Framework Evolution
1. Template standards evolve with PocketFlow updates
2. Validation criteria adapt to new patterns
3. Backward compatibility maintained for existing templates
4. Clear migration paths for template updates

---

## Troubleshooting Common Issues

### Syntax Errors
- **Issue**: Escaped characters in generated strings
- **Fix**: Use proper string formatting in generator code
- **Prevention**: Test generator output with validation pipeline

### Pattern Violations
- **Issue**: Missing required methods in Node classes
- **Fix**: Update generator templates to include all required methods
- **Prevention**: Maintain generator method templates aligned with PocketFlow API

### Poor Educational Value
- **Issue**: Generic or unhelpful TODO comments
- **Fix**: Enhance generator smart defaults with context-aware messages
- **Prevention**: Regular review of generated template quality

---

## Framework Philosophy Reminder

**Templates are educational starting points, not finished applications.**

- Missing implementations are features, not bugs
- TODO stubs guide users toward correct patterns
- Template validation ensures quality guidance, not completeness
- Framework generates learning tools, not production code

This validation framework maintains the balance between structural correctness and educational value, ensuring users receive high-quality templates that teach PocketFlow patterns while remaining flexible for their specific implementations.