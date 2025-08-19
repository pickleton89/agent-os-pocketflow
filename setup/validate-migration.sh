#!/bin/bash
# Enhanced Agent OS + PocketFlow Migration Validation Script
# Validates successful migration and installation integrity

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_VERSION="1.0.0"
EXPECTED_VERSION="1.4.0"
DEFAULT_INSTALL_PATH="$HOME/.agent-os"

# Validation options
INSTALL_PATH="$DEFAULT_INSTALL_PATH"
VERBOSE=false
CHECK_PROJECTS=false
FIX_ISSUES=false
OUTPUT_FORMAT="human"  # human, json, summary

# Test categories
TEST_CATEGORIES=("structure" "permissions" "configuration" "integration" "functionality")

# Global validation result variables
declare -A TEST_RESULTS
declare -A TEST_DETAILS
declare -A ISSUES_FOUND

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_highlight() { echo -e "${PURPLE}🎯 $1${NC}"; }
log_step() { echo -e "${CYAN}📋 $1${NC}"; }
log_debug() { [[ $VERBOSE == true ]] && echo -e "${CYAN}🔍 $1${NC}"; }

# Display header
show_header() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║           Agent OS Migration Validation Tool                ║
║           Enhanced PocketFlow Edition                       ║
║                                                              ║
║  🔍 Comprehensive Migration and Installation Validation     ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Help message
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
  --install-path PATH     Agent OS installation path (default: $DEFAULT_INSTALL_PATH)
  --check-projects        Also validate project installations
  --fix                   Attempt to fix discovered issues
  --verbose              Enable verbose output
  --format FORMAT         Output format: human, json, summary (default: human)
  
Test Categories:
  --test-structure        Test directory and file structure
  --test-permissions      Test file permissions and executability
  --test-configuration    Test configuration files and settings
  --test-integration      Test PocketFlow and tool integration
  --test-functionality    Test core functionality

Examples:
  $0                                          # Run all validation tests
  $0 --verbose                                # Run with detailed output
  $0 --check-projects                         # Include project validation
  $0 --fix                                    # Fix issues automatically
  $0 --format json > validation-report.json  # Generate JSON report

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install-path)
                INSTALL_PATH="$2"
                shift 2
                ;;
            --check-projects)
                CHECK_PROJECTS=true
                shift
                ;;
            --fix)
                FIX_ISSUES=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            --test-*)
                # Enable specific test category
                category=$(echo "$1" | sed 's/--test-//')
                if [[ " ${TEST_CATEGORIES[*]} " =~ " $category " ]]; then
                    SELECTED_TESTS+=("$category")
                else
                    log_error "Unknown test category: $category"
                    exit 1
                fi
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # If no specific tests selected, run all
    if [[ ${#SELECTED_TESTS[@]} -eq 0 ]]; then
        SELECTED_TESTS=("${TEST_CATEGORIES[@]}")
    fi
}

# Initialize validation results
init_results() {
    TOTAL_TESTS=0
    PASSED_TESTS=0
    FAILED_TESTS=0
    WARNING_TESTS=0
    FIXED_ISSUES=0
    
    # Clear the associative arrays
    TEST_RESULTS=()
    TEST_DETAILS=()
    ISSUES_FOUND=()
}

# Record test result
record_test() {
    local test_name="$1"
    local status="$2"  # pass, fail, warning
    local detail="$3"
    
    ((TOTAL_TESTS++))
    TEST_RESULTS["$test_name"]="$status"
    TEST_DETAILS["$test_name"]="$detail"
    
    case "$status" in
        pass)
            ((PASSED_TESTS++))
            [[ $OUTPUT_FORMAT == "human" ]] && log_success "$test_name"
            ;;
        fail)
            ((FAILED_TESTS++))
            [[ $OUTPUT_FORMAT == "human" ]] && log_error "$test_name: $detail"
            ISSUES_FOUND["$test_name"]="$detail"
            ;;
        warning)
            ((WARNING_TESTS++))
            [[ $OUTPUT_FORMAT == "human" ]] && log_warning "$test_name: $detail"
            ;;
    esac
    
    log_debug "Test: $test_name | Status: $status | Detail: $detail"
}

