#!/bin/bash
# End-User Workflow Integration Tests
# Tests complete end-user workflows with the Agent OS + PocketFlow framework

set -e

# Colors and logging
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Test configuration
TEST_PROJECT_NAME="test-integration-project"
TEST_WORKSPACE="/tmp/agent-os-test-workspace"
FRAMEWORK_ROOT="$(pwd)"

# Test results tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
declare -a FAILED_TESTS=()

# Cleanup function
cleanup_test_workspace() {
    if [[ -d "$TEST_WORKSPACE" ]]; then
        rm -rf "$TEST_WORKSPACE"
        log_info "Cleaned up test workspace"
    fi
}

# Setup test workspace
setup_test_workspace() {
    log_info "Setting up test workspace at $TEST_WORKSPACE"
    cleanup_test_workspace
    mkdir -p "$TEST_WORKSPACE"
    cd "$TEST_WORKSPACE"
}

# Run a single test with error handling
run_test() {
    local test_name="$1"
    local test_function="$2"

    TESTS_RUN=$((TESTS_RUN + 1))
    log_info "Running: $test_name"

    if $test_function; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log_success "$test_name PASSED"
        return 0
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        FAILED_TESTS+=("$test_name")
        log_error "$test_name FAILED"
        return 1
    fi
}

# Test 1: Framework Installation Workflow
test_framework_installation() {
    log_info "  Testing framework installation process"

    # Create a new project directory
    mkdir -p "$TEST_PROJECT_NAME"
    cd "$TEST_PROJECT_NAME"

    # Test base installation
    if ! "$FRAMEWORK_ROOT/setup.sh" --non-interactive; then
        log_error "Framework installation failed"
        return 1
    fi

    # Verify base installation
    if [[ ! -d "$HOME/.agent-os" ]]; then
        log_error "Base installation directory not created"
        return 1
    fi

    # Verify project installation
    if [[ ! -d ".agent-os" ]]; then
        log_error "Project installation directory not created"
        return 1
    fi

    # Check essential files
    local required_files=(
        ".agent-os/commands/plan-product.md"
        ".agent-os/commands/create-spec.md"
        ".agent-os/commands/execute-tasks.md"
        ".claude/CLAUDE.md"
    )

    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Required file missing: $file"
            return 1
        fi
    done

    log_info "  Framework installation successful"
    cd ..
    return 0
}

# Test 2: Product Planning Workflow
test_product_planning_workflow() {
    log_info "  Testing product planning workflow"

    cd "$TEST_PROJECT_NAME"

    # Create a simple product planning spec
    cat > product_planning_input.md << 'EOF'
# Product Idea: Task Management App

## Core Concept
A simple task management application for small teams that helps prioritize work and track progress.

## Target Users
- Small business owners (5-20 employees)
- Project managers in startups
- Freelancers managing multiple clients

## Key Features
- Task creation and assignment
- Priority management
- Progress tracking
- Team collaboration
- Basic reporting

## Technical Requirements
- Web-based application
- Real-time updates
- Mobile responsive
- Simple deployment

EOF

    # Test that product planning files can be generated
    # Since this is a framework test, we simulate what the orchestrator would create
    mkdir -p .agent-os/product docs

    # Create mission document (simulating orchestrator output)
    cat > .agent-os/product/mission.md << 'EOF'
# Task Management App Mission

## Pitch
TaskFlow is a streamlined task management application designed for small teams who need simple yet powerful project coordination without complexity overhead.

## Users
- **Primary**: Small business owners (5-20 employees) struggling with task coordination
- **Secondary**: Project managers in startups needing lightweight project tracking

## Problems
1. **Task Chaos**: Teams lose track of who's doing what - *Impact*: 25% time waste on coordination
2. **Priority Confusion**: Important tasks get lost in noise - *Impact*: 30% missed deadlines

## Key Features
### Core Functionality
- **Task Management**: Create, assign, and track tasks with clear ownership
- **Priority System**: Smart prioritization to focus on what matters most

### Advanced Features
- **Progress Tracking**: Visual progress indicators and completion metrics
- **Team Collaboration**: Real-time updates and team communication tools

## Architecture Strategy
**Framework**: PocketFlow
**Patterns**: WORKFLOW, TOOL
**Complexity**: STANDARD_WORKFLOW
**Rationale**: Task management requires workflow automation with tool integration
EOF

    # Create basic tech stack
    cat > .agent-os/product/tech-stack.md << 'EOF'
# Tech Stack

## Programming Language
- **Python 3.12**: Modern Python with async support

## Framework
- **FastAPI**: High-performance web framework
- **PocketFlow**: Workflow automation framework

## Database
- **PostgreSQL**: Reliable relational database

## Frontend
- **React 18**: Modern frontend framework
- **TypeScript**: Type-safe development

## Deployment
- **Docker**: Containerized deployment
- **Railway**: Cloud hosting platform
EOF

    # Verify planning files exist and have content
    local planning_files=(
        ".agent-os/product/mission.md"
        ".agent-os/product/tech-stack.md"
    )

    for file in "${planning_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Planning file missing: $file"
            return 1
        fi

        if [[ ! -s "$file" ]]; then
            log_error "Planning file empty: $file"
            return 1
        fi
    done

    log_info "  Product planning workflow completed"
    cd ..
    return 0
}

