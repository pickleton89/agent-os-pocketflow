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

# Check for source directories
src_dirs=("src/nodes" "src/flows" "src/schemas" "src/utils")
for dir in "${src_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "✅ Directory found: $dir"
    else
        echo "❌ Directory missing: $dir"
        exit 1
    fi
done

echo "🎉 PocketFlow validation passed!"
