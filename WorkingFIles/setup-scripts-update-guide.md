# Step-by-Step Implementation Guide: Updating setup.sh for Templates Directory

## Overview
This document provides detailed instructions for updating `setup.sh` to handle the new `/templates` directory that contains PocketFlow templates required by the updated Agent OS + PocketFlow integration.

## Prerequisites
- Access to `setup.sh` file in the Agent OS repository root
- Understanding of bash scripting basics
- Knowledge of the current file structure and template dependencies

## Implementation Steps

### Step 1: Add Templates Flag to Argument Parsing

**Location**: Around line 13-22 (in the argument parsing while loop)

**Action**: Add the new `--overwrite-templates` flag option

**Changes**:
1. Locate the line with `OVERWRITE_STANDARDS=false`
2. Add after that line:
   ```bash
   OVERWRITE_TEMPLATES=false
   ```

3. In the `while [[ $# -gt 0 ]]` loop, after the `--overwrite-standards)` case, add:
   ```bash
   --overwrite-templates)
       OVERWRITE_TEMPLATES=true
       shift
       ;;
   ```

### Step 2: Update Help Text

**Location**: Around line 24-32 (in the help section)

**Action**: Add documentation for the new flag

**Changes**:
1. Locate the line: `echo "  --overwrite-standards       Overwrite existing standards files"`
2. Add after that line:
   ```bash
   echo "  --overwrite-templates       Overwrite existing template files"
   ```

### Step 3: Add Templates Directory Creation

**Location**: Around line 49-54 (in the directory creation section)

**Action**: Add templates directory to the mkdir commands

**Changes**:
1. Locate the line: `mkdir -p "$HOME/.agent-os/instructions/meta"`
2. Add after that line:
   ```bash
   mkdir -p "$HOME/.agent-os/templates"
   ```

### Step 4: Add Templates Download Section

**Location**: After the Python-specific style files download section, before instruction files

**Action**: Insert complete templates download section

**Changes**:
1. Locate the end of the testing-style.md download block
2. Insert the following complete section:

```bash
# Download template files
echo ""
echo "📥 Downloading template files to ~/.agent-os/templates/"

# pocketflow-templates.md
if [ -f "$HOME/.agent-os/templates/pocketflow-templates.md" ] && [ "$OVERWRITE_TEMPLATES" = false ]; then
    echo "  ⚠️  ~/.agent-os/templates/pocketflow-templates.md already exists - skipping"
else
    curl -s -o "$HOME/.agent-os/templates/pocketflow-templates.md" "${BASE_URL}/templates/pocketflow-templates.md"
    if [ -f "$HOME/.agent-os/templates/pocketflow-templates.md" ] && [ "$OVERWRITE_TEMPLATES" = true ]; then
        echo "  ✓ ~/.agent-os/templates/pocketflow-templates.md (overwritten)"
    else
        echo "  ✓ ~/.agent-os/templates/pocketflow-templates.md"
    fi
fi

# fastapi-templates.md
if [ -f "$HOME/.agent-os/templates/fastapi-templates.md" ] && [ "$OVERWRITE_TEMPLATES" = false ]; then
    echo "  ⚠️  ~/.agent-os/templates/fastapi-templates.md already exists - skipping"
else
    curl -s -o "$HOME/.agent-os/templates/fastapi-templates.md" "${BASE_URL}/templates/fastapi-templates.md"
    if [ -f "$HOME/.agent-os/templates/fastapi-templates.md" ] && [ "$OVERWRITE_TEMPLATES" = true ]; then
        echo "  ✓ ~/.agent-os/templates/fastapi-templates.md (overwritten)"
    else
        echo "  ✓ ~/.agent-os/templates/fastapi-templates.md"
    fi
fi

# task-templates.md
if [ -f "$HOME/.agent-os/templates/task-templates.md" ] && [ "$OVERWRITE_TEMPLATES" = false ]; then
    echo "  ⚠️  ~/.agent-os/templates/task-templates.md already exists - skipping"
else
    curl -s -o "$HOME/.agent-os/templates/task-templates.md" "${BASE_URL}/templates/task-templates.md"
    if [ -f "$HOME/.agent-os/templates/task-templates.md" ] && [ "$OVERWRITE_TEMPLATES" = true ]; then
        echo "  ✓ ~/.agent-os/templates/task-templates.md (overwritten)"
    else
        echo "  ✓ ~/.agent-os/templates/task-templates.md"
    fi
fi
```

