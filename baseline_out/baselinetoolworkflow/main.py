from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as baselinetoolworkflow_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="BaselineTOOLWorkflow API",
    description="Baseline generation snapshot for TOOL pattern",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baselinetoolworkflow_router, prefix="/api/v1", tags=["BaselineTOOLWorkflow"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}