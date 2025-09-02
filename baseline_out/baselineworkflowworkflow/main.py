from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as baselineworkflowworkflow_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="BaselineWORKFLOWWorkflow API",
    description="Baseline generation snapshot for WORKFLOW pattern",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baselineworkflowworkflow_router, prefix="/api/v1", tags=["BaselineWORKFLOWWorkflow"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}