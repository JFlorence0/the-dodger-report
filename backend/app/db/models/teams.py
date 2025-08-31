from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from ..database import Base

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    city = Column(String(100), nullable=False)
    state = Column(String(50))
    division = Column(String(50))  # e.g., "NL West", "AL East"
    league = Column(String(20))    # e.g., "NL", "AL"
    founded = Column(Integer)      # Year founded
    description = Column(Text)     # Team description/history
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Team(name='{self.name}', city='{self.city}', division='{self.division}')>"
