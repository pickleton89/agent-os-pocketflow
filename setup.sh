#!/bin/bash
# Agent OS + PocketFlow Integration Setup
# Version: 2.0.0 - Complete Integration
set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Configuration
SETUP_VERSION="2.0.0"
REQUIRED_PYTHON_VERSION="3.12"

# Main setup function
main() {
    log_info "Starting Agent OS + PocketFlow Integration Setup v${SETUP_VERSION}"
    
    # Phase 1: Prerequisites
    log_info "Phase 1: Checking prerequisites..."
    check_prerequisites
    
    # Phase 2: Directory Structure
    log_info "Phase 2: Creating modular directory structure..."
    create_directory_structure
    
    # Phase 3: Core Files
    log_info "Phase 3: Installing core instruction files..."
    install_core_files
    
    # Phase 4: Extensions
    log_info "Phase 4: Installing extension modules..."
    install_extensions
    
    # Phase 5: Orchestration System
    log_info "Phase 5: Setting up orchestration system..."
    setup_orchestration
    
    # Phase 6: Templates
    log_info "Phase 6: Installing template system..."
    install_templates
    
    # Phase 7: Agent Installation
    log_info "Phase 7: Installing PocketFlow Orchestrator agent..."
    install_orchestrator_agent
    
    # Phase 8: Validation
    log_info "Phase 8: Validating installation..."
    validate_installation
    
    # Phase 9: Create validation scripts
    log_info "Phase 9: Creating validation scripts..."
    create_validation_scripts
    
    log_success "Setup completed successfully!"
    display_next_steps
}

