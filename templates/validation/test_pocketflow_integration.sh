#!/bin/bash
# PocketFlow Integration Test Script - PROJECT SETUP VALIDATION
# Tests that framework-generated templates and structure are properly installed
# This template is installed by the Agent OS + PocketFlow setup process

echo "🧪 Testing PocketFlow Setup Integration (Project Mode)..."

# This script validates that the framework successfully generated templates and structure
echo "ℹ️  Project mode: validating framework-generated templates and setup"

# Test 1: Framework-generated directory structure
echo "🔍 Testing framework-generated directory structure..."
essential_dirs=(
    ".agent-os"
    ".agent-os/pocketflow-tools" 
    ".agent-os/instructions"
    ".agent-os/templates"
)

missing_dirs=()
for dir in "${essential_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "✅ Framework-generated directory exists: $dir"
    else
        echo "⚠️  Framework-generated directory missing: $dir"
        missing_dirs+=("$dir")
    fi
done

if [[ ${#missing_dirs[@]} -gt 0 ]]; then
    echo "❌ Missing essential framework-generated directories. Re-run: ./setup.sh"
    exit 1
fi

# Test 2: Framework-generated tool templates
echo "🔍 Testing framework-generated tool templates..."
expected_templates=(
    ".agent-os/pocketflow-tools/pattern_analyzer.py"
    ".agent-os/pocketflow-tools/dependency_orchestrator.py" 
    ".agent-os/pocketflow-tools/agent_coordination.py"
)

missing_templates=()
for template in "${expected_templates[@]}"; do
    if [[ -f "$template" ]]; then
        echo "✅ Framework template exists: $(basename "$template")"
        
        # Check if template has TODO stubs (expected for generated templates)
        if grep -q "TODO\|FIXME\|NotImplementedError\|pass  # Implementation needed" "$template" 2>/dev/null; then
            echo "✅ Template contains TODO stubs for customization (expected)"
        else
            echo "ℹ️  Template ready for use (may be pre-implemented)"
        fi
    else
        echo "⚠️  Framework template missing: $(basename "$template")"
        missing_templates+=("$template")
    fi
done

if [[ ${#missing_templates[@]} -gt 0 ]]; then
    echo "❌ Missing framework-generated templates. Re-run: ./setup.sh"
    exit 1
fi

# Test 3: Framework-generated configuration files
echo "🔍 Testing framework-generated configuration..."
config_files=(
    ".agent-os/instructions/core/agent-orchestration.md"
    ".agent-os/instructions/core/pocketflow-coordination.md"
)

for config_file in "${config_files[@]}"; do
    if [[ -f "$config_file" ]]; then
        echo "✅ Framework configuration exists: $(basename "$config_file")"
    else
        echo "ℹ️  Framework configuration not found: $(basename "$config_file") (may be optional)"
    fi
done

# Test 4: Agent template preparation (end-user customization area)
echo "🔍 Testing agent template preparation..."

# Check if .claude directory is ready for agent files (end-user creates these)
if [[ -d ".claude" ]]; then
    echo "✅ Claude directory exists for agent definitions"
    
    # Count any agent files (created by end-users, not framework)
    agent_count=$(find .claude -name "*.md" 2>/dev/null | wc -l)
    if [[ $agent_count -gt 0 ]]; then
        echo "✅ Found $agent_count agent file(s) (end-user customized)"
    else
        echo "ℹ️  No agent files yet (end-users create these as needed)"
    fi
else
    echo "ℹ️  Claude directory not present (can be created: mkdir -p .claude/agents)"
fi

# Test 5: Template customization readiness
echo "🔍 Testing template customization readiness..."

# Check for development environment setup
if command -v uv >/dev/null 2>&1; then
    echo "✅ uv package manager available (needed for template development)"
else
    echo "❌ uv package manager not found - required for template customization"
    echo "    Install from: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

if python3 --version >/dev/null 2>&1; then
    echo "✅ Python 3 available (needed for template development)"
else
    echo "❌ Python 3 not found"
    exit 1
fi

# Test 6: Framework-generated wrapper scripts (if they exist)
echo "🔍 Testing framework-generated wrapper scripts..."
if [[ -f ".agent-os/pocketflow-tools/run.sh" ]]; then
    echo "✅ Framework-generated wrapper script exists"
    
    # Test that wrapper can show help (basic functionality test)
    if bash ".agent-os/pocketflow-tools/run.sh" --help >/dev/null 2>&1; then
        echo "✅ Wrapper script shows help (basic functionality working)"
    else
        echo "ℹ️  Wrapper script may need customization for your project"
    fi
else
    echo "ℹ️  No wrapper script generated (may be created during development)"
fi

# Test 7: Template development environment
echo "🔍 Testing template development environment..."

# Check if we're in a git repository (good practice for template development)
if git rev-parse --git-dir >/dev/null 2>&1; then
    echo "✅ Git repository detected (good for template development)"
else
    echo "ℹ️  Not a git repository (consider: git init for version control)"
fi

# Check for project-level requirements or environment files
if [[ -f "pyproject.toml" ]] || [[ -f "requirements.txt" ]] || [[ -f "uv.lock" ]]; then
    echo "✅ Project dependency management detected"
else
    echo "ℹ️  No dependency management files found (create as needed for your project)"
fi

echo "🎉 Framework setup validation complete!"
echo ""
echo "📋 Framework Setup Summary:"
echo "  ✅ Framework-generated directory structure in place"
echo "  ✅ Tool templates installed and ready for customization"
echo "  ✅ Configuration templates available"
echo "  ✅ Development environment ready"
echo "  ✅ Template customization environment prepared"
echo ""
echo "🎯 Framework vs Usage Reminder:"
echo "  📦 Framework generated TEMPLATES and starting points"
echo "  🛠️  You implement and customize these templates for your project"
echo "  🚀 Templates become working applications through your development"
echo ""
echo "💡 Next Steps (Template Customization):"
echo "  1. Review templates in .agent-os/pocketflow-tools/ for TODO stubs"
echo "  2. Implement the template functions according to your project needs"  
echo "  3. Create agent files in .claude/agents/ for your workflow"
echo "  4. Test your implementations as you develop them"
echo "  5. Use the orchestrator once your templates are working"