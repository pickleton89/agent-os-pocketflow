---
description: Rules to finish off and deliver to user set of tasks that have been completed using Agent OS + PocketFlow
globs:
alwaysApply: false
version: 2.1 # Complete 3-phase post-execution workflow for v1.4.1
encoding: UTF-8
---

# Task Post-Execution Rules

## Overview

Follow these steps to validate implementation, mark progress updates, create a recap, and deliver the final report to the user. Enhanced with PocketFlow LLM/AI validation capabilities and integrated with the project-manager subagent.

<pre_flight_check>
  EXECUTE: @~/.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" name="pocketflow_validation" conditional="true">

### Step 1: PocketFlow Implementation Validation (Conditional)

**Condition**: Execute only if LLM/AI components are detected in the implementation.

<llm_ai_detection>
  <check_criteria>
    - Existence of docs/design.md file
    - Presence of nodes.py or flow.py files
    - PocketFlow pattern usage in tasks
    - LLM-related utility functions in utils/
    - AI/ML libraries in dependencies
  </check_criteria>
</llm_ai_detection>

<conditional_execution>
  <if_llm_ai_detected>
    <validation_checklist>
      - [ ] docs/design.md exists and is complete
      - [ ] Implementation follows design.md specifications
      - [ ] PocketFlow patterns correctly implemented
      - [ ] Node/Flow structure matches design
      - [ ] Utility functions have proper type hints
      - [ ] LLM calls include proper error handling
      - [ ] Structured output validation works
      - [ ] Chat history/caching implemented as designed
    </validation_checklist>
    
    <validation_actions>
      VERIFY: All PocketFlow components match design.md
      CHECK: Node prep/exec/post methods implemented correctly
      VALIDATE: Flow connections and transitions work
      CONFIRM: Error handling converts to proper action strings
      TEST: LLM integration functions as expected
    </validation_actions>
  </if_llm_ai_detected>
  
  <if_no_llm_ai>
    <skip_message>Skipping PocketFlow validation - no LLM/AI components detected</skip_message>
  </if_no_llm_ai>
</conditional_execution>

<instructions>
  DETECT: Check for LLM/AI artifacts before executing
  CONDITIONAL: Execute validation only if LLM/AI components present
  VALIDATE: Complete PocketFlow pattern compliance
  DOCUMENT: Any deviations found during validation
</instructions>

</step>

<step number="2" name="test_suite_validation">

### Step 2: Test Suite Validation

<step_metadata>
  <validates>all tests pass before delivery</validates>
  <ensures>code quality standards met</ensures>
</step_metadata>

<test_execution_sequence>
  <linting>
    <command>uv run ruff check --fix .</command>
    <command>uv run ruff format .</command>
    <requirement>zero linting errors</requirement>
  </linting>
  
  <type_checking>
    <command>uv run ty check</command>
    <requirement>zero type errors</requirement>
  </type_checking>
  
  <unit_tests>
    <command>uv run pytest -v</command>
    <requirement>100% test pass rate</requirement>
  </unit_tests>
</test_execution_sequence>

<failure_handling>
  <on_failure>
    - Document specific failures
    - Fix issues before proceeding
    - Re-run failed test categories
    - Block delivery until all tests pass
  </on_failure>
</failure_handling>

<instructions>
  ACTION: Run complete test validation sequence
  REQUIRE: All tests must pass before proceeding
  FIX: Any failures immediately
  BLOCK: Delivery if quality standards not met
</instructions>

</step>

<step number="3" subagent="project-manager" name="task_completion_verification">

### Step 3: Task Completion Verification

<step_metadata>
  <uses>project-manager subagent</uses>
  <validates>all spec tasks completed</validates>
  <updates>task tracking files</updates>
</step_metadata>

Use the project-manager subagent to verify all tasks in the current spec are properly completed and update task tracking documentation.

<verification_request>
  REQUEST: "Verify completion status for all tasks in current spec:
           - Check tasks.md completion status
           - Validate implementation matches requirements  
           - Update any incomplete task markings
           - Identify any missed subtasks"
</verification_request>

<completion_criteria>
  - All parent tasks marked [x] in tasks.md
  - All subtasks properly completed
  - Implementation meets acceptance criteria
  - No blocking issues remain unresolved
</completion_criteria>

<instructions>
  ACTION: Use project-manager subagent for verification
  VALIDATE: Complete task completion across spec
  UPDATE: Task status files as needed
  CONFIRM: 100% completion before proceeding
</instructions>

</step>

<step number="4" subagent="project-manager" name="roadmap_progress_update">

### Step 4: Roadmap Progress Update

<step_metadata>
  <uses>project-manager subagent</uses>
  <updates>roadmap.md progress tracking</updates>
  <conditional>only if spec completes roadmap items</conditional>
</step_metadata>

Use the project-manager subagent to check if the completed spec fulfills any roadmap milestones and update roadmap.md accordingly.

<roadmap_update_request>
  REQUEST: "Review roadmap.md and update progress:
           - Check if current spec completes roadmap items
           - Mark completed milestones as [x]
           - Update progress percentages
           - Document completion dates"
</roadmap_update_request>

<update_criteria>
  <cautious_approach>
    - Only mark roadmap items complete if absolutely certain
    - Spec must fully implement the roadmap feature
    - All related tests must be passing
    - Implementation must be production-ready
  </cautious_approach>
</update_criteria>

<instructions>
  ACTION: Use project-manager subagent for roadmap updates
  EVALUATE: Whether spec completes roadmap goals
  UPDATE: Roadmap progress if applicable
  DOCUMENT: Completion status and dates
</instructions>

</step>

<step number="5" subagent="project-manager" name="recap_generation">

### Step 5: Recap Generation

