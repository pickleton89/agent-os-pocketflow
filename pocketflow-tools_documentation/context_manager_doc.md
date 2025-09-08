How does the context_manager.py file work?


The pocketflow-tools/context_manager.py file is a design-time content extractor that
  analyzes project documentation to inform PocketFlow template generation. Here's how it
  works:

  Core Purpose

  Extracts project context from repository docs (requirements, design, architecture) to
  create structured input for PocketFlow generation - NOT a runtime coordinator.

  Key Components

  1. Document Processing Pipeline

  - Input: Scans docs/ directory for .md files
  - Classification: Identifies document types (requirements, design, architecture, etc.)
  - Extraction: Uses regex patterns to extract structured information
  - Output: Creates ProjectContext with requirements, tech stack, and patterns

  2. Document Types Supported (lines 29-37)

  REQUIREMENTS, ROADMAP, DESIGN, ARCHITECTURE,
  USER_STORIES, TECHNICAL_SPEC, API_SPEC

  3. Intelligent Pattern Recognition

  Requirement Extraction (lines 74-92):
  - Functional: "user shall", "system provides", "users can"
  - Technical: "using", "built on", "database", "integration with"
  - Constraints: "cannot", "limited to", "bounded by"

  PocketFlow Pattern Detection (lines 95-116):
  - RAG: "search", "retrieval", "document", "semantic", "vector"
  - AGENT: "intelligent", "autonomous", "reasoning", "conversation"
  - WORKFLOW: "process", "pipeline", "automation", "orchestration"
  - TOOL: "utility", "function", "command", "execute"
  - MULTI_AGENT: "collaboration", "distributed", "coordination"

  4. Technical Stack Detection (lines 285-342)

  Identifies technologies from:
  - Explicit mentions: "using FastAPI", "built on PostgreSQL"
  - Common keywords: python, react, docker, chromadb, openai
  - Canonicalizes names: "fastapi" → "FastAPI", "postgresql" → "PostgreSQL"

  Core Workflow

  Main Process (extract_project_context, lines 118-163):

  1. Scan docs/ directory for .md files
  2. For each document:
     - Classify document type (requirements vs design vs architecture)
     - Extract relevant information based on type
     - Store in ProjectContext structure
  3. Analyze patterns and assess complexity
  4. Return structured ProjectContext

  Key Extraction Methods:

  - _extract_requirements(): Uses regex patterns to find functional/technical requirements
  - _extract_design_info(): Identifies technical stack and architecture decisions
  - _analyze_patterns(): Detects PocketFlow patterns from requirement text
  - _assess_complexity(): Scores complexity based on requirements count, tech diversity,
  integrations

  Output Formats

  1. ProjectContext (lines 52-63)

  Structured representation with:
  - Requirements list with priority/type/confidence
  - Technical stack array
  - Detected patterns
  - Complexity indicators
  - Integration needs

  2. Workflow Specification (create_workflow_specification, lines 410-444)

  YAML/JSON output ready for PocketFlow generator:
  name: MyWorkflow
  pattern: RAG
  description: System that processes documents
  technical_stack: [FastAPI, PostgreSQL, ChromaDB]
  patterns_detected: [RAG, WORKFLOW]
  complexity_level: medium

  Context in Framework

  Design-Time vs Runtime:
  - ContextManager: Analyzes project docs to create generation inputs (this file)
  - CoordinationContext: Manages runtime state during agent handoffs (agent_coordination.py)

  Integration Points:
  - Used by PocketFlow generators to understand project requirements
  - Creates input specifications for template customization
  - Bridges planning documents → implementation generation

  CLI Interface

  python context_manager.py --project-root . --workflow-name MyApp --output analysis.json
  --spec workflow.yaml

  Real-World Usage

  In end-user projects, this tool:
  1. Reads docs/requirements.md, docs/architecture.md
  2. Extracts "RAG system for document search with ChromaDB"
  3. Detects RAG pattern + FastAPI stack
  4. Creates specification for PocketFlow RAG template generation
  5. Feeds into generator to create customized application

  The system transforms unstructured documentation into structured generation inputs for
  intelligent PocketFlow template creation.

---

