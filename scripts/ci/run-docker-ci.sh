#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
IMAGE_NAME="${IMAGE_NAME:-agent-os-pocketflow-ci}" 
CONTAINER_NAME="${CONTAINER_NAME:-agent-os-pocketflow-ci-run}"
SHOULD_BUILD=true
NO_CACHE=false
MOUNT_ARTIFACTS=true

usage() {
  cat <<USAGE
Usage: ${0##*/} [options]

Build the Docker CI image and execute the framework CI workflow inside the container.

Options:
  --skip-build       Skip rebuilding the Docker image (use existing IMAGE_NAME)
  --no-cache         Build the Docker image without using cache
  --no-artifacts     Do not mount ci-artifacts directory from host
  --image NAME       Override the Docker image tag (default: ${IMAGE_NAME})
  -h, --help         Show this help message
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-build)
      SHOULD_BUILD=false
      shift
      ;;
    --no-cache)
      NO_CACHE=true
      shift
      ;;
    --no-artifacts)
      MOUNT_ARTIFACTS=false
      shift
      ;;
    --image)
      IMAGE_NAME="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ "$SHOULD_BUILD" == true ]]; then
  echo "[docker-ci] Building image ${IMAGE_NAME}"
  BUILD_ARGS=(-f "${REPO_ROOT}/docker/Dockerfile.ci")
  if [[ "$NO_CACHE" == true ]]; then
    BUILD_ARGS+=(--no-cache)
  fi
  BUILD_ARGS+=(-t "$IMAGE_NAME" "$REPO_ROOT")
  docker build "${BUILD_ARGS[@]}"
else
  echo "[docker-ci] Skipping image build"
fi

RUN_ARGS=(--rm --name "$CONTAINER_NAME" -e CI=true)

if [[ "$MOUNT_ARTIFACTS" == true ]]; then
  HOST_ARTIFACTS_DIR="${REPO_ROOT}/ci-artifacts/docker"
  mkdir -p "$HOST_ARTIFACTS_DIR"
  RUN_ARGS+=(-v "${HOST_ARTIFACTS_DIR}:/workspace/ci-artifacts")
fi

RUN_ARGS+=("$IMAGE_NAME")

echo "[docker-ci] Running container"
docker run "${RUN_ARGS[@]}"

echo "[docker-ci] Docker CI execution completed"
