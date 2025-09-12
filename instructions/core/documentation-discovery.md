---
description: Documentation Discovery Rules for Agent OS
globs:
alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Documentation Discovery Rules

## Overview

<purpose>
  - Intelligently gather and process external documentation
  - Extract relevant patterns, constraints, and best practices
  - Integrate documentation insights into design and implementation
  - Maintain persistent documentation registry for reuse
</purpose>

<context>
  - Part of Agent OS framework Phase 2 enhancements
  - Supports plan-product and create-spec workflows
  - Enables design-first methodology with accurate technical context
</context>

## Handler Types

### URL Handler
**Purpose**: Fetch and analyze web-based documentation

**Capabilities**:
- Use WebFetch tool with targeted extraction prompts
- Cache fetched content with 24-hour TTL
- Extract: API methods, patterns, constraints, examples
- Support common documentation formats (HTML, Markdown)

**Process**:
1. Validate URL accessibility
2. Fetch content using WebFetch with specific extraction prompt
3. Parse and extract relevant technical information
4. Cache results with appropriate TTL
5. Return structured documentation data

### Local File Handler  
**Purpose**: Process local documentation files

**Capabilities**:
- Use Read tool for local documentation
- Support markdown, text, and structured formats
- Watch for file updates if in project directory
- Handle relative and absolute paths

**Process**:
1. Validate file path and accessibility
2. Read file content using Read tool
3. Parse content based on file format
4. Extract relevant sections and patterns
5. Return structured documentation data

### API Specification Handler
**Purpose**: Parse API specifications for integration details

**Capabilities**:
- Parse OpenAPI/Swagger specifications
- Extract endpoints, schemas, auth requirements
- Generate Pydantic models from schemas
- Identify rate limits and usage patterns

**Process**:
1. Detect specification format (OpenAPI, Swagger, etc.)
2. Parse specification structure
3. Extract API endpoints and methods
4. Map schemas to Pydantic model structures
5. Identify authentication and authorization patterns

### GitHub Repository Handler
**Purpose**: Extract documentation from GitHub repositories

**Capabilities**:
- Fetch README and docs/ directory
- Index code examples and patterns
- Extract from specific tagged versions
- Support both public and private repositories

**Process**:
1. Parse GitHub URL for repository information
2. Fetch README.md and documentation directory
3. Extract code examples and usage patterns
4. Index relevant sections for easy reference
5. Track version information for compatibility

## Processing Pipeline

### 1. Validation
**Objective**: Ensure documentation source is accessible and valid

**Steps**:
- Check source accessibility (URL reachable, file exists)
- Verify format compatibility with handlers
- Validate version requirements if applicable
- Confirm user permissions for private sources

**Error Handling**:
- Log inaccessible sources and provide fallback options
- Warn about version mismatches
- Provide alternative documentation suggestions

### 2. Extraction
**Objective**: Parse and extract relevant content from documentation

**Steps**:
- Parse documentation structure (headers, sections, code blocks)
- Extract relevant sections based on current workflow context
- Identify code examples and implementation patterns
- Capture version information and compatibility notes

**Context-Aware Extraction**:
- Plan-product context: Focus on architecture patterns, best practices
- Create-spec context: Focus on specific APIs, integration patterns
- Feature-specific context: Extract relevant functionality examples

### 3. Analysis
**Objective**: Map extracted content to PocketFlow patterns and constraints

**Steps**:
- Map documentation patterns to PocketFlow patterns (WORKFLOW, TOOL, AGENT, etc.)
- Identify technical constraints and requirements
- Extract best practices and anti-patterns
- Analyze compatibility with current tech stack

**Pattern Mapping**:
```python
documentation_patterns = {
    "api_endpoints": "TOOL pattern",
    "workflow_orchestration": "WORKFLOW pattern", 
    "decision_making": "AGENT pattern",
    "data_retrieval": "RAG pattern",
    "batch_processing": "MAPREDUCE pattern"
}
```

### 4. Integration
**Objective**: Store processed documentation and enrich workflow context

**Steps**:
- Update docs-registry.yaml with new documentation
- Enrich current workflow context with extracted insights
- Generate pattern recommendations based on documentation
- Create cross-references for easy access

**Registry Structure**:
```yaml
[source_name]:
  type: "framework|api|standard|compliance"
  source: "URL or local path"
  last_fetched: "YYYY-MM-DD"
  relevance: ["pattern", "constraints", "examples"]
  version: "version if applicable"
  extracted_patterns: ["list", "of", "relevant", "patterns"]
```

