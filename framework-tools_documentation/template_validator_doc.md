How does the template_validator.py file work?

The template_validator.py file is a comprehensive validation system for
  PocketFlow templates. Here's how it works:

  Core Architecture

  The validator uses three main classes:

  - ValidationIssue - Represents individual problems with severity levels
  (ERROR, WARNING, INFO)
  - ValidationResult - Aggregates issues for a file/directory with overall
  validity status
  - PocketFlowValidator - Main validation engine that orchestrates all checks

  Validation Process

  1. Directory-Level Validation (validate_directory)

  - Checks if template directory exists
  - Finds all Python files recursively
  - Validates each Python file individually
  - Validates overall template structure
  - Returns aggregated results

  2. File-Level Validation (validate_file)

  - Syntax validation - Uses AST parsing to catch Python syntax errors
  - Type-specific validation - Different rules based on file name/location:
    - nodes.py → PocketFlow node pattern validation
    - flow.py → Flow structure validation
    - models.py/schemas → Pydantic model validation
    - utils/ → Utility function validation
    - tests/ → Test file validation
  - Quality checks - Placeholder quality and framework distinction

  3. Specialized Validators

  Node Validation (_validate_nodes_file):
  - Checks for required PocketFlow imports (Node, AsyncNode, BatchNode)
  - Validates each node class has required methods (prep, post,
  exec/exec_async)
  - Verifies method signatures match PocketFlow patterns

  Flow Validation (_validate_flow_file):
  - Ensures Flow import and class inheritance
  - Checks for __init__ method
  - Validates nodes/edges configuration presence

  Model Validation (_validate_pydantic_models):
  - Checks BaseModel imports and inheritance
  - Validates field definitions

  4. Quality Assurance

  Placeholder Quality (_validate_placeholder_quality):
  - Counts TODO comments (flags files with none)
  - Identifies generic/poor TODO messages
  - Promotes educational placeholder content

  Framework Distinction (_validate_framework_distinction):
  - Detects potentially completed implementations without TODO markers
  - Ensures templates remain educational starting points, not finished code

  5. Structure Validation

  Required Files:
  - nodes.py, flow.py, schemas/models.py

  Design Documentation:
  - Requires docs/design.md
  - Validates Mermaid diagram presence
  - Checks for required sections (Requirements, Flow Design, Node
  Design/Specifications)

  CLI Usage

  python template_validator.py <template_directory>

  The validator generates detailed reports showing errors, warnings, and
  suggestions grouped by category, helping developers ensure their generated
  templates follow PocketFlow patterns and maintain educational value.

---

How does it actually work in the context of this project?

⏺ Based on examining the codebase, here's how the template_validator.py
  actually works in the context of this Agent OS + PocketFlow framework
  project:

  Project Integration Architecture

  The template validator operates as part of a layered validation system:

  1. Core Validation Engine (framework-tools/template_validator.py)

  - Single source of truth for all PocketFlow template validation logic
  - Contains comprehensive AST-based Python validation
  - Validates PocketFlow patterns, Pydantic models, workflow structure
  - Used by multiple validation scripts as the canonical validator

  2. Shell Script Wrappers

  - validate-template-structure.sh: Basic structural checks + delegates to
  Python validator
  - validate-design-docs.sh: Validates design documentation using the Python
  validator
  - Multiple orchestration scripts reference the core validator

  3. Python Wrapper (validate-generation.py)

  - Dynamically imports the core validator module
  - Adds code quality checks (ruff linting, type checking)
  - Maps validation results to consistent error/warning format
  - Used for validating generated workflow directories

  Framework Context Usage

  Framework Development (this repository):

  The validator ensures the framework itself generates proper templates:

  # Direct usage for validating generated templates
  python3 framework-tools/template_validator.py
  .agent-os/workflows/my_workflow

  # Via wrapper scripts
  ./scripts/validation/validate-template-structure.sh
  .agent-os/workflows/my_workflow
  ./scripts/validation/validate-generation.py --workflow my_workflow

  End-User Project Usage:

  The validator gets copied to end-user projects via setup scripts:
  - setup/base.sh and setup/project.sh copy the validator
  - Creates .claude/agents/template-validator.md agent definition
  - End-user projects can then validate their generated workflows

  Validation Flow

  1. Template Generation → Generator creates workflow templates
  2. Core Validation → template_validator.py performs comprehensive checks
  3. Quality Validation → Wrapper adds linting/type checking
  4. Integration Validation → Shell scripts verify framework integration
  5. Orchestration Validation → Higher-level scripts coordinate the process

  Key Design Principles

  Framework vs Usage Distinction: The validator enforces that generated
  templates are meaningful placeholders, not completed implementations:
  - Validates TODO stubs are educational
  - Ensures NotImplementedError usage for unimplemented functions
  - Prevents completed business logic in templates
  - Maintains learning value for developers

  Educational Philosophy: Templates should guide implementation without doing
  the work:
  - AST analysis ensures proper structure without functionality
  - Validates PocketFlow patterns are correctly stubbed
  - Checks that placeholders show clear implementation intent

  The validator is essentially the quality gate ensuring this framework
  generates proper starting-point templates rather than finished applications.

---

How does the template_validator.py get called or activated for use?

⏺ The template_validator.py gets called or activated through multiple pathways
  in this project:

  1. Direct CLI Usage

  # Direct invocation as standalone script
  python3 framework-tools/template_validator.py <template_directory>

  # Example usage
  python3 framework-tools/template_validator.py
  .agent-os/workflows/my_workflow

  2. Shell Script Wrappers

  validate-template-structure.sh

  ./scripts/validation/validate-template-structure.sh
  .agent-os/workflows/my_workflow
  - Does basic structural checks first
  - Then calls: python3 framework-tools/template_validator.py "$TEMPLATE_DIR"

  validate-design-docs.sh

  ./scripts/validation/validate-design-docs.sh
  - Calls run_template_validator() function which executes the Python validator
  - Used for validating design documentation compliance

  3. Python Wrapper Scripts

  validate-generation.py

  python3 scripts/validation/validate-generation.py --workflow my_workflow
  python3 scripts/validation/validate-generation.py --all
  - Dynamically imports the validator module using importlib.util
  - Calls PocketFlowValidator().validate_directory()
  - Adds additional code quality checks (ruff, type checking)

  4. Framework Installation Process

  Setup Scripts (setup/base.sh, setup/project.sh)

  - Copy the validator to end-user projects during installation
  - Create .claude/agents/template-validator.md agent configuration
  - Enable the template-validator agent for end-user projects

  5. Agent-Based Activation

  Template-Validator Agent (.claude/agents/template-validator.md)

  - Proactively invoked after template generation
  - Agent description: "MUST BE USED PROACTIVELY for validating generated
  PocketFlow templates"
  - Integration point for Claude Code to automatically validate templates

  6. Integration Testing Scripts

  Multiple validation scripts reference and check for the template validator:
  - validate-integration.sh - Checks agent integration
  - validate-sub-agents.sh - Validates agent configuration
  - validate-orchestration.sh - Tests orchestration workflows
  - validate-end-to-end.sh - Full system validation

  Key Activation Patterns

  Framework Development (this repo):
  - Direct CLI calls for testing generated templates
  - Integration with shell validation scripts
  - Part of comprehensive validation suites

  End-User Projects:
  - Installed via setup scripts as .claude/agents/template-validator.md
  - Automatically invoked by Claude Code after template generation
  - Available for manual validation of generated workflows

  The validator serves as the canonical source of truth - all other validation
  scripts delegate core validation logic to it while adding their own specific
  checks (structure, quality, integration).