#!/bin/bash
# Complete Integration Validation Script
# Tests all aspects of Agent OS + PocketFlow integration
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    log_info "Running test: $test_name"
    
    if eval "$test_command"; then
        log_success "PASSED: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        log_error "FAILED: $test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Test 1: Directory Structure
test_directory_structure() {
    local required_dirs=(
        ".agent-os/instructions/core"
        ".agent-os/instructions/extensions"
        ".agent-os/instructions/orchestration"
        ".agent-os/workflows"
        "templates"
        ".claude/agents"
        "scripts/validation"
        "scripts/coordination"
        "src/nodes"
        "src/flows"
        "src/schemas"
        "src/utils"
        "tests/unit"
        "tests/integration"
    )
    
    for dir in "${required_dirs[@]}"; do
        [[ -d "$dir" ]] || return 1
    done
    return 0
}

# Test 2: Core Files
test_core_files() {
    local required_files=(
        ".agent-os/instructions/orchestration/coordination.yaml"
        ".agent-os/instructions/orchestration/orchestrator-hooks.md"
        ".agent-os/instructions/orchestration/dependency-validation.md"
        ".agent-os/instructions/extensions/llm-workflow-extension.md"
        ".agent-os/instructions/extensions/design-first-enforcement.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
        ".claude/agents/pocketflow-orchestrator.md"
    )
    
    for file in "${required_files[@]}"; do
        [[ -f "$file" ]] || return 1
    done
    return 0
}

# Test 3: Agent Configuration
test_agent_configuration() {
    if [[ -f ".claude/agents/pocketflow-orchestrator.md" ]]; then
        # Check agent has required fields
        grep -q "name: pocketflow-orchestrator" ".claude/agents/pocketflow-orchestrator.md" || return 1
        grep -q "description:" ".claude/agents/pocketflow-orchestrator.md" || return 1
        grep -q "tools:" ".claude/agents/pocketflow-orchestrator.md" || return 1
        return 0
    fi
    return 1
}

# Test 4: Coordination Configuration
test_coordination_config() {
    if [[ -f ".agent-os/instructions/orchestration/coordination.yaml" ]]; then
        # Check required coordination sections
        grep -q "coordination_map:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
        grep -q "plan-product:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
        grep -q "create-spec:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
        grep -q "execute-tasks:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
        grep -q "hooks:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
        return 0
    fi
    return 1
}

# Test 5: Extension Modules
test_extension_modules() {
    local extensions=(
        ".agent-os/instructions/extensions/llm-workflow-extension.md"
        ".agent-os/instructions/extensions/design-first-enforcement.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
    )
    
    for ext in "${extensions[@]}"; do
        [[ -f "$ext" ]] || return 1
        # Check extension has content
        [[ -s "$ext" ]] || return 1
    done
    return 0
}

# Test 6: Orchestrator Hooks
test_orchestrator_hooks() {
    if [[ -f ".agent-os/instructions/orchestration/orchestrator-hooks.md" ]]; then
        # Check required hooks exist
        grep -q "design_document_validation" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
        grep -q "validate_workflow_implementation" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
        grep -q "orchestrator_fallback" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
        return 0
    fi
    return 1
}

# Test 7: Template System
test_template_system() {
    [[ -d ".agent-os/templates" ]] || return 1
    
    local template_files=(
        ".agent-os/templates/pocketflow-templates.md"
        ".agent-os/templates/fastapi-templates.md"
        ".agent-os/templates/task-templates.md"
    )
    
    for template in "${template_files[@]}"; do
        [[ -f "$template" ]] || return 1
    done
    return 0
}

# Test 8: Validation Scripts
test_validation_scripts() {
    local validation_scripts=(
        "scripts/validation/validate-integration.sh"
        "scripts/validation/validate-design.sh"
        "scripts/validation/validate-pocketflow.sh"
    )
    
    for script in "${validation_scripts[@]}"; do
        [[ -f "$script" ]] || return 1
        [[ -x "$script" ]] || return 1
    done
    return 0
}

