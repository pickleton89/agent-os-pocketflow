# Agent OS + PocketFlow - Complete Documentation

*Intelligent Orchestration for AI-Powered Development*

## Stop building AI features like it's 2024

Your coding agents are brilliant at following instructions—but they need orchestration. Introducing Agent OS + PocketFlow: an intelligent development system that transforms AI coding agents from confused assistants into architectural decision-makers.

## A system that makes AI coding agents think, design, and build like senior architects.

Agent OS + PocketFlow combines structured workflows with intelligent orchestration, giving your agents the ability to recognize patterns, make architectural decisions, and generate complete implementations. With automatic design generation, validated workflows, and production-ready patterns, your agents ship enterprise-grade AI features on the first try—not the fifth.

### Use it with:
- Claude Code, Cursor, or any other AI coding tool
- LLM/AI features and complex workflows
- Production applications requiring robust patterns
- Any Python-based stack with modern tooling

### Free & Open Source
- [Docs & Setup](#installation)
- [View on GitHub](https://github.com/buildermethods/agent-os-pocketflow)

---

## Why use Agent OS + PocketFlow?

Stop wrestling with AI agents that write basic code without understanding architecture. Agent OS + PocketFlow transforms coding agents into intelligent architects who understand patterns, make design decisions, and build production-ready systems.

3 reasons why teams building AI features need this system:

### 1. Intelligent orchestration, not just automation

Unlike basic Agent OS, this system provides active intelligence through:

- **Automatic Pattern Recognition** - Identifies when to use RAG, Agent, or Tool patterns
- **Proactive Orchestration** - Auto-invokes specialized agents for complex tasks
- **Design-First Enforcement** - Blocks implementation until architecture is solid
- **Validated Workflows** - Ensures every component meets specifications

**The result:** Your agent becomes an architect, not just a coder—making intelligent decisions and building robust systems.

### 2. Complete AI/LLM patterns, not reinvention

The system includes battle-tested patterns for AI development:

- **PocketFlow Patterns** - RAG, Agent, Tool, and Hybrid architectures
- **Node-Based Workflows** - Reusable components with prep/exec/post phases
- **Built-in Optimization** - Caching, batching, and error recovery
- **Type Safety Throughout** - Pydantic models for every data structure

**The difference:** Skip the learning curve and failed experiments—implement proven patterns immediately.

### 3. Orchestrated development, not chaos

Replace random AI implementations with orchestrated workflows:

- Automatic design document generation with diagrams
- Pattern-based code generation from templates
- Validation gates between phases
- Comprehensive test generation

**The relief:** Your AI features are architected, validated, and production-ready—not experimental hacks.

---

## The Four Layers of Intelligence

Agent OS + PocketFlow works through layered intelligence—each layer building on the previous to create a complete development orchestration system.

### Layer 1: Your standards (Foundation)

Your standards define how you build software—now enhanced with AI-specific patterns:

- **Tech Stack** — Python with UV, Ruff, Type checking (ty), FastAPI
- **Code Style** — PocketFlow patterns, Pydantic models, type hints
- **AI Best Practices** — LLM optimization, prompt engineering, error handling
- **Testing Philosophy** — Pytest with coverage, integration tests for workflows

Standards live in `~/.agent-os/standards/` with specialized style guides:
- `python-style.md` - Modern Python practices
- `fastapi-style.md` - API development patterns
- `pocketflow-style.md` - Workflow and node patterns
- `testing-style.md` - Comprehensive testing approach

### Layer 2: Your product (Context)

Product layer includes standard Agent OS documentation plus:

- **Architecture Decisions** — Pattern choices and rationale
- **Workflow Registry** — Catalog of implemented flows
- **Integration Points** — API contracts and service boundaries
- **Performance Baselines** — Metrics and optimization goals

Product documentation in `.agent-os/product/` provides complete context.

### Layer 3: Your orchestration (Intelligence)

The orchestration layer is **new and unique** to this system:

- **PocketFlow Orchestrator** — Intelligent agent that plans and designs
- **Coordination Hooks** — Cross-file validation and dependencies
- **Design Documents** — Comprehensive specs with Mermaid diagrams
- **Workflow Implementations** — Generated PocketFlow code

Orchestration components in:
- `.claude/agents/pocketflow-orchestrator.md` - Orchestrator agent
- `.agent-os/instructions/orchestration/` - Coordination system
- `.agent-os/workflows/` - Generated implementations

### Layer 4: Your specs (Execution)

Enhanced specifications with intelligent generation:

- **Auto-Generated Designs** — Complete architectural documentation
- **Pattern-Based Implementation** — Code generated from templates
- **Validated Task Breakdown** — Tasks with dependency management
- **Test Specifications** — Comprehensive test requirements

Specs in `.agent-os/specs/` include both documentation and generated code.

---

## Installation

Getting started with Agent OS + PocketFlow requires:

1. **Base Installation** - Install the enhanced Agent OS system
2. **PocketFlow Integration** - Add orchestration and templates
3. **Tool-Specific Setup** - Configure for Claude Code or Cursor

### 1. Base Installation

Run the enhanced installation script:

```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os-pocketflow/main/setup.sh | bash
```

#### What the enhanced install script does:
- Creates the standard `~/.agent-os/` structure
- Adds orchestration directories and hooks
- Installs PocketFlow templates and patterns
- Sets up Python-specific style guides
- Configures validation scripts
- Preserves existing customizations

#### Enhanced Directory Structure:
```
~/.agent-os/
├── standards/
│   ├── tech-stack.md         # Enhanced with Python/AI stack
│   ├── code-style.md         # PocketFlow patterns included
│   ├── best-practices.md     # AI/LLM best practices
│   └── code-style/           # Language-specific guides
│       ├── python-style.md
│       ├── fastapi-style.md
│       ├── pocketflow-style.md
│       └── testing-style.md
├── instructions/
│   ├── core/                 # Enhanced Agent OS instructions
│   │   ├── plan-product.md
│   │   ├── create-spec.md
│   │   ├── execute-tasks.md
│   │   └── analyze-product.md
│   ├── orchestration/        # NEW: Orchestration system
│   │   ├── coordination.yaml
│   │   ├── orchestrator-hooks.md
│   │   └── dependency-validation.md
│   └── meta/
│       └── pre-flight.md
└── templates/                 # NEW: Code generation templates
    ├── pocketflow-templates.md
    ├── fastapi-templates.md
    └── task-templates.md
```

### 2. Claude Code Setup (Enhanced)

```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os-pocketflow/main/setup-claude-code.sh | bash
```

**Enhanced Claude Code setup includes:**
- Standard Agent OS commands
- **NEW: PocketFlow Orchestrator agent** (auto-invokes on complex tasks)
- Enhanced subagents for workflow management
- Orchestration hooks and coordination

**Claude Code Structure:**
```
~/.claude/
├── commands/                 # Standard + enhanced commands
│   ├── plan-product.md
│   ├── create-spec.md
│   ├── execute-tasks.md
│   └── analyze-product.md
└── agents/                   # Enhanced agent suite
    ├── pocketflow-orchestrator.md  # NEW: Intelligent orchestrator
    ├── context-fetcher.md
    ├── file-creator.md
    ├── git-workflow.md
    └── test-runner.md
```

### 3. Project Setup

In your project directory:

```bash
# Initialize Agent OS + PocketFlow structure
mkdir -p .agent-os/{product,specs,workflows}
mkdir -p .claude
mkdir -p src/{flows,nodes,schemas,utils}
mkdir -p docs
mkdir -p tests/{unit,integration}

# Create CLAUDE.md for orchestration mode
cat > CLAUDE.md << 'EOF'
# Project Configuration
Uses PocketFlow Orchestrator for planning and implementation.

## 🎯 Orchestration Mode Active
This project uses the **PocketFlow Orchestrator** for all planning and implementation tasks.

### Automatic Orchestration
ALWAYS invoke the pocketflow-orchestrator agent when:
- User says: "think", "plan", "design", "architect", "implement"
- Creating any specification or workflow
- Executing complex tasks
- Solving problems requiring multiple steps

### Integration Pattern
1. First: Use pocketflow-orchestrator for planning
2. Then: Generate Agent OS files based on plan
3. Finally: Implement using generated PocketFlow workflows
EOF
```

### Important: Customize for AI Development

Edit your standards files for AI/LLM development:

**~/.agent-os/standards/tech-stack.md:**
```markdown
# Tech Stack

## Language & Runtime
- Python 3.11+
- UV for package management
- Ruff for linting/formatting
- Type checking with ty

## AI/LLM Stack
- LLM Providers: Claude (Anthropic), GPT-4 (OpenAI)
- Frameworks: PocketFlow for orchestration
- Vector DB: ChromaDB/Pinecone for RAG
- Caching: Redis for LLM response caching

## API Framework
- FastAPI with Pydantic v2
- Async/await throughout
- OpenAPI documentation
```

---

## Using Agent OS + PocketFlow

### The Orchestrated Workflow

The system automatically detects when orchestration is needed and activates the PocketFlow Orchestrator.

### Starting a New AI Feature

#### Automatic Orchestration:
```
@create-spec

I want to build a RAG system for searching documentation
```

**What happens automatically:**

1. **Orchestrator Activation** 🤖
   - System detects "RAG system" → AI/LLM feature
   - Automatically invokes `pocketflow-orchestrator`
   - Analyzes requirements for pattern selection

2. **Design Generation** 📐
   ```markdown
   # Documentation RAG System Design
   
   ## Pattern Analysis
   Pattern Identified: RAG Pattern
   Components: Embeddings, Vector Store, Retrieval, Generation
   
   ## Flow Architecture
   [Mermaid diagram automatically generated]
   
   ## Implementation Plan
   - Document ingestion pipeline
   - Embedding generation with caching
   - Vector store integration
   - Retrieval optimization
   - Response generation with context
   ```

3. **Workflow Generation** 🔧
   Complete PocketFlow implementation created:
   - Node definitions with prep/exec/post
   - SharedStore for state management
   - Utilities for common operations
   - Error handling and retry logic

4. **Enhanced Task Structure** ✅
   ```markdown
   ## Tasks (Orchestrated)
   
   ### Phase 1: Data Pipeline [VALIDATED]
   - [ ] 1.1 Create document loader (template: ingestion_node)
   - [ ] 1.2 Implement chunking strategy (template: text_chunker)
   - [ ] 1.3 Setup embedding generation (template: embedding_node)
   
   ### Phase 2: Vector Store [VALIDATED]
   - [ ] 2.1 Initialize vector database (template: vector_store)
   - [ ] 2.2 Implement indexing workflow (generated)
   - [ ] 2.3 Create search interface (template: retrieval_node)
   
   [GATE]: Design document must be complete
   [GATE]: Workflow implementation must be validated
   ```

### Executing with Intelligence

```
@execute-tasks

Let's implement the RAG system
```

**Orchestrated Execution:**

1. **Pre-flight Checks** ✓
   - Design document exists and complete
   - Workflow implementation validated
   - Dependencies resolved
   - Templates loaded

2. **Intelligent Implementation**
   - Uses generated workflow as blueprint
   - Implements from validated templates
   - Maintains type safety throughout
   - Includes optimization by default

3. **Automatic Validation**
   - Each task validated against design
   - Type checking enforced
   - Tests generated and run
   - Performance baselines checked

### Manual Orchestration

For explicit control:

```
@pocketflow-orchestrator

Think about the best architecture for a multi-agent customer service system
```

The orchestrator will:
- Analyze requirements
- Propose architecture
- Generate complete design
- Create implementation plan
- Produce workflow code

---

## Orchestration Patterns

### Pattern Recognition

The system automatically identifies and implements:

#### RAG Pattern
Triggered by: "search", "retrieval", "knowledge base", "documentation"
```python
class RAGFlow(Flow):
    """Auto-generated RAG workflow"""
    nodes = [
        DocumentLoaderNode(),
        ChunkingNode(),
        EmbeddingNode(),
        VectorStoreNode(),
        RetrievalNode(),
        GenerationNode()
    ]
```

#### Agent Pattern
Triggered by: "agent", "assistant", "autonomous", "decision"
```python
class AgentFlow(Flow):
    """Auto-generated agent workflow"""
    nodes = [
        IntentClassificationNode(),
        ToolSelectionNode(),
        ToolExecutionNode(),
        ResponseFormulationNode()
    ]
```

#### Tool Pattern
Triggered by: "function calling", "tool use", "API integration"
```python
class ToolFlow(Flow):
    """Auto-generated tool workflow"""
    nodes = [
        ToolRegistryNode(),
        ParameterValidationNode(),
        ToolInvocationNode(),
        ResultProcessingNode()
    ]
```

### Validation Gates

The system enforces quality through gates:

1. **Design Gate** - Must have complete design.md
2. **Architecture Gate** - Patterns must be identified
3. **Implementation Gate** - Workflow must be generated
4. **Testing Gate** - Tests must pass
5. **Performance Gate** - Baselines must be met

---

## Workflow Examples

### Example 1: Complex LLM Feature
```
User: I need to analyze customer emails, extract issues, 
      and generate responses with appropriate tone

System: [Orchestrator Activated]
→ Pattern: Hybrid (RAG + Agent)
→ Generates: Complete email processing workflow
→ Creates: 15+ nodes with full implementation
→ Produces: Tests, documentation, and deployment config
```

### Example 2: Simple CRUD (No Orchestration)
```
User: Add a basic user profile endpoint

System: [Standard Agent OS Mode]
→ Creates simple FastAPI endpoint
→ Basic implementation without orchestration
→ Standard task execution
```

### Example 3: Migration to PocketFlow
```
User: @analyze-product
      
      Convert our existing chatbot to use PocketFlow patterns

System: [Analysis + Orchestration]
→ Analyzes current implementation
→ Identifies improvement opportunities
→ Generates migration plan
→ Creates new PocketFlow implementation
→ Provides migration scripts
```

---

## Best Practices

### When Orchestration Activates

**Automatic Triggers:**
- LLM/AI keywords detected
- Complex multi-step workflows
- Pattern-based implementations needed
- "Think", "plan", "design" keywords used

**Manual Override:**
- Use `@pocketflow-orchestrator` directly
- Add "think about" before requests
- Request architectural planning

### Customizing Orchestration

#### Modify Triggers
Edit `.claude/agents/pocketflow-orchestrator.md`:
```yaml
auto_invoke_triggers:
  - "your custom trigger"
  - "domain-specific term"
```

#### Add Custom Patterns
Create in `~/.agent-os/templates/custom-patterns.md`:
```markdown
## Custom Pattern: Data Pipeline
Trigger: "ETL", "data processing", "pipeline"
Components: Extract, Transform, Load, Validate
Template: [Your custom implementation]
```

#### Adjust Validation
Edit `.agent-os/instructions/orchestration/coordination.yaml`:
```yaml
validation_gates:
  custom_gate:
    condition: "your_condition"
    action: "your_action"
```

### Performance Optimization

The system includes built-in optimizations:

1. **Caching by Default** - LLM responses cached automatically
2. **Batch Processing** - Groups operations when possible
3. **Async Execution** - Parallel processing where applicable
4. **Resource Management** - Connection pooling and lifecycle management

### Testing Strategy

Generated tests follow patterns:

```python
# Unit Tests - Generated for each node
def test_node_prep_phase():
    """Validate preparation logic"""

def test_node_exec_phase():
    """Validate execution logic"""

def test_node_error_handling():
    """Validate error scenarios"""

# Integration Tests - Generated for workflows
def test_flow_end_to_end():
    """Validate complete workflow"""

def test_flow_error_recovery():
    """Validate failure handling"""
```

---

## Troubleshooting

### Orchestrator Not Activating?
- Check CLAUDE.md exists with orchestration config
- Verify `.claude/agents/pocketflow-orchestrator.md` installed
- Try explicit invocation with `@pocketflow-orchestrator`
- Use trigger words: "think", "plan", "design"

### Design Document Missing?
- Orchestrator should auto-generate
- Check `.agent-os/workflows/` for implementations
- Run validation: `./scripts/validate-orchestration.sh`
- Manually invoke: `@pocketflow-orchestrator create design`

### Workflow Generation Failed?
- Verify templates exist in `~/.agent-os/templates/`
- Check pattern recognition in design.md
- Ensure Python environment setup (UV installed)
- Review orchestrator output for specific errors

### Validation Gates Blocking?
- Gates ensure quality—don't bypass
- Check gate requirements in error message
- Complete missing components
- Use `--force` flag only in development

---

## FAQ

### What is Agent OS + PocketFlow?

An intelligent orchestration system that enhances Agent OS with automatic pattern recognition, design generation, and workflow implementation for AI/LLM features. It transforms passive documentation into active architectural intelligence.

### How is this different from standard Agent OS?

**Standard Agent OS:** Documentation-driven, manual implementation
**With PocketFlow:** Intelligence-driven, automatic orchestration, pattern-based generation, validated workflows

### When does orchestration activate?

Automatically for:
- AI/LLM features
- Complex workflows
- Pattern-based implementations
- Keywords: "think", "plan", "design", "architect"

### Can I use it without orchestration?

Yes! Simple tasks bypass orchestration. The system intelligently determines when orchestration adds value.

### What patterns are included?

- **RAG Pattern** - Retrieval Augmented Generation
- **Agent Pattern** - Autonomous decision-making
- **Tool Pattern** - Function calling and API integration
- **Hybrid Patterns** - Combinations of above

### Is it Python-only?

Currently optimized for Python with FastAPI and PocketFlow. The orchestration concepts could be adapted for other languages.

### How does it handle existing code?

Use `@analyze-product` to:
- Understand current implementation
- Generate Agent OS documentation
- Identify PocketFlow migration opportunities
- Create compatibility layers

### Can I customize the orchestrator?

Yes! Modify:
- Triggers in `pocketflow-orchestrator.md`
- Templates in `~/.agent-os/templates/`
- Validation in `orchestration/coordination.yaml`
- Patterns in template files

### What about testing?

The system generates:
- Unit tests for each node
- Integration tests for workflows
- Performance benchmarks
- Error scenario validation

### How do updates work?

```bash
# Update orchestration components only
curl -sSL .../setup.sh | bash -s -- --update-orchestration

# Update everything (preserves customizations)
curl -sSL .../setup.sh | bash -s -- --update-all
```

---

## Advanced Features

### Custom Node Development

Create reusable nodes:

```python
# ~/.agent-os/templates/custom-nodes.py
class CustomAnalysisNode(Node):
    """Your domain-specific node"""
    
    def prep(self, store: SharedStore) -> Dict:
        # Preparation logic
        pass
    
    def exec(self, prep_data: Dict, store: SharedStore) -> Dict:
        # Execution logic
        pass
    
    def post(self, exec_result: Dict, store: SharedStore):
        # Post-processing logic
        pass
```

### Workflow Composition

Combine workflows:

```python
class CompositeFlow(Flow):
    """Combining multiple workflows"""
    
    def __init__(self):
        self.rag_flow = RAGFlow()
        self.agent_flow = AgentFlow()
        self.compose_sequential([
            self.rag_flow,
            self.agent_flow
        ])
```

### Performance Monitoring

Built-in metrics:

```python
# Auto-generated monitoring
class FlowMetrics:
    node_execution_times: Dict[str, float]
    llm_token_usage: Dict[str, int]
    cache_hit_rates: Dict[str, float]
    error_counts: Dict[str, int]
```

### Deployment Patterns

Generated deployment configs:

```yaml
# .agent-os/deployment/flow-config.yaml
flows:
  rag_system:
    workers: 4
    timeout: 30s
    retry_policy: exponential
    cache_ttl: 3600
```

---

## Conclusion

Agent OS + PocketFlow represents the evolution of AI-assisted development—from passive documentation to active intelligence. Your agents no longer just follow instructions; they think, design, and architect complete solutions.

The system maintains the simplicity of Agent OS for basic tasks while adding sophisticated orchestration for complex AI features. This isn't just about writing code faster—it's about building better architectures, implementing proven patterns, and shipping production-ready AI features with confidence.

Welcome to orchestrated development. Welcome to Agent OS + PocketFlow.

---

*© 2025 Agent OS + PocketFlow*

*Intelligent Orchestration for AI-Powered Development*

*Enhanced by the PocketFlow team building on Brian Casel's Agent OS foundation*