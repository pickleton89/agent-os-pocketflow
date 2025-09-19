# Workflow Instructions Customization

## Overview
Core workflow instructions that orchestrate the design-first methodology. These instructions define how agents coordinate product planning, feature specification, and implementation phases.

The instructions/core directory contains the fundamental workflow definitions that ensure architectural consistency and design-first compliance across all development activities. Modify these instructions with caution to maintain framework integrity.

## Safe Customization Practices

### ✅ Recommended Customizations
- Add project-specific validation steps to existing workflows
- Extend pre/post execution hooks for custom quality gates
- Add custom quality gates that complement design-first requirements
- Integrate project-specific tools with existing workflow steps
- Add domain-specific document sections to specification templates

### ❌ Critical Boundaries - Do Not Modify
- Don't remove design-first requirements (breaks architectural foundation)
- Don't bypass validation steps (compromises quality assurance)
- Don't skip product planning phases (undermines methodology)
- Don't eliminate cross-agent coordination (creates workflow fragmentation)
- Don't remove template generation steps (breaks consistency)

### Extension Strategies
- **Validation Extensions**: Add to existing validation without replacing core checks
- **Hook Integration**: Use pre/post hooks rather than modifying core logic
- **Quality Gates**: Layer additional checks on top of framework requirements
- **Tool Integration**: Extend existing steps rather than creating parallel workflows

## Workflow Integration Points

### Product Planning Customization
- **Pre-flight checks**: Add custom requirements in `meta/pre-flight.md`
- **Mission validation**: Extend mission document requirements
- **Technology selection**: Add domain-specific technology validation
- **Architectural planning**: Integrate custom architectural patterns

### Specification Customization
- **Custom specs**: Extend `create-spec.md` templates with domain requirements
- **Feature validation**: Add business logic validation to specification workflow
- **Integration planning**: Enhance integration requirement templates
- **Testing strategy**: Extend testing specification requirements

### Implementation Customization
- **Task execution**: Hook into `execute-tasks.md` with custom pre-implementation checks
- **Code generation**: Extend template generation with project-specific patterns
- **Quality validation**: Add custom quality gates to implementation workflow
- **Documentation**: Integrate custom documentation generation

### Cross-Agent Coordination
- **Document orchestration**: Customize parallel document creation workflows
- **Agent dependencies**: Define custom agent execution dependencies
- **Error handling**: Extend error handling and recovery procedures
- **Performance optimization**: Add custom coordination optimizations

## Workflow Architecture

### Design-First Enforcement
The core instructions ensure design-first methodology through:

1. **Validation Gates**: Prevent implementation without complete design
2. **Template Generation**: Create structured design document templates
3. **Cross-References**: Maintain consistency between planning and implementation
4. **Quality Assurance**: Validate architectural compliance at each phase

### Agent Orchestration
Instructions coordinate specialized agents for:

- **Document Creation**: Parallel generation of mission, roadmap, and design documents
- **Specification Management**: Feature specification creation and validation
- **Implementation Planning**: Task breakdown and dependency management
- **Quality Control**: Testing, validation, and compliance checking

### Workflow Phases
1. **Product Planning**: Mission definition, technology selection, roadmap creation
2. **Feature Specification**: Design extension, integration planning, testing strategy
3. **Implementation**: Task execution, code generation, validation
4. **Quality Assurance**: Testing, documentation, compliance verification

## Cross-References

### Framework Integration
@../../../CLAUDE.md - Project-level instructions and framework usage
@../standards/best-practices.md - Framework standards and compliance requirements
@../product/ - Product planning document templates and evolution guidelines
@../framework-tools/ - Generator and validation tool integration

### Workflow Dependencies
- **Product Planning** → **Feature Specification**: Design continuity validation
- **Feature Specification** → **Implementation**: Architectural compliance checking
- **Implementation** → **Quality Assurance**: Testing and validation integration
- **All Phases** → **Documentation**: Continuous documentation evolution

## Customization Examples

### Adding Custom Validation
```markdown
# In create-spec.md, add to validation section:
## Custom Business Logic Validation
- Validate feature aligns with business requirements
- Check integration with existing business processes
- Verify compliance with industry standards
- Ensure performance requirements are met
```

### Extending Quality Gates
```markdown
# In execute-tasks.md, add to pre-implementation:
## Custom Pre-Implementation Checks
- Security review completion
- Performance impact assessment
- User experience validation
- Accessibility compliance check
```

### Project-Specific Hooks
```markdown
# Create custom hook file: custom-hooks.md
## Pre-Planning Hook
- Initialize project-specific requirements
- Set up domain-specific validation rules
- Configure custom quality metrics

## Post-Implementation Hook
- Run custom test suites
- Generate project-specific documentation
- Update custom tracking systems
```

## Framework Compliance

### Mandatory Requirements
- Maintain design-first validation at all workflow phases
- Preserve cross-agent coordination and dependency management
- Keep template generation and architectural consistency checks
- Ensure documentation evolution and cross-reference maintenance

### Quality Standards
- All customizations must enhance, not replace, framework functionality
- Custom workflows must integrate with existing agent coordination
- Validation additions must complement, not bypass, design-first requirements
- Documentation customizations must maintain framework documentation standards

The core instructions provide the foundation for design-first methodology. Customizations should strengthen this foundation while respecting the architectural boundaries that ensure project consistency and quality.