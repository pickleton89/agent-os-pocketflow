# Generator Workflow Diagrams

> **Visual documentation of the PocketFlow workflow generation process**

## Overview

The generator workflow transforms YAML specifications into complete PocketFlow applications through a multi-stage pipeline. This document provides detailed visual documentation of each stage.

## Complete Generation Workflow

```mermaid
flowchart TD
    A[YAML Specification] --> B[Input Validation]
    B --> C[Template Loading]
    C --> D[Spec Processing]
    D --> E[Core File Generation]
    E --> F[API Integration]
    F --> G[Test Suite Generation]
    G --> H[Documentation Creation]
    H --> I[Validation Pipeline]
    I --> J[Project Assembly]
    J --> K[Quality Assurance]
    K --> L[Generated PocketFlow App]
    
    subgraph "Parallel Processing"
        M[Node Generation]
        N[Flow Assembly]
        O[Schema Creation]
        P[Utility Generation]
    end
    
    E --> M
    E --> N
    E --> O
    E --> P
    
    style A fill:#e1f5fe
    style L fill:#e8f5e8
    style K fill:#fff3e0
```

## 1. Input Processing Stage

### YAML Specification Parsing
**Location:** [`.agent-os/workflows/generator.py:1115`](./.agent-os/workflows/generator.py:1115)

```mermaid
sequenceDiagram
    participant U as User
    participant F as File System
    participant Y as YAML Parser
    participant V as Validator
    participant S as WorkflowSpec
    
    U->>F: Provide YAML file
    F->>Y: Read specification
    Y->>Y: Parse YAML structure
    Y->>V: Validate schema
    V->>S: Create WorkflowSpec object
    S-->>Y: Structured specification
    Y-->>F: Validated spec
    F-->>U: Ready for generation
```

### Specification Validation Flow
```mermaid
flowchart TD
    A[Raw YAML] --> B{Valid YAML?}
    B -->|No| C[YAML Error]
    B -->|Yes| D[Schema Validation]
    D --> E{Required Fields?}
    E -->|No| F[Schema Error]
    E -->|Yes| G[Pattern Validation]
    G --> H{Valid Pattern?}
    H -->|No| I[Pattern Error]
    H -->|Yes| J[WorkflowSpec Object]
    
    C --> K[Error Report]
    F --> K
    I --> K
    K --> L[User Feedback]
    
    J --> M[Generation Ready]
```

## 2. Template Processing Stage

### Template Loading Architecture
**Location:** [`.agent-os/workflows/generator.py:61`](./.agent-os/workflows/generator.py:61)

```mermaid
flowchart LR
    A[Templates Directory] --> B[Template Scanner]
    B --> C[File Filter]
    C --> D[Content Loader]
    D --> E[Template Cache]
    
    subgraph "Template Types"
        F[*.md files]
        G[Global Templates]
        H[Pattern-Specific]
    end
    
    C --> F
    F --> G
    F --> H
    
    E --> I[Ready for Processing]
    
    style E fill:#f3e5f5
```

### Template Variable Extraction
```mermaid
sequenceDiagram
    participant S as WorkflowSpec
    participant E as Extractor
    participant V as Variables
    participant T as Templates
    participant P as Processor
    
    S->>E: Input specification
    E->>V: Extract node variables
    E->>V: Extract utility variables
    E->>V: Extract API variables
    V->>T: Load matching templates
    T->>P: Template + Variables
    P->>P: Variable substitution
    P-->>E: Processed content
    E-->>S: Ready for generation
```

## 3. Code Generation Stages

### Core File Generation Pipeline
**Location:** [`.agent-os/workflows/generator.py:68`](./.agent-os/workflows/generator.py:68)

```mermaid
flowchart TD
    A[WorkflowSpec] --> B[File Type Router]
    
    B --> C[Design Document]
    B --> D[Pydantic Models]
    B --> E[Utility Functions]
    B --> F[PocketFlow Nodes]
    B --> G[Flow Assembly]
    B --> H[Package Structure]
    
    C --> I[design.md Generator]
    D --> J[schemas/models.py Generator]
    E --> K[utils/*.py Generator]
    F --> L[nodes.py Generator]
    G --> M[flow.py Generator]
    H --> N[__init__.py Generator]
    
    I --> O[Generated Files Dictionary]
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
    
    style O fill:#e8f5e8
```

### Node Generation Workflow
**Location:** [`.agent-os/workflows/generator.py:509`](./.agent-os/workflows/generator.py:509)

```mermaid
flowchart TD
    A[Node Specifications] --> B[Node Type Analysis]
    B --> C[Smart Defaults Generator]
    C --> D[Method Generation]
    
    subgraph "Method Generation"
        E[prep() Method]
        F[exec() Method]
        G[post() Method]
    end
    
    D --> E
    D --> F
    D --> G
    
    E --> H[Type Hints Addition]
    F --> H
    G --> H
    
    H --> I[Documentation Generation]
    I --> J[Logging Integration]
    J --> K[Complete Node Class]
    
    subgraph "Smart Defaults Logic"
        L[Name Pattern Matching]
        M[Description Analysis]
        N[Type Inference]
    end
    
    C --> L
    C --> M
    C --> N
```

