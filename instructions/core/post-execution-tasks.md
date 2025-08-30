---
description: Rules to finish off and deliver to user set of tasks that have been completed using Agent OS + PocketFlow
globs:
alwaysApply: false
version: 2.1 # Complete 3-phase post-execution workflow for v1.4.1
encoding: UTF-8
---

# Task Post-Execution Rules

## Overview

Follow these steps to validate implementation, mark progress updates, create a recap, and deliver the final report to the user. Enhanced with Universal PocketFlow validation capabilities and integrated with the project-manager subagent.

<pre_flight_check>
  EXECUTE: @~/.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="test-runner" name="test_suite_verification">

### Step 1: Run All Tests

Use the test-runner subagent to run ALL tests in the application's test suite to ensure no regressions and fix any failures until all tests pass.

<instructions>
  ACTION: Use test-runner subagent
  REQUEST: "Run the full test suite with comprehensive validation:
            - Execute linting: uv run ruff check --fix .
            - Execute formatting: uv run ruff format .
            - Execute type checking: uv run ty check
            - Execute unit tests: uv run pytest -v
            - Ensure 100% pass rate for all categories"
  WAIT: For test-runner analysis
  PROCESS: Fix any reported failures
  REPEAT: Until all tests pass
</instructions>

<test_execution>
  <order>
    1. Run linting and formatting
    2. Run type checking
    3. Run full test suite
    4. Fix any failures
  </order>
  <requirement>100% pass rate across all categories</requirement>
</test_execution>

<failure_handling>
  IF test_runner_fails:
    - Capture detailed error output and failure context
    - Attempt to fix obvious linting/formatting issues automatically
    - Re-run failed test categories up to 2 additional times
    - If tests still fail after 3 attempts, document specific failures
    - BLOCK progression and request user guidance on test failures
  ELSE:
    - Proceed to next step with confirmed test success
</failure_handling>

</step>

<step number="2" name="pocketflow_validation" universal="true">

### Step 2: PocketFlow Implementation Validation (Universal)

<step_metadata>
  <validates>PocketFlow architecture compliance</validates>
  <ensures>universal design-first methodology</ensures>
</step_metadata>

**Requirement**: Execute for all projects using universal PocketFlow architecture.

<universal_pocketflow_requirements>
  <validation_criteria>
    - Existence of docs/design.md file (mandatory)
    - Presence of nodes.py and flow.py files (universal)
    - PocketFlow pattern implementation in tasks
    - Domain-specific utility functions in utils/
    - Proper dependency management and tooling
  </validation_criteria>
</universal_pocketflow_requirements>

<universal_execution>
  <validation_checklist>
    - [ ] docs/design.md exists and is complete
    - [ ] Implementation follows design.md specifications
    - [ ] PocketFlow patterns correctly implemented
    - [ ] Node/Flow structure matches design
    - [ ] Utility functions have proper type hints
    - [ ] Domain logic includes proper error handling
    - [ ] Data validation and processing works
    - [ ] Architecture patterns implemented as designed
  </validation_checklist>
  
  <validation_actions>
    VERIFY: All PocketFlow components match design.md
    CHECK: Node prep/exec/post methods implemented correctly
    VALIDATE: Flow connections and transitions work
    CONFIRM: Error handling converts to proper action strings
    TEST: All integrations function as expected
  </validation_actions>
</universal_execution>

<validation_failure_handling>
  IF pocketflow_validation_fails:
    - Document specific compliance failures found
    - Identify missing components (docs/design.md, nodes.py, flow.py)
    - Check for pattern implementation gaps
    - BLOCK progression until critical architecture issues resolved
    - Provide specific remediation steps for each failure
  ELSE:
    - Proceed with validated PocketFlow implementation
</validation_failure_handling>

<instructions>
  UNIVERSAL: Execute for all projects using PocketFlow architecture
  VALIDATE: Complete PocketFlow pattern compliance for all projects
  VERIFY: Universal design-first methodology compliance
  DOCUMENT: Any deviations found during validation
  BLOCK: Progression on critical architecture failures
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

<verification_failure_handling>
  IF project_manager_fails_verification:
    - Document specific incomplete tasks or verification failures
    - Re-run verification with enhanced context if needed
    - Request manual task completion if verification is blocked
    - BLOCK progression until all tasks are properly completed
  ELSE:
    - Proceed with confirmed task completion status
</verification_failure_handling>

<instructions>
  ACTION: Use project-manager subagent for verification
  VALIDATE: Complete task completion across spec
  UPDATE: Task status files as needed
  CONFIRM: 100% completion before proceeding
  BLOCK: Progression on incomplete task verification
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

