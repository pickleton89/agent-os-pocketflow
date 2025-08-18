# System Architecture Overview

> **Framework Type:** Meta-Framework that generates PocketFlow applications  
> **Status:** Production Ready  
> **Installation Location:** `~/.agent-os/`  
> **Generated Projects:** Use PocketFlow as dependency

## Executive Summary

The Agent OS + PocketFlow integration is a **meta-framework** that generates educational PocketFlow templates with intentional placeholder TODOs. This is NOT a PocketFlow application itself, but rather the system that creates learning-oriented template projects for end-users to implement.

**Key Principle**: Missing implementations in generated templates are features, not bugs. This framework creates starting points that teach proper implementation patterns.

## High-Level System Architecture

```mermaid
graph TB
    subgraph "Meta-Framework Repository (THIS IS THE FRAMEWORK)"
        A[Agent OS Core] --> B[Integration Layer]
        B --> C[PocketFlow Generator]
        C --> D[Template System]
        D --> E[Validation Framework]
        
        subgraph "Sub-Agents Enhancement System"
            SA1[Pattern Recognizer Agent]
            SA2[Template Validator Agent] 
            SA3[Dependency Orchestrator Agent]
        end
        
        C --> SA1
        SA1 --> C
        C --> SA2
        SA2 --> C
        C --> SA3
        SA3 --> C
    end
    
    subgraph "Generated User Projects (FRAMEWORK OUTPUT)"
        F[Generated PocketFlow App]
        G[FastAPI Integration]
        H[Complete Test Suite]
        I[Design Documents]
        J[Educational TODO Placeholders]
    end
    
    subgraph "System Installation"
        K["~/.agent-os/"]
        L[Global Templates]
        M[Workflow Scripts]
        N[Agent Configurations]
    end
    
    C --> F
    C --> G
    C --> H
    C --> I
    SA2 --> J
    D --> K
    D --> L
    D --> M
    SA1 --> N
    SA2 --> N
    SA3 --> N
    
    style A fill:#e1f5fe
    style C fill:#f3e5f5
    style F fill:#e8f5e8
    style SA1 fill:#e3f2fd
    style SA2 fill:#e8f5e8
    style SA3 fill:#fff3e0
```

## Component Architecture

### 1. Agent OS Core (`.agent-os/instructions/`)
- **Location:** [`.agent-os/instructions/core/`](./.agent-os/instructions/core/)
- **Purpose:** Workflow management and structured development
- **Key Files:**
  - `analyze-product.md` - Product analysis workflows
  - `create-spec.md` - Specification creation with design-first enforcement
  - `execute-tasks.md` - Quality-gated implementation

### 2. PocketFlow Generator ([`.agent-os/workflows/generator.py`](./.agent-os/workflows/generator.py))
- **Purpose:** Generates complete PocketFlow applications from YAML specs
- **Capabilities:**
  - Creates 12+ files per workflow pattern
  - Supports all PocketFlow patterns (Agent, Workflow, RAG, MapReduce, etc.)
  - Template substitution and validation
- **Output:** Complete Python projects with PocketFlow dependency

### 3. Template System ([`templates/`](./templates/))
- **Global Templates:** Framework-level templates for all projects
- **Generated Templates:** Created per-project by the generator
- **Standards Enforcement:** Code style and best practices

### 4. Validation Framework ([`scripts/validation/`](./scripts/validation/))
- **75+ Tests:** Comprehensive validation across 5 test suites
- **Integration Testing:** Framework installation and generation
- **Quality Assurance:** Generated code validation

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent OS
    participant PR as Pattern Recognizer
    participant G as Generator
    participant T as Templates
    participant TV as Template Validator
    participant DO as Dependency Orchestrator
    participant P as Generated Project
    
    U->>A: /create-spec workflow.yaml
    A->>PR: Analyze requirements
    PR->>PR: Identify optimal patterns
    PR-->>A: Pattern recommendations
    A->>G: Generate PocketFlow app
    G->>T: Load templates
    T-->>G: Template content
    G->>G: Process YAML spec
    G->>DO: Request dependency config
    DO->>DO: Generate dependencies
    DO-->>G: pyproject.toml + configs
    G->>P: Create 12+ files with placeholders
    P-->>G: Generated structure
    G->>TV: Validate generated templates
    TV->>TV: Check structure + educational value
    TV-->>G: Validation results
    G-->>A: Generation complete
    A-->>U: Educational template ready for implementation
