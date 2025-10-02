#!/bin/bash
# Agent OS + PocketFlow Setup Entry Point
# Intelligent router for base installations, migrations, and project setup
# Version: 1.0.0 - Compatible with Agent OS v1.4.0

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_VERSION="1.0.0"
AGENT_OS_COMPATIBILITY="1.4.0"
REPO_URL="https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_SETUP_DIR="${SCRIPT_DIR}/setup"
NON_INTERACTIVE=false

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${PURPLE}🔧 $1${NC}"; }

# Help function
show_help() {
    echo -e "${BLUE}Agent OS + PocketFlow Setup v${SCRIPT_VERSION}${NC}"
    echo "Intelligent setup router for Agent OS v1.4.0 + PocketFlow integration"
    echo ""
    echo "USAGE:"
    echo "  $0 [OPTIONS]"
    echo ""
    echo "INSTALLATION MODES:"
    echo "  base              Install Agent OS + PocketFlow to ~/.agent-os/"
    echo "  project           Install Agent OS into current project directory"
    echo "  base-then-project Install base installation first, then project setup"
    echo "  auto              Auto-detect context and choose appropriate mode"
    echo ""
    echo "BASE INSTALLATION OPTIONS:"
    echo "  --claude-code     Enable Claude Code integration"
    echo "  --path PATH       Custom installation path (default: ~/.agent-os)"
    echo ""
    echo "PROJECT INSTALLATION OPTIONS:"
    echo "  --no-base-install Skip base installation check"
    echo "  --type TYPE       Project type (default: pocketflow-enhanced)"
    echo ""
    echo "GENERAL OPTIONS:"
    echo "  --force           Force installation even if target exists"
    echo "  --help, -h        Show this help message"
    echo "  --version, -v     Show version information"
    echo ""
    echo "EXAMPLES:"
    echo "  # Base installation with Claude Code"
    echo "  $0 base --claude-code"
    echo ""
    echo "  # Project installation (requires base installation)"
    echo "  cd /path/to/your-project && $0 project"
    echo ""
    echo "  # Auto-detect and install"
    echo "  $0 auto"
    echo ""
    echo "For more information: https://github.com/pickleton89/agent-os-pocketflow"
}

# Version information
show_version() {
    echo "Agent OS + PocketFlow Setup v${SCRIPT_VERSION}"
    echo "Compatible with Agent OS v${AGENT_OS_COMPATIBILITY}"
    echo "Repository: https://github.com/pickleton89/agent-os-pocketflow"
}

# Detection functions
detect_existing_installation() {
    local base_path="$HOME/.agent-os"
    local project_path="./.agent-os"
    
    # Check for base installation
    if [ -d "$base_path" ] && [ -f "$base_path/config.yml" ]; then
        echo "base"
        return 0
    fi
    
    
    # Check for v1.4.0 project installation
    if [ -d "$project_path" ] && [ -f "$project_path/config.yml" ]; then
        echo "project"
        return 0
    fi
    
    echo "none"
}

# Context detection
detect_context() {
    local installation=$(detect_existing_installation)
    
    case "$installation" in
        "base")
            # Base exists, probably want project installation
            if [ -f "./package.json" ] || [ -f "./pyproject.toml" ] || [ -f "./Cargo.toml" ]; then
                echo "project"
            else
                echo "base"
            fi
            ;;
        "project")
            echo "project"
            ;;
        "none")
            # No installation, check if we're in a project directory
            if [ -f "./package.json" ] || [ -f "./pyproject.toml" ] || [ -f "./Cargo.toml" ]; then
                echo "base-then-project"
            else
                echo "base"
            fi
            ;;
    esac
}

# Translate parameters for base.sh
translate_base_args() {
    local args="$@"
    local translated_args=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --path)
                translated_args="$translated_args --install-path $2"
                shift 2
                ;;
            *)
                translated_args="$translated_args $1"
                shift
                ;;
        esac
    done
    
    echo "$translated_args"
}

# Translate parameters for project.sh
translate_project_args() {
    local args="$@"
    local translated_args=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-base-install)
                translated_args="$translated_args --no-base"
                shift
                ;;
            --type)
                translated_args="$translated_args --project-type $2"
                shift 2
                ;;
            --path)
                translated_args="$translated_args --base-path $2"
                shift 2
                ;;
            *)
                translated_args="$translated_args $1"
                shift
                ;;
        esac
    done
    
    echo "$translated_args"
}

