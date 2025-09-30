Analyzing TODOs...
Found 627 TODOs
Generating report...
# TODO Analysis Report

Generated: /Users/jeffkiefer/Documents/projects/agent-os-pocketflow

## Summary

**Total TODOs**: 627

### By Category

- **BUG_FIX**: 11 (1.8%)
- **DOCUMENTATION**: 9 (1.4%)
- **ENHANCEMENT**: 30 (4.8%)
- **INTEGRATION**: 17 (2.7%)
- **TEMPLATE_PLACEHOLDER**: 49 (7.8%)
- **TESTING**: 5 (0.8%)
- **UNCATEGORIZED**: 506 (80.7%)

## Recommended Actions

### Template Placeholders
**49 TODOs** - These are intentional features. Keep as educational markers.

### Integration TODOs
**17 TODOs** - Convert to GitHub issues with `integration` label.

### Enhancement TODOs
**30 TODOs** - Convert to GitHub issues with `enhancement` label.

### Bug Fix TODOs
**11 TODOs** - Convert to GitHub issues with `bug` label. **Prioritize these!**

### Documentation TODOs
**9 TODOs** - Convert to GitHub issues with `documentation` label.

### Testing TODOs
**5 TODOs** - Convert to GitHub issues with `testing` label.

## Detailed Listings

### BUG_FIX (11 items)

#### CODEBASE_IMPROVEMENT_RECOMMENDATIONS.md

- Line 429: `"TODO: Fix",`
- Line 430: `"TODO: Debug",`
- Line 431: `"FIXME",`

#### CONTRIBUTING.md

- Line 361: `- Examples: "TODO: Fix error handling", "FIXME: Debug this logic"`

#### scripts/analyze-todos.py

- Line 67: `r"TODO: Fix",`
- Line 68: `r"TODO: Debug",`
- Line 69: `r"FIXME",`
- Line 70: `r"TODO: Handle error",`
- Line 71: `r"TODO: Add error handling",`
- Line 104: `Match TODO, FIXME, XXX patterns`
- Line 105: `if re.search(r'\b(TODO|FIXME|XXX)\b', line, re.IGNORECASE):`

### DOCUMENTATION (9 items)

#### CONTRIBUTING.md

- Line 366: `- Examples: "TODO: Document API contract", "TODO: Add docstring"`

#### claude-code/agents/pre-flight-checklist-creator.md

- Line 91: `- TODO: Document all external APIs and service dependencies`
- Line 150: `- TODO: Document utility function contracts and usage patterns`
- Line 213: `- TODO: Document complete development environment setup steps`

#### instructions/extensions/llm-workflow-extension.md

- Line 238: `"metadata": {"source": "TODO: Document source"}`

#### scripts/analyze-todos.py

- Line 74: `r"TODO: Document",`
- Line 75: `r"TODO: Add docstring",`
- Line 76: `r"TODO: Update docs",`
- Line 77: `r"TODO: Write docs",`

### ENHANCEMENT (30 items)

#### .agent-os/workflows/cli-smoke/customeragent/nodes.py

- Line 28: `TODO: Consider input validation if needed (but keep it lightweight)`
- Line 123: `TODO: Consider input validation if needed (but keep it lightweight)`
- Line 218: `TODO: Consider input validation if needed (but keep it lightweight)`
- Line 313: `TODO: Consider input validation if needed (but keep it lightweight)`
- Line 408: `TODO: Consider input validation if needed (but keep it lightweight)`

#### CODEBASE_IMPROVEMENT_RECOMMENDATIONS.md

- Line 424: `"TODO: Consider",`
- Line 425: `"TODO: Future",`
- Line 426: `"TODO: Optional",`

#### CONTRIBUTING.md

- Line 356: `- Examples: "TODO: Consider optimization", "TODO: Future feature idea"`

#### claude-code/agents/api-spec-creator.md

- Line 546: `<!-- TODO: Enhanced coordination with ToolCoordinator for optimized API specification orchestration -->`

#### claude-code/agents/claude-md-manager.md

- Line 222: `<!-- TODO: Future ToolCoordinator Integration -->`

#### claude-code/agents/database-schema-creator.md

- Line 344: `<!-- TODO: Enhanced coordination with ToolCoordinator for optimized database schema orchestration -->`

#### claude-code/agents/document-creation-error-handler.md

- Line 364: `<!-- TODO: Future ToolCoordinator Integration -->`

#### claude-code/agents/document-orchestration-coordinator.md

- Line 1153: `<!-- TODO: Future ToolCoordinator Integration -->`

#### claude-code/agents/mission-document-creator.md

- Line 245: `<!-- TODO: Future ToolCoordinator Integration -->`

#### claude-code/agents/pre-flight-checklist-creator.md

- Line 372: `<!-- TODO: Future ToolCoordinator Integration -->`

#### claude-code/agents/roadmap-document-creator.md

- Line 315: `<!-- TODO: Future ToolCoordinator Integration -->`

#### claude-code/agents/spec-document-creator.md

- Line 202: `<!-- TODO: Enhanced coordination with ToolCoordinator for optimized agent orchestration -->`

#### claude-code/agents/task-breakdown-creator.md

- Line 342: `<!-- TODO: Enhanced coordination with ToolCoordinator for optimized task breakdown orchestration -->`

#### claude-code/agents/technical-spec-creator.md

- Line 295: `<!-- TODO: Enhanced coordination with ToolCoordinator for optimized technical specification orchestration -->`

#### claude-code/agents/test-spec-creator.md

- Line 476: `<!-- TODO: Enhanced coordination with ToolCoordinator for optimized test specification orchestration -->`

#### pocketflow_tools/generators/code_generators.py

- Line 599: `" TODO: Consider input validation if needed (but keep it lightweight)",`

#### scripts/analyze-todos.py

- Line 57: `r"TODO: Consider",`
- Line 58: `r"TODO: Future",`
- Line 59: `r"TODO: Optional",`
- Line 60: `r"TODO: Potential",`
- Line 61: `r"TODO: Could",`
- Line 62: `r"TODO: Maybe",`
- Line 63: `r"TODO: Improve",`
- Line 64: `r"TODO: Enhance",`

### INTEGRATION (17 items)

#### CODEBASE_IMPROVEMENT_RECOMMENDATIONS.md

- Line 419: `"TODO: Integrate with",`
- Line 420: `"TODO: Connect to",`
- Line 421: `"TODO: Wire up",`

#### CONTRIBUTING.md

- Line 351: `- Examples: "TODO: Integrate with ToolCoordinator", "TODO: Connect to external API"`

#### claude-code/agents/dependency-orchestrator.md

- Line 154: `TODO: Integrate with ToolCoordinator for unified dependency management`

#### claude-code/agents/design-document-creator.md

