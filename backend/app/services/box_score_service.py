import requests
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from ..core.config import settings
from ..db.models.games import Game, PlayerGameStats
from ..db.models.players import Player
import re

class BoxScoreService:
    """
    Service for fetching and parsing ESPN box score data.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.espn_base_url = settings.ESPN_BASE_URL
    
    def fetch_game_box_score(self, espn_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch box score data for a specific game from ESPN.
        """
        try:
            # ESPN scoreboard endpoint - this is what we know works
            url = f"{self.espn_base_url}/scoreboard"
            print(f"Fetching from ESPN endpoint: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # Find the specific game in events
            events = data.get('events', [])
            target_event = None
            
            for event in events:
                if event.get('id') == espn_id:
                    print(f"Found game in events: {espn_id}")
                    target_event = event
                    break
            
            if not target_event:
                print(f"Game with ESPN ID {espn_id} not found in scoreboard")
                return None
            
            return target_event
            
        except Exception as e:
            print(f"Error fetching box score for game {espn_id}: {e}")
            return None
    
    def parse_player_batting_stats(self, competitor_data: Dict[str, Any], game_id: int) -> List[PlayerGameStats]:
        """
        Parse batting statistics for all players in a game.
        For now, this is a placeholder since ESPN's public API doesn't provide detailed player stats.
        We'll need to either:
        1. Use a different data source (MLB Stats API when approved)
        2. Scrape the ESPN website box scores
        3. Find an alternative free API
        """
        print("Note: ESPN's public API doesn't provide detailed player statistics")
        print("This method is a placeholder for future implementation")
        return []
    
    def parse_player_pitching_stats(self, competitor_data: Dict[str, Any], game_id: int) -> List[PlayerGameStats]:
        """
        Parse pitching statistics for all players in a game.
        For now, this is a placeholder since ESPN's public API doesn't provide detailed player stats.
        """
        print("Note: ESPN's public API doesn't provide detailed player statistics")
        print("This method is a placeholder for future implementation")
        return []
    
    def _parse_innings(self, ip_string: str) -> float:
        """
        Parse innings pitched string (e.g., "6.2" for 6 2/3 innings).
        """
        try:
            if not ip_string:
                return 0.0
            
            # Handle cases like "6.2" (6 2/3 innings)
            if '.' in ip_string:
                parts = ip_string.split('.')
                whole = int(parts[0])
                fraction = int(parts[1])
                
                # Convert fraction to decimal (e.g., 2 = 0.67, 1 = 0.33)
                if fraction == 1:
                    return whole + 0.33
                elif fraction == 2:
                    return whole + 0.67
                else:
                    return whole + (fraction / 10)
            
            return float(ip_string)
        except:
            return 0.0
    
    def sync_game_player_stats(self, espn_id: str) -> Dict[str, Any]:
        """
        Sync player statistics for a specific game.
        Note: This is currently a placeholder since ESPN's public API doesn't provide detailed player stats.
        """
        try:
            # Get the game from our database
            game = self.db.query(Game).filter(Game.espn_id == espn_id).first()
            if not game:
                return {
                    "synced": False,
                    "reason": f"Game with ESPN ID {espn_id} not found in database"
                }
            
            # Fetch box score from ESPN (this works and gives us game structure)
            box_score_data = self.fetch_game_box_score(espn_id)
            if not box_score_data:
                return {
                    "synced": False,
                    "reason": "Failed to fetch box score data from ESPN"
                }
            
            print(f"Successfully fetched game data for {espn_id}")
            print(f"Game structure: {list(box_score_data.keys())}")
            
            # For now, return a placeholder response since we can't get player stats yet
            return {
                "synced": False,
                "reason": "ESPN's public API doesn't provide detailed player statistics. This endpoint is ready for when we get access to MLB Stats API or implement web scraping.",
                "game_found": True,
                "game_structure": list(box_score_data.keys()) if isinstance(box_score_data, dict) else "Not a dict"
            }
            
        except Exception as e:
            return {
                "synced": False,
                "reason": f"Error syncing player stats: {e}"
            }
    
    def get_player_game_stats(self, game_id: int) -> List[PlayerGameStats]:
        """
        Get all player statistics for a specific game.
        """
        return self.db.query(PlayerGameStats).filter(
            PlayerGameStats.game_id == game_id
        ).all()
    
    def get_player_season_stats(self, player_id: int, season: int = None) -> Dict[str, Any]:
        """
        Get aggregated season statistics for a specific player.
        """
        if not season:
            season = 2025  # Default to current season
        
        # Get all games for the season
        season_games = self.db.query(Game).filter(
            Game.game_date >= f"{season}-01-01",
            Game.game_date <= f"{season}-12-31"
        ).all()
        
        game_ids = [game.id for game in season_games]
        
        # Get all player stats for these games
        player_stats = self.db.query(PlayerGameStats).filter(
            PlayerGameStats.player_id == player_id,
            PlayerGameStats.game_id.in_(game_ids)
        ).all()
        
        # Aggregate the stats
        aggregated = {
            'games_played': len(player_stats),
            'at_bats': sum(ps.at_bats or 0 for ps in player_stats),
            'runs': sum(ps.runs or 0 for ps in player_stats),
            'hits': sum(ps.hits or 0 for ps in player_stats),
            'doubles': sum(ps.doubles or 0 for ps in player_stats),
            'triples': sum(ps.triples or 0 for ps in player_stats),
            'home_runs': sum(ps.home_runs or 0 for ps in player_stats),
            'rbis': sum(ps.rbis or 0 for ps in player_stats),
            'walks': sum(ps.walks or 0 for ps in player_stats),
            'strikeouts': sum(ps.strikeouts or 0 for ps in player_stats),
            'stolen_bases': sum(ps.stolen_bases or 0 for ps in player_stats),
            'caught_stealing': sum(ps.caught_stealing or 0 for ps in player_stats),
        }
        
        # Calculate batting average
        if aggregated['at_bats'] > 0:
            aggregated['batting_average'] = round(aggregated['hits'] / aggregated['at_bats'], 3)
        else:
            aggregated['batting_average'] = 0.000
        
        return aggregated
