# Documentation Discovery User Guide

> Intelligent External Documentation Integration for Agent OS + PocketFlow Projects

## Overview

The Documentation Discovery system automatically gathers and processes external documentation to provide accurate technical context during development. It integrates seamlessly with Agent OS workflows to ensure your AI agents have access to the latest technical information when planning and implementing features.

### What Documentation Discovery Provides

- **Intelligent Pattern Detection**: Automatically suggests relevant documentation based on your specifications
- **Smart Caching**: Optimizes performance with intelligent refresh strategies  
- **Version Management**: Tracks compatibility between documentation and your project dependencies
- **Progressive Disclosure**: Shows the right level of detail based on your current workflow phase
- **Context-Aware Processing**: Extracts relevant information based on whether you're planning, specifying, or implementing

## How It Works

Documentation Discovery operates through three main phases integrated into your Agent OS workflows:

### 1. **Product Planning Phase** (`/plan-product`)
During project initialization, Step 1.6 prompts you to provide documentation sources for:
- **Tech Stack Documentation** (frameworks, libraries, tools)
- **External API Documentation** (third-party services, APIs)
- **Internal Standards & Architecture** (company guidelines, patterns)
- **Compliance & Security Requirements** (regulatory, industry standards)

### 2. **Feature Specification Phase** (`/create-spec`)
When creating feature specifications, the system automatically:
- Detects technology patterns in your spec
- Suggests relevant documentation sources
- Validates compatibility with existing documentation
- Enriches your planning context with extracted insights

### 3. **Implementation Phase** (`/execute-tasks`)
During task execution, the system:
- Validates documentation registry accessibility
- Provides implementation-specific technical context
- Suggests critical documentation for successful implementation
- Warns about outdated or inaccessible sources

## Getting Started

### Initial Setup

Documentation Discovery is automatically available in all Agent OS + PocketFlow projects. No additional setup is required.

### First Time Usage

1. **Initialize Your Project**: Run `/plan-product` as normal
2. **Provide Documentation**: When prompted at Step 1.6, provide documentation sources
3. **Choose Categories**: Select from tech stack, APIs, standards, or compliance docs
4. **Specify Sources**: Provide URLs, local file paths, or skip categories as needed

### Example Documentation Discovery Session

```
I can reference external documentation to ensure accurate technical implementation.
Would you like me to incorporate any of the following?

1. **Tech Stack Documentation** 
   Examples: FastAPI docs, Next.js guides, Django documentation
   
2. **External API Documentation**
   Examples: Stripe API, Auth0, AWS services, custom APIs
   
3. **Internal Standards & Architecture**
   Examples: Company style guides, architecture decisions, design systems
   
4. **Compliance & Security Requirements**
   Examples: HIPAA, SOC2, GDPR, security policies

For each category you want to include:
- Provide a URL to fetch documentation from, OR
- Provide a local file path (starting with / or ~), OR  
- Type 'skip' to proceed without

Format: [category_number]: [url_or_path_or_skip]
```

**Your Response Examples:**
```
1: https://fastapi.tiangolo.com/
2: https://stripe.com/docs/api  
3: ~/company-docs/api-standards.md
4: skip
```

## Documentation Sources

### Supported Source Types

#### 1. **Web URLs**
- **Format**: `https://example.com/docs`
- **Supports**: Official documentation sites, GitHub wikis, API references
- **Processing**: Fetches content, extracts patterns, caches with 24-hour TTL
- **Examples**: 
  - `https://fastapi.tiangolo.com/`
  - `https://docs.stripe.com/api`
  - `https://reactjs.org/docs`

#### 2. **Local Files**
- **Format**: `/absolute/path/file.md` or `~/relative/path/file.md`
- **Supports**: Markdown, text, YAML, JSON files
- **Processing**: Reads local content, watches for updates
- **Examples**:
  - `~/company-docs/coding-standards.md`
  - `/project/docs/architecture-decisions.md`

