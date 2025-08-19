#!/bin/bash
# Enhanced Agent OS + PocketFlow Migration Script
# Migrates existing Agent OS installations to v1.4.0 + PocketFlow
# Handles backup, migration, and validation

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
TARGET_VERSION="1.4.0"
REPO_URL="https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main"
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)_$$

# Migration options
BACKUP_PATH="$HOME/.agent-os-backup-$BACKUP_TIMESTAMP"
NEW_INSTALL_PATH="$HOME/.agent-os"
DRY_RUN=false
AUTO_CONFIRM=false
PRESERVE_CUSTOMIZATIONS=true
ENABLE_POCKETFLOW=true

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_highlight() { echo -e "${PURPLE}🎯 $1${NC}"; }
log_step() { echo -e "${CYAN}📋 $1${NC}"; }

# Display header
show_header() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║               Agent OS Migration Tool                        ║
║               Enhanced PocketFlow Edition                    ║
║                                                              ║
║  🚀 Migrate to Agent OS v1.4.0 + PocketFlow Integration     ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Help message
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Migration Options:
  --dry-run                Run migration analysis without making changes
  --auto-confirm          Skip confirmation prompts (use with caution)
  --backup-path PATH      Custom backup location (default: ~/.agent-os-backup-TIMESTAMP)
  --install-path PATH     Target installation path (default: ~/.agent-os)
  --no-pocketflow        Skip PocketFlow integration
  --no-preserve          Don't preserve existing customizations

Examples:
  $0                      Interactive migration with defaults
  $0 --dry-run           Analyze what would be migrated
  $0 --auto-confirm      Automated migration (use with caution)

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --auto-confirm)
                AUTO_CONFIRM=true
                shift
                ;;
            --backup-path)
                BACKUP_PATH="$2"
                shift 2
                ;;
            --install-path)
                NEW_INSTALL_PATH="$2"
                shift 2
                ;;
            --no-pocketflow)
                ENABLE_POCKETFLOW=false
                shift
                ;;
            --no-preserve)
                PRESERVE_CUSTOMIZATIONS=false
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Global variables for detected installations
declare -a DETECTED_PATHS
declare -a DETECTED_VERSIONS
DETECTED_COUNT=0

# Detect existing Agent OS installation
detect_existing_installation() {
    log_step "Detecting existing Agent OS installation..."
    
    # Reset global arrays
    DETECTED_PATHS=()
    DETECTED_VERSIONS=()
    DETECTED_COUNT=0
    
    # Check common installation locations
    local check_paths=(
        "$HOME/.agent-os"
        "$HOME/agent-os"
        "$HOME/.claude/agent-os"
        "/usr/local/agent-os"
    )
    
    for path in "${check_paths[@]}"; do
        if [[ -d "$path" ]]; then
            DETECTED_PATHS+=("$path")
            
            # Try to detect version
            local version="unknown"
            if [[ -f "$path/config.yml" ]]; then
                version=$(grep "version:" "$path/config.yml" 2>/dev/null | cut -d' ' -f2 | tr -d '"' || echo "unknown")
            elif [[ -f "$path/VERSION" ]]; then
                version=$(cat "$path/VERSION" 2>/dev/null || echo "unknown")
            elif [[ -f "$path/setup.sh" ]]; then
                version="pre-1.4.0"
            fi
            DETECTED_VERSIONS+=("$version")
            ((DETECTED_COUNT++))
        fi
    done
    
    # Check for .claude directory customizations
    if [[ -d "$HOME/.claude" ]]; then
        log_info "Found Claude configuration directory: $HOME/.claude"
        if [[ -d "$HOME/.claude/commands" ]]; then
            log_info "Found custom commands in: $HOME/.claude/commands"
        fi
    fi
    
    return 0
}

