#!/bin/bash

# validate-template-structure.sh
# Minimal structural validation wrapper. Delegates core checks to
# pocketflow-tools/template_validator.py (canonical source of truth).
# Last Updated: 2025-08-31

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Validating PocketFlow Template Structure...${NC}"
echo "=============================================="

# Check if we're in the project root
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found${NC}"
    echo "This script must be run from the project root directory."
    echo "Current directory: $(pwd)"
    exit 1
fi

# Track validation results
VALIDATION_PASSED=true

# Function to report validation results
report_result() {
    local check_name="$1"
    local status="$2"
    local message="$3"
    
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ $check_name${NC}: $message"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  $check_name${NC}: $message"
    else
        echo -e "${RED}❌ $check_name${NC}: $message"
        VALIDATION_PASSED=false
    fi
}

# Main validation logic
if [ $# -eq 0 ]; then
    echo "Usage: $0 <template_directory>"
    echo "Example: $0 .agent-os/workflows/my_workflow"
    exit 1
fi

TEMPLATE_DIR="$1"

if [ ! -d "$TEMPLATE_DIR" ]; then
    report_result "Template Directory" "FAIL" "Directory not found: $TEMPLATE_DIR"
    exit 1
fi

echo -e "\n📂 Validating template directory: $TEMPLATE_DIR"

# Check for required template files
echo -e "\n🔍 Validating required template structure..."
REQUIRED_FILES=("nodes.py" "flow.py" "schemas/models.py")
MISSING_FILES=()

for req_file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$TEMPLATE_DIR/$req_file" ]; then
        echo -e "  ✓ Found $req_file"
    else
        MISSING_FILES+=("$req_file")
    fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    report_result "Required Files" "PASS" "All required template files present"
else
    report_result "Required Files" "FAIL" "Missing files: ${MISSING_FILES[*]}"
fi

# Validate flow graph structure if flow.py exists
if [ -f "$TEMPLATE_DIR/flow.py" ]; then
    echo -e "\n🔍 Validating flow graph structure..."
    
    # Check for Flow class inheritance
    if grep -q "class.*Flow.*:" "$TEMPLATE_DIR/flow.py" && \
       grep -q "def __init__" "$TEMPLATE_DIR/flow.py" && \
       grep -q "nodes = {" "$TEMPLATE_DIR/flow.py" && \
       grep -q "edges = {" "$TEMPLATE_DIR/flow.py"; then
        report_result "Flow Structure" "PASS" "Flow class has proper structure"
    else
        report_result "Flow Structure" "FAIL" "Flow class missing required structure"
    fi
fi

# Delegate comprehensive checks to canonical Python validator
echo -e "\n🔍 Running canonical template validation..."
pushd "$(dirname "$0")/../.." > /dev/null
if python3 pocketflow-tools/template_validator.py "$TEMPLATE_DIR" > /dev/null 2>&1; then
    report_result "Canonical Validation" "PASS" "All canonical checks passed"
else
    echo -e "\n📋 Detailed canonical validation results:"
    python3 pocketflow-tools/template_validator.py "$TEMPLATE_DIR"
    report_result "Canonical Validation" "FAIL" "See issues above (source of truth)"
fi
popd > /dev/null

# Final validation summary
echo -e "\n" 
echo "=============================================="
if [ "$VALIDATION_PASSED" = true ]; then
    echo -e "${GREEN}🎉 Template Structure Validation PASSED${NC}"
    echo "All templates have valid structure and follow PocketFlow patterns."
    echo ""
    echo "✅ Templates are ready for user implementation!"
else
    echo -e "${RED}💥 Template Structure Validation FAILED${NC}"
    echo "Some structural issues need to be addressed."
    echo ""
    echo "📚 See .claude/agents/template-validator.md for validation criteria"
fi

echo ""
exit $([ "$VALIDATION_PASSED" = true ] && echo 0 || echo 1)