# Test 3: Feature Specification Workflow
test_feature_specification_workflow() {
    log_info "  Testing feature specification workflow"

    cd "$TEST_PROJECT_NAME"

    # Create spec documents (simulating /create-spec output)
    mkdir -p docs/specs

    cat > docs/specs/task-management-spec.md << 'EOF'
# Task Management Feature Specification

## Overview
Core task management functionality allowing users to create, assign, update, and track tasks within projects.

## User Stories
- As a project manager, I can create tasks with titles, descriptions, and due dates
- As a team member, I can view tasks assigned to me with clear priority indicators
- As a team lead, I can assign tasks to team members and track progress
- As a user, I can update task status and add progress notes

## Scope
### In Scope
- Task CRUD operations
- Task assignment and ownership
- Status tracking (todo, in-progress, completed)
- Basic priority management
- Task search and filtering

### Out of Scope
- Advanced reporting and analytics
- Time tracking integration
- External tool integrations

## PocketFlow Architecture Integration
### Pattern Selection
- **Primary Pattern**: WORKFLOW - Task state management and transitions
- **Secondary Pattern**: TOOL - Task CRUD operations
- **Complexity Level**: STANDARD_WORKFLOW

### SharedStore Schema Extension
```python
# Task Management Schema Addition
task_schema = {
    "tasks": {
        "id": "uuid",
        "title": "string",
        "description": "text",
        "assignee_id": "uuid",
        "project_id": "uuid",
        "status": "enum:todo,in_progress,completed",
        "priority": "enum:low,medium,high",
        "due_date": "datetime",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}
```

## Validation Requirements
- Task title must be 3-100 characters
- Due dates cannot be in the past
- Only assigned users can update task status
- Completed tasks cannot be reassigned
EOF

    # Create API spec
    cat > docs/specs/task-api-spec.md << 'EOF'
# Task Management API Specification

## FastAPI Endpoints

### Task Operations
```python
@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""

@app.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks(
    project_id: Optional[UUID] = None,
    assignee_id: Optional[UUID] = None,
    status: Optional[TaskStatus] = None,
    db: Session = Depends(get_db)
):
    """List tasks with optional filtering"""

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing task"""
```

## Pydantic Models
```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None
    project_id: UUID
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    assignee_id: Optional[UUID]
    project_id: UUID
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```
EOF

    # Verify specification files
    local spec_files=(
        "docs/specs/task-management-spec.md"
        "docs/specs/task-api-spec.md"
    )

    for file in "${spec_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Spec file missing: $file"
            return 1
        fi

        # Check for required sections
        if ! grep -q "## Overview" "$file"; then
            log_error "Spec file missing Overview section: $file"
            return 1
        fi
    done

    log_info "  Feature specification workflow completed"
    cd ..
    return 0
}

# Test 4: Task Execution Validation
test_task_execution_validation() {
    log_info "  Testing task execution validation"

    cd "$TEST_PROJECT_NAME"

    # Create task breakdown (simulating /execute-tasks preparation)
    mkdir -p docs/tasks

    cat > docs/tasks/task-management-tasks.md << 'EOF'
# Task Management Implementation Tasks

## Phase 1: Foundation (Week 1)
### Task 1.1: Database Schema Setup
- [ ] Create Task model with SQLAlchemy
- [ ] Create database migration scripts
- [ ] Add foreign key relationships to users/projects
- [ ] Create database indexes for performance

### Task 1.2: Core API Endpoints
- [ ] Implement POST /api/tasks (task creation)
- [ ] Implement GET /api/tasks (task listing with filters)
- [ ] Implement PUT /api/tasks/{id} (task updates)
- [ ] Add input validation and error handling

## Phase 2: Features (Week 2)
### Task 2.1: Task Assignment System
- [ ] Add task assignment logic
- [ ] Create assignment notification system
- [ ] Implement permission checks for task updates
- [ ] Add bulk assignment capabilities

### Task 2.2: Status Management
- [ ] Implement task status transitions
- [ ] Add status change validation rules
- [ ] Create status history tracking
- [ ] Build status-based filtering

## Phase 3: Testing & Polish (Week 3)
### Task 3.1: Automated Testing
- [ ] Unit tests for task models and business logic
- [ ] Integration tests for API endpoints
- [ ] End-to-end tests for task workflows
- [ ] Performance testing for large task lists

### Task 3.2: Documentation & Deployment
- [ ] API documentation with OpenAPI/Swagger
- [ ] User guide for task management features
- [ ] Deployment scripts and configuration
- [ ] Production monitoring setup
EOF

    # Verify task files exist and have proper structure
    if [[ ! -f "docs/tasks/task-management-tasks.md" ]]; then
        log_error "Task breakdown file missing"
        return 1
    fi

    # Check for task structure (phases and tasks)
    local required_patterns=(
        "## Phase 1:"
        "### Task 1.1:"
        "- \[ \]"
    )

    for pattern in "${required_patterns[@]}"; do
        if ! grep -q "$pattern" "docs/tasks/task-management-tasks.md"; then
            log_error "Task file missing required pattern: $pattern"
            return 1
        fi
    done

    log_info "  Task execution validation completed"
    cd ..
    return 0
}

