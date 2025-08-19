#!/bin/bash
# Enhanced Agent OS + PocketFlow Backup & Restore Utility
# Provides comprehensive backup and restore functionality

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
DEFAULT_BACKUP_DIR="$HOME/.agent-os-backups"
DEFAULT_INSTALL_PATH="$HOME/.agent-os"

# Operation mode
OPERATION=""
BACKUP_PATH=""
RESTORE_PATH=""
INSTALL_PATH="$DEFAULT_INSTALL_PATH"
COMPRESSION=true
VERIFY_INTEGRITY=true
INCLUDE_PROJECTS=false
AUTO_CLEANUP=false
MAX_BACKUPS=10

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
║             Agent OS Backup & Restore Utility               ║
║             Enhanced PocketFlow Edition                      ║
║                                                              ║
║  💾 Comprehensive Backup and Restore for Agent OS           ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Help message
show_help() {
    cat << EOF
Usage: $0 OPERATION [OPTIONS]

Operations:
  backup              Create backup of Agent OS installation
  restore             Restore Agent OS from backup
  list                List available backups
  cleanup             Remove old backups
  verify              Verify backup integrity

Backup Options:
  --output PATH       Backup output directory (default: $DEFAULT_BACKUP_DIR)
  --name NAME         Custom backup name (default: timestamp-based)
  --no-compress       Skip compression
  --include-projects  Include project installations in backup
  --install-path PATH Agent OS installation path (default: $DEFAULT_INSTALL_PATH)

Restore Options:
  --backup PATH       Path to backup file/directory
  --target PATH       Restore target path (default: $DEFAULT_INSTALL_PATH)
  --no-verify         Skip integrity verification

Cleanup Options:
  --keep NUM          Number of backups to keep (default: $MAX_BACKUPS)
  --older-than DAYS   Remove backups older than N days

Examples:
  $0 backup                                    # Create backup with defaults
  $0 backup --name "pre-migration"             # Create named backup
  $0 backup --include-projects                 # Include project installations
  $0 restore --backup ~/.agent-os-backups/backup-20240819_143022
  $0 list                                      # List available backups
  $0 cleanup --keep 5                          # Keep only 5 most recent backups
  $0 verify --backup ~/.agent-os-backups/backup-20240819_143022

EOF
}

# Parse command line arguments
parse_args() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 1
    fi
    
    OPERATION="$1"
    shift
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --output)
                DEFAULT_BACKUP_DIR="$2"
                shift 2
                ;;
            --name)
                BACKUP_NAME="$2"
                shift 2
                ;;
            --backup)
                BACKUP_PATH="$2"
                shift 2
                ;;
            --target)
                RESTORE_PATH="$2"
                shift 2
                ;;
            --install-path)
                INSTALL_PATH="$2"
                shift 2
                ;;
            --no-compress)
                COMPRESSION=false
                shift
                ;;
            --no-verify)
                VERIFY_INTEGRITY=false
                shift
                ;;
            --include-projects)
                INCLUDE_PROJECTS=true
                shift
                ;;
            --keep)
                MAX_BACKUPS="$2"
                shift 2
                ;;
            --older-than)
                CLEANUP_DAYS="$2"
                shift 2
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

# Generate backup name
generate_backup_name() {
    if [[ -n "$BACKUP_NAME" ]]; then
        echo "backup-$BACKUP_NAME-$(date +%Y%m%d_%H%M%S)"
    else
        echo "backup-$(date +%Y%m%d_%H%M%S)"
    fi
}

# Check if Agent OS installation exists
check_installation() {
    if [[ ! -d "$INSTALL_PATH" ]]; then
        log_error "Agent OS installation not found at: $INSTALL_PATH"
        return 1
    fi
    
    if [[ ! -f "$INSTALL_PATH/config.yml" ]]; then
        log_warning "No config.yml found. This might be an older installation."
    fi
    
    return 0
}