How does it actually work in the context of this project?

  Based on my analysis, here's how context_manager.py actually works in the context of this 
  framework repository:

  Real Context: Framework Repository Usage

  ⚠️ Key Insight: In this framework repository, context_manager.py serves as a testing and 
  validation component rather than active production code.

  Current Actual Usage in This Framework

  1. Primary Usage: Testing Infrastructure

  The context_manager.py is primarily used in test_phase2_orchestration.py:

  Test Results From Live Run:
  🔍 Testing Context Extraction...
    ✅ Context extraction: PASSED
    📊 Details: {
      'requirements_found': 23,
      'technical_stack': ['FastAPI', 'ChromaDB', 'AWS S3', 'OpenAI', 'PostgreSQL', 'Redis'],
      'patterns_detected': ['RAG'],
      'source_documents': 3,
      'primary_pattern': 'RAG'
    }

  2. Framework Testing Context

  The test system:
  - Creates temporary test projects with mock documentation
  - Tests context extraction capabilities from sample design docs
  - Validates pattern detection (successfully detected RAG pattern)
  - Generates workflow specifications for testing

  3. Template Generation Integration Status

  Current State: The context manager is NOT actively integrated with the main template
  generation system (pocketflow_tools/).

  Evidence:
  - No imports of context_manager in pocketflow_tools/generators/
  - Template generation works independently using hardcoded patterns
  - Context manager exists as standalone capability

  4. Framework Architecture Role

  As Framework Component:
  - Location: pocketflow-tools/context_manager.py (tools directory)
  - Purpose: Provides context extraction capability for end-user projects
  - Installation: Gets copied to end-user projects during project installation
  - Usage: Intended for use by end-user projects to analyze their own docs

  Not Used For:
  - Generating templates in this framework repo
  - Analyzing this framework repo's own documentation
  - Active participation in template generation pipeline

  5. Intended vs Actual Usage

  Intended Design (for end-user projects):
  # In an end-user project
  context_manager = ContextManager(".")  # Analyze project docs
  context = context_manager.extract_project_context("MyApp")
  # Feed context into PocketFlow generators

  Actual Usage (in framework repo):
  # In framework testing
  context_manager = ContextManager(test_project_dir)  # Test on mock docs  
  context = context_manager.extract_project_context("TestApp")
  # Validate extraction capabilities

  Key Insights

  1. Dormant in Framework Repository

  Like agent_coordination.py, the context manager is largely dormant in this framework repo
  because:
  - This repo creates the framework, not applications using it
  - No need to analyze this repo's docs for template generation
  - Template generation uses predefined patterns, not doc analysis

  2. Active in End-User Projects

  The context manager becomes active when installed in end-user projects:
  - Analyzes project's docs/ directory
  - Extracts requirements from user documentation
  - Feeds structured context to PocketFlow generators
  - Enables intelligent template customization

  3. Framework vs Usage Pattern

  This follows the same pattern as other components:
  - Framework Repository: Contains testing and validation
  - End-User Projects: Where the tool actually performs its intended function

  The context manager is a framework capability that gets deployed to end-user projects where
   it analyzes their documentation to inform intelligent PocketFlow template generation.

---

How does the context_manager.py get called or activated for use?

⏺ Based on my analysis of the codebase, here's how context_manager.py gets
  called or activated:

  Activation Methods

  1. Direct CLI Usage (Primary Method)
  # Basic usage
  python3 pocketflow-tools/context_manager.py --project-root . --workflow-name
  "MyApp"

  # With full options
  python3 pocketflow-tools/context_manager.py \
    --project-root /path/to/project \
    --workflow-name "MyWorkflow" \
    --output context_analysis.json \
    --spec workflow_spec.yaml \
    --verbose

  2. Programmatic Import Usage
  from context_manager import ContextManager

  # Create and use context manager
  manager = ContextManager(".")  # Current directory
  context = manager.extract_project_context("MyApp")

  3. Testing Infrastructure
  - Used in test_phase2_orchestration.py:185 and
  test_phase2_orchestration.py:367
  - Creates test projects and validates context extraction capabilities

  Key Insights

  Framework vs Usage Context:
  - Framework Repository (this repo): Used primarily for testing and validation
  - End-User Projects: Where it performs its intended function of analyzing
  project docs

  Current Status:
  - ✅ CLI interface implemented (context_manager.py:515-563)
  - ✅ Python API available for programmatic use
  - ✅ Active in testing infrastructure
  - ❌ Not integrated with main template generation pipeline
  - ❌ No orchestrator agent automation

  The context manager exists as a standalone tool ready for integration but
  requires manual activation or programmatic calling - it's not automatically
  invoked by other framework components yet.