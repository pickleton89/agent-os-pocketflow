#!/usr/bin/env bash
set -euo pipefail

# Phase 1 CLI smoke tests for pocketflow_tools.cli
# - Validates error messages/exit codes for missing/invalid YAML
# - Validates successful generation on example spec

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "[cli-smoke] Using Python: $(python3 -V 2>/dev/null || echo 'python3 not found')"

# Check PyYAML availability; do not install here to keep framework clean
set +e
python3 - << 'PY' 2>/dev/null
try:
    import yaml  # noqa: F401
    print("ok")
except Exception:
    raise SystemExit(1)
PY
set -e
if [ $? -ne 0 ]; then
  echo "[cli-smoke] SKIP: PyYAML not available. Install with: uv pip install pyyaml" >&2
  exit 0
fi

echo "[cli-smoke] PyYAML detected. Running tests..."

# 0) Help command
set +e
out=$(uv run python -m pocketflow_tools.cli --help 2>&1)
code=$?
set -e
echo "$out" | rg -n "Generate PocketFlow workflows from specifications" >/dev/null || {
  echo "[cli-smoke] FAIL: Help message mismatch"; echo "$out"; exit 1; }
test "$code" -eq 0 || { echo "[cli-smoke] FAIL: Help should return zero"; exit 1; }

# 1) Missing file
set +e
out=$(uv run python -m pocketflow_tools.cli --spec does-not-exist.yaml 2>&1)
code=$?
set -e
echo "$out" | rg -n "Error: Specification file not found" >/dev/null || {
  echo "[cli-smoke] FAIL: Missing file message mismatch"; echo "$out"; exit 1; }
test "$code" -ne 0 || { echo "[cli-smoke] FAIL: Missing file should return non-zero"; exit 1; }

# 2) Invalid YAML
tmp_yaml="$(mktemp -t invalid-spec.XXXXXX.yaml)"
printf 'name: "BadSpec"\npattern: [unterminated\n' > "$tmp_yaml"
set +e
out=$(uv run python -m pocketflow_tools.cli --spec "$tmp_yaml" 2>&1)
code=$?
set -e
rm -f "$tmp_yaml"
echo "$out" | rg -n "Error: Invalid YAML" >/dev/null || {
  echo "[cli-smoke] FAIL: Invalid YAML message mismatch"; echo "$out"; exit 1; }
test "$code" -ne 0 || { echo "[cli-smoke] FAIL: Invalid YAML should return non-zero"; exit 1; }

# 3) Valid generation (agent example)
outdir=".agent-os/workflows/cli-smoke"
rm -rf "$outdir" || true
uv run python -m pocketflow_tools.cli \
  --spec framework-tools/examples/agent-workflow-spec.yaml \
  --output "$outdir"

expected=(
  "docs/design.md"
  "schemas/models.py"
  "nodes.py"
  "flow.py"
  "main.py"
  "router.py"
  "utils"
  "tests"
  "pyproject.toml"
  "requirements.txt"
  "README.md"
  ".gitignore"
)

# Find the generated project directory (should be exactly one)
proj_dirs=($(find "$outdir" -maxdepth 1 -type d ! -name "$(basename "$outdir")"))
if [ ${#proj_dirs[@]} -ne 1 ]; then
    echo "[cli-smoke] FAIL: Expected exactly 1 project directory, found ${#proj_dirs[@]}"; exit 1
fi
proj_dir="${proj_dirs[0]}"
test -d "$proj_dir" || { echo "[cli-smoke] FAIL: output project dir missing: $proj_dir"; exit 1; }

for f in "${expected[@]}"; do
  if [ ! -e "$proj_dir/$f" ]; then
    echo "[cli-smoke] FAIL: Missing expected output: $f"; exit 1
  fi
done

echo "[cli-smoke] PASS: CLI smoke tests completed"