# Route to appropriate installer
route_installation() {
    local mode="$1"
    shift
    local args="$@"
    local base_script="${LOCAL_SETUP_DIR}/base.sh"
    local project_script="${LOCAL_SETUP_DIR}/project.sh"

    case "$mode" in
        "base")
            log_step "Routing to base installation..."
            local base_args=$(translate_base_args $args)
            if [[ -f "$base_script" ]]; then
                bash "$base_script" $base_args
            else
                curl -sSL "${REPO_URL}/setup/base.sh" | bash -s -- $base_args
            fi
            ;;
        "project")
            log_step "Routing to project installation..."
            local project_args=$(translate_project_args $args)
            if [ -f "$HOME/.agent-os/setup/project.sh" ]; then
                "$HOME/.agent-os/setup/project.sh" $project_args
            else
                log_warning "Base installation not found. Installing base first..."
                local base_args=$(translate_base_args $args)
                if [[ -f "$base_script" ]]; then
                    bash "$base_script" $base_args
                else
                    curl -sSL "${REPO_URL}/setup/base.sh" | bash -s -- $base_args
                fi
                log_step "Now installing project components..."
                if [ -f "$HOME/.agent-os/setup/project.sh" ]; then
                    "$HOME/.agent-os/setup/project.sh" $project_args
                elif [[ -f "$project_script" ]]; then
                    bash "$project_script" $project_args
                else
                    log_error "Project installation script not found after base install"
                    exit 1
                fi
            fi
            ;;
        "base-then-project")
            log_step "Installing base installation first..."
            local base_args=$(translate_base_args $args)
            if [[ -f "$base_script" ]]; then
                bash "$base_script" $base_args
            else
                curl -sSL "${REPO_URL}/setup/base.sh" | bash -s -- $base_args
            fi
            log_step "Now installing project components..."
            local project_args=$(translate_project_args $args)
            if [ -f "$HOME/.agent-os/setup/project.sh" ]; then
                "$HOME/.agent-os/setup/project.sh" $project_args
            elif [[ -f "$project_script" ]]; then
                bash "$project_script" $project_args
            else
                log_error "Project installation script not found after base install"
                exit 1
            fi
            ;;
        *)
            log_error "Unknown installation mode: $mode"
            show_help
            exit 1
            ;;
    esac
}

# Auto-detection with user confirmation
auto_detect_and_install() {
    local context=$(detect_context)
    local installation=$(detect_existing_installation)
    
    log_info "Auto-detecting installation context..."
    echo ""
    
    case "$context" in
        "base")
            echo -e "${CYAN}📋 Context Analysis:${NC}"
            echo "   • Working directory: $(pwd)"
            echo "   • Existing installation: $installation"
            echo "   • Recommended action: Base installation"
            echo ""
            if [[ "$NON_INTERACTIVE" == true ]]; then
                log_info "Non-interactive mode enabled; proceeding with base installation."
                route_installation "base" "$@"
            else
                read -p "Install Agent OS + PocketFlow to ~/.agent-os/? [Y/n]: " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
                    route_installation "base" "$@"
                else
                    log_info "Installation cancelled by user"
                    exit 0
                fi
            fi
            ;;
        "project")
            echo -e "${CYAN}📋 Context Analysis:${NC}"
            echo "   • Working directory: $(pwd)"
            echo "   • Existing installation: $installation"
            echo "   • Project files detected: ✓"
            echo "   • Recommended action: Project installation"
            echo ""
            if [[ "$NON_INTERACTIVE" == true ]]; then
                log_info "Non-interactive mode enabled; proceeding with project installation."
                route_installation "project" "$@"
            else
                read -p "Install Agent OS into this project? [Y/n]: " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
                    route_installation "project" "$@"
                else
                    log_info "Installation cancelled by user"
                    exit 0
                fi
            fi
            ;;
        "base-then-project")
            echo -e "${CYAN}📋 Context Analysis:${NC}"
            echo "   • Working directory: $(pwd)"
            echo "   • Existing installation: $installation"
            echo "   • Project files detected: ✓"
            echo "   • Recommended action: Base + Project installation"
            echo ""
            if [[ "$NON_INTERACTIVE" == true ]]; then
                log_info "Non-interactive mode enabled; installing base then project components."
                route_installation "base-then-project" "$@"
            else
                read -p "Install Agent OS base and project components? [Y/n]: " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
                    route_installation "base-then-project" "$@"
                else
                    log_info "Installation cancelled by user"
                    exit 0
                fi
            fi
            ;;
        *)
            log_error "Unable to determine appropriate installation mode"
            echo ""
            echo "Please specify installation mode explicitly:"
            echo "  base     - Install to ~/.agent-os/"
            echo "  project  - Install to current project"
            exit 1
            ;;
    esac
}

# Main execution
main() {
    local cleaned_args=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --non-interactive|--yes|-y)
                NON_INTERACTIVE=true
                shift
                ;;
            *)
                cleaned_args+=("$1")
                shift
                ;;
        esac
    done

    set -- "${cleaned_args[@]}"

    # Handle version and help first
    if [[ $# -gt 0 ]]; then
        case "$1" in
            --version|-v)
                show_version
                exit 0
                ;;
            --help|-h|help)
                show_help
                exit 0
                ;;
        esac
    fi
    
    echo -e "${BLUE}🚀 Agent OS + PocketFlow Setup v${SCRIPT_VERSION}${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
    
    # Parse mode
    local mode="auto"
    if [ $# -gt 0 ] && [[ ! "$1" =~ ^-- ]]; then
        mode="$1"
        shift
    fi
    
    # Execute based on mode
    case "$mode" in
        "auto")
            auto_detect_and_install "$@"
            ;;
        "base"|"project"|"base-then-project")
            route_installation "$mode" "$@"
            ;;
        *)
            log_error "Unknown mode: $mode"
            echo ""
            show_help
            exit 1
            ;;
    esac
    
    echo ""
    log_success "Setup completed successfully!"
    log_info "For more information: https://github.com/pickleton89/agent-os-pocketflow"
}

# Execute main function with all arguments
main "$@"
