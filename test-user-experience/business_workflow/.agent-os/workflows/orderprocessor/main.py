from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as orderprocessor_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="OrderProcessor API",
    description="Complex business workflow for e-commerce orders",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orderprocessor_router, prefix="/api/v1", tags=["OrderProcessor"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}