- Line 250: `TODO: Integrate with ToolCoordinator for comprehensive workflow generation`

#### claude-code/agents/strategic-planner.md

- Line 332: `TODO: Integrate with ToolCoordinator for strategic pattern analysis`

#### claude-code/agents/template-validator.md

- Line 196: `TODO: Integrate with ToolCoordinator for comprehensive template validation`

#### instructions/extensions/design-first-enforcement.md

- Line 113: `TODO: Integrate with your CI/CD pipeline`

#### instructions/extensions/llm-workflow-extension.md

- Line 134: `TODO: Integrate with your project's template generation`

#### instructions/extensions/pocketflow-integration.md

- Line 169: `TODO: Integrate with your project setup`
- Line 347: `TODO: Integrate with your project development workflow`

#### scripts/analyze-todos.py

- Line 50: `r"TODO: Integrate with",`
- Line 51: `r"TODO: Connect to",`
- Line 52: `r"TODO: Wire up",`
- Line 53: `r"TODO: Hook up",`
- Line 54: `r"TODO: Add integration",`

### TEMPLATE_PLACEHOLDER (49 items)

#### .agent-os/workflows/cli-smoke/customeragent/flow.py

- Line 14: `TODO: Customize node instances and their configurations`
- Line 34: `TODO: Customize workflow connections and error handling`

#### .agent-os/workflows/cli-smoke/customeragent/router.py

- Line 52: `TODO: Customize error handling and response codes`

#### .code/agents/8596ddee-ffa2-4bbe-80b8-575b4dcf5720/result.txt

- Line 639: `TODO: Customize detection logic for your project requirements`

#### CHANGELOG.md

- Line 131: `- Clear TODO customization guidance ("TODO: Customize this prep logic based on your needs")`

#### CODEBASE_IMPROVEMENT_RECOMMENDATIONS.md

- Line 415: `"TODO: Implement business logic",`
- Line 416: `"TODO: Add your",`

#### CONTRIBUTING.md

- Line 346: `- Examples: "TODO: Implement business logic", "TODO: Customize this prep logic"`

#### claude-code/agents/document-creation-error-handler.md

- Line 243: `TODO: Define your target users`

#### claude-code/agents/mission-document-creator.md

- Line 103: `%% TODO: Customize based on your specific architecture`

#### docs/DESIGN_FIRST_IMPLEMENTATION_PLAN.md

- Line 132: `%% TODO: Replace with actual system flow based on your features`
- Line 219: `%% TODO: Customize based on your specific architecture`

#### instructions/extensions/design-first-enforcement.md

- Line 27: `%% TODO: Replace with actual workflow design`
- Line 57: `TODO: Customize validation logic for your project requirements`
- Line 128: `TODO: Customize validation trigger logic`

#### instructions/extensions/llm-workflow-extension.md

- Line 25: `TODO: Customize pattern detection logic for your specific use cases`
- Line 40: `"""TODO: Customize pattern detection algorithms for your project needs"""`
- Line 43: `TODO: Add your custom pattern indicators`
- Line 99: `"""TODO: Customize implementation guidance for each pattern"""`
- Line 182: `TODO: Add your decision-making algorithm`
- Line 265: `TODO: Customize orchestrator integration for your LLM workflows`

#### instructions/extensions/pocketflow-integration.md

- Line 15: `TODO: Customize detection logic for your project requirements`
- Line 27: `"""TODO: Customize project analysis structure"""`
- Line 35: `"""TODO: Customize auto-detection algorithms for your project"""`
- Line 159: `TODO: Customize structure based on patterns`
- Line 191: `TODO: Customize orchestrator integration for your project workflow`
- Line 201: `"""TODO: Customize orchestrator integration for your project needs"""`
- Line 308: `"""TODO: Define your project's directory structure preferences"""`
- Line 356: `TODO: Customize workflow for your development process`
- Line 439: `TODO: Customize configuration for your project`

#### instructions/orchestration/orchestrator-hooks.md

- Line 24: `TODO: Customize this validation logic for your specific requirements`
- Line 77: `TODO: Customize this validation logic for your PocketFlow workflows`

#### pocketflow_tools/generators/code_generators.py

- Line 345: `"     TODO: Customize error handling and response codes",`
- Line 710: `"         TODO: Customize node instances and their configurations",`
- Line 731: `"         TODO: Customize workflow connections and error handling",`

#### scripts/analyze-todos.py

- Line 43: `r"TODO: Implement business logic",`
- Line 44: `r"TODO: Add your",`
- Line 45: `r"TODO: Customize",`
- Line 46: `r"TODO: Replace with actual",`
- Line 47: `r"TODO: Define your",`

#### templates/claude-md/framework-tools.md

- Line 14: `- All generators create starter templates with TODO placeholders for customization`
- Line 30: `- Generated code includes intentional TODO placeholders`
- Line 46: `- Don't remove TODO placeholders from generated templates`

#### templates/pocketflow-templates.md

- Line 55: `%% TODO: Replace with actual system flow based on your features`
- Line 67: `TODO: Define based on feature requirements from roadmap`

#### templates/validation/test_pocketflow_integration.sh

- Line 48: `Check if template has TODO stubs (expected for generated templates)`
- Line 49: `if grep -q "TODO\|FIXME\|NotImplementedError\|pass   Implementation needed" "$template" 2>/dev/null; then`
- Line 50: `echo "✅ Template contains TODO stubs for customization (expected)"`
- Line 164: `echo "  1. Review templates in .agent-os/framework-tools/ for TODO stubs"`

### TESTING (5 items)

#### CONTRIBUTING.md

- Line 371: `- Examples: "TODO: Add test coverage", "TODO: Write integration test"`

#### scripts/analyze-todos.py

- Line 80: `r"TODO: Test",`
- Line 81: `r"TODO: Add test",`
- Line 82: `r"TODO: Write test",`
- Line 83: `r"TODO: Cover",`

### UNCATEGORIZED (506 items)

#### .agent-os/workflows/cli-smoke/customeragent/README.md

- Line 143: `Generated on: TODO-SET-DATE`

#### .agent-os/workflows/cli-smoke/customeragent/flow.py

- Line 16: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`
- Line 36: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`

#### .agent-os/workflows/cli-smoke/customeragent/nodes.py

