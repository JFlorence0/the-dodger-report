import requests
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from ..db.models import Game, GameResult, PlayerGameStats, Player
from ..db.schemas import GameCreate, GameResultCreate, PlayerGameStatsCreate
from .stadium_service import StadiumService
from ..core.config import settings
import re

class GameService:
    def __init__(self, db: Session):
        self.db = db
        self.espn_base_url = settings.ESPN_BASE_URL
        self.dodgers_team_id = settings.DODGERS_TEAM_ID
        self.stadium_service = StadiumService(db)

    def sync_dodgers_schedule(self) -> Dict[str, Any]:
        """
        Sync the Dodgers' current season schedule from ESPN.
        Returns sync result with game count and status.
        """
        try:
            print("Fetching Dodgers schedule from ESPN...")
            
            # Get schedule
            schedule_url = f"{self.espn_base_url}/teams/{self.dodgers_team_id}/schedule"
            response = requests.get(schedule_url)
            response.raise_for_status()
            
            schedule_data = response.json()
            events = schedule_data.get('events', [])
            
            if not events:
                return {
                    "synced": False,
                    "reason": "No games found in schedule",
                    "games_count": 0
                }
            
            print(f"Found {len(events)} games in schedule")
            
            # Clear existing games for this season
            current_year = datetime.now().year
            self.db.query(Game).filter(
                Game.game_date >= date(current_year, 1, 1)
            ).delete()
            self.db.commit()
            
            added_games = 0
            processed_games = set()  # Track unique games to avoid duplicates
            
            for event in events:
                try:
                    game_data = self._parse_schedule_event(event)
                    if game_data:
                        # Skip Spring Training games (March games)
                        if game_data['game_date'].month == 3:
                            print(f"Skipping Spring Training: {game_data['away_team']} @ {game_data['home_team']} on {game_data['game_date']}")
                            continue
                        
                        # Create a unique key for the game (date + teams)
                        game_key = f"{game_data['game_date']}_{game_data['home_team']}_{game_data['away_team']}"
                        
                        # Skip if we've already processed this exact game
                        if game_key in processed_games:
                            print(f"Skipping duplicate game: {game_data['away_team']} @ {game_data['home_team']} on {game_data['game_date']}")
                            continue
                        
                        processed_games.add(game_key)
                        
                        # Check if game already exists by ESPN ID
                        existing_game = self.db.query(Game).filter(
                            Game.espn_id == game_data['espn_id']
                        ).first()
                        
                        if not existing_game:
                            game = Game(**game_data)
                            self.db.add(game)
                            self.db.flush()  # Get the game ID
                            
                            # Create generic game result
                            game_result = self._create_game_result(game, event)
                            if game_result:
                                self.db.add(game_result)
                            
                            added_games += 1
                            print(f"Added game: {game_data['away_team']} @ {game_data['home_team']} on {game_data['game_date']}")
                        else:
                            print(f"Game already exists: {game_data['away_team']} @ {game_data['home_team']}")
                            
                except Exception as e:
                    print(f"Error processing game: {e}")
                    continue
            
            self.db.commit()
            
            return {
                "synced": True,
                "reason": f"Successfully synced {added_games} games from ESPN",
                "games_count": added_games,
                "total_games": len(events)
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Error syncing schedule: {e}")
            return {
                "synced": False,
                "reason": f"Error: {str(e)}",
                "games_count": 0
            }

    def _parse_schedule_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse a single schedule event from ESPN API into our game format.
        """
        try:
            # Extract basic game info
            espn_id = event.get('id')
            game_date_str = event.get('date')
            name = event.get('name', '')
            
            if not espn_id or not game_date_str:
                return None
            
            # Parse date
            game_date = datetime.fromisoformat(game_date_str.replace('Z', '+00:00')).date()
            
            # Extract team names from game name (e.g., "Los Angeles Dodgers at Chicago Cubs")
            teams = self._extract_teams_from_name(name)
            if not teams:
                return None
            
            away_team, home_team = teams
            
            # Get competition data
            competition = event.get('competitions', [{}])[0] if event.get('competitions') else {}
            
            # Extract scores
            home_score = None
            away_score = None
            if competition.get('competitors'):
                for competitor in competition['competitors']:
                    if competitor.get('homeAway') == 'home':
                        home_score = competitor.get('score', {}).get('value')
                    elif competitor.get('homeAway') == 'away':
                        away_score = competitor.get('score', {}).get('value')
            
            # Extract venue info
            venue = None
            if competition.get('venue'):
                venue = competition['venue'].get('fullName')
            
            # Extract attendance
            attendance = competition.get('attendance')
            
            # Extract game duration
            game_duration = None
            if competition.get('gameDuration'):
                game_duration = competition['gameDuration']
            
            # Determine if game is final
            is_final = False
            if competition.get('status', {}).get('type', {}).get('state') == 'post':
                is_final = True
            
            # Calculate day of week
            day_of_week = game_date.strftime('%A')
            
            # Determine if night game (simplified - could be enhanced with actual game times)
            is_night_game = None  # We'll need actual game times for this
            
            # Check if neutral site
            neutral_site = competition.get('neutralSite', False)
            
            # Check for extra innings
            extra_innings = False
            if competition.get('status', {}).get('period') and competition['status']['period'] > 9:
                extra_innings = True
            
            return {
                'espn_id': espn_id,
                'game_date': game_date,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'venue': venue,
                'attendance': attendance,
                'game_duration': game_duration,
                'extra_innings': extra_innings,
                'neutral_site': neutral_site,
                'is_final': is_final,
                'day_of_week': day_of_week,
                'is_night_game': is_night_game
            }
            
        except Exception as e:
            print(f"Error parsing event: {e}")
            return None

    def _extract_teams_from_name(self, name: str) -> Optional[tuple]:
        """
        Extract home and away teams from ESPN game name.
        Example: "Los Angeles Dodgers at Chicago Cubs" -> ("Los Angeles Dodgers", "Chicago Cubs")
        """
        try:
            # Pattern: "Team A at Team B"
            match = re.match(r'(.+?)\s+at\s+(.+)', name)
            if match:
                away_team = match.group(1).strip()
                home_team = match.group(2).strip()
                return away_team, home_team
            return None
        except Exception as e:
            print(f"Error extracting teams from name '{name}': {e}")
            return None

    def _create_game_result(self, game: Game, event: Dict[str, Any]) -> Optional[GameResult]:
        """
        Create a GameResult record for a game.
        """
        try:
            competition = event.get('competitions', [{}])[0] if event.get('competitions') else {}
            
            # Find home and away competitors
            home_competitor = None
            away_competitor = None
            
            for competitor in competition.get('competitors', []):
                if competitor.get('homeAway') == 'home':
                    home_competitor = competitor
                elif competitor.get('homeAway') == 'away':
                    away_competitor = competitor
            
            if not home_competitor or not away_competitor:
                return None
            
            # Get scores
            home_score = home_competitor.get('score', {}).get('value', 0)
            away_score = away_competitor.get('score', {}).get('value', 0)
            
            # Get team names
            home_team = home_competitor.get('team', {}).get('displayName', 'Unknown')
            away_team = away_competitor.get('team', {}).get('displayName', 'Unknown')
            
            # Get records after game
            home_record_after = None
            away_record_after = None
            
            if home_competitor.get('record'):
                for record in home_competitor['record']:
                    if record.get('type') == 'total':
                        home_record_after = record.get('displayValue')
                        break
            
            if away_competitor.get('record'):
                for record in away_competitor['record']:
                    if record.get('type') == 'total':
                        away_record_after = record.get('displayValue')
                        break
            
            return GameResult(
                game_id=game.id,
                home_team=home_team,
                away_team=away_team,
                home_score=home_score,
                away_score=away_score,
                home_record_after=home_record_after,
                away_record_after=away_record_after
            )
            
        except Exception as e:
            print(f"Error creating game result: {e}")
            return None

    def get_dodgers_games(self, limit: int = 10) -> List[Game]:
        """
        Get recent Dodgers games.
        """
        return self.db.query(Game).filter(
            (Game.home_team == 'Los Angeles Dodgers') | (Game.away_team == 'Los Angeles Dodgers')
        ).order_by(Game.is_final.desc(), Game.game_date.desc()).limit(limit).all()

    def get_game_by_espn_id(self, espn_id: str) -> Optional[Game]:
        """
        Get a game by its ESPN ID.
        """
        return self.db.query(Game).filter(Game.espn_id == espn_id).first()

    def get_dodger_record(self) -> Dict[str, Any]:
        """
        Get current Dodgers record and recent performance.
        """
        # Get all Dodger game results
        results = self.db.query(GameResult).join(Game).filter(
            (GameResult.home_team == 'Los Angeles Dodgers') | (GameResult.away_team == 'Los Angeles Dodgers')
        ).order_by(Game.game_date.desc()).all()
        
        if not results:
            return {"wins": 0, "losses": 0, "ties": 0, "record": "0-0"}
        
        wins = 0
        losses = 0
        ties = 0
        
        for result in results:
            if result.home_team == 'Los Angeles Dodgers':
                if result.home_score > result.away_score:
                    wins += 1
                elif result.home_score < result.away_score:
                    losses += 1
                else:
                    ties += 1
            else:  # Dodgers are away team
                if result.away_score > result.home_score:
                    wins += 1
                elif result.away_score < result.home_score:
                    losses += 1
                else:
                    ties += 1
        
        return {
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "record": f"{wins}-{losses}",
            "total_games": len(results),
            "last_game": results[0].game.game_date if results else None
        }

    def debug_espn_schedule(self) -> Dict[str, Any]:
        """
        Debug method to inspect what ESPN is sending us.
        """
        try:
            schedule_url = f"{self.espn_base_url}/teams/{self.dodgers_team_id}/schedule"
            response = requests.get(schedule_url)
            response.raise_for_status()
            
            schedule_data = response.json()
            events = schedule_data.get('events', [])
            
            # Analyze the data
            date_counts = {}
            team_combinations = {}
            spring_training_count = 0
            regular_season_count = 0
            
            for event in events:
                date_str = event.get('date', 'Unknown')
                name = event.get('name', 'Unknown')
                
                # Parse date to check month
                try:
                    event_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
                    if event_date.month == 3:
                        spring_training_count += 1
                    else:
                        regular_season_count += 1
                except:
                    pass
                
                if date_str in date_counts:
                    date_counts[date_str] += 1
                else:
                    date_counts[date_str] = 1
                
                if name in team_combinations:
                    team_combinations[name] += 1
                else:
                    team_combinations[name] = 1
            
            return {
                "total_events": len(events),
                "spring_training_games": spring_training_count,
                "regular_season_games": regular_season_count,
                "unique_dates": len(date_counts),
                "date_counts": dict(sorted(date_counts.items())[:10]),  # Top 10 dates
                "duplicate_games": {k: v for k, v in team_combinations.items() if v > 1},
                "sample_events": [
                    {
                        "id": event.get('id'),
                        "date": event.get('date'),
                        "name": event.get('name'),
                        "status": event.get('status', {}).get('type', {}).get('state') if event.get('status') else None
                    }
                    for event in events[:5]  # First 5 events
                ]
            }
            
        except Exception as e:
            return {"error": str(e)}

    def debug_espn_scoreboard(self) -> Dict[str, Any]:
        """
        Debug method to inspect what ESPN scoreboard API is sending us.
        """
        try:
            url = f"{self.espn_base_url}/scoreboard"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            events = data.get('events', [])
            
            # Find Dodgers games in the scoreboard
            dodgers_games = []
            for event in events:
                name = event.get('name', '')
                if 'Los Angeles Dodgers' in name:
                    dodgers_games.append({
                        "id": event.get('id'),
                        "name": name,
                        "date": event.get('date'),
                        "status": event.get('status', {}).get('type', {}).get('state') if event.get('status') else None,
                        "competitions": event.get('competitions', [])
                    })
            
            return {
                "total_events": len(events),
                "dodgers_games_found": len(dodgers_games),
                "dodgers_games": dodgers_games[:5],  # First 5 Dodgers games
                "sample_events": events[:3]  # First 3 events for structure
            }
            
        except Exception as e:
            return {"error": str(e)}

    def calculate_existing_game_results(self) -> Dict[str, Any]:
        """
        Calculate and update game results for existing games that already have scores.
        This is a one-time fix for games we already have, separate from ESPN sync.
        """
        try:
            # Get all games that have scores but no calculated result
            games_to_update = self.db.query(Game).filter(
                Game.home_score.isnot(None),
                Game.away_score.isnot(None),
                Game.is_final == True,
                Game.game_result.is_(None)
            ).all()
            
            updated_games = 0
            
            for game in games_to_update:
                try:
                    # Calculate the result (W/L) for Dodgers games
                    if game.home_team == 'Los Angeles Dodgers':
                        game.game_result = 'W' if game.home_score > game.away_score else 'L'
                    elif game.away_team == 'Los Angeles Dodgers':
                        game.game_result = 'W' if game.away_score > game.home_score else 'L'
                    
                    updated_games += 1
                    print(f"Calculated result for game {game.espn_id}: {game.away_team} @ {game.home_team} - {game.away_score}-{game.home_score} = {game.game_result}")
                
                except Exception as e:
                    print(f"Error calculating result for game {game.espn_id}: {e}")
                    continue
            
            self.db.commit()
            
            return {
                "synced": True,
                "reason": f"Successfully calculated results for {updated_games} existing games",
                "updated_games": updated_games
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Error calculating game results: {e}")
            return {
                "synced": False,
                "reason": f"Error: {str(e)}",
                "updated_games": 0
            }

    def sync_game_results(self) -> Dict[str, Any]:
        """
        Sync actual game results (scores, final status) from ESPN scoreboard.
        This updates existing games with real scores and final status.
        """
        try:
            url = f"{self.espn_base_url}/scoreboard"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            events = data.get('events', [])
            
            updated_games = 0
            games_with_scores = 0
            
            for event in events:
                try:
                    espn_id = event.get('id')
                    if not espn_id:
                        continue
                    
                    # Find our game by ESPN ID
                    game = self.db.query(Game).filter(Game.espn_id == espn_id).first()
                    if not game:
                        continue
                    
                    # Get competition data
                    competition = event.get('competitions', [{}])[0] if event.get('competitions') else {}
                    
                    # Extract scores
                    home_score = None
                    away_score = None
                    is_final = False
                    
                    if competition.get('competitors'):
                        for competitor in competition['competitors']:
                            if competitor.get('homeAway') == 'home':
                                score_val = competitor.get('score', {}).get('value')
                                if score_val is not None:
                                    home_score = int(score_val)
                            elif competitor.get('homeAway') == 'away':
                                score_val = competitor.get('score', {}).get('value')
                                if score_val is not None:
                                    away_score = int(score_val)
                    
                    # Check if game is final
                    if competition.get('status', {}).get('type', {}).get('state') == 'post':
                        is_final = True
                    
                    # Update game if we have new data
                    if home_score is not None or away_score is not None or is_final != game.is_final:
                        if home_score is not None:
                            game.home_score = home_score
                        if away_score is not None:
                            game.away_score = away_score
                        game.is_final = is_final
                        
                        # Calculate the result (W/L) for Dodgers games
                        calculated_result = None
                        if home_score is not None and away_score is not None and is_final:
                            if game.home_team == 'Los Angeles Dodgers':
                                calculated_result = 'W' if home_score > away_score else 'L'
                            elif game.away_team == 'Los Angeles Dodgers':
                                calculated_result = 'W' if away_score > home_score else 'L'
                        
                        # Store the calculated result
                        game.game_result = calculated_result
                        
                        # Update or create game result
                        game_result = self.db.query(GameResult).filter(
                            GameResult.game_id == game.id
                        ).first()
                        
                        if not game_result:
                            game_result = GameResult(
                                game_id=game.id,
                                home_team=game.home_team,
                                away_team=game.away_team,
                                home_score=game.home_score or 0,
                                away_score=game.away_score or 0,
                                home_record_after=None,  # We'll calculate this later
                                away_record_after=None
                            )
                            self.db.add(game_result)
                        else:
                            game_result.home_score = game.home_score or 0
                            game_result.away_score = game.away_score or 0
                        
                        updated_games += 1
                        
                        if home_score is not None or away_score != None:
                            games_with_scores += 1
                            
                        # Try to get weather data for this game
                        if game.venue:
                            try:
                                weather_data = self.stadium_service.get_weather_for_game(
                                    game.venue, 
                                    game.game_date.strftime("%Y-%m-%d"),
                                    game.game_time.strftime("%H:%M") if game.game_time else None
                                )
                                
                                if weather_data:
                                    game.weather_temp = weather_data['temperature']
                                    game.weather_conditions = weather_data['conditions']
                                    game.wind_speed = weather_data['wind_speed']
                                    game.wind_direction = weather_data['wind_direction']
                                    game.humidity = weather_data['humidity']
                                    print(f"Added weather data for {game.venue}: {weather_data['temperature']}°F, {weather_data['conditions']}")
                            except Exception as weather_err:
                                print(f"Error getting weather for {game.venue}: {weather_err}")
                        
                        print(f"Updated game {espn_id}: {game.away_team} @ {game.home_team} - {away_score}-{home_score} (Final: {is_final}) Result: {calculated_result}")
                
                except Exception as e:
                    print(f"Error updating game {event.get('id', 'unknown')}: {e}")
                    continue
            
            self.db.commit()
            
            return {
                "synced": True,
                "reason": f"Successfully updated {updated_games} games with results",
                "updated_games": updated_games,
                "games_with_scores": games_with_scores
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Error syncing game results: {e}")
            return {
                "synced": False,
                "reason": f"Error: {str(e)}",
                "updated_games": 0,
                "games_with_scores": 0
            }

    def sync_weather_for_existing_games(self) -> Dict[str, Any]:
        """
        Sync weather data for existing games that don't have weather information.
        """
        try:
            # Get all games that don't have weather data but have venues
            games_to_update = self.db.query(Game).filter(
                Game.venue.isnot(None),
                Game.weather_temp.is_(None)
            ).all()
            
            updated_games = 0
            
            for game in games_to_update:
                try:
                    weather_data = self.stadium_service.get_weather_for_game(
                        game.venue,
                        game.game_date.strftime("%Y-%m-%d"),
                        game.game_time.strftime("%H:%M") if game.game_time else None
                    )
                    
                    if weather_data:
                        game.weather_temp = weather_data['temperature']
                        game.weather_conditions = weather_data['conditions']
                        game.wind_speed = weather_data['wind_speed']
                        game.wind_direction = weather_data['wind_direction']
                        game.humidity = weather_data['humidity']
                        
                        updated_games += 1
                        print(f"Added weather for {game.venue} on {game.game_date}: {weather_data['temperature']}°F, {weather_data['conditions']}")
                
                except Exception as e:
                    print(f"Error getting weather for game {game.espn_id}: {e}")
                    continue
            
            self.db.commit()
            
            return {
                "synced": True,
                "reason": f"Successfully added weather for {updated_games} games",
                "updated_games": updated_games
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Error syncing weather: {e}")
            return {
                "synced": False,
                "reason": f"Error: {str(e)}",
                "updated_games": 0
            }
