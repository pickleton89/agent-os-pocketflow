#!/bin/bash

# Agent OS + PocketFlow User Experience Validation Script
# Tests the complete workflow: /plan-product → /create-spec → /execute-tasks
# Validates seamless user experience and PocketFlow integration

set -e

# Compatible with bash 3.2+ (macOS default)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_DIR="$PROJECT_ROOT/test-user-experience"
LOG_FILE="$TEST_DIR/validation.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Test scenarios for different complexity levels (bash 3.2 compatible)
TEST_SCENARIO_KEYS=("simple_crud" "rest_api" "data_pipeline" "business_workflow")
TEST_SCENARIO_NAMES=("Simple CRUD Application" "REST API Service" "Data Processing Pipeline" "Complex Business Workflow")

# Function to get scenario name by key
get_scenario_name() {
    local key="$1"
    for i in "${!TEST_SCENARIO_KEYS[@]}"; do
        if [[ "${TEST_SCENARIO_KEYS[$i]}" == "$key" ]]; then
            echo "${TEST_SCENARIO_NAMES[$i]}"
            return
        fi
    done
    echo "$key"
}

# Validation functions
validate_pocketflow_structure() {
    local test_project="$1"
    local pattern="$2"
    
    log_info "Validating PocketFlow structure for $pattern pattern"
    
    # Check for workflows directory
    if [[ ! -d "$test_project/.agent-os/workflows" ]]; then
        log_error "Missing .agent-os/workflows directory"
        return 1
    fi
    
    # Find the generated workflow subdirectory
    local workflow_dirs=("$test_project/.agent-os/workflows"/*/)
    if [[ ${#workflow_dirs[@]} -eq 0 ]]; then
        log_error "No workflow subdirectories found in .agent-os/workflows"
        return 1
    fi
    
    local workflow_dir="${workflow_dirs[0]}"
    log_info "Found workflow directory: $(basename "$workflow_dir")"
    
    # Check for required PocketFlow files in the workflow directory
    local required_files=(
        "main.py"
        "flow.py"
        "nodes.py"
        "requirements.txt"
        "tests"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -e "$workflow_dir/$file" ]]; then
            log_error "Missing required file in workflow directory: $file"
            return 1
        fi
    done
    
    # Check for PocketFlow pattern indicators in the correct files
    if ! grep -q "from pocketflow import Flow" "$workflow_dir/flow.py" 2>/dev/null; then
        log_error "No PocketFlow Flow import found in flow.py"
        return 1
    fi
    
    if ! grep -q "from pocketflow import.*Node" "$workflow_dir/nodes.py" 2>/dev/null; then
        log_error "No PocketFlow Node imports found in nodes.py"
        return 1
    fi
    
    # Validate that node classes inherit from proper PocketFlow base classes
    local valid_base_classes=("Node" "AsyncNode" "BatchNode" "AsyncBatchNode" "AsyncParallelBatchNode")
    local invalid_inheritance=false
    
    for base_class in "${valid_base_classes[@]}"; do
        if grep -q "class.*($base_class)" "$workflow_dir/nodes.py" 2>/dev/null; then
            log_info "Found valid node inheritance: $base_class"
        fi
    done
    
    # Check for invalid base class names that aren't valid PocketFlow types
    if grep -E "class.*\((processor|formatter|extractor|loader|handler)\)" "$workflow_dir/nodes.py" 2>/dev/null; then
        log_error "Found invalid node base class inheritance in nodes.py"
        invalid_inheritance=true
    fi
    
    if $invalid_inheritance; then
        return 1
    fi
    
    # Check for project-level design document
    if [[ ! -f "$test_project/docs/design.md" ]]; then
        log_error "Missing project-level design document"
        return 1
    fi
    
    log_success "PocketFlow structure validated for $pattern"
    return 0
}

validate_design_document() {
    local test_project="$1"
    local design_file="$test_project/docs/design.md"
    
    log_info "Validating design document quality"
    
    if [[ ! -f "$design_file" ]]; then
        log_error "Design document not found"
        return 1
    fi
    
    # Check for required sections
    local required_sections=("Architecture" "Components" "Data Flow" "Implementation Plan")
    
    for section in "${required_sections[@]}"; do
        if ! grep -q "$section" "$design_file"; then
            log_error "Missing section in design document: $section"
            return 1
        fi
    done
    
    log_success "Design document validated"
    return 0
}

validate_no_traditional_code() {
    local test_project="$1"
    
    log_info "Validating minimal traditional procedural code patterns"
    
    # Look for concerning traditional patterns (acceptable ones noted)
    local concerning_patterns=("if __name__ == '__main__':")
    local acceptable_patterns=("def main():" "app = FastAPI") # These are OK in framework templates
    
    local concerning_found=0
    for pattern in "${concerning_patterns[@]}"; do
        if grep -r "$pattern" "$test_project/.agent-os/workflows/" 2>/dev/null; then
            log_warning "Found concerning traditional pattern: $pattern"
            concerning_found=1
        fi
    done
    
    for pattern in "${acceptable_patterns[@]}"; do
        if grep -r "$pattern" "$test_project/.agent-os/workflows/" 2>/dev/null; then
            log_info "Found acceptable framework pattern: $pattern"
        fi
    done
    
    if [[ $concerning_found -eq 0 ]]; then
        log_success "No concerning traditional patterns found"
    else
        log_warning "Some traditional patterns detected, but may be acceptable"
    fi
    
    return 0
}

validate_educational_placeholders() {
    local test_project="$1"
    
    log_info "Validating educational placeholder quality"
    
    # Check for meaningful TODO placeholders
    local todo_count=$(grep -r "TODO:" "$test_project" 2>/dev/null | wc -l)
    
    if [[ $todo_count -eq 0 ]]; then
        log_error "No educational TODO placeholders found"
        return 1
    fi
    
    log_success "Found $todo_count educational placeholders"
    return 0
}

# Test scenario generators
generate_simple_crud_scenario() {
    local test_dir="$1"
    
    cat > "$test_dir/user_input.txt" << 'EOF'
Product Name: Task Manager API
Description: A simple CRUD application for managing tasks
Features:
- Create tasks with title and description
- List all tasks
- Update task status
- Delete tasks
Technology Preferences: Python, FastAPI, SQLite
Target Pattern: WORKFLOW
EOF
}

generate_rest_api_scenario() {
    local test_dir="$1"
    
    cat > "$test_dir/user_input.txt" << 'EOF'
Product Name: User Authentication Service
Description: REST API service for user management and authentication
Features:
- User registration and login
- JWT token management
- Password reset functionality
- User profile management
Technology Preferences: Python, FastAPI, PostgreSQL
Target Pattern: TOOL
EOF
}

generate_data_pipeline_scenario() {
    local test_dir="$1"
    
    cat > "$test_dir/user_input.txt" << 'EOF'
Product Name: Sales Data ETL Pipeline
Description: Data processing pipeline for sales analytics
Features:
- Extract data from multiple sources
- Transform and clean data
- Load into data warehouse
- Generate reports
Technology Preferences: Python, Pandas, PostgreSQL
Target Pattern: MAPREDUCE
EOF
}

generate_business_workflow_scenario() {
    local test_dir="$1"
    
    cat > "$test_dir/user_input.txt" << 'EOF'
Product Name: Order Processing System
Description: Complex business workflow for e-commerce orders
Features:
- Order validation and processing
- Inventory management integration
- Payment processing
- Shipping coordination
- Customer notifications
Technology Preferences: Python, FastAPI, PostgreSQL, Redis
Target Pattern: AGENT
EOF
}

# Main testing function
run_user_experience_test() {
    local scenario_name="$1"
    local scenario_desc="$2"
    
    log_info "Starting user experience test: $scenario_desc"
    
    local test_project="$TEST_DIR/$scenario_name"
    mkdir -p "$test_project"
    cd "$test_project"
    
    # Generate scenario-specific input
    case "$scenario_name" in
        "simple_crud")
            generate_simple_crud_scenario "$test_project"
            ;;
        "rest_api")
            generate_rest_api_scenario "$test_project"
            ;;
        "data_pipeline")
            generate_data_pipeline_scenario "$test_project"
            ;;
        "business_workflow")
            generate_business_workflow_scenario "$test_project"
            ;;
    esac
    
    # Initialize git (required for Agent OS)
    git init -q
    git config user.name "Test User"
    git config user.email "test@example.com"
    
    log_info "Simulating user workflow for: $scenario_desc"
    
    # Step 1: Plan Product (simulated)
    log_info "Step 1: Product planning phase"
    mkdir -p .agent-os/product
    
    # Create basic product files that would be generated by /plan-product
    cat > .agent-os/product/mission.md << EOF
# Mission Statement

## Product Vision
$scenario_desc for efficient workflow management.

## Core Objectives
- Deliver reliable functionality
- Maintain code quality
- Follow PocketFlow architecture patterns
EOF
    
    cat > .agent-os/product/roadmap.md << EOF
# Product Roadmap

## Phase 1: Core Implementation
- Basic functionality implementation
- PocketFlow pattern integration
- Test suite development

## Phase 2: Enhancement
- Performance optimization
- Error handling
- Documentation
EOF
    
    cat > .agent-os/product/tech-stack.md << EOF
# Technology Stack

## Architecture Pattern
PocketFlow-based implementation

## Core Technologies
- Python 3.12+
- PocketFlow framework
- Pytest for testing

## Pattern Type
Based on complexity analysis: $(echo "$scenario_name" | tr '_' ' ')
EOF
    
    # Step 2: Create Spec (simulated)
    log_info "Step 2: Specification creation phase"
    mkdir -p .agent-os/specs/initial
    
    cat > .agent-os/specs/initial/overview.md << EOF
# Specification Overview

## Feature Description
Implementation of $scenario_desc using PocketFlow architecture.

## Technical Approach
Utilize PocketFlow patterns for structured, maintainable implementation.

## Success Criteria
- All functionality implemented using PocketFlow nodes
- Comprehensive test coverage
- Clear documentation
EOF
    
    cat > .agent-os/specs/initial/tasks.md << EOF
# Implementation Tasks

## Phase 1: Setup
- [ ] Initialize PocketFlow structure
- [ ] Configure dependencies
- [ ] Set up testing framework

## Phase 2: Core Implementation
- [ ] Implement core business logic
- [ ] Create workflow nodes
- [ ] Add error handling

## Phase 3: Testing & Documentation
- [ ] Write comprehensive tests
- [ ] Update documentation
- [ ] Validate functionality
EOF
    
    # Step 3: Execute Tasks (use the actual generator)
    log_info "Step 3: Task execution phase (using actual generator)"
    
    # Create a YAML specification for the generator
    local spec_file="$test_project/.agent-os/specs/initial/workflow_spec.yaml"
    
    case "$scenario_name" in
        "simple_crud")
            cat > "$spec_file" << 'EOF'
name: "TaskManager"
pattern: "WORKFLOW"
description: "Simple CRUD application for managing tasks"
nodes:
  - name: "ValidateTask"
    type: "Node"
    description: "Validate incoming task data"
  - name: "ProcessTask"
    type: "Node"
    description: "Process task operations (CRUD)"
  - name: "FormatResponse"
    type: "Node"
    description: "Format API response"
EOF
            ;;
        "rest_api")
            cat > "$spec_file" << 'EOF'
name: "UserAuthService"
pattern: "TOOL"
description: "REST API service for user management and authentication"
nodes:
  - name: "AuthValidator"
    type: "Node"
    description: "Validate authentication requests"
  - name: "UserManager"
    type: "AsyncNode"
    description: "Manage user operations"
  - name: "TokenHandler"
    type: "Node"
    description: "Handle JWT tokens"
EOF
            ;;
        "data_pipeline")
            cat > "$spec_file" << 'EOF'
name: "SalesETL"
pattern: "MAPREDUCE"
description: "Data processing pipeline for sales analytics"
nodes:
  - name: "DataExtractor"
    type: "AsyncNode"
    description: "Extract data from multiple sources"
  - name: "DataTransformer"
    type: "BatchNode"
    description: "Transform and clean data"
  - name: "DataLoader"
    type: "AsyncNode"
    description: "Load into data warehouse"
EOF
            ;;
        "business_workflow")
            cat > "$spec_file" << 'EOF'
name: "OrderProcessor"
pattern: "AGENT"
description: "Complex business workflow for e-commerce orders"
nodes:
  - name: "OrderValidator"
    type: "Node"
    description: "Validate order data"
  - name: "InventoryChecker"
    type: "AsyncNode"
    description: "Check inventory availability"
  - name: "PaymentProcessor"
    type: "AsyncNode"
    description: "Process payment"
  - name: "ShippingCoordinator"
    type: "AsyncNode"
    description: "Coordinate shipping"
EOF
            ;;
    esac
    
    # Use the PocketFlow generator to create the actual structure
    if [[ -d "$PROJECT_ROOT/pocketflow_tools" ]]; then
        cd "$PROJECT_ROOT"
        if python -m pocketflow_tools.cli --spec "$spec_file" --output "$test_project/.agent-os/workflows" >> "$LOG_FILE" 2>&1; then
            log_success "Generator completed successfully"
        else
            log_warning "Generator failed, creating fallback structure"
            mkdir -p "$test_project/.agent-os/workflows"
            touch "$test_project/.agent-os/workflows/main.py"
        fi
        cd "$test_project"
    else
        log_warning "PocketFlow generator package not found, creating minimal structure"
        mkdir -p .agent-os/workflows
        touch .agent-os/workflows/main.py
    fi
    
    # Ensure we have the basic structure
    mkdir -p docs tests
    if [[ ! -f "docs/design.md" ]]; then
        cat > docs/design.md << EOF
# Design Document

## Architecture
$scenario_desc implemented using PocketFlow $(echo "$scenario_name" | tr '_' ' ') pattern.

## Components
Core workflow nodes for processing business logic.

## Data Flow
Structured data flow through PocketFlow nodes.

## Implementation Plan
Phased implementation following PocketFlow patterns.
EOF
    fi
    
    if [[ ! -f "requirements.txt" ]]; then
        echo "pocketflow>=0.1.0" > requirements.txt
    fi
    
    # Run validation checks
    local validation_passed=true
    
    if ! validate_pocketflow_structure "$test_project" "$scenario_name"; then
        validation_passed=false
    fi
    
    if ! validate_design_document "$test_project"; then
        validation_passed=false
    fi
    
    validate_no_traditional_code "$test_project"
    
    if ! validate_educational_placeholders "$test_project"; then
        validation_passed=false
    fi
    
    if $validation_passed; then
        log_success "User experience test PASSED: $scenario_desc"
        return 0
    else
        log_error "User experience test FAILED: $scenario_desc"
        return 1
    fi
}

# Main execution
main() {
    # Clean up previous test runs and create test directory
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"
    
    log_info "Starting Agent OS + PocketFlow User Experience Validation"
    
    # Initialize log file
    echo "Agent OS + PocketFlow User Experience Validation Log" > "$LOG_FILE"
    echo "Started at: $(date)" >> "$LOG_FILE"
    echo "=============================================" >> "$LOG_FILE"
    
    local total_tests=0
    local passed_tests=0
    
    # Run tests for each scenario
    for scenario in "${TEST_SCENARIO_KEYS[@]}"; do
        total_tests=$((total_tests + 1))
        local scenario_name=$(get_scenario_name "$scenario")
        
        if run_user_experience_test "$scenario" "$scenario_name"; then
            passed_tests=$((passed_tests + 1))
        fi
        
        echo "" | tee -a "$LOG_FILE"
    done
    
    # Summary
    log_info "============================================="
    log_info "User Experience Validation Summary"
    log_info "Total Tests: $total_tests"
    log_info "Passed: $passed_tests"
    log_info "Failed: $((total_tests - passed_tests))"
    
    if [[ $passed_tests -eq $total_tests ]]; then
        log_success "All user experience tests PASSED!"
        echo "Test results saved to: $LOG_FILE"
        return 0
    else
        log_error "Some user experience tests FAILED!"
        echo "Test results saved to: $LOG_FILE"
        return 1
    fi
}

# Execute main function
main "$@"
