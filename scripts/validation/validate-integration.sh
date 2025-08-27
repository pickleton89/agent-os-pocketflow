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

# Test 3: Extension modules
extensions=(
    "$AGENT_OS_DIR/instructions/extensions/llm-workflow-extension.md"
    "$AGENT_OS_DIR/instructions/extensions/design-first-enforcement.md"
    "$AGENT_OS_DIR/instructions/extensions/pocketflow-integration.md"
)

for ext in "${extensions[@]}"; do
    if [[ -f "$ext" ]]; then
        echo "✅ Extension found: $(basename "$ext")"
    else
        echo "❌ Extension missing: $(basename "$ext")"
        exit 1
    fi
done

# Test 4: Coordination configuration
if [[ -f "$AGENT_OS_DIR/instructions/orchestration/coordination.yaml" ]]; then
    echo "✅ Coordination configuration found"
else
    echo "❌ Coordination configuration missing"
    exit 1
fi

echo "🎉 All integration tests passed!"
