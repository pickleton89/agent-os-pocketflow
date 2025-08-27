#!/bin/bash
# PocketFlow Setup Validation Script
echo "⚙️ Validating PocketFlow setup..."

# Check Python environment
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
else
    echo "❌ Python 3 not found"
    exit 1
fi

# Check for PocketFlow workflow structure
if [[ -d ".agent-os/workflows" ]]; then
    echo "✅ PocketFlow workflows directory found"
    
    # Check for any workflow subdirectories
    workflow_count=$(find .agent-os/workflows -maxdepth 1 -type d | grep -v "^\.agent-os/workflows$" | wc -l)
    if [[ $workflow_count -gt 0 ]]; then
        echo "✅ Found $workflow_count PocketFlow workflow(s)"
        
        # Check for PocketFlow files in workflows
        pocketflow_files=("nodes.py" "flow.py")
        for workflow_dir in .agent-os/workflows/*/; do
            if [[ -d "$workflow_dir" ]]; then
                workflow_name=$(basename "$workflow_dir")
                echo "  Checking workflow: $workflow_name"
                
                for file in "${pocketflow_files[@]}"; do
                    if [[ -f "$workflow_dir$file" ]]; then
                        echo "    ✅ Found: $file"
                    else
                        echo "    ❌ Missing: $file"
                    fi
                done
            fi
        done
    else
        echo "❌ No workflows found in .agent-os/workflows"
        exit 1
    fi
else
    echo "❌ PocketFlow workflows directory missing: .agent-os/workflows"
    exit 1
fi

echo "🎉 PocketFlow validation passed!"