### Flow Assembly Generation
**Location:** [`.agent-os/workflows/generator.py:573`](./.agent-os/workflows/generator.py:573)

```mermaid
flowchart TD
    A[Node List] --> B[Flow Class Generator]
    B --> C[Node Dictionary Creation]
    C --> D[Edge Generation]
    
    subgraph "Edge Logic"
        E[Sequential Connections]
        F[Error Handling Routes]
        G[Success Path Mapping]
    end
    
    D --> E
    D --> F
    D --> G
    
    E --> H[Flow Constructor]
    F --> H
    G --> H
    
    H --> I[Import Generation]
    I --> J[Class Documentation]
    J --> K[Complete Flow Class]
    
    style K fill:#e1f5fe
```

## 4. FastAPI Integration Workflow

### API Generation Pipeline
**Conditional Generation:** Only when `fast_api_integration: true`

```mermaid
flowchart TD
    A[FastAPI Flag Check] --> B{API Enabled?}
    B -->|No| C[Skip API Generation]
    B -->|Yes| D[API Component Generation]
    
    D --> E[main.py Generation]
    D --> F[router.py Generation]
    D --> G[API Models Generation]
    
    E --> H[FastAPI App Setup]
    H --> I[Middleware Configuration]
    I --> J[Router Integration]
    
    F --> K[Endpoint Generation]
    K --> L[Request/Response Models]
    L --> M[Error Handling]
    
    G --> N[Request Models]
    G --> O[Response Models]
    
    J --> P[Complete FastAPI Integration]
    M --> P
    N --> P
    O --> P
```

### Endpoint Generation Flow
**Location:** [`.agent-os/workflows/generator.py:667`](./.agent-os/workflows/generator.py:667)

```mermaid
sequenceDiagram
    participant A as API Endpoints
    participant G as Generator
    participant T as Template Engine
    participant V as Validator
    participant F as File Generator
    
    A->>G: Endpoint specifications
    G->>T: Load API templates
    T-->>G: Template content
    G->>G: Generate route handlers
    G->>V: Validate endpoint logic
    V-->>G: Validation results
    G->>F: Generate router.py
    F-->>G: Generated API code
    G-->>A: Complete API integration
```

## 5. Test Generation Workflow

### Test Suite Architecture
**Location:** [`.agent-os/workflows/generator.py:721`](./.agent-os/workflows/generator.py:721)

```mermaid
flowchart TD
    A[Test Requirements] --> B[Test Type Router]
    
    B --> C[Node Tests]
    B --> D[Flow Tests]
    B --> E[API Tests]
    
    C --> F[test_nodes.py Generator]
    D --> G[test_flow.py Generator]
    E --> H[test_api.py Generator]
    
    F --> I[Fixture Generation]
    F --> J[Unit Test Methods]
    
    G --> K[Integration Test Setup]
    G --> L[Flow Execution Tests]
    
    H --> M[API Client Setup]
    H --> N[Endpoint Test Methods]
    
    I --> O[Complete Test Suite]
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
```

### Test Method Generation Flow
```mermaid
sequenceDiagram
    participant N as Node Spec
    participant T as Test Generator
    participant F as Fixture Builder
    participant M as Method Generator
    participant A as Assertion Builder
    
    N->>T: Node specification
    T->>F: Create test fixtures
    F-->>T: Test setup code
    T->>M: Generate test methods
    M->>A: Add assertions
    A-->>M: Test validation
    M-->>T: Complete test method
    T-->>N: Generated test class
```

## 6. Documentation Generation Workflow

### Design Document Creation
**Location:** [`.agent-os/workflows/generator.py:210`](./.agent-os/workflows/generator.py:210)

```mermaid
flowchart TD
    A[Specification Input] --> B[Design Doc Generator]
    B --> C[Requirements Section]
    B --> D[Architecture Diagram]
    B --> E[Node Sequence]
    B --> F[Utilities Documentation]
    B --> G[Data Design]
    
    C --> H[Problem Statement]
    C --> I[Success Criteria]
    
    D --> J[Mermaid Diagram Generation]
    J --> K[Node Flow Visualization]
    
    E --> L[Step-by-Step Flow]
    
    F --> M[Utility Function Specs]
    
    G --> N[SharedStore Schema]
    
    H --> O[Complete Design Document]
    I --> O
    K --> O
    L --> O
    M --> O
    N --> O
```

### Task List Generation
**Location:** [`.agent-os/workflows/generator.py:849`](./.agent-os/workflows/generator.py:849)

