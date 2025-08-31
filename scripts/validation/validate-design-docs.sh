#!/bin/bash

# ========================================
# Design Documentation Smoke Validation Script
# ========================================
# Validates that generated PocketFlow projects include proper design documentation
# with required structure and content.
#
# Part of Agent OS + PocketFlow Framework
# Last Updated: 2025-01-31
# ========================================

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VALIDATION_LOG="$PROJECT_ROOT/validation-design-docs.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$VALIDATION_LOG"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1" | tee -a "$VALIDATION_LOG"; }
log_warning() { echo -e "${YELLOW}[⚠]${NC} $1" | tee -a "$VALIDATION_LOG"; }
log_error() { echo -e "${RED}[✗]${NC} $1" | tee -a "$VALIDATION_LOG"; }

# Initialize log
echo "========================================" > "$VALIDATION_LOG"
echo "Design Documentation Validation" >> "$VALIDATION_LOG"
echo "$(date)" >> "$VALIDATION_LOG"
echo "========================================" >> "$VALIDATION_LOG"

# Function to validate a single project's design doc
validate_design_doc() {
    local project_dir="$1"
    local project_name="$(basename "$project_dir")"
    local design_doc="$project_dir/docs/design.md"
    local errors=0
    
    log_info "Validating design documentation for: $project_name"
    
    # Check if design doc exists
    if [[ ! -f "$design_doc" ]]; then
        log_error "Missing design documentation at docs/design.md"
        return 1
    fi
    
    log_success "Design document exists"
    
    # Check for Mermaid diagram
    if ! grep -q '```mermaid' "$design_doc"; then
        log_error "Design document missing Mermaid flow diagram"
        ((errors++))
    else
        log_success "Mermaid diagram found"
    fi
    
    # Check for required sections
    local required_sections=(
        "## Requirements"
        "## Flow Design"
        "## Node Specifications"
    )
    
    for section in "${required_sections[@]}"; do
        if ! grep -q "^$section" "$design_doc"; then
            log_error "Missing required section: $section"
            ((errors++))
        else
            log_success "Found section: $section"
        fi
    done
    
    # Check for workflow components documentation
    if grep -q "### Node:" "$design_doc"; then
        log_success "Node specifications documented"
    else
        log_warning "No detailed node specifications found"
    fi
    
    if grep -q "### Edge:" "$design_doc"; then
        log_success "Edge specifications documented"
    else
        log_warning "No edge specifications found (may not be required)"
    fi
    
    # Check for PocketFlow metadata
    if grep -q "PocketFlow" "$design_doc"; then
        log_success "PocketFlow framework referenced"
    else
        log_warning "No PocketFlow framework reference found"
    fi
    
    return $errors
}

# Function to run template validator
run_template_validator() {
    local project_dir="$1"
    local validator_script="$PROJECT_ROOT/pocketflow-tools/template_validator.py"
    
    if [[ ! -f "$validator_script" ]]; then
        log_warning "Template validator not found at $validator_script"
        return 1
    fi
    
    log_info "Running template validator..."
    
    # Run the validator and capture output
    if python3 "$validator_script" "$project_dir" >> "$VALIDATION_LOG" 2>&1; then
        log_success "Template validation passed"
        return 0
    else
        log_error "Template validation failed (see log for details)"
        return 1
    fi
}

# Main validation logic
main() {
    local total_errors=0
    local projects_validated=0
    
    echo ""
    log_info "Starting design documentation validation..."
    echo ""
    
    # Check if running in a specific project or searching for test projects
    if [[ -f ".agent-os/config.yml" ]] && [[ -d "docs" ]]; then
        # Running in a project directory
        log_info "Validating current project..."
        if validate_design_doc "."; then
            log_success "Design documentation validation passed"
        else
            ((total_errors++))
        fi
        
        if run_template_validator "."; then
            log_success "Template structure validation passed"
        else
            ((total_errors++))
        fi
        
        ((projects_validated++))
    else
        # Search for test projects
        log_info "Searching for test projects to validate..."
        
        # Look for test-user-experience projects
        if [[ -d "$PROJECT_ROOT/test-user-experience" ]]; then
            for project in "$PROJECT_ROOT/test-user-experience"/*; do
                if [[ -d "$project/.agent-os" ]]; then
                    echo ""
                    echo "----------------------------------------"
                    if validate_design_doc "$project"; then
                        log_success "Design validation passed for $(basename "$project")"
                    else
                        ((total_errors++))
                    fi
                    
                    # Find workflow directories to validate
                    for workflow_dir in "$project/.agent-os/workflows"/*; do
                        if [[ -d "$workflow_dir" ]] && [[ -f "$workflow_dir/flow.py" ]]; then
                            if run_template_validator "$workflow_dir"; then
                                log_success "Template validation passed for $(basename "$workflow_dir")"
                            else
                                ((total_errors++))
                            fi
                        fi
                    done
                    
                    ((projects_validated++))
                fi
            done
        fi
        
        # Look for any project with .agent-os directory
        for project_dir in "$PROJECT_ROOT"/*; do
            if [[ -d "$project_dir/.agent-os" ]] && [[ "$project_dir" != *"test-user-experience"* ]]; then
                echo ""
                echo "----------------------------------------"
                if validate_design_doc "$project_dir"; then
                    log_success "Design validation passed for $(basename "$project_dir")"
                else
                    ((total_errors++))
                fi
                ((projects_validated++))
            fi
        done
    fi
    
    # Summary
    echo ""
    echo "========================================"
    echo "VALIDATION SUMMARY"
    echo "========================================"
    echo "Projects validated: $projects_validated"
    echo "Total errors: $total_errors"
    echo "Log file: $VALIDATION_LOG"
    echo ""
    
    if [[ $total_errors -eq 0 ]]; then
        log_success "All design documentation validations passed!"
        exit 0
    else
        log_error "Design documentation validation failed with $total_errors error(s)"
        echo ""
        echo "To fix these issues:"
        echo "1. Ensure all projects have docs/design.md"
        echo "2. Include Mermaid flow diagrams"
        echo "3. Add all required sections (Requirements, Flow Design, Node Specifications)"
        echo "4. Run the generator with --design-first flag for new projects"
        exit 1
    fi
}

# Run main function
main "$@"