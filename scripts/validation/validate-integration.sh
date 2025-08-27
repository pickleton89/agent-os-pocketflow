#!/bin/bash
# Integration Validation Script
echo "🧪 Testing Agent OS + PocketFlow Integration..."

# Test 1: Directory structure (check project .agent-os first, then fall back to base)
if [[ -d ".agent-os/instructions/orchestration" ]]; then
    echo "✅ Project orchestration directory exists"
    AGENT_OS_DIR=".agent-os"
elif [[ -d "$HOME/.agent-os/instructions/orchestration" ]]; then
    echo "✅ Base orchestration directory exists"
    AGENT_OS_DIR="$HOME/.agent-os"
else
    echo "❌ Orchestration directory missing"
    exit 1
fi

# Test 2: Orchestrator agent
if [[ -f ".claude/agents/pocketflow-orchestrator.md" ]]; then
    echo "✅ Orchestrator agent found"
else
    echo "❌ Orchestrator agent missing"
    exit 1
fi

# Test 3: Extension modules - Template Quality Validation
extensions=(
    "$AGENT_OS_DIR/instructions/extensions/llm-workflow-extension.md"
    "$AGENT_OS_DIR/instructions/extensions/design-first-enforcement.md"
    "$AGENT_OS_DIR/instructions/extensions/pocketflow-integration.md"
)

echo "🔍 Testing extension template quality..."

validate_extension_quality() {
    local ext_file="$1"
    local ext_name=$(basename "$ext_file")
    
    echo "Testing $ext_name..."
    
    # Test 1: File exists and is not empty
    if [[ ! -f "$ext_file" || ! -s "$ext_file" ]]; then
        echo "❌ Extension missing or empty: $ext_name"
        return 1
    fi
    
    # Test 2: Contains template generation guidance
    if ! grep -q "Template Generation Guide\|Template Output" "$ext_file"; then
        echo "❌ $ext_name missing template generation guidance"
        return 1
    fi
    
    # Test 3: Contains TODO placeholders for end-users
    local todo_count=$(grep -c "TODO:" "$ext_file" || echo "0")
    if [[ $todo_count -lt 5 ]]; then
        echo "❌ $ext_name has insufficient TODO guidance ($todo_count found, minimum 5 required)"
        return 1
    fi
    
    # Test 4: Contains framework boundary language
    if ! grep -q "end-user projects\|End-User Projects" "$ext_file"; then
        echo "❌ $ext_name missing framework vs usage boundary clarity"
        return 1
    fi
    
    # Test 5: Contains orchestrator integration examples
    if ! grep -q "orchestrator\|Orchestrator" "$ext_file"; then
        echo "❌ $ext_name missing orchestrator integration guidance"
        return 1
    fi
    
    # Test 6: Contains code template examples
    if ! grep -q "```python\|```bash" "$ext_file"; then
        echo "❌ $ext_name missing code template examples"
        return 1
    fi
    
    # Test 7: Framework-specific validation
    case "$ext_name" in
        "design-first-enforcement.md")
            if ! grep -q "validation.*script\|design.*document" "$ext_file"; then
                echo "❌ $ext_name missing design validation templates"
                return 1
            fi
            ;;
        "llm-workflow-extension.md")
            if ! grep -q "pattern.*detection\|LLM\|AI" "$ext_file"; then
                echo "❌ $ext_name missing LLM pattern detection templates"
                return 1
            fi
            ;;
        "pocketflow-integration.md")
            if ! grep -q "auto.*detection\|project.*analysis" "$ext_file"; then
                echo "❌ $ext_name missing auto-detection templates"
                return 1
            fi
            ;;
    esac
    
    echo "✅ $ext_name template quality validation passed"
    return 0
}

# Validate each extension
for ext in "${extensions[@]}"; do
    if ! validate_extension_quality "$ext"; then
        echo "❌ Extension template quality validation failed"
        exit 1
    fi
done

echo "✅ All extensions passed template quality validation"

# Test 4: Orchestrator Hooks Template Quality
echo "🔍 Testing orchestrator hooks template quality..."

validate_orchestrator_hooks() {
    local hooks_file="$AGENT_OS_DIR/instructions/orchestration/orchestrator-hooks.md"
    
    if [[ ! -f "$hooks_file" || ! -s "$hooks_file" ]]; then
        echo "❌ Orchestrator hooks file missing or empty"
        return 1
    fi
    
    # Test 1: Contains hook sections referenced by coordination.yaml
    if ! grep -q "## validate_design_document" "$hooks_file"; then
        echo "❌ Missing validate_design_document section"
        return 1
    fi
    
    if ! grep -q "## validate_workflow_implementation" "$hooks_file"; then
        echo "❌ Missing validate_workflow_implementation section"
        return 1
    fi
    
    # Test 2: Hook sections contain template code for end-users
    if ! grep -A 20 "## validate_design_document" "$hooks_file" | grep -q "```bash"; then
        echo "❌ validate_design_document section missing template code"
        return 1
    fi
    
    if ! grep -A 20 "## validate_workflow_implementation" "$hooks_file" | grep -q "```bash"; then
        echo "❌ validate_workflow_implementation section missing template code"
        return 1
    fi
    
    # Test 3: Template sections contain TODO guidance
    local validate_design_todos=$(grep -A 50 "## validate_design_document" "$hooks_file" | grep -c "TODO:" || echo "0")
    if [[ $validate_design_todos -lt 3 ]]; then
        echo "❌ validate_design_document section has insufficient TODO guidance ($validate_design_todos found)"
        return 1
    fi
    
    local validate_workflow_todos=$(grep -A 50 "## validate_workflow_implementation" "$hooks_file" | grep -c "TODO:" || echo "0")
    if [[ $validate_workflow_todos -lt 3 ]]; then
        echo "❌ validate_workflow_implementation section has insufficient TODO guidance ($validate_workflow_todos found)"
        return 1
    fi
    
    # Test 4: Template sections contain orchestrator integration guidance
    if ! grep -A 50 "## validate_design_document" "$hooks_file" | grep -q "claude-code.*orchestrator"; then
        echo "❌ validate_design_document section missing orchestrator integration"
        return 1
    fi
    
    echo "✅ Orchestrator hooks template quality validation passed"
    return 0
}

if ! validate_orchestrator_hooks; then
    echo "❌ Orchestrator hooks template quality validation failed"
    exit 1
fi

# Test 5: Coordination configuration
if [[ -f "$AGENT_OS_DIR/instructions/orchestration/coordination.yaml" ]]; then
    echo "✅ Coordination configuration found"
else
    echo "❌ Coordination configuration missing"
    exit 1
fi

echo "🎉 All integration tests passed!"
