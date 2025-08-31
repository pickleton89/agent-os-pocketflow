#!/bin/bash
# Master Test Runner - Runs all validation tests in sequence
# This script orchestrates the complete validation of Agent OS + PocketFlow integration
set -e

# Repo type detection
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/lib/repo-detect.sh" ]]; then
  # shellcheck disable=SC1091
  source "${SCRIPT_DIR}/lib/repo-detect.sh"
fi

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

# Configuration
VERBOSE=false
STOP_ON_ERROR=true
QUICK_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--continue)
            STOP_ON_ERROR=false
            shift
            ;;
        -q|--quick)
            QUICK_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose       Show detailed output from each test"
            echo "  -c, --continue      Continue running tests even if one fails"
            echo "  -q, --quick         Run only essential tests (faster)"
            echo "  -h, --help          Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Test suite configuration
declare -a TEST_SUITES=(
    "Configuration:scripts/validation/validate-configuration.sh:Framework configuration validation"
    "Integration:scripts/validation/validate-integration.sh:Core integration validation"
    "Design:scripts/validation/validate-design.sh:Design document validation" 
    "PocketFlow:scripts/validation/validate-pocketflow.sh:PocketFlow setup validation"
    "Sub-Agents:scripts/validation/validate-sub-agents.sh:Sub-agent implementation validation"
    "Orchestration:scripts/validation/validate-orchestration.sh:Orchestration system validation"
    "End-to-End:scripts/validation/validate-end-to-end.sh:Complete end-to-end testing"
)

# Quick mode test suites (essential only)
declare -a QUICK_SUITES=(
    "Configuration:scripts/validation/validate-configuration.sh:Framework configuration validation"
    "Integration:scripts/validation/validate-integration.sh:Core integration validation"
    "PocketFlow:scripts/validation/validate-pocketflow.sh:PocketFlow setup validation"
    "Sub-Agents:scripts/validation/validate-sub-agents.sh:Sub-agent implementation validation"
    "Orchestration:scripts/validation/validate-orchestration.sh:Orchestration system validation"
)

# Framework-focused suites (skip project-only checks entirely)
declare -a FRAMEWORK_SUITES=(
    "Configuration:scripts/validation/validate-configuration.sh:Framework configuration validation"
    "Integration:scripts/validation/validate-integration.sh:Framework sanity checks + skip project-only"
)

declare -a FRAMEWORK_QUICK_SUITES=(
    "Configuration:scripts/validation/validate-configuration.sh:Framework configuration validation"
    "Integration:scripts/validation/validate-integration.sh:Framework sanity checks + skip project-only"
)

# Test results tracking
SUITES_RUN=0
SUITES_PASSED=0
SUITES_FAILED=0
declare -a FAILED_SUITES=()

# Function to run a test suite
run_test_suite() {
    local suite_name="$1"
    local script_path="$2"
    local description="$3"
    
    SUITES_RUN=$((SUITES_RUN + 1))
    
    log_info "Running $suite_name Test Suite"
    log_info "Description: $description"
    log_info "Script: $script_path"
    echo "----------------------------------------"
    
    # Check if script exists and is executable
    if [[ ! -f "$script_path" ]]; then
        log_error "Test script not found: $script_path"
        SUITES_FAILED=$((SUITES_FAILED + 1))
        FAILED_SUITES+=("$suite_name (Script not found)")
        return 1
    fi
    
    if [[ ! -x "$script_path" ]]; then
        log_error "Test script not executable: $script_path"
        chmod +x "$script_path" 2>/dev/null || {
            SUITES_FAILED=$((SUITES_FAILED + 1))
            FAILED_SUITES+=("$suite_name (Not executable)")
            return 1
        }
        log_warning "Made script executable: $script_path"
    fi
    
    # Run the test suite
    local start_time
    start_time=$(date +%s)
    
    if [[ "$VERBOSE" == true ]]; then
        if "$script_path"; then
            local end_time
            end_time=$(date +%s)
            local duration=$((end_time - start_time))
            log_success "$suite_name Test Suite PASSED (${duration}s)"
            SUITES_PASSED=$((SUITES_PASSED + 1))
        else
            local end_time
            end_time=$(date +%s)
            local duration=$((end_time - start_time))
            log_error "$suite_name Test Suite FAILED (${duration}s)"
            SUITES_FAILED=$((SUITES_FAILED + 1))
            FAILED_SUITES+=("$suite_name")
            return 1
        fi
    else
        if "$script_path" > /dev/null 2>&1; then
            local end_time
            end_time=$(date +%s)
            local duration=$((end_time - start_time))
            log_success "$suite_name Test Suite PASSED (${duration}s)"
            SUITES_PASSED=$((SUITES_PASSED + 1))
        else
            local end_time
            end_time=$(date +%s)
            local duration=$((end_time - start_time))
            log_error "$suite_name Test Suite FAILED (${duration}s)"
            SUITES_FAILED=$((SUITES_FAILED + 1))
            FAILED_SUITES+=("$suite_name")
            
            # Show error details in non-verbose mode
            log_info "Running $suite_name again with verbose output to show errors:"
            "$script_path" || true
            
            return 1
        fi
    fi
    
    echo
    return 0
}

