from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as baselineragworkflow_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="BaselineRAGWorkflow API",
    description="Baseline generation snapshot for RAG pattern",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baselineragworkflow_router, prefix="/api/v1", tags=["BaselineRAGWorkflow"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}