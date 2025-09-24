#!/bin/bash
# Phase 4 Component CI Integration Script
#
# Orchestrates all Phase 4 optimization testing components for CI/CD pipeline
# This is the primary entry point for automated testing of Phase 4 components
#
# Usage:
#   ./scripts/ci/run-phase4-ci-tests.sh [--json] [--cleanup] [--performance] [--reports]

set -e

# Colors and logging
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
JSON_OUTPUT=false
CLEANUP=false
RUN_PERFORMANCE=false
GENERATE_REPORTS=false
VERBOSE=false

# Test results tracking
COMPONENTS_RUN=0
COMPONENTS_PASSED=0
COMPONENTS_FAILED=0
declare -a FAILED_COMPONENTS=()
TEST_START_TIME=$(date +%s)

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --cleanup)
            CLEANUP=true
            shift
            ;;
        --performance)
            RUN_PERFORMANCE=true
            shift
            ;;
        --reports)
            GENERATE_REPORTS=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --all)
            RUN_PERFORMANCE=true
            GENERATE_REPORTS=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Phase 4 Component CI Testing Script"
            echo ""
            echo "Options:"
            echo "  --json              Output results in JSON format"
            echo "  --cleanup           Clean up test artifacts after execution"
            echo "  --performance       Run performance benchmarks"
            echo "  --reports           Generate quality assurance reports"
            echo "  --all               Run all components (equivalent to --performance --reports)"
            echo "  --verbose, -v       Show detailed output"
            echo "  -h, --help          Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  CI                  Set to 'true' to enable CI-specific optimizations"
            echo "  PHASE4_TIMEOUT      Timeout for individual components (default: 300s)"
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

# Environment setup
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
TIMEOUT=${PHASE4_TIMEOUT:-300}

# Create output directory for CI artifacts
mkdir -p "${PROJECT_ROOT}/ci-artifacts"
ARTIFACTS_DIR="${PROJECT_ROOT}/ci-artifacts"

# Function to run a component with timeout and error handling
run_component() {
    local component_name="$1"
    local component_command="$2"
    local component_description="$3"
    local optional="${4:-false}"

    COMPONENTS_RUN=$((COMPONENTS_RUN + 1))

    log_info "Running Phase 4 Component: $component_name"
    log_info "Description: $component_description"

    if [[ "$VERBOSE" == true ]]; then
        log_info "Command: $component_command"
    fi

    echo "----------------------------------------"

    # Create component-specific artifact directory
    local component_artifacts_dir="$ARTIFACTS_DIR/$component_name"
    mkdir -p "$component_artifacts_dir"

    # Run component with timeout
    local start_time=$(date +%s)
    local exit_code=0
    local output_file="$component_artifacts_dir/output.log"

    if timeout "$TIMEOUT" bash -c "$component_command" > "$output_file" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        log_success "$component_name PASSED (${duration}s)"
        COMPONENTS_PASSED=$((COMPONENTS_PASSED + 1))

        # Show last few lines of output for context
        if [[ "$VERBOSE" == true ]]; then
            echo "Last 10 lines of output:"
            tail -10 "$output_file" || true
        fi

        return 0
    else
        exit_code=$?
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        if [[ "$optional" == "true" ]]; then
            log_warning "$component_name FAILED (${duration}s) - Optional component, continuing"
            return 0
        else
            log_error "$component_name FAILED (${duration}s)"
            COMPONENTS_FAILED=$((COMPONENTS_FAILED + 1))
            FAILED_COMPONENTS+=("$component_name")

            # Show error output
            echo "Error output (last 20 lines):"
            tail -20 "$output_file" || true

            return $exit_code
        fi
    fi
}

# Function to check prerequisites
check_prerequisites() {
    log_info "Checking Phase 4 component prerequisites..."

    # Check Python availability
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not available"
        return 1
    fi

    # Check required scripts exist
    local required_scripts=(
        "claude-code/testing/test-phase4-optimization.py"
    )

    for script in "${required_scripts[@]}"; do
        if [[ ! -f "$PROJECT_ROOT/$script" ]]; then
            log_error "Required script not found: $script"
            return 1
        fi
    done

    # Check optional scripts
    if [[ "$RUN_PERFORMANCE" == true ]]; then
        if [[ ! -f "$PROJECT_ROOT/claude-code/testing/performance-benchmarking.py" ]]; then
            log_warning "Performance benchmarking script not found - skipping performance tests"
            RUN_PERFORMANCE=false
        fi
    fi

    if [[ "$GENERATE_REPORTS" == true ]]; then
        if [[ ! -f "$PROJECT_ROOT/scripts/testing/generate-quality-report.py" ]]; then
            log_warning "Quality report generator not found - skipping report generation"
            GENERATE_REPORTS=false
        fi
    fi

    log_success "Prerequisites check completed"
    return 0
}

# Function to run core Phase 4 optimization tests
run_phase4_core_tests() {
    local test_script="$PROJECT_ROOT/claude-code/testing/test-phase4-optimization.py"
    local cmd="cd '$PROJECT_ROOT' && python3 '$test_script'"

    # Add command-line options
    if [[ "$JSON_OUTPUT" == true ]]; then
        cmd="$cmd --json"
    fi

    if [[ "$CLEANUP" == true ]]; then
        cmd="$cmd --cleanup"
    fi

    if [[ "$VERBOSE" == true ]]; then
        cmd="$cmd --verbose"
    fi

    run_component \
        "phase4-optimization-tests" \
        "$cmd" \
        "Core Phase 4 optimization component testing (validation, monitoring, context optimization, error handling)"
}

