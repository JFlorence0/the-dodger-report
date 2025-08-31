from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date

from ..db.models import Player
from ..db.schemas import PlayerCreate, PlayerUpdate

class PlayerService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_players(self, position: Optional[str] = None, status: Optional[str] = None) -> List[Player]:
        """
        Get all players with optional filtering by position and status.
        """
        query = self.db.query(Player)
        
        if position:
            query = query.filter(Player.position == position)
        
        if status:
            query = query.filter(Player.status == status)
        
        return query.order_by(Player.jersey_number, Player.name).all()
    
    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """
        Get a player by their ID.
        """
        return self.db.query(Player).filter(Player.id == player_id).first()
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """
        Get a player by their name.
        """
        return self.db.query(Player).filter(Player.name == name).first()
    
    def create_player(self, player: PlayerCreate) -> Player:
        """
        Create a new player.
        """
        db_player = Player(**player.dict())
        self.db.add(db_player)
        self.db.commit()
        self.db.refresh(db_player)
        return db_player
    
    def update_player(self, player_id: int, player_update: PlayerUpdate) -> Optional[Player]:
        """
        Update an existing player.
        """
        db_player = self.get_player_by_id(player_id)
        if not db_player:
            return None
        
        update_data = player_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_player, field, value)
        
        self.db.commit()
        self.db.refresh(db_player)
        return db_player
    
    def delete_player(self, player_id: int) -> bool:
        """
        Delete a player.
        """
        db_player = self.get_player_by_id(player_id)
        if not db_player:
            return False
        
        self.db.delete(db_player)
        self.db.commit()
        return True
    
    def get_players_by_position(self, position: str) -> List[Player]:
        """
        Get all players at a specific position.
        """
        return self.db.query(Player).filter(Player.position == position).order_by(Player.jersey_number).all()
    
    def get_active_players(self) -> List[Player]:
        """
        Get all active players.
        """
        return self.db.query(Player).filter(Player.status == "Active").order_by(Player.jersey_number, Player.name).all()
    
    def search_players(self, search_term: str) -> List[Player]:
        """
        Search players by name (case-insensitive).
        """
        return self.db.query(Player).filter(Player.name.ilike(f"%{search_term}%")).all()
