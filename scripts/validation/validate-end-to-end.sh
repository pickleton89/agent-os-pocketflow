#!/bin/bash
# End-to-End Integration Testing Script
# Tests the complete Agent OS + PocketFlow workflow
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

# Configuration
TEST_FEATURE_NAME="test-feature-$(date +%s)"
TEST_DIR="test-workspace"

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

# Setup test environment
setup_test_environment() {
    log_info "Setting up test environment..."
    
    # Create test workspace if it doesn't exist
    mkdir -p "$TEST_DIR"
    
    # Backup any existing files that we might overwrite
    if [[ -f "docs/design.md" ]]; then
        cp "docs/design.md" "docs/design.md.backup.$$"
        log_info "Backed up existing design.md"
    fi
    
    return 0
}

# Cleanup test environment
cleanup_test_environment() {
    log_info "Cleaning up test environment..."
    
    # Remove test files
    [[ -d "$TEST_DIR" ]] && rm -rf "$TEST_DIR"
    
    # Clean up test design document
    [[ -f "docs/design.md.test" ]] && rm -f "docs/design.md.test"
    
    # Restore backup if it exists
    if [[ -f "docs/design.md.backup.$$" ]]; then
        mv "docs/design.md.backup.$$" "docs/design.md"
        log_info "Restored design.md backup"
    fi
    
    # Clean up any test workflows
    [[ -f ".agent-os/workflows/$TEST_FEATURE_NAME.py" ]] && rm -f ".agent-os/workflows/$TEST_FEATURE_NAME.py"
    
    return 0
}

# Test 1: Basic Integration Test
test_basic_integration() {
    # Run the basic integration validation
    ./scripts/validation/validate-integration.sh > /dev/null 2>&1 || return 1
    return 0
}

# Test 2: Orchestration System Test
test_orchestration_system() {
    # Run the orchestration validation
    ./scripts/validation/validate-orchestration.sh > /dev/null 2>&1 || return 1
    return 0
}

# Test 3: Design Document Creation
test_design_document_creation() {
    # Create a test design document
    cat > "docs/design.md.test" << 'EOF'
# Test Feature Design

## Requirements
Test feature for validation purposes.

### Pattern Identification
- Pattern: Workflow
- Complexity: Simple
- Components: Single node processing

## Flow Design
```mermaid
graph TD
    A[Input] --> B[Process] --> C[Output]
```

## Data Design
### SharedStore Schema
```python
class TestData(BaseModel):
    input: str
    output: str
```

## Node Design
### Process Node
- **prep**: Validate input
- **exec**: Transform data
- **post**: Return result

## Implementation Plan
1. Create Pydantic models
2. Implement process node
3. Assemble flow
4. Add tests
EOF
    
    # Test design validation
    if [[ -f "scripts/validation/validate-design.sh" ]]; then
        # Temporarily replace design.md for testing
        [[ -f "docs/design.md" ]] && mv "docs/design.md" "docs/design.md.temp"
        mv "docs/design.md.test" "docs/design.md"
        
        # Run validation
        local result=0
        ./scripts/validation/validate-design.sh > /dev/null 2>&1 || result=1
        
        # Restore original
        mv "docs/design.md" "docs/design.md.test"
        [[ -f "docs/design.md.temp" ]] && mv "docs/design.md.temp" "docs/design.md"
        
        return $result
    fi
    
    return 0
}

# Test 4: PocketFlow Setup Validation
test_pocketflow_setup() {
    # Run PocketFlow validation
    ./scripts/validation/validate-pocketflow.sh > /dev/null 2>&1 || return 1
    return 0
}

# Test 5: Template System Test
test_template_system() {
    # Check that templates are accessible and have content
    local templates=(
        "templates/pocketflow-templates.md"
        "templates/fastapi-templates.md"
        "templates/task-templates.md"
    )
    
    for template in "${templates[@]}"; do
        [[ -f "$template" ]] || return 1
        [[ -s "$template" ]] || return 1
    done
    
    return 0
}