<roadmap_update_failure_handling>
  IF project_manager_cannot_update_roadmap:
    - Document roadmap access or parsing issues
    - Attempt manual roadmap review if subagent fails
    - Skip roadmap updates with clear documentation if blocked
    - Continue to next step (non-blocking failure)
  ELSE:
    - Proceed with roadmap updates completed
</roadmap_update_failure_handling>

<instructions>
  ACTION: Use project-manager subagent for roadmap updates
  EVALUATE: Whether spec completes roadmap goals
  UPDATE: Roadmap progress if applicable
  DOCUMENT: Completion status and dates
  FALLBACK: Manual review if subagent fails (non-blocking)
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
    - PocketFlow Patterns: Architecture specifics (universal requirement)
    - Challenges: Issues and resolutions
    - Testing: Coverage and validation
    - Future Considerations: Improvements and follow-ups
  </sections>
</recap_template>

<recap_failure_handling>
  IF project_manager_fails_recap_generation:
    - Document recap generation failures or access issues
    - Attempt manual recap creation if subagent fails
    - Use fallback template to create basic recap
    - BLOCK progression until recap is successfully created
  ELSE:
    - Proceed with recap successfully generated
</recap_failure_handling>

<instructions>
  ACTION: Use project-manager subagent for recap creation
  GENERATE: Comprehensive completion documentation
  STORE: In .agent-os/recaps/ directory
  INCLUDE: All relevant technical and process details
  BLOCK: Progression until recap successfully created
</instructions>

</step>

<step number="6" subagent="git-workflow" name="git_workflow">

### Step 6: Git Workflow

<step_metadata>
  <uses>git-workflow subagent</uses>
  <commits>all changes</commits>
  <creates>pull request</creates>
</step_metadata>

Use the git-workflow subagent to create git commit, push to GitHub, and create pull request for the implemented features.

<instructions>
  ACTION: Use git-workflow subagent
  REQUEST: "Complete git workflow for [SPEC_NAME] feature:
            - Spec: [SPEC_FOLDER_PATH]
            - Changes: All modified files including PocketFlow components
            - Target: main branch
            - Description: [SUMMARY_OF_IMPLEMENTED_FEATURES]
            - Include PocketFlow patterns and architecture details"
  WAIT: For workflow completion
  PROCESS: Save PR URL for summary
</instructions>