# Analyze migration requirements
analyze_migration() {
    log_step "Analyzing migration requirements..."
    
    detect_existing_installation
    
    if [[ $DETECTED_COUNT -eq 0 ]]; then
        log_warning "No existing Agent OS installation detected"
        log_info "This appears to be a fresh installation"
        return 0
    fi
    
    log_success "Found $DETECTED_COUNT existing installation(s)"
    
    for ((i=0; i<DETECTED_COUNT; i++)); do
        log_info "Installation $((i+1)): ${DETECTED_PATHS[i]} (version: ${DETECTED_VERSIONS[i]})"
        
        # Analyze what needs to be migrated
        if [[ -d "${DETECTED_PATHS[i]}/instructions" ]]; then
            log_info "  - Found instructions directory"
        fi
        if [[ -d "${DETECTED_PATHS[i]}/standards" ]]; then
            log_info "  - Found standards directory"
        fi
        if [[ -d "${DETECTED_PATHS[i]}/commands" ]]; then
            log_info "  - Found commands directory"
        fi
        if [[ -d "${DETECTED_PATHS[i]}/workflows" ]]; then
            log_info "  - Found workflows directory (will migrate to pocketflow-tools)"
        fi
    done
    
    return 0
}

# Create backup
create_backup() {
    if [[ $DRY_RUN == true ]]; then
        log_info "[DRY RUN] Would create backup at: $BACKUP_PATH"
        return 0
    fi
    
    log_step "Creating backup..."
    
    mkdir -p "$BACKUP_PATH"
    
    # Backup existing Agent OS installation
    detect_existing_installation
    
    if [[ $DETECTED_COUNT -gt 0 ]]; then
        for ((i=0; i<DETECTED_COUNT; i++)); do
            local source_path="${DETECTED_PATHS[i]}"
            local backup_name="agent-os-$((i+1))"
            
            log_info "Backing up: $source_path -> $BACKUP_PATH/$backup_name"
            if ! cp -r "$source_path" "$BACKUP_PATH/$backup_name"; then
                log_error "Failed to backup: $source_path"
                return 1
            fi
        done
    fi
    
    # Backup Claude configuration
    if [[ -d "$HOME/.claude" ]]; then
        log_info "Backing up Claude configuration: $HOME/.claude -> $BACKUP_PATH/claude-config"
        if ! cp -r "$HOME/.claude" "$BACKUP_PATH/claude-config"; then
            log_error "Failed to backup Claude configuration"
            return 1
        fi
    fi
    
    # Create backup manifest
    cat > "$BACKUP_PATH/backup-manifest.txt" << EOF
Agent OS Migration Backup
Created: $(date)
Script Version: $SCRIPT_VERSION
Target Version: $TARGET_VERSION

Backup Contents:
$(find "$BACKUP_PATH" -type f | head -20)
$([ $(find "$BACKUP_PATH" -type f | wc -l) -gt 20 ] && echo "... and $(( $(find "$BACKUP_PATH" -type f | wc -l) - 20 )) more files")

Instructions for Restore:
1. Remove current installation: rm -rf "$NEW_INSTALL_PATH"
2. Restore from backup: cp -r "$BACKUP_PATH/agent-os-1" "$NEW_INSTALL_PATH"
3. Restore Claude config: cp -r "$BACKUP_PATH/claude-config" "$HOME/.claude"
EOF
    
    log_success "Backup created at: $BACKUP_PATH"
}

# Preserve customizations
preserve_customizations() {
    if [[ $PRESERVE_CUSTOMIZATIONS != true ]]; then
        return 0
    fi
    
    log_step "Preserving customizations..."
    
    detect_existing_installation
    
    if [[ $DETECTED_COUNT -eq 0 ]]; then
        return 0
    fi
    
    local main_installation="${DETECTED_PATHS[0]}"
    
    # Create temp directory for preserved files
    local preserve_dir="/tmp/agent-os-preserve-$$"
    mkdir -p "$preserve_dir"
    
    # Preserve custom instructions
    if [[ -d "$main_installation/instructions" ]]; then
        log_info "Preserving custom instructions..."
        cp -r "$main_installation/instructions" "$preserve_dir/"
    fi
    
    # Preserve custom standards
    if [[ -d "$main_installation/standards" ]]; then
        log_info "Preserving custom standards..."
        cp -r "$main_installation/standards" "$preserve_dir/"
    fi
    
    # Preserve custom commands
    if [[ -d "$main_installation/commands" ]]; then
        log_info "Preserving custom commands..."
        cp -r "$main_installation/commands" "$preserve_dir/"
    fi
    
    # Store preservation path for later use
    echo "$preserve_dir" > "/tmp/agent-os-migration-preserve-path"
    
    log_success "Customizations preserved in temporary location"
}

