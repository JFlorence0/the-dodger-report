import requests
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..core.config import settings
from ..db.models.stadiums import Stadium

class StadiumService:
    """
    Service for managing stadium data and weather information.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_api_key = settings.WEATHER_API_KEY
        self.weather_base_url = settings.WEATHER_BASE_URL
    
    def get_stadium_by_name(self, venue_name: str) -> Optional[Stadium]:
        """
        Get stadium by name (with fuzzy matching).
        """
        if not venue_name:
            return None
            
        # Try exact match first
        stadium = self.db.query(Stadium).filter(
            Stadium.name == venue_name
        ).first()
        
        if stadium:
            return stadium
        
        # Try partial matches
        stadium = self.db.query(Stadium).filter(
            Stadium.name.contains(venue_name)
        ).first()
        
        if stadium:
            return stadium
        
        # Try reverse partial match
        stadium = self.db.query(Stadium).filter(
            venue_name.contains(Stadium.name)
        ).first()
        
        return stadium
    
    def get_stadium_coordinates(self, venue_name: str) -> Optional[Dict[str, float]]:
        """
        Get coordinates for a stadium by name.
        """
        stadium = self.get_stadium_by_name(venue_name)
        if stadium:
            return stadium.coordinates
        return None
    
    def create_stadium(self, name: str, city: str, state: str, latitude: float, longitude: float, **kwargs) -> Stadium:
        """
        Create a new stadium record.
        """
        stadium = Stadium(
            name=name,
            city=city,
            state=state,
            latitude=latitude,
            longitude=longitude,
            **kwargs
        )
        self.db.add(stadium)
        self.db.commit()
        self.db.refresh(stadium)
        return stadium
    
    def update_stadium_coordinates(self, stadium_id: int, latitude: float, longitude: float) -> bool:
        """
        Update stadium coordinates.
        """
        stadium = self.db.query(Stadium).filter(Stadium.id == stadium_id).first()
        if stadium:
            stadium.latitude = latitude
            stadium.longitude = longitude
            self.db.commit()
            return True
        return False
    
    def seed_mlb_stadiums(self) -> Dict[str, int]:
        """
        Seed the database with current MLB stadiums.
        Returns count of stadiums added.
        """
        mlb_stadiums = [
            {
                "name": "Dodger Stadium",
                "city": "Los Angeles",
                "state": "CA",
                "latitude": 34.0739,
                "longitude": -118.2400,
                "primary_team": "Los Angeles Dodgers",
                "capacity": 56000,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1962
            },
            {
                "name": "Petco Park",
                "city": "San Diego",
                "state": "CA",
                "latitude": 32.7075,
                "longitude": -117.1570,
                "primary_team": "San Diego Padres",
                "capacity": 40162,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2004
            },
            {
                "name": "Oracle Park",
                "city": "San Francisco",
                "state": "CA",
                "latitude": 37.7786,
                "longitude": -122.3893,
                "primary_team": "San Francisco Giants",
                "capacity": 41915,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2000
            },
            {
                "name": "Chase Field",
                "city": "Phoenix",
                "state": "AZ",
                "latitude": 33.4454,
                "longitude": -112.0669,
                "primary_team": "Arizona Diamondbacks",
                "capacity": 48405,
                "surface_type": "Grass",
                "roof_type": "Retractable",
                "opened_year": 1998
            },
            {
                "name": "Coors Field",
                "city": "Denver",
                "state": "CO",
                "latitude": 39.7562,
                "longitude": -104.9941,
                "primary_team": "Colorado Rockies",
                "capacity": 50144,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1995
            },
            {
                "name": "Minute Maid Park",
                "city": "Houston",
                "state": "TX",
                "latitude": 29.7569,
                "longitude": -95.3550,
                "primary_team": "Houston Astros",
                "capacity": 41168,
                "surface_type": "Grass",
                "roof_type": "Retractable",
                "opened_year": 2000
            },
            {
                "name": "Globe Life Field",
                "city": "Arlington",
                "state": "TX",
                "latitude": 32.7511,
                "longitude": -97.0827,
                "primary_team": "Texas Rangers",
                "capacity": 40300,
                "surface_type": "Grass",
                "roof_type": "Retractable",
                "opened_year": 2020
            },
            {
                "name": "Truist Park",
                "city": "Atlanta",
                "state": "GA",
                "latitude": 33.8904,
                "longitude": -84.4679,
                "primary_team": "Atlanta Braves",
                "capacity": 41084,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2017
            },
            {
                "name": "American Family Field",
                "city": "Milwaukee",
                "state": "WI",
                "latitude": 43.0284,
                "longitude": -87.9711,
                "primary_team": "Milwaukee Brewers",
                "capacity": 41900,
                "surface_type": "Grass",
                "roof_type": "Retractable",
                "opened_year": 2001
            },
            {
                "name": "Wrigley Field",
                "city": "Chicago",
                "state": "IL",
                "latitude": 41.9484,
                "longitude": -87.6553,
                "primary_team": "Chicago Cubs",
                "capacity": 41649,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1914
            },
            {
                "name": "Guaranteed Rate Field",
                "city": "Chicago",
                "state": "IL",
                "latitude": 41.8300,
                "longitude": -87.6338,
                "primary_team": "Chicago White Sox",
                "capacity": 40615,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1991
            },
            {
                "name": "Comerica Park",
                "city": "Detroit",
                "state": "MI",
                "latitude": 42.3390,
                "longitude": -83.0485,
                "primary_team": "Detroit Tigers",
                "capacity": 41083,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2000
            },
            {
                "name": "Progressive Field",
                "city": "Cleveland",
                "state": "OH",
                "latitude": 41.4962,
                "longitude": -81.6852,
                "primary_team": "Cleveland Guardians",
                "capacity": 34530,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1994
            },
            {
                "name": "Target Field",
                "city": "Minneapolis",
                "state": "MN",
                "latitude": 44.9817,
                "longitude": -93.2773,
                "primary_team": "Minnesota Twins",
                "capacity": 38544,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2010
            },
            {
                "name": "Kauffman Stadium",
                "city": "Kansas City",
                "state": "MO",
                "latitude": 39.0511,
                "longitude": -94.4806,
                "primary_team": "Kansas City Royals",
                "capacity": 37903,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1973
            },
            {
                "name": "Fenway Park",
                "city": "Boston",
                "state": "MA",
                "latitude": 42.3467,
                "longitude": -71.0972,
                "primary_team": "Boston Red Sox",
                "capacity": 37155,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1912
            },
            {
                "name": "Yankee Stadium",
                "city": "New York",
                "state": "NY",
                "latitude": 40.8296,
                "longitude": -73.9262,
                "primary_team": "New York Yankees",
                "capacity": 46537,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2009
            },
            {
                "name": "Citi Field",
                "city": "New York",
                "state": "NY",
                "latitude": 40.7569,
                "longitude": -73.8458,
                "primary_team": "New York Mets",
                "capacity": 41922,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2009
            },
            {
                "name": "Citizens Bank Park",
                "city": "Philadelphia",
                "state": "PA",
                "latitude": 39.9059,
                "longitude": -75.1666,
                "primary_team": "Philadelphia Phillies",
                "capacity": 42792,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2004
            },
            {
                "name": "Nationals Park",
                "city": "Washington",
                "state": "DC",
                "latitude": 38.8730,
                "longitude": -77.0074,
                "primary_team": "Washington Nationals",
                "capacity": 41339,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2008
            },
            {
                "name": "Oriole Park at Camden Yards",
                "city": "Baltimore",
                "state": "MD",
                "latitude": 39.2839,
                "longitude": -76.6217,
                "primary_team": "Baltimore Orioles",
                "capacity": 45971,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 1992
            },
            {
                "name": "Rogers Centre",
                "city": "Toronto",
                "state": "ON",
                "country": "Canada",
                "latitude": 43.6414,
                "longitude": -79.3891,
                "primary_team": "Toronto Blue Jays",
                "capacity": 49282,
                "surface_type": "Turf",
                "roof_type": "Retractable",
                "opened_year": 1989
            },
            {
                "name": "Tropicana Field",
                "city": "St. Petersburg",
                "state": "FL",
                "latitude": 27.7682,
                "longitude": -82.6534,
                "primary_team": "Tampa Bay Rays",
                "capacity": 25000,
                "surface_type": "Turf",
                "roof_type": "Fixed",
                "opened_year": 1990
            },
            {
                "name": "loanDepot Park",
                "city": "Miami",
                "state": "FL",
                "latitude": 25.7780,
                "longitude": -80.2196,
                "primary_team": "Miami Marlins",
                "capacity": 36742,
                "surface_type": "Grass",
                "roof_type": "Retractable",
                "opened_year": 2012
            },
            {
                "name": "PNC Park",
                "city": "Pittsburgh",
                "state": "PA",
                "latitude": 40.4469,
                "longitude": -80.0058,
                "primary_team": "Pittsburgh Pirates",
                "capacity": 38747,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2001
            },
            {
                "name": "Great American Ball Park",
                "city": "Cincinnati",
                "state": "OH",
                "latitude": 39.0979,
                "longitude": -84.5082,
                "primary_team": "Cincinnati Reds",
                "capacity": 43431,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2003
            },
            {
                "name": "Busch Stadium",
                "city": "St. Louis",
                "state": "MO",
                "latitude": 38.6226,
                "longitude": -90.1928,
                "primary_team": "St. Louis Cardinals",
                "capacity": 45494,
                "surface_type": "Grass",
                "roof_type": "Open",
                "opened_year": 2006
            }
        ]
        
        added_count = 0
        for stadium_data in mlb_stadiums:
            # Check if stadium already exists
            existing = self.db.query(Stadium).filter(
                Stadium.name == stadium_data["name"]
            ).first()
            
            if not existing:
                self.create_stadium(**stadium_data)
                added_count += 1
                print(f"Added stadium: {stadium_data['name']}")
            else:
                print(f"Stadium already exists: {stadium_data['name']}")
        
        return {"added": added_count, "total": len(mlb_stadiums)}
    
    def get_weather_for_game(self, venue_name: str, game_date: str, game_time: Optional[str] = None) -> Optional[Dict]:
        """
        Get weather data for a specific game using stadium coordinates.
        """
        try:
            # Get stadium coordinates from database
            stadium = self.get_stadium_by_name(venue_name)
            if not stadium:
                print(f"No stadium found for venue: {venue_name}")
                return None
            
            coords = stadium.coordinates
            
            # Parse game date and time
            game_datetime = datetime.strptime(game_date, "%Y-%m-%d")
            
            # Default to 7:00 PM if no game time
            if game_time:
                try:
                    time_obj = datetime.strptime(game_time, "%H:%M").time()
                    game_datetime = datetime.combine(game_datetime.date(), time_obj)
                except ValueError:
                    # If time parsing fails, default to 7:00 PM
                    game_datetime = datetime.combine(game_datetime.date(), datetime.strptime("19:00", "%H:%M").time())
            else:
                game_datetime = datetime.combine(game_datetime.date(), datetime.strptime("19:00", "%H:%M").time())
            
            # Calculate 3-hour window around game time
            start_time = game_datetime - timedelta(hours=1.5)
            end_time = game_datetime + timedelta(hours=1.5)
            
            # Format for WeatherAPI
            date_str = game_date
            time_str = start_time.strftime("%H:%M")
            
            # Build API URL
            url = f"{self.weather_base_url}/history.json"
            params = {
                "key": self.weather_api_key,
                "q": f"{coords['lat']},{coords['lon']}",
                "dt": date_str,
                "hour": time_str
            }
            
            # Make API request
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather data
            if 'forecast' in data and 'forecastday' in data['forecast']:
                forecast_day = data['forecast']['forecastday'][0]
                
                # Get hourly data for the 3-hour window
                hourly_data = []
                for hour_data in forecast_day['hour']:
                    hour_time = datetime.strptime(hour_data['time'], "%Y-%m-%d %H:%M")
                    if start_time <= hour_time <= end_time:
                        hourly_data.append({
                            'time': hour_data['time'],
                            'temp_f': hour_data['temp_f'],
                            'condition': hour_data['condition']['text'],
                            'wind_mph': hour_data['wind_mph'],
                            'wind_dir': hour_data['wind_dir'],
                            'humidity': hour_data['humidity'],
                            'precip_in': hour_data['precip_in']
                        })
                
                if hourly_data:
                    # Calculate averages for the game window
                    avg_temp = sum(h['temp_f'] for h in hourly_data) / len(hourly_data)
                    avg_wind = sum(h['wind_mph'] for h in hourly_data) / len(hourly_data)
                    avg_humidity = sum(h['humidity'] for h in hourly_data) / len(hourly_data)
                    
                    # Get most common condition
                    conditions = [h['condition'] for h in hourly_data]
                    most_common_condition = max(set(conditions), key=conditions.count)
                    
                    return {
                        'temperature': round(avg_temp),
                        'conditions': most_common_condition,
                        'wind_speed': round(avg_wind),
                        'wind_direction': hourly_data[0]['wind_dir'],  # Use first hour's direction
                        'humidity': round(avg_humidity),
                        'hourly_data': hourly_data
                    }
            
            return None
            
        except Exception as e:
            print(f"Error getting weather for {venue_name} on {game_date}: {e}")
            return None
    
    def get_weather_summary(self, venue_name: str, game_date: str) -> Optional[str]:
        """
        Get a simple weather summary for display.
        """
        weather = self.get_weather_for_game(venue_name, game_date)
        if weather:
            return f"{weather['temperature']}°F, {weather['conditions']}, Wind: {weather['wind_speed']} mph"
        return None
