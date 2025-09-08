# PocketFlow Tools Implementation Plan for End-User Projects

## Executive Summary

This plan outlines how to properly integrate the `pocketflow-tools/` Python tools into end-user projects, ensuring they are accessible via command-line, sub-agents in `claude-code/agents/`, and instruction files. The current gap is that while the framework installs the pocketflow_tools package (installable CLI), it doesn't properly copy the developer tools (`pocketflow-tools/` directory) that agents and instructions need to invoke.

## Current State Analysis

### What Works
1. **Base Installation** (`setup/base.sh`):
   - Installs pocketflow_tools package via `uv pip install -e .`
   - Copies pocketflow-tools/*.py files to `~/.agent-os/pocketflow-tools/`
   - Verifies CLI availability via `uv run python -m pocketflow_tools.cli`

2. **Project Installation** (`setup/project.sh`):
   - Creates `.agent-os/` directory structure in project
   - Checks for pocketflow_tools CLI availability
   - Does NOT copy pocketflow-tools files to project

### The Gap
- **Missing Link**: End-user projects don't have access to the Python tools in `pocketflow-tools/` directory
- **Agent References**: Agents reference tools like `python3 pocketflow-tools/pattern_analyzer.py` but these files don't exist in the project
- **Instruction References**: Instructions expect to call `python3 pocketflow-tools/template_validator.py` but path doesn't exist

## Implementation Architecture

### Three-Layer Tool System

#### Layer 1: Framework Package (`pocketflow_tools/`)
- **Purpose**: Installable Python package with CLI for workflow generation
- **Location**: Installed in Python environment via `uv pip install`
- **Usage**: `uv run python -m pocketflow_tools.cli --spec workflow.yaml`
- **Status**: ✅ Working

#### Layer 2: Developer Tools (`pocketflow-tools/`)
- **Purpose**: Analysis, validation, and orchestration tools
- **Location**: Should be in `.agent-os/pocketflow-tools/` in each project
- **Usage**: Direct Python invocation by agents/instructions
- **Status**: ❌ Not being copied to projects

#### Layer 3: Agent/Instruction Integration
- **Purpose**: Orchestrated tool invocation during workflows
- **Location**: References in `claude-code/agents/` and `instructions/`
- **Usage**: Called via subprocess or import by agents
- **Status**: ❌ Broken due to missing Layer 2

## Implementation Steps

### Phase 1: Fix Installation Scripts (Immediate)

#### 1.1 Update `setup/project.sh`
```bash
# Add after line 456 in install_pocketflow_tools()
# Copy developer tools from base installation or framework
if [[ "$NO_BASE_INSTALL" == "false" ]] && [[ -d "$BASE_INSTALL_PATH/pocketflow-tools" ]]; then
    log_info "Copying PocketFlow developer tools from base installation..."
    if safe_copy "$BASE_INSTALL_PATH/pocketflow-tools"/* ".agent-os/pocketflow-tools/" "pocketflow-tools"; then
        log_success "Copied PocketFlow developer tools"
    else
        log_error "Failed to copy PocketFlow developer tools"
        exit 1
    fi
else
    # Fallback: Copy from framework repository if available
    local framework_tools_dir="$(dirname "$(dirname "$(realpath "$0")")")/pocketflow-tools"
    if [[ -d "$framework_tools_dir" ]]; then
        log_info "Copying PocketFlow developer tools from framework..."
        cp "$framework_tools_dir"/*.py ".agent-os/pocketflow-tools/" 2>/dev/null || true
        log_success "Copied PocketFlow developer tools from framework"
    else
        log_warning "PocketFlow developer tools not found - agents may have limited functionality"
    fi
fi
```

### Phase 2: Create Tool Wrapper Scripts (Day 1-2)

#### 2.1 Create `.agent-os/pocketflow-tools/run.sh`
```bash
#!/bin/bash
# Wrapper script for running pocketflow-tools with proper Python environment
TOOL_NAME="$1"
shift
uv run python "$(dirname "$0")/${TOOL_NAME}.py" "$@"
```

#### 2.2 Update Agent References
- Change: `python3 pocketflow-tools/pattern_analyzer.py`
- To: `.agent-os/pocketflow-tools/run.sh pattern_analyzer`

### Phase 3: Implement Agent Coordination (Day 3-5)

#### 3.1 Create Coordination Module
Create `.agent-os/pocketflow-tools/coordinator.py`:
```python
"""Coordination module for agent-tool integration"""
import sys
import json
from pathlib import Path

# Add pocketflow-tools to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_coordination import coordinate_pattern_analysis, create_subagent_handoff
from pattern_analyzer import PatternAnalyzer
from dependency_orchestrator import DependencyOrchestrator

class ToolCoordinator:
    """Unified interface for agents to access pocketflow-tools"""
    
    def analyze_pattern(self, project_name: str, requirements: str) -> dict:
        """Analyze requirements and return pattern recommendation"""
        ctx = coordinate_pattern_analysis(project_name, requirements)
        handoff = create_subagent_handoff(ctx)
        return {
            "pattern": ctx.pattern_recommendation.primary_pattern.value,
            "confidence": ctx.pattern_recommendation.confidence_score,
            "handoff": handoff.payload,
            "target_agent": handoff.target_agent,
        }
    
    def generate_dependencies(self, project_name: str, pattern: str) -> dict:
        """Generate dependency configurations"""
        orch = DependencyOrchestrator()
        return {
            "pyproject": orch.generate_pyproject_toml(project_name, pattern),
            "uv_config": orch.generate_uv_config(project_name, pattern)
        }

if __name__ == "__main__":
    # CLI interface for agents
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["analyze", "deps"])
    parser.add_argument("--project", required=True)
    parser.add_argument("--requirements", help="Requirements text or file")
    parser.add_argument("--pattern", help="Pattern type")
    args = parser.parse_args()
    
    coordinator = ToolCoordinator()
    
    if args.command == "analyze":
        result = coordinator.analyze_pattern(args.project, args.requirements)
        print(json.dumps(result, indent=2))
    elif args.command == "deps":
        result = coordinator.generate_dependencies(args.project, args.pattern)
        print(json.dumps(result, indent=2))
```

### Phase 4: Update Agent Specifications (Day 5-7)

#### 4.1 Pattern Analyzer Agent Update
Update `claude-code/agents/pattern-analyzer.md`:
```markdown
## Tool Invocation

### Option 1: Direct Python (if in project)
```python
import sys
sys.path.append('.agent-os/pocketflow-tools')
from coordinator import ToolCoordinator

coordinator = ToolCoordinator()
result = coordinator.analyze_pattern(project_name, requirements)
```

### Option 2: CLI Invocation
```bash
cd .agent-os/pocketflow-tools
python coordinator.py analyze --project "$PROJECT" --requirements "$REQUIREMENTS"
```
```

#### 4.2 Update All Agent TODOs
Replace TODO placeholders in agents with actual invocation code:
- `design-document-creator.md`: Add workflow graph generation
- `dependency-orchestrator.md`: Add dependency generation calls
- `template-validator.md`: Add validation invocations
- `strategic-planner.md`: Add pattern analysis integration

### Phase 5: Instruction File Updates (Day 7-9)

#### 5.1 Core Instructions
Update instructions to use proper tool paths:
- `instructions/core/create-spec.md`: Add context manager invocation
- `instructions/core/execute-task.md`: Add status reporter integration
- `instructions/orchestration/template-standards.md`: Fix validator path

#### 5.2 Create Helper Scripts
Create `.agent-os/bin/` directory with wrapper scripts:
```bash
# .agent-os/bin/analyze-pattern
#!/bin/bash
exec python3 .agent-os/pocketflow-tools/coordinator.py analyze "$@"
```

### Phase 6: Testing & Validation (Day 10-12)

#### 6.1 Integration Tests
Create `test_pocketflow_integration.sh`:
```bash
#!/bin/bash
# Test that all tools are accessible in a project

# Test 1: CLI availability
uv run python -m pocketflow_tools.cli --help || exit 1

# Test 2: Developer tools availability
python3 .agent-os/pocketflow-tools/pattern_analyzer.py --help || exit 1

# Test 3: Coordinator module
python3 .agent-os/pocketflow-tools/coordinator.py analyze \
    --project test --requirements "Build a RAG system" || exit 1

# Test 4: Agent invocation simulation
# ... additional tests
```

## Migration Path for Existing Projects

### For Projects Without Tools
1. Run updated `setup/project.sh` with `--update-tools` flag
2. Verify tools copied to `.agent-os/pocketflow-tools/`
3. Test agent invocations

### For Projects With Old Structure
1. Backup existing `.agent-os/` directory
2. Run migration script (to be created)
3. Validate all tools accessible

## Success Criteria

### Immediate (Phase 1)
- [ ] Developer tools copied to project during installation
- [ ] Basic Python invocation works: `python3 .agent-os/pocketflow-tools/pattern_analyzer.py`

### Short-term (Phase 2-3)
- [ ] Wrapper scripts simplify invocation
- [ ] Coordinator module provides unified interface
- [ ] Agents can successfully call tools

### Complete (Phase 4-6)
- [ ] All agent TODOs replaced with working code
- [ ] Instructions properly reference tool paths
- [ ] End-to-end workflow tested and documented
- [ ] Integration tests pass

## Risk Mitigation

### Path Issues
- **Risk**: Tools not found due to path problems
- **Mitigation**: Use absolute paths or path resolution in wrapper scripts

### Python Environment
- **Risk**: Import errors due to environment issues
- **Mitigation**: Always use `uv run` for consistent environment

### Backwards Compatibility
- **Risk**: Breaking existing projects
- **Mitigation**: Add version checking and migration scripts

## Recommended Immediate Actions

1. **Fix `setup/project.sh`** to copy pocketflow-tools (30 minutes)
2. **Create coordinator.py** module (2 hours)
3. **Update pattern-analyzer.md** agent with working code (1 hour)
4. **Test in a fresh project** (1 hour)
5. **Document the working flow** (30 minutes)

## Long-term Improvements

1. **Package pocketflow-tools** as a separate installable package
2. **Create MCP server** for tool access
3. **Build VS Code extension** for visual tool invocation
4. **Implement tool versioning** for compatibility

## Conclusion

The core issue is that `pocketflow-tools/` developer tools aren't being copied to end-user projects. The immediate fix is updating the installation scripts, followed by creating wrapper scripts and coordination modules to make the tools easily accessible to agents and instructions. This plan provides a clear path from the current broken state to a fully integrated tool system.