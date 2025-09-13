# Detailed Report: Non-Test Files in `framework-tools/`

## 🏗️ Core Framework Infrastructure

### **`agent_coordination.py`**
**Purpose:** Runtime coordination system managing handoffs between PocketFlow sub-agents  
**Key Functions:** Orchestrates pattern-analyzer, design-document-creator, strategic-planner, file-creator, and template-validator agents  
**Context:** Handles coordination state during agent workflows (different from context_manager.py which extracts design-time context)

### **`context_manager.py`**
**Purpose:** Design-time context extraction from project documentation  
**Key Functions:** Extracts requirements, design, and architecture from repository docs to inform PocketFlow generation  
**Context:** Planning-to-implementation handoff utility (Phase 2 implementation)

### **`dependency_orchestrator.py`**
**Purpose:** Manages Python tooling and dependency configurations for generated templates  
**Key Functions:** Handles pyproject.toml generation, dependency specifications, development environment setup

## 🔍 Analysis & Validation Tools

### **`antipattern_detector.py`**
**Purpose:** Code quality analysis tool identifying common PocketFlow implementation mistakes  
**Key Functions:** AST-based pattern detection, antipattern identification, quality assurance  
**Usage:** `python antipattern_detector.py [path] [options]`

### **`antipattern_demo.py`**
**Purpose:** Educational demonstration file containing intentional antipatterns  
**Key Functions:** Showcases both good/bad patterns for detector testing and learning  
**Context:** Framework repository code with mock classes (doesn't require PocketFlow installation)

### **`pattern_analyzer.py`**
**Purpose:** Core pattern analysis engine analyzing user requirements  
**Key Functions:** Identifies optimal PocketFlow patterns (RAG, AGENT, WORKFLOW, TOOL)  
**Integration:** Used by Pattern Analyzer Agent for requirement analysis

### **`pattern_definitions.py`**
**Purpose:** Centralized pattern definitions and node templates  
**Key Functions:** Single source of truth for pattern structures, canonical pattern data  
**Usage:** Imported by both generator and workflow graph generator

### **`template_validator.py`**
**Purpose:** Validation engine for generated PocketFlow templates  
**Key Functions:** Validates template structure, syntax, and compliance with framework standards  
**Integration:** Core validation logic used by template-validator agent

## 📊 Reporting & Feedback Systems

### **`status_reporter.py`**
**Purpose:** Enhanced user feedback and progress tracking system  
**Key Functions:** Workflow progress reporting, operation status tracking, user notifications  
**Context:** Phase 3 implementation for improved user experience

### **`validation_feedback.py`**
**Purpose:** Intelligent feedback loops between validation results and template generation  
**Key Functions:** Processes validation errors, suggests improvements, implements feedback cycles  
**Context:** Phase 2 feedback requirements implementation

### **`workflow_graph_generator.py`**
**Purpose:** Generates Mermaid diagrams and workflow structures  
**Key Functions:** Visual workflow representation, pattern-based graph generation  
**Integration:** Part of Pattern Analyzer Agent for workflow visualization

## 🛠️ Development & Testing Utilities

### **`check-pocketflow-install.py`**
**Purpose:** Installation checker for target projects  
**Key Functions:** Verifies PocketFlow dependencies, optional automatic installation  
**Usage:** `python check-pocketflow-install.py [--install]`

### **`test-generator.py`**
**Purpose:** Test script for workflow generator without external dependencies  
**Key Functions:** Tests generator functionality, validates imports, framework testing

## 📁 Generated Example Project

### **`testcontentanalyzer/`**
**Purpose:** Complete generated PocketFlow project for validation and testing  
**Description:** AI-powered content analysis tool demonstrating RAG pattern implementation  
**Key Files:**
- `flow.py` - Main PocketFlow workflow implementation
- `nodes.py` - Custom PocketFlow nodes for content analysis  
- `main.py` - FastAPI application entry point
- `schemas/models.py` - Pydantic data models
- `utils/` - Custom utility functions for content analysis
- `.agent-os/` - Complete Agent OS configuration for the project

**Architecture:** Uses PocketFlow RAG pattern for content analysis with multi-LLM support (GPT-4, Claude, Gemini)

## Summary

The `framework-tools/` directory serves as a comprehensive **framework development workspace** containing:

- **Core orchestration tools** for managing agent workflows
- **Analysis engines** for pattern detection and validation  
- **Code quality tools** for antipattern detection
- **Reporting systems** for user feedback and progress tracking
- **Development utilities** for testing and validation
- **Complete working example** demonstrating real-world PocketFlow usage

This is much more than just testing - it's the complete development and validation infrastructure for the Agent OS + PocketFlow framework.

## Framework vs Usage Context

**Important Note:** This repository IS the Agent OS + PocketFlow framework itself, NOT a project using it.

- `pocketflow_tools/` (underscore) = The installable Python package 
- `framework-tools/` (hyphen) = The framework development workspace

The `framework-tools/` directory contains the tools and infrastructure needed to build, validate, and maintain the framework, while `pocketflow_tools/` contains the actual framework code that gets installed in end-user projects.