# Fix issue if possible
attempt_fix() {
    local issue_type="$1"
    local issue_detail="$2"
    local fix_command="$3"
    
    if [[ $FIX_ISSUES != true ]]; then
        return 1
    fi
    
    log_info "Attempting to fix: $issue_type"
    log_debug "Fix command: $fix_command"
    
    if eval "$fix_command"; then
        log_success "Fixed: $issue_type"
        ((FIXED_ISSUES++))
        return 0
    else
        log_error "Failed to fix: $issue_type"
        return 1
    fi
}

# Test 1: Directory and file structure
test_structure() {
    if [[ ! " ${SELECTED_TESTS[*]} " =~ " structure " ]]; then
        return 0
    fi
    
    log_step "Testing directory and file structure..."
    
    # Check main installation directory
    if [[ ! -d "$INSTALL_PATH" ]]; then
        record_test "installation_directory_exists" "fail" "Installation directory not found: $INSTALL_PATH"
        return 1
    fi
    record_test "installation_directory_exists" "pass" ""
    
    # Check required directories
    local required_dirs=(
        "instructions"
        "standards"
        "commands"
        "setup"
        "claude-code/agents"
    )
    
    for dir in "${required_dirs[@]}"; do
        local full_path="$INSTALL_PATH/$dir"
        if [[ ! -d "$full_path" ]]; then
            record_test "directory_$dir" "fail" "Required directory missing: $dir"
            attempt_fix "create_directory_$dir" "Missing directory: $dir" "mkdir -p '$full_path'"
        else
            record_test "directory_$dir" "pass" ""
        fi
    done
    
    # Check PocketFlow integration if enabled
    if [[ -f "$INSTALL_PATH/config.yml" ]]; then
        local pocketflow_enabled=$(grep "pocketflow:" "$INSTALL_PATH/config.yml" | grep -i "true" || echo "")
        if [[ -n "$pocketflow_enabled" ]]; then
            if [[ ! -d "$INSTALL_PATH/pocketflow-tools" ]]; then
                record_test "pocketflow_tools_directory" "fail" "PocketFlow tools directory missing"
            else
                record_test "pocketflow_tools_directory" "pass" ""
            fi
        fi
    fi
    
    # Check required files
    local required_files=(
        "config.yml"
        "setup/base.sh"
        "setup/project.sh"
    )
    
    for file in "${required_files[@]}"; do
        local full_path="$INSTALL_PATH/$file"
        if [[ ! -f "$full_path" ]]; then
            record_test "file_$file" "fail" "Required file missing: $file"
        else
            record_test "file_$file" "pass" ""
        fi
    done
    
    return 0
}

# Test 2: File permissions and executability
test_permissions() {
    if [[ ! " ${SELECTED_TESTS[*]} " =~ " permissions " ]]; then
        return 0
    fi
    
    log_step "Testing file permissions..."
    
    # Check executable scripts
    local executable_scripts=(
        "setup/base.sh"
        "setup/project.sh"
        "setup/migrate.sh"
        "setup/backup-restore.sh"
        "setup/validate-migration.sh"
    )
    
    for script in "${executable_scripts[@]}"; do
        local full_path="$INSTALL_PATH/$script"
        if [[ -f "$full_path" ]]; then
            if [[ -x "$full_path" ]]; then
                record_test "executable_$script" "pass" ""
            else
                record_test "executable_$script" "fail" "Script not executable: $script"
                attempt_fix "make_executable_$script" "Make script executable" "chmod +x '$full_path'"
            fi
        fi
    done
    
    # Check directory permissions
    local important_dirs=(
        "instructions"
        "standards"
        "commands"
        "setup"
    )
    
    for dir in "${important_dirs[@]}"; do
        local full_path="$INSTALL_PATH/$dir"
        if [[ -d "$full_path" ]]; then
            if [[ -r "$full_path" && -w "$full_path" ]]; then
                record_test "permissions_$dir" "pass" ""
            else
                record_test "permissions_$dir" "fail" "Directory permissions issue: $dir"
                attempt_fix "fix_permissions_$dir" "Fix directory permissions" "chmod 755 '$full_path'"
            fi
        fi
    done
    
    return 0
}

