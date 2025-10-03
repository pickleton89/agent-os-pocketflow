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
SCRIPT_VERSION="2.1.0" 
AGENT_OS_COMPATIBILITY="1.4.1"
REPO_URL="https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main"

# Installation options (can be set via command line arguments)
BASE_INSTALL_PATH=""
ENABLE_POCKETFLOW=true
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
    
    # Standard Agent OS only (no PocketFlow)
    $0 --no-pocketflow
    
    # Standalone installation (no base required)
    $0 --no-base
    
    # Custom project type
    $0 --project-type python-pocketflow

NOTES:
    • Run this script from your project's root directory
    • If no base installation is found, --no-base mode will be used automatically
    • PocketFlow features include workflow generators, pattern analyzers, and validators
    • Claude Code integration is handled by base installation (run base setup first)

EOF
}

# Auto-detect base installation path
detect_base_installation() {
    if [[ -n "$BASE_INSTALL_PATH" ]]; then
        # Use provided path
        BASE_INSTALL_PATH="${BASE_INSTALL_PATH/#\~/$HOME}"
        return 0
    fi
    
    # Common installation locations (prioritize actual base installations)
    local common_paths=(
        "$HOME/.agent-os"
        "/usr/local/agent-os"
        "$(pwd)/../.agent-os"
    )
    
    # First check standard base installation locations
    for path in "${common_paths[@]}"; do
        if [[ -f "$path/config.yml" ]] && [[ -d "$path/commands" ]]; then
            BASE_INSTALL_PATH="$path"
            log_info "Found base installation: $BASE_INSTALL_PATH"
            return 0
        fi
    done
    
    # Fallback: try to detect from script location (framework location)
    local script_dir="$(dirname "$(dirname "$(realpath "$0")")" 2>/dev/null || echo "")"
    if [[ -f "$script_dir/config.yml" ]]; then
        BASE_INSTALL_PATH="$script_dir"
        log_info "Detected framework installation: $BASE_INSTALL_PATH (commands will be copied from framework source)"
        return 0
    fi
    
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
            "$BASE_INSTALL_PATH/framework-tools"
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
            ".agent-os/framework-tools"
            ".agent-os/templates"
            ".agent-os/product"
            ".agent-os/specs"
            ".agent-os/recaps"
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
    
    log_info "Checking PocketFlow framework tools availability..."
    
    # Note: For project installations, we rely on the framework tools being available
    # in the system environment (installed via base setup or development environment)
    # The project itself gets generated workflow templates, not the generator tools
    
    # Check UV availability first
    if ! command -v uv >/dev/null 2>&1; then
        log_error "UV package manager not found. Please install UV first: https://docs.astral.sh/uv/"
        exit 1
    fi
    
    if uv run python -m pocketflow_tools.cli --help >/dev/null 2>&1; then
        log_success "Framework CLI is available for workflow generation"
    else
        log_error "pocketflow_tools CLI not found or not working."
        log_info "Please ensure framework tools are installed:"
        log_info "  - Run base installation: ./setup/base.sh"  
        log_info "  - Or install in development mode: uv pip install -e . from framework root"
        exit 1
    fi
    
    # Ensure framework-tools directory exists
    mkdir -p ".agent-os/framework-tools"
    
    # Copy developer tools from base installation or framework
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/framework-tools" ]]; then
        log_info "Copying PocketFlow developer tools from base installation..."
        if safe_copy "$BASE_INSTALL_PATH/framework-tools" ".agent-os/framework-tools-temp" "framework-tools"; then
            # Move contents to target directory (including subdirectories)
            cp -r ".agent-os/framework-tools-temp"/* ".agent-os/framework-tools/" 2>/dev/null || true
            rm -rf ".agent-os/framework-tools-temp"
            log_success "Copied PocketFlow developer tools"
        else
            log_error "Failed to copy PocketFlow developer tools"
            exit 1
        fi
    else
        # Fallback: Copy from framework repository if available
        local script_realpath
        script_realpath="$(realpath "$0" 2>/dev/null)" || script_realpath="$0"
        local framework_tools_dir="$(dirname "$(dirname "$script_realpath")")/framework-tools"
        if [[ -d "$framework_tools_dir" ]]; then
            log_info "Copying PocketFlow developer tools from framework..."
            # Copy all files and subdirectories from framework
            cp -r "$framework_tools_dir"/* ".agent-os/framework-tools/" 2>/dev/null || true
            log_success "Copied PocketFlow developer tools from framework"
        else
            log_warning "PocketFlow developer tools not found - agents may have limited functionality"
        fi
    fi
    
    # Install templates
    if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/templates" ]]; then
        if safe_copy "$BASE_INSTALL_PATH/templates" ".agent-os/templates-temp" "templates"; then
            # Move contents to target directory
            cp -r ".agent-os/templates-temp"/* ".agent-os/templates/" 2>/dev/null || true
            rm -rf ".agent-os/templates-temp"
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
    
    # Install validation templates (always from framework)
    mkdir -p ".agent-os/validation"
    
    # Get framework path for validation templates
    local script_realpath
    script_realpath="$(realpath "$0" 2>/dev/null)" || script_realpath="$0"
    local framework_validation_dir="$(dirname "$(dirname "$script_realpath")")/templates/validation"
    
    if [[ -d "$framework_validation_dir" ]]; then
        log_info "Installing project validation templates from framework..."
        # Copy validation templates from framework
        cp -r "$framework_validation_dir"/* ".agent-os/validation/" 2>/dev/null || true
        
        # Make validation scripts executable
        find ".agent-os/validation" -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
        
        log_success "Installed project validation templates"
        log_info "Use: ./.agent-os/validation/test_pocketflow_integration.sh to validate project setup"
    else
        log_warning "Framework validation templates not found - skipping validation template installation"
        echo "# Validation scripts will be installed here" > ".agent-os/validation/README.md"
    fi
    
    # Initialize documentation registry
    initialize_docs_registry
}

# Initialize documentation registry
initialize_docs_registry() {
    log_info "Initializing documentation registry..."
    
    # Get framework path for registry template
    local script_realpath
    script_realpath="$(realpath "$0" 2>/dev/null)" || script_realpath="$0"
    local framework_template_dir="$(dirname "$(dirname "$script_realpath")")/templates"
    local registry_template="$framework_template_dir/docs-registry.yaml.template"
    
    # Create docs registry from template if it exists and registry doesn't exist
    if [[ -f "$registry_template" ]] && [[ ! -f ".agent-os/docs-registry.yaml" ]]; then
        # Copy template and customize it
        cp "$registry_template" ".agent-os/docs-registry.yaml"
        
        # Update the template with current date
        local current_date
        current_date="$(date +'%Y-%m-%d')"
        
        # Use sed to update the date placeholder
        if command -v sed >/dev/null 2>&1; then
            sed -i.bak "s/YYYY-MM-DD/$current_date/g" ".agent-os/docs-registry.yaml" 2>/dev/null || true
            rm -f ".agent-os/docs-registry.yaml.bak" 2>/dev/null || true
        fi
        
        log_success "Created documentation registry at .agent-os/docs-registry.yaml"
        log_info "Customize the registry by editing .agent-os/docs-registry.yaml with your tech stack and API references"
    elif [[ -f ".agent-os/docs-registry.yaml" ]]; then
        log_info "Documentation registry already exists - skipping initialization"
    else
        log_warning "Documentation registry template not found - creating basic registry"
        # Create a minimal registry if template is missing
        local current_date
        current_date="$(date +'%Y-%m-%d')"
        cat > ".agent-os/docs-registry.yaml" << EOF
# Agent OS Documentation Registry
version: 1.0.0
last_updated: $current_date

tech_stack: {}
external_apis: {}
internal_standards: {}
compliance: {}
pocketflow_patterns: {}

discovery_settings:
  auto_discover: true
  scan_paths:
    - "docs/"
    - "README.md"
    - "*.md"
    - ".agent-os/"
  include_patterns:
    - "*.md"
    - "*.yaml"
    - "*.yml"
    - "*.json"
  exclude_patterns:
    - "node_modules/"
    - ".git/"
    - ".venv/"
    - "dist/"
    - "build/"

metadata:
  created_by: "Agent OS Framework"
  framework_version: "1.4.0"
  registry_format_version: "1.0.0"
EOF
        log_info "Created basic documentation registry - customize by editing .agent-os/docs-registry.yaml"
    fi
}

# Install subfolder CLAUDE.md templates
install_subfolder_claude_md() {
    log_info "Installing subfolder CLAUDE.md templates..."

    # Get framework path for templates
    local script_realpath
    script_realpath="$(realpath "$0" 2>/dev/null)" || script_realpath="$0"
    local framework_templates_dir="$(dirname "$(dirname "$script_realpath")")/templates/claude-md"

    # Install templates if framework directory exists
    if [[ -d "$framework_templates_dir" ]]; then
        # Framework-tools CLAUDE.md
        if [[ -f "$framework_templates_dir/framework-tools.md" ]]; then
            mkdir -p ".agent-os/framework-tools"
            if safe_copy "$framework_templates_dir/framework-tools.md" ".agent-os/framework-tools/CLAUDE.md" "framework-tools CLAUDE.md"; then
                log_success "Installed framework-tools CLAUDE.md"
            else
                log_error "Failed to install framework-tools CLAUDE.md"
            fi
        fi

        # Instructions/core CLAUDE.md
        if [[ -f "$framework_templates_dir/instructions-core.md" ]]; then
            mkdir -p ".agent-os/instructions/core"
            if safe_copy "$framework_templates_dir/instructions-core.md" ".agent-os/instructions/core/CLAUDE.md" "instructions/core CLAUDE.md"; then
                log_success "Installed instructions/core CLAUDE.md"
            else
                log_error "Failed to install instructions/core CLAUDE.md"
            fi
        fi

        # Product CLAUDE.md
        if [[ -f "$framework_templates_dir/product.md" ]]; then
            mkdir -p ".agent-os/product"
            if safe_copy "$framework_templates_dir/product.md" ".agent-os/product/CLAUDE.md" "product CLAUDE.md"; then
                log_success "Installed product CLAUDE.md"
            else
                log_error "Failed to install product CLAUDE.md"
            fi
        fi

        # Standards CLAUDE.md
        if [[ -f "$framework_templates_dir/standards.md" ]]; then
            mkdir -p ".agent-os/standards"
            if safe_copy "$framework_templates_dir/standards.md" ".agent-os/standards/CLAUDE.md" "standards CLAUDE.md"; then
                log_success "Installed standards CLAUDE.md"
            else
                log_error "Failed to install standards CLAUDE.md"
            fi
        fi
    else
        log_warning "Framework CLAUDE.md templates not found - subfolder guidance will be limited"
    fi

    # Create root Claude Code guidance file
    mkdir -p ".claude"
    cat > ".claude/CLAUDE.md" <<'EOF'
# PocketFlow Project Guidance

## Platform & Language Scope
- Supported OS: macOS only (current focus)
- Language: Python 3.12 (managed with `uv`)

## Mission Overview
- .agent-os/product/mission.md

## Execution Support
- .agent-os/commands/plan-product.md
- .agent-os/instructions/core/plan-product.md
- .agent-os/instructions/core/create-spec.md

## Instruction Resolution Order
When invoking instructions, resolution occurs in this order:
1) `.agent-os/instructions/core`
2) `.agent-os/instructions`
3) `~/.agent-os/instructions/core`
4) `~/.agent-os/instructions`

Project‑local instructions take precedence over the base installation.

## Reminder
- Keep `docs/design.md` and mission artifacts updated before running automation.
EOF
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
  pocketflow: $ENABLE_POCKETFLOW

# Project paths
paths:
  instructions: ".agent-os/instructions"
  standards: ".agent-os/standards"
  pocketflow_tools: ".agent-os/framework-tools"
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
        if ! grep -q ".agent-os/framework-tools/__pycache__" .gitignore 2>/dev/null; then
            echo "" >> .gitignore
            echo "# Agent OS + PocketFlow" >> .gitignore
            echo ".agent-os/framework-tools/__pycache__/" >> .gitignore
            echo ".agent-os/framework-tools/*.pyc" >> .gitignore
            echo ".agent-os/product/*.tmp" >> .gitignore
            echo ".agent-os/specs/*.tmp" >> .gitignore
            log_success "Updated .gitignore"
        fi
    else
        # Create .gitignore if it doesn't exist
        cat > .gitignore << EOF
# Agent OS + PocketFlow
.agent-os/framework-tools/__pycache__/
.agent-os/framework-tools/*.pyc
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
            ".agent-os/framework-tools"
            ".agent-os/templates"
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
        echo "  • Workflow generators in .agent-os/framework-tools/"
        echo "  • Pattern analyzers and validators"
        echo "  • Enhanced LLM workflow capabilities"
        echo "  • Template validation tools"
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
    log_info "PocketFlow: $(if [[ "$ENABLE_POCKETFLOW" == "true" ]]; then echo "Enabled"; else echo "Disabled"; fi)"
    echo ""
    
    check_prerequisites
    validate_base_installation
    check_existing_installation
    create_project_structure
    install_instructions
    install_standards
    install_subfolder_claude_md
    install_pocketflow_tools
    create_project_configuration
    update_gitignore
    validate_installation
    show_completion_message
    
    log_success "Enhanced Agent OS + PocketFlow project installation completed successfully!"
}

# Run main function with all arguments
main "$@"
