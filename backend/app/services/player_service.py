from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date
import requests
from bs4 import BeautifulSoup
import re

from ..db.models import Player, PlayerPosition
from ..db.schemas import PlayerCreate, PlayerUpdate

class PlayerService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_players(self, position: Optional[str] = None, status: Optional[str] = None) -> List[Player]:
        """
        Get all players with optional filtering by position and status.
        """
        query = self.db.query(Player)
        
        if position:
            query = query.filter(Player.position == position)
        
        if status:
            query = query.filter(Player.status == status)
        
        return query.order_by(Player.uniform_number, Player.name).all()
    
    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """
        Get a player by their ID.
        """
        return self.db.query(Player).filter(Player.id == player_id).first()
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """
        Get a player by their name.
        """
        return self.db.query(Player).filter(Player.name == name).first()
    
    def create_player(self, player: PlayerCreate) -> Player:
        """
        Create a new player with positions.
        """
        # Extract positions from the create data
        positions_data = player.positions
        player_data = player.dict(exclude={'positions'})
        
        # Create the player
        db_player = Player(**player_data)
        self.db.add(db_player)
        self.db.flush()  # Get the ID without committing
        
        # Create position records
        for i, pos in enumerate(positions_data):
            is_primary = (i == 0)  # First position is primary
            position = PlayerPosition(
                player_id=db_player.id,
                position=pos,
                is_primary=is_primary
            )
            self.db.add(position)
        
        self.db.commit()
        self.db.refresh(db_player)
        return db_player
    
    def update_player(self, player_id: int, player_update: PlayerUpdate) -> Optional[Player]:
        """
        Update an existing player.
        """
        db_player = self.get_player_by_id(player_id)
        if not db_player:
            return None
        
        update_data = player_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_player, field, value)
        
        self.db.commit()
        self.db.refresh(db_player)
        return db_player
    
    def delete_player(self, player_id: int) -> bool:
        """
        Delete a player.
        """
        db_player = self.get_player_by_id(player_id)
        if not db_player:
            return False
        
        self.db.delete(db_player)
        self.db.commit()
        return True
    
    def get_players_by_position(self, position: str) -> List[Player]:
        """
        Get all players at a specific position.
        """
        return self.db.query(Player).filter(Player.position == position).order_by(Player.uniform_number).all()
    
    def get_active_players(self) -> List[Player]:
        """
        Get all active players.
        """
        return self.db.query(Player).filter(Player.status == "Active").order_by(Player.uniform_number, Player.name).all()
    
    def search_players(self, search_term: str) -> List[Player]:
        """
        Search players by name (case-insensitive).
        """
        return self.db.query(Player).filter(Player.name.ilike(f"%{search_term}%")).all()
    
    def should_sync_roster(self) -> bool:
        """
        Check if roster should be synced (more than 24 hours since last update).
        TEMPORARILY DISABLED for testing - always returns True
        """
        print("24-hour lock temporarily disabled for testing - sync allowed")
        return True

    def sync_roster_from_espn(self) -> List[dict]:
        """
        Sync current roster from ESPN and return parsed data (no DB changes).
        """
        # ESPN Dodgers roster page
        url = "https://www.espn.com/mlb/team/roster/_/name/lad/los-angeles-dodgers"
        
        try:
            print("Fetching roster data from ESPN...", flush=True)
            
            # Add proper headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            print(f"Response status: {response.status_code}")
            print(f"Response length: {len(response.text)} characters")
            print("First 1000 characters of HTML:")
            print(response.text[:1000])
            print("...")
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract roster data from the page
            players = self._parse_espn_roster(soup)
            
            print(f"Successfully parsed {len(players)} players from ESPN", flush=True)
            return players
            
        except Exception as e:
            print(f"Error syncing from ESPN: {e}")
            return []

    def sync_roster_to_database(self) -> dict:
        """
        Sync current roster from ESPN and save to database.
        Returns sync result with player count and sync status.
        """
        from datetime import datetime
        
        # Check if we should sync
        if not self.should_sync_roster():
            return {
                "synced": False,
                "reason": "Roster updated within last 24 hours",
                "players_count": self.db.query(Player).count()
            }
        
        # Get current roster from ESPN
        players_data = self.sync_roster_from_espn()
        if not players_data:
            return {
                "synced": False,
                "reason": "Failed to fetch roster data from ESPN",
                "players_count": 0
            }
        
        try:
            # Clear existing roster data
            print("Clearing existing roster data...")
            self.db.query(PlayerPosition).delete()
            self.db.query(Player).delete()
            self.db.commit()
            
            # Add new roster data
            current_time = datetime.now().isoformat()
            added_players = 0
            
            for player_data in players_data:
                # Create player
                player = Player(
                    name=player_data['name'],
                    uniform_number=player_data['uniform_number'],
                    team=player_data['team'],
                    status=player_data['status'],
                    bats=player_data.get('bats'),
                    throws=player_data.get('throws'),
                    height=player_data.get('height'),
                    weight=player_data.get('weight'),
                    last_updated=current_time
                )
                self.db.add(player)
                self.db.flush()  # Get the ID
                
                # Create position records
                for i, pos in enumerate(player_data['positions']):
                    is_primary = (i == 0)  # First position is primary
                    position = PlayerPosition(
                        player_id=player.id,
                        position=pos,
                        is_primary=is_primary
                    )
                    self.db.add(position)
                
                added_players += 1
            
            self.db.commit()
            
            return {
                "synced": True,
                "reason": "Roster successfully synced from ESPN",
                "players_count": added_players,
                "sync_time": current_time
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Error syncing roster to database: {e}")
            return {
                "synced": False,
                "reason": f"Database error: {str(e)}",
                "players_count": 0
            }
    
    def _parse_espn_roster(self, soup: BeautifulSoup) -> List[dict]:
        """
        Parse the ESPN HTML to extract roster information.
        """
        players = []
        
        try:
            # ESPN has multiple roster tables organized by position groups
            # Look for all tables with class 'Table' within roster sections
            roster_tables = soup.find_all('table', class_='Table')
            
            if not roster_tables:
                print("No roster tables found on ESPN page")
                return players
            
            print(f"Found {len(roster_tables)} ESPN roster tables")
            
            # Debug: Let's look at the first table structure
            if roster_tables:
                first_table = roster_tables[0]
                header_row = first_table.find('tr')
                if header_row:
                    headers = header_row.find_all('th')
                    print("Table headers found:")
                    for i, header in enumerate(headers):
                        print(f"  Column {i}: {header.get_text().strip()}")
                    print()
            
            for table_idx, table in enumerate(roster_tables):
                # Find all rows in the table
                rows = table.find_all('tr')
                print(f"Processing table {table_idx + 1} with {len(rows)} rows")
                
                for row in rows:
                    # Skip header rows
                    if row.find('th'):
                        continue
                    
                    # Get all cells in the row
                    cells = row.find_all('td')
                    
                    # Debug: Show what we're getting in this row
                    if len(cells) > 0:
                        print(f"Row has {len(cells)} cells:")
                        for i, cell in enumerate(cells[:8]):  # Show first 8 cells
                            cell_text = cell.get_text().strip()
                            print(f"  Cell {i}: '{cell_text}'")
                    
                    if len(cells) >= 7:  # ESPN has: Headshot, Name, Position, Bats, Throws, Age, Height, Weight, Birth Place
                        try:
                            # Extract player name (second column, index 1)
                            name_cell = cells[1]
                            name_link = name_cell.find('a')
                            player_name = name_link.get_text().strip() if name_link else name_cell.get_text().strip()
                            
                            # Extract position (third column, index 2)
                            position = cells[2].get_text().strip() if len(cells) > 2 else 'Unknown'
                            
                            # Extract bats (fourth column, index 3)
                            bats = cells[3].get_text().strip() if len(cells) > 3 else None
                            
                            # Extract throws (fifth column, index 4)
                            throws = cells[4].get_text().strip() if len(cells) > 4 else None
                            
                            # Extract age (sixth column, index 5)
                            age_text = cells[5].get_text().strip() if len(cells) > 5 else None
                            age = None
                            if age_text and age_text.isdigit():
                                age = int(age_text)
                            
                            # Extract height (seventh column, index 6)
                            height = cells[6].get_text().strip() if len(cells) > 6 else None
                            
                            # Extract weight (eighth column, index 7)
                            weight_text = cells[7].get_text().strip() if len(cells) > 7 else None
                            weight = None
                            if weight_text:
                                # Extract number from "212 lbs" format
                                weight_match = re.search(r'(\d+)', weight_text)
                                if weight_match:
                                    weight = int(weight_match.group(1))
                            
                            # Extract jersey number from name cell (it's in a span with class 'n10')
                            uniform_number = None
                            jersey_span = name_cell.find('span', class_='n10')
                            if jersey_span:
                                jersey_text = jersey_span.get_text().strip()
                                number_match = re.search(r'(\d+)', jersey_text)
                                if number_match:
                                    uniform_number = int(number_match.group(1))
                            
                            # If no uniform number found in span, try to extract from name
                            if uniform_number is None:
                                name_number_match = re.search(r'(\d+)$', player_name)
                                if name_number_match:
                                    uniform_number = int(name_number_match.group(1))
                                    # Clean the name by removing the number
                                    player_name = re.sub(r'\d+$', '', player_name).strip()
                            
                            # Only add if we have a valid player name
                            if player_name and len(player_name) > 2 and self._is_valid_player_name(player_name):
                                player_info = {
                                    'name': player_name,
                                    'uniform_number': uniform_number,
                                    'positions': [position],  # Start with primary position
                                    'bats': bats,
                                    'throws': throws,
                                    'height': height,
                                    'weight': weight,
                                    'status': 'Active',
                                    'team': 'Los Angeles Dodgers'
                                }
                                players.append(player_info)
                                print(f"Table {table_idx + 1}: Found player: {player_name} - {position} - #{uniform_number} - B:{bats}/T:{throws} - {height} {weight}lbs")
                    
                        except Exception as e:
                            print(f"Error parsing row: {e}")
                            continue
            
            print(f"Total players found: {len(players)}")
            
        except Exception as e:
            print(f"Error parsing ESPN roster: {e}")
        
        return players
    
    def _is_valid_player_name(self, text: str) -> bool:
        """
        Check if text looks like a valid player name.
        """
        if not text or len(text) < 3:
            return False
        
        # Filter out common non-player entries
        invalid_patterns = [
            r'league|division|conference|association',
            r'\d{4}[-–]\d{4}',  # Year ranges like "1890-1891"
            r'present|current|former',
            r'championship|title|award',
            r'stadium|ballpark|venue',
            r'coach|manager|owner|executive',
            r'minor league|triple-a|double-a|single-a',
            r'rookie|veteran|all-star|mvp'
        ]
        
        text_lower = text.lower()
        for pattern in invalid_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # Must look like a person's name (first and last name)
        if not re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', text):
            return False
        
        return True
    
    def _extract_player_info_from_table(self, row) -> Optional[dict]:
        """
        Extract player information from a table row.
        """
        try:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                return None
            
            name = cells[0].get_text().strip()
            if not self._is_valid_player_name(name):
                return None
            
            position = cells[1].get_text().strip() if len(cells) > 1 else 'Unknown'
            
            # Try to extract jersey number from name or position
            uniform_number = None
            number_match = re.search(r'#(\d+)', name + ' ' + position)
            if number_match:
                uniform_number = int(number_match.group(1))
            
            return {
                'name': name,
                'position': position,
                'uniform_number': uniform_number,
                'status': 'Active',
                'team': 'Los Angeles Dodgers'
            }
            
        except Exception as e:
            print(f"Error extracting player info from table row: {e}")
            return None
    
    def _extract_player_info(self, player_text: str) -> Optional[dict]:
        """
        Extract player information from text.
        """
        try:
            # Basic parsing - this will need refinement based on actual data format
            player_info = {
                'name': player_text.strip(),
                'position': 'Unknown',
                'uniform_number': None,
                'status': 'Active',
                'team': 'Los Angeles Dodgers'
            }
            
            # Try to extract position if it's in parentheses or after a dash
            if '(' in player_text:
                # Look for position in parentheses
                match = re.search(r'\(([^)]+)\)', player_text)
                if match:
                    position = match.group(1).strip()
                    if any(pos in position.upper() for pos in ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH']):
                        player_info['position'] = position
                        player_info['name'] = player_text.split('(')[0].strip()
            
            # Try to extract jersey number
            number_match = re.search(r'#(\d+)', player_text)
            if number_match:
                player_info['uniform_number'] = int(number_match.group(1))
            
            return player_info
            
        except Exception as e:
            print(f"Error extracting player info from '{player_text}': {e}")
            return None
    

