# Component Architecture

> **Detailed breakdown of framework components and their interactions**

## Core Component Map

```mermaid
graph TB
    subgraph "Core Agent OS Components"
        A[Instructions Core] --> B[Workflow Management]
        B --> C[Quality Gates]
    end
    
    subgraph "PocketFlow Integration"
        D[Generator Engine] --> E[Template Processor]
        E --> F[Code Generator]
        F --> G[Validation Engine]
    end
    
    subgraph "Sub-Agents System (NEW)"
        SA1[Pattern Recognizer Agent]
        SA2[Template Validator Agent]
        SA3[Dependency Orchestrator Agent]
        
        SA1 --> SA4[Agent Coordination]
        SA2 --> SA4
        SA3 --> SA4
        SA4 --> SA5[Performance Caching]
    end
    
    subgraph "Claude Code Integration"
        H[Orchestrator Agent] --> I[Planning System]
        I --> J[Cross-file Coordination]
    end
    
    subgraph "Validation Framework"
        K[Unit Tests] --> L[Integration Tests]
        L --> M[End-to-End Tests]
        M --> N[Quality Assurance]
    end
    
    A --> D
    C --> G
    H --> B
    N --> C
    
    D --> SA1
    SA1 --> D
    F --> SA2
    SA2 --> F
    F --> SA3
    SA3 --> F
    
    style SA1 fill:#e3f2fd
    style SA2 fill:#e8f5e8
    style SA3 fill:#fff3e0
    style SA4 fill:#f3e5f5
    style SA5 fill:#fce4ec
```

## 1. Generator Engine

**Location:** [`.agent-os/workflows/generator.py`](./.agent-os/workflows/generator.py:1)

### Architecture
```mermaid
classDiagram
    class PocketFlowGenerator {
        +templates_path: Path
        +output_path: Path
        +templates: Dict[str, str]
        +generate_workflow(spec) Dict[str, str]
        +save_workflow(spec, files) None
    }
    
    class WorkflowSpec {
        +name: str
        +pattern: str
        +description: str
        +nodes: List[Dict]
        +utilities: List[Dict]
        +api_endpoints: List[Dict]
    }
    
    PocketFlowGenerator --> WorkflowSpec : uses
```

### Key Capabilities
- **Template Loading:** Loads all `.md` templates from templates directory
- **YAML Processing:** Converts workflow specifications to complete projects
- **File Generation:** Creates 12+ files per PocketFlow pattern
- **Smart Defaults:** Generates intelligent code based on node names/descriptions

### Code Pointers
- **Main Generator Class:** [`.agent-os/workflows/generator.py:36`](./.agent-os/workflows/generator.py:36)
- **Workflow Generation:** [`.agent-os/workflows/generator.py:68`](./.agent-os/workflows/generator.py:68)
- **Template Processing:** [`.agent-os/workflows/generator.py:61`](./.agent-os/workflows/generator.py:61)
- **Sub-Agent Coordination:** [`.agent-os/workflows/generator.py:coordinate_template_validation`](./.agent-os/workflows/generator.py)

## 1a. Sub-Agents System (NEW)

**Location:** [`.claude/agents/`](../../.claude/agents/) and [`.agent-os/workflows/`](../../.agent-os/workflows/)

### Sub-Agents Architecture
```mermaid
graph TB
    subgraph "Pattern Recognition"
        PR1[Requirements Analysis] --> PR2[Pattern Indicators]
        PR2 --> PR3[Confidence Scoring]
        PR3 --> PR4[Template Selection]
    end
    
    subgraph "Template Validation"
        TV1[Syntax Validation] --> TV2[Pattern Compliance]
        TV2 --> TV3[Educational Quality]
        TV3 --> TV4[Framework Philosophy]
    end
    
    subgraph "Dependency Orchestration"
        DO1[Pattern Dependencies] --> DO2[Tool Configuration]
        DO2 --> DO3[Environment Setup]
        DO3 --> DO4[Compatibility Check]
    end
    
    subgraph "Coordination & Caching"
        CC1[Agent Coordination] --> CC2[Performance Cache]
        CC2 --> CC3[LRU Management]
    end
    
    PR4 --> CC1
    TV4 --> CC1
    DO4 --> CC1
```