<step_metadata>
  <uses>project-manager subagent</uses>
  <creates>completion recap document</creates>
  <replaces>deprecated decisions.md approach</replaces>
</step_metadata>

Use the project-manager subagent to generate a comprehensive recap document for the completed spec in the .agent-os/recaps/ directory.

<recap_generation_request>
  REQUEST: "Generate completion recap for current spec:
           - Create recap file in .agent-os/recaps/
           - Include implementation summary and technical details
           - Document PocketFlow patterns used (if applicable)
           - Note challenges encountered and solutions
           - Record testing approach and coverage
           - Identify future considerations or improvements"
</recap_generation_request>

<recap_template>
  <filename>SPEC_NAME_recap.md</filename>
  <sections>
    - Summary: What was implemented
    - Implementation Details: Technical approach
    - PocketFlow Patterns: LLM/AI specifics (if applicable)
    - Challenges: Issues and resolutions
    - Testing: Coverage and validation
    - Future Considerations: Improvements and follow-ups
  </sections>
</recap_template>

<instructions>
  ACTION: Use project-manager subagent for recap creation
  GENERATE: Comprehensive completion documentation
  STORE: In .agent-os/recaps/ directory
  INCLUDE: All relevant technical and process details
</instructions>

</step>

<step number="6" name="git_workflow_completion">

### Step 6: Git Workflow Completion

<step_metadata>
  <commits>all changes</commits>
  <creates>pull request</creates>
  <completes>delivery workflow</completes>
</step_metadata>

<git_workflow_sequence>
  <commit_process>
    <stage>git add -A</stage>
    <commit>
      <message>Descriptive summary of implemented features</message>
      <format>Conventional commits style</format>
      <attribution>
        🤖 Generated with [Claude Code](https://claude.ai/code)
        
        Co-Authored-By: Claude &lt;noreply@anthropic.com&gt;
      </attribution>
    </commit>
  </commit_process>
  
  <push_and_pr>
    <push>git push origin [branch]</push>
    <pull_request>
      <title>Clear, descriptive PR title</title>
      <description>
        - Summary of changes
        - Key features implemented  
        - Testing coverage
        - Any special considerations
      </description>
    </pull_request>
  </push_and_pr>
</git_workflow_sequence>

<instructions>
  ACTION: Complete git workflow with commit and PR
  COMMIT: All changes with proper attribution
  PUSH: To appropriate branch
  CREATE: Pull request with comprehensive description
</instructions>

</step>

<step number="7" name="completion_notification">

### Step 7: Completion Notification

<step_metadata>
  <notifies>user of completion</step_metadata>
  <plays>completion sound</plays>
</step_metadata>

<notification_sequence>
  <system_sound>
    <command>afplay /System/Library/Sounds/Glass.aiff</command>
    <purpose>Alert user of completion</purpose>
  </system_sound>
</notification_sequence>

<instructions>
  ACTION: Play system completion sound
  ALERT: User that all tasks are complete
</instructions>

</step>

<step number="8" name="delivery_summary">

### Step 8: Delivery Summary

<step_metadata>
  <creates>final user report</creates>
  <summarizes>all completed work</step_metadata>
</step_metadata>

<summary_template>
  ## ✅ Implementation Complete
  
  **Spec**: [SPEC_NAME]
  **Features Implemented**: 
  - [FEATURE_1] - [BRIEF_DESCRIPTION]
  - [FEATURE_2] - [BRIEF_DESCRIPTION]
  
  **PocketFlow Components** (if applicable):
  - [COMPONENT_1] - [DESCRIPTION]
  
  **Testing**:
  - All tests passing ✓
  - Code quality standards met ✓
  - Type safety validated ✓
  
  **Documentation**:
  - Tasks marked complete in tasks.md ✓
  - Roadmap updated (if applicable) ✓ 
  - Recap created in .agent-os/recaps/ ✓
  
  **Pull Request**: [PR_URL]
  
  **Next Steps**:
  - [RECOMMENDED_ACTION_1]
  - [RECOMMENDED_ACTION_2]
</summary_template>

<conditional_sections>
  <pocketflow_details>
    **PocketFlow Implementation Details**:
    - Design compliance: [STATUS]
    - LLM providers used: [PROVIDERS]
    - Node/Flow patterns: [PATTERNS]
  </pocketflow_details>
  
  <issues_encountered>
    **Issues Resolved**:
    - [ISSUE_1] - [RESOLUTION]
  </issues_encountered>
</conditional_sections>

<instructions>
  ACTION: Generate comprehensive delivery summary
  INCLUDE: All completed features and validation results
  HIGHLIGHT: Key achievements and next steps
  FORMAT: Clear, scannable structure with emojis
</instructions>

</step>

</process_flow>

## Quality Assurance

<quality_checklist>
  - [ ] PocketFlow validation completed (if LLM/AI components)
  - [ ] All tests passing (linting, types, unit tests)
  - [ ] Task completion verified by project-manager
  - [ ] Roadmap updated (if applicable)  
  - [ ] Recap generated and stored
  - [ ] Git workflow completed with PR
  - [ ] User notified with completion sound
  - [ ] Delivery summary provided
</quality_checklist>

<blocking_criteria>
  <must_complete_before_delivery>
    - Test suite must pass 100%
    - All spec tasks must be marked complete
    - PocketFlow validation must pass (if applicable)
    - Git commit and push must succeed
  </must_complete_before_delivery>
</blocking_criteria>

## Integration Notes

This workflow integrates with:
- **project-manager subagent**: For task verification, roadmap updates, and recap generation
- **PocketFlow validation**: For LLM/AI component compliance checking
- **Recaps system**: Replacing deprecated decisions.md approach
- **3-phase execution model**: As the final phase after pre-execution and execution