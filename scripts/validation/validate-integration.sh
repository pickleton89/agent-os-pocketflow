#!/bin/bash
# Integration Validation Script
echo "🧪 Testing Agent OS + PocketFlow Integration..."

# Test 1: Directory structure
if [[ -d ".agent-os/instructions/orchestration" ]]; then
    echo "✅ Orchestration directory exists"
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
local extensions=(
    ".agent-os/instructions/extensions/llm-workflow-extension.md"
    ".agent-os/instructions/extensions/design-first-enforcement.md"
    ".agent-os/instructions/extensions/pocketflow-integration.md"
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
if [[ -f ".agent-os/instructions/orchestration/coordination.yaml" ]]; then
    echo "✅ Coordination configuration found"
else
    echo "❌ Coordination configuration missing"
    exit 1
fi

echo "🎉 All integration tests passed!"
