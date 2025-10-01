#!/bin/bash
"""
Auto-generation workflow example script

Demonstrates the complete workflow generation process from specification
to validated implementation.
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Change to project root
cd "$(dirname "$0")/../.."

log_info "Starting PocketFlow workflow generation example..."

# Step 1: Generate workflow from specification
log_info "Step 1: Generating workflow from specification..."
if ! python3 .agent-os/workflows/generator.py --spec .agent-os/workflows/example-workflow-spec.yaml; then
    log_error "Workflow generation failed"
    exit 1
fi
log_success "Workflow generated successfully"

# Step 2: Validate generated workflow
log_info "Step 2: Validating generated workflow..."
if ! python3 scripts/validation/validate-generation.py --workflow contentanalyzer; then
    log_warning "Validation found issues (this is expected for example workflow)"
else
    log_success "Validation passed"
fi

# Step 3: Show generated structure
log_info "Step 3: Generated workflow structure:"
if [ -d ".agent-os/workflows/contentanalyzer" ]; then
    tree .agent-os/workflows/contentanalyzer/ || find .agent-os/workflows/contentanalyzer/ -type f | sort
else
    log_warning "Generated workflow directory not found"
fi

# Step 4: Check for required files
log_info "Step 4: Checking required files..."
required_files=(
    ".agent-os/workflows/contentanalyzer/docs/design.md"
    ".agent-os/workflows/contentanalyzer/schemas/models.py"
    ".agent-os/workflows/contentanalyzer/nodes.py"
    ".agent-os/workflows/contentanalyzer/flow.py"
    ".agent-os/workflows/contentanalyzer/tasks.md"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        log_success "✓ $file"
    else
        log_error "✗ $file"
        all_files_exist=false
    fi
done

if $all_files_exist; then
    log_success "All required files generated"
else
    log_warning "Some required files missing"
fi

# Step 5: Test code quality (if tools available)
log_info "Step 5: Testing code quality..."

if command -v uv &> /dev/null; then
    log_info "Running linting checks..."
    if uv run ruff check .agent-os/workflows/contentanalyzer/ 2>/dev/null; then
        log_success "Linting passed"
    else
        log_warning "Linting found issues (expected for generated template code)"
    fi
    
    log_info "Running type checks..."
    if uv run ty check .agent-os/workflows/contentanalyzer/ 2>/dev/null; then
        log_success "Type checking passed"
    else
        log_warning "Type checking found issues (expected for template code)"
    fi
else
    log_warning "uv not available, skipping code quality checks"
fi

# Step 6: Show sample files
log_info "Step 6: Sample generated files:"

echo -e "\n${BLUE}=== Generated Design Document (first 20 lines) ===${NC}"
if [ -f ".agent-os/workflows/contentanalyzer/docs/design.md" ]; then
    head -20 .agent-os/workflows/contentanalyzer/docs/design.md
else
    log_warning "Design document not found"
fi

echo -e "\n${BLUE}=== Generated Node Structure ===${NC}"
if [ -f ".agent-os/workflows/contentanalyzer/nodes.py" ]; then
    grep -n "class.*Node" .agent-os/workflows/contentanalyzer/nodes.py || log_warning "No node classes found"
else
    log_warning "Nodes file not found"
fi

echo -e "\n${BLUE}=== Generated Flow Structure ===${NC}"
if [ -f ".agent-os/workflows/contentanalyzer/flow.py" ]; then
    grep -n "class.*Flow" .agent-os/workflows/contentanalyzer/flow.py || log_warning "No flow class found"
else
    log_warning "Flow file not found"
fi

# Step 7: Summary
log_info "Step 7: Generation Summary"
echo -e "\n${GREEN}=== Workflow Generation Complete ===${NC}"
echo "Generated workflow: ContentAnalyzer"
echo "Pattern: RAG (Retrieval-Augmented Generation)"
echo "Location: .agent-os/workflows/contentanalyzer/"
echo ""
echo "Next steps:"
echo "1. Review generated design document"
echo "2. Implement utility functions in utils/"
echo "3. Complete node implementations"
echo "4. Add comprehensive tests"
echo "5. Integrate with FastAPI if needed"
echo ""
echo "Validation command:"
echo "  python3 scripts/validation/validate-generation.py --workflow contentanalyzer"
echo ""
echo "Clean up command:"
echo "  rm -rf .agent-os/workflows/contentanalyzer/"

log_success "Workflow generation example completed!"