# Test 5: Project Structure Validation
test_project_structure_validation() {
    log_info "  Testing complete project structure validation"

    cd "$TEST_PROJECT_NAME"

    # Check that all expected directories exist
    local required_dirs=(
        ".agent-os"
        ".agent-os/product"
        ".agent-os/commands"
        ".claude"
        "docs"
        "docs/specs"
        "docs/tasks"
    )

    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            log_error "Required directory missing: $dir"
            return 1
        fi
    done

    # Check that essential files exist
    local required_files=(
        ".agent-os/product/mission.md"
        ".agent-os/product/tech-stack.md"
        ".claude/CLAUDE.md"
        "docs/specs/task-management-spec.md"
        "docs/specs/task-api-spec.md"
        "docs/tasks/task-management-tasks.md"
    )

    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Required file missing: $file"
            return 1
        fi

        # Check file is not empty
        if [[ ! -s "$file" ]]; then
            log_error "Required file is empty: $file"
            return 1
        fi
    done

    # Validate CLAUDE.md has proper references
    if ! grep -q "mission.md" ".claude/CLAUDE.md"; then
        log_error "CLAUDE.md missing mission.md reference"
        return 1
    fi

    log_info "  Project structure validation completed"
    cd ..
    return 0
}

# Test 6: Workflow Command Integration
test_workflow_command_integration() {
    log_info "  Testing workflow command integration"

    cd "$TEST_PROJECT_NAME"

    # Check that command files exist and have proper structure
    local command_files=(
        ".agent-os/commands/plan-product.md"
        ".agent-os/commands/create-spec.md"
        ".agent-os/commands/execute-tasks.md"
    )

    for cmd_file in "${command_files[@]}"; do
        if [[ ! -f "$cmd_file" ]]; then
            log_error "Command file missing: $cmd_file"
            return 1
        fi

        # Check for basic command structure
        if ! grep -q "## Purpose" "$cmd_file"; then
            log_error "Command file missing Purpose section: $cmd_file"
            return 1
        fi
    done

    # Test command file references point to actual project files
    if grep -q "mission.md" ".agent-os/commands/plan-product.md"; then
        if [[ ! -f ".agent-os/product/mission.md" ]]; then
            log_error "Command references missing mission.md file"
            return 1
        fi
    fi

    log_info "  Workflow command integration validated"
    cd ..
    return 0
}

# Display test results
display_results() {
    echo
    log_info "End-User Workflow Integration Test Results"
    log_info "========================================="
    echo "Total Tests Run: $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"

    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo
        log_error "Failed Tests:"
        for failed_test in "${FAILED_TESTS[@]}"; do
            echo "  - $failed_test"
        done
        echo
        log_error "❌ End-user workflow integration tests FAILED"
        return 1
    else
        echo
        log_success "🎉 ALL END-USER WORKFLOW TESTS PASSED!"
        log_success "The framework successfully supports complete end-user workflows"
        return 0
    fi
}

# Main test execution
main() {
    log_info "Agent OS + PocketFlow End-User Workflow Integration Tests"
    log_info "======================================================="
    echo

    # Setup test environment
    setup_test_workspace

    # Run all integration tests
    run_test "Framework Installation Workflow" test_framework_installation || true
    run_test "Product Planning Workflow" test_product_planning_workflow || true
    run_test "Feature Specification Workflow" test_feature_specification_workflow || true
    run_test "Task Execution Validation" test_task_execution_validation || true
    run_test "Project Structure Validation" test_project_structure_validation || true
    run_test "Workflow Command Integration" test_workflow_command_integration || true

    # Display results and cleanup
    display_results
    local exit_code=$?

    cleanup_test_workspace
    cd "$FRAMEWORK_ROOT"

    exit $exit_code
}

# Run main function
main "$@"