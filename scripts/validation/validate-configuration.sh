#!/bin/bash

# validate-configuration.sh
# Validates that configuration files maintain framework vs application boundaries
# Last Updated: 2025-08-16

set -e

echo "🔍 Validating Framework Configuration Boundaries..."
echo "=================================================="

# Check if we're in the project root (pyproject.toml should exist)
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found${NC}"
    echo "This script must be run from the project root directory."
    echo "Current directory: $(pwd)"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Check 1: No application-specific environment files
echo -e "\n📋 Checking for inappropriate environment files..."
ENV_FILES=$(find . -name "*.env*" -not -path "./.venv/*" -not -path "./.git/*" -not -path "./.gitignore" 2>/dev/null || true)
if [ -z "$ENV_FILES" ]; then
    report_result "Environment Files" "PASS" "No application-specific .env files found"
else
    report_result "Environment Files" "FAIL" "Found inappropriate .env files: $ENV_FILES"
fi

# Check 2: No PocketFlow runtime dependencies
echo -e "\n📋 Checking for PocketFlow dependencies..."
POCKETFLOW_DEPS=$(grep '"pocketflow' pyproject.toml uv.lock 2>/dev/null | grep -v 'name.*agent-os-pocketflow' || true)
if [ -z "$POCKETFLOW_DEPS" ]; then
    report_result "PocketFlow Dependencies" "PASS" "No PocketFlow runtime dependencies found"
else
    report_result "PocketFlow Dependencies" "FAIL" "Found PocketFlow dependencies in framework: $POCKETFLOW_DEPS"
fi

# Check 3: No application deployment configurations
echo -e "\n📋 Checking for application deployment configs..."
DEPLOY_CONFIGS=$(find . -name "docker-compose.yml" -o -name "Dockerfile" -o -name "kubernetes.yaml" -o -name "k8s.yaml" -not -path "./.venv/*" 2>/dev/null || true)
if [ -z "$DEPLOY_CONFIGS" ]; then
    report_result "Deployment Configs" "PASS" "No application deployment configs found"
else
    report_result "Deployment Configs" "WARN" "Found deployment configs (may be templates): $DEPLOY_CONFIGS"
fi

# Check 4: No CI/CD application pipelines
echo -e "\n📋 Checking for CI/CD pipelines..."
if [ ! -d ".github/workflows" ] && [ ! -f ".gitlab-ci.yml" ] && [ ! -f ".travis.yml" ] && [ ! -f "circle.yml" ]; then
    report_result "CI/CD Pipelines" "PASS" "No application CI/CD pipelines found"
else
    CICD_FILES=$(find .github .gitlab-ci.yml .travis.yml circle.yml 2>/dev/null || true)
    report_result "CI/CD Pipelines" "WARN" "Found CI/CD configs (check they're for framework): $CICD_FILES"
fi

# Check 5: Framework description in pyproject.toml
echo -e "\n📋 Checking pyproject.toml description..."
DESCRIPTION=$(grep "description.*framework" pyproject.toml -i || true)
if [ -n "$DESCRIPTION" ]; then
    report_result "Project Description" "PASS" "Description clearly identifies this as framework"
else
    report_result "Project Description" "FAIL" "Description should identify this as Agent OS + PocketFlow framework"
fi

# Check 6: Only appropriate dependencies
echo -e "\n📋 Checking dependency appropriateness..."
# List of inappropriate dependencies for a framework
INAPPROPRIATE_DEPS=$(grep -E "(django|flask|rails|express|database|postgres|mysql|redis|mongodb)" pyproject.toml -i || true)
if [ -z "$INAPPROPRIATE_DEPS" ]; then
    report_result "Framework Dependencies" "PASS" "No inappropriate application dependencies found"
else
    report_result "Framework Dependencies" "WARN" "Found potentially inappropriate deps: $INAPPROPRIATE_DEPS"
fi

# Check 7: Template vs implementation patterns
echo -e "\n📋 Checking for proper template structure..."
TEMPLATE_DIRS=$(find .agent-os -name "workflows" -o -name "templates" 2>/dev/null || true)
if [ -n "$TEMPLATE_DIRS" ]; then
    report_result "Template Structure" "PASS" "Found appropriate template directories"
else
    report_result "Template Structure" "WARN" "No template directories found in .agent-os"
fi

# Check 8: Claude configuration appropriateness
echo -e "\n📋 Checking Claude configuration..."
if [ -f ".claude/config.json" ]; then
    # Check for framework-appropriate MCP servers
    FRAMEWORK_MCPS=$(grep -E "(pocketflow|agent-os|git)" .claude/config.json || true)
    if [ -n "$FRAMEWORK_MCPS" ]; then
        report_result "Claude Config" "PASS" "Claude config contains framework-appropriate MCP servers"
    else
        report_result "Claude Config" "WARN" "Claude config may not contain framework-specific MCP servers"
    fi
else
    report_result "Claude Config" "WARN" "No Claude configuration found"
fi

# Final validation summary
echo -e "\n" 
echo "=================================================="
if [ "$VALIDATION_PASSED" = true ]; then
    echo -e "${GREEN}🎉 Configuration Validation PASSED${NC}"
    echo "Framework configuration boundaries are properly maintained."
    exit 0
else
    echo -e "${RED}💥 Configuration Validation FAILED${NC}"
    echo "Some configuration issues need to be addressed."
    echo ""
    echo "📚 See docs/CONFIGURATION.md for guidelines on framework vs application configs"
    exit 1
fi