# Calculate directory size
calc_size() {
    local path="$1"
    if [[ -d "$path" ]]; then
        du -sh "$path" 2>/dev/null | cut -f1
    else
        echo "0B"
    fi
}

# Create backup
create_backup() {
    log_step "Creating Agent OS backup..."
    
    # Check installation
    if ! check_installation; then
        return 1
    fi
    
    # Setup backup directory
    mkdir -p "$DEFAULT_BACKUP_DIR"
    local backup_name=$(generate_backup_name)
    local backup_dir="$DEFAULT_BACKUP_DIR/$backup_name"
    
    log_info "Backup location: $backup_dir"
    
    # Create backup structure
    mkdir -p "$backup_dir"
    
    # Create backup manifest
    cat > "$backup_dir/backup-manifest.json" << EOF
{
  "backup_info": {
    "created": "$(date -Iseconds)",
    "script_version": "$SCRIPT_VERSION",
    "backup_name": "$backup_name",
    "source_path": "$INSTALL_PATH",
    "compression": $COMPRESSION,
    "include_projects": $INCLUDE_PROJECTS
  },
  "installation_info": {
    "path": "$INSTALL_PATH",
    "size": "$(calc_size "$INSTALL_PATH")",
    "version": "$(grep "version:" "$INSTALL_PATH/config.yml" 2>/dev/null | cut -d' ' -f2 | tr -d '"' || echo "unknown")",
    "components": []
  }
}
EOF
    
    # Backup main installation
    log_info "Backing up main installation..."
    if ! cp -r "$INSTALL_PATH" "$backup_dir/agent-os"; then
        log_error "Failed to backup main installation from: $INSTALL_PATH"
        return 1
    fi
    
    # Update manifest with component info
    local components=()
    for dir in "$INSTALL_PATH"/*; do
        if [[ -d "$dir" ]]; then
            local dirname=$(basename "$dir")
            local size=$(calc_size "$dir")
            components+=("\"$dirname\": {\"size\": \"$size\"}")
        fi
    done
    
    # Backup Claude configuration if exists
    if [[ -d "$HOME/.claude" ]]; then
        log_info "Backing up Claude configuration..."
        if ! cp -r "$HOME/.claude" "$backup_dir/claude-config"; then
            log_error "Failed to backup Claude configuration"
            return 1
        fi
        components+=("\"claude-config\": {\"size\": \"$(calc_size "$HOME/.claude")\"}")
    fi
    
    # Backup project installations if requested
    if [[ $INCLUDE_PROJECTS == true ]]; then
        log_info "Searching for project installations..."
        local project_count=0
        
        # Search for .agent-os directories in common project locations
        local search_paths=("$HOME/projects" "$HOME/dev" "$HOME/work" "$HOME/code" "$HOME/src")
        for search_path in "${search_paths[@]}"; do
            if [[ -d "$search_path" ]]; then
                find "$search_path" -name ".agent-os" -type d 2>/dev/null | while read -r project_agent_os; do
                    local project_path=$(dirname "$project_agent_os")
                    local project_name=$(basename "$project_path")
                    
                    log_info "Found project installation: $project_name"
                    mkdir -p "$backup_dir/projects"
                    cp -r "$project_agent_os" "$backup_dir/projects/$project_name-agent-os"
                    ((project_count++))
                done
            fi
        done
        
        if [[ $project_count -gt 0 ]]; then
            components+=("\"projects\": {\"count\": $project_count}")
        fi
    fi
    
    # Update manifest with components
    local components_json=$(printf "%s," "${components[@]}" | sed 's/,$//')
    sed -i.bak "s/\"components\": \[\]/\"components\": {$components_json}/" "$backup_dir/backup-manifest.json"
    rm -f "$backup_dir/backup-manifest.json.bak"
    
    # Create integrity checksum
    log_info "Generating integrity checksum..."
    find "$backup_dir" -type f -exec sha256sum {} \; > "$backup_dir/integrity.sha256"
    
    # Compress if requested
    if [[ $COMPRESSION == true ]]; then
        log_info "Compressing backup..."
        local archive_path="$backup_dir.tar.gz"
        tar -czf "$archive_path" -C "$DEFAULT_BACKUP_DIR" "$backup_name"
        rm -rf "$backup_dir"
        backup_dir="$archive_path"
        
        # Update paths in variables for later use
        BACKUP_PATH="$archive_path"
    else
        BACKUP_PATH="$backup_dir"
    fi
    
    # Calculate final size
    local final_size=$(calc_size "$backup_dir")
    
    log_success "Backup created successfully!"
    log_info "Location: $BACKUP_PATH"
    log_info "Size: $final_size"
    
    return 0
}

# List available backups
list_backups() {
    log_step "Available Agent OS backups:"
    
    if [[ ! -d "$DEFAULT_BACKUP_DIR" ]]; then
        log_warning "No backup directory found at: $DEFAULT_BACKUP_DIR"
        return 0
    fi
    
    local backup_count=0
    
    # List compressed backups
    for backup in "$DEFAULT_BACKUP_DIR"/backup-*.tar.gz; do
        if [[ -f "$backup" ]]; then
            local name=$(basename "$backup" .tar.gz)
            local size=$(calc_size "$backup")
            local date=$(date -r "$backup" +%Y-%m-%d 2>/dev/null || stat -c %y "$backup" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
            
            log_info "📦 $name"
            log_info "   Size: $size | Date: $date | Path: $backup"
            ((backup_count++))
        fi
    done
    
    # List uncompressed backups
    for backup in "$DEFAULT_BACKUP_DIR"/backup-*; do
        if [[ -d "$backup" ]]; then
            local name=$(basename "$backup")
            local size=$(calc_size "$backup")
            local date=$(date -r "$backup" +%Y-%m-%d 2>/dev/null || stat -c %y "$backup" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
            
            log_info "📁 $name"
            log_info "   Size: $size | Date: $date | Path: $backup"
            ((backup_count++))
        fi
    done
    
    if [[ $backup_count -eq 0 ]]; then
        log_warning "No backups found in: $DEFAULT_BACKUP_DIR"
    else
        log_success "Found $backup_count backup(s)"
    fi
    
    return 0
}

# Verify backup integrity
verify_backup() {
    local backup_path="$BACKUP_PATH"
    
    if [[ -z "$backup_path" ]]; then
        log_error "Backup path not specified. Use --backup PATH"
        return 1
    fi
    
    log_step "Verifying backup integrity: $backup_path"
    
    local temp_dir=""
    local cleanup_temp=false
    
    # Handle compressed backups
    if [[ "$backup_path" == *.tar.gz ]]; then
        if [[ ! -f "$backup_path" ]]; then
            log_error "Backup file not found: $backup_path"
            return 1
        fi
        
        temp_dir="/tmp/agent-os-verify-$$"
        mkdir -p "$temp_dir"
        cleanup_temp=true
        
        log_info "Extracting compressed backup for verification..."
        tar -xzf "$backup_path" -C "$temp_dir"
        backup_path="$temp_dir/$(basename "$backup_path" .tar.gz)"
    fi
    
    # Check if backup directory exists
    if [[ ! -d "$backup_path" ]]; then
        log_error "Backup directory not found: $backup_path"
        [[ $cleanup_temp == true ]] && rm -rf "$temp_dir"
        return 1
    fi
    
    local errors=0
    
    # Check manifest
    if [[ ! -f "$backup_path/backup-manifest.json" ]]; then
        log_error "Backup manifest not found"
        ((errors++))
    else
        log_success "Backup manifest found"
        
        # Parse and display backup info
        local created=$(grep '"created"' "$backup_path/backup-manifest.json" | cut -d'"' -f4)
        local version=$(grep '"version"' "$backup_path/backup-manifest.json" | cut -d'"' -f4)
        log_info "Created: $created"
        log_info "Version: $version"
    fi
    
    # Check main installation backup
    if [[ ! -d "$backup_path/agent-os" ]]; then
        log_error "Main installation backup not found"
        ((errors++))
    else
        log_success "Main installation backup found"
    fi
    
    # Verify integrity checksums if available
    if [[ -f "$backup_path/integrity.sha256" ]]; then
        log_info "Verifying checksums..."
        if (cd "$backup_path" && sha256sum -c integrity.sha256 --quiet); then
            log_success "Integrity verification passed"
        else
            log_error "Integrity verification failed"
            ((errors++))
        fi
    else
        log_warning "No integrity checksums found (older backup format)"
    fi
    
    # Check essential components
    local required_files=("agent-os/config.yml" "agent-os/setup/base.sh" "agent-os/setup/project.sh")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$backup_path/$file" ]]; then
            log_error "Required file missing: $file"
            ((errors++))
        fi
    done
    
    # Cleanup temp directory
    [[ $cleanup_temp == true ]] && rm -rf "$temp_dir"
    
    if [[ $errors -eq 0 ]]; then
        log_success "Backup verification completed successfully!"
        return 0
    else
        log_error "Backup verification failed with $errors error(s)"
        return 1
    fi
}

# Restore from backup
restore_backup() {
    local backup_path="$BACKUP_PATH"
    local target_path="${RESTORE_PATH:-$DEFAULT_INSTALL_PATH}"
    
    if [[ -z "$backup_path" ]]; then
        log_error "Backup path not specified. Use --backup PATH"
        return 1
    fi
    
    log_step "Restoring Agent OS from backup..."
    log_info "Source: $backup_path"
    log_info "Target: $target_path"
    
    # Verify backup if requested
    if [[ $VERIFY_INTEGRITY == true ]]; then
        if ! verify_backup; then
            log_error "Backup verification failed. Aborting restore."
            return 1
        fi
    fi
    
    local temp_dir=""
    local cleanup_temp=false
    local restore_source=""
    
    # Handle compressed backups
    if [[ "$backup_path" == *.tar.gz ]]; then
        if [[ ! -f "$backup_path" ]]; then
            log_error "Backup file not found: $backup_path"
            return 1
        fi
        
        temp_dir="/tmp/agent-os-restore-$$"
        mkdir -p "$temp_dir"
        cleanup_temp=true
        
        log_info "Extracting compressed backup..."
        tar -xzf "$backup_path" -C "$temp_dir"
        restore_source="$temp_dir/$(basename "$backup_path" .tar.gz)"
    else
        if [[ ! -d "$backup_path" ]]; then
            log_error "Backup directory not found: $backup_path"
            return 1
        fi
        restore_source="$backup_path"
    fi
    
    # Create backup of current installation if it exists
    if [[ -d "$target_path" ]]; then
        log_warning "Existing installation found at: $target_path"
        local current_backup="$target_path.restore-backup.$(date +%Y%m%d_%H%M%S)"
        log_info "Creating backup of current installation: $current_backup"
        mv "$target_path" "$current_backup"
        log_success "Current installation backed up to: $current_backup"
    fi
    
    # Restore main installation
    log_info "Restoring main installation..."
    if [[ ! -d "$restore_source/agent-os" ]]; then
        log_error "Main installation not found in backup"
        [[ $cleanup_temp == true ]] && rm -rf "$temp_dir"
        return 1
    fi
    
    if ! cp -r "$restore_source/agent-os" "$target_path"; then
        log_error "Failed to restore main installation to: $target_path"
        [[ $cleanup_temp == true ]] && rm -rf "$temp_dir"
        return 1
    fi
    
    # Restore Claude configuration if available and not already exists
    if [[ -d "$restore_source/claude-config" ]] && [[ ! -d "$HOME/.claude" ]]; then
        log_info "Restoring Claude configuration..."
        cp -r "$restore_source/claude-config" "$HOME/.claude"
        log_success "Claude configuration restored"
    fi
    
    # Make scripts executable
    find "$target_path/setup" -name "*.sh" -exec chmod +x {} \;
    
    # Cleanup temp directory
    [[ $cleanup_temp == true ]] && rm -rf "$temp_dir"
    
    log_success "Restore completed successfully!"
    log_info "Agent OS restored to: $target_path"
    
    # Verify restored installation
    log_info "Verifying restored installation..."
    if [[ -f "$target_path/config.yml" ]]; then
        local version=$(grep "version:" "$target_path/config.yml" | cut -d' ' -f2 | tr -d '"')
        log_success "Restored version: $version"
    fi
    
    return 0
}

# Cleanup old backups
cleanup_backups() {
    log_step "Cleaning up old backups..."
    
    if [[ ! -d "$DEFAULT_BACKUP_DIR" ]]; then
        log_warning "No backup directory found at: $DEFAULT_BACKUP_DIR"
        return 0
    fi
    
    local keep_count=${MAX_BACKUPS:-10}
    local cleanup_days=${CLEANUP_DAYS:-0}
    
    log_info "Cleanup policy: Keep $keep_count recent backups"
    [[ $cleanup_days -gt 0 ]] && log_info "Also remove backups older than $cleanup_days days"
    
    # Get list of all backups (both compressed and uncompressed)
    local all_backups=()
    for backup in "$DEFAULT_BACKUP_DIR"/backup-*.tar.gz "$DEFAULT_BACKUP_DIR"/backup-*; do
        if [[ -e "$backup" ]]; then
            all_backups+=("$backup")
        fi
    done
    
    # Sort by modification time (newest first)
    local sorted_backups=($(printf "%s\n" "${all_backups[@]}" | xargs ls -1t 2>/dev/null || true))
    
    local total_count=${#sorted_backups[@]}
    local removed_count=0
    
    log_info "Found $total_count backup(s)"
    
    # Remove by count (keep only the most recent ones)
    if [[ $total_count -gt $keep_count ]]; then
        log_info "Removing old backups (keeping $keep_count most recent)..."
        for ((i=$keep_count; i<$total_count; i++)); do
            local backup_path="${sorted_backups[i]}"
            local backup_name=$(basename "$backup_path")
            
            log_info "Removing: $backup_name"
            rm -rf "$backup_path"
            ((removed_count++))
        done
    fi
    
    # Remove by age if specified
    if [[ $cleanup_days -gt 0 ]]; then
        log_info "Removing backups older than $cleanup_days days..."
        find "$DEFAULT_BACKUP_DIR" -name "backup-*" -type f -o -name "backup-*" -type d | while read -r backup_path; do
            local age_days=$(( ($(date +%s) - $(stat -c %Y "$backup_path" 2>/dev/null || date -r "$backup_path" +%s 2>/dev/null || echo 0)) / 86400 ))
            
            if [[ $age_days -gt $cleanup_days ]]; then
                local backup_name=$(basename "$backup_path")
                log_info "Removing old backup: $backup_name (age: $age_days days)"
                rm -rf "$backup_path"
                ((removed_count++))
            fi
        done
    fi
    
    if [[ $removed_count -eq 0 ]]; then
        log_success "No backups needed to be removed"
    else
        log_success "Removed $removed_count old backup(s)"
    fi
    
    # Show remaining backups
    log_info "Remaining backups:"
    list_backups
    
    return 0
}

# Main function
main() {
    show_header
    parse_args "$@"
    
    case "$OPERATION" in
        backup)
            create_backup
            ;;
        restore)
            restore_backup
            ;;
        list)
            list_backups
            ;;
        verify)
            verify_backup
            ;;
        cleanup)
            cleanup_backups
            ;;
        *)
            log_error "Unknown operation: $OPERATION"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"