# Install new version
install_new_version() {
    if [[ $DRY_RUN == true ]]; then
        log_info "[DRY RUN] Would install new version to: $NEW_INSTALL_PATH"
        return 0
    fi
    
    log_step "Installing Agent OS v$TARGET_VERSION + PocketFlow..."
    
    # Remove existing installation if it exists
    if [[ -d "$NEW_INSTALL_PATH" ]]; then
        log_info "Removing existing installation..."
        rm -rf "$NEW_INSTALL_PATH"
    fi
    
    # Download and run the base installation script
    local install_args="--claude-code"
    if [[ $ENABLE_POCKETFLOW == true ]]; then
        install_args="$install_args --pocketflow"
    fi
    
    log_info "Downloading and running base installation script..."
    if ! curl -sSL "$REPO_URL/setup/base.sh" | bash -s -- $install_args --install-path "$NEW_INSTALL_PATH"; then
        log_error "Failed to download or run base installation script"
        log_error "URL: $REPO_URL/setup/base.sh"
        log_error "Install args: $install_args --install-path $NEW_INSTALL_PATH"
        return 1
    fi
    
    log_success "New version installed successfully"
}

# Restore customizations
restore_customizations() {
    if [[ $PRESERVE_CUSTOMIZATIONS != true ]] || [[ $DRY_RUN == true ]]; then
        return 0
    fi
    
    local preserve_path_file="/tmp/agent-os-migration-preserve-path"
    if [[ ! -f "$preserve_path_file" ]]; then
        return 0
    fi
    
    local preserve_dir=$(cat "$preserve_path_file")
    if [[ ! -d "$preserve_dir" ]]; then
        return 0
    fi
    
    log_step "Restoring preserved customizations..."
    
    # Restore custom instructions (merge with new ones)
    if [[ -d "$preserve_dir/instructions" ]]; then
        log_info "Merging custom instructions..."
        cp -r "$preserve_dir/instructions"/* "$NEW_INSTALL_PATH/instructions/" 2>/dev/null || true
    fi
    
    # Restore custom standards (merge with new ones)
    if [[ -d "$preserve_dir/standards" ]]; then
        log_info "Merging custom standards..."
        mkdir -p "$NEW_INSTALL_PATH/standards"
        cp -r "$preserve_dir/standards"/* "$NEW_INSTALL_PATH/standards/" 2>/dev/null || true
    fi
    
    # Restore custom commands (merge with new ones)
    if [[ -d "$preserve_dir/commands" ]]; then
        log_info "Merging custom commands..."
        mkdir -p "$NEW_INSTALL_PATH/commands"
        cp -r "$preserve_dir/commands"/* "$NEW_INSTALL_PATH/commands/" 2>/dev/null || true
    fi
    
    # Cleanup
    rm -rf "$preserve_dir"
    rm -f "$preserve_path_file"
    
    log_success "Customizations restored successfully"
}

# Validate migration
validate_migration() {
    log_step "Validating migration..."
    
    local errors=0
    
    # Check if new installation exists
    if [[ ! -d "$NEW_INSTALL_PATH" ]]; then
        log_error "New installation directory not found: $NEW_INSTALL_PATH"
        ((errors++))
    else
        log_success "Installation directory exists: $NEW_INSTALL_PATH"
    fi
    
    # Check config file
    if [[ ! -f "$NEW_INSTALL_PATH/config.yml" ]]; then
        log_error "Configuration file not found: $NEW_INSTALL_PATH/config.yml"
        ((errors++))
    else
        local version=$(grep "version:" "$NEW_INSTALL_PATH/config.yml" | cut -d' ' -f2 | tr -d '"')
        if [[ "$version" == "$TARGET_VERSION" ]]; then
            log_success "Version verified: $version"
        else
            log_error "Version mismatch. Expected: $TARGET_VERSION, Found: $version"
            ((errors++))
        fi
    fi
    
    # Check essential directories
    local required_dirs=("instructions" "standards" "commands" "setup")
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$NEW_INSTALL_PATH/$dir" ]]; then
            log_error "Required directory missing: $NEW_INSTALL_PATH/$dir"
            ((errors++))
        else
            log_success "Directory exists: $dir"
        fi
    done
    
    # Check PocketFlow integration if enabled
    if [[ $ENABLE_POCKETFLOW == true ]]; then
        if [[ ! -d "$NEW_INSTALL_PATH/pocketflow-tools" ]]; then
            log_error "PocketFlow tools directory missing"
            ((errors++))
        else
            log_success "PocketFlow integration verified"
        fi
    fi
    
    # Check scripts are executable
    local scripts=("setup/base.sh" "setup/project.sh")
    for script in "${scripts[@]}"; do
        if [[ ! -x "$NEW_INSTALL_PATH/$script" ]]; then
            log_error "Script not executable: $NEW_INSTALL_PATH/$script"
            ((errors++))
        else
            log_success "Script executable: $script"
        fi
    done
    
    if [[ $errors -eq 0 ]]; then
        log_success "Migration validation passed!"
        return 0
    else
        log_error "Migration validation failed with $errors error(s)"
        return 1
    fi
}

# Show migration summary
show_summary() {
    log_highlight "Migration Summary"
    echo
    log_info "Backup Location: $BACKUP_PATH"
    log_info "New Installation: $NEW_INSTALL_PATH"
    log_info "Target Version: $TARGET_VERSION"
    log_info "PocketFlow Enabled: $ENABLE_POCKETFLOW"
    log_info "Customizations Preserved: $PRESERVE_CUSTOMIZATIONS"
    echo
    
    if [[ $DRY_RUN == true ]]; then
        log_warning "This was a DRY RUN - no changes were made"
        log_info "Run without --dry-run to perform the actual migration"
    else
        log_success "Migration completed successfully!"
        echo
        log_info "Next Steps:"
        log_info "1. Test your new installation: ls -la $NEW_INSTALL_PATH"
        log_info "2. Update your projects: $NEW_INSTALL_PATH/setup/project.sh"
        log_info "3. Your backup is available at: $BACKUP_PATH"
        echo
        log_warning "If you encounter issues, you can restore from backup:"
        log_warning "rm -rf $NEW_INSTALL_PATH && cp -r $BACKUP_PATH/agent-os-1 $NEW_INSTALL_PATH"
    fi
}

# Confirmation prompt
confirm_migration() {
    if [[ $AUTO_CONFIRM == true ]] || [[ $DRY_RUN == true ]]; then
        return 0
    fi
    
    echo
    log_warning "This will migrate your Agent OS installation to v$TARGET_VERSION + PocketFlow"
    log_warning "Your existing installation will be backed up to: $BACKUP_PATH"
    echo
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Migration cancelled by user"
        exit 0
    fi
}

# Rollback function
rollback_migration() {
    log_error "Migration failed! Attempting rollback..."
    
    if [[ -d "$BACKUP_PATH" ]]; then
        log_info "Restoring from backup..."
        
        # Remove failed installation
        if [[ -d "$NEW_INSTALL_PATH" ]]; then
            rm -rf "$NEW_INSTALL_PATH"
        fi
        
        # Restore from backup
        if [[ -d "$BACKUP_PATH/agent-os-1" ]]; then
            cp -r "$BACKUP_PATH/agent-os-1" "$NEW_INSTALL_PATH"
            log_success "Installation restored from backup"
        fi
        
        # Restore Claude config if needed
        if [[ -d "$BACKUP_PATH/claude-config" ]] && [[ ! -d "$HOME/.claude" ]]; then
            cp -r "$BACKUP_PATH/claude-config" "$HOME/.claude"
            log_success "Claude configuration restored"
        fi
        
        log_warning "Rollback completed. Your previous installation has been restored."
    else
        log_error "Backup not found. Please restore manually if needed."
    fi
}

# Main migration process
main() {
    show_header
    parse_args "$@"
    
    # Trap errors for rollback
    if [[ $DRY_RUN != true ]]; then
        trap 'rollback_migration' ERR
    fi
    
    # Run migration steps
    analyze_migration
    confirm_migration
    create_backup
    preserve_customizations
    install_new_version
    restore_customizations
    
    # Validate only if not dry run
    if [[ $DRY_RUN != true ]]; then
        if ! validate_migration; then
            log_error "Migration validation failed"
            exit 1
        fi
    fi
    
    show_summary
    
    # Disable trap on successful completion
    trap - ERR
}

# Run main function with all arguments
main "$@"