### Key Capabilities
- **Pattern Recognizer**: Analyzes requirements and identifies optimal PocketFlow patterns
- **Template Validator**: Ensures generated templates maintain educational quality and structural correctness
- **Dependency Orchestrator**: Manages Python tooling and creates proper dependency configurations
- **Intelligent Caching**: 100x+ performance improvements through pattern and dependency caching

### Code Pointers
- **Pattern Analyzer:** [`.agent-os/workflows/pattern_analyzer.py`](../../.agent-os/workflows/pattern_analyzer.py)
- **Template Validator:** [`.agent-os/workflows/template_validator.py`](../../.agent-os/workflows/template_validator.py)
- **Dependency Orchestrator:** [`.agent-os/workflows/dependency_orchestrator.py`](../../.agent-os/workflows/dependency_orchestrator.py)
- **Agent Coordination:** [`.agent-os/workflows/agent_coordination.py`](../../.agent-os/workflows/agent_coordination.py)
- **Agent Configs:** [`.claude/agents/`](../../.claude/agents/)

## 2. Template System

**Locations:** [`templates/`](../../templates/) and [`.agent-os/workflows/`](../../.agent-os/workflows/)

### Template Architecture
```mermaid
graph LR
    A[Global Templates] --> B[Template Processor]
    C[YAML Specs] --> B
    B --> D[Variable Substitution]
    D --> E[Generated Files]
    
    subgraph "Template Types"
        F[PocketFlow Templates]
        G[FastAPI Templates]
        H[Task Templates]
    end
    
    B --> F
    B --> G
    B --> H
```

### Generated File Structure
Each workflow generates this complete structure:

```
generated-workflow/
├── __init__.py              # Package initialization with exports
├── main.py                  # FastAPI application entry point
├── nodes.py                 # PocketFlow nodes with type hints
├── flow.py                  # PocketFlow flow assembly
├── router.py                # FastAPI routing integration
├── schemas/
│   ├── __init__.py          # Schema package exports
│   └── models.py            # Pydantic models with validation
├── utils/                   # Custom utility functions
│   ├── __init__.py          # Auto-import utility functions
│   └── [custom_utils].py    # Generated utility functions
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── test_nodes.py        # Node unit tests with fixtures
│   ├── test_flow.py         # Flow integration tests
│   └── test_api.py          # FastAPI endpoint tests
├── docs/
│   ├── __init__.py          # Documentation package
│   └── design.md            # Mandatory design document
├── check-install.py         # Installation validator script
└── tasks.md                 # Implementation task checklist
```

### Template Processing Flow
```mermaid
sequenceDiagram
    participant S as YAML Spec
    participant G as Generator
    participant T as Templates
    participant V as Variables
    participant F as Generated Files
    
    S->>G: Load workflow specification
    G->>T: Load template files
    T-->>G: Template content
    G->>V: Extract variables from spec
    V-->>G: Variable mappings
    G->>G: Process each template
    G->>F: Write generated files
```

## 3. Validation Framework

**Location:** [`scripts/validation/`](./scripts/validation/)

### Validation Architecture
```mermaid
graph TD
    A[Master Test Runner] --> B[Integration Tests]
    A --> C[Orchestration Tests]
    A --> D[Design Tests]
    A --> E[PocketFlow Tests]
    A --> F[End-to-End Tests]
    
    B --> G[Framework Installation]
    C --> H[Agent Coordination]
    D --> I[Design Document Validation]
    E --> J[Generator System]
    F --> K[Complete Workflow]
```

### Test Suites

#### 1. Integration Tests ([`scripts/validation/validate-integration.sh`](./scripts/validation/validate-integration.sh))
- Framework installation validation
- Directory structure verification
- Template system functionality
- Basic generation capabilities

#### 2. Orchestration Tests ([`scripts/validation/validate-orchestration.sh`](./scripts/validation/validate-orchestration.sh))
- Agent coordination validation
- Cross-file dependency checking
- Workflow state management
- Error handling verification

#### 3. Design Tests ([`scripts/validation/validate-design.sh`](./scripts/validation/validate-design.sh))
- Design document generation
- Mermaid diagram validation
- Requirements completeness
- Template structure verification

#### 4. PocketFlow Tests ([`scripts/validation/validate-pocketflow.sh`](./scripts/validation/validate-pocketflow.sh))
- Generator engine functionality
- All workflow patterns support
- Template substitution accuracy
- Generated code quality

#### 5. End-to-End Tests ([`scripts/validation/validate-end-to-end.sh`](./scripts/validation/validate-end-to-end.sh))
- Complete workflow generation
- Generated project validation
- Integration with external tools
- Production readiness verification

