# Standards Customization Guide

## Overview
Framework standards that ensure consistency across your project while maintaining compatibility with the Agent OS + PocketFlow architecture. These standards provide the foundation for code quality, architectural patterns, and development workflows.

The standards directory contains customizable guidelines that bridge framework requirements with project-specific needs. Customize these standards carefully to maintain framework compatibility while adapting to your team's requirements.

## Override Hierarchy

Understanding the standards hierarchy ensures proper customization without breaking framework functionality:

### 1. **Project CLAUDE.md** (Highest Priority)
- **Location**: Root `CLAUDE.md` in your project
- **Scope**: Project-wide overrides and custom requirements
- **Purpose**: Define project-specific development guidelines and team conventions
- **Override Capability**: Can override any lower-level standard while maintaining framework compatibility

### 2. **Local Standards** (`.agent-os/standards/`)
- **Location**: Project-specific standards in `.agent-os/standards/`
- **Scope**: Framework component customizations
- **Purpose**: Adapt framework standards to project requirements
- **Override Capability**: Extends and customizes base installation standards

### 3. **Base Installation Standards** (`~/.agent-os/`)
- **Location**: User's base Agent OS installation
- **Scope**: Cross-project standards and team-wide conventions
- **Purpose**: Consistent standards across multiple projects
- **Override Capability**: Provides defaults that can be overridden by project-specific standards

### 4. **Framework Defaults** (Lowest Priority)
- **Location**: Agent OS + PocketFlow framework installation
- **Scope**: Core framework requirements and architectural patterns
- **Purpose**: Ensure PocketFlow compatibility and design-first methodology
- **Override Capability**: Baseline standards that should rarely be overridden

## Safe Customization Practices

### ✅ Recommended Customizations

#### Project-Specific Code Style Rules
- Add language-specific formatting preferences
- Define naming conventions for your domain
- Establish code organization patterns
- Set up project-specific linting rules

#### PocketFlow Pattern Extensions
- Create domain-specific node types
- Define custom data flow patterns
- Establish integration patterns for your architecture
- Add project-specific validation rules

#### Team Conventions
- Document development workflow preferences
- Define code review standards
- Establish testing and quality assurance guidelines
- Set up documentation and communication standards

#### Tool Integration
- Configure project-specific development tools
- Set up continuous integration standards
- Define deployment and DevOps conventions
- Establish monitoring and observability standards

### ❌ Critical Boundaries - Avoid These Changes

#### PocketFlow Architectural Patterns
- Don't break core PocketFlow node communication patterns
- Don't bypass SharedStore data management requirements
- Don't eliminate error handling and validation patterns
- Don't remove design-first methodology enforcement

#### Framework Integration Requirements
- Don't remove design-first validation requirements
- Don't bypass template generation workflows
- Don't eliminate cross-agent coordination patterns
- Don't break document evolution and cross-reference systems

#### Core Development Methodology
- Don't skip product planning and architectural design phases
- Don't bypass feature specification and design validation
- Don't eliminate testing and quality assurance requirements
- Don't remove framework compatibility validation

## Standards Categories

### Code Quality Standards
- **Formatting**: Language-specific code formatting rules
- **Naming**: Variable, function, and class naming conventions
- **Organization**: File and directory structure patterns
- **Documentation**: Code commenting and documentation requirements

### Architectural Standards
- **PocketFlow Integration**: Node types, data flows, and SharedStore usage
- **Design Patterns**: Consistent architectural pattern application
- **Integration Patterns**: Service integration and API design standards
- **Error Handling**: Consistent error handling and validation approaches

### Development Workflow Standards
- **Design-First**: Architectural design and validation requirements
- **Feature Development**: Specification creation and implementation workflows
- **Testing**: Test coverage, quality, and automation standards
- **Code Review**: Review process, criteria, and approval requirements