- Line 27: `TODO: Extract the exact data exec() needs from shared store`
- Line 56: `TODO: Implement the core processing logic using only prep_result`
- Line 57: `TODO: Return the processed result (avoid side effects here)`
- Line 86: `TODO: Store exec_result in shared store with appropriate key`
- Line 87: `TODO: Return flow signal for branching ('success', 'error', specific state)`
- Line 122: `TODO: Extract the exact data exec() needs from shared store`
- Line 151: `TODO: Implement the core processing logic using only prep_result`
- Line 152: `TODO: Return the processed result (avoid side effects here)`
- Line 181: `TODO: Store exec_result in shared store with appropriate key`
- Line 182: `TODO: Return flow signal for branching ('success', 'error', specific state)`
- Line 217: `TODO: Extract the exact data exec() needs from shared store`
- Line 246: `TODO: Implement the core processing logic using only prep_result`
- Line 247: `TODO: Return the processed result (avoid side effects here)`
- Line 276: `TODO: Store exec_result in shared store with appropriate key`
- Line 277: `TODO: Return flow signal for branching ('success', 'error', specific state)`
- Line 312: `TODO: Extract the exact data exec() needs from shared store`
- Line 341: `TODO: Implement the core processing logic using only prep_result`
- Line 342: `TODO: Return the processed result (avoid side effects here)`
- Line 371: `TODO: Store exec_result in shared store with appropriate key`
- Line 372: `TODO: Return flow signal for branching ('success', 'error', specific state)`
- Line 407: `TODO: Extract the exact data exec() needs from shared store`
- Line 436: `TODO: Implement the core processing logic using only prep_result`
- Line 437: `TODO: Return the processed result (avoid side effects here)`
- Line 466: `TODO: Store exec_result in shared store with appropriate key`
- Line 467: `TODO: Return flow signal for branching ('success', 'error', specific state)`

#### .agent-os/workflows/cli-smoke/customeragent/router.py

- Line 16: `TODO: Add authentication and authorization logic here`
- Line 18: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`
- Line 29: `TODO: Add input validation and sanitization`
- Line 31: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`
- Line 54: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`

#### .agent-os/workflows/cli-smoke/customeragent/utils/classify_intent.py

- Line 40: `TODO: Implement classify_intent`
- Line 42: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`

#### .agent-os/workflows/cli-smoke/customeragent/utils/execute_action.py

- Line 40: `TODO: Implement execute_action`
- Line 42: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`

#### .agent-os/workflows/cli-smoke/customeragent/utils/generate_response.py

- Line 44: `TODO: Implement generate_response`
- Line 46: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`

#### .agent-os/workflows/cli-smoke/customeragent/utils/get_customer_history.py

- Line 40: `TODO: Implement get_customer_history`
- Line 42: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`

#### .code/agents/8596ddee-ffa2-4bbe-80b8-575b4dcf5720/result.txt

- Line 653: `"""TODO: Scan existing project structure"""`
- Line 663: `"""TODO: Invoke orchestrator for design document creation"""`
- Line 675: `- **Clear Implementation Guidance**: Step-by-step TODO instructions throughout the process`
- Line 680: `- **Clear Customization Points**: All TODO placeholders include specific implementation guidance`

#### AGENTS.md

- Line 45: `- Don’t “fix” TODO placeholders in generated templates; they are intentional teaching stubs.`

#### CHANGELOG.md

- Line 113: `- Replace agent TODO placeholders with working invocations`
- Line 123: `- Proper Node/Flow patterns with educational TODO placeholders`
- Line 138: `- 14+ TODO placeholders ensuring templates remain educational, not working implementations`
- Line 207: `- Intentional TODO placeholders explained as educational features`
- Line 596: `- Educational placeholder quality assessment (TODO comment evaluation, NotImplementedError usage)`
- Line 653: `- Template placeholders and TODO stubs preserved as intentional educational design features`
- Line 705: `- **Framework Validation Infrastructure Validated**: Confirmed `.agent-os/workflows/testcontentanalyzer/` as appropriate framework validation infrastructure containing generated template examples with TODO placeholders`
- Line 721: `- **Template Generation Documentation**: All examples properly demonstrate template generation patterns with YAML specifications creating placeholder code with TODO stubs`
- Line 752: `- **Proper Placeholder Usage**: Confirmed all generated code contains appropriate TODO comments with NotImplementedError for utilities and meaningful placeholder logic`
- Line 789: `- **Template Quality Assessment**: Verified all generated code contains proper TODO comments, NotImplementedError placeholders, and guided implementation instructions`
- Line 835: `- **Main README Clarity**: Enhanced testcontentanalyzer description to emphasize it's a generated template with TODO placeholders`
- Line 839: `- **Template Generation Validated**: Confirmed generator creates proper starting point templates with TODO placeholders for end-user implementation`
- Line 841: `- **Framework Principle Reinforced**: Template placeholders and TODO stubs confirmed as intentional design features, not bugs`
- Line 849: `- **Generated Code Review**: Analyzed `.agent-os/workflows/testcontentanalyzer/` and confirmed it contains proper template output with TODO placeholders`
- Line 941: `- Comprehensive "What NOT to do" section with specific examples (don't fix TODO placeholders, don't install PocketFlow here, don't invoke orchestrator)`
- Line 978: `- **Impact**: Generator now produces intelligent, working starter templates instead of TODO-heavy stubs, with proper type safety and dependency management`
- Line 988: `- Documented explicit DO NOT guidelines for framework development (don't invoke orchestrator, don't fix TODO templates, don't install PocketFlow)`
- Line 990: `- Explained that TODO placeholders in generator.py are intentional templates, not bugs`
- Line 993: `- **Context**: This resolves issues where agents tried to "fix" the generator's TODO stubs, install PocketFlow dependencies, or expect application tests in a meta-framework`

#### CLAUDE.md

- Line 12: `| Template placeholders and TODO stubs are intentional features | Where placeholder code gets implemented |`
- Line 26: `- TODO stubs in generated files are starting points, not bugs to fix`
- Line 33: `- Try to "fix" TODO placeholders in generated templates (they're intentional)`
- Line 42: `- Understand that `generator.py` creates STARTER templates with TODO stubs for customization`
- Line 72: `- **TODO Comments**: Indicate incomplete framework features - should be implemented`
- Line 82: `- **Quality Standard**: Placeholder functions, educational comments, TODO stubs expected`
- Line 84: `- **TODO Comments**: Guide developers on what to customize - are intentional features`
- Line 88: `- `nodes.py`, `flow.py` in end-user projects - Generated files with ` TODO` placeholders`
- Line 96: `- **TODO Comments**: May indicate areas for expanding demo coverage`
- Line 114: `├─ TODO in framework code → INCOMPLETE - should implement`
- Line 115: `├─ TODO in template → FEATURE - guides customization`
- Line 133: `**Scenario 3**: Found TODO in `framework-tools/validate-setup.sh``
- Line 210: `**Generated templates include intentional TODO placeholders**:`

#### CODEBASE_IMPROVEMENT_RECOMMENDATIONS.md

- Line 233: `- Placeholder functions, educational comments, TODO stubs`
- Line 400: `3.3 Optimize TODO Management`
- Line 439: `**Actionable TODO Workflow**:`
- Line 625: `Framework generates application templates with TODO placeholders and`

