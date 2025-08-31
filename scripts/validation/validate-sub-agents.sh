#!/bin/bash

# validate-sub-agents.sh
# Validates that the three new sub-agents are properly configured and detectable
# Part of Phase 1 sub-agent implementation
# Last Updated: 2025-01-18

set -e

echo "🔍 Validating Sub-Agent Implementation..."
echo "========================================"

# Check if we're in the project root
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

# Check 1: Sub-agent files exist
echo -e "\n📋 Checking for sub-agent files..."
REQUIRED_AGENTS=("template-validator.md" "pattern-analyzer.md" "dependency-orchestrator.md")
MISSING_AGENTS=()

for agent in "${REQUIRED_AGENTS[@]}"; do
    if [ -f ".claude/agents/$agent" ]; then
        echo -e "  ✓ Found .claude/agents/$agent"
    else
        MISSING_AGENTS+=("$agent")
    fi
done

if [ ${#MISSING_AGENTS[@]} -eq 0 ]; then
    report_result "Agent Files" "PASS" "All three sub-agent files found"
else
    report_result "Agent Files" "FAIL" "Missing agents: ${MISSING_AGENTS[*]}"
fi

# Check 2: Agent YAML frontmatter validation
echo -e "\n📋 Validating agent YAML frontmatter..."
YAML_ERRORS=()

for agent in "${REQUIRED_AGENTS[@]}"; do
    if [ -f ".claude/agents/$agent" ]; then
        # Check for required YAML fields
        if grep -q "^name:" ".claude/agents/$agent" && \
           grep -q "^description:" ".claude/agents/$agent" && \
           grep -q "^tools:" ".claude/agents/$agent"; then
            echo -e "  ✓ $agent has valid YAML structure"
        else
            YAML_ERRORS+=("$agent")
        fi
    fi
done

if [ ${#YAML_ERRORS[@]} -eq 0 ]; then
    report_result "YAML Frontmatter" "PASS" "All agent YAML frontmatter is valid"
else
    report_result "YAML Frontmatter" "FAIL" "Invalid YAML in: ${YAML_ERRORS[*]}"
fi

# Check 3: Coordination configuration
echo -e "\n📋 Checking coordination configuration..."
COORD_FILE=".agent-os/instructions/orchestration/coordination.yaml"
if [ -f "$COORD_FILE" ]; then
    # Check for new agents in coordination map
    if grep -q "template-validator:" "$COORD_FILE" && \
       grep -q "pattern-analyzer:" "$COORD_FILE" && \
       grep -q "dependency-orchestrator:" "$COORD_FILE"; then
        report_result "Coordination Config" "PASS" "All sub-agents found in coordination.yaml"
    else
        report_result "Coordination Config" "FAIL" "Sub-agents not properly configured in coordination.yaml"
    fi
else
    report_result "Coordination Config" "FAIL" "Coordination configuration file not found"
fi

# Check 4: Setup script includes new agents
echo -e "\n📋 Checking setup script integration..."
SETUP_FILE="setup-claude-code.sh"
if [ -f "$SETUP_FILE" ]; then
    if grep -q "template-validator" "$SETUP_FILE" && \
       grep -q "pattern-analyzer" "$SETUP_FILE" && \
       grep -q "dependency-orchestrator" "$SETUP_FILE"; then
        report_result "Setup Script" "PASS" "All sub-agents included in setup script"
    else
        report_result "Setup Script" "FAIL" "Sub-agents not found in setup script"
    fi
else
    report_result "Setup Script" "FAIL" "Setup script not found"
fi

# Check 5: Generator coordination functions
echo -e "\n📋 Checking generator coordination logic..."
GENERATOR_FILE=".agent-os/workflows/generator.py"
if [ -f "$GENERATOR_FILE" ]; then
    if grep -q "coordinate_template_validation" "$GENERATOR_FILE" && \
       grep -q "request_pattern_analysis" "$GENERATOR_FILE" && \
       grep -q "generate_dependency_config" "$GENERATOR_FILE"; then
        report_result "Generator Logic" "PASS" "All coordination functions found in generator"
    else
        report_result "Generator Logic" "FAIL" "Missing coordination functions in generator"
    fi
else
    report_result "Generator Logic" "FAIL" "Generator file not found"
fi

# Check 6: Validation data classes
echo -e "\n📋 Checking validation data classes..."
if [ -f "$GENERATOR_FILE" ]; then
    if grep -q "class ValidationResult" "$GENERATOR_FILE" && \
       grep -q "class PatternRecommendation" "$GENERATOR_FILE" && \
       grep -q "class DependencyConfig" "$GENERATOR_FILE"; then
        report_result "Data Classes" "PASS" "All coordination data classes found"
    else
        report_result "Data Classes" "FAIL" "Missing coordination data classes"
    fi
fi

# Check 7: Agent specialization flags
echo -e "\n📋 Checking agent specialization flags..."
SPECIALIZATION_FLAGS=()

if [ -f ".claude/agents/template-validator.md" ]; then
    if grep -q "validates_templates: true" ".claude/agents/template-validator.md"; then
        echo -e "  ✓ template-validator has validates_templates flag"
    else
        SPECIALIZATION_FLAGS+=("template-validator missing validates_templates")
    fi
fi

if [ -f ".claude/agents/pattern-analyzer.md" ]; then
    if grep -q "pattern_specialist: true" ".claude/agents/pattern-analyzer.md"; then
        echo -e "  ✓ pattern-analyzer has pattern_specialist flag"
    else
        SPECIALIZATION_FLAGS+=("pattern-analyzer missing pattern_specialist")
    fi
fi

if [ -f ".claude/agents/dependency-orchestrator.md" ]; then
    if grep -q "dependency_specialist: true" ".claude/agents/dependency-orchestrator.md"; then
        echo -e "  ✓ dependency-orchestrator has dependency_specialist flag"
    else
        SPECIALIZATION_FLAGS+=("dependency-orchestrator missing dependency_specialist")
    fi
fi

if [ ${#SPECIALIZATION_FLAGS[@]} -eq 0 ]; then
    report_result "Specialization Flags" "PASS" "All agents have proper specialization flags"
else
    report_result "Specialization Flags" "FAIL" "Issues: ${SPECIALIZATION_FLAGS[*]}"
fi

# Check 8: Framework vs usage distinction maintained
echo -e "\n📋 Checking framework vs usage distinction..."
FRAMEWORK_VIOLATIONS=()

# Check that agent descriptions mention framework enhancement
for agent in "${REQUIRED_AGENTS[@]}"; do
    if [ -f ".claude/agents/$agent" ]; then
        if grep -q -i "template\|framework\|generation" ".claude/agents/$agent"; then
            echo -e "  ✓ $agent maintains framework focus"
        else
            FRAMEWORK_VIOLATIONS+=("$agent")
        fi
    fi
done

if [ ${#FRAMEWORK_VIOLATIONS[@]} -eq 0 ]; then
    report_result "Framework Focus" "PASS" "All agents maintain framework vs usage distinction"
else
    report_result "Framework Focus" "WARN" "Agents may need framework focus review: ${FRAMEWORK_VIOLATIONS[*]}"
fi

# Final validation summary
echo -e "\n" 
echo "========================================"
if [ "$VALIDATION_PASSED" = true ]; then
    echo -e "${GREEN}🎉 Sub-Agent Validation PASSED${NC}"
    echo "All three sub-agents are properly configured and detectable."
    echo ""
    echo "✅ Phase 1 Foundation Setup Complete!"
    echo "📋 Next: Proceed to Phase 2 - Template Validator Implementation"
    exit 0
else
    echo -e "${RED}💥 Sub-Agent Validation FAILED${NC}"
    echo "Some sub-agent configuration issues need to be addressed."
    echo ""
    echo "📚 See docs/sub-agents-implementation.md for implementation guidelines"
    exit 1
fi
