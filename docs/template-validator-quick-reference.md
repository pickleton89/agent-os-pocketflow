# Template Validator Quick Reference

> Agent OS + PocketFlow Framework - Template Validator Commands & Usage
> Last Updated: 2025-01-18

---

## Quick Commands

### Validate Generated Template
```bash
# Using bash script (recommended)
bash scripts/validation/validate-template-structure.sh path/to/template

# Using Python module directly
python .agent-os/workflows/template_validator.py path/to/template

# Check if validation system is properly installed
bash scripts/validation/validate-sub-agents.sh
```

### Run All Framework Validation
```bash
# Complete framework validation suite
./scripts/run-all-tests.sh

# Specific validation suites
./scripts/validation/validate-integration.sh
./scripts/validation/validate-orchestration.sh
./scripts/validation/validate-end-to-end.sh
```

---

## Automatic Validation

### During Template Generation
The Template Validator runs automatically when templates are generated:

```bash
cd .agent-os/workflows
python generator.py --spec myspec.yaml
# Output includes:
# ✅ Template validation passed!
# or
# ❌ Template validation issues found:
#   • Error: Missing required method...
```

### Integration Points
- **Generator Pipeline**: Automatic validation after template creation
- **Template-Validator Agent**: Proactively invoked for template operations
- **Bash Scripts**: Manual validation of existing templates

---

## Validation Categories

### ✅ What Gets Validated

#### 1. Python Syntax
- AST parsing success
- Import statement correctness
- Function/class definition syntax
- String formatting and escaping

#### 2. PocketFlow Patterns  
- Node class inheritance (Node, AsyncNode, BatchNode)
- Required methods: prep(), exec()/exec_async(), post()
- Method signatures and parameter types
- Flow class structure and connectivity

#### 3. Educational Quality
- TODO comment presence and quality
- NotImplementedError usage in utilities
- Framework vs usage distinction
- Learning value assessment

#### 4. Structure Requirements
- Required files: nodes.py, flow.py, schemas/models.py
- Package initialization files
- Import dependencies
- Graph connectivity logic

### ⚠️ What Does NOT Get Validated
- **Business Logic**: Templates should have placeholders, not implementations
- **Runtime Functionality**: Templates are learning tools, not working applications
- **External Dependencies**: Validation focuses on structure, not runtime behavior
- **User Customizations**: Templates are starting points for user implementation

---

## Understanding Validation Results

### Error Levels
- **❌ ERROR**: Blocks template usage (syntax errors, missing required methods)
- **⚠️ WARNING**: Should be addressed (quality issues, missing imports)
- **ℹ️ INFO**: Optional improvements (additional TODO comments, style suggestions)

### Example Output
```bash
📋 Template Validation Report
========================================
Errors: 0 | Warnings: 3 | Info: 2

## Patterns Issues (0)
✅ All PocketFlow patterns valid

## Quality Issues (3)
⚠️ utils/process_data.py
   Found 1 generic TODO comments
   💡 Make TODO comments more specific and educational

## Framework Issues (2)
ℹ️ __init__.py
   No TODO comments found - consider adding educational placeholders
```

---

## Common Validation Scenarios

### ✅ Healthy Template
- All Python files have valid syntax
- PocketFlow nodes have required methods
- TODO comments are educational and specific
- Flow graph is properly connected
- Educational placeholders throughout

### ❌ Problematic Template
- Syntax errors in generated Python code
- Missing prep/exec/post methods in nodes
- Generic "TODO: implement" comments
- Missing required files or imports
- Completed implementations violating framework philosophy

---

## Framework Context Reminder

### This is a Framework Repository
- Templates are generated FOR other projects
- Missing implementations are intentional design features
- TODO stubs and NotImplementedError are educational tools
- Validation ensures template quality, not completeness

### Template Purpose
- **Starting Points**: Templates provide structure, not solutions
- **Educational**: Code shows patterns and guides implementation
- **Flexible**: Users customize templates for their specific needs
- **Standards-Compliant**: Templates follow PocketFlow and Python best practices

---

## Quick Troubleshooting

### "Syntax error: unexpected character"
**Fix**: Check generator.py for escaped newlines (`\\n` should be `\n`)

### "Missing required method"
**Fix**: Update generator to include all PocketFlow required methods

### "Template validation module not available"  
**Fix**: Check that `.agent-os/workflows/template_validator.py` exists and Python path is correct

### "Generic TODO comments"
**Fix**: Enhance generator smart defaults with specific, educational guidance

---

## Integration with Development Workflow

### Framework Development
1. Make changes to generator or templates
2. Generate test template to verify changes
3. Validation runs automatically during generation
4. Address any validation issues before committing

### Template Quality Assurance
1. Regular validation of existing templates
2. Update validation criteria as PocketFlow evolves
3. Maintain educational value in generated content
4. Ensure framework vs usage distinction

---

For detailed troubleshooting, see [template-validator-troubleshooting.md](template-validator-troubleshooting.md)

For validation criteria details, see [.agent-os/instructions/orchestration/template-standards.md](.agent-os/instructions/orchestration/template-standards.md)