#### CONTRIBUTING.md

- Line 27: `- Template placeholders and TODO stubs are intentional design features`
- Line 329: `TODO Management Workflow`
- Line 331: `Understanding TODO Categories`
- Line 333: `The framework contains many TODO comments that serve different purposes. Use the TODO analysis script to categorize and manage them effectively:`
- Line 336: `Generate comprehensive TODO analysis report`
- Line 340: `TODO Categories`
- Line 377: `TODO Workflow Best Practices`
- Line 384: `2. **Periodic TODO Review** (Quarterly):`
- Line 391: `Update template TODO quality if needed`
- Line 395: `- Extract context and requirements from TODO comment`
- Line 399: `- Remove TODO once issue is created (or add issue reference)`
- Line 401: `4. **Template TODO Quality Standards**:`
- Line 402: `- Be specific: "TODO: Implement user authentication via OAuth2" vs "TODO: implement"`
- Line 403: `- Provide context: "TODO: Add rate limiting (5 req/sec per IP)" vs "TODO: add rate limiting"`
- Line 404: `- Include guidance: "TODO: Fetch from vector DB, rank by relevance" vs "TODO: fetch data"`
- Line 406: `Current TODO Status`

#### METRICS.md

- Line 65: `- Template generators with intentional TODO placeholders`

#### README.md

- Line 52: `- Provides educational TODO placeholders for business logic`
- Line 294: `├── nodes.py                 PocketFlow nodes (with TODO placeholders)`
- Line 307: `**Note:** TODO placeholders in generated code are intentional - they mark where you implement your specific business logic.`
- Line 361: `- Implement business logic in generated TODO placeholders`

#### WARP.md

- Line 12: `- Template placeholders and TODO stubs are intentional design features`
- Line 210: `- nodes.py (PocketFlow nodes with TODO placeholders)`
- Line 305: `**"TODO placeholders should be implemented"**`
- Line 332: `- ✅ Template placeholders and TODO stubs are intentional features`
- Line 334: `- ❌ Don't try to "fix" TODO placeholders (they're educational templates)`

#### claude-code/agents/api-spec-creator.md

- Line 547: `<!-- TODO: Dynamic endpoint complexity assessment based on existing API analysis -->`
- Line 548: `<!-- TODO: Automated API versioning and backward compatibility validation -->`

#### claude-code/agents/claude-md-manager.md

- Line 208: `4. **Standards Directory Missing**: Use fallback references with todo markers for future setup`

#### claude-code/agents/database-schema-creator.md

- Line 345: `<!-- TODO: Dynamic migration complexity assessment based on existing schema analysis -->`
- Line 346: `<!-- TODO: Automated constraint conflict detection and resolution guidance -->`

#### claude-code/agents/dependency-orchestrator.md

- Line 162: `TODO: Initialize tool coordinator`
- Line 165: `TODO: Generate comprehensive dependency configuration`
- Line 168: `TODO: Get pattern analysis for additional context`
- Line 171: `TODO: Combine results for complete dependency setup`
- Line 184: `TODO: Implement dependency orchestration using the framework-tools module`
- Line 191: `TODO: Initialize dependency orchestrator`
- Line 194: `TODO: Generate pattern-specific configuration`
- Line 197: `TODO: Create pyproject.toml content`
- Line 200: `TODO: Generate tool configurations (ruff, pytest, etc.)`
- Line 203: `TODO: Create UV environment configuration`
- Line 206: `TODO: Return complete configuration package`
- Line 216: `TODO: Pattern-specific dependency generation examples`
- Line 254: `TODO: CLI interface for direct dependency generation`

#### claude-code/agents/design-document-creator.md

- Line 258: `TODO: Initialize tool coordinator`
- Line 261: `TODO: Generate workflow graph for design document`
- Line 264: `TODO: Get pattern-specific design recommendations`
- Line 267: `TODO: Combine results for comprehensive design document`
- Line 283: `TODO: Integrate workflow graph generation based on selected pattern`
- Line 290: `TODO: Initialize workflow graph generator`
- Line 293: `TODO: Generate workflow graph based on detected pattern`
- Line 300: `TODO: Convert to Mermaid diagram for design document`
- Line 303: `TODO: Return formatted diagram for inclusion in design.md`
- Line 308: `TODO: Pattern-specific workflow generation examples`

#### claude-code/agents/document-creation-error-handler.md

- Line 135: `- Provide template skeleton with TODO placeholders`
- Line 171: `- Provide document templates with TODO placeholders`
- Line 239: `TODO: Describe your product in 1-2 sentences`
- Line 248: `TODO: List 2-4 key problems your product solves`
- Line 253: `TODO: List 8-10 key features organized by category`
- Line 264: `**Patterns**: TODO: Select appropriate patterns (WORKFLOW, TOOL, AGENT, RAG, MAPREDUCE)`
- Line 265: `**Complexity**: TODO: Choose complexity level (SIMPLE_WORKFLOW/ENHANCED_WORKFLOW/COMPLEX_APPLICATION/LLM_APPLICATION)`
- Line 267: `TODO: Complete architecture section based on your specific requirements`

#### claude-code/agents/document-orchestration-coordinator.md

- Line 367: `3. Use simplified template with TODO placeholders`
- Line 373: `- Clear TODO items for user completion`
- Line 875: `'[ ] Complete any TODO items in generated templates',`
- Line 888: `'completion_steps': result.get('completion_guidance', 'Follow template TODO items'),`
- Line 896: `'completion_steps': 'Review and complete TODO placeholders',`
- Line 1093: `- [ ] Complete TODO items in template files`

#### claude-code/agents/mission-document-creator.md

- Line 155: `- Include customization markers (TODO comments)`

#### claude-code/agents/pattern-analyzer.md

- Line 136: `TODO: Implement ToolCoordinator integration for agent handoffs`
- Line 145: `TODO: Initialize tool coordinator`
- Line 148: `TODO: Analyze patterns and get handoff recommendations`
- Line 151: `TODO: Process handoff based on target agent`
- Line 155: `TODO: Return coordination results for next phase`
- Line 166: `TODO: Agent-specific handoff implementations`

#### claude-code/agents/pocketflow-orchestrator.md

- Line 100: `- Poor TODO quality in generated templates`

#### claude-code/agents/pre-flight-checklist-creator.md

