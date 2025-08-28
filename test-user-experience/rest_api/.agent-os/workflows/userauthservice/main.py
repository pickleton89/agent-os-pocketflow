from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as userauthservice_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="UserAuthService API",
    description="REST API service for user management and authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userauthservice_router, prefix="/api/v1", tags=["UserAuthService"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}