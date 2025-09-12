# Documentation Fetch Implementation Plan

> Plan for implementing active documentation fetching in Agent OS + PocketFlow Framework
> Created: 2025-09-12

## Overview

This plan addresses the gap where documentation URLs are collected but never actually fetched or used. The framework needs to provide better instructions for agents in end-user projects to actively fetch, cache, and use documentation.

## Framework Context

**Important:** This repository IS the Agent OS + PocketFlow framework itself - NOT a project using it.
- We generate **instruction files** that tell agents what to do in end-user projects
- We're not implementing the fetching here - we're writing instructions for agents to follow
- The actual fetching happens when agents follow these instructions in real projects

## Current State Analysis

### What Currently Happens
1. Step 1.6 in plan-product asks users for documentation sources ✅
2. Users provide URLs or local file paths ✅
3. docs-registry.yaml gets created with source references ✅
4. **Gap:** Documentation is never actually fetched or cached ❌
5. **Gap:** No explicit instructions for agents to use WebFetch or Read tools ❌
6. **Gap:** Cache directory is never created or populated ❌

### Root Cause
- Instructions say "Fetch content using appropriate handler" but don't provide explicit tool usage directives
- smart_features.py contains placeholder TODOs (intentional for framework templates)
- No clear distinction between URL and local file handling in instructions

## Implementation Tasks

### Task 1: Enhance instructions/core/plan-product.md Step 1.6

**Purpose:** Add explicit instructions for agents to fetch and cache documentation

**Enhanced instructions to add:**
```xml
<documentation_processing>
  FOR each provided documentation source:
    IF source starts with "http://" or "https://":
      INSTRUCT: Use WebFetch tool with extraction prompt for API patterns, authentication methods, key endpoints, and implementation examples
      INSTRUCT: Store fetched content in .agent-os/cache/ using appropriate naming
    ELIF source starts with "/" or "~":
      INSTRUCT: Use Read tool to access the local file
      INSTRUCT: Process content based on file type (.md, .pdf, .txt, .html) capabilities
      INSTRUCT: Extract patterns and store in cache with consistent structure
    INSTRUCT: Create .agent-os/cache/ directory as needed
    INSTRUCT: Update .agent-os/docs-registry.yaml with appropriate metadata:
      - source_type identification
      - original_path preservation
      - extracted_patterns documentation
      - timestamp tracking
      - cache reference information
</documentation_processing>
```

### Task 2: Update instructions/core/execute-tasks.md Step 2.7

**Purpose:** Add instructions for validating and using cached documentation

**Enhanced validation instructions:**
```xml
<validation_process>
  INSTRUCT: Read .agent-os/docs-registry.yaml if present
  FOR each documented source:
    IF source_type is "url":
      INSTRUCT: Check cache freshness, refresh with WebFetch as needed
    ELIF source_type is "local":
      INSTRUCT: Verify file still exists at original_path
      INSTRUCT: Re-read with Read tool if file appears modified
    INSTRUCT: Load available cached documentation content
    INSTRUCT: Provide context-aware suggestions based on available documentation
</validation_process>
```

### Task 3: Enhance instructions/core/create-spec.md

**Purpose:** Add documentation lookup during specification creation

**Pattern detection instructions to add:**
```xml
<pattern_detection>
  INSTRUCT: When technology patterns detected, check .agent-os/docs-registry.yaml
  FOR matching documentation:
    IF source_type is "local":
      INSTRUCT: Read latest version of file if accessible
      INSTRUCT: Extract implementation examples relevant to detected patterns
    ELIF source_type is "url":
      INSTRUCT: Use cached content or refresh as appropriate
    INSTRUCT: Include relevant documentation snippets in specification context
</pattern_detection>
```

### Task 4: Update instructions/core/documentation-discovery.md

**Purpose:** Define clear handler instructions for different source types

**Handler instruction sections to enhance:**
```xml
<url_handler_instructions>
  TOOLS_TO_USE: WebFetch
  PROCESS_FLOW: Instruct agents on Fetch → Extract → Cache → Register workflow
  EXTRACTION_GUIDANCE: Direct agents to identify API patterns, authentication, endpoints, examples
  CACHE_GUIDANCE: Provide TTL recommendations (24 hours overview, 6 hours implementation)
</url_handler_instructions>

<local_file_handler_instructions>
  TOOLS_TO_USE: Read (for .md, .txt), Read with PDF capability (for .pdf)
  PROCESS_FLOW: Instruct agents on Read → Parse → Extract → Cache → Register workflow
  SUPPORTED_FORMATS: Guide agents on .md, .txt, .pdf, .html, .rst, .json, .yaml handling
  EXTRACTION_GUIDANCE: Direct agents to apply same pattern extraction as URL handler
  CHANGE_DETECTION: Instruct agents on file modification time checking approaches
</local_file_handler_instructions>
```

### Task 5: Update templates/docs-registry.yaml.template

**Purpose:** Enhance registry structure to support both source types

**Template structure enhancements:**
```yaml
# Registry template showing structure for agents to populate
tech_stack:
  example_entry:
    source_type: "url|local"  # agents determine type
    source: "URL_OR_PATH"     # agents populate with actual source
    original_path: "..."      # agents preserve for reference
    cache_reference: "..."    # agents create cache lookup method
    last_accessed: "DATE"     # agents track access time
    file_modified: "DATE"     # agents track for local files
    extracted_patterns:       # agents populate based on content
      - "Pattern descriptions agents identify"
    cache_suggestions: 24     # suggested TTL hours
    status: "active|stale|error"  # agents maintain status
```

### Task 6: Keep smart_features.py as Template (No Changes)

**Rationale:** This file intentionally contains TODO placeholders as it's a template showing structure for end-user implementations. The framework provides guidance; agents in end-user projects do the actual work.

## Expected Outcomes

After implementing these instruction enhancements:

1. **Instructions will direct agents** to fetch documentation when URLs are provided during plan-product
2. **Instructions will guide agents** to read and process local documentation files alongside web sources
3. **Instructions will tell agents** to create cache directories and store processed documentation
4. **Instructions will enable agents** to use documentation content during spec creation and task execution
5. **Instructions will guide agents** on change detection for local files
6. **Instructions will direct agents** on TTL-based refresh for web documentation

## Testing Strategy

### In Framework Repository
1. Validate instruction files have clear, actionable directives
2. Ensure registry template supports both source types
3. Verify instructions distinguish between URL and local file handling

### In End-User Project (Testing Framework-Generated Instructions)
1. Run `/plan-product` and provide both URL and local documentation
2. Observe if enhanced instructions guide agent to create `.agent-os/cache/` directory
3. Verify enhanced instructions result in cache files with extracted content
4. Check that enhanced instructions populate `docs-registry.yaml` with patterns
5. Run `/create-spec` and verify enhanced instructions enable documentation suggestions
6. Run `/execute-tasks` and confirm enhanced instructions enable documentation usage

## Success Criteria

- [ ] Instructions explicitly tell agents to use WebFetch for URLs
- [ ] Instructions explicitly tell agents to use Read for local files
- [ ] Cache directory creation is explicitly instructed
- [ ] Registry structure supports both source types
- [ ] Instructions direct agents to fetch and cache documentation in end-user projects
- [ ] Instructions enable agents to use cached documentation during workflows

## Notes

- We're improving **instructions that agents follow**, not implementing functionality ourselves
- The framework provides guidance; agents in end-user projects do the work
- TODO placeholders in smart_features.py are intentional - they show structure for customization
- This approach respects the Framework vs Usage distinction