- Line 13: `2. **Best Practices Validation**: Generate actionable TODO items based on PocketFlow framework best practices`
- Line 32: `- TODO items are clear, measurable, and actionable`
- Line 56: `- TODO: Verify user personas are specific and actionable`
- Line 57: `- TODO: Confirm problem statements include quantifiable impact metrics`
- Line 58: `- TODO: Validate competitive differentiators with evidence`
- Line 61: `- TODO: Confirm PocketFlow is specified as workflow framework`
- Line 62: `- TODO: Verify Python 3.12+ with FastAPI, Pydantic, uv, and Ruff`
- Line 63: `- TODO: Validate database and hosting selections are appropriate`
- Line 66: `- TODO: Confirm all features are tagged with PocketFlow patterns`
- Line 67: `- TODO: Verify effort estimates use standard scale (XS/S/M/L/XL)`
- Line 68: `- TODO: Validate phase dependencies and logical progression`
- Line 72: `- TODO: Review feature descriptions for user-benefit focus`
- Line 73: `- TODO: Ensure features map to appropriate PocketFlow patterns`
- Line 74: `- TODO: Validate feature scope and complexity assessments`
- Line 80: `- TODO: Confirm system purpose and complexity assessment`
- Line 81: `- TODO: Verify PocketFlow pattern selection and justification`
- Line 82: `- TODO: Validate high-level data flow diagram completion`
- Line 85: `- TODO: Map each feature to optimal pattern (WORKFLOW/TOOL/AGENT/RAG/MAPREDUCE)`
- Line 86: `- TODO: Justify pattern selections based on complexity and requirements`
- Line 87: `- TODO: Verify pattern combinations are compatible and efficient`
- Line 92: `- TODO: Define integration patterns and error handling strategies`
- Line 93: `- TODO: Plan authentication and security requirements`
- Line 99: `- TODO: Define core data types and structures needed`
- Line 100: `- TODO: Plan data transformation requirements between nodes`
- Line 101: `- TODO: Identify shared state management needs`
- Line 104: `- TODO: List all input/output data structures needed`
- Line 105: `- TODO: Define validation rules and error handling patterns`
- Line 106: `- TODO: Plan schema evolution and versioning strategy`
- Line 110: `- TODO: Map user inputs to system data structures`
- Line 111: `- TODO: Define processing pipelines and transformation steps`
- Line 112: `- TODO: Plan output formats and delivery mechanisms`
- Line 118: `- TODO: Map business logic functions to Node/AsyncNode/BatchNode types`
- Line 119: `- TODO: Plan node composition and reusability patterns`
- Line 120: `- TODO: Define node input/output contracts and interfaces`
- Line 123: `- TODO: Design primary workflow sequences and decision points`
- Line 124: `- TODO: Plan parallel processing opportunities and dependencies`
- Line 125: `- TODO: Define flow error handling and recovery strategies`
- Line 129: `- TODO: Define single-purpose nodes with clear interfaces`
- Line 130: `- TODO: Plan utility function integration within nodes`
- Line 131: `- TODO: Avoid business logic duplication across nodes`
- Line 137: `- TODO: Identify all external service integrations needed`
- Line 138: `- TODO: Design utility function interfaces and error handling`
- Line 139: `- TODO: Plan authentication, rate limiting, and retry strategies`
- Line 142: `- TODO: List all data processing and transformation needs`
- Line 143: `- TODO: Design reusable utility functions for common operations`
- Line 144: `- TODO: Plan file handling, parsing, and format conversion utilities`
- Line 148: `- TODO: Plan custom utility functions rather than depending on framework examples`
- Line 149: `- TODO: Design utilities for maximum flexibility and reusability`
- Line 156: `- TODO: Map all potential failure points in the system`
- Line 157: `- TODO: Design error recovery strategies for each failure type`
- Line 158: `- TODO: Plan user-friendly error messages and logging strategies`
- Line 161: `- TODO: Plan retry mechanisms for transient failures`
- Line 162: `- TODO: Design circuit breaker patterns for external service calls`
- Line 163: `- TODO: Define graceful degradation strategies for system components`
- Line 167: `- TODO: Define log levels and categories for different components`
- Line 168: `- TODO: Plan structured logging for debugging and monitoring`
- Line 169: `- TODO: Design error tracking and alerting mechanisms`
- Line 175: `- TODO: Plan unit tests for all nodes, utilities, and data models`
- Line 176: `- TODO: Design mock strategies for external service dependencies`
- Line 177: `- TODO: Define test coverage targets and quality gates`
- Line 180: `- TODO: Design flow-level integration tests for complete workflows`
- Line 181: `- TODO: Plan API endpoint testing with realistic scenarios`
- Line 182: `- TODO: Define database integration testing strategies`
- Line 186: `- TODO: Plan workflow execution testing and validation`
- Line 187: `- TODO: Design SharedStore state management testing`
- Line 188: `- TODO: Plan node execution testing with various input scenarios`
- Line 194: `- TODO: Define acceptable response times for all user-facing operations`
- Line 195: `- TODO: Set throughput requirements for batch processing operations`
- Line 196: `- TODO: Plan performance monitoring and measurement strategies`
- Line 199: `- TODO: Identify potential performance bottlenecks and mitigation strategies`
- Line 200: `- TODO: Plan horizontal and vertical scaling approaches`
- Line 201: `- TODO: Design efficient data access and caching strategies`
- Line 205: `- TODO: Plan memory usage optimization for large data processing`
- Line 206: `- TODO: Design efficient database query patterns and indexing`
- Line 207: `- TODO: Plan API rate limiting and resource throttling strategies`
- Line 214: `- TODO: Plan dependency management with uv package manager`
- Line 215: `- TODO: Define development workflow and code quality standards`
- Line 218: `- TODO: Choose and configure hosting platform based on tech-stack.md`
- Line 219: `- TODO: Plan CI/CD pipeline with testing and quality gates`
- Line 220: `- TODO: Define environment configuration and secrets management`
- Line 224: `- TODO: Plan application monitoring, logging, and alerting strategies`
- Line 225: `- TODO: Define backup and recovery procedures for data persistence`
- Line 226: `- TODO: Plan security updates and vulnerability management processes`
- Line 282: `3. **Include Actionable Guidance**: Ensure each TODO item is specific and actionable`
- Line 291: `4. **Actionability Check**: Confirm all TODO items are clear and measurable`
- Line 368: `2. **Actionability Check**: Verify all TODO items have clear validation criteria`

#### claude-code/agents/spec-document-creator.md

- Line 203: `<!-- TODO: Dynamic template selection based on project complexity analysis -->`
- Line 204: `<!-- TODO: Cross-spec consistency validation for multi-feature projects -->`

#### claude-code/agents/strategic-planner.md