# Function to display final results
display_results() {
    echo
    log_info "Test Suite Execution Summary"
    log_info "============================"
    echo "Total Suites Run: $SUITES_RUN"
    echo "Suites Passed: $SUITES_PASSED"
    echo "Suites Failed: $SUITES_FAILED"
    
    if [[ $SUITES_FAILED -gt 0 ]]; then
        echo
        log_error "Failed Test Suites:"
        for failed_suite in "${FAILED_SUITES[@]}"; do
            echo "  - $failed_suite"
        done
    fi
    
    echo
    if [[ $SUITES_FAILED -eq 0 ]]; then
        log_success "🎉 ALL TEST SUITES PASSED!"
        log_success "Agent OS + PocketFlow integration is fully validated and ready for use."
        
        # Display next steps
        echo
        log_info "Next Steps:"
        echo "1. Test the orchestrator: 'Think about building a simple feature'"
        echo "2. Create your first orchestrated spec with the /create-spec command"
        echo "3. Execute tasks with the /execute-tasks command"
        echo
        log_info "The system is now ready for production use!"
        
    else
        log_error "❌ $SUITES_FAILED test suite(s) failed."
        log_error "Please review and fix the issues above before proceeding."
        
        # Suggest specific next steps based on failures
        echo
        log_info "Troubleshooting suggestions:"
        echo "1. Run individual test suites with -v flag for detailed output"
        echo "2. Check that all prerequisites are installed"
        echo "3. Ensure you're running from the project root directory"
        echo "4. Review the setup.sh script output for any errors"
    fi
}

# Function to make all scripts executable
ensure_scripts_executable() {
    local scripts=(
        "scripts/validation/validate-configuration.sh"
        "scripts/validation/validate-integration.sh"
        "scripts/validation/validate-design.sh"
        "scripts/validation/validate-pocketflow.sh"
        "scripts/validation/validate-sub-agents.sh"
        "scripts/validation/validate-orchestration.sh"
        "scripts/validation/validate-end-to-end.sh"
        "scripts/validate-integration.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]] && [[ ! -x "$script" ]]; then
            chmod +x "$script"
            log_info "Made executable: $script"
        fi
    done
}

# Main function
main() {
    log_info "Agent OS + PocketFlow Integration - Master Test Runner"
    log_info "====================================================="
    log_info "Mode: $([ "$QUICK_MODE" == true ] && echo "Quick" || echo "Full")"
    if type print_repo_type >/dev/null 2>&1; then
        print_repo_type
    fi
    log_info "Verbose: $VERBOSE"
    log_info "Stop on Error: $STOP_ON_ERROR"
    echo
    
    # Ensure all scripts are executable
    ensure_scripts_executable
    
    # Select test suites based on mode and repo type
    local test_suites
    local rt=""
    if type detect_repo_type >/dev/null 2>&1; then
        rt="$(detect_repo_type)"
    fi
    if [[ "$QUICK_MODE" == true ]]; then
        if [[ "$rt" == "framework" ]]; then
            test_suites=("${FRAMEWORK_QUICK_SUITES[@]}")
            log_info "Running quick framework test suite"
        else
            test_suites=("${QUICK_SUITES[@]}")
            log_info "Running quick project test suite (essential tests only)"
        fi
    else
        if [[ "$rt" == "framework" ]]; then
            test_suites=("${FRAMEWORK_SUITES[@]}")
            log_info "Running full framework test suite"
        else
            test_suites=("${TEST_SUITES[@]}")
            log_info "Running full project test suite (all tests)"
        fi
    fi
    
    echo
    
    # Run each test suite
    for suite_config in "${test_suites[@]}"; do
        IFS=':' read -r suite_name script_path description <<< "$suite_config"
        
        if ! run_test_suite "$suite_name" "$script_path" "$description"; then
            if [[ "$STOP_ON_ERROR" == true ]]; then
                log_error "Stopping execution due to test failure"
                display_results
                exit 1
            fi
        fi
    done
    
    # Display final results
    display_results
    
    # Exit with appropriate code
    if [[ $SUITES_FAILED -eq 0 ]]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