### 5. Caching
**Objective**: Optimize performance and reduce redundant fetches

**Caching Strategy**:
- Store processed documentation with TTL based on source type
- Track version changes for automatic invalidation
- Implement intelligent cache refresh for frequently accessed docs
- Provide cache bypass option for development

**TTL Guidelines**:
- Official framework docs: 24 hours
- API specifications: 12 hours
- GitHub repositories: 6 hours  
- Local files: Watch for file changes

## Documentation Extraction Prompts

### Tech Stack Documentation
```
Extract from this documentation:
1. Core architectural patterns and best practices
2. Common integration approaches
3. Performance considerations and constraints
4. Security recommendations
5. Code examples for typical use cases
6. Version compatibility requirements

Focus on information relevant to building applications with this technology.
```

### API Documentation  
```
Extract from this API documentation:
1. Available endpoints and methods
2. Request/response schemas
3. Authentication and authorization methods
4. Rate limits and usage guidelines
5. Error codes and handling patterns
6. Code examples for common operations

Provide information suitable for API integration planning.
```

### Internal Standards
```
Extract from this standards document:
1. Coding conventions and style guides
2. Architecture decision records
3. Security and compliance requirements
4. Testing and quality standards
5. Deployment and operations guidelines
6. Team workflow and collaboration patterns

Focus on standards that impact development decisions.
```

### Compliance Documentation
```
Extract from this compliance documentation:
1. Regulatory requirements and constraints
2. Data handling and privacy requirements
3. Security control implementations
4. Audit and reporting requirements
5. Technical safeguards and controls
6. Compliance validation approaches

Focus on technical implementation requirements.
```

## Smart Features

### Pattern Detection Algorithm
**Objective**: Automatically suggest relevant documentation based on context

```python
def detect_documentation_needs(spec_text, context="create-spec"):
    """
    Detect documentation needs based on spec content and context
    
    Args:
        spec_text: Text content of specification
        context: Workflow context (plan-product, create-spec)
    
    Returns:
        List of suggested documentation categories
    """
    tech_patterns = {
        "stripe": ["payment", "subscription", "checkout", "billing"],
        "auth0": ["authentication", "login", "jwt", "oauth"],
        "aws": ["s3", "lambda", "dynamodb", "sqs"],
        "fastapi": ["api", "endpoint", "router", "dependency"],
        "django": ["model", "view", "template", "orm"],
        "react": ["component", "jsx", "state", "hook"],
        "postgresql": ["database", "query", "transaction", "index"]
    }
    
    suggested_docs = []
    for tech, patterns in tech_patterns.items():
        if any(pattern in spec_text.lower() for pattern in patterns):
            if tech not in current_docs_registry():
                suggested_docs.append({
                    "technology": tech,
                    "reason": f"Detected {tech} patterns in specification",
                    "priority": "high" if context == "create-spec" else "medium"
                })
    
    return suggested_docs
```

### Progressive Disclosure Strategy
**Objective**: Load documentation depth based on workflow needs

**Loading Strategy**:
1. **Initial Load**: High-level overview and getting started sections
2. **Feature Planning**: Drill down to specific functionality documentation  
3. **Implementation Phase**: Load detailed API references and examples
4. **Optimization Phase**: Access performance and best practices sections

**Implementation**:
```python
disclosure_levels = {
    "overview": ["introduction", "getting-started", "overview"],
    "planning": ["architecture", "patterns", "best-practices"],
    "implementation": ["api-reference", "examples", "integration"],
    "optimization": ["performance", "scaling", "troubleshooting"]
}
```

### Version Management
**Objective**: Track and manage documentation version compatibility

**Features**:
- Track framework/API versions in registry
- Warn when documentation version differs from project requirements
- Suggest documentation updates when versions change
- Maintain version-specific documentation cache

**Version Tracking**:
```yaml
version_tracking:
  framework_version: "1.2.3"
  docs_version: "1.2.x"  
  compatibility_status: "compatible|warning|incompatible"
  last_checked: "2025-01-12"
  update_available: true
```

## Error Handling and Fallbacks

### Documentation Fetch Failures
**Mitigation Strategies**:
- Implement robust fallback mechanisms
- Cache previously fetched documentation for offline access
- Allow manual documentation upload as backup
- Provide alternative documentation source suggestions