- Line 340: `TODO: Initialize tool coordinator`
- Line 343: `TODO: Perform comprehensive pattern analysis for strategic planning`
- Line 346: `TODO: Generate workflow graphs for strategic visualization`
- Line 350: `TODO: Get dependency insights for technology planning`
- Line 353: `TODO: Combine results for strategic decision making`
- Line 371: `TODO: Implement pattern analysis integration using the framework-tools module`
- Line 378: `TODO: Initialize pattern analyzer`
- Line 381: `TODO: Analyze requirements to identify optimal patterns`
- Line 384: `TODO: Generate pattern recommendations`
- Line 387: `TODO: Assess pattern complexity and strategic implications`
- Line 393: `TODO: Generate strategic pattern insights`
- Line 403: `TODO: Return comprehensive pattern analysis for strategic planning`
- Line 414: `TODO: Strategic pattern analysis helper functions`
- Line 452: `TODO: Pattern-specific strategic planning examples`

#### claude-code/agents/task-breakdown-creator.md

- Line 343: `<!-- TODO: Dynamic template customization based on feature complexity and implementation requirements -->`
- Line 344: `<!-- TODO: Automated phase dependency analysis and validation for complex multi-feature specifications -->`

#### claude-code/agents/tech-stack-document-creator.md

- Line 198: `Future Enhancements (TODO)`

#### claude-code/agents/technical-spec-creator.md

- Line 296: `<!-- TODO: Dynamic template selection based on PocketFlow pattern complexity and project architecture -->`
- Line 297: `<!-- TODO: Automated dependency conflict detection and resolution guidance -->`

#### claude-code/agents/template-validator.md

- Line 23: `- Ensures TODO stubs are meaningful and educational`
- Line 29: `- Complete TODO implementations`
- Line 70: `- TODO comments are descriptive and educational`
- Line 110: `- Improve TODO comment quality and educational value`
- Line 181: `2. **Placeholder Quality**: Assess TODO stubs and educational value`
- Line 204: `TODO: Initialize tool coordinator`
- Line 207: `TODO: Perform comprehensive template validation`
- Line 210: `TODO: Get coordination context for handoff processing`
- Line 220: `TODO: Return comprehensive validation and coordination status`
- Line 233: `TODO: Implement template validation using the framework-tools module`
- Line 240: `TODO: Initialize template validator`
- Line 243: `TODO: Discover Python files in template directory`
- Line 246: `TODO: Perform syntax validation`
- Line 252: `TODO: Validate PocketFlow pattern compliance`
- Line 258: `TODO: Check Pydantic model structure`
- Line 264: `TODO: Validate workflow graph connectivity`
- Line 271: `TODO: Assess placeholder quality`
- Line 277: `TODO: Generate comprehensive validation report`
- Line 281: `TODO: Return validation summary`
- Line 294: `TODO: Specific validation function examples`
- Line 314: `"""Example: Assess TODO stub educational value."""`
- Line 332: `TODO: Pattern-specific validation examples`

#### claude-code/agents/test-spec-creator.md

- Line 477: `<!-- TODO: Dynamic test template selection based on PocketFlow pattern complexity and testing requirements -->`
- Line 478: `<!-- TODO: Automated test coverage analysis and gap identification for comprehensive testing validation -->`

#### claude-code/testing/test-phase4-optimization.py

- Line 749: `'[ ] Complete any TODO items in generated templates',`

#### docs/DESIGN_FIRST_IMPLEMENTATION_PLAN.md

- Line 77: `- [ ] Generates docs/design.md with TODO templates`
- Line 144: `TODO: Define based on feature requirements from roadmap`
- Line 157: `- TODO: Define input/output contracts during spec creation`
- Line 159: `- TODO: Implement following PocketFlow utility philosophy`
- Line 177: `- [ ] Includes TODO placeholders for customization`
- Line 234: `- [ ] TODO comments guide customization`
- Line 308: `- [ ] Includes TODO items with guidance`
- Line 317: `TODO: Implement your business logic here`
- Line 319: `FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow`
- Line 417: `- [ ] Generated templates maintain "TODO for customization" approach`
- Line 424: `- **Templates, not implementations**: Continue providing TODO-filled starting points`

#### docs/POCKETFLOW_BEST_PRACTICES.md

- Line 26: `- Template placeholders and TODO stubs are intentional design features`

#### docs/POCKETFLOW_IMPLEMENTATION_PLAN.md

- Line 16: `2. **Generator Philosophy**: TODO stubs and placeholders are correctly implemented as features, not bugs`
- Line 121: `TODO: Read required data from shared store`
- Line 129: `TODO: Implement core logic`
- Line 151: `TODO: Implement simple LLM call`
- Line 374: `Medium (WARN): Complex utilities, poor TODO quality`

#### docs/document-creation-subagent-refactoring-plan.md

- Line 101: `- Include actionable TODO items with guidance`
- Line 277: `- **TODO placeholders** for future ToolCoordinator integration`

#### docs/documentation-fetch-implementation-plan.md

- Line 141: `**Rationale:** This file intentionally contains TODO placeholders as it's a template showing structure for end-user implementations. The framework provides guidance; agents in end-user projects do the actual work.`
- Line 182: `- TODO placeholders in smart_features.py are intentional - they show structure for customization`

#### framework-tools/end_to_end_test_scenarios.py

- Line 442: `Check that generated files have TODO placeholders (framework templates)`
- Line 460: `Look for various TODO patterns`
- Line 461: `if " TODO:" in content or "TODO:" in content or " TODO " in content:`

#### framework-tools/smart_features.py

- Line 261: `"content": f"TODO: Implement actual content extraction for {level} level",`

#### framework-tools/template_validator.py

- Line 565: `Check for TODO comments`
- Line 566: `todo_count = content.count("TODO:")`
- Line 573: `message="No TODO comments found - consider adding educational placeholders"`
- Line 576: `Check for generic/poor TODO messages`
- Line 577: `poor_todos = re.findall(r'TODO: (implement|fix|add|update|change)', content, re.IGNORECASE)`
- Line 584: `message=f"Found {len(poor_todos)} generic TODO comments",`
- Line 585: `suggestion="Make TODO comments more specific and educational"`
- Line 595: `This is a heuristic check - look for complex return statements without TODO markers`
- Line 599: `'TODO' not in line and`
- Line 608: `message="Potential completed implementation without TODO marker",`
- Line 609: `suggestion="Add TODO comment or ensure this is appropriate placeholder code"`

#### framework-tools/testcontentanalyzer/README.md

- Line 5: `This directory contains a **generated PocketFlow template with TODO placeholders** that serves as:`
- Line 7: `1. **Framework Validation**: Demonstrates that the Agent OS + PocketFlow framework generator produces proper template structure with TODO placeholders`
- Line 18: `- **This directory contains** a template example with TODO placeholders that the framework generates for end-user projects`
- Line 24: `- The TODO placeholders demonstrate the framework's design principle: provide starting points, not finished implementations`
- Line 25: `- Missing implementations in TODO sections are **features, not bugs** - they guide end-user development`
- Line 38: `- Validates that TODO placeholders are meaningful and guide implementation`
- Line 43: `- PocketFlow flows and nodes with TODO placeholders for implementation`
- Line 47: `- Documentation templates with TODO sections`
- Line 49: `This example shows the starting point templates the framework provides - you implement the TODO sections to create your working application.`

