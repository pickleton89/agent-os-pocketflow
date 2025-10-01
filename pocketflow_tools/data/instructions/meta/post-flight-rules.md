---
description: Common Post-Flight Steps for Agent OS Instructions
globs:
alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Post-Flight Rules

After completing all steps in a process_flow, always review your work and verify:

- Every numbered step has read, executed, and delivered according to its instructions.

- All steps that specified a subagent should be used, did in fact delegate those tasks to the specified subagent. IF they did not, see why the subagent was not used and report your findings to the user.

- IF you notice a step wasn't executed according to it's instructions, report your findings and explain which part of the instructions were misread or skipped and why.

## Verification Process

<verification_checklist>
  <step_completion_check>
    - [ ] Review each numbered step in the process_flow
    - [ ] Confirm step was actually executed (not just planned)
    - [ ] Verify step output matches step requirements
    - [ ] Document any steps that were skipped or modified
  </step_completion_check>

  <subagent_delegation_check>
    - [ ] Identify all steps marked with subagent attribute
    - [ ] Confirm Task tool was used for subagent delegation
    - [ ] Verify subagent actually completed the delegated work
    - [ ] Report any direct execution instead of delegation
  </subagent_delegation_check>

  <instruction_compliance_check>
    - [ ] Review step instructions vs actual execution
    - [ ] Identify any instruction misinterpretations
    - [ ] Document any deliberate deviations with justification
    - [ ] Report execution gaps or shortcuts taken
  </instruction_compliance_check>
</verification_checklist>

## Reporting Requirements

<compliance_reporting>
  <compliant_execution>
    MESSAGE: "✅ Post-Flight Verification Complete - All process_flow steps executed according to instructions with proper subagent delegation."
  </compliant_execution>

  <non_compliant_execution>
    REPORT: Detailed findings including:
    - Which steps were not executed properly
    - Why subagents were not used when specified
    - What instruction parts were misread or skipped
    - Impact of deviations on overall workflow
  </non_compliant_execution>
</compliance_reporting>

## Integration Notes

This post-flight verification should be executed as the final step in any process_flow to ensure:
- Process integrity and instruction compliance
- Proper subagent utilization patterns
- Quality assurance for workflow execution
- Audit trail for process improvements