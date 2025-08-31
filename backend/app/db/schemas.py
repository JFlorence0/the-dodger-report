from pydantic import BaseModel
from typing import Optional
from datetime import date

class PlayerBase(BaseModel):
    name: str
    position: str
    jersey_number: Optional[int] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    birth_date: Optional[date] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    team: str = "Los Angeles Dodgers"
    status: str = "Active"

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    birth_date: Optional[date] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    team: Optional[str] = None
    status: Optional[str] = None