#### framework-tools/validation_feedback.py

- Line 66: `"template": "TODO placeholder found in {component}: {detail}"`
- Line 189: `elif 'TODO' in line.upper():`
- Line 233: `if category == 'missing_implementation' or 'TODO' in message:`
- Line 238: `issue_description=f"TODO placeholder needs implementation: {message}",`
- Line 283: `"""Get relevant context information for TODO implementation."""`
- Line 339: `"description": "Focus on implementing TODO placeholders",`
- Line 341: `"Review context requirements for each TODO",`

#### framework-tools_documentation/template_validator_doc.md

- Line 57: `- Counts TODO comments (flags files with none)`
- Line 58: `- Identifies generic/poor TODO messages`
- Line 62: `- Detects potentially completed implementations without TODO markers`
- Line 152: `- Validates TODO stubs are educational`

#### framework-tools_documentation/test-generator_doc.md

- Line 98: `- Generates complete project structures with TODO placeholders`
- Line 105: `intentional TODO placeholders and import statements that will only work in`

#### framework-tools_documentation/validation_feedback_doc.md

- Line 27: `- Categorizes issues as TODO placeholders, import errors, or structural`
- Line 32: `- Suggests relevant context needed for TODO implementations`
- Line 76: `- Mock validation output with TODO placeholders, import errors, and warnings`
- Line 91: `dependencies) and manual tasks (like implementing TODO placeholders)`

#### instructions/extensions/design-first-enforcement.md

- Line 15: `<!-- TODO: Define functional and non-functional requirements -->`
- Line 22: `<!-- TODO: Create Mermaid diagram showing data flow -->`
- Line 31: `<!-- TODO: Define SharedStore schema and data models -->`
- Line 32: `- Input Schema: TODO - Define Pydantic models`
- Line 33: `- Output Schema: TODO - Define Pydantic models`
- Line 34: `- Intermediate Data: TODO - Define data structures`
- Line 37: `<!-- TODO: Define PocketFlow nodes with prep/exec/post pattern -->`
- Line 38: `- Preparation Nodes: TODO - Data validation and preprocessing`
- Line 39: `- Execution Nodes: TODO - Core business logic`
- Line 40: `- Post-processing Nodes: TODO - Output formatting and validation`
- Line 43: `<!-- TODO: Define utility functions with input/output contracts -->`
- Line 44: `- Helper Functions: TODO - Reusable utility functions`
- Line 45: `- Integration Points: TODO - External API integrations`
- Line 72: `TODO: Implement section validation`
- Line 80: `TODO: Implement Mermaid diagram validation`
- Line 85: `TODO: Implement pattern identification validation`
- Line 122: `TODO: Enable this hook by making it executable: chmod +x .git/hooks/pre-commit`
- Line 142: `TODO: Add to your project's validation workflow`
- Line 177: `5. **Clear Implementation Guidance**: Step-by-step TODO instructions`

#### instructions/extensions/llm-workflow-extension.md

- Line 69: `TODO: Implement pattern detection based on feature description and requirements`
- Line 86: `TODO: Analyze requirements file if provided`
- Line 89: `TODO: Add requirement-based pattern detection`
- Line 138: `Example usage - TODO: Replace with your feature description`
- Line 157: `"""TODO: Define agent input schema"""`
- Line 163: `"""TODO: Define decision structure"""`
- Line 170: `"""TODO: Define agent output schema"""`
- Line 180: `"""TODO: Implement decision-making logic"""`
- Line 186: `"reasoning": "TODO: Add reasoning logic"`
- Line 191: `"""TODO: Implement action execution logic"""`
- Line 193: `TODO: Execute the decided action`
- Line 195: `result = f"TODO: Execute action: {action}"`
- Line 207: `"""TODO: Define RAG query schema"""`
- Line 213: `"""TODO: Define document structure"""`
- Line 219: `"""TODO: Define RAG response schema"""`
- Line 230: `"""TODO: Implement document retrieval logic"""`
- Line 233: `TODO: Implement vector search or keyword retrieval`
- Line 236: `"content": "TODO: Retrieved document content",`
- Line 244: `"""TODO: Implement context assembly logic"""`
- Line 247: `TODO: Assemble context from retrieved documents`
- Line 248: `context = "TODO: Assembled context from documents"`
- Line 252: `"""TODO: Implement response generation logic"""`
- Line 255: `TODO: Generate response using LLM with context`
- Line 256: `response = "TODO: Generated response based on context"`
- Line 300: `TODO: Add to your project's LLM development workflow`
- Line 309: `3. **Clear Implementation Guidance**: Provide step-by-step TODO instructions for each pattern`
- Line 317: `- Clear TODO guidance for implementing LLM integrations`

#### instructions/extensions/pocketflow-integration.md

- Line 39: `TODO: Add custom detection triggers based on your project needs`
- Line 65: `TODO: Implement comprehensive project analysis`
- Line 99: `"""TODO: Analyze requirements.txt or pyproject.toml for complexity indicators"""`
- Line 108: `TODO: Add custom dependency analysis`
- Line 119: `"""TODO: Analyze code structure for complexity patterns"""`
- Line 129: `TODO: Analyze function complexity, class structures, etc.`
- Line 134: `"""TODO: Analyze documentation for complexity indicators"""`
- Line 148: `"""TODO: Suggest optimal project structure based on detected patterns"""`
- Line 208: `"""TODO: Build comprehensive context for orchestrator"""`
- Line 218: `"""TODO: Extract project requirements"""`
- Line 225: `"""TODO: Scan existing project structure"""`
- Line 235: `"""TODO: Invoke orchestrator for design document creation"""`
- Line 258: `"""TODO: Invoke orchestrator for pattern detection"""`
- Line 271: `TODO: Parse orchestrator response to extract pattern`
- Line 284: `"""TODO: Invoke orchestrator for workflow generation"""`
- Line 319: `"""TODO: Invoke orchestrator for implementation validation"""`
- Line 360: `TODO: Configure your project settings`
- Line 376: `TODO: Implement feature development workflow`
- Line 418: `log_info "2. Customize TODO placeholders in generated code"`
- Line 423: `TODO: Implement project setup workflow`
- Line 436: `TODO: Create project-specific configuration`
- Line 443: `patterns: []   TODO: List preferred patterns`
- Line 455: `validation_level: "strict"   TODO: Choose: strict, moderate, lenient`
- Line 457: `TODO: Add custom settings`
- Line 463: `TODO: Add more workflow commands as needed`
- Line 475: `echo "TODO: Add custom commands for your workflow"`
- Line 524: `- **Clear Implementation Guidance**: Step-by-step TODO instructions throughout the process`
- Line 529: `- **Clear Customization Points**: All TODO placeholders include specific implementation guidance`

