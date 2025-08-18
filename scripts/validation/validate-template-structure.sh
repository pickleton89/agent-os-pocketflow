#!/bin/bash

# validate-template-structure.sh
# Validates generated PocketFlow templates for structural correctness
# Part of Phase 2 Template Validator implementation
# Last Updated: 2025-01-18

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

# Function to validate Python syntax using AST
validate_python_syntax() {
    local file_path="$1"
    local temp_output=$(mktemp)
    
    # Use Python to parse and validate syntax
    python3 -c "
import ast
import sys

try:
    with open('$file_path', 'r') as f:
        content = f.read()
    
    # Parse the AST to check syntax
    ast.parse(content, filename='$file_path')
    print('SYNTAX_VALID')
    
except SyntaxError as e:
    print(f'SYNTAX_ERROR:{e.lineno}:{e.msg}')
    sys.exit(1)
except Exception as e:
    print(f'PARSE_ERROR:{str(e)}')
    sys.exit(1)
" > "$temp_output" 2>&1
    
    local result=$?
    local output=$(cat "$temp_output")
    rm -f "$temp_output"
    
    if [ $result -eq 0 ] && [[ $output == "SYNTAX_VALID" ]]; then
        return 0
    else
        echo "$output"
        return 1
    fi
}

# Function to check PocketFlow patterns
validate_pocketflow_patterns() {
    local file_path="$1"
    
    python3 -c "
import ast
import sys

class PocketFlowValidator(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.node_classes = []
        
    def visit_ClassDef(self, node):
        # Check for PocketFlow node classes
        base_names = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)
        
        if any(base in ['Node', 'AsyncNode', 'BatchNode'] for base in base_names):
            self.node_classes.append({
                'name': node.name,
                'bases': base_names,
                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            })
        
        self.generic_visit(node)
    
    def validate_node_structure(self):
        for node_class in self.node_classes:
            methods = node_class['methods']
            name = node_class['name']
            
            # Check required methods
            if 'prep' not in methods:
                self.errors.append(f'{name}: Missing required prep() method')
            
            if 'post' not in methods:
                self.errors.append(f'{name}: Missing required post() method')
            
            # Check exec method based on base class
            has_async_base = any(base in ['AsyncNode', 'BatchNode'] for base in node_class['bases'])
            if has_async_base:
                if 'exec_async' not in methods:
                    self.errors.append(f'{name}: Missing required exec_async() method for async node')
            else:
                if 'exec' not in methods:
                    self.errors.append(f'{name}: Missing required exec() method')

try:
    with open('$file_path', 'r') as f:
        content = f.read()
    
    tree = ast.parse(content, filename='$file_path')
    validator = PocketFlowValidator()
    validator.visit(tree)
    validator.validate_node_structure()
    
    if validator.errors:
        for error in validator.errors:
            print(f'PATTERN_ERROR:{error}')
        sys.exit(1)
    else:
        print('PATTERNS_VALID')
        
except Exception as e:
    print(f'VALIDATION_ERROR:{str(e)}')
    sys.exit(1)
"
}

# Function to check for educational placeholder quality
validate_placeholder_quality() {
    local file_path="$1"
    local issues=0
    
    # Check for TODO comments
    if ! grep -q "TODO:" "$file_path" 2>/dev/null; then
        echo "QUALITY_WARN: No TODO comments found - templates should have educational placeholders"
        ((issues++))
    fi
    
    # Check for NotImplementedError
    if ! grep -q "NotImplementedError" "$file_path" 2>/dev/null; then
        echo "QUALITY_WARN: No NotImplementedError found - utility functions should raise this"
        ((issues++))
    fi
    
    # Check for completed implementations (potential framework violation)
    if grep -q "def.*:.*return.*[^NotImplementedError]" "$file_path" 2>/dev/null; then
        if ! grep -q "# TODO:" "$file_path" 2>/dev/null; then
            echo "QUALITY_ERROR: Found completed implementations without TODO markers"
            ((issues++))
        fi
    fi
    
    if [ $issues -eq 0 ]; then
        echo "QUALITY_VALID"
        return 0
    else
        return 1
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

# Find all Python files in the template directory
PYTHON_FILES=$(find "$TEMPLATE_DIR" -name "*.py" -type f)

if [ -z "$PYTHON_FILES" ]; then
    report_result "Python Files" "FAIL" "No Python files found in template directory"
    exit 1
fi

echo -e "\n📋 Found Python files:"
echo "$PYTHON_FILES" | while read -r file; do
    echo "  - $(basename "$file")"
done

# Validate each Python file
echo -e "\n🔍 Validating Python syntax..."
SYNTAX_ERRORS=0
while IFS= read -r file; do
    if validate_python_syntax "$file"; then
        echo -e "  ✓ $(basename "$file")"
    else
        echo -e "  ❌ $(basename "$file")"
        ((SYNTAX_ERRORS++))
    fi
done <<< "$PYTHON_FILES"

if [ $SYNTAX_ERRORS -eq 0 ]; then
    report_result "Python Syntax" "PASS" "All files have valid Python syntax"
else
    report_result "Python Syntax" "FAIL" "$SYNTAX_ERRORS files have syntax errors"
fi

# Validate using Python template validator for consistency
echo -e "\n🔍 Running comprehensive template validation..."
PYTHON_VALIDATOR="$(dirname "$0")/../../.agent-os/workflows/template_validator.py"

if [ -f "$PYTHON_VALIDATOR" ]; then
    cd "$(dirname "$0")/../.."
    if python3 "$PYTHON_VALIDATOR" "$TEMPLATE_DIR" > /dev/null 2>&1; then
        report_result "Template Validation" "PASS" "All templates passed comprehensive validation"
    else
        echo -e "\n📋 Detailed validation results:"
        python3 "$PYTHON_VALIDATOR" "$TEMPLATE_DIR"
        report_result "Template Validation" "WARN" "Some validation issues found (see details above)"
    fi
else
    report_result "Template Validation" "WARN" "Python validator not available, skipping detailed validation"
fi

# Validate placeholder quality
echo -e "\n🔍 Validating placeholder quality..."
QUALITY_ISSUES=0
while IFS= read -r file; do
    if result=$(validate_placeholder_quality "$file"); then
        if [[ $result == "QUALITY_VALID" ]]; then
            echo -e "  ✓ $(basename "$file") - Good placeholder quality"
        fi
    else
        echo -e "  ⚠️  $(basename "$file") - Quality issues detected"
        ((QUALITY_ISSUES++))
    fi
done <<< "$PYTHON_FILES"

if [ $QUALITY_ISSUES -eq 0 ]; then
    report_result "Placeholder Quality" "PASS" "All templates have good educational placeholders"
else
    report_result "Placeholder Quality" "WARN" "$QUALITY_ISSUES files have quality issues (non-blocking)"
fi

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