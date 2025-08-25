#!/bin/bash
# Agent OS + PocketFlow Project Update Script
# Updates existing project installations with latest base installation content
# Compatible with Agent OS v1.4.0 architecture

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_VERSION="1.0.0"
AGENT_OS_COMPATIBILITY="1.4.1"

# Installation options
BASE_INSTALL_PATH=""
UPDATE_INSTRUCTIONS=false
UPDATE_STANDARDS=false
UPDATE_POCKETFLOW_TOOLS=false
UPDATE_ALL=false
BACKUP_EXISTING=true
FORCE_UPDATE=false

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
║              Agent OS + PocketFlow Project Updater          ║
║                        v1.0.0                               ║
║                                                              ║
║  🔄 Update existing projects with latest base installation   ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --base-path)
                BASE_INSTALL_PATH="$2"
                shift 2
                ;;
            --update-instructions)
                UPDATE_INSTRUCTIONS=true
                shift
                ;;
            --update-standards)
                UPDATE_STANDARDS=true
                shift
                ;;
            --update-pocketflow-tools)
                UPDATE_POCKETFLOW_TOOLS=true
                shift
                ;;
            --update-all)
                UPDATE_ALL=true
                UPDATE_INSTRUCTIONS=true
                UPDATE_STANDARDS=true
                UPDATE_POCKETFLOW_TOOLS=true
                shift
                ;;
            --no-backup)
                BACKUP_EXISTING=false
                shift
                ;;
            --force)
                FORCE_UPDATE=true
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

Agent OS + PocketFlow Project Update Tool

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --base-path PATH            Path to base installation (auto-detected if not provided)
    --update-instructions       Update instructions directory
    --update-standards          Update standards directory  
    --update-pocketflow-tools   Update PocketFlow tools
    --update-all                Update all components
    --no-backup                 Skip backing up existing files
    --force                     Force update even if no changes detected
    --help                      Show this help message

EXAMPLES:
    # Update all components from base installation
    $0 --update-all
    
    # Update only instructions
    $0 --update-instructions
    
    # Update standards and PocketFlow tools
    $0 --update-standards --update-pocketflow-tools
    
    # Update with custom base path
    $0 --base-path ~/my-agent-os --update-all

NOTES:
    • Run this script from your project's root directory
    • Existing files are backed up by default before updating
    • Base installation must exist and be valid

EOF
}

# Auto-detect base installation path
detect_base_installation() {
    if [[ -n "$BASE_INSTALL_PATH" ]]; then
        BASE_INSTALL_PATH="${BASE_INSTALL_PATH/#\~/$HOME}"
        return 0
    fi
    
    # Try to read from project config
    if [[ -f ".agent-os/config.yml" ]]; then
        local config_base_path=$(grep "base_installation:" ".agent-os/config.yml" | sed 's/.*base_installation: *"\?\([^"]*\)"\?/\1/' | head -n1)
        if [[ -n "$config_base_path" && "$config_base_path" != "standalone" && -d "$config_base_path" ]]; then
            BASE_INSTALL_PATH="$config_base_path"
            log_info "Detected base installation from config: $BASE_INSTALL_PATH"
            return 0
        fi
    fi
    
    # Common installation locations
    local common_paths=(
        "$HOME/.agent-os"
        "/usr/local/agent-os"
    )
    
    for path in "${common_paths[@]}"; do
        if [[ -f "$path/config.yml" && -d "$path/setup" ]]; then
            BASE_INSTALL_PATH="$path"
            log_info "Found base installation: $BASE_INSTALL_PATH"
            return 0
        fi
    done
    
    return 1
}

# Validate project and base installation
validate_installations() {
    # Check if we're in a valid project
    if [[ ! -d ".agent-os" ]]; then
        log_error "No .agent-os directory found. This doesn't appear to be an Agent OS project."
        log_info "Run this script from your project's root directory."
        exit 1
    fi
    
    # Check if project has config
    if [[ ! -f ".agent-os/config.yml" ]]; then
        log_error "No config.yml found in .agent-os directory."
        log_info "This may not be a valid Agent OS project installation."
        exit 1
    fi
    
    # Detect base installation
    if ! detect_base_installation; then
        log_error "No base installation found."
        log_info "Please specify base installation path with --base-path"
        exit 1
    fi
    
    # Validate base installation
    if [[ ! -d "$BASE_INSTALL_PATH" ]]; then
        log_error "Base installation directory not found: $BASE_INSTALL_PATH"
        exit 1
    fi
    
    if [[ ! -f "$BASE_INSTALL_PATH/config.yml" ]]; then
        log_error "Invalid base installation: missing config.yml"
        exit 1
    fi
    
    log_success "Validated project and base installation"
}

# Backup existing files
backup_files() {
    if [[ "$BACKUP_EXISTING" != "true" ]]; then
        return 0
    fi
    
    log_info "Creating backup of existing files..."
    
    local backup_dir=".agent-os-backup-$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup directories that will be updated
    if [[ "$UPDATE_INSTRUCTIONS" == "true" && -d ".agent-os/instructions" ]]; then
        cp -r ".agent-os/instructions" "$backup_dir/"
        log_success "Backed up instructions to $backup_dir/"
    fi
    
    if [[ "$UPDATE_STANDARDS" == "true" && -d ".agent-os/standards" ]]; then
        cp -r ".agent-os/standards" "$backup_dir/"
        log_success "Backed up standards to $backup_dir/"
    fi
    
    if [[ "$UPDATE_POCKETFLOW_TOOLS" == "true" && -d ".agent-os/pocketflow-tools" ]]; then
        cp -r ".agent-os/pocketflow-tools" "$backup_dir/"
        log_success "Backed up pocketflow-tools to $backup_dir/"
    fi
    
    log_info "Backup completed: $backup_dir"
}

