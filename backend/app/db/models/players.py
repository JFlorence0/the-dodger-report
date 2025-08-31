from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    uniform_number = Column(Integer, nullable=False)
    height = Column(String(10))  # e.g., "6'2\""
    weight = Column(Integer)  # in pounds
    birth_date = Column(Date)
    bats = Column(String(5))  # L, R, S (switch)
    throws = Column(String(5))  # L, R
    team = Column(String(50), default="Los Angeles Dodgers")
    status = Column(String(20), default="Active")  # Active, Injured, Suspended, etc.
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())
    last_updated = Column(String, server_default=func.now())  # When roster data was last synced
    
    # Unique constraint: team + uniform_number must be unique
    __table_args__ = (
        UniqueConstraint('team', 'uniform_number', name='uq_team_uniform_number'),
    )
    
    # Relationship to positions
    positions = relationship("PlayerPosition", back_populates="player", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Player(name='{self.name}', uniform_number={self.uniform_number}, team='{self.team}')>"

class PlayerPosition(Base):
    __tablename__ = "player_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    position = Column(String(20), nullable=False)  # e.g., "SS", "2B", "LF", "DH"
    is_primary = Column(Boolean, default=False)  # True if this is their main position
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())
    
    # Relationship back to player
    player = relationship("Player", back_populates="positions")
    
    def __repr__(self):
        return f"<PlayerPosition(player_id={self.player_id}, position='{self.position}', is_primary={self.is_primary})>"
