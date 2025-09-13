# Claude Code Sub-Agents: Complete Guide

## What are Sub-Agents?

Sub-agents are specialized AI assistants within Claude Code that handle specific tasks with their own configurations and contexts. Think of them as expert consultants that you can call upon for specialized work.

### Key Features
- **Isolated Context**: Each sub-agent operates in its own conversation context, preventing information spillover
- **Specialized Expertise**: Configured with specific system prompts for domain expertise
- **Tool Control**: Can be restricted to specific tools for security and focus
- **Automatic or Manual Invocation**: Claude Code can automatically choose the right sub-agent, or you can explicitly request one

## How Sub-Agents Work

When you invoke a sub-agent:
1. Claude Code creates a separate conversation context
2. Transfers relevant information from your main conversation
3. The sub-agent processes the task with its specialized configuration
4. Results are returned to your main conversation

## Creating Sub-Agents

### Using the `/agents` Command
```bash
/agents
```
This opens an interactive interface where you can:
- Create new sub-agents
- Modify existing ones
- Choose project-level or user-level storage
- Configure tool access

### File Structure
Sub-agents are stored as Markdown files with frontmatter:

```markdown
---
name: code-reviewer
description: Expert code review specialist. Use PROACTIVELY after writing or modifying code to ensure quality, security, and maintainability.
tools: Read, Edit, Grep, Bash
---

You are an expert code reviewer with deep knowledge of software engineering best practices, security vulnerabilities, and performance optimization.

Your role is to:
- Review code for bugs, security issues, and performance problems
- Check adherence to coding standards and best practices
- Suggest improvements for readability and maintainability
- Verify proper error handling and edge cases

Always provide specific, actionable feedback with code examples when possible.
```

### Storage Locations
- **Project-level**: `.claude/agents/` (committed to version control)
- **User-level**: `~/.claude/agents/` (personal, cross-project)

## Best Practices

### 1. Single Responsibility Principle
Create focused sub-agents that excel at one specific task:
```markdown
# Good
name: python-linter
description: Python code linting and formatting specialist

# Avoid
name: general-developer
description: Does everything development-related
```

### 2. Proactive Usage
Include keywords in descriptions to encourage automatic invocation:
```markdown
description: Security audit specialist. Use PROACTIVELY when code touches authentication, data handling, or external APIs.
```

### 3. Tool Restrictions
Limit tools to only what's necessary:
```markdown
tools: Read, Grep, WebSearch  # Security-focused sub-agent doesn't need Edit
```

### 4. Detailed System Prompts
Provide comprehensive guidance in the system prompt:
```markdown
---
name: test-engineer
description: Automated testing specialist for comprehensive test coverage
tools: Read, Write, Edit, Bash
---

You are a testing expert specializing in:
- Unit testing with appropriate frameworks
- Integration testing strategies  
- Test-driven development (TDD)
- Mocking and stubbing best practices

When reviewing code:
1. Identify untested code paths
2. Suggest appropriate test types (unit, integration, e2e)
3. Write comprehensive test cases
4. Ensure proper test organization and naming

Always follow the existing testing patterns in the codebase.
```

## Common Sub-Agent Types

### Development Specialists
- **Frontend Developer**: React/Vue/Angular UI specialist
- **Backend Engineer**: API and server-side logic expert  
- **Full Stack Developer**: End-to-end feature implementation
- **Database Expert**: SQL optimization and schema design

### Quality & Security
- **Code Reviewer**: Quality, security, and best practices
- **Security Auditor**: Vulnerability assessment and secure coding
- **Performance Engineer**: Optimization and profiling
- **Test Engineer**: Comprehensive testing strategies

### DevOps & Infrastructure
- **Cloud Architect**: AWS/GCP/Azure deployment expert
- **DevOps Engineer**: CI/CD and automation specialist
- **Container Expert**: Docker and Kubernetes specialist
- **Monitoring Specialist**: Observability and alerting

### Language Specialists
- **Python Expert**: Python ecosystem and best practices
- **TypeScript Pro**: TypeScript patterns and tooling
- **Rust Specialist**: Systems programming and safety
- **Go Expert**: Concurrent programming and microservices

## Implementation Patterns

### 1. Verification Workflow
```markdown
# Main conversation: Implement feature
# Sub-agent: Verify implementation quality
Use the code-reviewer sub-agent to verify this implementation
```

### 2. Multi-Stage Development
```markdown
1. Use architecture-designer to plan the system
2. Use backend-developer to implement APIs  
3. Use frontend-developer to build UI
4. Use test-engineer to add comprehensive tests
```

### 3. Problem Investigation
```markdown
# When debugging complex issues
Use the debugger sub-agent to analyze this stack trace and identify root causes
```

## Invocation Methods

### Automatic Delegation
Claude Code automatically chooses appropriate sub-agents based on context:
```bash
# This might automatically invoke a database expert
"Optimize this slow SQL query"
```

### Explicit Invocation
Request specific sub-agents:
```bash
"Use the security-auditor sub-agent to review this authentication code"
```

### Proactive Patterns
Configure sub-agents to be automatically suggested:
```markdown
description: Use PROACTIVELY when working with React components to ensure modern patterns and performance
```

## Advanced Configuration

### Custom Tool Sets
```markdown
---
name: data-analyst
tools: Read, mcp__database__query, WebSearch, mcp__visualization__create
---
```

### Context Passing
Sub-agents receive relevant context automatically, but you can be explicit:
```bash
"Use the python-expert sub-agent to refactor this function, keeping in mind our existing error handling patterns"
```

### Team Workflows
```markdown
# Different sub-agents for different team roles
- junior-mentor: Provides learning-focused explanations
- senior-reviewer: Performs architecture-level reviews
- tech-lead: Makes technical decisions and trade-offs
```

## Use Cases by Scenario

### New Feature Development
1. **Architect**: Design system structure
2. **Developer**: Implement core logic
3. **Reviewer**: Quality and security check
4. **Tester**: Comprehensive test coverage

### Bug Investigation
1. **Debugger**: Analyze logs and stack traces
2. **Performance**: Check for performance bottlenecks
3. **Security**: Verify no security implications

### Code Refactoring  
1. **Reviewer**: Identify refactoring opportunities
2. **Specialist**: Language-specific optimizations
3. **Tester**: Ensure behavior preservation

### Deployment & Operations
1. **DevOps**: Setup CI/CD pipeline
2. **Cloud**: Configure infrastructure
3. **Monitor**: Add observability

## Performance Considerations

### Benefits
- Preserves main conversation context
- Provides specialized expertise
- Reduces cognitive load on main conversation
- Enables parallel problem-solving approaches

### Trade-offs
- Slight latency for context transfer
- Additional complexity in workflow
- Need to manage multiple configurations

## Getting Started

1. **Start Simple**: Create 2-3 focused sub-agents for your most common tasks
2. **Iterate**: Refine prompts based on results
3. **Expand**: Add specialized sub-agents as needs arise
4. **Share**: Use project-level sub-agents for team consistency


This foundation covers most development workflows while remaining manageable and focused.