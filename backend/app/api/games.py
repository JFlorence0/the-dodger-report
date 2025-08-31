from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..db.database import get_db
from ..db.models import Game, GameResult
from ..db.schemas import Game as GameSchema, GameResult as GameResultSchema
from ..services.game_service import GameService
from ..services.stadium_service import StadiumService

router = APIRouter(tags=["games"])

@router.get("/games", response_model=List[GameSchema], summary="Get Dodgers Games")
async def get_dodgers_games(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """
    Get recent Dodgers games.
    
    - **limit**: Maximum number of games to return (default: 10)
    """
    game_service = GameService(db)
    return game_service.get_dodgers_games(limit=limit)

@router.get("/games/record", summary="Get Dodgers Record")
async def get_dodgers_record(db: Session = Depends(get_db)):
    """
    Get current Dodgers record and recent performance.
    """
    game_service = GameService(db)
    return game_service.get_dodger_record()

@router.post("/games/sync-schedule", summary="Sync Dodgers Schedule from ESPN")
async def sync_dodgers_schedule(db: Session = Depends(get_db)):
    """
    Sync the Dodgers' current season schedule from ESPN.
    This will fetch all games and update the database.
    """
    game_service = GameService(db)
    result = game_service.sync_dodgers_schedule()
    
    if not result["synced"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["reason"]
        )
    
    return result

@router.post("/games/sync-results", summary="Sync Game Results from ESPN")
async def sync_game_results(db: Session = Depends(get_db)):
    """
    Sync actual game results (scores, final status) from ESPN scoreboard.
    This updates existing games with real scores and final status.
    """
    game_service = GameService(db)
    result = game_service.sync_game_results()
    
    if not result["synced"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["reason"]
        )
    
    return result

@router.post("/games/fix-existing-results", summary="Fix Existing Game Results")
async def fix_existing_game_results(db: Session = Depends(get_db)):
    """
    Calculate and update game results for existing games that already have scores.
    This is a one-time fix for games we already have, separate from ESPN sync.
    """
    game_service = GameService(db)
    result = game_service.calculate_existing_game_results()
    
    if not result["synced"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["reason"]
        )
    
    return result

@router.post("/games/sync-weather", summary="Sync Weather Data for Existing Games")
async def sync_weather_data(db: Session = Depends(get_db)):
    """
    Sync weather data for existing games that don't have weather information.
    """
    game_service = GameService(db)
    result = game_service.sync_weather_for_existing_games()
    
    if not result["synced"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["reason"]
        )
    
    return result



@router.get("/games/{espn_id}", response_model=GameSchema, summary="Get Game by ESPN ID")
async def get_game_by_espn_id(
    espn_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific game by its ESPN ID.
    
    - **espn_id**: ESPN's event ID for the game
    """
    game_service = GameService(db)
    game = game_service.get_game_by_espn_id(espn_id)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ESPN ID {espn_id} not found"
        )
    
    return game

@router.get("/games/{espn_id}/result", response_model=GameResultSchema, summary="Get Game Result")
async def get_game_result(
    espn_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the result for a specific game.
    
    - **espn_id**: ESPN's event ID for the game
    """
    game_service = GameService(db)
    game = game_service.get_game_by_espn_id(espn_id)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ESPN ID {espn_id} not found"
        )
    
    # Get game result for this game
    game_result = db.query(GameResult).filter(
        GameResult.game_id == game.id
    ).first()
    
    if not game_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No result found for game {espn_id}"
        )
    
    return game_result

@router.get("/games/debug/espn-schedule", summary="Debug ESPN Schedule Data")
async def debug_espn_schedule(db: Session = Depends(get_db)):
    """
    Debug endpoint to inspect what ESPN is sending us.
    This helps identify why we might be getting duplicate games.
    """
    game_service = GameService(db)
    return game_service.debug_espn_schedule()

@router.get("/games/debug/espn-scoreboard", summary="Debug ESPN Scoreboard Data")
async def debug_espn_scoreboard(db: Session = Depends(get_db)):
    """
    Debug endpoint to inspect what ESPN scoreboard API is sending us.
    This helps identify why game results sync isn't working.
    """
    game_service = GameService(db)
    return game_service.debug_espn_scoreboard()

@router.post("/games/seed-stadiums", summary="Seed MLB Stadiums")
async def seed_stadiums(db: Session = Depends(get_db)):
    """
    Seed the database with current MLB stadiums and their coordinates.
    This is a one-time setup to populate stadium data.
    """
    stadium_service = StadiumService(db)
    result = stadium_service.seed_mlb_stadiums()
    return result
