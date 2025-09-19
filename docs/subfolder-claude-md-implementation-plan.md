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
1. **Create Template Directory**: Establish `templates/claude-md/` to store all CLAUDE.md templates
2. **Draft Content**: Create comprehensive guidance for each directory following the content structure
3. **Cross-Reference Integration**: Establish proper import chains using `@path/to/import` syntax
4. **Validation**: Ensure templates align with framework principles and v1.4.0 architecture

#### 2.2 Template Files to Create
- **`templates/claude-md/framework-tools.md`**: For `.agent-os/framework-tools/CLAUDE.md`
- **`templates/claude-md/instructions-core.md`**: For `.agent-os/instructions/core/CLAUDE.md`
- **`templates/claude-md/product.md`**: For `.agent-os/product/CLAUDE.md`
- **`templates/claude-md/standards.md`**: For `.agent-os/standards/CLAUDE.md`

#### 2.3 Content Structure for Each Template
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
```

#### 2.4 Detailed Template Content Specifications

##### Framework-Tools Template (`framework-tools.md`)
```markdown
# Framework Tools Guidance

## Overview
These tools generate PocketFlow templates and validate patterns. They are part of the framework, not your application code.

## Usage Guidelines
- Use pattern generators via `.agent-os/bin/` commands
- Run validation with `check-pocketflow-install.py`
- Coordinate agents with `coordinator.py`
- Analyze patterns with `pattern_analyzer.py`

## Safe Customization
- ✅ Add new pattern validators in separate files
- ✅ Extend coordinator with project-specific logic
- ❌ Don't modify core generator.py logic
- ❌ Don't change pattern analyzer fundamentals

## Integration
@../standards/pocket-flow.md - Pattern specifications
@../instructions/core/create-spec.md - Specification workflow
```

##### Instructions-Core Template (`instructions-core.md`)
```markdown
# Workflow Instructions Customization

## Overview
Core workflow instructions that orchestrate the design-first methodology. Modify with caution.

## Safe Customization Practices
- ✅ Add project-specific validation steps
- ✅ Extend pre/post execution hooks
- ✅ Add custom quality gates
- ❌ Don't remove design-first requirements
- ❌ Don't bypass validation steps

## Workflow Integration Points
- Pre-flight checks: Add in `meta/pre-flight.md`
- Custom specs: Extend `create-spec.md` templates
- Task execution: Hook into `execute-tasks.md`

## References
@../../../CLAUDE.md - Project-level instructions
@../standards/best-practices.md - Framework standards
```

##### Product Template (`product.md`)
```markdown
# Product Documentation Management

## Overview
Product planning documents that define your project's vision and architecture.

## Document Standards
- **mission.md**: Product vision and goals
- **tech-stack.md**: Technology choices and rationale
- **roadmap.md**: 5-phase development plan
- **design.md**: Architectural blueprints

## Evolution Guidelines
1. Start with mission.md during /plan-product
2. Expand design.md with each /create-spec
3. Update roadmap.md after major milestones
4. Keep tech-stack.md current with dependencies

## Cross-References
@../instructions/core/plan-product.md - Planning workflow
@../specs/ - Feature specifications
```

##### Standards Template (`standards.md`)
```markdown
# Standards Customization Guide

## Overview
Framework standards that ensure consistency across your project. Customize carefully.

## Override Hierarchy
1. Project CLAUDE.md (highest priority)
2. Local standards in .agent-os/standards/
3. Base installation standards ~/.agent-os/
4. Framework defaults (lowest priority)

## Safe Customization
- ✅ Add project-specific code style rules
- ✅ Extend PocketFlow patterns for your domain
- ✅ Define team conventions
- ❌ Don't break PocketFlow architectural patterns
- ❌ Don't remove design-first requirements

## PocketFlow Integration
@pocket-flow.md - Core patterns and rules
@code-style/*.md - Language-specific standards
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
    log_info "Installing subfolder CLAUDE.md templates..."

    # Get framework path for templates
    local script_realpath
    script_realpath="$(realpath "$0" 2>/dev/null)" || script_realpath="$0"
    local framework_templates_dir="$(dirname "$(dirname "$script_realpath")")/templates/claude-md"

    # Install templates if framework directory exists
    if [[ -d "$framework_templates_dir" ]]; then
        # Framework-tools CLAUDE.md
        if [[ -f "$framework_templates_dir/framework-tools.md" ]]; then
            mkdir -p ".agent-os/framework-tools"
            if safe_copy "$framework_templates_dir/framework-tools.md" ".agent-os/framework-tools/CLAUDE.md" "framework-tools CLAUDE.md"; then
                log_success "Installed framework-tools CLAUDE.md"
            else
                log_error "Failed to install framework-tools CLAUDE.md"
            fi
        fi

        # Instructions/core CLAUDE.md
        if [[ -f "$framework_templates_dir/instructions-core.md" ]]; then
            mkdir -p ".agent-os/instructions/core"
            if safe_copy "$framework_templates_dir/instructions-core.md" ".agent-os/instructions/core/CLAUDE.md" "instructions/core CLAUDE.md"; then
                log_success "Installed instructions/core CLAUDE.md"
            else
                log_error "Failed to install instructions/core CLAUDE.md"
            fi
        fi

        # Product CLAUDE.md
        if [[ -f "$framework_templates_dir/product.md" ]]; then
            mkdir -p ".agent-os/product"
            if safe_copy "$framework_templates_dir/product.md" ".agent-os/product/CLAUDE.md" "product CLAUDE.md"; then
                log_success "Installed product CLAUDE.md"
            else
                log_error "Failed to install product CLAUDE.md"
            fi
        fi

        # Standards CLAUDE.md
        if [[ -f "$framework_templates_dir/standards.md" ]]; then
            mkdir -p ".agent-os/standards"
            if safe_copy "$framework_templates_dir/standards.md" ".agent-os/standards/CLAUDE.md" "standards CLAUDE.md"; then
                log_success "Installed standards CLAUDE.md"
            else
                log_error "Failed to install standards CLAUDE.md"
            fi
        fi
    else
        log_warning "Framework CLAUDE.md templates not found - subfolder guidance will be limited"
    fi
}
```

**Integration Point**: Add call to `install_subfolder_claude_md()` in main installation flow after the `install_standards()` function call.

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
- [x] Design framework-specific template structure
- [x] Define detailed template content specifications
- [x] Plan installation integration strategy
- [ ] Create template directory structure
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