# Test 9: Python Environment
test_python_environment() {
    command -v python3 &> /dev/null || return 1
    
    # Check Python version (should be 3.12+)
    local python_version
    python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
    
    if [[ "$(printf '%s\n' "3.12" "$python_version" | sort -V | head -n1)" != "3.12" ]]; then
        return 1
    fi
    return 0
}

# Test 10: Git Repository
test_git_repository() {
    git rev-parse --git-dir > /dev/null 2>&1 || return 1
    return 0
}

# Test 11: CLAUDE.md Configuration
test_claude_md_config() {
    if [[ -f "CLAUDE.md" ]]; then
        grep -q "pocketflow-orchestrator" "CLAUDE.md" || return 1
        grep -q "Orchestration Mode Active" "CLAUDE.md" || return 1
        return 0
    fi
    return 1
}

# Test 12: Source Code Structure
test_source_structure() {
    local src_dirs=("src/nodes" "src/flows" "src/schemas" "src/utils")
    for dir in "${src_dirs[@]}"; do
        [[ -d "$dir" ]] || return 1
    done
    return 0
}

# Test 13: Test Structure
test_test_structure() {
    local test_dirs=("tests/unit" "tests/integration")
    for dir in "${test_dirs[@]}"; do
        [[ -d "$dir" ]] || return 1
    done
    return 0
}

# Test 14: Instruction File Integration
test_instruction_integration() {
    local core_files=(
        ".agent-os/instructions/core/plan-product.md"
        ".agent-os/instructions/core/create-spec.md"
        ".agent-os/instructions/core/execute-tasks.md"
    )
    
    for file in "${core_files[@]}"; do
        if [[ -f "$file" ]]; then
            # Check for orchestration integration
            grep -q "orchestrator-hooks" "$file" || return 1
        fi
    done
    return 0
}

# Test 15: Dependency Validation
test_dependency_validation() {
    if [[ -f ".agent-os/instructions/orchestration/dependency-validation.md" ]]; then
        # Check required validation categories
        grep -q "Design Document Dependencies" ".agent-os/instructions/orchestration/dependency-validation.md" || return 1
        grep -q "PocketFlow Dependencies" ".agent-os/instructions/orchestration/dependency-validation.md" || return 1
        grep -q "Implementation Dependencies" ".agent-os/instructions/orchestration/dependency-validation.md" || return 1
        return 0
    fi
    return 1
}

# Main test runner
main() {
    log_info "Starting comprehensive Agent OS + PocketFlow integration validation"
    log_info "================================================================="
    echo
    
    # Run all tests
    run_test "Directory Structure" "test_directory_structure"
    run_test "Core Files" "test_core_files" 
    run_test "Agent Configuration" "test_agent_configuration"
    run_test "Coordination Configuration" "test_coordination_config"
    run_test "Extension Modules" "test_extension_modules"
    run_test "Orchestrator Hooks" "test_orchestrator_hooks"
    run_test "Template System" "test_template_system"
    run_test "Validation Scripts" "test_validation_scripts"
    run_test "Python Environment" "test_python_environment"
    run_test "Git Repository" "test_git_repository"
    run_test "CLAUDE.md Configuration" "test_claude_md_config"
    run_test "Source Code Structure" "test_source_structure"
    run_test "Test Structure" "test_test_structure"
    run_test "Instruction File Integration" "test_instruction_integration"
    run_test "Dependency Validation" "test_dependency_validation"
    
    echo
    log_info "Test Results Summary"
    log_info "==================="
    echo "Tests Run: $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo
        log_success "🎉 All integration tests passed! System is ready for use."
        exit 0
    else
        echo
        log_error "❌ $TESTS_FAILED test(s) failed. Please fix the issues above."
        exit 1
    fi
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi