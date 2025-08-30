#!/bin/bash
# Enhanced Agent OS + PocketFlow Base Installation Script
# Compatible with Agent OS v1.4.0 architecture
# Installs the framework to user's chosen location (default: ~/.agent-os)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_VERSION="2.1.0"
AGENT_OS_COMPATIBILITY="1.4.1"
REPO_URL="https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main"
DEFAULT_INSTALL_PATH="$HOME/.agent-os"

# Installation options (can be set via command line arguments)
INSTALL_PATH="$DEFAULT_INSTALL_PATH"
ENABLE_CLAUDE_CODE=true  # Default enabled for consistency with project.sh
ENABLE_POCKETFLOW=true  # Default enabled in our enhanced version
OVERWRITE_INSTRUCTIONS=false
OVERWRITE_STANDARDS=false
UPDATE_POCKETFLOW_TOOLS=false
FORCE_INSTALL=false

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_highlight() { echo -e "${PURPLE}🎯 $1${NC}"; }

# Display header
show_header() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║              Enhanced Agent OS + PocketFlow                  ║
║              Base Installation Script v2.0.0                 ║
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
            --install-path)
                INSTALL_PATH="$2"
                shift 2
                ;;
            --claude-code)
                ENABLE_CLAUDE_CODE=true
                shift
                ;;
            --no-pocketflow)
                ENABLE_POCKETFLOW=false
                shift
                ;;
            --overwrite-instructions)
                OVERWRITE_INSTRUCTIONS=true
                shift
                ;;
            --overwrite-standards)
                OVERWRITE_STANDARDS=true
                shift
                ;;
            --update-pocketflow-tools)
                UPDATE_POCKETFLOW_TOOLS=true
                shift
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
    
    # Expand tilde in install path
    INSTALL_PATH="${INSTALL_PATH/#\~/$HOME}"
}

# Show help
show_help() {
    cat << EOF

Enhanced Agent OS + PocketFlow Base Installation

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --install-path PATH      Install to custom path (default: ~/.agent-os)
    --claude-code           Enable Claude Code integration
    --no-pocketflow         Disable PocketFlow enhancements (standard Agent OS only)
    --overwrite-instructions Overwrite existing instructions directory
    --overwrite-standards   Overwrite existing standards directory
    --update-pocketflow-tools Update PocketFlow tools to latest version
    --force                 Force installation even if directory exists
    --help                  Show this help message

EXAMPLES:
    # Basic enhanced Agent OS installation
    $0
    
    # With Claude Code support
    $0 --claude-code
    
    # With Claude Code support
    $0 --claude-code
    
    # Custom installation path
    $0 --install-path ~/my-agent-os --claude-code
    
    # Standard Agent OS only (no PocketFlow)
    $0 --no-pocketflow --claude-code
    
    # Update instructions only
    $0 --overwrite-instructions --claude-code
    
    # Update standards only
    $0 --overwrite-standards --claude-code
    
    # Update PocketFlow tools only
    $0 --update-pocketflow-tools

EOF
}

# Get script directory with fallback for systems without realpath
get_script_dir() {
    if command -v realpath &> /dev/null; then
        dirname "$(realpath "$0")"
    else
        # Fallback for systems without realpath
        cd "$(dirname "$0")" && pwd
    fi
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check for required tools
    local required_tools=("curl" "git" "python3" "mkdir" "cp" "chmod")
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
    
    # Check Python version (require 3.8+)
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
        if [[ "$(printf '%s\n' "3.8" "$python_version" | sort -V | head -n1)" != "3.8" ]]; then
            log_error "Python 3.8+ required. Found: $python_version"
            exit 1
        fi
        log_success "Python version check passed: $python_version"
    fi
    
    log_success "All prerequisites satisfied"
}

# Check existing installation
check_existing_installation() {
    if [[ -d "$INSTALL_PATH" ]]; then
        if [[ "$FORCE_INSTALL" == "true" ]]; then
            log_warning "Existing installation found at $INSTALL_PATH - will overwrite (--force enabled)"
        else
            log_warning "Existing installation found at $INSTALL_PATH"
            echo "Options:"
            echo "  1. Use --force to overwrite completely"
            echo "  2. Use --overwrite-instructions to update instructions only"
            echo "  3. Use --install-path to choose different location"
            echo "  4. Backup and remove existing installation manually"
            exit 1
        fi
    fi
}

# Create directory structure
create_directory_structure() {
    log_info "Creating directory structure..."
    
    # Core Agent OS directories (v1.4.0 compatible)
    local core_dirs=(
        "$INSTALL_PATH"
        "$INSTALL_PATH/instructions"
        "$INSTALL_PATH/standards"
        "$INSTALL_PATH/shared"
        "$INSTALL_PATH/commands"
        "$INSTALL_PATH/setup"
        "$INSTALL_PATH/recaps"
    )
    
    # PocketFlow enhancement directories
    local pocketflow_dirs=(
        "$INSTALL_PATH/pocketflow-tools"
        "$INSTALL_PATH/templates"
    )
    
    # Claude Code directories (only agents, commands are in base commands/ directory)
    local ide_dirs=(
        "$INSTALL_PATH/claude-code/agents"
    )
    
    # Create core directories
    for dir in "${core_dirs[@]}"; do
        mkdir -p "$dir"
        log_success "Created: $dir"
    done
    
    # Create PocketFlow directories if enabled
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        for dir in "${pocketflow_dirs[@]}"; do
            mkdir -p "$dir"
            log_success "Created: $dir"
        done
    fi
    
    # Create IDE directories if needed
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        for dir in "${ide_dirs[@]}"; do
            mkdir -p "$dir"
            log_success "Created: $dir"
        done
    fi
}

# Install base Agent OS instructions
install_instructions() {
    log_info "Installing enhanced instructions..."
    
    local source_dir="$(dirname "$(dirname "$(realpath "$0")")")/instructions"
    
    if [[ -d "$source_dir" ]]; then
        # Install from local source (development mode)
        log_info "Installing from local source: $source_dir"
        cp -r "$source_dir"/* "$INSTALL_PATH/instructions/"
        log_success "Copied local instructions to $INSTALL_PATH/instructions/"
    else
        # Download from repository
        log_info "Downloading instructions from repository..."
        
        # Create subdirectories first
        mkdir -p "$INSTALL_PATH/instructions/core"
        mkdir -p "$INSTALL_PATH/instructions/meta"
        
        local instruction_files=("analyze-product.md" "create-spec.md" "execute-task.md" "execute-tasks.md" "plan-product.md" "post-execution-tasks.md")
        
        for file in "${instruction_files[@]}"; do
            local target_file="$INSTALL_PATH/instructions/core/$file"
            local file_existed=false
            
            # Check if file exists before download
            if [[ -f "$target_file" ]]; then
                file_existed=true
                if [[ "$OVERWRITE_INSTRUCTIONS" != "true" ]]; then
                    log_info "Preserved existing: $file"
                    continue
                fi
            fi
            
            curl -s -o "$target_file" "$REPO_URL/instructions/core/$file"
            if [[ $? -eq 0 ]]; then
                log_success "$(if [[ "$file_existed" == "true" ]]; then echo "Updated"; else echo "Downloaded"; fi): $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
        
        # Download meta instructions
        curl -s -o "$INSTALL_PATH/instructions/meta/pre-flight.md" "$REPO_URL/instructions/meta/pre-flight.md"
        if [[ $? -eq 0 ]]; then
            log_success "Downloaded: pre-flight.md"
        else
            log_warning "Failed to download pre-flight.md (optional)"
        fi
    fi
}

# Install enhanced standards
install_standards() {
    log_info "Installing enhanced standards..."
    
    local source_dir="$(dirname "$(dirname "$(realpath "$0")")")/standards"
    
    if [[ -d "$source_dir" ]]; then
        # Install from local source
        cp -r "$source_dir"/* "$INSTALL_PATH/standards/"
        log_success "Copied local standards to $INSTALL_PATH/standards/"
    else
        # Download from repository
        log_info "Downloading standards from repository..."
        local standard_files=("best-practices.md" "code-style.md" "pocket-flow.md" "tech-stack.md")
        
        for file in "${standard_files[@]}"; do
            local target_file="$INSTALL_PATH/standards/$file"
            local file_existed=false
            
            # Check if file exists before download
            if [[ -f "$target_file" ]]; then
                file_existed=true
                if [[ "$OVERWRITE_STANDARDS" != "true" ]]; then
                    log_info "Preserved existing: $file"
                    continue
                fi
            fi
            
            curl -s -o "$target_file" "$REPO_URL/standards/$file"
            if [[ $? -eq 0 ]]; then
                log_success "$(if [[ "$file_existed" == "true" ]]; then echo "Updated"; else echo "Downloaded"; fi): $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
        
        # Download code style subdirectory
        mkdir -p "$INSTALL_PATH/standards/code-style"
        local code_style_files=("fastapi-style.md" "pocketflow-style.md" "python-style.md" "testing-style.md")
        
        for file in "${code_style_files[@]}"; do
            local target_file="$INSTALL_PATH/standards/code-style/$file"
            local file_existed=false
            
            # Check if file exists before download
            if [[ -f "$target_file" ]]; then
                file_existed=true
                if [[ "$OVERWRITE_STANDARDS" != "true" ]]; then
                    log_info "Preserved existing: standards/code-style/$file"
                    continue
                fi
            fi
            
            curl -s -o "$target_file" "$REPO_URL/standards/code-style/$file"
            if [[ $? -eq 0 ]]; then
                log_success "$(if [[ "$file_existed" == "true" ]]; then echo "Updated"; else echo "Downloaded"; fi): standards/code-style/$file"
            else
                log_error "Failed to download: standards/code-style/$file"
                exit 1
            fi
        done
    fi
}

# Install shared utilities
install_shared() {
    log_info "Installing shared utilities..."
    
    local source_dir="$(dirname "$(dirname "$(realpath "$0")")")/shared"
    
    if [[ -d "$source_dir" ]]; then
        # Install from local source
        cp -r "$source_dir"/* "$INSTALL_PATH/shared/"
        log_success "Copied local shared utilities to $INSTALL_PATH/shared/"
    else
        # Download from repository
        log_info "Downloading shared utilities from repository..."
        local shared_files=("execution_utils.md")
        
        for file in "${shared_files[@]}"; do
            local target_file="$INSTALL_PATH/shared/$file"
            
            curl -s -o "$target_file" "$REPO_URL/shared/$file"
            if [[ $? -eq 0 ]]; then
                log_success "Downloaded: $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
    fi
}

# Install commands directory (Agent OS v1.4.0 requirement)
install_commands() {
    log_info "Installing commands..."
    
    # Create commands based on instructions (original Agent OS v1.4.0 behavior)
    local instructions_dir="$INSTALL_PATH/instructions"
    local commands_dir="$INSTALL_PATH/commands"
    
    if [[ -d "$instructions_dir" ]]; then
        local instruction_files=(
            "analyze-product"
            "create-spec"
            "execute-task"
            "execute-tasks"
            "plan-product"
        )
        
        for cmd in "${instruction_files[@]}"; do
            local source_file=""
            
            # Look for instruction file in core/ subdirectory first, then fallback
            if [[ -f "$instructions_dir/core/$cmd.md" ]]; then
                source_file="$instructions_dir/core/$cmd.md"
            elif [[ -f "$instructions_dir/$cmd.md" ]]; then
                source_file="$instructions_dir/$cmd.md"
            fi
            
            if [[ -n "$source_file" ]] && [[ ! -f "$commands_dir/$cmd.md" || "$OVERWRITE_INSTRUCTIONS" == "true" ]]; then
                cp "$source_file" "$commands_dir/$cmd.md"
                log_success "Installed command: $cmd.md"
            elif [[ -f "$commands_dir/$cmd.md" ]]; then
                log_info "Preserved existing command: $cmd.md"
            else
                log_warning "Command source not found: $cmd.md"
            fi
        done
    else
        log_warning "Instructions directory not found - cannot create commands"
    fi
}


# Install PocketFlow tools
install_pocketflow_tools() {
    if [[ "$ENABLE_POCKETFLOW" != "true" ]] && [[ "$UPDATE_POCKETFLOW_TOOLS" != "true" ]]; then
        log_info "Skipping PocketFlow tools (--no-pocketflow specified)"
        return 0
    fi
    
    if [[ "$UPDATE_POCKETFLOW_TOOLS" == "true" ]]; then
        log_info "Updating PocketFlow tools..."
    else
        log_info "Installing PocketFlow tools..."
    fi
    
    local source_dir="$(dirname "$(dirname "$(realpath "$0")")")/pocketflow-tools"
    
    if [[ -d "$source_dir" ]]; then
        # Install from local source
        cp -r "$source_dir"/* "$INSTALL_PATH/pocketflow-tools/"
        chmod +x "$INSTALL_PATH/pocketflow-tools"/*.py
        chmod +x "$INSTALL_PATH/pocketflow-tools"/*.sh
        log_success "Copied PocketFlow tools to $INSTALL_PATH/pocketflow-tools/"
    else
        # Download from repository
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
            curl -s -o "$INSTALL_PATH/pocketflow-tools/$file" "$REPO_URL/pocketflow-tools/$file"
            if [[ $? -eq 0 ]]; then
                chmod +x "$INSTALL_PATH/pocketflow-tools/$file"
                log_success "Downloaded: $file"
            else
                log_error "Failed to download: $file"
                exit 1
            fi
        done
    fi
    
    # Create Python __init__.py
    echo "# PocketFlow Tools Package" > "$INSTALL_PATH/pocketflow-tools/__init__.py"
    
    # Install templates if available
    local templates_source_dir="$(dirname "$(dirname "$(realpath "$0")")")/templates"
    if [[ -d "$templates_source_dir" ]]; then
        cp -r "$templates_source_dir"/* "$INSTALL_PATH/templates/"
        log_success "Copied templates to $INSTALL_PATH/templates/"
    else
        # Create basic template structure
        mkdir -p "$INSTALL_PATH/templates/pocketflow"
        echo "# PocketFlow Templates" > "$INSTALL_PATH/templates/README.md"
        log_info "Created basic template structure"
    fi
}

# Create configuration file
create_configuration() {
    log_info "Creating configuration file..."
    
    local config_file="$INSTALL_PATH/config.yml"
    local source_config="$(dirname "$(dirname "$(realpath "$0")")")/config.yml"
    
    if [[ -f "$source_config" ]]; then
        # Copy and customize from local source
        cp "$source_config" "$config_file"
        
        # Update configuration with user settings
        sed -i.bak "s/claude_code: .*/claude_code: $ENABLE_CLAUDE_CODE/g" "$config_file"
        sed -i.bak "s/pocketflow: .*/pocketflow: $ENABLE_POCKETFLOW/g" "$config_file"
        sed -i.bak "s|base_installation: \".*\"|base_installation: \"$INSTALL_PATH\"|g" "$config_file"
        rm -f "$config_file.bak"
        log_success "Updated configuration with user settings"
    else
        # Create configuration from template
        cat > "$config_file" << EOF
# Agent OS + PocketFlow Enhanced Configuration
# This configuration was generated during base installation

version: "2.0.0"
base_agent_os_version: "1.4.0"
created: "$(date +'%Y-%m-%d')"
updated: "$(date +'%Y-%m-%d')"

# Tool configuration
tools:
  claude_code: $ENABLE_CLAUDE_CODE
  pocketflow: $ENABLE_POCKETFLOW

# PocketFlow-specific configuration
pocketflow:
  generator_path: "$INSTALL_PATH/pocketflow-tools/generator.py"
  templates_path: "$INSTALL_PATH/templates/"
  orchestrator_enabled: $ENABLE_POCKETFLOW
  pattern_analyzer_enabled: $ENABLE_POCKETFLOW
  dependency_orchestrator_enabled: $ENABLE_POCKETFLOW
  template_validator_enabled: $ENABLE_POCKETFLOW

# Installation paths
paths:
  base_installation: "$INSTALL_PATH"
  instructions: "$INSTALL_PATH/instructions"
  standards: "$INSTALL_PATH/standards"
  pocketflow_tools: "$INSTALL_PATH/pocketflow-tools"
  templates: "$INSTALL_PATH/templates"
  commands: "$INSTALL_PATH/commands"
  claude_code_agents: "$INSTALL_PATH/claude-code/agents"

# Framework identification
framework:
  name: "Agent OS + PocketFlow"
  description: "Enhanced Agent OS with PocketFlow LLM workflow capabilities"
  repository: "https://github.com/pickleton89/agent-os-pocketflow"
  
# Compatibility and feature flags
compatibility:
  agent_os_v1_4: true
  backward_compatible: true
  self_contained_projects: true
  
features:
  enhanced_instructions: true
  pocketflow_generators: $ENABLE_POCKETFLOW
  pattern_analysis: $ENABLE_POCKETFLOW
  template_validation: $ENABLE_POCKETFLOW
  dependency_orchestration: $ENABLE_POCKETFLOW
  claude_code_integration: $ENABLE_CLAUDE_CODE
EOF
    fi
    
    log_success "Configuration file created: $config_file"
}

