# Agent OS Recaps Directory

This directory contains completion recaps for implemented features and specifications. Recaps replace the deprecated `decisions.md` approach with more practical post-completion documentation.

## Structure

- Each spec gets its own recap file: `SPEC_NAME_recap.md`
- Recaps are generated automatically by the project-manager subagent
- Files include implementation details, challenges, and patterns used

## Usage

Recaps are created automatically during the post-execution workflow when:
1. A spec is marked as complete
2. All tasks in the spec's tasks.md are finished
3. Tests are passing and code is committed

## Template

New recap files follow this structure:
- **Summary**: Brief description of what was implemented
- **Implementation Details**: Technical approach and patterns used
- **PocketFlow Patterns**: LLM/AI specific patterns (if applicable) 
- **Challenges**: Issues encountered and how they were resolved
- **Testing**: Test coverage and validation approach
- **Future Considerations**: Potential improvements or follow-ups