#### 3. **GitHub Repositories** (via URL handler)
- **Format**: `https://github.com/owner/repo`
- **Supports**: README files, docs/ directories, specific file paths
- **Processing**: Extracts documentation and code examples
- **Examples**:
  - `https://github.com/tiangolo/fastapi`
  - `https://github.com/your-org/internal-standards`

#### 4. **API Specifications** (detected automatically)
- **Format**: URLs pointing to OpenAPI/Swagger specifications
- **Supports**: OpenAPI 3.0, Swagger 2.0 specifications
- **Processing**: Parses endpoints, schemas, generates integration patterns
- **Examples**:
  - `https://api.stripe.com/v1/openapi.json`
  - `https://petstore.swagger.io/v2/swagger.json`

## Smart Features

### Pattern Detection

The system automatically detects 14+ technology patterns in your specifications:

- **Payment Processing**: Stripe, PayPal patterns
- **Authentication**: Auth0, OAuth, JWT patterns  
- **Cloud Infrastructure**: AWS, Azure, GCP services
- **API Frameworks**: FastAPI, Django, Express patterns
- **Frontend Frameworks**: React, Vue, Angular patterns
- **Databases**: PostgreSQL, MongoDB, Redis patterns
- **AI Services**: OpenAI, Anthropic, LangChain patterns

**Example Detection:**
```yaml
# From specification: "payment processing with Stripe and PostgreSQL database"
pattern_suggestions:
  - technology: stripe
    priority: critical
    confidence: 90%
    matched_patterns: [payment, subscription, webhook]
  - technology: postgresql  
    priority: high
    confidence: 85%
    matched_patterns: [database, query, schema]
```

### Progressive Disclosure

Documentation is loaded at different levels based on your workflow phase:

#### **Overview Level** (Product Planning)
- Introduction and getting-started guides
- Core concepts and terminology
- Cache TTL: 24 hours

#### **Planning Level** (Feature Specification)  
- Architecture patterns and best practices
- Design principles and constraints
- Cache TTL: 12 hours

#### **Implementation Level** (Task Execution)
- API references and code examples
- Integration guides and configuration
- Cache TTL: 6 hours

#### **Optimization Level** (Post-Implementation)
- Performance tuning and scaling
- Troubleshooting and monitoring
- Cache TTL: 24 hours

### Version Management

The system tracks version compatibility between documentation and your project:

- **Semantic Versioning**: Detects major.minor.patch versions
- **Date Versioning**: Handles YYYY-MM-DD versioned documentation  
- **Compatibility Warnings**: Alerts about version mismatches
- **Automatic Detection**: Extracts version info from documentation content

**Example Compatibility Check:**
```yaml
compatibility_report:
  technology: fastapi
  registry_version: "0.104.1"
  project_version: "0.103.0"  
  status: probably_compatible
  warnings:
    - "Minor version difference: docs=0.104.1, project=0.103.0"
```

## Documentation Registry

### Registry Structure

All processed documentation is stored in `.agent-os/docs-registry.yaml`:

```yaml
version: 1.0.0
last_updated: 2025-01-12

tech_stack:
  fastapi:
    type: framework
    source: https://fastapi.tiangolo.com/
    last_fetched: 2025-01-12
    relevance: [api_patterns, dependency_injection, async_support]
    version: 0.104.1
    extracted_patterns:
      - API endpoint definition patterns
      - Pydantic model integration
      - Dependency injection for utilities

external_apis:
  stripe:
    type: rest
    source: https://stripe.com/docs/api
    spec_format: openapi
    last_fetched: 2025-01-12
    relevance: [payment_processing, webhook_handling]
    extracted_patterns:
      - Payment intent workflow patterns
      - Webhook signature verification
```

### Registry Management

The registry is automatically maintained but you can manually manage it:

#### **Validation**
```bash
# Validate registry structure and accessibility
python scripts/validate-docs-registry.py .agent-os/docs-registry.yaml
```

#### **Manual Updates**
- Edit `.agent-os/docs-registry.yaml` directly
- Add new documentation sources
- Update version information
- Modify relevance categories

#### **Cache Management**
- Cache stored in `.agent-os/cache/` directory
- Automatic refresh based on TTL settings
- Manual cache clearing by deleting cache files

## Workflow Integration Examples

### Example 1: FastAPI Project with Stripe Integration

**Initial Setup (`/plan-product`):**
```
1: https://fastapi.tiangolo.com/
2: https://stripe.com/docs/api
3: skip
4: skip
```

**Generated Registry:**
```yaml
tech_stack:
  fastapi:
    type: framework
    source: https://fastapi.tiangolo.com/
    extracted_patterns:
      - API endpoint definition patterns
      - Pydantic model integration
      
external_apis:
  stripe:
    type: rest
    source: https://stripe.com/docs/api
    extracted_patterns:
      - Payment intent workflow patterns
      - Webhook signature verification
```

**Feature Specification (`/create-spec subscription-management`):**
- System detects "subscription" and "payment" patterns
- Suggests Stripe documentation sections
- Provides implementation-level progressive disclosure
- Validates compatibility with project FastAPI version

**Task Execution (`/execute-tasks`):**
- Validates registry accessibility
- Suggests critical Stripe integration documentation
- Provides FastAPI-specific implementation patterns
- Ensures design document includes payment flow architecture

### Example 2: Internal Standards Compliance

**Documentation Source:**
```
3: ~/company-docs/api-standards.md
4: ~/compliance/hipaa-requirements.md
```

**Registry Integration:**
```yaml
internal_standards:
  api_standards:
    type: architecture
    source: ~/company-docs/api-standards.md
    last_fetched: 2025-01-12
    relevance: [naming_conventions, error_handling, security]
    
compliance:
  hipaa:
    type: regulatory
    source: ~/compliance/hipaa-requirements.md
    requirements:
      - Data encryption at rest and in transit
      - Access logging and audit trails
    technical_controls:
      - Database encryption implementation
      - API authentication and authorization
```

**Workflow Benefits:**
- Company standards automatically enforced during implementation
- Compliance requirements integrated into design validation
- Technical controls suggested based on regulatory needs

## Troubleshooting

### Common Issues

#### **Documentation Source Inaccessible**
```
⚠️ Documentation Registry Issues Detected

Issues Found:
- https://example.com/docs: Connection timeout
- ~/missing-file.md: File not found

Recommendations:
1. Update inaccessible documentation sources
2. Consider using alternative documentation URLs
```

**Solutions:**
- Update URLs in `.agent-os/docs-registry.yaml`
- Check network connectivity for external sources
- Verify local file paths exist and are readable

#### **Version Compatibility Warnings**
```
⚠️ Version Compatibility Issues

fastapi: docs=0.104.1, project=0.100.0 (major difference)
stripe: docs=2023-10-16, project=unknown (cannot compare)
```

**Solutions:**
- Update project dependencies to match documentation versions
- Add version information to project configuration
- Use version-specific documentation URLs

#### **Stale Documentation Cache**
```
⚠️ Registry hasn't been updated in 45 days - consider reviewing
```

**Solutions:**
- Re-run `/plan-product` to refresh documentation
- Manually update `last_fetched` dates in registry
- Clear cache directory to force refresh

### Performance Optimization

#### **Large Documentation Sets**
- Use progressive disclosure to load only relevant sections
- Enable caching to avoid repeated fetches
- Configure appropriate TTL values for different source types

#### **Network Constraints**
- Prefer local documentation sources when available
- Use cached content for offline development
- Configure longer TTL values to reduce network requests

#### **Registry Size Management**
- Remove unused documentation entries
- Use relevance filtering to focus on current needs
- Regular cleanup of stale or outdated sources