```mermaid
flowchart TD
    A[Generated Files] --> B[Task Generator]
    B --> C[Phase 0: Design]
    B --> D[Phase 1: Schemas]
    B --> E[Phase 2: Utilities]
    B --> F[Phase 3: FastAPI]
    B --> G[Phase 4: Nodes]
    B --> H[Phase 5: Flow]
    B --> I[Phase 6: Integration]
    B --> J[Phase 7: Optimization]
    
    C --> K[Design Validation Tasks]
    D --> L[Pydantic Model Tasks]
    E --> M[Utility Implementation Tasks]
    F --> N[API Development Tasks]
    G --> O[Node Implementation Tasks]
    H --> P[Flow Assembly Tasks]
    I --> Q[Testing Tasks]
    J --> R[Optimization Tasks]
    
    K --> S[Complete Task Checklist]
    L --> S
    M --> S
    N --> S
    O --> S
    P --> S
    Q --> S
    R --> S
```

## 7. Validation and Quality Assurance

### Generated Code Validation Pipeline
```mermaid
flowchart TD
    A[Generated Files] --> B[Syntax Validation]
    B --> C[Import Verification]
    C --> D[Type Checking]
    D --> E[Code Style Validation]
    E --> F[Test Validation]
    F --> G[Documentation Check]
    G --> H[Quality Gates]
    
    H --> I{All Checks Pass?}
    I -->|Yes| J[Project Ready]
    I -->|No| K[Error Collection]
    
    K --> L[Detailed Error Report]
    L --> M[Resolution Guidance]
    M --> N[Regeneration Required]
    
    J --> O[Success Report]
    O --> P[Generated Project]
```

### Quality Gate Workflow
```mermaid
sequenceDiagram
    participant G as Generated Code
    participant V as Validator
    participant S as Syntax Checker
    participant T as Type Checker
    participant Q as Quality Assessor
    participant R as Reporter
    
    G->>V: Submit for validation
    V->>S: Check syntax
    S-->>V: Syntax results
    V->>T: Verify types
    T-->>V: Type results
    V->>Q: Apply quality gates
    Q-->>V: Quality metrics
    V->>R: Generate report
    R-->>V: Validation report
    V-->>G: Final status
```

## 8. Project Assembly and Output

### File System Assembly
```mermaid
flowchart TD
    A[Generated Content] --> B[Directory Structure]
    B --> C[File Placement]
    C --> D[Package Initialization]
    D --> E[Permission Setting]
    E --> F[Metadata Addition]
    F --> G[Final Validation]
    G --> H[Project Complete]
    
    subgraph "Directory Creation"
        I[Root Package]
        J[Source Directories]
        K[Test Directories]
        L[Documentation]
    end
    
    B --> I
    B --> J
    B --> K
    B --> L
    
    subgraph "File Organization"
        M[Core Files]
        N[Test Files]
        O[Documentation Files]
        P[Configuration Files]
    end
    
    C --> M
    C --> N
    C --> O
    C --> P
```

### Project Output Structure
**Location:** [`.agent-os/workflows/generator.py:1062`](./.agent-os/workflows/generator.py:1062)

```mermaid
graph TB
    A[Generated Project] --> B[Package Root]
    B --> C[Source Code]
    B --> D[Tests]
    B --> E[Documentation]
    B --> F[Configuration]
    
    C --> G["__init__.py<br/>Package exports"]
    C --> H["nodes.py<br/>PocketFlow nodes"]
    C --> I["flow.py<br/>Flow assembly"]
    C --> J["main.py<br/>FastAPI app"]
    C --> K["router.py<br/>API routes"]
    C --> L["schemas/<br/>Pydantic models"]
    C --> M["utils/<br/>Custom utilities"]
    
    D --> N["tests/__init__.py<br/>Test package"]
    D --> O["test_nodes.py<br/>Node tests"]
    D --> P["test_flow.py<br/>Flow tests"]
    D --> Q["test_api.py<br/>API tests"]
    
    E --> R["docs/design.md<br/>Design document"]
    E --> S["tasks.md<br/>Implementation tasks"]
    
    F --> T["check-install.py<br/>Dependency checker"]
    
    style A fill:#e8f5e8
    style C fill:#e1f5fe
    style D fill:#fff3e0
    style E fill:#f3e5f5
```

## Performance Optimization Workflow

### Generation Performance Pipeline
```mermaid
gantt
    title Workflow Generation Performance
    dateFormat X
    axisFormat %s
    
    section Initialization
    Template Loading    :0, 100
    Spec Validation     :100, 150
    
    section Core Generation
    Node Generation     :150, 400
    Flow Assembly       :400, 500
    Schema Creation     :150, 300
    
    section Integration
    API Generation      :500, 650
    Test Generation     :650, 900
    
    section Documentation
    Design Document     :900, 1100
    Task Generation     :1100, 1200
    
    section Finalization
    File Assembly       :1200, 1400
    Validation          :1400, 1600
    Quality Check       :1600, 1800
```

---

**Next:** See [Cross-References and Code Pointers](./code-pointers.md) for comprehensive code navigation.