<commit_process>
  <commit>
    <message>descriptive summary of changes</message>
    <format>conventional commits if applicable</format>
    <attribution>
      🤖 Generated with [Claude Code](https://claude.ai/code)
      
      Co-Authored-By: Claude &lt;noreply@anthropic.com&gt;
    </attribution>
  </commit>
  <push>
    <target>spec branch</target>
    <remote>origin</remote>
  </push>
  <pull_request>
    <title>descriptive PR title</title>
    <description>functionality recap with PocketFlow details</description>
  </pull_request>
</commit_process>

<git_workflow_failure_handling>
  IF git_workflow_subagent_fails:
    - Document git operation failures (commit, push, or PR creation)
    - Attempt manual git operations as fallback
    - Check for connectivity issues, authentication problems, or merge conflicts
    - BLOCK progression until git operations complete successfully
    - Save error context for troubleshooting
  ELSE:
    - Proceed with successful git workflow completion
</git_workflow_failure_handling>

</step>

<step number="7" subagent="project-manager" name="completion_notification">

### Step 7: Task Completion Notification

<step_metadata>
  <uses>project-manager subagent</uses>
  <notifies>user of completion</notifies>
  <plays>completion sound</plays>
</step_metadata>

Use the project-manager subagent to play a system sound to alert the user that tasks are complete.

<notification_command>
  afplay /System/Library/Sounds/Glass.aiff
</notification_command>

<notification_failure_handling>
  IF project_manager_fails_notification:
    - Document sound playback failures
    - Attempt direct command execution as fallback
    - Continue to next step (non-blocking failure)
  ELSE:
    - Proceed with successful notification
</notification_failure_handling>

<instructions>
  ACTION: Use project-manager subagent
  REQUEST: "Play completion sound to alert user:
            - Execute: afplay /System/Library/Sounds/Glass.aiff
            - Purpose: Alert user that task is complete"
  PROCESS: Confirm sound played successfully
  FALLBACK: Continue if sound fails (non-blocking)
</instructions>

</step>

<step number="8" subagent="project-manager" name="completion_summary">

### Step 8: Completion Summary

<step_metadata>
  <uses>project-manager subagent</uses>
  <creates>structured summary message</creates>
  <includes>PocketFlow implementation details</includes>
</step_metadata>

Use the project-manager subagent to create a structured summary message with emojis showing what was done, any issues, testing instructions, and PR link.

<instructions>
  ACTION: Use project-manager subagent
  REQUEST: "Create comprehensive completion summary:
            - Include all implemented features with PocketFlow components
            - Document any issues encountered and resolutions
            - Add testing instructions if applicable
            - Include PR link and next steps
            - Format with emoji headers for scannability"
  WAIT: For summary generation
  PROCESS: Verify all key information included
</instructions>

<summary_template>
  ## ✅ What's been done

  1. **[FEATURE_1]** - [ONE_SENTENCE_DESCRIPTION]
  2. **[FEATURE_2]** - [ONE_SENTENCE_DESCRIPTION]

  ## 🏗️ PocketFlow Components (if applicable)
  
  - **[COMPONENT_1]** - [DESCRIPTION]
  - **Design compliance**: [STATUS]
  - **Node/Flow patterns**: [PATTERNS]

  ## ⚠️ Issues encountered

  [ONLY_IF_APPLICABLE]
  - **[ISSUE_1]** - [DESCRIPTION_AND_REASON]

  ## 🧪 Ready to test in browser

  [ONLY_IF_APPLICABLE]
  1. [STEP_1_TO_TEST]
  2. [STEP_2_TO_TEST]

  ## 📦 Pull Request

  View PR: [GITHUB_PR_URL]
  
  ## 📋 Next Steps
  
  - [RECOMMENDED_ACTION_1]
  - [RECOMMENDED_ACTION_2]
</summary_template>

<summary_sections>
  <required>
    - functionality recap
    - PocketFlow components (if applicable)
    - pull request info
    - next steps
  </required>
  <conditional>
    - issues encountered (if any)
    - testing instructions (if testable in browser)
  </conditional>
</summary_sections>

<summary_failure_handling>
  IF project_manager_fails_summary_generation:
    - Document summary generation failures
    - Use fallback template to create manual summary
    - Include all required sections with available information
    - BLOCK delivery until summary is successfully created
  ELSE:
    - Proceed with comprehensive summary generated
</summary_failure_handling>

</step>

<step number="9" name="post_flight_verification">

### Step 9: Post-Flight Rules Verification

<step_metadata>
  <validates>process_flow execution compliance</validates>
  <ensures>instruction adherence and subagent utilization</ensures>
</step_metadata>

Execute post-flight verification to ensure all process_flow steps were executed according to instructions with proper subagent delegation.

<post_flight_execution>
  EXECUTE: @~/.agent-os/instructions/meta/post-flight-rules.md
</post_flight_execution>

<verification_scope>
  <step_completion>
    - Verify each numbered step (1-8) was actually executed
    - Confirm step outputs match step requirements
    - Document any skipped or modified steps
  </step_completion>
  
  <subagent_delegation>
    - Confirm step 1 used test-runner subagent via Task tool
    - Confirm steps 3, 4, 5, 7, 8 used project-manager subagent via Task tool
    - Confirm step 6 used git-workflow subagent via Task tool
    - Verify delegation occurred rather than direct execution
    - Report any subagent bypassing with justification
  </subagent_delegation>
  
  <instruction_compliance>
    - Review execution vs written instructions
    - Identify any misinterpretations or shortcuts
    - Document deviations with impact assessment
  </instruction_compliance>
</verification_scope>

<instructions>
  ACTION: Execute post-flight verification process
  VALIDATE: All process_flow steps executed per instructions
  VERIFY: Proper subagent delegation occurred
  REPORT: Any compliance issues or deviations found
</instructions>

</step>

</process_flow>

## Quality Assurance

<quality_checklist>
  - [ ] All tests passing via test-runner subagent
  - [ ] PocketFlow validation completed (universal requirement)
  - [ ] Task completion verified by project-manager
  - [ ] Roadmap updated (if applicable) by project-manager
  - [ ] Recap generated and stored by project-manager
  - [ ] Git workflow completed with PR via git-workflow subagent
  - [ ] User notified with completion sound
  - [ ] Delivery summary provided by project-manager
  - [ ] Post-flight verification completed
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
- **test-runner subagent**: For comprehensive test suite execution and validation
- **project-manager subagent**: For task verification, roadmap updates, recap generation, and completion summaries
- **git-workflow subagent**: For git commit, push, and pull request creation
- **PocketFlow validation**: For universal architecture compliance checking
- **Recaps system**: Replacing deprecated decisions.md approach
- **Post-flight verification**: For process compliance and instruction adherence validation
- **3-phase execution model**: As the final phase after pre-execution and execution