# Update instructions
update_instructions() {
    if [[ "$UPDATE_INSTRUCTIONS" != "true" ]]; then
        return 0
    fi
    
    log_info "Updating instructions from base installation..."
    
    if [[ ! -d "$BASE_INSTALL_PATH/instructions" ]]; then
        log_error "Base installation missing instructions directory"
        return 1
    fi
    
    # Remove existing instructions
    if [[ -d ".agent-os/instructions" ]]; then
        rm -rf ".agent-os/instructions"
    fi
    
    # Copy new instructions
    cp -r "$BASE_INSTALL_PATH/instructions" ".agent-os/"
    if [[ $? -eq 0 ]]; then
        log_success "Updated instructions from base installation"
    else
        log_error "Failed to update instructions"
        return 1
    fi
}

# Update standards
update_standards() {
    if [[ "$UPDATE_STANDARDS" != "true" ]]; then
        return 0
    fi
    
    log_info "Updating standards from base installation..."
    
    if [[ ! -d "$BASE_INSTALL_PATH/standards" ]]; then
        log_error "Base installation missing standards directory"
        return 1
    fi
    
    # Remove existing standards
    if [[ -d ".agent-os/standards" ]]; then
        rm -rf ".agent-os/standards"
    fi
    
    # Copy new standards
    cp -r "$BASE_INSTALL_PATH/standards" ".agent-os/"
    if [[ $? -eq 0 ]]; then
        log_success "Updated standards from base installation"
    else
        log_error "Failed to update standards"
        return 1
    fi
}

# Update PocketFlow tools
update_pocketflow_tools() {
    if [[ "$UPDATE_POCKETFLOW_TOOLS" != "true" ]]; then
        return 0
    fi
    
    log_info "Updating PocketFlow tools from base installation..."
    
    if [[ ! -d "$BASE_INSTALL_PATH/pocketflow-tools" ]]; then
        log_warning "Base installation missing pocketflow-tools directory - skipping"
        return 0
    fi
    
    # Remove existing PocketFlow tools
    if [[ -d ".agent-os/pocketflow-tools" ]]; then
        rm -rf ".agent-os/pocketflow-tools"
    fi
    
    # Copy new PocketFlow tools
    mkdir -p ".agent-os/pocketflow-tools"
    cp -r "$BASE_INSTALL_PATH/pocketflow-tools"/* ".agent-os/pocketflow-tools/"
    if [[ $? -eq 0 ]]; then
        log_success "Updated PocketFlow tools from base installation"
    else
        log_error "Failed to update PocketFlow tools"
        return 1
    fi
}

# Update project configuration
update_project_config() {
    log_info "Updating project configuration..."
    
    # Update the config file with new update timestamp
    if [[ -f ".agent-os/config.yml" ]]; then
        # Add or update last_updated field
        if grep -q "updated:" ".agent-os/config.yml"; then
            sed -i.bak "s/updated: .*/updated: \"$(date +'%Y-%m-%d')\"/" ".agent-os/config.yml"
        else
            echo "updated: \"$(date +'%Y-%m-%d')\"" >> ".agent-os/config.yml"
        fi
        rm -f ".agent-os/config.yml.bak"
        
        log_success "Updated project configuration timestamp"
    fi
}

# Display completion message
show_completion_message() {
    echo ""
    echo -e "${GREEN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                🎉 Project Update Complete! 🎉               ║
║              Agent OS + PocketFlow Updated                   ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    log_highlight "Updated from base installation: $BASE_INSTALL_PATH"
    
    echo ""
    log_info "Components updated:"
    [[ "$UPDATE_INSTRUCTIONS" == "true" ]] && echo "  ✅ Instructions"
    [[ "$UPDATE_STANDARDS" == "true" ]] && echo "  ✅ Standards" 
    [[ "$UPDATE_POCKETFLOW_TOOLS" == "true" ]] && echo "  ✅ PocketFlow Tools"
    
    if [[ "$BACKUP_EXISTING" == "true" ]]; then
        echo ""
        log_info "Previous files backed up to: .agent-os-backup-*"
    fi
    
    echo ""
    log_info "Your project is now updated with the latest Agent OS + PocketFlow components!"
    echo ""
}

# Main execution
main() {
    show_header
    parse_arguments "$@"
    
    # Set default behavior if no specific updates requested
    if [[ "$UPDATE_INSTRUCTIONS" != "true" && "$UPDATE_STANDARDS" != "true" && "$UPDATE_POCKETFLOW_TOOLS" != "true" && "$UPDATE_ALL" != "true" ]]; then
        log_warning "No update components specified. Use --update-all or specific --update-* flags."
        show_help
        exit 1
    fi
    
    log_info "Starting Agent OS + PocketFlow project update..."
    echo ""
    
    validate_installations
    backup_files
    update_instructions
    update_standards
    update_pocketflow_tools
    update_project_config
    show_completion_message
    
    log_success "Project update completed successfully!"
}

# Run main function with all arguments
main "$@"