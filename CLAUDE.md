# Agent OS + PocketFlow Integration Project

> **Status**: Core Integration Complete ✅ | Additional Files & Logic Needed 🔄
> **Last Updated**: 2025-01-09

## Claude Code High Level Instructions

You are a senior software engineer fluent in modern Python development practices, particularly with FastAPI and Pydantic. You are tasked with integrating **Agent OS** and **PocketFlow** into a cohesive development framework. Your focus is on maintaining structured workflows, type safety, and design-first principles. You
should always follow the **Agent OS** and **PocketFlow** integration patterns when developing new features or updating existing code. This document outlines the key principles, architecture, and workflows for using this integrated system effectively.

Repsoned in concise and clear language. Ask clarifying questions if needed, but do not make assumptions about the project scope or requirements. Always refer to the provided documentation for guidance on specific tasks.


## Project Overview

This project successfully integrates **Agent OS** (structured AI development workflows) with **PocketFlow** (design-first LLM framework) to create a modern Python-based development system. The integration combines Agent OS's proven workflow management with PocketFlow's 8-step Agentic Coding methodology and a contemporary Python tech stack.

## What We've Accomplished

### ✅ Complete 3-Phase Integration

**Phase 1: create-spec.md Updates**
- Added mandatory design document creation step (docs/design.md)
- Enhanced LLM workflow specifications with Pydantic schemas
- Included FastAPI endpoint specifications  
- Updated task breakdown to follow 8-step methodology

**Phase 2: execute-tasks.md Updates**
- Added design document validation before implementation
- Restructured implementation phases (schemas→utilities→APIs→nodes→flows)
- Integrated comprehensive development toolchain (Ruff, ty, pytest)
- Added type safety validation steps

**Phase 3: plan-product.md Updates**
- Updated tech stack defaults to Python/FastAPI/Pydantic
- Enhanced mission and roadmap templates with LLM strategy sections
- Added standard project structure template
- Integrated PocketFlow design patterns

### ✅ Complete File Migration
- All standards files updated with PocketFlow methodology
- All instruction files enhanced with modern Python stack
- New templates directory with comprehensive workflow templates


## Architecture Integration

### Core Pattern: FastAPI + PocketFlow
```
FastAPI (main.py) → Pydantic Models (schemas/) → PocketFlow Flows (flow.py) → PocketFlow Nodes (nodes.py) → Utility Functions (utils/)
```

### Standard Project Structure
```
project/
├── main.py           # FastAPI app entry point
├── nodes.py          # PocketFlow nodes
├── flow.py           # PocketFlow flows  
├── schemas/          # Pydantic models
│   ├── requests.py   # API request models
│   └── responses.py  # API response models
├── utils/            # Custom utilities (call_llm.py, etc.)
├── docs/
│   └── design.md     # MANDATORY design document
└── requirements.txt
```

### 8-Step Agentic Coding Integration
1. **Requirements** - Clarify project needs and AI system fit
2. **Flow Design** - High-level workflow with Mermaid diagrams
3. **Utilities** - External API wrappers and integrations
4. **Data Design** - SharedStore schema using Pydantic models
5. **Node Design** - PocketFlow node specifications
6. **Implementation** - Code following design.md specifications
7. **Optimization** - Performance tuning and prompt engineering
8. **Reliability** - Error handling, retries, and comprehensive testing

## Documentation Locations

### Primary Documentation
- **Agent OS Full Docs**: `WorkingFiles/docs/agent-os-full-documentation.md`
- **PocketFlow Guidelines**: `WorkingFiles/docs/PocketFlowGuidelines.md`
- **Integration Plan**: `WorkingFiles/docs/agent-os-pocketflow-integration-plan.md`

### Key References
- Agent OS focuses on structured workflows and project management
- PocketFlow provides LLM development methodology and code patterns
- Integration plan contains detailed implementation specifics

## Files Created/Updated

### Standards Files (Enhanced)
- `standards/tech-stack.md` - Python 3.12+, FastAPI, Pydantic, uv defaults
- `standards/code-style.md` - Python formatting with Ruff, type safety emphasis
- `standards/best-practices.md` - PocketFlow methodology, design-first philosophy
- `standards/pocket-flow.md` - **NEW** - Comprehensive PocketFlow workflow guidance

### Instruction Files (Enhanced)
- `instructions/create-spec.md` - Mandatory design docs, PocketFlow workflow sections
- `instructions/execute-tasks.md` - Design validation, 8-step methodology, type safety
- `instructions/plan-product.md` - LLM strategy sections, modern tech stack defaults
- `instructions/analyze-product.md` - Updated for Python/PocketFlow analysis

### Templates Directory (NEW)
- `templates/pocketflow-templates.md` - Complete PocketFlow workflow templates
- `templates/fastapi-templates.md` - FastAPI + Pydantic integration templates  
- `templates/task-templates.md` - 8-step methodology task breakdowns

### Infrastructure (Preserved)
- All original Agent OS commands and setup scripts maintained
- Compatible with existing Agent OS command structure (`/plan-product`, `/create-spec`, etc.)
- Claude Code integration preserved and enhanced

## Tech Stack Summary

### Core Technologies
- **Language**: Python 3.12+
- **Web Framework**: FastAPI (serves MCP endpoints)
- **Data Validation**: Pydantic (type safety at all boundaries)
- **Package Manager**: uv (modern Python package management)
- **LLM Framework**: PocketFlow (design-first workflow orchestration)

### Development Tooling
- **Linting/Formatting**: Ruff (`ruff check --fix . && ruff format .`)
- **Type Checking**: ty (`uvx ty check`)
- **Testing**: pytest with comprehensive test suites
- **API Documentation**: FastAPI automatic OpenAPI generation

### Integration Patterns
- **Type Safety**: Pydantic models for all data structures
- **Error Handling**: Node retry mechanisms (no try/except in utilities)
- **API Pattern**: FastAPI endpoint → PocketFlow Flow → Pydantic response
- **Design-First**: Mandatory docs/design.md before any implementation

## Development Philosophy

### Key Principles
1. **Design Before Code** - Always create docs/design.md with Mermaid diagrams
2. **Utility Function Approach** - "Examples provided, implement your own" 
3. **Type Safety First** - Pydantic validation at every boundary
4. **Fail Fast** - Use Node retry mechanisms, avoid inline error handling
5. **Standards Driven** - Consistent code style and architectural patterns

### Workflow Integration
- Agent OS provides structured project management and context layering
- PocketFlow provides LLM-specific development methodology and code patterns
- FastAPI provides modern Python web framework with automatic API docs
- Pydantic ensures type safety and data validation throughout

## Next Steps Context

### Current Status
✅ **Core Integration Complete** - Standards and instruction files successfully updated
✅ **Architecture Defined** - Clear patterns for FastAPI + PocketFlow development  
✅ **Documentation Framework** - Templates and examples provided

### Remaining Work
🔄 **Additional Files & Logic** - Need to update additional files to match current project structure
🔄 **Implementation Alignment** - Ensure all components work cohesively with integrated approach
🔄 **Validation & Testing** - Test updated workflows with real projects
🔄 **Scope Refinement** - Determine full extent of remaining integration work

### Current State
- Foundation integration work completed (standards, core instructions, templates)
- Additional files and logic updates needed for complete integration
- Project scope still being evaluated and refined
- Not yet ready for production use - integration work ongoing


This integrated system provides structured, standards-driven development workflows specifically optimized for building LLM applications with modern Python tooling.