#!/usr/bin/env bash
# repo-detect.sh
# Detects whether this checkout is the Framework repo or an end-user Project repo
# and provides small helpers for gating validation checks.

# Returns: "framework" or "project"
detect_repo_type() {
  # Allow explicit override via environment
  if [[ -n "${REPO_TYPE:-}" ]]; then
    echo "$REPO_TYPE"
    return 0
  fi

  # Framework heuristics
  if [[ -d "pocketflow_tools" ]]; then
    echo "framework"; return 0
  fi
  if [[ -f "CLAUDE.md" ]] && grep -qE 'This IS the Framework' "CLAUDE.md" 2>/dev/null; then
    echo "framework"; return 0
  fi

  # Project heuristics
  if [[ -d ".agent-os/workflows" ]]; then
    # If workflows has at least one subdirectory, treat as project
    if find .agent-os/workflows -mindepth 1 -maxdepth 1 -type d | read -r _; then
      echo "project"; return 0
    fi
  fi
  if [[ -f "docs/design.md" ]] || [[ -d "tests" ]]; then
    echo "project"; return 0
  fi

  # Default to framework per repository principle
  echo "framework"
}

is_framework() { [[ "$(detect_repo_type)" == "framework" ]]; }
is_project()   { [[ "$(detect_repo_type)" == "project" ]]; }

# Convenience helpers for tests
skip_if_framework() {
  local reason="$1"
  if is_framework; then
    echo "⏭️  SKIP (framework mode): ${reason}"
    return 0
  fi
  return 1
}

skip_if_project() {
  local reason="$1"
  if is_project; then
    echo "⏭️  SKIP (project mode): ${reason}"
    return 0
  fi
  return 1
}

print_repo_type() {
  local rt
  rt="$(detect_repo_type)"
  echo "Repo Type: ${rt}"
}

