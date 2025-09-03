#!/bin/bash
# Determinism validation for PocketFlow generator
# Validates that generator produces consistent, deterministic output
# by comparing against known baseline outputs

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

# Configuration
TEST_OUTPUT_DIR="tmp_determinism_test"
BASELINE_DIR="baseline_out"
PATTERNS=("RAG" "AGENT" "TOOL" "WORKFLOW")

# Enable deterministic mode
export POCKETFLOW_TEST_MODE=1

log_info "Starting determinism validation"
log_info "Test mode enabled: POCKETFLOW_TEST_MODE=$POCKETFLOW_TEST_MODE"

# Clean up any previous test outputs
rm -rf "$TEST_OUTPUT_DIR" || true
mkdir -p "$TEST_OUTPUT_DIR"

# Track validation results
TOTAL_PATTERNS=0
PASSED_PATTERNS=0
declare -a FAILED_PATTERNS=()

# Function to normalize file content for comparison
normalize_content() {
    local file="$1"
    # Remove extra whitespace, normalize line endings, sort if appropriate
    sed -e 's/[[:space:]]*$//' -e '/^[[:space:]]*$/d' "$file" | \
    sed 's/\r$//' | \
    LC_ALL=C sort 2>/dev/null || cat
}

# Function to compute content hash
compute_hash() {
    local file="$1"
    if [[ -f "$file" ]]; then
        normalize_content "$file" | sha256sum | cut -d' ' -f1
    else
        echo "missing_file"
    fi
}

# Function to validate a single pattern
validate_pattern() {
    local pattern="$1"
    local pattern_lower
    pattern_lower=$(echo "$pattern" | tr '[:upper:]' '[:lower:]')
    local test_name="baseline${pattern_lower}workflow"
    
    TOTAL_PATTERNS=$((TOTAL_PATTERNS + 1))
    
    log_info "Validating $pattern pattern determinism"
    
    # Create temporary spec file for this pattern
    local spec_file="$TEST_OUTPUT_DIR/${pattern_lower}-spec.yaml"
    cat > "$spec_file" << EOF
name: "Baseline${pattern}Workflow"
pattern: "$pattern"
description: "Baseline workflow for $pattern pattern determinism testing"
EOF
    
    # Generate workflow using CLI
    local output_dir="$TEST_OUTPUT_DIR/$test_name"
    if ! python3 -m pocketflow_tools.cli --spec "$spec_file" --output "$TEST_OUTPUT_DIR" 2>/dev/null; then
        log_error "$pattern: CLI generation failed"
        FAILED_PATTERNS+=("$pattern (CLI generation failed)")
        return 1
    fi
    
    # Check if baseline exists
    local baseline_dir="$BASELINE_DIR/$test_name"
    if [[ ! -d "$baseline_dir" ]]; then
        log_error "$pattern: Baseline directory not found: $baseline_dir"
        FAILED_PATTERNS+=("$pattern (no baseline)")
        return 1
    fi
    
    # Compare generated files against baseline
    local mismatches=0
    local total_files=0
    
    # Get all files from both baseline and generated output (compatible with BSD/GNU find)
    local all_files
    all_files=$(
        (cd "$baseline_dir" 2>/dev/null && find . -type f | sed 's|^\./||' || true;
         cd "$output_dir" 2>/dev/null && find . -type f | sed 's|^\./||' || true) | \
        sort -u
    )
    
    while IFS= read -r rel_file; do
        [[ -n "$rel_file" ]] || continue
        total_files=$((total_files + 1))
        
        local baseline_file="$baseline_dir/$rel_file"
        local generated_file="$output_dir/$rel_file"
        
        # Compute normalized hashes
        local baseline_hash
        local generated_hash
        baseline_hash=$(compute_hash "$baseline_file")
        generated_hash=$(compute_hash "$generated_file")
        
        if [[ "$baseline_hash" != "$generated_hash" ]]; then
            mismatches=$((mismatches + 1))
            log_warning "$pattern: Hash mismatch in $rel_file"
            
            # Show detailed diff for first few mismatches
            if [[ $mismatches -le 3 ]]; then
                if [[ -f "$baseline_file" && -f "$generated_file" ]]; then
                    echo "    Baseline hash: $baseline_hash"
                    echo "    Generated hash: $generated_hash"
                    echo "    First 5 lines of diff:"
                    diff -u "$baseline_file" "$generated_file" | head -10 || true
                fi
            fi
        fi
    done <<< "$all_files"
    
    if [[ $mismatches -eq 0 ]]; then
        log_success "$pattern: All $total_files files match baseline (deterministic)"
        PASSED_PATTERNS=$((PASSED_PATTERNS + 1))
        return 0
    else
        log_error "$pattern: $mismatches/$total_files files don't match baseline"
        FAILED_PATTERNS+=("$pattern ($mismatches/$total_files mismatches)")
        return 1
    fi
}

# Function to validate required files structure
validate_file_structure() {
    local pattern="$1"
    local output_dir="$2"
    
    local required_files=(
        "schemas/models.py"
        "nodes.py"
        "flow.py"
        "router.py"
    )
    
    for req_file in "${required_files[@]}"; do
        if [[ ! -f "$output_dir/$req_file" ]]; then
            log_error "$pattern: Missing required file: $req_file"
            return 1
        fi
    done
    
    return 0
}

# Function to validate TODO placeholders exist
validate_todo_placeholders() {
    local pattern="$1"
    local output_dir="$2"
    
    local files_to_check=("nodes.py" "flow.py" "router.py")
    local missing_todos=0
    
    for file in "${files_to_check[@]}"; do
        local file_path="$output_dir/$file"
        if [[ -f "$file_path" ]]; then
            if ! grep -q "TODO:" "$file_path"; then
                log_warning "$pattern: No TODO placeholders found in $file"
                missing_todos=$((missing_todos + 1))
            fi
        fi
    done
    
    if [[ $missing_todos -gt 0 ]]; then
        log_warning "$pattern: $missing_todos files missing TODO placeholders"
    fi
}

# Main validation loop
log_info "Validating determinism for ${#PATTERNS[@]} patterns"
echo

for pattern in "${PATTERNS[@]}"; do
    if validate_pattern "$pattern"; then
        # Additional structural checks for passed patterns  
        pattern_lower=$(echo "$pattern" | tr '[:upper:]' '[:lower:]')
        test_name="baseline${pattern_lower}workflow"
        output_dir="$TEST_OUTPUT_DIR/$test_name"
        
        validate_file_structure "$pattern" "$output_dir"
        validate_todo_placeholders "$pattern" "$output_dir"
    fi
    echo
done

# Clean up test outputs
rm -rf "$TEST_OUTPUT_DIR" || true

# Final results
log_info "Determinism Validation Results"
echo "================================"
echo "Total patterns tested: $TOTAL_PATTERNS"
echo "Patterns passed: $PASSED_PATTERNS"
echo "Patterns failed: $((TOTAL_PATTERNS - PASSED_PATTERNS))"

if [[ ${#FAILED_PATTERNS[@]} -gt 0 ]]; then
    echo
    log_error "Failed patterns:"
    for failed in "${FAILED_PATTERNS[@]}"; do
        echo "  - $failed"
    done
fi

echo
if [[ $PASSED_PATTERNS -eq $TOTAL_PATTERNS ]]; then
    log_success "🎉 All patterns are deterministic!"
    log_success "Generator produces consistent, reproducible output."
    exit 0
else
    log_error "❌ Determinism validation failed"
    log_error "Generator output is not consistent with baselines."
    log_error "This indicates non-deterministic behavior in the generator."
    exit 1
fi