#### instructions/orchestration/orchestrator-hooks.md

- Line 29: `TODO: Implement design document existence check`
- Line 36: `TODO: Implement section validation`
- Line 46: `TODO: Implement Mermaid diagram validation`
- Line 57: `TODO: Add this function call to your project's validation workflow`
- Line 83: `TODO: Implement workflow file existence check`
- Line 90: `TODO: Implement Python syntax validation`
- Line 97: `TODO: Implement Pydantic model validation`
- Line 105: `TODO: Implement node validation`
- Line 113: `TODO: Validate workflow structure matches design.md`
- Line 116: `echo "💡 TODO: Implement design-workflow consistency check"`
- Line 124: `TODO: Add this function call to your project's CI/CD pipeline`

#### instructions/orchestration/template-standards.md

- Line 14: `**Critical Distinction**: These standards validate template structure and educational quality, NOT functional completeness. Missing implementations and TODO stubs are intentional design features.`
- Line 101: `TODO Comment Standards`
- Line 102: `- **Descriptive**: TODO comments must explain WHAT needs to be implemented`
- Line 104: `- **Specific**: Avoid generic "TODO: implement" - be specific about the task`
- Line 109: `TODO: Implement document retrieval from your vector database`
- Line 118: `TODO: implement this`
- Line 135: `- **Guided**: Clear TODO items direct users toward proper implementation`
- Line 161: `- Generic TODO comments`
- Line 168: `- Files without TODO comments (acceptable for simple files)`
- Line 200: `2. Include descriptive TODO comments with context`
- Line 231: `- **Issue**: Generic or unhelpful TODO comments`
- Line 242: `- TODO stubs guide users toward correct patterns`

#### pocketflow_tools/generators/code_generators.py

- Line 220: `f"     TODO: Implement {utility['name']}",`
- Line 222: `"     FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow",`
- Line 309: `"     TODO: Add authentication and authorization logic here",`
- Line 311: `"     FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow",`
- Line 322: `"     TODO: Add input validation and sanitization",`
- Line 324: `"     FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow",`
- Line 347: `"     FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow",`
- Line 598: `" TODO: Extract the exact data exec() needs from shared store",`
- Line 617: `for todo in prep_todos:`
- Line 618: `nodes_code.append(f"        {todo}")`
- Line 641: `" TODO: Implement the core processing logic using only prep_result",`
- Line 642: `" TODO: Return the processed result (avoid side effects here)",`
- Line 648: `for todo in exec_todos:`
- Line 649: `nodes_code.append(f"        {todo}")`
- Line 672: `" TODO: Store exec_result in shared store with appropriate key",`
- Line 673: `" TODO: Return flow signal for branching ('success', 'error', specific state)",`
- Line 679: `for todo in post_todos:`
- Line 680: `nodes_code.append(f"        {todo}")`
- Line 712: `"         FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow",`
- Line 733: `"         FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow",`

#### pocketflow_tools/generators/config_generators.py

- Line 232: `Generated on: TODO-SET-DATE`

#### pocketflow_tools/generators/template_engine.py

- Line 68: `Matches the legacy regex-based extraction of code blocks and TODO lines.`
- Line 79: `todo_lines = re.findall(r".*TODO:.*", content)`

#### scripts/analyze-todos.py

- Line 4: `This script analyzes TODO comments across the codebase and categorizes them`
- Line 37: `TODO categorization patterns`
- Line 95: `"""Find all TODO comments in a file.`
- Line 114: `"""Categorize a TODO based on patterns and file location.`
- Line 155: `Categorize each TODO`
- Line 167: `print(" TODO Analysis Report")`
- Line 243: `Clean up the TODO text for display`

#### scripts/validation/validate-determinism.sh

- Line 173: `Function to validate TODO placeholders exist`
- Line 184: `if ! grep -q "TODO:" "$file_path"; then`
- Line 185: `log_warning "$pattern: No TODO placeholders found in $file"`
- Line 192: `log_warning "$pattern: $missing_todos files missing TODO placeholders"`

#### scripts/validation/validate-end-user-workflows.sh

- Line 251: `- Status tracking (todo, in-progress, completed)`
- Line 276: `"status": "enum:todo,in_progress,completed",`

#### scripts/validation/validate-integration.sh

- Line 96: `Test 3: Contains TODO placeholders for end-users`
- Line 97: `local todo_count=$(grep -c "TODO:" "$ext_file" || echo "0")`
- Line 99: `echo "❌ $ext_name has insufficient TODO guidance ($todo_count found, minimum 5 required)"`
- Line 214: `Test 3: Template sections contain TODO guidance`
- Line 215: `local validate_design_todos=$(grep -A 50 " validate_design_document" "$hooks_file" | grep -c "TODO:" || echo "0")`
- Line 217: `echo "❌ validate_design_document section has insufficient TODO guidance ($validate_design_todos found)"`
- Line 221: `local validate_workflow_todos=$(grep -A 50 " validate_workflow_implementation" "$hooks_file" | grep -c "TODO:" || echo "0")`
- Line 223: `echo "❌ validate_workflow_implementation section has insufficient TODO guidance ($validate_workflow_todos found)"`

#### scripts/validation/validate-orchestration.sh

- Line 131: `Check for adequate TODO guidance (minimum 5 TODOs)`
- Line 132: `local todo_count=$(grep -c "TODO:" "$ext" || echo "0")`

#### scripts/validation/validate-phase3-integrity.sh

- Line 59: `Phase 3 Requirement 1: Assert TODO placeholders exist in nodes.py, flow.py, router.py`
- Line 61: `log_info "Checking TODO placeholders in required files"`
- Line 69: `if grep -q "TODO:" "$file_path"; then`
- Line 70: `echo "  ✓ $file contains TODO placeholders"`
- Line 75: `report_result "TODO Placeholders" "FAIL" "Required file missing: $file"`
- Line 81: `report_result "TODO Placeholders" "PASS" "All required files contain TODO placeholders"`
- Line 83: `report_result "TODO Placeholders" "FAIL" "Files missing TODO placeholders: ${missing_todos[*]}"`

#### scripts/validation/validate-user-experience.sh

- Line 198: `Check for meaningful TODO placeholders`
- Line 199: `local todo_count=$(grep -r "TODO:" "$test_project" 2>/dev/null | wc -l)`
- Line 202: `log_error "No educational TODO placeholders found"`

#### standards/best-practices.md

- Line 650: `- Generated utilities should include TODO comments`

