from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PlayerPositionBase(BaseModel):
    position: str
    is_primary: bool = False

class PlayerPositionCreate(PlayerPositionBase):
    pass

class PlayerPosition(PlayerPositionBase):
    id: int
    player_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class PlayerBase(BaseModel):
    name: str
    uniform_number: int
    height: Optional[str] = None
    weight: Optional[int] = None
    birth_date: Optional[date] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    team: str = "Los Angeles Dodgers"
    status: str = "Active"

class PlayerCreate(PlayerBase):
    positions: List[str]  # List of position strings like ["SS", "2B"]

class Player(PlayerBase):
    id: int
    positions: List[PlayerPosition] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_updated: Optional[str] = None
    
    class Config:
        from_attributes = True

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    uniform_number: Optional[int] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    birth_date: Optional[date] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    team: Optional[str] = None
    status: Optional[str] = None
    last_updated: Optional[str] = None
