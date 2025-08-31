from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..db.database import get_db
from ..db.models import Player
from ..db.schemas import Player as PlayerSchema, PlayerCreate, PlayerUpdate
from ..services.player_service import PlayerService

router = APIRouter()

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
