# Subfolder CLAUDE.md Implementation Plan

## Research Summary

### Best Practices Discovered

#### 1. Hierarchical Organization Support
- **Automatic Discovery**: Claude recursively loads CLAUDE.md files from both root and subdirectories
- **Monorepo Pattern**: Multiple CLAUDE.md files at different levels create layered context
- **Import Depth**: Support for recursive imports up to 5 levels deep
- **Context Layering**: Files at different directory levels provide appropriate context scope

#### 2. Import and Cross-Reference Mechanisms
- **Local References**: `@path/to/import` syntax for project-relative imports
- **Global References**: `@~/.agent-os/` syntax for framework-wide standards
- **Recursive Imports**: Enable modular organization with clear dependency chains
- **Cross-Document Links**: Establish connections between related documentation

#### 3. Content Organization Principles
- **Modular Boundaries**: Clear markdown formatting prevents instruction bleed
- **Context Specificity**: Folder-specific guidance reduces cognitive load
- **Scope Clarity**: Distinct separation between framework and application guidance
- **Preservation Strategy**: Smart merge capabilities for existing content

#### 4. Framework vs Usage Distinction
- **Framework Guidance**: Focus on component usage, not application development
- **Template Customization**: Guide end-users on safe customization practices
- **Boundary Documentation**: Explain when to modify vs when to regenerate
- **Component Integration**: How framework pieces work together

#### 5. Be concise and focused to keep new CLAUDE.md files focused and manageable.

## Action Plan

### Phase 1: Template Design and Creation

#### 1.1 Design Framework-Specific Templates
**Objective**: Create contextual CLAUDE.md templates for each `.agent-os/` subdirectory

**Approach**:
- Focus on **framework component guidance**, not application development
- Provide **template customization instructions** for end-users
- Explain **framework vs generated code boundaries**
- Document **safe modification practices**

#### 1.2 Target Directories and Content Scope

##### `.agent-os/framework-tools/CLAUDE.md`
**Content Focus**: Framework utility usage and customization
- **Generator Usage**: How to use pattern generators and template system
- **Validation Tools**: Pattern analyzers, validators, and quality checks
- **Smart Features**: Context management, coordination, and optimization
- **Extension Points**: Safe customization and enhancement practices

##### `.agent-os/instructions/core/CLAUDE.md`
**Content Focus**: Workflow instruction customization
- **Modification Guidelines**: Safe ways to customize core workflow instructions
- **Extension Patterns**: How to add project-specific workflow steps
- **Consistency Maintenance**: Preserving framework design-first methodology
- **Integration Points**: How custom instructions work with sub-agents

##### `.agent-os/product/CLAUDE.md`
**Content Focus**: Product planning document management
- **Document Standards**: Mission, tech-stack, roadmap, and design document formats
- **Evolution Guidelines**: How product documents should evolve over time
- **Cross-Reference Management**: Maintaining links between product documents
- **Planning Workflow**: Design-first methodology enforcement

##### `.agent-os/standards/CLAUDE.md`
**Content Focus**: Standards customization and framework compatibility
- **Customization Guidelines**: How to safely modify standards while maintaining framework compatibility
- **Override Hierarchy**: Understanding global vs project-specific standards
- **PocketFlow Integration**: How standards enforce PocketFlow architectural patterns
- **Team Collaboration**: Shared standards management and version control

### Phase 2: Template Implementation

#### 2.1 Template Creation Process
1. **Research Existing Patterns**: Analyze current framework documentation patterns
2. **Draft Content**: Create comprehensive guidance for each directory
3. **Cross-Reference Integration**: Establish proper import chains and links
4. **Validation**: Ensure templates align with framework principles

#### 2.2 Content Structure for Each Template
```markdown
# Framework Component Guidance
## Overview
- Component purpose and scope
- When to use vs when to modify
- Framework vs usage boundaries

## Usage Guidelines
- Safe customization practices
- Extension points and patterns
- Common pitfalls to avoid

## Integration
- Cross-references to related components
- Import chains and dependencies
- Framework consistency requirements

## Examples
- Template customization examples
- Common modification patterns
- Best practice implementations
```

### Phase 3: Installation Integration

#### 3.1 Update Setup Scripts
**Target**: `setup/project.sh` - Framework installation script

**Changes Required**:
- Add logic to install subfolder CLAUDE.md files
- Ensure templates are copied to appropriate locations
- Validate installation completeness
- Maintain v1.4.0 architecture compatibility