# Generate project installation script
generate_project_script() {
    log_info "Generating project installation script..."
    
    local project_script="$INSTALL_PATH/setup/project.sh"
    local update_script="$INSTALL_PATH/setup/update-project.sh"
    
    cat > "$project_script" << 'EOF'
#!/bin/bash
# Enhanced Agent OS + PocketFlow Project Installation Script
# This script installs Agent OS into individual project directories

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Get base installation path
BASE_INSTALL_PATH="$(dirname "$(dirname "$(realpath "$0")")")"

# Options
ENABLE_POCKETFLOW=true
ENABLE_CLAUDE_CODE=false

# Parse arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --pocketflow)
                ENABLE_POCKETFLOW=true
                shift
                ;;
            --no-pocketflow)
                ENABLE_POCKETFLOW=false
                shift
                ;;
            --claude-code)
                ENABLE_CLAUDE_CODE=true
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

show_help() {
    cat << HELP_EOF

Enhanced Agent OS + PocketFlow Project Installation

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --pocketflow            Enable PocketFlow features (default)
    --no-pocketflow         Disable PocketFlow features
    --claude-code           Enable Claude Code integration
    --help                  Show this help message

EXAMPLES:
    # Basic project installation with PocketFlow
    $0
    
    # With Claude Code support
    $0 --claude-code
    
    # Standard Agent OS only
    $0 --no-pocketflow

HELP_EOF
}

# Main installation function
install_project() {
    log_info "Installing Agent OS into current project..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_warning "Not in a git repository. Installing anyway..."
    fi
    
    # Create project directories
    local project_dirs=(
        ".agent-os"
        ".agent-os/instructions"
        ".agent-os/standards"
    )
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        project_dirs+=(
            ".agent-os/pocketflow-tools"
            ".agent-os/templates"
        )
    fi
    
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        project_dirs+=(
            ".claude/commands"
            ".claude/agents"
        )
    fi
    
    # Create directories
    for dir in "${project_dirs[@]}"; do
        mkdir -p "$dir"
        log_success "Created: $dir"
    done
    
    # Copy instructions
    if [[ -d "$BASE_INSTALL_PATH/instructions" ]]; then
        cp -r "$BASE_INSTALL_PATH/instructions"/* ".agent-os/instructions/"
        log_success "Copied instructions from base installation"
    else
        log_error "Base installation instructions not found at $BASE_INSTALL_PATH/instructions"
        exit 1
    fi
    
    # Copy standards
    if [[ -d "$BASE_INSTALL_PATH/standards" ]]; then
        cp -r "$BASE_INSTALL_PATH/standards"/* ".agent-os/standards/"
        log_success "Copied standards from base installation"
    else
        log_error "Base installation standards not found at $BASE_INSTALL_PATH/standards"
        exit 1
    fi
    
    # Copy PocketFlow tools if enabled
    if [[ "$ENABLE_POCKETFLOW" == "true" ]] && [[ -d "$BASE_INSTALL_PATH/pocketflow-tools" ]]; then
        cp -r "$BASE_INSTALL_PATH/pocketflow-tools"/* ".agent-os/pocketflow-tools/"
        log_success "Copied PocketFlow tools from base installation"
    fi
    
    # Copy Claude Code files if enabled
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        # Copy commands from base commands directory (Agent OS v1.4.0 architecture)
        if [[ -d "$BASE_INSTALL_PATH/commands" ]]; then
            cp -r "$BASE_INSTALL_PATH/commands"/* ".claude/commands/"
            log_success "Copied Claude Code commands"
        fi
        
        if [[ -d "$BASE_INSTALL_PATH/claude-code/agents" ]]; then
            cp -r "$BASE_INSTALL_PATH/claude-code/agents"/* ".claude/agents/"
            log_success "Copied Claude Code agents"
        fi
    fi
    
    # Create project-specific config
    cat > ".agent-os/config.yml" << CONFIG_EOF
# Project-specific Agent OS configuration
version: "2.0.0"
base_installation: "$BASE_INSTALL_PATH"
project_type: "$(if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then echo "pocketflow-enhanced"; else echo "standard-agent-os"; fi)"
created: "$(date +'%Y-%m-%d')"

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
CONFIG_EOF
    
    log_success "Project configuration created"
    
    # Create .gitignore entries
    if [[ -f ".gitignore" ]]; then
        if ! grep -q ".agent-os/pocketflow-tools/__pycache__" .gitignore 2>/dev/null; then
            echo -e "\n# Agent OS + PocketFlow" >> .gitignore
            echo ".agent-os/pocketflow-tools/__pycache__/" >> .gitignore
            echo ".agent-os/pocketflow-tools/*.pyc" >> .gitignore
            log_success "Updated .gitignore"
        fi
    fi
    
    log_success "Project installation complete!"
    
    # Display next steps
    echo ""
    log_info "Next steps:"
    echo "  • Use /plan-product to start a new project"
    echo "  • Use /analyze-product for existing projects" 
    echo "  • Use /create-spec to create new features"
    echo "  • Use /execute-tasks to implement features"
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        echo ""
        log_info "PocketFlow features available:"
        echo "  • Workflow generators in .agent-os/pocketflow-tools/"
        echo "  • Pattern analyzers and validators"
        echo "  • Enhanced LLM workflow capabilities"
    fi
}

# Parse arguments and run installation
parse_arguments "$@"
install_project
EOF
    
    chmod +x "$project_script"
    log_success "Project installation script created: $project_script"
    
    # Copy update-project.sh script
    local source_update_script="$(get_script_dir)/update-project.sh"
    if [[ -f "$source_update_script" ]]; then
        cp "$source_update_script" "$update_script"
        chmod +x "$update_script"
        log_success "Project update script created: $update_script"
    else
        log_warning "Update script not found in source, creating minimal version"
        echo "#!/bin/bash" > "$update_script"
        echo "echo 'Update script not available in this installation'" >> "$update_script"
        chmod +x "$update_script"
    fi
}

# Install Claude Code integration
install_claude_code_integration() {
    if [[ "$ENABLE_CLAUDE_CODE" != "true" ]]; then
        log_info "Skipping Claude Code integration (not enabled)"
        return 0
    fi
    
    log_info "Installing Claude Code integration..."
    
    # Install Claude Code agents (commands are handled by install_commands function)
    local agents_dir="$INSTALL_PATH/claude-code/agents"
    local source_agents_dir="$(dirname "$(dirname "$(realpath "$0")")")/claude-code/agents"
    
    if [[ -d "$source_agents_dir" ]]; then
        cp -r "$source_agents_dir"/* "$agents_dir/"
        log_success "Copied Claude Code agents"
    else
        # Download agents from repository
        local agent_files=(
            "context-fetcher.md"
            "date-checker.md"
            "file-creator.md"
            "test-runner.md"
            "project-manager.md"
            "git-workflow.md"
        )
        
        for agent in "${agent_files[@]}"; do
            curl -s -o "$agents_dir/$agent" "$REPO_URL/claude-code/agents/$agent"
            if [[ $? -eq 0 ]]; then
                log_success "Downloaded Claude Code agent: $agent"
            else
                log_error "Failed to download agent: $agent"
            fi
        done
    fi
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]] && [[ ! -d "$source_agents_dir" ]]; then
        # Add PocketFlow-specific agents (only if not copied locally)
        local pocketflow_agents=(
            "design-document-creator.md"
            "strategic-planner.md"
            "pattern-recognizer.md"
            "template-validator.md"
            "dependency-orchestrator.md"
        )
        
        for agent in "${pocketflow_agents[@]}"; do
            curl -s -o "$agents_dir/$agent" "$REPO_URL/claude-code/agents/$agent" || {
                log_warning "Could not download $agent - will be created during project setup"
            }
        done
    fi
}

# Run installation validation
validate_installation() {
    log_info "Validating installation..."
    
    local validation_failed=false
    
    # Check core directories
    local required_dirs=(
        "$INSTALL_PATH/instructions"
        "$INSTALL_PATH/standards" 
        "$INSTALL_PATH/setup"
    )
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        required_dirs+=(
            "$INSTALL_PATH/pocketflow-tools"
            "$INSTALL_PATH/templates"
        )
    fi
    
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        required_dirs+=(
            "$INSTALL_PATH/claude-code/agents"
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
        "$INSTALL_PATH/config.yml"
        "$INSTALL_PATH/setup/project.sh"
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
║                🎉 Installation Complete! 🎉                 ║
║              Enhanced Agent OS + PocketFlow                  ║
║                     Ready to Use                             ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    log_highlight "Base installation location: $INSTALL_PATH"
    echo ""
    log_info "Next Steps:"
    echo ""
    echo "1. Install into a project:"
    echo "   cd /path/to/your/project"
    echo "   $INSTALL_PATH/setup/project.sh"
    echo ""
    
    if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then
        echo "2. For Claude Code projects, also add:"
        echo "   $INSTALL_PATH/setup/project.sh --claude-code"
        echo ""
    fi
    
    if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then
        echo "3. PocketFlow features include:"
        echo "   • Advanced workflow generators"
        echo "   • Pattern analysis and validation"
        echo "   • LLM-enhanced development workflows"
        echo ""
    fi
    
    echo "4. Usage Commands:"
    echo "   /plan-product     - Start planning a new product"
    echo "   /analyze-product  - Analyze existing product"
    echo "   /create-spec      - Create feature specifications"  
    echo "   /execute-tasks    - Implement features"
    echo ""
    echo "5. Update Commands:"
    echo "   $INSTALL_PATH/setup/update-project.sh --update-all"
    echo "   $INSTALL_PATH/setup/base.sh --overwrite-instructions"
    echo "   $INSTALL_PATH/setup/base.sh --overwrite-standards"
    echo ""
    echo "📖 Documentation: https://github.com/pickleton89/agent-os-pocketflow"
    echo ""
}

# Main execution
main() {
    show_header
    parse_arguments "$@"
    
    log_info "Starting Enhanced Agent OS + PocketFlow installation..."
    log_info "Installation path: $INSTALL_PATH"
    log_info "Claude Code: $(if [[ "$ENABLE_CLAUDE_CODE" == "true" ]]; then echo "Enabled"; else echo "Disabled"; fi)"
    log_info "PocketFlow: $(if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then echo "Enabled"; else echo "Disabled"; fi)"
    echo ""
    
    check_prerequisites
    check_existing_installation
    create_directory_structure
    install_instructions
    install_standards
    install_shared
    install_commands
    install_pocketflow_tools
    create_configuration
    generate_project_script
    install_claude_code_integration
    validate_installation
    show_completion_message
    
    log_success "Enhanced Agent OS + PocketFlow installation completed successfully!"
}

# Run main function with all arguments
main "$@"
