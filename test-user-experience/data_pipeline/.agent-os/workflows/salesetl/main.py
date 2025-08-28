from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as salesetl_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="SalesETL API",
    description="Data processing pipeline for sales analytics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salesetl_router, prefix="/api/v1", tags=["SalesETL"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}