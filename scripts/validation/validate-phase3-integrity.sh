#!/bin/bash
# Phase 3 Template Integrity Validation
# Validates specific Phase 3 requirements for generated templates

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Resolve script location and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <template_directory>"
    echo "Example: $0 .agent-os/workflows/my_workflow"
    exit 1
fi

TEMPLATE_DIR="$1"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
    log_error "Template directory not found: $TEMPLATE_DIR"
    exit 1
fi

log_info "Phase 3 Template Integrity Validation"
log_info "Template: $TEMPLATE_DIR"
echo "===================================="

VALIDATION_PASSED=true

# Function to report validation results
report_result() {
    local check_name="$1"
    local status="$2"
    local message="$3"
    
    if [[ "$status" == "PASS" ]]; then
        log_success "$check_name: $message"
    elif [[ "$status" == "WARN" ]]; then
        log_warning "$check_name: $message"
    else
        log_error "$check_name: $message"
        VALIDATION_PASSED=false
    fi
}

# Phase 3 Requirement 1: Assert TODO placeholders exist in nodes.py, flow.py, router.py
check_todo_placeholders() {
    log_info "Checking TODO placeholders in required files"
    
    local required_files=("nodes.py" "flow.py" "router.py")
    local missing_todos=()
    
    for file in "${required_files[@]}"; do
        local file_path="$TEMPLATE_DIR/$file"
        if [[ -f "$file_path" ]]; then
            if grep -q "TODO:" "$file_path"; then
                echo "  ✓ $file contains TODO placeholders"
            else
                missing_todos+=("$file")
            fi
        else
            report_result "TODO Placeholders" "FAIL" "Required file missing: $file"
            return
        fi
    done
    
    if [[ ${#missing_todos[@]} -eq 0 ]]; then
        report_result "TODO Placeholders" "PASS" "All required files contain TODO placeholders"
    else
        report_result "TODO Placeholders" "FAIL" "Files missing TODO placeholders: ${missing_todos[*]}"
    fi
}

# Phase 3 Requirement 2: Assert no unintended vendor SDK imports
check_vendor_imports() {
    log_info "Checking for unintended vendor SDK imports"
    
    # Define unintended vendor SDKs that shouldn't appear in generated templates
    local unintended_sdks=(
        "boto3"           # AWS SDK
        "azure"           # Azure SDK
        "google-cloud"    # Google Cloud SDK
        "salesforce"      # Salesforce SDK
        "stripe"          # Stripe SDK
        "twilio"          # Twilio SDK
        "slack_sdk"       # Slack SDK
        "discord"         # Discord SDK
        "kubernetes"      # K8s client
        "docker"          # Docker SDK
        "terraform"       # Terraform
    )
    
    local found_imports=()
    
    # Check all Python files for unintended imports (precise matching)
    while IFS= read -r -d '' py_file; do
        for sdk in "${unintended_sdks[@]}"; do
            # Match import statements more precisely to avoid false positives
            if grep -E "^[[:space:]]*(import[[:space:]]+${sdk}([[:space:]]*$|[[:space:]]*#|[[:space:]]+as[[:space:]])|from[[:space:]]+${sdk}([[:space:]]*$|[[:space:]]*#|[[:space:]]+import))" "$py_file" >/dev/null 2>&1; then
                found_imports+=("$(basename "$py_file"):$sdk")
            fi
        done
    done < <(find "$TEMPLATE_DIR" -name "*.py" -print0)
    
    if [[ ${#found_imports[@]} -eq 0 ]]; then
        report_result "Vendor SDK Imports" "PASS" "No unintended vendor SDK imports found"
    else
        report_result "Vendor SDK Imports" "FAIL" "Found unintended imports: ${found_imports[*]}"
    fi
}

# Phase 3 Requirement 3: Assert generated file set and relative paths unchanged
check_file_structure() {
    log_info "Checking generated file set and structure"
    
    local required_files=(
        "schemas/models.py"
        "nodes.py"
        "flow.py"
        "main.py"
        "router.py"
    )
    
    local missing_files=()
    local structure_valid=true
    
    for file in "${required_files[@]}"; do
        local file_path="$TEMPLATE_DIR/$file"
        if [[ -f "$file_path" ]]; then
            echo "  ✓ Found $file"
        else
            missing_files+=("$file")
            structure_valid=false
        fi
    done
    
    # Check for additional expected structure
    local expected_dirs=("schemas" "tests" "docs" "utils")
    for dir in "${expected_dirs[@]}"; do
        local dir_path="$TEMPLATE_DIR/$dir"
        if [[ -d "$dir_path" ]]; then
            echo "  ✓ Found directory $dir/"
        else
            log_warning "Directory structure: Missing expected directory: $dir/"
        fi
    done
    
    if $structure_valid; then
        report_result "File Structure" "PASS" "All required files present at expected paths"
    else
        report_result "File Structure" "FAIL" "Missing required files: ${missing_files[*]}"
    fi
}

# Additional Phase 3 checks: Validate file content quality
check_content_quality() {
    log_info "Checking template content quality"
    
    local quality_issues=0
    
    # Check that files are not empty
    local key_files=("nodes.py" "flow.py" "router.py" "schemas/models.py")
    for file in "${key_files[@]}"; do
        local file_path="$TEMPLATE_DIR/$file"
        if [[ -f "$file_path" ]]; then
            local line_count
            line_count=$(wc -l < "$file_path")
            if [[ $line_count -lt 10 ]]; then
                log_warning "Content Quality: $file appears too short ($line_count lines)"
                quality_issues=$((quality_issues + 1))
            fi
        fi
    done
    
    # Check for Python syntax validity
    local syntax_errors=0
    while IFS= read -r -d '' py_file; do
        if ! python3 -m py_compile "$py_file" >/dev/null 2>&1; then
            log_error "Content Quality: Syntax error in $(basename "$py_file")"
            syntax_errors=$((syntax_errors + 1))
        fi
    done < <(find "$TEMPLATE_DIR" -name "*.py" -print0)
    
    if [[ $syntax_errors -eq 0 && $quality_issues -eq 0 ]]; then
        report_result "Content Quality" "PASS" "All template files have valid syntax and adequate content"
    elif [[ $syntax_errors -eq 0 ]]; then
        report_result "Content Quality" "WARN" "$quality_issues quality issues found (but valid syntax)"
    else
        report_result "Content Quality" "FAIL" "$syntax_errors files have syntax errors"
    fi
}

# Check PocketFlow patterns are correctly used
check_pocketflow_patterns() {
    log_info "Checking PocketFlow pattern usage"
    
    local pattern_issues=0
    
    # Check nodes.py for proper Node inheritance
    if [[ -f "$TEMPLATE_DIR/nodes.py" ]]; then
        if grep -E "class.*\(.*Node.*\):" "$TEMPLATE_DIR/nodes.py" >/dev/null 2>&1; then
            echo "  ✓ nodes.py contains proper Node inheritance"
        else
            log_warning "PocketFlow Patterns: nodes.py missing proper Node inheritance"
            pattern_issues=$((pattern_issues + 1))
        fi
    fi
    
    # Check flow.py for proper Flow inheritance
    if [[ -f "$TEMPLATE_DIR/flow.py" ]]; then
        if grep -E "class.*\(.*Flow.*\):" "$TEMPLATE_DIR/flow.py" >/dev/null 2>&1; then
            echo "  ✓ flow.py contains proper Flow inheritance"
        else
            log_warning "PocketFlow Patterns: flow.py missing proper Flow inheritance"
            pattern_issues=$((pattern_issues + 1))
        fi
    fi
    
    if [[ $pattern_issues -eq 0 ]]; then
        report_result "PocketFlow Patterns" "PASS" "Proper PocketFlow patterns detected"
    else
        report_result "PocketFlow Patterns" "WARN" "$pattern_issues pattern issues found"
    fi
}

# Run all Phase 3 validation checks
echo
check_todo_placeholders
echo
check_vendor_imports  
echo
check_file_structure
echo
check_content_quality
echo
check_pocketflow_patterns
echo

# Final validation summary
echo "===================================="
if $VALIDATION_PASSED; then
    log_success "🎉 Phase 3 Template Integrity Validation PASSED"
    log_success "All template integrity requirements met"
    echo
    echo "✅ Template ready for Phase 3 validation suite"
    exit 0
else
    log_error "💥 Phase 3 Template Integrity Validation FAILED"
    log_error "Template does not meet Phase 3 requirements"
    echo
    echo "❌ Please address the issues above before proceeding"
    exit 1
fi