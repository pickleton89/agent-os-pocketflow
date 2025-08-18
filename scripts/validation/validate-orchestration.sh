#!/bin/bash
# Orchestration System Validation Script
# Tests the complete orchestration workflow
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

# Test 1: Orchestrator Agent Exists
test_orchestrator_agent_exists() {
    [[ -f ".claude/agents/pocketflow-orchestrator.md" ]] || return 1
    
    # Check required YAML frontmatter
    grep -q "^name: pocketflow-orchestrator" ".claude/agents/pocketflow-orchestrator.md" || return 1
    grep -q "^description:" ".claude/agents/pocketflow-orchestrator.md" || return 1
    grep -q "^tools:" ".claude/agents/pocketflow-orchestrator.md" || return 1
    
    return 0
}

# Test 2: Coordination Configuration Valid
test_coordination_config_valid() {
    [[ -f ".agent-os/instructions/orchestration/coordination.yaml" ]] || return 1
    
    # Check YAML syntax is valid (if pyyaml is available)
    if command -v python3 &> /dev/null; then
        if python3 -c "import yaml" 2>/dev/null; then
            python3 -c "import yaml; yaml.safe_load(open('.agent-os/instructions/orchestration/coordination.yaml'))" 2>/dev/null || return 1
        fi
    fi
    
    # Check required sections
    local required_sections=("coordination_map" "hooks")
    for section in "${required_sections[@]}"; do
        grep -q "$section:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
    done
    
    return 0
}

# Test 3: Hook System Functional
test_hook_system_functional() {
    [[ -f ".agent-os/instructions/orchestration/orchestrator-hooks.md" ]] || return 1
    
    # Check required hooks are defined
    local required_hooks=(
        "design_document_validation"
        "validate_workflow_implementation"
        "orchestrator_fallback"
    )
    
    for hook in "${required_hooks[@]}"; do
        grep -q "## Hook: $hook" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
    done
    
    return 0
}

# Test 4: Extension Modules Loadable
test_extension_modules_loadable() {
    local extensions=(
        ".agent-os/instructions/extensions/llm-workflow-extension.md"
        ".agent-os/instructions/extensions/design-first-enforcement.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
    )
    
    for ext in "${extensions[@]}"; do
        [[ -f "$ext" ]] || return 1
        [[ -s "$ext" ]] || return 1  # Check file is not empty
        
        # Check extension has proper structure
        grep -q "^# " "$ext" || return 1  # Has title
    done
    
    return 0
}

# Test 5: Workflow Directory Structure
test_workflow_directory_structure() {
    [[ -d ".agent-os/workflows" ]] || return 1
    
    # Should be empty initially but directory should exist
    [[ -d ".agent-os/workflows" ]] || return 1
    
    return 0
}

# Test 6: Template System Accessible
test_template_system_accessible() {
    [[ -d "templates" ]] || return 1
    
    local templates=(
        "templates/pocketflow-templates.md"
        "templates/fastapi-templates.md"
        "templates/task-templates.md"
    )
    
    for template in "${templates[@]}"; do
        [[ -f "$template" ]] || return 1
    done
    
    return 0
}

# Test 7: Core Instruction Integration
test_core_instruction_integration() {
    local core_files=(
        ".agent-os/instructions/core/plan-product.md"
        ".agent-os/instructions/core/create-spec.md"
        ".agent-os/instructions/core/execute-tasks.md"
    )
    
    for file in "${core_files[@]}"; do
        if [[ -f "$file" ]]; then
            # Check for orchestration integration markers
            grep -q "@include orchestration/orchestrator-hooks.md\|orchestrator-hooks" "$file" || return 1
        fi
    done
    
    return 0
}

# Test 8: Design Document Validation
test_design_document_validation() {
    # Test the design validation script exists and is executable
    [[ -f "scripts/validation/validate-design.sh" ]] || return 1
    [[ -x "scripts/validation/validate-design.sh" ]] || return 1
    
    return 0
}

# Test 9: PocketFlow Validation
test_pocketflow_validation() {
    # Test the PocketFlow validation script exists and is executable
    [[ -f "scripts/validation/validate-pocketflow.sh" ]] || return 1
    [[ -x "scripts/validation/validate-pocketflow.sh" ]] || return 1
    
    return 0
}

