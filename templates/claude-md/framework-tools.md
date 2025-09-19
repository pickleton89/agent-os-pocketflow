# Framework Tools Guidance

## Overview
These tools generate PocketFlow templates and validate patterns. They are part of the framework, not your application code.

The framework-tools directory contains utilities that orchestrate template generation, pattern validation, and agent coordination. These tools enable the design-first methodology by providing generators and validators that ensure architectural consistency.

## Usage Guidelines

### Pattern Generators
- Use pattern generators via `.agent-os/framework-tools/` Python scripts
- Run `uv run python .agent-os/framework-tools/coordinator.py info` to see available PocketFlow patterns
- Use `uv run python .agent-os/framework-tools/coordinator.py generate` to create dependency configurations
- All generators create starter templates with TODO placeholders for customization

### Validation Tools
- Run validation with `uv run python .agent-os/framework-tools/check-pocketflow-install.py`
- Use `uv run python .agent-os/framework-tools/pattern_analyzer.py` to validate pattern compliance
- Validate integration with framework validation suites
- Validation ensures design-first methodology compliance

### Agent Coordination
- Coordinate agents with `uv run python .agent-os/framework-tools/coordinator.py`
- Use for parallel document creation and task orchestration
- Handles dependency management between specialized agents
- Optimizes performance for complex multi-agent workflows

### Template System
- Templates in `generator.py` create PocketFlow project structures
- Generated code includes intentional TODO placeholders
- Templates provide architectural foundation with guided customization points
- Focus on enabling developers, not replacing developer decisions

## Safe Customization

### ✅ Recommended Extensions
- Add new pattern validators in separate files
- Extend coordinator with project-specific logic
- Create custom template additions for domain-specific patterns
- Add project-specific validation rules that complement framework standards

### ❌ Avoid These Modifications
- Don't modify core generator.py logic (breaks template integrity)
- Don't change pattern analyzer fundamentals (affects validation consistency)
- Don't bypass design-first validation requirements
- Don't remove TODO placeholders from generated templates

### Extension Points
- Custom validators: Add to `validators/` subdirectory
- Project logic: Extend coordinator through configuration
- Template additions: Use template inheritance patterns
- Domain patterns: Create supplementary pattern definitions

## Integration

### Cross-References
@../standards/pocket-flow.md - Pattern specifications and architectural rules
@../instructions/core/create-spec.md - Specification workflow integration
@../instructions/core/plan-product.md - Product planning coordination
@../../CLAUDE.md - Project-level framework usage instructions

### Framework Dependencies
- Templates depend on PocketFlow pattern definitions
- Validation requires standards compliance
- Coordination integrates with instruction workflows
- Generated code follows architectural boundaries

### Development Workflow Integration
The framework tools integrate with the overall design-first methodology:

1. **Planning Phase**: Tools validate product architecture requirements
2. **Specification Phase**: Generators create feature specification templates
3. **Implementation Phase**: Validators ensure design compliance before coding
4. **Testing Phase**: Framework tools validate implementation matches design

## Framework vs Application Boundary

**CRITICAL UNDERSTANDING**: These tools generate framework components for your application - they are not part of your application logic.

### Framework Components (these tools)
- Generate PocketFlow templates and validation rules
- Create agent coordination infrastructure
- Provide architectural pattern enforcement
- Enable design-first methodology through tooling

### Application Components (what gets generated)
- PocketFlow nodes and data flows
- Business logic implementation stubs
- Feature-specific specifications
- Application-level integration patterns

The framework tools create the foundation and guardrails. Your application implements the business logic within that architectural framework.