### Outdated Documentation
**Mitigation Strategies**:
- Version tracking and compatibility warnings
- Regular cache refresh cycles with user notifications
- User confirmation prompts for old documentation
- Automatic suggestions for updated documentation sources

### Information Overload
**Mitigation Strategies**:
- Progressive disclosure based on workflow context
- Context-aware filtering and relevance scoring
- Relevance scoring for documentation sections
- User preferences for documentation depth

### Performance Impact
**Mitigation Strategies**:
- Asynchronous fetching to avoid blocking workflows
- Intelligent caching strategies with appropriate TTLs
- Lazy loading of documentation sections
- Background refresh of frequently accessed documentation

## Integration with Existing Workflows

### Plan-Product Integration
**Enhancement**: Step 1.6 documentation discovery prompts
**Context**: Gather foundational documentation for product architecture
**Focus**: Framework patterns, architectural constraints, compliance requirements

### Create-Spec Integration  
**Enhancement**: Step 3 pattern detection and suggestions
**Context**: Feature-specific documentation for implementation planning
**Focus**: API integrations, specific functionality, implementation patterns

### Execute-Tasks Integration
**Enhancement**: Documentation validation during implementation
**Context**: Verify implementation against documented best practices
**Focus**: Code examples, implementation patterns, testing approaches

## Registry Management

### Registry Structure
**Location**: `.agent-os/docs-registry.yaml`
**Purpose**: Central registry for all documentation references

**Schema**:
```yaml
version: 1.0.0
last_updated: YYYY-MM-DD

tech_stack:
  [framework_name]:
    type: "framework|library|tool"
    source: "URL or local path"
    last_fetched: "YYYY-MM-DD"
    relevance: ["list", "of", "relevant", "topics"]
    version: "framework version if applicable"
    
external_apis:
  [api_name]:
    type: "rest|graphql|websocket|custom"
    source: "URL or local path"
    spec_format: "openapi|swagger|custom"
    relevance: ["integration points"]
    
internal_standards:
  [standard_name]:
    type: "architecture|style|security|compliance"
    source: "local path or URL"
    relevance: ["applicable areas"]
    
compliance:
  [compliance_type]:
    type: "regulatory|security|industry"
    source: "documentation location"
    requirements: ["key requirements"]
```

### Registry Operations
**Initialize**: Create registry on first documentation discovery
**Update**: Add new documentation sources and refresh existing entries
**Validate**: Ensure registry integrity and source accessibility
**Cleanup**: Remove outdated or inaccessible documentation references

## Usage Examples

### Example 1: FastAPI Project Documentation Discovery
```yaml
# User provides FastAPI documentation
tech_stack:
  fastapi:
    type: "framework"
    source: "https://fastapi.tiangolo.com/"
    last_fetched: "2025-01-12"
    relevance: ["api_patterns", "dependency_injection", "async_support"]
    version: "0.104.1"
    extracted_patterns: 
      - "API endpoint definition patterns"
      - "Pydantic model integration"
      - "Dependency injection for utilities"
```

### Example 2: Stripe API Integration
```yaml  
# User provides Stripe API documentation
external_apis:
  stripe:
    type: "rest"
    source: "https://stripe.com/docs/api"
    spec_format: "openapi"
    last_fetched: "2025-01-12"
    relevance: ["payment_processing", "webhook_handling", "subscription_management"]
    extracted_patterns:
      - "Payment intent workflow"
      - "Webhook signature verification"
      - "Error handling patterns"
```

## Best Practices

### Documentation Selection
- Prefer official documentation over third-party sources
- Use version-specific documentation when available
- Validate documentation currency and accuracy
- Consider team expertise and familiarity

### Context-Aware Processing
- Tailor extraction based on current workflow phase
- Focus on immediately relevant information
- Avoid information overload with progressive disclosure
- Maintain clear connection between documentation and implementation

### Quality Assurance
- Validate extracted patterns against known best practices
- Cross-reference multiple documentation sources when possible
- Maintain audit trail of documentation decisions
- Regular review and update of documentation registry

### Performance Optimization
- Cache frequently accessed documentation
- Use asynchronous processing for large documentation sets
- Implement intelligent refresh strategies
- Monitor and optimize documentation processing performance

## Orchestration Integration

@include orchestration/orchestrator-hooks.md

This instruction integrates with the orchestrator system for coordinated documentation discovery and processing.