# Test 10: Dependency Validation System
test_dependency_validation_system() {
    [[ -f ".agent-os/instructions/orchestration/dependency-validation.md" ]] || return 1
    
    # Check validation categories are defined
    local categories=(
        "Design Document Dependencies"
        "PocketFlow Dependencies"  
        "Implementation Dependencies"
    )
    
    for category in "${categories[@]}"; do
        grep -q "$category" ".agent-os/instructions/orchestration/dependency-validation.md" || return 1
    done
    
    return 0
}

# Test 11: Source Structure Ready
test_source_structure_ready() {
    local src_dirs=("src/nodes" "src/flows" "src/schemas" "src/utils")
    
    for dir in "${src_dirs[@]}"; do
        [[ -d "$dir" ]] || return 1
    done
    
    return 0
}

# Test 12: Test Structure Ready
test_test_structure_ready() {
    local test_dirs=("tests/unit" "tests/integration")
    
    for dir in "${test_dirs[@]}"; do
        [[ -d "$dir" ]] || return 1
    done
    
    return 0
}

# Test 13: CLAUDE.md Integration
test_claude_md_integration() {
    [[ -f "CLAUDE.md" ]] || return 1
    
    # For framework repository: Check that it properly identifies itself as framework
    grep -q "This IS the Framework" "CLAUDE.md" || return 1
    grep -q "Framework Development Guidelines" "CLAUDE.md" || return 1
    grep -q "pocketflow-orchestrator.*for end-user projects" "CLAUDE.md" || return 1
    
    return 0
}

# Test 14: Scripts Executable
test_scripts_executable() {
    local scripts=(
        "scripts/validation/validate-integration.sh"
        "scripts/validation/validate-design.sh"
        "scripts/validation/validate-pocketflow.sh"
        "scripts/validate-integration.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]]; then
            [[ -x "$script" ]] || return 1
        fi
    done
    
    return 0
}

# Test 15: Full Integration Ready
test_full_integration_ready() {
    # Final comprehensive check that everything is ready
    local critical_files=(
        ".claude/agents/pocketflow-orchestrator.md"
        ".agent-os/instructions/orchestration/coordination.yaml"
        ".agent-os/instructions/orchestration/orchestrator-hooks.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
        "CLAUDE.md"
    )
    
    for file in "${critical_files[@]}"; do
        [[ -f "$file" ]] || return 1
        [[ -s "$file" ]] || return 1
    done
    
    return 0
}

# Main test runner
main() {
    log_info "Starting orchestration system validation"
    log_info "========================================"
    echo
    
    # Run all tests
    run_test "Orchestrator Agent Exists" "test_orchestrator_agent_exists"
    run_test "Coordination Configuration Valid" "test_coordination_config_valid"
    run_test "Hook System Functional" "test_hook_system_functional"
    run_test "Extension Modules Loadable" "test_extension_modules_loadable"
    run_test "Workflow Directory Structure" "test_workflow_directory_structure"
    run_test "Template System Accessible" "test_template_system_accessible"
    run_test "Core Instruction Integration" "test_core_instruction_integration"
    run_test "Design Document Validation" "test_design_document_validation"
    run_test "PocketFlow Validation" "test_pocketflow_validation"
    run_test "Dependency Validation System" "test_dependency_validation_system"
    run_test "Source Structure Ready" "test_source_structure_ready"
    run_test "Test Structure Ready" "test_test_structure_ready"
    run_test "CLAUDE.md Integration" "test_claude_md_integration"
    run_test "Scripts Executable" "test_scripts_executable"
    run_test "Full Integration Ready" "test_full_integration_ready"
    
    echo
    log_info "Orchestration Test Results Summary"
    log_info "=================================="
    echo "Tests Run: $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo
        log_success "🎉 All orchestration tests passed! System is ready for orchestration."
        exit 0
    else
        echo
        log_error "❌ $TESTS_FAILED orchestration test(s) failed. Please fix the issues above."
        exit 1
    fi
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi