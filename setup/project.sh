#!/bin/bash
# Enhanced Agent OS + PocketFlow Project Installation Script
# Compatible with Agent OS v1.4.0 architecture
# Installs Agent OS into individual project directories

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_VERSION="2.0.0"
AGENT_OS_COMPATIBILITY="1.4.0"
REPO_URL="https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main"

# Installation options (can be set via command line arguments)
BASE_INSTALL_PATH=""
ENABLE_POCKETFLOW=true
ENABLE_CLAUDE_CODE=true
NO_BASE_INSTALL=false
PROJECT_TYPE="pocketflow-enhanced"
FORCE_INSTALL=false

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_highlight() { echo -e "${PURPLE}🎯 $1${NC}"; }

# Safe download function with validation
safe_download() {
    local url="$1"
    local target="$2"
    local description="${3:-file}"
    
    curl -s -o "$target" "$url"
    local curl_exit=$?
    
    if [[ $curl_exit -ne 0 ]]; then
        log_error "Failed to download $description (curl error: $curl_exit)"
        return 1
    fi
    
    if [[ ! -f "$target" ]]; then
        log_error "Download failed: $description not created"
        return 1
    fi
    
    if [[ ! -s "$target" ]]; then
        log_error "Download failed: $description is empty"
        rm -f "$target"
        return 1
    fi
    
    return 0
}

# Safe copy function with validation
safe_copy() {
    local source="$1"
    local target="$2"
    local description="${3:-files}"
    
    if [[ ! -e "$source" ]]; then
        log_error "Source not found for $description: $source"
        return 1
    fi
    
    cp -r "$source" "$target"
    local cp_exit=$?
    
    if [[ $cp_exit -ne 0 ]]; then
        log_error "Failed to copy $description (cp error: $cp_exit)"
        return 1
    fi
    
    if [[ ! -e "$target" ]]; then
        log_error "Copy failed: $description not created at $target"
        return 1
    fi
    
    return 0
}

# Display header
show_header() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║              Enhanced Agent OS + PocketFlow                  ║
║             Project Installation Script v2.0.0              ║
║                                                              ║
║  🎯 Agent OS v1.4.0 Compatible + PocketFlow Enhancements    ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --base-path)
                if [[ -z "$2" ]]; then
                    log_error "--base-path requires a path argument"
                    exit 1
                fi
                BASE_INSTALL_PATH="$2"
                shift 2
                ;;
            --no-base)
                NO_BASE_INSTALL=true
                shift
                ;;
            --pocketflow)
                ENABLE_POCKETFLOW=true
                shift
                ;;
            --no-pocketflow)
                ENABLE_POCKETFLOW=false
                PROJECT_TYPE="standard-agent-os"
                shift
                ;;
            --claude-code)
                ENABLE_CLAUDE_CODE=true
                shift
                ;;
            --project-type)
                if [[ -z "$2" ]]; then
                    log_error "--project-type requires a type argument"
                    exit 1
                fi
                PROJECT_TYPE="$2"
                shift 2
                ;;
            --force)
                FORCE_INSTALL=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown argument: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Show help
show_help() {
    cat << EOF

Enhanced Agent OS + PocketFlow Project Installation

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --base-path PATH        Path to base installation (auto-detected if not provided)
    --no-base              Install without base installation (standalone mode)
    --pocketflow           Enable PocketFlow features (default)
    --no-pocketflow        Disable PocketFlow features (standard Agent OS only)
    --claude-code          Enable Claude Code integration
    --project-type TYPE    Project type (default: pocketflow-enhanced)
    --force                Force installation even if .agent-os exists
    --help                 Show this help message

PROJECT TYPES:
    pocketflow-enhanced    Full PocketFlow + Agent OS (default)
    standard-agent-os      Standard Agent OS only
    python-pocketflow      Python-optimized PocketFlow setup
    fastapi-pocketflow     FastAPI + PocketFlow setup

EXAMPLES:
    # Basic enhanced Agent OS + PocketFlow installation
    $0
    
    # With Claude Code support
    $0 --claude-code
    
    # Standard Agent OS only (no PocketFlow)
    $0 --no-pocketflow --claude-code
    
    # Standalone installation (no base required)
    $0 --no-base --claude-code
    
    # Custom project type
    $0 --project-type python-pocketflow --claude-code

NOTES:
    • Run this script from your project's root directory
    • If no base installation is found, --no-base mode will be used automatically
    • PocketFlow features include workflow generators, pattern analyzers, and validators

EOF
}

# Auto-detect base installation path
detect_base_installation() {
    if [[ -n "$BASE_INSTALL_PATH" ]]; then
        # Use provided path
        BASE_INSTALL_PATH="${BASE_INSTALL_PATH/#\~/$HOME}"
        return 0
    fi
    
    # Try to detect from script location
    local script_dir="$(dirname "$(dirname "$(realpath "$0")")" 2>/dev/null || echo "")"
    if [[ -f "$script_dir/config.yml" ]]; then
        BASE_INSTALL_PATH="$script_dir"
        log_info "Detected base installation: $BASE_INSTALL_PATH"
        return 0
    fi
    
    # Common installation locations
    local common_paths=(
        "$HOME/.agent-os"
        "/usr/local/agent-os"
        "$(pwd)/../.agent-os"
    )
    
    for path in "${common_paths[@]}"; do
        if [[ -f "$path/config.yml" ]] && [[ -d "$path/setup" ]]; then
            BASE_INSTALL_PATH="$path"
            log_info "Found base installation: $BASE_INSTALL_PATH"
            return 0
        fi
    done
    
    return 1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check for required tools
    local required_tools=("git" "curl" "mkdir" "cp" "chmod")
    local missing_tools=()
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_info "Please install the missing tools and try again"
        exit 1
    fi
    
    # Check if we're in a directory suitable for a project
    if [[ ! -w "." ]]; then
        log_error "Current directory is not writable"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Validate base installation
validate_base_installation() {
    if [[ "$NO_BASE_INSTALL" == "true" ]]; then
        log_info "Standalone mode enabled (--no-base)"
        return 0
    fi
    
    if ! detect_base_installation; then
        log_warning "No base installation found"
        log_info "Options:"
        echo "  1. Install base first: curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup/base.sh | bash"
        echo "  2. Use --no-base for standalone installation"
        echo "  3. Use --base-path to specify custom base location"
        exit 1
    fi
    
    # Validate base installation structure
    local required_base_dirs=(
        "$BASE_INSTALL_PATH/instructions"
        "$BASE_INSTALL_PATH/standards"
    )
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        required_base_dirs+=(
            "$BASE_INSTALL_PATH/pocketflow-tools"
        )
    fi
    
    for dir in "${required_base_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            log_error "Invalid base installation: missing $dir"
            log_info "Please reinstall the base installation"
            exit 1
        fi
    done
    
    log_success "Base installation validated: $BASE_INSTALL_PATH"
}

# Check existing project installation
check_existing_installation() {
    if [[ -d ".agent-os" ]]; then
        if [[ "$FORCE_INSTALL" == "true" ]]; then
            log_warning "Existing .agent-os directory found - will overwrite (--force enabled)"
            rm -rf ".agent-os"
        else
            log_warning "Existing .agent-os directory found"
            echo "Options:"
            echo "  1. Use --force to overwrite completely"
            echo "  2. Remove .agent-os directory manually"
            echo "  3. Choose a different directory"
            exit 1
        fi
    fi
}

# Create project directory structure
create_project_structure() {
    log_info "Creating project directory structure..."
    
    # Core Agent OS directories (v1.4.0 compatible)
    local core_dirs=(
        ".agent-os"
        ".agent-os/instructions"
        ".agent-os/standards"
    )
    
    # PocketFlow enhancement directories
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        core_dirs+=(
            ".agent-os/pocketflow-tools"
            ".agent-os/templates"
            ".agent-os/product"
            ".agent-os/specs"
            ".agent-os/recaps"
        )
    fi
    
    # Claude Code directories
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        core_dirs+=(
            ".claude/commands"
            ".claude/agents"
        )
    fi
    
    # Create directories
    for dir in "${core_dirs[@]}"; do
        mkdir -p "$dir"
        log_success "Created: $dir"
    done
}

# Install instructions from base or repository (Agent OS v1.4.0 compliant)
install_instructions() {
    log_info "Installing instructions..."
    
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/instructions" ]]; then
        # Copy full instructions from base installation (v1.4.0 self-contained design)
        cp -r "$BASE_INSTALL_PATH/instructions"/* ".agent-os/instructions/"
        if [[ $? -eq 0 ]]; then
            log_success "Copied instructions from base installation"
        else
            log_error "Failed to copy instructions from base installation"
            exit 1
        fi
    else
        # Download from repository (standalone mode)
        log_info "Downloading instructions from repository..."
        
        # Create subdirectories
        mkdir -p ".agent-os/instructions/core"
        mkdir -p ".agent-os/instructions/meta"
        
        local instruction_files=("analyze-product.md" "create-spec.md" "execute-task.md" "execute-tasks.md" "plan-product.md" "post-execution-tasks.md")
        
        for file in "${instruction_files[@]}"; do
            if safe_download "$REPO_URL/instructions/core/$file" ".agent-os/instructions/core/$file" "$file"; then
                log_success "Downloaded: $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
        
        # Download meta instructions
        if ! safe_download "$REPO_URL/instructions/meta/pre-flight.md" ".agent-os/instructions/meta/pre-flight.md" "pre-flight.md"; then
            log_warning "Failed to download pre-flight.md (optional)"
        fi
    fi
}

# Install standards from base or repository (Agent OS v1.4.0 compliant)
install_standards() {
    log_info "Installing standards..."
    
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/standards" ]]; then
        # Copy full standards from base installation (v1.4.0 self-contained design)
        cp -r "$BASE_INSTALL_PATH/standards"/* ".agent-os/standards/"
        if [[ $? -eq 0 ]]; then
            log_success "Copied standards from base installation"
        else
            log_error "Failed to copy standards from base installation"
            exit 1
        fi
    else
        # Download from repository (standalone mode)
        log_info "Downloading standards from repository..."
        
        local standard_files=("best-practices.md" "code-style.md" "tech-stack.md")
        
        if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
            standard_files+=("pocket-flow.md")
        fi
        
        for file in "${standard_files[@]}"; do
            if safe_download "$REPO_URL/standards/$file" ".agent-os/standards/$file" "$file"; then
                log_success "Downloaded: $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
        
        # Download code style subdirectory if PocketFlow is enabled
        if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
            mkdir -p ".agent-os/standards/code-style"
            local code_style_files=("fastapi-style.md" "pocketflow-style.md" "python-style.md" "testing-style.md")
            
            for file in "${code_style_files[@]}"; do
                if safe_download "$REPO_URL/standards/code-style/$file" ".agent-os/standards/code-style/$file" "standards/code-style/$file"; then
                    log_success "Downloaded: standards/code-style/$file"
                else
                    log_warning "Failed to download: standards/code-style/$file"
                fi
            done
        fi
    fi
}

# Install PocketFlow tools
install_pocketflow_tools() {
    if [[ "$ENABLE_POCKETFLOW" != "true" ]]; then
        log_info "Skipping PocketFlow tools (--no-pocketflow specified)"
        return 0
    fi
    
    log_info "Installing PocketFlow tools..."
    
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/pocketflow-tools" ]]; then
        # Copy PocketFlow tools from base installation (v1.4.0 self-contained design)
        cp -r "$BASE_INSTALL_PATH/pocketflow-tools"/* ".agent-os/pocketflow-tools/"
        if [[ $? -eq 0 ]]; then
            log_success "Copied PocketFlow tools from base installation"
        else
            log_error "Failed to copy PocketFlow tools from base installation"
            exit 1
        fi
    else
        # Download from repository (standalone mode)
        log_info "Downloading PocketFlow tools from repository..."
        
        local tool_files=(
            "generator.py"
            "pattern_analyzer.py"
            "template_validator.py"
            "dependency_orchestrator.py"
            "agent_coordination.py"
            "workflow_graph_generator.py"
            "generate-example.sh"
        )
        
        for file in "${tool_files[@]}"; do
            if safe_download "$REPO_URL/pocketflow-tools/$file" ".agent-os/pocketflow-tools/$file" "$file"; then
                chmod +x ".agent-os/pocketflow-tools/$file"
                log_success "Downloaded: $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
    fi
    
    # Create Python __init__.py
    echo "# PocketFlow Tools Package" > ".agent-os/pocketflow-tools/__init__.py"
    
    # Install templates
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/templates" ]]; then
        if safe_copy "$BASE_INSTALL_PATH/templates"/* ".agent-os/templates/" "templates"; then
            log_success "Copied templates from base installation"
        else
            log_warning "Failed to copy templates from base installation"
        fi
    else
        # Create basic template structure
        mkdir -p ".agent-os/templates/pocketflow"
        echo "# PocketFlow Templates" > ".agent-os/templates/README.md"
        log_info "Created basic template structure"
    fi
}

# Install Claude Code integration (Agent OS v1.4.0 compliant)
install_claude_code_integration() {
    if [[ "$ENABLE_CLAUDE_CODE" != "true" ]]; then
        log_info "Skipping Claude Code integration (not enabled)"
        return 0
    fi
    
    log_info "Installing Claude Code integration..."
    
    # Copy command files from instructions (v1.4.0 self-contained design)
    local instruction_files=(
        "analyze-product"
        "create-spec"
        "execute-task"
        "execute-tasks"
        "plan-product"
        "post-execution-tasks"
    )
    
    for cmd in "${instruction_files[@]}"; do
        if [[ -f ".agent-os/instructions/core/$cmd.md" ]]; then
            if safe_copy ".agent-os/instructions/core/$cmd.md" ".claude/commands/$cmd.md" "Claude Code command $cmd.md"; then
                log_success "Created Claude Code command: $cmd.md"
            else
                log_warning "Failed to create Claude Code command: $cmd.md"
            fi
        else
            log_warning "Instruction file not found: $cmd.md"
        fi
    done
    
    # Install Claude Code agents from base installation or repository
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/claude-code/agents" ]]; then
        if safe_copy "$BASE_INSTALL_PATH/claude-code/agents"/* ".claude/agents/" "Claude Code agents"; then
            log_success "Copied Claude Code agents from base installation"
        else
            log_warning "Failed to copy Claude Code agents from base installation"
        fi
    else
        # Download basic agents from repository
        local agent_files=(
            "context-fetcher.md"
            "date-checker.md"
            "file-creator.md"
            "test-runner.md"
        )
        
        if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
            agent_files+=(
                "pocketflow-orchestrator.md"
                "pattern-recognizer.md"
                "template-validator.md"
                "dependency-orchestrator.md"
            )
        fi
        
        for agent in "${agent_files[@]}"; do
            if ! safe_download "$REPO_URL/claude-code/agents/$agent" ".claude/agents/$agent" "$agent"; then
                log_warning "Could not download $agent - will create minimal version"
                # Create minimal agent file
                echo "# $agent" > ".claude/agents/$agent"
                echo "This agent provides enhanced functionality. Please check the repository for the latest version." >> ".claude/agents/$agent"
            fi
        done
    fi
}


# Create project configuration
create_project_configuration() {
    log_info "Creating project configuration..."
    
    cat > ".agent-os/config.yml" << EOF
# Project-specific Agent OS + PocketFlow configuration
# Generated during project installation

version: "2.0.0"
base_agent_os_version: "1.4.0"
created: "$(date +'%Y-%m-%d')"
base_installation: "$(if [[ "$NO_BASE_INSTALL" == "false" ]]; then echo "$BASE_INSTALL_PATH"; else echo "standalone"; fi)"
project_type: "$PROJECT_TYPE"

# Tool configuration
tools:
  claude_code: $ENABLE_CLAUDE_CODE
  pocketflow: $ENABLE_POCKETFLOW

# Project paths
paths:
  instructions: ".agent-os/instructions"
  standards: ".agent-os/standards"
  pocketflow_tools: ".agent-os/pocketflow-tools"
  templates: ".agent-os/templates"
  product: ".agent-os/product"
  specs: ".agent-os/specs"

# PocketFlow configuration
pocketflow:
  enabled: $ENABLE_POCKETFLOW
  orchestrator_enabled: $ENABLE_POCKETFLOW
  pattern_analyzer_enabled: $ENABLE_POCKETFLOW
  template_validator_enabled: $ENABLE_POCKETFLOW
  dependency_orchestrator_enabled: $ENABLE_POCKETFLOW

# Framework identification
framework:
  name: "Agent OS + PocketFlow"
  description: "Enhanced Agent OS with PocketFlow LLM workflow capabilities"
  installation_mode: "$(if [[ "$NO_BASE_INSTALL" == "false" ]]; then echo "base-linked"; else echo "standalone"; fi)"
EOF
    
    log_success "Project configuration created"
}

# Update .gitignore
update_gitignore() {
    if [[ -f ".gitignore" ]]; then
        if ! grep -q ".agent-os/pocketflow-tools/__pycache__" .gitignore 2>/dev/null; then
            echo "" >> .gitignore
            echo "# Agent OS + PocketFlow" >> .gitignore
            echo ".agent-os/pocketflow-tools/__pycache__/" >> .gitignore
            echo ".agent-os/pocketflow-tools/*.pyc" >> .gitignore
            echo ".agent-os/product/*.tmp" >> .gitignore
            echo ".agent-os/specs/*.tmp" >> .gitignore
            log_success "Updated .gitignore"
        fi
    else
        # Create .gitignore if it doesn't exist
        cat > .gitignore << EOF
# Agent OS + PocketFlow
.agent-os/pocketflow-tools/__pycache__/
.agent-os/pocketflow-tools/*.pyc
.agent-os/product/*.tmp
.agent-os/specs/*.tmp

# IDE specific
.vscode/
.idea/

# OS specific
.DS_Store
Thumbs.db
EOF
        log_success "Created .gitignore"
    fi
}

# Validate project installation
validate_installation() {
    log_info "Validating project installation..."
    
    local validation_failed=false
    
    # Check core directories
    local required_dirs=(
        ".agent-os/instructions"
        ".agent-os/standards"
    )
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        required_dirs+=(
            ".agent-os/pocketflow-tools"
            ".agent-os/templates"
        )
    fi
    
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        required_dirs+=(
            ".claude/commands"
            ".claude/agents"
        )
    fi
    
    
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            log_error "Missing directory: $dir"
            validation_failed=true
        fi
    done
    
    # Check critical files
    local required_files=(
        ".agent-os/config.yml"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Missing file: $file"
            validation_failed=true
        fi
    done
    
    if [[ "$validation_failed" == "true" ]]; then
        log_error "Installation validation failed"
        exit 1
    fi
    
    log_success "Installation validation passed"
}

# Display completion message
show_completion_message() {
    echo ""
    echo -e "${GREEN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                🎉 Project Setup Complete! 🎉                ║
║              Enhanced Agent OS + PocketFlow                  ║
║                     Ready to Use                             ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    log_highlight "Project Type: $PROJECT_TYPE"
    log_highlight "Installation Mode: $(if [[ "$NO_BASE_INSTALL" == "false" ]]; then echo "Base-linked ($BASE_INSTALL_PATH)"; else echo "Standalone"; fi)"
    echo ""
    
    log_info "Available Commands:"
    echo "  /plan-product     - Start planning a new product"
    echo "  /analyze-product  - Analyze existing product"
    echo "  /create-spec      - Create feature specifications"
    echo "  /execute-tasks    - Implement features"
    echo ""
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        log_info "PocketFlow Features Available:"
        echo "  • Workflow generators in .agent-os/pocketflow-tools/"
        echo "  • Pattern analyzers and validators"
        echo "  • Enhanced LLM workflow capabilities"
        echo "  • Template validation tools"
        echo ""
    fi
    
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        log_info "Claude Code Integration:"
        echo "  • Commands available in .claude/commands/"
        echo "  • Enhanced agents in .claude/agents/"
        echo ""
    fi
    
    
    echo "📖 Documentation: https://github.com/pickleton89/agent-os-pocketflow"
    echo "🚀 Start with: /plan-product"
    echo ""
}

# Main execution
main() {
    show_header
    parse_arguments "$@"
    
    log_info "Starting Enhanced Agent OS + PocketFlow project installation..."
    log_info "Project Type: $PROJECT_TYPE"
    log_info "Claude Code: $(if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then echo "Enabled"; else echo "Disabled"; fi)"
    log_info "PocketFlow: $(if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then echo "Enabled"; else echo "Disabled"; fi)"
    echo ""
    
    check_prerequisites
    validate_base_installation
    check_existing_installation
    create_project_structure
    install_instructions
    install_standards
    install_pocketflow_tools
    install_claude_code_integration
    create_project_configuration
    update_gitignore
    validate_installation
    show_completion_message
    
    log_success "Enhanced Agent OS + PocketFlow project installation completed successfully!"
}

# Run main function with all arguments
main "$@"