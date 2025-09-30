#!/usr/bin/env bash
# scripts/measure-coverage.sh
# Measures test coverage for Agent OS + PocketFlow framework code

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MIN_COVERAGE=${MIN_COVERAGE:-60}
GENERATE_HTML=${GENERATE_HTML:-true}

echo -e "${BLUE}📊 Measuring test coverage for framework code...${NC}"
echo ""

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv not found. Please install uv first.${NC}"
    exit 1
fi

# Install dev dependencies if needed
echo -e "${BLUE}Ensuring dev dependencies are installed...${NC}"
uv pip install -e ".[dev]" --quiet

# Clean previous coverage data
echo -e "${BLUE}Cleaning previous coverage data...${NC}"
rm -f .coverage
rm -rf htmlcov/

# Run tests with coverage
echo -e "${BLUE}Running tests with coverage measurement...${NC}"
echo ""

# Run coverage on framework-tools and pocketflow_tools
if uv run coverage run -m pytest framework-tools/ pocketflow_tools/ -v; then
    echo ""
    echo -e "${GREEN}✅ Tests completed successfully${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Some tests failed, but continuing with coverage report...${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}                  COVERAGE REPORT${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Generate text report
uv run coverage report --show-missing

# Get coverage percentage
COVERAGE=$(uv run coverage report --format=total)

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Generate HTML report if requested
if [ "$GENERATE_HTML" = "true" ]; then
    echo ""
    echo -e "${BLUE}Generating HTML coverage report...${NC}"
    uv run coverage html
    echo -e "${GREEN}✅ HTML report generated: ${BLUE}htmlcov/index.html${NC}"
fi

echo ""

# Check if coverage meets minimum threshold
# Using awk for portability (avoids bc dependency)
if awk -v cov="$COVERAGE" -v min="$MIN_COVERAGE" 'BEGIN { exit (cov >= min) ? 0 : 1 }'; then
    echo -e "${GREEN}✅ Coverage ${COVERAGE}% meets minimum threshold of ${MIN_COVERAGE}%${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Coverage ${COVERAGE}% is below minimum threshold of ${MIN_COVERAGE}%${NC}"
    echo -e "${YELLOW}   Goals: Phase 1 (baseline), Phase 2 (60%), Phase 3 (70%), Phase 4 (80%)${NC}"
    exit 1
fi
