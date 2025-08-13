#!/bin/bash
# Design Document Validation Script
echo "📋 Validating design document..."

if [[ ! -f "docs/design.md" ]]; then
    echo "⚠️  docs/design.md not found - this is expected for new projects"
    echo "✅ Design document validation passed (no design.md required for initial setup)"
    exit 0
fi

# Check for required sections
required_sections=(
    "# Requirements"
    "# Flow Design"
    "# Data Design"
    "# Node Design"
    "# Implementation Plan"
)

for section in "${required_sections[@]}"; do
    if grep -q "$section" docs/design.md; then
        echo "✅ Found section: $section"
    else
        echo "❌ Missing section: $section"
        exit 1
    fi
done

echo "🎉 Design document validation passed!"