# Test 3: Configuration files and settings
test_configuration() {
    if [[ ! " ${SELECTED_TESTS[*]} " =~ " configuration " ]]; then
        return 0
    fi
    
    log_step "Testing configuration files..."
    
    # Check config.yml
    local config_file="$INSTALL_PATH/config.yml"
    if [[ ! -f "$config_file" ]]; then
        record_test "config_file_exists" "fail" "Configuration file missing"
        return 1
    fi
    record_test "config_file_exists" "pass" ""
    
    # Validate config.yml structure
    local required_config_keys=("version" "installation")
    for key in "${required_config_keys[@]}"; do
        if grep -q "^$key:" "$config_file"; then
            record_test "config_key_$key" "pass" ""
        else
            record_test "config_key_$key" "fail" "Configuration key missing: $key"
        fi
    done
    
    # Check version compatibility
    local installed_version=$(grep "version:" "$config_file" | cut -d' ' -f2 | tr -d '"')
    if [[ "$installed_version" == "$EXPECTED_VERSION" ]]; then
        record_test "version_compatibility" "pass" ""
    else
        record_test "version_compatibility" "warning" "Version mismatch. Expected: $EXPECTED_VERSION, Found: $installed_version"
    fi
    
    # Check instruction files
    local instruction_files=("core" "enhanced")
    for file in "${instruction_files[@]}"; do
        local instruction_path="$INSTALL_PATH/instructions/$file"
        if [[ -f "$instruction_path" ]]; then
            record_test "instruction_file_$file" "pass" ""
        else
            record_test "instruction_file_$file" "warning" "Instruction file missing: $file"
        fi
    done
    
    return 0
}

# Test 4: PocketFlow and tool integration
test_integration() {
    if [[ ! " ${SELECTED_TESTS[*]} " =~ " integration " ]]; then
        return 0
    fi
    
    log_step "Testing integration components..."
    
    # Check PocketFlow tools
    local pocketflow_dir="$INSTALL_PATH/pocketflow-tools"
    if [[ -d "$pocketflow_dir" ]]; then
        record_test "pocketflow_integration" "pass" ""
        
        # Check for key PocketFlow components
        local pocketflow_components=("generator.py" "patterns" "templates")
        for component in "${pocketflow_components[@]}"; do
            if [[ -e "$pocketflow_dir/$component" ]]; then
                record_test "pocketflow_component_$component" "pass" ""
            else
                record_test "pocketflow_component_$component" "warning" "PocketFlow component missing: $component"
            fi
        done
    else
        record_test "pocketflow_integration" "warning" "PocketFlow tools not installed"
    fi
    
    # Check Claude Code agent configurations
    local agents_dir="$INSTALL_PATH/claude-code/agents"
    if [[ -d "$agents_dir" ]]; then
        record_test "claude_code_agents" "pass" ""
        
        # Check for standard agents
        local agent_files=("pocketflow-orchestrator.md" "context-fetcher.md")
        for agent in "${agent_files[@]}"; do
            if [[ -f "$agents_dir/$agent" ]]; then
                record_test "agent_$agent" "pass" ""
            else
                record_test "agent_$agent" "warning" "Agent configuration missing: $agent"
            fi
        done
    else
        record_test "claude_code_agents" "warning" "Claude Code agents directory missing"
    fi
    
    return 0
}