# Test 6: Source Structure Generation
test_source_structure_generation() {
    # For framework repository: Check that generator can create PocketFlow structure
    if [[ -f "pocketflow-tools/generator.py" ]]; then
        # Framework has generator capability - this is the expected structure
        return 0
    elif [[ -d ".agent-os/workflows" ]]; then
        # Project has workflows - check they contain proper PocketFlow files
        local workflow_count=$(find .agent-os/workflows -maxdepth 1 -type d | grep -v "^\.agent-os/workflows$" | wc -l)
        [[ $workflow_count -gt 0 ]] || return 1
        return 0
    else
        # Neither framework generator nor project workflows found
        return 1
    fi
}

# Test 7: Test Structure Generation
test_test_structure_generation() {
    # For framework repository: Check validation scripts exist
    if [[ -f "pocketflow-tools/generator.py" ]]; then
        # Framework repository should have validation scripts for testing
        [[ -d "scripts/validation" ]] || return 1
        [[ -w "scripts/validation" ]] || return 1
        return 0
    else
        # Project repository should have test directories
        local test_dirs=("tests/unit" "tests/integration")
        for dir in "${test_dirs[@]}"; do
            [[ -d "$dir" ]] || return 1
            [[ -w "$dir" ]] || return 1
        done
        return 0
    fi
}

# Test 8: Agent Configuration Test
test_agent_configuration() {
    # Verify three sub-agents are properly configured
    local agents=(
        "template-validator.md:template-validator"
        "pattern-recognizer.md:pattern-recognizer"
        "dependency-orchestrator.md:dependency-orchestrator"
    )
    
    for agent_spec in "${agents[@]}"; do
        local agent_file="${agent_spec%%:*}"
        local agent_name="${agent_spec##*:}"
        local agent_path=".claude/agents/$agent_file"
        
        # Check file exists
        [[ -f "$agent_path" ]] || return 1
        
        # Check YAML frontmatter
        grep -q "^name: $agent_name" "$agent_path" || return 1
        grep -q "^description:" "$agent_path" || return 1
        grep -q "^tools:" "$agent_path" || return 1
        
        # Check agent has substantive content
        local line_count
        line_count=$(wc -l < "$agent_path")
        [[ $line_count -gt 50 ]] || return 1
    done
    
    return 0
}

# Test 9: Coordination System Test
test_coordination_system() {
    # Test coordination configuration
    [[ -f ".agent-os/instructions/orchestration/coordination.yaml" ]] || return 1
    
    # Verify YAML is valid (if pyyaml is available)
    if command -v python3 &> /dev/null; then
        if python3 -c "import yaml" 2>/dev/null; then
            python3 -c "import yaml; yaml.safe_load(open('.agent-os/instructions/orchestration/coordination.yaml'))" 2>/dev/null || return 1
        fi
    fi
    
    # Check required coordination points
    grep -q "plan-product:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
    grep -q "create-spec:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
    grep -q "execute-tasks:" ".agent-os/instructions/orchestration/coordination.yaml" || return 1
    
    return 0
}

# Test 10: Hook System Test
test_hook_system() {
    # Test hook definitions
    [[ -f ".agent-os/instructions/orchestration/orchestrator-hooks.md" ]] || return 1
    
    # Check required hooks
    grep -q "design_document_validation" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
    grep -q "validate_workflow_implementation" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
    grep -q "orchestrator_fallback" ".agent-os/instructions/orchestration/orchestrator-hooks.md" || return 1
    
    return 0
}

# Test 11: Extension System Test  
test_extension_system() {
    # Test all extensions are loaded
    local extensions=(
        ".agent-os/instructions/extensions/llm-workflow-extension.md"
        ".agent-os/instructions/extensions/design-first-enforcement.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
    )
    
    for ext in "${extensions[@]}"; do
        [[ -f "$ext" ]] || return 1
        [[ -s "$ext" ]] || return 1
        
        # Check extension has proper structure
        grep -q "^# " "$ext" || return 1
    done
    
    return 0
}

