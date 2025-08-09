# Tech Stack

> Version: 1.3.0
> Last Updated: 2025-07-21

## Context

This file is part of the Agent OS standards system. These global tech stack defaults are referenced by all product codebases when initializing new projects. Individual projects may override these choices in their `.agent-os/product/tech-stack.md` file.

## Core Technologies

## Application Framework

- **Primary Web Framework:** FastAPI  
  - Purpose: Serves MCP API endpoints, integrates with PocketFlow orchestration layer.  
- **Workflow Orchestration Framework:** PocketFlow (latest)  
  - Purpose: Manages Node/Flow execution for LLM-assisted interactions.
- **Language:** Python 3.12+

### AI/LLM Framework
- **Framework:** PocketFlow (latest)
- **Purpose:** LLM workflow orchestration

### Message Queue/Coordination
- **Framework:** FastMCP
- **Purpose:** Multi-agent messaging and coordination

## Database

### Orchestration State Storage
- **Store:** PocketFlow SharedStore (in-memory, with optional persistent backend)
- **Purpose:** Maintains agent workflow state, cached API responses, and metadata during and across flows.

### Vector Store
- **Database:** ChromaDB
- **Purpose:** Embeddings and semantic search

### Relational Store
- **Database:** SQLite (or similar file-based)
- **Purpose:** Structured data and metadata

## Python Libraries

### Data Manipulation & Analysis
- **Libraries:** Pandas, NumPy
- **Purpose:** Data structures and operations

### Visualization
- **Libraries:** Matplotlib, Seaborn
- **Purpose:** Data visualization

### API & Data Validation
- **Libraries:** Pydantic, FastAPI
- **Purpose:** Data validation and API building

### External API Clients
- **Library:** Custom API clients as needed
- **Purpose:** Interfacing with external services and APIs

## Development Tools

### Testing Framework
- **Framework:** Pytest

### Package Management
- **Tool:** uv

### Code Quality
- **Linting/Formatting:** Ruff
- **Type Checking:** mypy (via `uvx ty check`)

## Version Control
- **System:** Git
- **Hosting:** GitHub

## CI/CD
- **Platform:** GitHub Actions (linting, tests, build before deploy)

## Environment Variables
- **Tool:** python-dotenv

## Frontend
- **Framework:** None (API only)

## Hosting/Deployment
- **Platform:** Local development
- **Production:** TBD

## Observability

- **Logging Framework:** 
  - `structlog` for structured, JSON-formatted logs compatible with modern log aggregation tools.
  - Integrated with FastAPI's logging middleware for request/response tracking.
  - PocketFlow Node-level logging enabled for step-by-step workflow tracing.

- **Error Tracking:**
  - Sentry SDK for Python to capture exceptions from both FastAPI endpoints and PocketFlow execution flows.

- **Metrics & Monitoring:**
  - Prometheus-compatible metrics via `prometheus-fastapi-instrumentator` for endpoint latency, request counts, and error rates.
  - Optional PocketFlow custom metrics node for workflow timing and throughput.

- **Tracing:**
  - OpenTelemetry instrumentation for distributed tracing across MCP server requests, API calls, and internal PocketFlow nodes.

- **Log Retention & Storage:**
  - Development: Local log files (rotated daily).

---