# Test 5: Core functionality
test_functionality() {
    if [[ ! " ${SELECTED_TESTS[*]} " =~ " functionality " ]]; then
        return 0
    fi
    
    log_step "Testing core functionality..."
    
    # Test setup scripts syntax
    local scripts=("setup/base.sh" "setup/project.sh")
    for script in "${scripts[@]}"; do
        local script_path="$INSTALL_PATH/$script"
        if [[ -f "$script_path" ]]; then
            if bash -n "$script_path" 2>/dev/null; then
                record_test "syntax_$script" "pass" ""
            else
                record_test "syntax_$script" "fail" "Script has syntax errors: $script"
            fi
        fi
    done
    
    # Test that critical functions are defined in scripts
    local base_script="$INSTALL_PATH/setup/base.sh"
    if [[ -f "$base_script" ]]; then
        local required_functions=("show_header" "install_instructions" "install_pocketflow_tools")
        for func in "${required_functions[@]}"; do
            if grep -q "^${func}()" "$base_script"; then
                record_test "function_$func" "pass" ""
            else
                record_test "function_$func" "warning" "Function not found in base.sh: $func"
            fi
        done
    fi
    
    # Test project script functionality
    local project_script="$INSTALL_PATH/setup/project.sh"
    if [[ -f "$project_script" ]]; then
        # Test dry-run capability
        if "$project_script" --help >/dev/null 2>&1; then
            record_test "project_script_help" "pass" ""
        else
            record_test "project_script_help" "warning" "Project script help not accessible"
        fi
    fi
    
    return 0
}

# Test project installations
test_project_installations() {
    if [[ $CHECK_PROJECTS != true ]]; then
        return 0
    fi
    
    log_step "Testing project installations..."
    
    local project_count=0
    local search_paths=("$HOME/projects" "$HOME/dev" "$HOME/work" "$HOME/code" "$HOME/src")
    
    for search_path in "${search_paths[@]}"; do
        if [[ -d "$search_path" ]]; then
            find "$search_path" -name ".agent-os" -type d 2>/dev/null | while read -r project_agent_os; do
                local project_path=$(dirname "$project_agent_os")
                local project_name=$(basename "$project_path")
                
                log_debug "Found project installation: $project_name at $project_path"
                ((project_count++))
                
                # Check project structure
                if [[ -f "$project_agent_os/config.yml" ]]; then
                    record_test "project_config_$project_name" "pass" ""
                else
                    record_test "project_config_$project_name" "warning" "Project config missing: $project_name"
                fi
                
                # Check CLAUDE.md
                if [[ -f "$project_path/CLAUDE.md" ]]; then
                    record_test "project_claude_md_$project_name" "pass" ""
                else
                    record_test "project_claude_md_$project_name" "warning" "CLAUDE.md missing: $project_name"
                fi
            done
        fi
    done
    
    if [[ $project_count -eq 0 ]]; then
        record_test "project_installations_found" "warning" "No project installations found"
    else
        record_test "project_installations_found" "pass" "Found $project_count project installation(s)"
    fi
    
    return 0
}

# Generate validation report
generate_report() {
    case "$OUTPUT_FORMAT" in
        json)
            generate_json_report
            ;;
        summary)
            generate_summary_report
            ;;
        human)
            generate_human_report
            ;;
        *)
            log_error "Unknown output format: $OUTPUT_FORMAT"
            exit 1
            ;;
    esac
}