check_prerequisites() {
    # Check Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
        if [[ "$(printf '%s\n' "$REQUIRED_PYTHON_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_PYTHON_VERSION" ]]; then
            log_error "Python $REQUIRED_PYTHON_VERSION or higher required. Found: $PYTHON_VERSION"
            exit 1
        fi
        log_success "Python version check passed: $PYTHON_VERSION"
    else
        log_error "Python 3 not found. Please install Python $REQUIRED_PYTHON_VERSION or higher."
        exit 1
    fi
    
    # Check for required tools
    local tools=("git" "curl")
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool not found. Please install $tool."
            exit 1
        fi
    done
    log_success "All required tools found"
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_warning "Not in a git repository. Some features may not work optimally."
    fi
}

create_directory_structure() {
    # Create main directories
    local directories=(
        ".agent-os/instructions/core"
        ".agent-os/instructions/extensions" 
        ".agent-os/instructions/orchestration"
        ".agent-os/workflows"
        ".agent-os/templates"
        ".claude/agents"
        ".claude/commands"
        "scripts/validation"
        "scripts/coordination"
        "docs"
        "src/nodes"
        "src/flows"
        "src/schemas"
        "src/utils"
        "tests/unit"
        "tests/integration"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log_success "Created directory: $dir"
    done
}

install_core_files() {
    # Split existing instruction files into modular components
    if [[ -f "instructions/core/create-spec.md" ]]; then
        log_info "Backing up existing instruction files..."
        mkdir -p .agent-os/backup
        cp -r instructions/core/* .agent-os/backup/ 2>/dev/null || true
    fi
    
    # Move core instruction files to new location
    if [[ -d "instructions/core" ]]; then
        cp -r instructions/core/* .agent-os/instructions/core/
        log_success "Core instruction files installed"
    fi
    
    # Update file references to use modular includes
    update_instruction_file_includes
}

update_instruction_file_includes() {
    local files=(
        ".agent-os/instructions/core/create-spec.md"
        ".agent-os/instructions/core/execute-tasks.md"
        ".agent-os/instructions/core/plan-product.md"
    )
    
    for file in "${files[@]}"; do
        if [[ -f "$file" ]]; then
            # Add orchestration hooks (this would be more sophisticated in practice)
            if ! grep -q "orchestrator-hooks" "$file"; then
                echo -e "\n<!-- Orchestration Integration -->" >> "$file"
                echo "@include orchestration/orchestrator-hooks.md" >> "$file"
                log_success "Added orchestration hooks to $(basename "$file")"
            fi
        fi
    done
}

install_extensions() {
    # Create extension files for modular features
    
    # LLM/AI workflow extension
    cat > .agent-os/instructions/extensions/llm-workflow-extension.md << 'EOF'
# LLM/AI Workflow Extension

## Design Document Requirement (LLM/AI Features Only)
@include orchestration/orchestrator-hooks.md hook="design_document_validation"

**Blocking Condition:** Implementation CANNOT proceed without completed docs/design.md

## PocketFlow Pattern Selection
When LLM/AI components detected:
1. Analyze feature complexity
2. Select appropriate PocketFlow pattern:
   - **Agent**: Dynamic decision making
   - **Workflow**: Sequential processing  
   - **RAG**: Knowledge-enhanced responses
   - **MapReduce**: Large data processing
   - **Multi-Agent**: Collaborative systems

## Code Generation Requirements
Generate complete PocketFlow implementation:
- [ ] Pydantic models for all data structures
- [ ] Node implementations with proper lifecycle
- [ ] Flow assembly with error handling
- [ ] Utility functions with standalone tests
EOF
    
    # Design-first enforcement
    cat > .agent-os/instructions/extensions/design-first-enforcement.md << 'EOF'
# Design-First Enforcement

## Validation Gate: Design Document Required
**Purpose:** Ensure proper design before implementation

### Validation Steps:
1. Check if docs/design.md exists
2. Validate all required sections complete:
   - [ ] Requirements with pattern identification
   - [ ] Flow Design with Mermaid diagram
   - [ ] Utilities with input/output contracts  
   - [ ] Data Design with SharedStore schema
   - [ ] Node Design with prep/exec/post specs

### Enforcement Actions:
- **Missing design.md**: Invoke orchestrator to create
- **Incomplete sections**: Block progression until complete
- **Invalid Mermaid**: Request diagram correction

### Error Handling:
```bash
if [[ ! -f "docs/design.md" ]]; then
    echo "❌ BLOCKED: Implementation requires completed design document"
    echo "Please create docs/design.md using PocketFlow methodology"
    exit 1
fi
```
EOF

    # PocketFlow integration extension
    cat > .agent-os/instructions/extensions/pocketflow-integration.md << 'EOF'
# PocketFlow Integration Extension

## Auto-Detection and Orchestration
This extension automatically detects when PocketFlow patterns are needed and invokes the orchestrator.

### Detection Triggers:
- Complex data processing requirements
- Multi-step workflows
- AI/LLM integration needs
- Async processing patterns

### Integration Points:
1. **Planning Phase**: Identify PocketFlow patterns during product planning
2. **Specification Phase**: Generate PocketFlow-compatible specs
3. **Implementation Phase**: Create actual PocketFlow workflows

### Generated Artifacts:
- `.agent-os/workflows/[feature].py` - Complete PocketFlow implementation
- `src/schemas/[feature]_schema.py` - Pydantic models
- `src/nodes/[feature]_nodes.py` - Node implementations
- `src/flows/[feature]_flow.py` - Flow assembly
EOF
    
    log_success "Extension modules installed"
}

setup_orchestration() {
    # Create coordination configuration
    cat > .agent-os/instructions/orchestration/coordination.yaml << 'EOF'
# Agent OS + PocketFlow Coordination Configuration
coordination_map:
  plan-product:
    triggers_orchestrator: true
    orchestrator_scope: "full_product_planning"
    outputs: [".agent-os/product/", ".agent-os/workflows/"]
    next_files: ["create-spec"]
    
  create-spec:
    depends_on: ["plan-product"]
    checks_for_orchestrator: true
    fallback_to_orchestrator: true
    coordination_points:
      - step_4_5: "design_document_creation"
      - step_12: "task_decomposition"
    outputs: [".agent-os/specs/", ".agent-os/workflows/[feature].py"]
    next_files: ["execute-tasks"]
    
  execute-tasks:
    depends_on: ["create-spec"]
    requires_orchestrator_plan: true
    validation_gates:
      - "orchestrated_workflow_exists"
      - "design_document_complete"
      - "pydantic_models_defined"
    blocks_without: ["workflow_implementation"]

hooks:
  design_document_validation:
    file: "orchestration/orchestrator-hooks.md"
    section: "validate_design_document"
    required_for: ["create-spec", "execute-tasks"]
    
  validate_orchestrated_plan:
    file: "orchestration/orchestrator-hooks.md"
    section: "validate_workflow_implementation"  
    required_for: ["execute-tasks"]
EOF
    
    # Create orchestrator hooks
    cat > .agent-os/instructions/orchestration/orchestrator-hooks.md << 'EOF'
# Orchestration Hooks System

## Hook: design_document_validation
**Purpose:** Ensure design.md exists and is complete
**Usage:** @include orchestration/orchestrator-hooks.md hook="design_document_validation"

### Implementation Logic:
1. Check if docs/design.md exists
2. Validate all required sections complete
3. If incomplete: Invoke orchestrator to complete
4. If missing: Block progression with error

### Error States:
- `design_document_missing`: Invoke orchestrator for creation
- `design_incomplete`: Invoke orchestrator for completion  
- `mermaid_diagram_missing`: Invoke orchestrator for diagram

## Hook: validate_workflow_implementation
**Purpose:** Ensure PocketFlow workflow exists and matches spec
**Usage:** @include orchestration/orchestrator-hooks.md hook="validate_workflow_implementation"

### Implementation Logic:
1. Look for .agent-os/workflows/[feature-name].py
2. Validate workflow structure matches design
3. Check Pydantic models are defined
4. Verify flow connections match Mermaid diagram

## Hook: orchestrator_fallback
**Purpose:** Automatically invoke orchestrator when needed
**Usage:** @include orchestration/orchestrator-hooks.md hook="orchestrator_fallback"

### Implementation Logic:
1. Detect if current task requires orchestration
2. Check if orchestrator outputs exist
3. If missing: Invoke pocketflow-orchestrator with context
4. Wait for completion and validate outputs
EOF

    # Create dependency validation
    cat > .agent-os/instructions/orchestration/dependency-validation.md << 'EOF'
# Dependency Validation System

## Purpose
Ensure all required dependencies and prerequisites are met before proceeding with implementation phases.

## Validation Categories

### 1. Design Document Dependencies
- `docs/design.md` exists and is complete
- Mermaid diagrams are valid
- All required sections present

### 2. PocketFlow Dependencies
- Required Python packages installed
- PocketFlow patterns identified
- Workflow structure defined

### 3. Implementation Dependencies
- Source code structure matches design
- Tests exist for all components
- Documentation is up to date

## Validation Commands
```bash
# Validate design document
./scripts/validation/validate-design.sh

# Validate PocketFlow setup
./scripts/validation/validate-pocketflow.sh

# Validate implementation
./scripts/validation/validate-implementation.sh
```
EOF
    
    log_success "Orchestration system configured"
}

install_templates() {
    # Copy template files (these would be the actual template files)
    local template_files=(
        "pocketflow-templates.md"
        "fastapi-templates.md"  
        "task-templates.md"
    )
    
    for template in "${template_files[@]}"; do
        if [[ -f "templates/$template" ]]; then
            cp "templates/$template" ".agent-os/templates/"
            log_success "Installed template: $template"
        else
            log_warning "Template not found: templates/$template"
            # Create placeholder
            touch ".agent-os/templates/$template"
            echo "# $template - To be implemented" > ".agent-os/templates/$template"
        fi
    done
}

install_orchestrator_agent() {
    # Create the PocketFlow Orchestrator agent
    cat > .claude/agents/pocketflow-orchestrator.md << 'EOF'
---
name: pocketflow-orchestrator
description: MUST BE USED PROACTIVELY for planning, designing, and orchestrating complex Agent OS workflows using PocketFlow's graph-based architecture. Automatically invoked for LLM/AI features and complex planning tasks.
tools: [Read, Write, Grep, Glob, Bash, Edit, MultiEdit, TodoWrite, Task]
model: claude-3-5-sonnet-20241022
auto_invoke_triggers:
  - "think about"
  - "plan"
  - "design"
  - "architect" 
  - "implement"
  - "create spec for"
coordination_aware: true
generates_code: true
---

# PocketFlow Strategic Planning & Orchestration Agent

## Purpose
This agent is the central orchestrator for all Agent OS + PocketFlow integration tasks. It handles complex planning, design document creation, and workflow orchestration.

## Responsibilities

### 1. Strategic Planning
- Analyze user requirements and identify PocketFlow patterns
- Create comprehensive project plans
- Generate design documents with proper structure

### 2. Design Document Creation
- Create `docs/design.md` with all required sections
- Generate Mermaid diagrams for workflow visualization
- Define data structures and API contracts

### 3. Workflow Orchestration
- Generate complete PocketFlow implementations
- Create Pydantic models and node structures
- Ensure proper integration with Agent OS patterns

### 4. Quality Assurance
- Validate generated code against specifications
- Ensure test coverage and documentation
- Maintain consistency across all components

## Usage Patterns

### Automatic Invocation
The orchestrator is automatically invoked when:
- User requests planning or design work
- Complex implementation tasks are detected
- LLM/AI features need to be implemented
- Cross-component coordination is required

### Manual Invocation
Use explicitly when:
- Creating new features requiring PocketFlow patterns
- Refactoring existing code to use PocketFlow
- Generating comprehensive documentation

## Integration Points
- Reads from `.agent-os/instructions/orchestration/coordination.yaml`
- Generates files in `.agent-os/workflows/`
- Updates `docs/design.md` and related documentation
- Creates source code in `src/` directory structure
EOF
    
    # Update CLAUDE.md to use orchestrator
    if [[ -f "CLAUDE.md" ]]; then
        if ! grep -q "pocketflow-orchestrator" CLAUDE.md; then
            cat >> CLAUDE.md << 'EOF'

## 🎯 Orchestration Mode Active
This project uses the **PocketFlow Orchestrator** for all planning and implementation tasks.

### Automatic Orchestration
ALWAYS invoke the pocketflow-orchestrator agent when:
- User says: "think", "plan", "design", "architect", "implement"
- Creating any specification or workflow
- Executing complex tasks
- Solving problems requiring multiple steps

### Integration Pattern
1. First: Use pocketflow-orchestrator for planning
2. Then: Generate Agent OS files based on plan
3. Finally: Implement using generated PocketFlow workflows
EOF
            log_success "Updated CLAUDE.md with orchestration directives"
        fi
    else
        log_warning "CLAUDE.md not found. Creating minimal version."
        cat > CLAUDE.md << 'EOF'
# Project Configuration
Uses PocketFlow Orchestrator for planning and implementation.

## 🎯 Orchestration Mode Active
This project uses the **PocketFlow Orchestrator** for all planning and implementation tasks.

### Automatic Orchestration
ALWAYS invoke the pocketflow-orchestrator agent when:
- User says: "think", "plan", "design", "architect", "implement"
- Creating any specification or workflow
- Executing complex tasks
- Solving problems requiring multiple steps

### Integration Pattern
1. First: Use pocketflow-orchestrator for planning
2. Then: Generate Agent OS files based on plan
3. Finally: Implement using generated PocketFlow workflows
EOF
    fi
    
    log_success "PocketFlow Orchestrator agent installed"
}

validate_installation() {
    local validation_passed=true
    
    # Check directory structure
    local required_dirs=(
        ".agent-os/instructions/core"
        ".agent-os/instructions/extensions"
        ".agent-os/instructions/orchestration"
        ".claude/agents"
        "scripts/validation"
        "src/nodes"
        "src/flows"
        "src/schemas"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            log_error "Missing directory: $dir"
            validation_passed=false
        fi
    done
    
    # Check critical files
    local critical_files=(
        ".agent-os/instructions/orchestration/coordination.yaml"
        ".agent-os/instructions/orchestration/orchestrator-hooks.md"
        ".agent-os/instructions/orchestration/dependency-validation.md"
        ".agent-os/instructions/extensions/llm-workflow-extension.md"
        ".agent-os/instructions/extensions/design-first-enforcement.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
        ".claude/agents/pocketflow-orchestrator.md"
    )
    
    for file in "${critical_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Missing critical file: $file"
            validation_passed=false
        fi
    done
    
    # Check CLAUDE.md contains orchestration directives
    if [[ -f "CLAUDE.md" ]] && grep -q "pocketflow-orchestrator" CLAUDE.md; then
        log_success "CLAUDE.md configured for orchestration"
    else
        log_warning "CLAUDE.md may not be properly configured"
    fi
    
    if [[ "$validation_passed" == true ]]; then
        log_success "All validation checks passed"
    else
        log_error "Validation failed. Please check the errors above."
        exit 1
    fi
}

create_validation_scripts() {
    # Create main validation script
    cat > scripts/validation/validate-integration.sh << 'EOF'
#!/bin/bash
# Integration Validation Script
echo "🧪 Testing Agent OS + PocketFlow Integration..."

# Test 1: Directory structure
if [[ -d ".agent-os/instructions/orchestration" ]]; then
    echo "✅ Orchestration directory exists"
else
    echo "❌ Orchestration directory missing"
    exit 1
fi

# Test 2: Orchestrator agent
if [[ -f ".claude/agents/pocketflow-orchestrator.md" ]]; then
    echo "✅ Orchestrator agent found"
else
    echo "❌ Orchestrator agent missing"
    exit 1
fi

# Test 3: Extension modules
local extensions=(
    ".agent-os/instructions/extensions/llm-workflow-extension.md"
    ".agent-os/instructions/extensions/design-first-enforcement.md"
    ".agent-os/instructions/extensions/pocketflow-integration.md"
)

for ext in "${extensions[@]}"; do
    if [[ -f "$ext" ]]; then
        echo "✅ Extension found: $(basename "$ext")"
    else
        echo "❌ Extension missing: $(basename "$ext")"
        exit 1
    fi
done

# Test 4: Coordination configuration
if [[ -f ".agent-os/instructions/orchestration/coordination.yaml" ]]; then
    echo "✅ Coordination configuration found"
else
    echo "❌ Coordination configuration missing"
    exit 1
fi

echo "🎉 All integration tests passed!"
EOF

    # Create design validation script
    cat > scripts/validation/validate-design.sh << 'EOF'
#!/bin/bash
# Design Document Validation Script
echo "📋 Validating design document..."

if [[ ! -f "docs/design.md" ]]; then
    echo "❌ docs/design.md not found"
    exit 1
fi

# Check for required sections
required_sections=(
    "# Requirements"
    "# Flow Design"
    "# Data Design"
    "# Node Design"
    "# Implementation Plan"
)

for section in "${required_sections[@]}"; do
    if grep -q "$section" docs/design.md; then
        echo "✅ Found section: $section"
    else
        echo "❌ Missing section: $section"
        exit 1
    fi
done

echo "🎉 Design document validation passed!"
EOF

    # Create PocketFlow validation script  
    cat > scripts/validation/validate-pocketflow.sh << 'EOF'
#!/bin/bash
# PocketFlow Setup Validation Script
echo "⚙️ Validating PocketFlow setup..."

# Check Python environment
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
else
    echo "❌ Python 3 not found"
    exit 1
fi

# Check for source directories
src_dirs=("src/nodes" "src/flows" "src/schemas" "src/utils")
for dir in "${src_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "✅ Directory found: $dir"
    else
        echo "❌ Directory missing: $dir"
        exit 1
    fi
done

echo "🎉 PocketFlow validation passed!"
EOF

    # Make scripts executable
    chmod +x scripts/validation/validate-integration.sh
    chmod +x scripts/validation/validate-design.sh
    chmod +x scripts/validation/validate-pocketflow.sh
    
    log_success "Validation scripts created"
}

display_next_steps() {
    cat << 'EOF'

🎉 Agent OS + PocketFlow Integration Setup Complete!

📋 Next Steps:
1. Test the orchestrator: "Think about building a simple feature"
2. Create your first orchestrated spec: "/create-spec feature-name"  
3. Execute with orchestration: "/execute-tasks"

📁 Key Files Created:
- .claude/agents/pocketflow-orchestrator.md (Strategic planning agent)
- .agent-os/instructions/orchestration/ (Coordination system)
- .agent-os/templates/ (Complete template system)

🔧 Validation Commands:
- ./scripts/validation/validate-integration.sh (Run full validation)
- ./scripts/validation/validate-design.sh (Test design document)
- ./scripts/validation/validate-pocketflow.sh (Test PocketFlow setup)

📖 Documentation:
- docs/pocketflow-integration-implementation-plan.md (This plan)
- .agent-os/instructions/orchestration/coordination.yaml (Configuration)

⚡ Quick Test:
> Think about planning a new feature
The orchestrator should activate automatically!

EOF
}

# Run main function
main "$@"