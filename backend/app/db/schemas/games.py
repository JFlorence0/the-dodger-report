from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

class GameBase(BaseModel):
    espn_id: str
    game_date: date
    home_team: str
    away_team: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    venue: Optional[str] = None
    attendance: Optional[int] = None
    game_time: Optional[time] = None
    game_duration: Optional[str] = None
    extra_innings: bool = False
    neutral_site: bool = False
    is_final: bool = False
    game_result: Optional[str] = None
    day_of_week: Optional[str] = None
    is_night_game: Optional[bool] = None
    days_since_last_game: Optional[int] = None
    weather_temp: Optional[int] = None
    weather_conditions: Optional[str] = None
    wind_speed: Optional[int] = None
    wind_direction: Optional[str] = None
    humidity: Optional[int] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class GameUpdate(BaseModel):
    espn_id: Optional[str] = None
    game_date: Optional[date] = None
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    venue: Optional[str] = None
    attendance: Optional[int] = None
    game_time: Optional[time] = None
    game_duration: Optional[str] = None
    extra_innings: Optional[bool] = None
    neutral_site: Optional[bool] = None
    is_final: Optional[bool] = None
    game_result: Optional[str] = None
    day_of_week: Optional[str] = None
    is_night_game: Optional[bool] = None
    days_since_last_game: Optional[int] = None
    weather_temp: Optional[int] = None
    weather_conditions: Optional[str] = None
    wind_speed: Optional[int] = None
    wind_direction: Optional[str] = None
    humidity: Optional[int] = None

class GameResultBase(BaseModel):
    game_id: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    home_record_after: Optional[str] = None
    away_record_after: Optional[str] = None
    home_hits: Optional[int] = None
    home_errors: Optional[int] = None
    home_lob: Optional[int] = None
    home_risp: Optional[str] = None
    away_hits: Optional[int] = None
    away_errors: Optional[int] = None
    away_lob: Optional[int] = None
    away_risp: Optional[str] = None

class GameResultCreate(GameResultBase):
    pass

class GameResult(GameResultBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class GameResultUpdate(BaseModel):
    game_id: Optional[int] = None
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    home_record_after: Optional[str] = None
    away_record_after: Optional[str] = None
    home_hits: Optional[int] = None
    home_errors: Optional[int] = None
    home_lob: Optional[int] = None
    home_risp: Optional[str] = None
    away_hits: Optional[int] = None
    away_errors: Optional[int] = None
    away_lob: Optional[int] = None
    away_risp: Optional[str] = None

class PlayerGameStatsBase(BaseModel):
    game_id: int
    player_id: int
    is_starter: bool = False
    position: Optional[str] = None
    
    # Batting stats
    at_bats: Optional[int] = None
    runs: Optional[int] = None
    hits: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    home_runs: Optional[int] = None
    rbis: Optional[int] = None
    walks: Optional[int] = None
    strikeouts: Optional[int] = None
    stolen_bases: Optional[int] = None
    caught_stealing: Optional[int] = None
    hit_by_pitch: Optional[int] = None
    sacrifice_bunts: Optional[int] = None
    sacrifice_flies: Optional[int] = None
    left_on_base: Optional[int] = None
    
    # Pitching stats
    innings_pitched: Optional[float] = None
    hits_allowed: Optional[int] = None
    runs_allowed: Optional[int] = None
    earned_runs: Optional[int] = None
    walks_allowed: Optional[int] = None
    strikeouts_pitched: Optional[int] = None
    home_runs_allowed: Optional[int] = None
    wild_pitches: Optional[int] = None
    balks: Optional[int] = None
    hit_batters: Optional[int] = None
    pitches_thrown: Optional[int] = None
    strikes_thrown: Optional[int] = None
    
    # Fielding stats
    putouts: Optional[int] = None
    assists: Optional[int] = None
    errors: Optional[int] = None
    double_plays: Optional[int] = None
    passed_balls: Optional[int] = None
    
    # Game outcome
    win: bool = False
    loss: bool = False
    save: bool = False
    hold: bool = False
    blown_save: bool = False

class PlayerGameStatsCreate(PlayerGameStatsBase):
    pass

class PlayerGameStats(PlayerGameStatsBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class PlayerGameStatsUpdate(BaseModel):
    game_id: Optional[int] = None
    player_id: Optional[int] = None
    is_starter: Optional[bool] = None
    position: Optional[str] = None
    
    # Batting stats
    at_bats: Optional[int] = None
    runs: Optional[int] = None
    hits: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    home_runs: Optional[int] = None
    rbis: Optional[int] = None
    walks: Optional[int] = None
    strikeouts: Optional[int] = None
    stolen_bases: Optional[int] = None
    caught_stealing: Optional[int] = None
    hit_by_pitch: Optional[int] = None
    sacrifice_bunts: Optional[int] = None
    sacrifice_flies: Optional[int] = None
    left_on_base: Optional[int] = None
    
    # Pitching stats
    innings_pitched: Optional[float] = None
    hits_allowed: Optional[int] = None
    runs_allowed: Optional[int] = None
    earned_runs: Optional[int] = None
    walks_allowed: Optional[int] = None
    strikeouts_pitched: Optional[int] = None
    home_runs_allowed: Optional[int] = None
    wild_pitches: Optional[int] = None
    balks: Optional[int] = None
    hit_batters: Optional[int] = None
    pitches_thrown: Optional[int] = None
    strikes_thrown: Optional[int] = None
    
    # Fielding stats
    putouts: Optional[int] = None
    assists: Optional[int] = None
    errors: Optional[int] = None
    double_plays: Optional[int] = None
    passed_balls: Optional[int] = None
    
    # Game outcome
    win: Optional[bool] = None
    loss: Optional[bool] = None
    save: Optional[bool] = None
    hold: Optional[bool] = None
    blown_save: Optional[bool] = None
