from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .router import router as taskmanager_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="TaskManager API",
    description="Simple CRUD application for managing tasks",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(taskmanager_router, prefix="/api/v1", tags=["TaskManager"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}