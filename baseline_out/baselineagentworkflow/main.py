from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as baselineagentworkflow_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="BaselineAGENTWorkflow API",
    description="Baseline generation snapshot for AGENT pattern",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baselineagentworkflow_router, prefix="/api/v1", tags=["BaselineAGENTWorkflow"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}