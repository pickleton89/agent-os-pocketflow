#!/bin/bash
# Design Document Validation Script
echo "📋 Validating design document..."

if [[ ! -f "docs/design.md" ]]; then
    echo "❌ docs/design.md not found"
    exit 1
fi

# Check for required sections (accept any header level `#` or `##`)
required_base_titles=(
    "Requirements"
    "Flow Design"
    "Data Design"
    "Implementation Plan"
)

for title in "${required_base_titles[@]}"; do
    if grep -Eq "^#{1,6} ${title}$" docs/design.md; then
        echo "✅ Found section: ${title}"
    else
        echo "❌ Missing section: ${title}"
        exit 1
    fi
done

# Accept either Node Design OR Node Specifications
if grep -Eq '^#{1,6} (Node Design|Node Specifications)$' docs/design.md; then
    echo "✅ Found node section: Node Design/Specifications"
else
    echo "❌ Missing section: Node Design or Node Specifications"
    exit 1
fi

echo "🎉 Design document validation passed!"
