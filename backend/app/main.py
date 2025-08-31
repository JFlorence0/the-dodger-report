from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from .api import roster
from .db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dodger Report API",
    description="API for the 2025 Los Angeles Dodgers season",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(roster.router, prefix="/api/v1", tags=["roster"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Dodger Report API!",
        "version": "1.0.0",
        "endpoints": {
            "roster": "/api/v1/roster",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dodger-report-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
