# Streamlined Repository Structure

## Changes Made

### Removed Redundancies
1. **Deleted `.agent-os/backup/`** - Git provides version control
2. **Deleted `commands/`** - Redundant with `instructions/core/`
3. **Deleted `.agent-os/templates/`** - Using single `templates/` directory
4. **Symlinked `.agent-os/instructions/core/`** → `instructions/core/`

### New Simplified Structure

```
.
├── .agent-os/                        # Agent OS runtime configuration
│   ├── instructions/
│   │   ├── core → ../../instructions/core  # Symlink to source
│   │   ├── extensions/               # PocketFlow-specific extensions
│   │   │   ├── design-first-enforcement.md
│   │   │   ├── llm-workflow-extension.md
│   │   │   └── pocketflow-integration.md
│   │   └── orchestration/            # Coordination system
│   │       ├── coordination.yaml
│   │       ├── dependency-validation.md
│   │       └── orchestrator-hooks.md
│   └── workflows/                    # Generated PocketFlow code
│
├── instructions/                     # Single source of truth
│   ├── core/                         # Base Agent OS instructions
│   │   ├── analyze-product.md
│   │   ├── create-spec.md
│   │   ├── execute-task.md
│   │   ├── execute-tasks.md
│   │   └── plan-product.md
│   └── meta/
│       └── pre-flight.md
│
├── templates/                        # Single template location
│   ├── fastapi-templates.md
│   ├── pocketflow-templates.md
│   └── task-templates.md
│
├── src/                              # Implementation code
│   ├── flows/
│   ├── nodes/
│   ├── schemas/
│   └── utils/
│
└── [other directories remain unchanged]
```

## Benefits

1. **No More 5x Duplication** - Core instructions exist in one place
2. **Clear Separation** - Base instructions vs PocketFlow extensions
3. **Simpler Mental Model** - One source of truth for each file type
4. **Easier Maintenance** - Update once, reflected everywhere
5. **Reduced Confusion** - No questioning which file is "active"

## How It Works

- **Base Instructions**: Live in `instructions/core/`
- **Runtime Access**: `.agent-os/instructions/core` symlinks to base
- **Extensions**: PocketFlow-specific features in `.agent-os/instructions/extensions/`
- **Orchestration**: Coordination logic in `.agent-os/instructions/orchestration/`
- **Templates**: Single location at `templates/`

## Migration Notes

If you had local modifications in any of the removed directories:
- `.agent-os/backup/` - Check git history for any unique changes
- `commands/` - Content identical to `instructions/core/`
- `.agent-os/templates/` - Content moved to `templates/`