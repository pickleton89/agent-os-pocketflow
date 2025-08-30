# Technical Stack

> Last Updated: 2025-08-30
> Version: 1.0.0

## Core Technologies

- **Programming Language:** Python 3.12+
- **Application Framework:** FastAPI
- **Data Validation:** Pydantic
- **Package Manager:** uv
- **Linting & Formatting:** Ruff
- **Type Checking:** mypy/ty
- **Testing Framework:** pytest
- **Workflow Framework:** PocketFlow (latest)

## Data & Storage

- **Database System:** SQLite (development), PostgreSQL (production)
- **Vector Store:** ChromaDB (for content embeddings and similarity search)
- **Cache:** Redis (for performance optimization)

## AI & Machine Learning

- **LLM Providers:** 
  - OpenAI GPT-4 (primary content analysis)
  - Anthropic Claude (sentiment analysis)
  - Google Gemini (competitive analysis)
- **ML Libraries:** scikit-learn, transformers, langchain
- **Content Processing:** spaCy, nltk, beautifulsoup4

## Frontend & API

- **Frontend Framework:** React.js with TypeScript
- **API Documentation:** FastAPI automatic OpenAPI/Swagger
- **Authentication:** JWT with FastAPI Security
- **API Rate Limiting:** slowapi

## Infrastructure & Deployment

- **Application Hosting:** Digital Ocean Droplets / AWS EC2
- **Database Hosting:** Digital Ocean Managed Database / AWS RDS
- **Deployment Solution:** Docker with docker-compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Logging:** structured logging with loguru

## Development Tools

- **Code Repository:** GitHub
- **Environment Management:** uv for virtual environments and dependency management
- **Code Quality:** pre-commit hooks with Ruff and mypy
- **Documentation:** MkDocs with material theme

## Project Structure

The project follows the universal PocketFlow architecture:

```
testcontentanalyzer/
├── main.py              # FastAPI app entry point
├── nodes.py             # PocketFlow nodes for content analysis
├── flow.py              # PocketFlow flows for processing workflows
├── schemas/             # Pydantic models
│   ├── __init__.py
│   ├── requests.py      # API request models
│   └── responses.py     # API response models
├── utils/               # Custom utilities
│   ├── __init__.py
│   ├── content_analyzer.py
│   ├── sentiment_engine.py
│   └── competitive_intelligence.py
├── docs/
│   └── design.md        # MANDATORY design document
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_endpoints.py
│   └── test_flows.py
├── pyproject.toml       # uv package management
├── uv.lock             # dependency lockfile
├── .gitignore
└── README.md
```

## Architecture Notes

- **PocketFlow Integration:** All content processing workflows implemented as PocketFlow flows with specialized nodes
- **Design-First Approach:** `docs/design.md` must be completed before any implementation begins
- **Type Safety:** Full Pydantic validation at API boundaries and internal data structures
- **Scalability:** ChromaDB enables semantic search and content similarity analysis
- **Modularity:** Clear separation between API layer (FastAPI), business logic (PocketFlow), and utilities