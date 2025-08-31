import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..db.models.players import Player
from ..db.models.games import Game, PlayerGameStats

class PlayerGameService:
    def __init__(self, db: Session):
        self.db = db
        self.base_url = "https://www.espn.com/mlb/player/gamelog/_/id"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_player_espn_id(self, player_name: str) -> Optional[str]:
        """Get ESPN player ID from player name"""
        # This would need to be implemented based on how we map our players to ESPN IDs
        # For now, we'll use a simple mapping approach
        espn_id_mapping = {
            'Freddie Freeman': '30193',
            'Mookie Betts': '34081',
            'Shohei Ohtani': '39832',
            # Add more mappings as needed
        }
        return espn_id_mapping.get(player_name)

    def scrape_player_game_log(self, espn_id: str, player_name: str) -> List[Dict]:
        """Scrape player game log data from ESPN"""
        try:
            url = f"https://www.espn.com/mlb/player/gamelog/_/id/{espn_id}/{player_name.lower().replace(' ', '-')}"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the game log table
            game_log_table = soup.find('table', {'class': 'Table'})
            if not game_log_table:
                print(f"Game log table not found for {player_name}")
                return []
            
            games = []
            rows = game_log_table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 19:  # Ensure we have all columns
                    game_data = self._parse_game_row(cells)
                    if game_data:
                        games.append(game_data)
            
            print(f"Scraped {len(games)} games for {player_name}")
            return games
            
        except Exception as e:
            print(f"Error scraping game log for {player_name}: {e}")
            return []

    def _parse_game_row(self, cells) -> Dict:
        """Parse a single game row from the table"""
        try:
            # Parse date
            date_text = cells[0].get_text(strip=True)
            game_date = self._parse_game_date(date_text)
            
            # Parse opponent and home/away
            opp_text = cells[1].get_text(strip=True)
            opponent, is_home = self._parse_opponent(opp_text)
            
            # Parse result
            result_text = cells[2].get_text(strip=True)
            result = self._parse_result(result_text)
            
            # Parse stats
            stats = {
                'game_date': game_date,
                'opponent': opponent,
                'is_home': is_home,
                'result': result,
                'at_bats': self._safe_int(cells[3]),
                'runs': self._safe_int(cells[4]),
                'hits': self._safe_int(cells[5]),
                'doubles': self._safe_int(cells[6]),
                'triples': self._safe_int(cells[7]),
                'home_runs': self._safe_int(cells[8]),
                'rbis': self._safe_int(cells[9]),
                'walks': self._safe_int(cells[10]),
                'hit_by_pitch': self._safe_int(cells[11]),
                'strikeouts': self._safe_int(cells[12]),
                'stolen_bases': self._safe_int(cells[13]),
                'caught_stealing': self._safe_int(cells[14]),
                'batting_average': self._safe_float(cells[15]),
                'on_base_percentage': self._safe_float(cells[16]),
                'slugging_percentage': self._safe_float(cells[17]),
                'ops': self._safe_float(cells[18])
            }
            
            return stats
            
        except Exception as e:
            print(f"Error parsing game row: {e}")
            return None

    def _parse_game_date(self, date_text: str) -> str:
        """Parse ESPN date format (e.g., 'Sat 8/30') to ISO format"""
        try:
            # ESPN format: "Sat 8/30" -> convert to 2025-08-30
            current_year = 2025
            date_match = re.search(r'(\w+)\s+(\d+)/(\d+)', date_text)
            if date_match:
                month = int(date_match.group(2))
                day = int(date_match.group(3))
                return f"{current_year}-{month:02d}-{day:02d}"
            return date_text
        except:
            return date_text

    def _parse_opponent(self, opp_text: str) -> tuple:
        """Parse opponent text to get team abbreviation and home/away"""
        try:
            # ESPN format: "vs ARI", "@ SD", etc.
            if opp_text.startswith('vs '):
                return opp_text[3:], True  # Home game
            elif opp_text.startswith('@'):
                return opp_text[1:], False  # Away game
            else:
                return opp_text, True  # Default to home
        except:
            return opp_text, True

    def _parse_result(self, result_text: str) -> str:
        """Parse result text to get W/L and score"""
        try:
            # ESPN format: "L 6-1", "W 6-3"
            result_match = re.search(r'([WL])\s+(\d+)-(\d+)', result_text)
            if result_match:
                return result_match.group(1)
            return result_text
        except:
            return result_text

    def _safe_int(self, cell) -> int:
        """Safely extract integer from table cell"""
        try:
            text = cell.get_text(strip=True)
            return int(text) if text and text != '-' else 0
        except:
            return 0

    def _safe_float(self, cell) -> float:
        """Safely extract float from table cell"""
        try:
            text = cell.get_text(strip=True)
            return float(text) if text and text != '-' else 0.0
        except:
            return 0.0

    def sync_player_season_stats(self, player_id: int) -> Dict:
        """Sync complete season stats for a player"""
        try:
            # Get player from database
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                return {"error": "Player not found"}
            
            # Get ESPN ID for player
            espn_id = self.get_player_espn_id(player.name)
            if not espn_id:
                return {"error": f"ESPN ID not found for {player.name}"}
            
            # Scrape game log data
            games = self.scrape_player_game_log(espn_id, player.name)
            if not games:
                return {"error": f"No games found for {player.name}"}
            
            # Store games in database (this would need PlayerGameStats model)
            # For now, return the scraped data
            return {
                "success": True,
                "player_name": player.name,
                "games_scraped": len(games),
                "games": games[:10]  # Return first 10 for preview
            }
            
        except Exception as e:
            return {"error": f"Failed to sync player stats: {str(e)}"}

    def get_player_season_summary(self, player_id: int) -> Dict:
        """Get season summary stats for a player"""
        try:
            # This would query the database for aggregated stats
            # For now, return placeholder
            return {
                "games_played": 0,
                "at_bats": 0,
                "hits": 0,
                "home_runs": 0,
                "rbis": 0,
                "batting_average": 0.0,
                "on_base_percentage": 0.0,
                "slugging_percentage": 0.0,
                "ops": 0.0
            }
        except Exception as e:
            return {"error": f"Failed to get season summary: {str(e)}"}
