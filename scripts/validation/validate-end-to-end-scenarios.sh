#!/bin/bash
# End-to-End Universal PocketFlow Scenarios Validation (Task 5.1)
# Validates that the framework generates PocketFlow structure for ALL project types
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

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
POCKETFLOW_TOOLS_DIR="$PROJECT_ROOT/framework-tools"

main() {
    log_info "End-to-End Universal PocketFlow Scenarios Validation"
    log_info "==================================================="
    echo
    
    # Check prerequisites
    if ! check_prerequisites; then
        log_error "Prerequisites check failed"
        return 1
    fi
    
    # Navigate to the framework-tools directory
    cd "$POCKETFLOW_TOOLS_DIR" || {
        log_error "Could not access framework-tools directory: $POCKETFLOW_TOOLS_DIR"
        return 1
    }
    
    log_info "Running end-to-end test scenarios..."
    log_info "These tests validate universal PocketFlow integration for all project types."
    echo
    
    # Run the Python test scenarios with no cleanup for validation
    if python3 run_end_to_end_tests.py --no-cleanup; then
        log_success "All end-to-end test scenarios passed"
        echo
        log_success "✅ Universal PocketFlow integration validated successfully"
        log_success "✅ Framework generates PocketFlow structure for all project types"
        log_success "✅ CRUD applications → WORKFLOW pattern"
        log_success "✅ API services → TOOL pattern"
        log_success "✅ Data processing → MAPREDUCE pattern"
        log_success "✅ Complex workflows → AGENT pattern"
        log_success "✅ Search systems → RAG pattern"
        echo
        log_info "Task 5.1 (Create Test Scenarios) validation complete!"
        return 0
    else
        log_error "End-to-end test scenarios failed"
        echo
        log_error "❌ Universal PocketFlow integration has issues"
        log_error "❌ Review the test output above for specific failures"
        log_info "💡 Common issues:"
        echo "   - Pattern recognition not working correctly"
        echo "   - Template generation not producing PocketFlow structure"
        echo "   - Framework vs usage distinction not maintained"
        echo "   - Missing required files in generated templates"
        return 1
    fi
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python 3 availability
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        return 1
    fi
    
    # Check that we're in the framework repository
    if [[ ! -f "$PROJECT_ROOT/CLAUDE.md" ]]; then
        log_error "This script must be run from the Agent OS + PocketFlow framework repository"
        return 1
    fi
    
    # Check required test files exist
    local required_files=(
        "$POCKETFLOW_TOOLS_DIR/end_to_end_test_scenarios.py"
        "$POCKETFLOW_TOOLS_DIR/run_end_to_end_tests.py"
        "$POCKETFLOW_TOOLS_DIR/pattern_analyzer.py"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Required test file missing: $file"
            return 1
        fi
    done
    
    # Check that PocketFlow tools CLI is available
    if [[ -d "$PROJECT_ROOT/pocketflow_tools" ]] && uv run python -m pocketflow_tools.cli --help >/dev/null 2>&1; then
        log_info "Using pocketflow_tools package CLI"
    else
        log_error "pocketflow_tools CLI not found"
        return 1
    fi
    
    log_success "Prerequisites check passed"
    return 0
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi