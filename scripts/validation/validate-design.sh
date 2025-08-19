#!/bin/bash
# Design Document Validation Script
echo "📋 Validating design document..."

if [[ ! -f "docs/design.md" ]]; then
    echo "❌ docs/design.md not found"
    exit 1
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
