from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as contentanalyzer_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="ContentAnalyzer API",
    description="Analyze content using document retrieval and LLM processing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contentanalyzer_router, prefix="/api/v1", tags=["ContentAnalyzer"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}