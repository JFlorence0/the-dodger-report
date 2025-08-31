from sqlalchemy import Column, Integer, String, Float, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Stadium(Base):
    __tablename__ = "stadiums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), default="USA")
    
    # Coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Stadium details
    capacity = Column(Integer)
    surface_type = Column(String(50))  # Grass, Turf, etc.
    roof_type = Column(String(50))    # Open, Retractable, Fixed
    
    # Team associations
    primary_team = Column(String(100))  # Primary team that plays here
    league = Column(String(10), default="MLB")
    
    # Status
    is_active = Column(Boolean, default=True)
    opened_year = Column(Integer)
    
    # Metadata
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())

    # Relationships
    games = relationship("Game", back_populates="stadium_info")

    def __repr__(self):
        return f"<Stadium(name='{self.name}', city='{self.city}', lat={self.latitude}, lon={self.longitude})>"

    @property
    def coordinates(self):
        """Return coordinates as a dictionary."""
        return {"lat": self.latitude, "lon": self.longitude}
    
    @property
    def full_location(self):
        """Return full location string."""
        return f"{self.city}, {self.state}, {self.country}"
