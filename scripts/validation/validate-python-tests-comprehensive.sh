#!/bin/bash
# Python Test Comprehensive Suite (Framework repo)
set -e

# Resolve repo root to allow direct execution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../" && pwd)"
cd "$REPO_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

run_py() {
  local name="$1"; shift
  local cmd=("$@")
  log_info "Running comprehensive test: $name"
  if "${cmd[@]}"; then
    log_success "PASSED: $name"
  else
    log_error "FAILED: $name"
    return 1
  fi
}

main() {
  log_info "Starting Python comprehensive tests (framework)"

  # Full generation with dependencies (end-to-end within framework constraints)
  run_py "full generation + deps" uv run python pocketflow-tools/test_full_generation_with_dependencies.py

  # Dependency orchestrator comprehensive suite
  run_py "dependency orchestrator comprehensive" uv run python pocketflow-tools/test_dependency_orchestrator.py

  log_success "All comprehensive tests passed"
}

main "$@"