```

## Integration Points

### Framework Development vs Usage

**Framework Development (This Repository):**
```mermaid
graph LR
    A[Improve Generator] --> B[Enhance Templates]
    B --> C[Add Validation]
    C --> D[Update Standards]
    D --> A
    
    style A fill:#ffe0e0
    style B fill:#ffe0e0
    style C fill:#ffe0e0
    style D fill:#ffe0e0
```

**Framework Usage (Generated Projects):**
```mermaid
graph LR
    E[Install PocketFlow] --> F[Implement Nodes]
    F --> G[Build Flows]
    G --> H[Create APIs]
    H --> I[Deploy App]
    
    style E fill:#e0ffe0
    style F fill:#e0ffe0
    style G fill:#e0ffe0
    style H fill:#e0ffe0
    style I fill:#e0ffe0
```

## System Boundaries

### What This Framework Does
- ✅ Installs to `~/.agent-os/` globally
- ✅ Generates PocketFlow applications for users
- ✅ Provides templates and validation
- ✅ Manages workflow standards

### What Generated Projects Do
- ✅ Install PocketFlow as dependency
- ✅ Implement actual business logic
- ✅ Run in production environments
- ✅ Use orchestrator agent for planning

## Installation Architecture

```mermaid
graph TD
    A[Clone Meta-Framework] --> B[Run ./setup.sh]
    B --> C[Install to ~/.agent-os/]
    C --> D[Setup Claude Code Integration]
    D --> E[Validate Installation]
    E --> F[Ready for Project Generation]
    
    F --> G[Create User Project]
    G --> H[Generate PocketFlow App]
    H --> I[Implement Business Logic]
    I --> J[Deploy Application]
```

## Key Architectural Decisions

### 1. Meta-Framework Design
- **Decision:** Build system that generates frameworks rather than being one
- **Rationale:** Allows users to create multiple PocketFlow projects
- **Impact:** Clear separation between framework development and usage

### 2. Global Installation Pattern
- **Decision:** Install to `~/.agent-os/` rather than per-project
- **Rationale:** Reusable across multiple projects, consistent tooling
- **Impact:** Single installation serves all user projects

### 3. Template-Based Generation
- **Decision:** Use templates with variable substitution
- **Rationale:** Maintainable, consistent output, easy customization
- **Impact:** High code quality in generated projects

### 4. Design-First Enforcement
- **Decision:** Require design documents before implementation
- **Rationale:** Prevents implementation without planning
- **Impact:** Higher quality, more maintainable applications

## Security Considerations

- **Template Safety:** All templates are static and validated
- **Generated Code:** No dynamic code execution in generation
- **Installation:** Installs to user home directory only
- **Dependencies:** Clear separation between framework and generated project deps

## Performance Characteristics

- **Generation Speed:** ~2-3 seconds for complete PocketFlow application
- **Memory Usage:** Low, primarily file I/O operations
- **Disk Usage:** ~50MB for framework, ~5MB per generated project
- **Scalability:** Linear with number of projects generated

## Error Handling Architecture

```mermaid
graph TD
    A[User Input] --> B{Validation}
    B -->|Valid| C[Generate Project]
    B -->|Invalid| D[Return Error]
    C --> E{Template Processing}
    E -->|Success| F[Validate Generated Code]
    E -->|Failure| G[Template Error]
    F -->|Pass| H[Project Ready]
    F -->|Fail| I[Generation Error]
```

## Future Architecture Considerations

- **Plugin System:** Extensible template system for custom patterns
- **Remote Templates:** Template repository for community patterns
- **CI/CD Integration:** Automated validation in development workflows
- **Metrics Collection:** Usage analytics for improvement insights

---

**Next:** See [Component Details](./components.md) for detailed component architecture.