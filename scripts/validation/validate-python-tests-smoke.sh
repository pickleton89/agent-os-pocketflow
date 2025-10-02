#!/bin/bash
# Python Test Smoke Suite (Framework repo)
set -e

CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"
UV_RUN=("env" "UV_CACHE_DIR=${CACHE_DIR}" "UV_NO_SYNC=1" "uv" "run" "--no-sync")

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
  log_info "Running smoke test: $name"
  if "${cmd[@]}"; then
    log_success "PASSED: $name"
  else
    log_error "FAILED: $name"
    return 1
  fi
}

main() {
  log_info "Starting Python smoke tests (framework)"

  # Run generator smoke
  run_py "generator smoke" "${UV_RUN[@]}" python pocketflow_tools/generators/test_config_integration.py

  # Run dependency orchestrator smoke
  run_py "dependency orchestrator smoke" "${UV_RUN[@]}" python framework-tools/test_dependency_orchestrator.py

  log_success "All smoke tests passed"
}

main "$@"