#### 3.2 Installation Strategy
```bash
# New installation steps in setup/project.sh
install_subfolder_claude_md() {
    cp "$FRAMEWORK_PATH/templates/claude-md/framework-tools.md" \
       "$PROJECT_PATH/.agent-os/framework-tools/CLAUDE.md"

    cp "$FRAMEWORK_PATH/templates/claude-md/instructions-core.md" \
       "$PROJECT_PATH/.agent-os/instructions/core/CLAUDE.md"

    cp "$FRAMEWORK_PATH/templates/claude-md/product.md" \
       "$PROJECT_PATH/.agent-os/product/CLAUDE.md"

    cp "$FRAMEWORK_PATH/templates/claude-md/standards.md" \
       "$PROJECT_PATH/.agent-os/standards/CLAUDE.md"
}
```

### Phase 4: Validation and Testing

#### 4.1 Template Validation
- **Content Quality**: Ensure guidance is accurate and helpful
- **Cross-Reference Accuracy**: Verify all imports and links work
- **Framework Alignment**: Confirm templates support framework principles
- **End-User Testing**: Validate templates provide value to developers

#### 4.2 Installation Testing
- **Clean Installation**: Test templates install correctly in new projects
- **Existing Project Compatibility**: Ensure no conflicts with existing setups
- **Cross-Platform Support**: Validate installation works across environments
- **Integration Testing**: Confirm templates work with Claude Code workflows

## Implementation Timeline

### Session 1 (Current)
- [x] Research best practices for subfolder CLAUDE.md files
- [x] Create this implementation plan document
- [ ] Design framework-specific template structure
- [ ] Create first template (framework-tools)

### Session 2
- [ ] Complete remaining templates (instructions/core, product, standards)
- [ ] Implement cross-reference integration
- [ ] Create template validation framework

### Session 3
- [ ] Update setup/project.sh with installation logic
- [ ] Test installation process
- [ ] Validate template functionality

### Session 4
- [ ] End-user testing and feedback collection
- [ ] Refinement and optimization
- [ ] Documentation updates and finalization

## Success Criteria

### Template Quality
- ✅ **Contextual Relevance**: Each template provides specific guidance for its directory
- ✅ **Framework Alignment**: Templates reinforce framework principles and patterns
- ✅ **Safe Customization**: Clear guidance on what can be modified safely
- ✅ **Cross-Integration**: Proper links and imports between templates

### Installation Success
- ✅ **Automatic Installation**: Templates install without user intervention
- ✅ **No Conflicts**: Installation doesn't break existing functionality
- ✅ **Cross-Platform**: Works on all supported operating systems
- ✅ **Version Compatibility**: Maintains v1.4.0 architecture standards

### End-User Value
- ✅ **Reduced Confusion**: Clear guidance prevents framework misuse
- ✅ **Faster Onboarding**: New team members understand framework components
- ✅ **Better Customization**: Users can safely extend framework functionality
- ✅ **Consistent Usage**: Teams use framework components consistently

## Risk Mitigation

### Content Complexity Risk
- **Risk**: Templates become too complex or overwhelming
- **Mitigation**: Focus on essential guidance, use clear examples, maintain concise format

### Maintenance Burden Risk
- **Risk**: Multiple CLAUDE.md files become difficult to maintain
- **Mitigation**: Use import chains to reduce duplication, establish clear update procedures

### User Confusion Risk
- **Risk**: Multiple instruction files create confusion about hierarchy
- **Mitigation**: Clear documentation of override hierarchy, consistent cross-references

### Framework Drift Risk
- **Risk**: Templates encourage framework modifications that break compatibility
- **Mitigation**: Emphasize safe customization practices, provide clear boundaries

## Framework vs Usage Reminder

🎯 **CRITICAL**: This implementation creates **framework templates** that will be **installed into end-user projects**.

**Framework Repository (this repo)**:
- Creates CLAUDE.md templates for framework components
- Generates installation logic for setup scripts
- Defines safe customization boundaries
- Documents framework component interactions

**End-User Projects (after installation)**:
- Receive contextual CLAUDE.md files in `.agent-os/` subdirectories
- Get guidance on framework component usage
- Learn safe customization practices
- Understand framework vs application boundaries

**Key Principle**: These templates guide end-users on **using the framework effectively**, not on **developing the framework itself**.