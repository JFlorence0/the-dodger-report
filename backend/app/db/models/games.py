from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey, Text, Float, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    espn_id = Column(String(50), unique=True, nullable=False)  # ESPN's event ID
    game_date = Column(Date, nullable=False, index=True)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    home_score = Column(Integer)
    away_score = Column(Integer)
    venue = Column(String(100))  # Keep for backward compatibility
    stadium_id = Column(Integer, ForeignKey("stadiums.id"))
    attendance = Column(Integer)
    game_time = Column(Time)  # Game start time
    game_duration = Column(String(20))  # e.g., "2:38"
    extra_innings = Column(Boolean, default=False)
    neutral_site = Column(Boolean, default=False)
    is_final = Column(Boolean, default=False)
    
    # Calculated fields
    day_of_week = Column(String(10))  # Monday, Tuesday, etc.
    is_night_game = Column(Boolean)  # True if game starts after 6 PM
    days_since_last_game = Column(Integer)  # Days since team's last game
    game_result = Column(String(5))  # W, L, or NULL for TBD
    
    # Weather data (if available)
    weather_temp = Column(Integer)  # in Fahrenheit
    weather_conditions = Column(String(100))
    wind_speed = Column(Integer)  # in mph
    wind_direction = Column(String(10))
    humidity = Column(Integer)  # percentage
    
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())

    # Relationships
    game_results = relationship("GameResult", back_populates="game", cascade="all, delete-orphan")
    player_stats = relationship("PlayerGameStats", back_populates="game", cascade="all, delete-orphan")
    stadium_info = relationship("Stadium", back_populates="games")

    def __repr__(self):
        return f"<Game(date='{self.game_date}', {self.away_team} @ {self.home_team}, {self.away_score}-{self.home_score})>"

class GameResult(Base):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    home_record_after = Column(String(20))  # e.g., "1-0"
    away_record_after = Column(String(20))  # e.g., "0-1"
    
    # Team performance stats (for home team)
    home_hits = Column(Integer)
    home_errors = Column(Integer)
    home_lob = Column(Integer)  # Left on base
    home_risp = Column(String(20))  # Runners in scoring position (e.g., "3-15")
    
    # Team performance stats (for away team)
    away_hits = Column(Integer)
    away_errors = Column(Integer)
    away_lob = Column(Integer)
    away_risp = Column(String(20))
    
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())

    # Relationships
    game = relationship("Game", back_populates="game_results")

    def __repr__(self):
        return f"<GameResult(game_id={self.game_id}, {self.away_team} {self.away_score} @ {self.home_team} {self.home_score})>"

class PlayerGameStats(Base):
    __tablename__ = "player_game_stats"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    
    # Game context
    is_starter = Column(Boolean, default=False)
    position = Column(String(20))  # Position played in this game
    
    # Batting stats
    at_bats = Column(Integer)
    runs = Column(Integer)
    hits = Column(Integer)
    doubles = Column(Integer)
    triples = Column(Integer)
    home_runs = Column(Integer)
    rbis = Column(Integer)
    walks = Column(Integer)
    strikeouts = Column(Integer)
    stolen_bases = Column(Integer)
    caught_stealing = Column(Integer)
    hit_by_pitch = Column(Integer)
    sacrifice_bunts = Column(Integer)
    sacrifice_flies = Column(Integer)
    left_on_base = Column(Integer)
    
    # Pitching stats
    innings_pitched = Column(Float)  # e.g., 6.2 for 6 2/3 innings
    hits_allowed = Column(Integer)
    runs_allowed = Column(Integer)
    earned_runs = Column(Integer)
    walks_allowed = Column(Integer)
    strikeouts_pitched = Column(Integer)
    home_runs_allowed = Column(Integer)
    wild_pitches = Column(Integer)
    balks = Column(Integer)
    hit_batters = Column(Integer)
    pitches_thrown = Column(Integer)
    strikes_thrown = Column(Integer)
    
    # Fielding stats
    putouts = Column(Integer)
    assists = Column(Integer)
    errors = Column(Integer)
    double_plays = Column(Integer)
    passed_balls = Column(Integer)  # For catchers
    
    # Game outcome
    win = Column(Boolean, default=False)
    loss = Column(Boolean, default=False)
    save = Column(Boolean, default=False)
    hold = Column(Boolean, default=False)
    blown_save = Column(Boolean, default=False)
    
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())

    # Relationships
    game = relationship("Game", back_populates="player_stats")
    player = relationship("Player", backref="game_stats")

    def __repr__(self):
        return f"<PlayerGameStats(game_id={self.game_id}, player_id={self.player_id}, position='{self.position}')>"
