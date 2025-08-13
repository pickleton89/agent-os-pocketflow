 #!/bin/bash

# Agent OS Claude Code Setup Script
# This script installs Agent OS commands for Claude Code

set -e  # Exit on error

echo "🚀 Agent OS Claude Code Setup"
echo "============================="
echo ""

# Check if Agent OS base installation is present
if [ ! -d "$HOME/.agent-os/instructions/core" ] || [ ! -d "$HOME/.agent-os/instructions/extensions" ] || [ ! -d "$HOME/.agent-os/instructions/orchestration" ] || [ ! -d "$HOME/.agent-os/standards" ]; then
    echo "⚠️  Agent OS base installation not found or incomplete!"
    echo ""
    echo "Please install the Agent OS base installation first:"
    echo ""
    echo "Option 1 - Automatic installation:"
    echo "  curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash"
    echo ""
    echo "Option 2 - Manual installation:"
    echo "  Follow instructions at https://buildermethods.com/agent-os"
    echo ""
    echo "If you have an older installation, you may need to update it to include templates:"
    echo "  curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash --overwrite-instructions"
    echo ""
    exit 1
fi

# Base URL for raw GitHub content
BASE_URL="https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main"

# Create directories
echo "📁 Creating directories..."
mkdir -p "$HOME/.claude/commands"
mkdir -p "$HOME/.claude/agents"

# Link to instruction files instead of downloading commands
echo ""
echo "📥 Linking instruction files for Claude Code commands"

# Create symlinks to instruction files if local
if [ -d "instructions/core" ]; then
    echo "  ✓ Using local instruction files from instructions/core/"
else
    echo "  ⚠️  Local instructions not found - downloading from repository"
    # Download instruction files if not local
    for cmd in plan-product create-spec execute-tasks analyze-product execute-task; do
        curl -s -o "$HOME/.claude/commands/${cmd}.md" "${BASE_URL}/instructions/core/${cmd}.md"
        echo "  ✓ Downloaded ${cmd}.md"
    done
fi

# Download Claude Code agents
echo ""
echo "📥 Downloading Claude Code subagents to ~/.claude/agents/"

# List of agent files to download
agents=("test-runner" "context-fetcher" "git-workflow" "file-creator" "date-checker")

for agent in "${agents[@]}"; do
    if [ -f "$HOME/.claude/agents/${agent}.md" ]; then
        echo "  ⚠️  ~/.claude/agents/${agent}.md already exists - skipping"
    else
        curl -s -o "$HOME/.claude/agents/${agent}.md" "${BASE_URL}/claude-code/agents/${agent}.md"
        echo "  ✓ ~/.claude/agents/${agent}.md"
    fi
done

echo ""
echo "✅ Agent OS Claude Code installation complete!"
echo ""
echo "📍 Files installed to:"
echo "   instructions/core/         - Agent OS instructions (or ~/.claude/commands/ if downloaded)"
echo "   ~/.claude/agents/          - Claude Code specialized subagents"
echo ""
echo "Next steps:"
echo ""
echo "Initiate Agent OS in a new product's codebase with:"
echo "  /plan-product"
echo ""
echo "Initiate Agent OS in an existing product's codebase with:"
echo "  /analyze-product"
echo ""
echo "Initiate a new feature with:"
echo "  /create-spec (or simply ask 'what's next?')"
echo ""
echo "Build and ship code with:"
echo "  /execute-tasks"
echo ""
echo "Learn more at https://buildermethods.com/agent-os"
echo ""