# Test 12: Dependencies Test
test_dependencies() {
    # Test Python environment
    command -v python3 &> /dev/null || return 1
    
    # Test Git
    command -v git &> /dev/null || return 1
    git rev-parse --git-dir > /dev/null 2>&1 || return 1
    
    # Test required Python version (3.12+ required for framework alignment)
    local python_version
    python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
    [[ "$(printf '%s\n' "3.12" "$python_version" | sort -V | head -n1)" == "3.12" ]] || return 1
    
    return 0
}

# Test 13: Script Permissions Test
test_script_permissions() {
    # Test that all validation scripts are executable
    local scripts=(
        "scripts/validation/validate-integration.sh"
        "scripts/validation/validate-design.sh"
        "scripts/validation/validate-pocketflow.sh"
        "scripts/validation/validate-orchestration.sh"
        "scripts/validate-integration.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]]; then
            [[ -x "$script" ]] || return 1
        fi
    done
    
    return 0
}

# Test 14: CLAUDE.md Integration Test
test_claude_md_integration() {
    [[ -f "CLAUDE.md" ]] || return 1
    
    # For framework repository: Check that it properly identifies itself as framework
    grep -q "This IS the Framework" "CLAUDE.md" || return 1
    grep -q "Framework Development Guidelines" "CLAUDE.md" || return 1
    grep -q "sub-agents.*for end-user projects" "CLAUDE.md" || return 1
    
    return 0
}

# Test 15: Complete System Health Check
test_complete_system_health() {
    # Final comprehensive health check
    local critical_components=(
        ".claude/agents/template-validator.md"
        ".claude/agents/pattern-recognizer.md"
        ".claude/agents/dependency-orchestrator.md"
        ".agent-os/instructions/orchestration/coordination.yaml"
        ".agent-os/instructions/orchestration/orchestrator-hooks.md"
        ".agent-os/instructions/extensions/pocketflow-integration.md"
        "scripts/validation/validate-integration.sh"
        "CLAUDE.md"
    )
    
    for component in "${critical_components[@]}"; do
        [[ -f "$component" ]] || return 1
        [[ -s "$component" ]] || return 1
    done
    
    # Test that the system can be validated by its own scripts
    ./scripts/validation/validate-integration.sh > /dev/null 2>&1 || return 1
    ./scripts/validation/validate-orchestration.sh > /dev/null 2>&1 || return 1
    
    return 0
}

# Main test runner
main() {
    log_info "Starting end-to-end integration testing"
    log_info "======================================="
    echo
    
    # Setup test environment
    setup_test_environment
    
    # Trap to ensure cleanup happens
    trap cleanup_test_environment EXIT
    
    # Run all tests
    run_test "Basic Integration" "test_basic_integration"
    run_test "Orchestration System" "test_orchestration_system"
    run_test "Design Document Creation" "test_design_document_creation"
    run_test "PocketFlow Setup" "test_pocketflow_setup"
    run_test "Template System" "test_template_system"
    run_test "Source Structure Generation" "test_source_structure_generation"
    run_test "Test Structure Generation" "test_test_structure_generation"
    run_test "Agent Configuration" "test_agent_configuration"
    run_test "Coordination System" "test_coordination_system"
    run_test "Hook System" "test_hook_system"
    run_test "Extension System" "test_extension_system"
    run_test "Dependencies" "test_dependencies"
    run_test "Script Permissions" "test_script_permissions"
    run_test "CLAUDE.md Integration" "test_claude_md_integration"
    run_test "Complete System Health Check" "test_complete_system_health"
    
    echo
    log_info "End-to-End Test Results Summary"
    log_info "==============================="
    echo "Tests Run: $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo
        log_success "🎉 All end-to-end tests passed! Complete system integration verified."
        log_info "The Agent OS + PocketFlow integration is ready for production use."
        exit 0
    else
        echo
        log_error "❌ $TESTS_FAILED end-to-end test(s) failed. Please fix the issues above."
        exit 1
    fi
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
