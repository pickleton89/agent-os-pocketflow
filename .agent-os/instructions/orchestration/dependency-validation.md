# Cross-File Dependency Validation

## Dependency Chain
```
plan-product.md → create-spec.md → execute-tasks.md
                      ↓
               pocketflow-orchestrator
                      ↓  
              .agent-os/workflows/
```

## Validation Rules

### execute-tasks.md Dependencies
**Required Inputs:**
- [ ] `.agent-os/specs/[date-feature]/spec.md` (from create-spec.md)
- [ ] `.agent-os/workflows/[feature].py` (from orchestrator)
- [ ] `docs/design.md` (from orchestrator)
- [ ] Pydantic models defined (from orchestrator)

**Validation Logic:**
```python
def validate_execute_tasks_dependencies(feature_name: str) -> ValidationResult:
    """Validate all required inputs exist for execute-tasks.md"""
    
    missing = []
    
    # Check spec file
    spec_path = f".agent-os/specs/{get_latest_spec_folder(feature_name)}/spec.md"
    if not file_exists(spec_path):
        missing.append(f"Spec file: {spec_path}")
    
    # Check workflow implementation
    workflow_path = f".agent-os/workflows/{feature_name}.py"
    if not file_exists(workflow_path):
        missing.append(f"Workflow: {workflow_path}")
    
    # Check design document
    design_path = "docs/design.md"
    if not file_exists(design_path) or not is_complete(design_path):
        missing.append(f"Design document: {design_path}")
    
    # Check for Pydantic models
    if not has_pydantic_models(workflow_path):
        missing.append("Pydantic models not defined in workflow")
    
    if missing:
        return ValidationResult(
            valid=False,
            missing_dependencies=missing,
            resolution="invoke_orchestrator_for_missing_dependencies"
        )
    
    return ValidationResult(valid=True)
```

### create-spec.md Dependencies  
**Required Inputs:**
- [ ] `.agent-os/product/mission.md` (from plan-product.md)
- [ ] `.agent-os/product/roadmap.md` (from plan-product.md)
- [ ] `.agent-os/product/tech-stack.md` (from plan-product.md)

**Optional Orchestrator Outputs:**
- [ ] `.agent-os/workflows/[feature].py` (if LLM/AI feature)
- [ ] `docs/design.md` (if complex feature)

## Dependency Resolution Protocol

### Step 1: Detect Missing Dependencies
```python
def check_dependencies(instruction_file: str, context: dict) -> List[Dependency]:
    """Check all dependencies for current instruction file"""
    
    config = load_coordination_config()
    dependencies = config[instruction_file]["depends_on"]
    
    missing_deps = []
    for dep in dependencies:
        if not validate_dependency(dep, context):
            missing_deps.append(dep)
    
    return missing_deps
```

### Step 2: Auto-Resolution
```python
def resolve_dependencies(missing_deps: List[Dependency], context: dict):
    """Automatically resolve missing dependencies"""
    
    for dep in missing_deps:
        if dep.type == "instruction_file":
            # Invoke prerequisite instruction file
            invoke_instruction_file(dep.file, context)
        
        elif dep.type == "orchestrator_output":
            # Invoke orchestrator to generate missing output
            invoke_orchestrator_for_output(dep.output_type, context)
        
        elif dep.type == "validation_gate":
            # Run validation and fix if possible
            validation_result = run_validation(dep.validation_type, context)
            if not validation_result.valid:
                invoke_repair_action(validation_result.repair_action, context)
```

### Step 3: Failure Handling
```python
def handle_dependency_failure(dep: Dependency, context: dict):
    """Handle cases where dependency cannot be resolved"""
    
    if dep.critical:
        # Block progression with clear error message
        raise DependencyError(
            f"Critical dependency {dep.name} cannot be resolved. "
            f"Please {dep.manual_resolution_instruction}"
        )
    else:
        # Warn user but allow graceful degradation
        warn(f"Optional dependency {dep.name} missing. Continuing with reduced functionality.")
```