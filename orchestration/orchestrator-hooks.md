# Orchestrator Integration Hooks

## Document Orchestration Integration

The product planning process integrates with the document-orchestration-coordinator agent to optimize document creation through parallel execution patterns.

### Parallel Document Creation Hook

Replace sequential document creation (Steps 3-7) with coordinated parallel execution:

```markdown
<step number="3-7" subagent="document-orchestration-coordinator" name="parallel_document_creation">

### Steps 3-7: Coordinated Parallel Document Creation

**Uses:** document-orchestration-coordinator subagent for optimized parallel document generation

Use the document-orchestration-coordinator subagent to create all product documents in parallel groups based on dependency analysis, achieving 20%+ performance improvement over sequential execution.

<subagent_context>
  **Context:** User input, strategic planning, documentation requirements, parallel execution patterns
  **Output:** Complete set of product documents with consistency validation
  **Performance Target:** >20% improvement over sequential execution
</subagent_context>

**Parallel Groups:**
- **Group A (Independent)**: mission, tech-stack, design, pre-flight checklist
- **Group B (Dependent)**: roadmap, CLAUDE.md

**Quality Assurance:** Cross-document consistency validation and PocketFlow compliance

<instructions>
  ACTION: Use document-orchestration-coordinator subagent for parallel document creation
  REQUEST: "Coordinate parallel document creation for product planning:
            - User context: [COMPLETE_USER_INPUT_FROM_STEP_1]
            - Strategic planning: [STRATEGIC_RECOMMENDATIONS_FROM_STEP_1_5]
            - Documentation discovery: [EXTERNAL_DOCS_FROM_STEP_1_6]
            - Pattern validation: [VALIDATED_PATTERNS_FROM_STEP_4_6]
            - Target documents: [mission.md, tech-stack.md, design.md, pre-flight.md, roadmap.md, CLAUDE.md]
            - Parallel groups: [GROUP_A_INDEPENDENT, GROUP_B_DEPENDENT]
            - Quality requirements: [CONSISTENCY_VALIDATION, POCKETFLOW_COMPLIANCE]"
  PROCESS: Parallel document creation with dependency management
  VALIDATE: Cross-document consistency and architectural coherence
  REPORT: Performance metrics and completion status
</instructions>

</step>
```

### Integration Benefits

- **Performance**: 20%+ faster document creation through parallel execution
- **Consistency**: Automated cross-document validation ensures coherence
- **Quality**: Built-in PocketFlow compliance and template adherence
- **Reliability**: Error recovery and fallback strategies for robust execution

### Fallback Strategy

If document-orchestration-coordinator fails or is unavailable, the system automatically falls back to sequential document creation using individual specialized agents for each document type.

### Validation Hooks

The orchestrator provides additional validation layers:
- Pre-execution input validation
- Cross-document consistency checks
- PocketFlow architecture compliance
- Template format adherence
- Performance metrics collection