## Best Practices

### Documentation Selection

1. **Prioritize Official Sources**: Use official documentation over third-party guides
2. **Version-Specific URLs**: Link to specific version documentation when available
3. **Validate Currency**: Ensure documentation reflects current API versions
4. **Consider Team Expertise**: Include documentation appropriate for team skill level

### Registry Maintenance

1. **Regular Reviews**: Update registry quarterly or after major dependency updates
2. **Source Validation**: Test documentation accessibility before major implementations
3. **Version Tracking**: Keep documentation versions in sync with project dependencies
4. **Relevance Curation**: Update relevance categories based on actual usage patterns

### Workflow Integration

1. **Early Planning**: Provide documentation during initial product planning
2. **Context-Specific Sources**: Add feature-specific documentation during spec creation
3. **Implementation Focus**: Use implementation-level disclosure during task execution
4. **Continuous Updates**: Refresh documentation as project requirements evolve

## Advanced Configuration

### Custom Pattern Detection

Add custom technology patterns to smart features:

```python
# In pocketflow-tools/smart_features.py (framework development)
custom_patterns = {
    "your_custom_tech": {
        "patterns": ["custom", "pattern", "keywords"],
        "weight": 3,
        "category": "custom_category",
        "contexts": ["create-spec", "execute-tasks"]
    }
}
```

### Cache Configuration

Customize caching behavior:

```yaml
# In docs-registry.yaml
smart_features:
  progressive_disclosure:
    cache_ttl_hours:
      overview: 48      # Longer cache for stable content
      planning: 6       # Shorter cache for evolving content
      implementation: 2  # Very short cache for detailed references
      optimization: 24
```

### Registry Schema Extensions

Add custom metadata to registry entries:

```yaml
tech_stack:
  custom_framework:
    type: framework
    source: https://docs.example.com
    # Standard fields...
    custom_metadata:
      internal_contact: "dev-team@company.com"  
      migration_guide: "https://migration.example.com"
      support_level: "enterprise"
```

## Integration with Other Agent OS Features

### PocketFlow Pattern Detection

Documentation Discovery integrates with PocketFlow pattern selection:

- **Pattern Mapping**: Maps documentation patterns to PocketFlow patterns (WORKFLOW, TOOL, AGENT, etc.)
- **Design Integration**: Extracted patterns inform design document creation
- **Implementation Guidance**: Provides pattern-specific implementation examples

### Agent Coordination

Smart suggestions coordinate with other Agent OS agents:

- **Strategic Planner**: Documentation insights inform strategic planning
- **Pattern Analyzer**: Documentation patterns enhance pattern analysis
- **Context Fetcher**: Documentation content enriches implementation context

### Template Generation

Documentation Discovery enhances template generation:

- **Context-Aware Templates**: Generated templates include relevant documentation references
- **Pattern-Specific Examples**: Templates include examples from discovered documentation
- **Best Practice Integration**: Templates incorporate best practices from documentation sources

## Support and Troubleshooting

### Getting Help

1. **Validation Scripts**: Use `scripts/validate-docs-registry.py` for registry validation
2. **Test Suite**: Run `pocketflow-tools/test_smart_features.py` for functionality testing
3. **Debug Mode**: Enable verbose logging in smart features for detailed analysis

### Reporting Issues

When reporting issues, include:

1. **Registry Content**: Copy of `.agent-os/docs-registry.yaml`
2. **Error Messages**: Full error output from validation scripts
3. **Source Accessibility**: Results of manual source verification
4. **Context Information**: Current workflow phase and specifications

### Community Resources

- **Framework Documentation**: See main Agent OS documentation
- **Pattern Examples**: Review `templates/examples/` for usage patterns
- **Best Practices**: Check `docs/` directory for additional guides

---

*This guide covers the complete Documentation Discovery system. For framework development details, see the technical documentation in `instructions/core/documentation-discovery.md`.*