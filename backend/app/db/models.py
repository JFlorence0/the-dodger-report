from sqlalchemy import Column, Integer, String, Date, Float, Text
from sqlalchemy.sql import func
from .database import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    position = Column(String(20), nullable=False)
    jersey_number = Column(Integer)
    height = Column(String(10))  # e.g., "6'2\""
    weight = Column(Integer)  # in pounds
    birth_date = Column(Date)
    bats = Column(String(5))  # L, R, S (switch)
    throws = Column(String(5))  # L, R
    team = Column(String(50), default="Los Angeles Dodgers")
    status = Column(String(20), default="Active")  # Active, Injured, Suspended, etc.
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Player(name='{self.name}', position='{self.position}', jersey_number={self.jersey_number})>"
