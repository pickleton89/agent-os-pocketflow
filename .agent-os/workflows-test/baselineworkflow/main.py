from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as baselineworkflow_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="BaselineWorkflow API",
    description="Test workflow",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baselineworkflow_router, prefix="/api/v1", tags=["BaselineWorkflow"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}