### Step 5: Update Installation Complete Message

**Location**: Around line 223 (in the completion message)

**Action**: Add templates directory to the installed files list

**Changes**:
1. Locate the line: `echo "   ~/.agent-os/instructions/  - Agent OS instructions"`
2. Add after that line:
   ```bash
   echo "   ~/.agent-os/templates/     - PocketFlow templates"
   ```

### Step 6: Update Flag Handling Logic in Completion Message

**Location**: Around line 226-237 (in the conditional completion message)

**Action**: Update the flag handling logic to include templates

**Changes**:
1. Locate the condition: `if [ "$OVERWRITE_INSTRUCTIONS" = false ] && [ "$OVERWRITE_STANDARDS" = false ]; then`
2. Replace with:
   ```bash
   if [ "$OVERWRITE_INSTRUCTIONS" = false ] && [ "$OVERWRITE_STANDARDS" = false ] && [ "$OVERWRITE_TEMPLATES" = false ]; then
   ```

3. Update the subsequent conditional messages to include templates flag logic:
   ```bash
   else
       echo "💡 Note: Some files were overwritten based on your flags"
       if [ "$OVERWRITE_INSTRUCTIONS" = false ]; then
           echo "   Existing instruction files were preserved"
       fi
       if [ "$OVERWRITE_STANDARDS" = false ]; then
           echo "   Existing standards files were preserved"
       fi
       if [ "$OVERWRITE_TEMPLATES" = false ]; then
           echo "   Existing template files were preserved"
       fi
   fi
   ```

### Step 7: Update Script Documentation Header (Optional)

**Location**: Lines 1-5 (script header comments)

**Action**: Update any version comments or descriptions if needed

**Changes**:
Consider updating any version numbers or descriptions in the header comments to reflect the PocketFlow integration changes.

## Validation Steps

### Step 1: Syntax Check
```bash
bash -n setup.sh
```

### Step 2: Test Directory Creation
```bash
# Test without overwrite flags
./setup.sh --help
```

### Step 3: Test Dry Run
Create a test environment and run:
```bash
# Test with all flags
./setup.sh --overwrite-instructions --overwrite-standards --overwrite-templates
```

### Step 4: Verify Template Downloads
Check that all three template files are downloaded:
- `~/.agent-os/templates/pocketflow-templates.md`
- `~/.agent-os/templates/fastapi-templates.md`
- `~/.agent-os/templates/task-templates.md`

### Step 5: Test Flag Logic
```bash
# Run again without flags to test skip logic
./setup.sh
```

## Testing Checklist

- [ ] Script parses `--overwrite-templates` flag correctly
- [ ] Help text displays new flag option
- [ ] Templates directory is created
- [ ] All three template files download successfully
- [ ] Existing file skip logic works for templates
- [ ] Overwrite logic works for templates when flag is used
- [ ] Completion message includes templates directory
- [ ] Flag handling logic includes templates in conditionals
- [ ] Script exits gracefully on all test scenarios

## Rollback Plan

If issues occur during implementation:

1. **Immediate Rollback**: Revert `setup.sh` to previous version from git
2. **Partial Rollback**: Comment out templates section while keeping flag infrastructure
3. **Debug Mode**: Add `set -x` at top of script to trace execution

## Files Modified Summary

- **Modified**: `setup.sh` (7 sections updated)
- **Not Modified**: `setup-claude-code.sh`, `setup-cursor.sh`

## Post-Implementation Notes

After successful implementation:

1. Test the updated script in a clean environment
2. Verify that `create-spec.md` can properly access the template files via `@templates/` references
3. Update documentation or README files that reference the setup process
4. Consider updating any CI/CD scripts that use the setup scripts

## Background Context

### Template Dependencies Identified
- **Only `create-spec.md`** references templates (13 total references)
- **Template files required**:
  - `pocketflow-templates.md` (7 references)
  - `fastapi-templates.md` (3 references)
  - `task-templates.md` (3 references)

### Integration Importance
These templates are critical for the Agent OS + PocketFlow integration as they provide:
- Design document templates with 8-step methodology
- FastAPI + Pydantic integration patterns
- PocketFlow workflow templates
- Task breakdown structures following the new paradigm

Without these templates, the `create-spec.md` instruction file will fail when trying to reference `@templates/` paths, breaking the core spec creation workflow.