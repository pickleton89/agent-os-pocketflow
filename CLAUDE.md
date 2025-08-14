# Project Configuration
Uses PocketFlow Orchestrator for planning and implementation.

## 🎯 Orchestration Mode Active
This project uses the **PocketFlow Orchestrator** for all planning and implementation tasks.

### Automatic Orchestration
ALWAYS invoke the pocketflow-orchestrator agent when:
- User says: "think", "plan", "design", "architect", "implement"
- Creating any specification or workflow
- Executing complex tasks
- Solving problems requiring multiple steps

### Automatic Codebase Analysis
ALWAYS invoke analyze-product when user says:
- "analyze existing project"
- "analyze current codebase"
- "analyze this project" 
- "what's already implemented"
- "understand this codebase"
- "what's in this project"
- "review existing code"
- "assess current implementation"

### Integration Pattern
1. First: Use pocketflow-orchestrator for planning
2. Then: Generate Agent OS files based on plan
3. Finally: Implement using generated PocketFlow workflows