# Generate JSON report
generate_json_report() {
    cat << EOF
{
  "validation_info": {
    "timestamp": "$(date -Iseconds)",
    "script_version": "$SCRIPT_VERSION",
    "install_path": "$INSTALL_PATH",
    "expected_version": "$EXPECTED_VERSION"
  },
  "summary": {
    "total_tests": $TOTAL_TESTS,
    "passed": $PASSED_TESTS,
    "failed": $FAILED_TESTS,
    "warnings": $WARNING_TESTS,
    "fixed_issues": $FIXED_ISSUES,
    "success_rate": $(( TOTAL_TESTS > 0 ? PASSED_TESTS * 100 / TOTAL_TESTS : 0 ))
  },
  "test_results": {
EOF
    
    local first=true
    for test_name in "${!TEST_RESULTS[@]}"; do
        [[ $first == false ]] && echo ","
        first=false
        echo -n "    \"$test_name\": {"
        echo -n "\"status\": \"${TEST_RESULTS[$test_name]}\""
        if [[ -n "${TEST_DETAILS[$test_name]}" ]]; then
            echo -n ", \"detail\": \"${TEST_DETAILS[$test_name]}\""
        fi
        echo -n "}"
    done
    
    echo ""
    echo "  },"
    
    # Issues found
    echo "  \"issues\": {"
    first=true
    for issue_name in "${!ISSUES_FOUND[@]}"; do
        [[ $first == false ]] && echo ","
        first=false
        echo -n "    \"$issue_name\": \"${ISSUES_FOUND[$issue_name]}\""
    done
    echo ""
    echo "  }"
    echo "}"
}

# Generate summary report
generate_summary_report() {
    local success_rate=$(( TOTAL_TESTS > 0 ? PASSED_TESTS * 100 / TOTAL_TESTS : 0 ))
    
    cat << EOF
AGENT OS MIGRATION VALIDATION SUMMARY
=====================================
Timestamp: $(date)
Installation: $INSTALL_PATH
Expected Version: $EXPECTED_VERSION

Test Results:
  Total Tests: $TOTAL_TESTS
  Passed: $PASSED_TESTS
  Failed: $FAILED_TESTS
  Warnings: $WARNING_TESTS
  Success Rate: $success_rate%

Fixed Issues: $FIXED_ISSUES

EOF

    if [[ $FAILED_TESTS -gt 0 ]]; then
        echo "FAILED TESTS:"
        echo "============="
        for test_name in "${!TEST_RESULTS[@]}"; do
            if [[ "${TEST_RESULTS[$test_name]}" == "fail" ]]; then
                echo "- $test_name: ${TEST_DETAILS[$test_name]}"
            fi
        done
        echo
    fi
    
    if [[ $WARNING_TESTS -gt 0 ]]; then
        echo "WARNINGS:"
        echo "========="
        for test_name in "${!TEST_RESULTS[@]}"; do
            if [[ "${TEST_RESULTS[$test_name]}" == "warning" ]]; then
                echo "- $test_name: ${TEST_DETAILS[$test_name]}"
            fi
        done
        echo
    fi
}

# Generate human-readable report
generate_human_report() {
    echo
    log_highlight "Validation Summary"
    echo
    
    local success_rate=$(( TOTAL_TESTS > 0 ? PASSED_TESTS * 100 / TOTAL_TESTS : 0 ))
    
    log_info "Total Tests: $TOTAL_TESTS"
    log_success "Passed: $PASSED_TESTS"
    [[ $FAILED_TESTS -gt 0 ]] && log_error "Failed: $FAILED_TESTS"
    [[ $WARNING_TESTS -gt 0 ]] && log_warning "Warnings: $WARNING_TESTS"
    log_info "Success Rate: $success_rate%"
    
    if [[ $FIXED_ISSUES -gt 0 ]]; then
        log_success "Fixed Issues: $FIXED_ISSUES"
    fi
    
    echo
    
    if [[ $FAILED_TESTS -eq 0 ]]; then
        log_success "🎉 Migration validation completed successfully!"
        if [[ $WARNING_TESTS -gt 0 ]]; then
            log_warning "Some warnings were found but don't prevent normal operation"
        fi
    else
        log_error "❌ Migration validation failed"
        log_info "Review the failed tests above and consider running with --fix to auto-resolve issues"
    fi
    
    echo
    log_info "Installation Path: $INSTALL_PATH"
    log_info "Expected Version: $EXPECTED_VERSION"
    echo
}

# Main validation function
main() {
    show_header
    parse_args "$@"
    init_results
    
    log_step "Starting validation of: $INSTALL_PATH"
    
    # Run selected test categories
    for category in "${SELECTED_TESTS[@]}"; do
        case "$category" in
            structure)
                test_structure
                ;;
            permissions)
                test_permissions
                ;;
            configuration)
                test_configuration
                ;;
            integration)
                test_integration
                ;;
            functionality)
                test_functionality
                ;;
            *)
                log_error "Unknown test category: $category"
                ;;
        esac
    done
    
    # Test project installations if requested
    test_project_installations
    
    # Generate report
    generate_report
    
    # Return appropriate exit code
    if [[ $FAILED_TESTS -eq 0 ]]; then
        exit 0
    else
        exit 1
    fi
}

# Initialize arrays
declare -a SELECTED_TESTS

# Run main function with all arguments
main "$@"