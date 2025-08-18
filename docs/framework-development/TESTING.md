# Testing the Framework

> **Testing the Agent OS + PocketFlow Framework Itself**

## ⚠️ Framework Testing Context

**This guide covers testing the framework, NOT applications built with it.**

We test:
- ✅ Template generation logic
- ✅ Validation systems  
- ✅ Sub-agent coordination
- ✅ Framework installation
- ❌ End-user applications (that's for generated projects)

---

## Running Framework Tests

### Complete Test Suite
```bash
# Run all framework validation tests
./scripts/run-all-tests.sh
```

### Individual Test Suites
```bash
# Integration tests
./scripts/validation/validate-integration.sh

# Orchestration validation  
./scripts/validation/validate-orchestration.sh

# End-to-end framework testing
./scripts/validation/validate-end-to-end.sh

# Template structure validation
./scripts/validation/validate-template-structure.sh
```

### Sub-Agent Testing
```bash
# Test pattern recognition
python .agent-os/workflows/test_pattern_recognizer.py

# Test dependency orchestrator
python .agent-os/workflows/test_dependency_orchestrator.py

# Test template validator
python .agent-os/workflows/test_full_generation_with_dependencies.py
```

---

## What We Test

### 1. Template Generation
- Generator creates proper file structures
- Templates contain correct placeholder TODOs
- Generated code follows PocketFlow patterns
- Sub-agents enhance template quality

### 2. Framework Installation
- Setup scripts work correctly
- Agent configurations are valid
- Coordination system functions
- Dependencies are properly configured

### 3. Pattern Recognition
- Pattern analyzer identifies correct patterns
- Confidence scoring works properly
- Template customization is appropriate
- Integration with orchestrator functions

### 4. Validation Systems
- Template validator catches structural issues
- Framework vs usage distinction maintained
- Educational placeholder quality enforced
- Generated code follows best practices

---

## Test Philosophy

### Framework Tests Should:
- ✅ Test the generator itself
- ✅ Validate template structure (not content implementation)
- ✅ Ensure proper placeholder TODOs are created
- ✅ Verify framework installation works
- ✅ Test agent coordination

### Framework Tests Should NOT:
- ❌ Test business logic in generated templates
- ❌ Require PocketFlow runtime dependencies
- ❌ Validate application functionality
- ❌ Complete TODO implementations

---

## Test Structure

```
tests/
├── framework/          # Framework internals
│   ├── test_generator.py
│   ├── test_validation.py
│   └── test_coordination.py
├── templates/          # Template generation
│   ├── test_structure.py
│   ├── test_placeholders.py
│   └── test_patterns.py
└── integration/        # End-to-end framework tests
    ├── test_setup.py
    └── test_workflow.py
```

---

## Adding New Tests

When adding framework functionality:

1. **Test the Generator Logic** - Ensure it creates proper templates
2. **Test Validation Rules** - Ensure quality standards are maintained  
3. **Test Integration Points** - Ensure components work together
4. **Update Test Documentation** - Keep this guide current

Remember: We test the framework's ability to generate good starting points, not the end-user's ability to complete them.