# Function to run performance benchmarks
run_performance_benchmarks() {
    if [[ "$RUN_PERFORMANCE" == false ]]; then
        return 0
    fi

    local benchmark_script="$PROJECT_ROOT/claude-code/testing/performance-benchmarking.py"
    local output_file="$ARTIFACTS_DIR/performance-benchmarks/results.json"
    local cmd="cd '$PROJECT_ROOT' && python3 '$benchmark_script' --output '$output_file'"

    run_component \
        "performance-benchmarks" \
        "$cmd" \
        "Performance benchmarking for optimization validation (context reduction, parallel processing, memory usage)" \
        "true"  # Optional component
}

# Function to run end-user workflow integration tests
run_workflow_integration_tests() {
    local workflow_script="$PROJECT_ROOT/scripts/validation/validate-end-user-workflows.sh"

    if [[ ! -f "$workflow_script" ]]; then
        log_warning "End-user workflow script not found - skipping workflow integration tests"
        return 0
    fi

    local cmd="cd '$PROJECT_ROOT' && bash '$workflow_script'"

    run_component \
        "end-user-workflow-integration" \
        "$cmd" \
        "End-user workflow integration testing (installation, planning, specification, execution)" \
        "true"  # Optional component
}

# Function to generate quality assurance reports
generate_qa_reports() {
    if [[ "$GENERATE_REPORTS" == false ]]; then
        return 0
    fi

    local report_script="$PROJECT_ROOT/scripts/testing/generate-quality-report.py"
    local cmd="cd '$PROJECT_ROOT' && python3 '$report_script' --output-dir '$ARTIFACTS_DIR/qa-reports' --format both"

    run_component \
        "quality-assurance-reports" \
        "$cmd" \
        "Comprehensive quality assurance report generation" \
        "true"  # Optional component
}

# Function to generate CI summary
generate_ci_summary() {
    local end_time=$(date +%s)
    local total_duration=$((end_time - TEST_START_TIME))
    local success_rate=0

    if [[ $COMPONENTS_RUN -gt 0 ]]; then
        success_rate=$(( (COMPONENTS_PASSED * 100) / COMPONENTS_RUN ))
    fi

    # Create summary data
    local summary_data="{
        \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
        \"total_duration_seconds\": $total_duration,
        \"components_run\": $COMPONENTS_RUN,
        \"components_passed\": $COMPONENTS_PASSED,
        \"components_failed\": $COMPONENTS_FAILED,
        \"success_rate\": $success_rate,
        \"failed_components\": [$(printf '"%s",' "${FAILED_COMPONENTS[@]}" | sed 's/,$//')]
    }"

    # Save summary to artifacts
    echo "$summary_data" > "$ARTIFACTS_DIR/ci-summary.json"

    # Display results
    echo
    log_info "Phase 4 CI Testing Summary"
    log_info "=========================="
    echo "Total Duration: ${total_duration}s"
    echo "Components Run: $COMPONENTS_RUN"
    echo "Components Passed: $COMPONENTS_PASSED"
    echo "Components Failed: $COMPONENTS_FAILED"
    echo "Success Rate: ${success_rate}%"

    if [[ $COMPONENTS_FAILED -gt 0 ]]; then
        echo
        log_error "Failed Components:"
        for failed_component in "${FAILED_COMPONENTS[@]}"; do
            echo "  - $failed_component"
        done
    fi

    echo
    if [[ $COMPONENTS_FAILED -eq 0 ]]; then
        log_success "🎉 ALL PHASE 4 COMPONENTS PASSED!"
        log_success "Phase 4 optimization components are validated and ready for production."
    else
        log_error "❌ $COMPONENTS_FAILED Phase 4 component(s) failed."
        log_error "Please review the failures and fix issues before proceeding."
    fi

    # Output JSON if requested
    if [[ "$JSON_OUTPUT" == true ]]; then
        echo
        echo "=== JSON OUTPUT ==="
        echo "$summary_data"
    fi
}

# Function to cleanup artifacts if requested
cleanup_artifacts() {
    if [[ "$CLEANUP" == true ]]; then
        log_info "Cleaning up CI artifacts..."

        # Keep summary and essential logs, remove temporary files
        find "$ARTIFACTS_DIR" -name "*.tmp" -delete 2>/dev/null || true
        find "$ARTIFACTS_DIR" -name "*.log" -mtime +1 -delete 2>/dev/null || true

        log_info "Cleanup completed"
    fi
}

# Main execution function
main() {
    log_info "Phase 4 Component CI Testing Script"
    log_info "==================================="
    log_info "Project Root: $PROJECT_ROOT"
    log_info "Artifacts Dir: $ARTIFACTS_DIR"
    log_info "JSON Output: $JSON_OUTPUT"
    log_info "Cleanup: $CLEANUP"
    log_info "Performance: $RUN_PERFORMANCE"
    log_info "Reports: $GENERATE_REPORTS"
    echo

    # Check prerequisites
    if ! check_prerequisites; then
        log_error "Prerequisites check failed"
        exit 1
    fi

    # Change to project root
    cd "$PROJECT_ROOT"

    # Run all Phase 4 components
    log_info "Starting Phase 4 component execution..."
    echo

    # Core tests (required)
    run_phase4_core_tests || true

    # Performance benchmarks (optional)
    run_performance_benchmarks || true

    # End-user workflow integration tests (optional)
    run_workflow_integration_tests || true

    # Quality assurance reports (optional)
    generate_qa_reports || true

    # Generate summary
    generate_ci_summary

    # Cleanup if requested
    cleanup_artifacts

    # Exit with appropriate code
    if [[ $COMPONENTS_FAILED -eq 0 ]]; then
        exit 0
    else
        exit 1
    fi
}

# Handle script interruption
trap 'echo; log_error "Script interrupted"; exit 130' INT TERM

# Run main function
main "$@"