from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import os

from .api import roster, games
from .db.database import engine, Base
from .core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the 2025 Los Angeles Dodgers season",
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(roster.router, prefix="/api/v1", tags=["roster"])
app.include_router(games.router, prefix="/api/v1", tags=["games"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}!",
        "version": settings.VERSION,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": {
            "roster": "/api/v1/roster",
            "roster_sync_status": "/api/v1/roster-sync-status",
            "roster_espn_test": "/api/v1/roster-espn-test",
            "roster_espn_sync": "/api/v1/roster-espn-sync",
            "games": "/api/v1/games",
            "games_sync_schedule": "/api/v1/games/sync-schedule",
            "games_record": "/api/v1/games/record",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dodger-report-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
