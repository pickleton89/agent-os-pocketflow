#!/usr/bin/env bash
set -euo pipefail

cd /workspace

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

log "Starting Docker CI workflow"

log "Running ruff lint"
uv run ruff check .

log "Running ruff format check"
uv run ruff format --check .

log "Running master validation suite"
bash ./scripts/run-all-tests.sh

log "Running generator regression tests"
uv run python framework-tools/test-generator.py
uv run python framework-tools/test_full_generation_with_dependencies.py

log "Executing Phase 4 optimization tests"
python3 claude-code/testing/test-phase4-optimization.py --json --cleanup

log "Executing Phase 4 CI suite"
./scripts/ci/run-phase4-ci-tests.sh --json --cleanup --all --verbose

log "Docker CI workflow completed successfully"
