from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import router as testcontentanalyzer_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="TestContentAnalyzer API",
    description="Test content analyzer using RAG pattern for validation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    testcontentanalyzer_router, prefix="/api/v1", tags=["TestContentAnalyzer"]
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