## 4. Claude Code Integration

**Location:** [`.claude/agents/pocketflow-orchestrator.md`](./.claude/agents/pocketflow-orchestrator.md)

### Orchestrator Architecture
```mermaid
graph TB
    A[User Request] --> B{Complex Task?}
    B -->|Yes| C[Invoke Orchestrator]
    B -->|No| D[Standard Processing]
    
    C --> E[Strategic Planning]
    E --> F[Task Decomposition]
    F --> G[Dependency Analysis]
    G --> H[Execution Planning]
    H --> I[Quality Validation]
    
    subgraph "Orchestrator Capabilities"
        J[Graph-based Workflow Design]
        K[LLM Feature Planning]
        L[Complex Task Coordination]
        M[Cross-file Management]
    end
    
    E --> J
    F --> K
    G --> L
    H --> M
```

### Automatic Invocation Triggers
- Keywords: "think", "plan", "design", "architect", "implement"
- LLM/AI feature development requests
- Complex multi-step tasks
- Workflow specification creation

## 5. Standards System

**Location:** [`standards/`](./standards/)

### Standards Architecture
```mermaid
graph LR
    A[Code Style Standards] --> B[Template Enforcement]
    C[PocketFlow Guidelines] --> B
    D[Tech Stack Standards] --> B
    E[Best Practices] --> B
    
    B --> F[Generated Code Quality]
    F --> G[Consistent Output]
    G --> H[Maintainable Projects]
```

### Standard Components
- **PocketFlow Guidelines:** [`standards/pocket-flow.md`](./standards/pocket-flow.md)
- **Code Style:** [`standards/code-style.md`](./standards/code-style.md)
- **Tech Stack:** [`standards/tech-stack.md`](./standards/tech-stack.md)
- **Best Practices:** [`standards/best-practices.md`](./standards/best-practices.md)

## Component Interactions

### Generator → Template System
```mermaid
sequenceDiagram
    participant G as Generator
    participant T as Template System
    participant F as File System
    
    G->>T: Load templates
    T->>F: Read template files
    F-->>T: Template content
    T-->>G: Processed templates
    G->>G: Apply variable substitution
    G->>F: Write generated files
```

### Validation → Generated Code
```mermaid
sequenceDiagram
    participant V as Validator
    participant G as Generated Code
    participant T as Test Framework
    participant Q as Quality Gates
    
    V->>G: Analyze generated files
    G-->>V: Code structure
    V->>T: Run test suites
    T-->>V: Test results
    V->>Q: Apply quality gates
    Q-->>V: Validation status
```

### Agent OS → PocketFlow Integration
```mermaid
sequenceDiagram
    participant A as Agent OS
    participant O as Orchestrator
    participant G as Generator
    participant P as PocketFlow App
    
    A->>O: Complex task detected
    O->>O: Strategic planning
    O->>G: Generate workflow
    G->>P: Create PocketFlow app
    P-->>G: Generated structure
    G-->>O: Generation complete
    O-->>A: Task ready for implementation
```

## Performance Characteristics

### Generator Performance
- **Template Loading:** ~100ms for all templates
- **YAML Processing:** ~50ms per specification
- **File Generation:** ~10ms per generated file
- **Total Generation Time:** ~2-3 seconds for complete project

### Memory Usage
- **Template Cache:** ~5MB for all templates
- **Processing:** ~10MB peak during generation
- **Generated Output:** ~1MB per project

### Scalability Limits
- **Templates:** Up to 100 templates efficiently
- **Generated Files:** Up to 50 files per project
- **Concurrent Generation:** 10+ projects simultaneously

## Error Handling Strategy

### Component-Level Error Handling
```mermaid
graph TD
    A[Component Error] --> B{Error Type}
    B -->|Template Error| C[Template Validation]
    B -->|Generation Error| D[Rollback Generation]
    B -->|Validation Error| E[Detailed Feedback]
    
    C --> F[User Feedback]
    D --> F
    E --> F
    F --> G[Resolution Guidance]
```

### Recovery Mechanisms
- **Template Errors:** Fallback to basic templates
- **Generation Failures:** Partial cleanup and retry
- **Validation Issues:** Detailed error reports with fixes
- **System Errors:** Comprehensive logging and diagnosis

---

**Next:** See [Data Flow Documentation](./data-flow.md) for detailed data flow analysis.