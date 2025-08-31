from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..db.database import get_db
from ..db.models import Player
from ..db.schemas import Player as PlayerSchema, PlayerCreate, PlayerUpdate
from ..services.player_service import PlayerService

router = APIRouter(tags=["roster"])

@router.get("/roster", response_model=List[PlayerSchema], summary="Get Dodgers Roster")
async def get_roster(
    db: Session = Depends(get_db),
    position: str = None,
    status: str = None
):
    """
    Get the complete Dodgers roster.
    
    - **position**: Filter by position (e.g., "P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF")
    - **status**: Filter by status (e.g., "Active", "Injured", "Suspended")
    """
    player_service = PlayerService(db)
    return player_service.get_players(position=position, status=status)

@router.get("/roster/{player_id}", response_model=PlayerSchema, summary="Get Player by ID")
async def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Get a specific player by their ID.
    """
    player_service = PlayerService(db)
    player = player_service.get_player_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return player

@router.post("/roster", response_model=PlayerSchema, status_code=status.HTTP_201_CREATED, summary="Add New Player")
async def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Add a new player to the Dodgers roster.
    """
    player_service = PlayerService(db)
    return player_service.create_player(player)

@router.put("/roster/{player_id}", response_model=PlayerSchema, summary="Update Player")
async def update_player(
    player_id: int, 
    player_update: PlayerUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing player's information.
    """
    player_service = PlayerService(db)
    player = player_service.update_player(player_id, player_update)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return player

@router.delete("/roster/{player_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Player")
async def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Remove a player from the roster.
    """
    player_service = PlayerService(db)
    success = player_service.delete_player(player_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return None

@router.get("/roster-sync-status", summary="Check Roster Sync Status")
async def check_sync_status(db: Session = Depends(get_db)):
    """
    Check if the roster needs to be synced (more than 24 hours since last update).
    """
    player_service = PlayerService(db)
    should_sync = player_service.should_sync_roster()
    player_count = db.query(Player).count()
    
    # Get last update time
    latest_player = db.query(Player).order_by(Player.last_updated.desc()).first()
    last_updated = latest_player.last_updated if latest_player else None
    
    return {
        "should_sync": should_sync,
        "player_count": player_count,
        "last_updated": last_updated,
        "message": "Roster needs sync" if should_sync else "Roster is up to date"
    }

@router.get("/roster-espn-test", summary="Test ESPN Parsing (No DB Changes)")
async def test_espn_parsing(db: Session = Depends(get_db)):
    """
    Test the ESPN parsing to see what data we can extract (no database changes).
    """
    player_service = PlayerService(db)
    players = player_service.sync_roster_from_espn()
    
    return {
        "message": "ESPN parsing test completed",
        "players_found": len(players),
        "players": players,  # Show all players
        "note": "This is test data only - no database changes were made"
    }

@router.post("/roster-espn-sync", summary="Sync ESPN Roster to Database")
async def sync_espn_roster(db: Session = Depends(get_db)):
    """
    Sync the current Dodgers roster from ESPN to the database.
    This will only sync if the roster hasn't been updated in the last 24 hours.
    """
    player_service = PlayerService(db)
    result = player_service.sync_roster_to_database()
    
    return result