### Team Collaboration Standards
- **Communication**: Documentation, meeting, and decision-making protocols
- **Version Control**: Git workflow, branching, and merge standards
- **Project Management**: Task tracking, milestone, and delivery standards
- **Knowledge Sharing**: Documentation, training, and onboarding practices

## PocketFlow Integration Standards

### Core Pattern Compliance
The framework ensures these PocketFlow patterns remain consistent:

#### Node Communication Patterns
- **Standard Interface**: All nodes implement consistent input/output interfaces
- **Error Propagation**: Standardized error handling and recovery patterns
- **State Management**: Consistent SharedStore integration for state persistence
- **Performance**: Standard monitoring and optimization patterns

#### Data Flow Architecture
- **Pipeline Design**: Consistent data transformation and processing patterns
- **Validation**: Standard data validation and schema enforcement
- **Caching**: Consistent caching strategies and cache invalidation
- **Monitoring**: Standard observability and debugging capabilities

#### Integration Boundaries
- **Service Integration**: Standard patterns for external service integration
- **API Design**: Consistent API design and versioning approaches
- **Database Integration**: Standard data access and migration patterns
- **Testing Integration**: Consistent testing patterns for PocketFlow components

### Customization Guidelines for PocketFlow

#### Safe Extensions
- **Custom Node Types**: Create domain-specific nodes that follow framework patterns
- **Data Flow Enhancements**: Add project-specific data transformation patterns
- **Integration Adapters**: Build custom integrations using framework interfaces
- **Validation Extensions**: Add business logic validation that complements framework validation

#### Pattern Preservation
- **Interface Consistency**: Maintain standard node interfaces while adding functionality
- **Error Handling**: Extend error handling without bypassing framework error patterns
- **State Management**: Use SharedStore patterns for all state management needs
- **Testing Patterns**: Follow framework testing patterns for all custom components

## Cross-References

### Framework Standards Integration
@pocket-flow.md - Core PocketFlow patterns, rules, and architectural requirements
@code-style/*.md - Language-specific standards and formatting guidelines
@best-practices.md - Development methodology and quality standards
@../instructions/core/ - Workflow integration requirements and validation standards

### Project Integration
@../../CLAUDE.md - Project-level standards and team conventions
@../product/ - Product planning standards and document evolution requirements
@../framework-tools/ - Tool integration and validation standards
@../specs/ - Feature specification standards and design validation requirements

## Customization Examples

### Project-Specific Code Style
```markdown
# In code-style/python.md, add project customizations:
## Project-Specific Python Standards
- Use domain-specific type hints for business objects
- Follow project naming patterns for database models
- Implement project-specific logging patterns
- Use project-specific error handling conventions
```

### Custom PocketFlow Patterns
```markdown
# In pocket-flow.md, add project extensions:
## Project-Specific Node Types
- PaymentProcessorNode: Handles payment flow integration
- NotificationNode: Manages multi-channel notifications
- AnalyticsNode: Processes user behavior analytics
- WorkflowNode: Orchestrates business process automation
```

### Team Workflow Standards
```markdown
# In best-practices.md, add team conventions:
## Team Development Standards
- Code review requires two approvals for production changes
- All features require design documents before implementation
- Test coverage must exceed 85% for new code
- Documentation updates required for all public API changes
```

## Standards Evolution

### Maintenance Responsibilities
- **Framework Compatibility**: Ensure customizations don't break framework integration
- **Team Alignment**: Keep standards synchronized across team members
- **Documentation Currency**: Maintain accurate and up-to-date standard documentation
- **Quality Validation**: Regularly validate that standards improve development quality

### Update Strategies
- **Incremental Evolution**: Make small, validated changes rather than major overhauls
- **Team Consensus**: Ensure team agreement on standard changes before implementation
- **Framework Alignment**: Validate that custom standards support framework methodology
- **Continuous Improvement**: Regularly review and refine standards based on development experience

The standards system provides flexibility for project customization while ensuring framework compatibility and team consistency. Focus on extending and enhancing framework capabilities rather than replacing core functionality.