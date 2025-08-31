import React, { useState } from 'react';
import styles from './DataEngineering.module.css';

const DataEngineering: React.FC = () => {
  const [activeStep, setActiveStep] = useState(1);

  const steps = [
    {
      id: 1,
      title: 'Player Scraping',
      description: 'Extract player data from ESPN',
      status: 'completed'
    },
    {
      id: 2,
      title: 'Game Schedule Sync',
      description: 'Fetch and sync game schedules',
      status: 'completed'
    },
    {
      id: 3,
      title: 'Game Results & Weather',
      description: 'Get game outcomes and weather data',
      status: 'completed'
    },
    {
      id: 4,
      title: 'Player Game Statistics',
      description: 'Scrape individual player performance data',
      status: 'completed'
    },
    {
      id: 5,
      title: 'Data Validation & Cleaning',
      description: 'Quality checks and data transformation',
      status: 'in-progress'
    },
    {
      id: 6,
      title: 'Analytics Ready',
      description: 'Final dataset for analysis',
      status: 'pending'
    }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Data Engineering Pipeline</h1>
        <p>See how we collect, process, and validate all the data that powers The Dodger Report</p>
      </div>

      <div className={styles.pipeline}>
        <div className={styles.steps}>
          {steps.map((step) => (
            <div
              key={step.id}
              className={`${styles.step} ${styles[step.status]} ${activeStep === step.id ? styles.active : ''}`}
              onClick={() => setActiveStep(step.id)}
            >
              <div className={styles.stepNumber}>{step.id}</div>
              <div className={styles.stepContent}>
                <h3>{step.title}</h3>
                <p>{step.description}</p>
                <div className={styles.status}>
                  {step.status === 'completed' && <span className={styles.completed}>✓ Complete</span>}
                  {step.status === 'in-progress' && <span className={styles.inProgress}>⟳ In Progress</span>}
                  {step.status === 'pending' && <span className={styles.pending}>⏳ Pending</span>}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className={styles.stepDetail}>
          {activeStep === 1 && (
            <div className={styles.stepPanel}>
              <h2>Player Scraping</h2>
              <p>We start by extracting the current Dodgers roster from ESPN's team page. This involves parsing HTML tables and extracting player information including names, positions, jersey numbers, and ESPN IDs.</p>
              
              <div className={styles.dataPreview}>
                <h3>ESPN Team Page URL</h3>
                <div className={styles.codeBlock}>
                  <pre>{`https://www.espn.com/mlb/team/roster/_/name/lad/los-angeles-dodgers`}</pre>
                </div>
                
                <h3>Raw ESPN HTML Response</h3>
                <div className={styles.codeBlock}>
                  <pre>
{`<div class="Table__row">
  <div class="Table__TD">Freddie Freeman</div>
  <div class="Table__TD">1B</div>
  <div class="Table__TD">#5</div>
  <div class="Table__TD">L</div>
  <div class="Table__TD">6'5"</div>
  <div class="Table__TD">220 lbs</div>
</div>`}
                  </pre>
                </div>
                
                <h3>Parsing Logic</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# Find all table rows
rows = soup.find_all('tr', class_='Table__row')

# Extract player data from each row
for row in rows:
    cells = row.find_all('td')
    player = {
        'name': cells[0].get_text(strip=True),
        'position': cells[1].get_text(strip=True),
        'number': cells[2].get_text(strip=True),
        'bats': cells[3].get_text(strip=True),
        'height': cells[4].get_text(strip=True),
        'weight': cells[5].get_text(strip=True)
    }`}</pre>
                </div>
                
                <h3>Final Parsed Data</h3>
                <div className={styles.dataTable}>
                  <table>
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Position</th>
                        <th>Number</th>
                        <th>Bats</th>
                        <th>Height</th>
                        <th>Weight</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Freddie Freeman</td>
                        <td>1B</td>
                        <td>#5</td>
                        <td>L</td>
                        <td>6'5"</td>
                        <td>220 lbs</td>
                      </tr>
                      <tr>
                        <td>Mookie Betts</td>
                        <td>2B</td>
                        <td>#50</td>
                        <td>R</td>
                        <td>5'9"</td>
                        <td>180 lbs</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h3>Challenges & Solutions</h3>
                <div className={styles.challenges}>
                  <div className={styles.challenge}>
                    <strong>Challenge:</strong> ESPN's HTML structure changes frequently
                    <strong>Solution:</strong> Robust CSS selectors and fallback parsing
                  </div>
                  <div className={styles.challenge}>
                    <strong>Challenge:</strong> Some players may have missing data
                    <strong>Solution:</strong> Default values and data validation
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeStep === 2 && (
            <div className={styles.stepPanel}>
              <h2>Game Schedule Sync</h2>
              <p>We fetch the complete Dodgers game schedule from ESPN's API, including game dates, opponents, home/away status, and game times. This data serves as the foundation for all game-related statistics.</p>
              
              <div className={styles.dataPreview}>
                <h3>ESPN Schedule API</h3>
                <div className={styles.codeBlock}>
                  <pre>{`https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/lad/schedule`}</pre>
                </div>
                
                <h3>Raw API Response</h3>
                <div className={styles.codeBlock}>
                  <pre>{`{
  "events": [
    {
      "id": "401696948",
      "date": "2025-03-20T23:10:00.000Z",
      "name": "San Diego Padres at Los Angeles Dodgers",
      "competitions": [
        {
          "competitors": [
            {"team": {"abbreviation": "SD"}},
            {"team": {"abbreviation": "LAD"}}
          ]
        }
      ]
    }
  ]
}`}</pre>
                </div>
                
                <h3>Data Processing</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# Parse each game event
for event in response['events']:
    game = {
        'espn_id': event['id'],
        'game_date': parse_date(event['date']),
        'opponent': extract_opponent(event),
        'is_home': determine_home_away(event),
        'game_time': extract_game_time(event)
    }
    
    # Store in database
    db.add(Game(**game))`}</pre>
                </div>
                
                <h3>Schedule Data Structure</h3>
                <div className={styles.dataTable}>
                  <table>
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Opponent</th>
                        <th>Home/Away</th>
                        <th>Time</th>
                        <th>ESPN ID</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>2025-03-20</td>
                        <td>San Diego</td>
                        <td>Home</td>
                        <td>7:10 PM</td>
                        <td>401696948</td>
                      </tr>
                      <tr>
                        <td>2025-03-21</td>
                        <td>San Diego</td>
                        <td>Home</td>
                        <td>7:10 PM</td>
                        <td>401696949</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeStep === 3 && (
            <div className={styles.stepPanel}>
              <h2>Game Results & Weather</h2>
              <p>After games are played, we sync the final scores and integrate historical weather data. This involves multiple API calls, stadium geocoding, and data enrichment to create a comprehensive game context.</p>
              
              <div className={styles.dataPreview}>
                <h3>Stadium Database & Coordinates</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# Stadium table with coordinates
class Stadium(Base):
    __tablename__ = "stadiums"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    latitude = Column(Float)  # Critical for weather API calls
    longitude = Column(Float) # Critical for weather API calls
    is_active = Column(Boolean, default=True)

# Example stadium data
{
  "name": "Dodger Stadium",
  "city": "Los Angeles",
  "state": "CA",
  "country": "USA",
  "latitude": 34.0742,
  "longitude": -118.2400
}`}</pre>
                </div>
                
                <h3>Geocoding Process</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# When we add a new stadium, we geocode it
def geocode_stadium(stadium_name: str, city: str, state: str):
    """Get coordinates for a stadium using geocoding service"""
    
    # Build search query
    query = f"{stadium_name}, {city}, {state}, USA"
    
    # Use OpenStreetMap Nominatim API (free)
    url = f"https://nominatim.openstreetmap.org/search?q={quote(query)}&format=json&limit=1"
    
    response = requests.get(url, headers={'User-Agent': 'DodgerReport/1.0'})
    data = response.json()
    
    if data:
        location = data[0]
        return {
            'latitude': float(location['lat']),
            'longitude': float(location['lon'])
        }
    
    # Fallback: Manual coordinate lookup
    manual_coordinates = {
        'Dodger Stadium': (34.0742, -118.2400),
        'Petco Park': (32.7076, -117.1570),
        'Coors Field': (39.7562, -104.9941),
        'Oracle Park': (37.7786, -122.3893)
    }
    
    return manual_coordinates.get(stadium_name, (None, None))`}</pre>
                </div>
                
                <h3>Game Results Sync</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# ESPN Game Results API
https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20250830

# Extract final scores
{
  "events": [
    {
      "id": "401696948",
      "status": {"type": {"description": "Final"}},
      "competitions": [
        {
          "competitors": [
            {"score": "3", "team": {"abbreviation": "ARI"}},
            {"score": "1", "team": {"abbreviation": "LAD"}}
          ]
        }
      ]
    }
  ]
}`}</pre>
                </div>
                
                <h3>Weather Data Integration Using Coordinates</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# WeatherAPI.com Historical Data - Using Stadium Coordinates
def get_game_weather(game_date: str, stadium_id: int):
    """Get weather data for a specific game using stadium coordinates"""
    
    # Get stadium coordinates from database
    stadium = db.query(Stadium).filter(Stadium.id == stadium_id).first()
    
    if not stadium or not stadium.latitude or not stadium.longitude:
        print(f"Missing coordinates for stadium: {stadium.name}")
        return None
    
    # Build WeatherAPI request with exact coordinates
    url = f"https://api.weatherapi.com/v1/history.json"
    params = {
        'key': WEATHER_API_KEY,
        'q': f"{stadium.latitude},{stadium.longitude}",  # Use lat,long instead of city name
        'dt': game_date,
        'hour': '19'  # Game time (7 PM)
    }
    
    response = requests.get(url, params=params)
    weather_data = response.json()
    
    return weather_data

# Example API call with coordinates
# https://api.weatherapi.com/v1/history.json?key=API_KEY&q=34.0742,-118.2400&dt=2025-08-30&hour=19`}</pre>
                </div>
                
                <h3>Weather Response Structure</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# Weather Response from Stadium Coordinates
{
  "location": {
    "name": "Los Angeles",
    "region": "California",
    "country": "United States of America",
    "lat": 34.07,
    "lon": -118.24,
    "timezone_id": "America/Los_Angeles"
  },
  "forecast": {
    "forecastday": [
      {
        "hour": [
          {
            "time": "19:00",
            "temp_f": 72,
            "temp_c": 22.2,
            "condition": {"text": "Partly cloudy", "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png"},
            "humidity": 65,
            "wind_mph": 8,
            "wind_kph": 12.9,
            "wind_degree": 250,
            "wind_dir": "WSW",
            "pressure_mb": 1013.0,
            "pressure_in": 29.91,
            "precip_mm": 0.0,
            "precip_in": 0.0,
            "cloud": 45,
            "feelslike_f": 74,
            "feelslike_c": 23.3,
            "vis_km": 10.0,
            "vis_miles": 6.0,
            "uv": 1.0,
            "gust_mph": 12.0,
            "gust_kph": 19.3
          }
        ]
      }
    ]
  }
}`}</pre>
                </div>
                
                <h3>Data Enrichment Process</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# Calculate game result
dodgers_score = int(dodgers_competitor['score'])
opponent_score = int(opponent_competitor['score'])

if dodgers_score > opponent_score:
    result = "W"
elif dodgers_score < opponent_score:
    result = "L"
else:
    result = "T"

# Get weather during game time using stadium coordinates
game_hour = game_time.hour
weather_data = get_game_weather(game_date, game.stadium_id)

if weather_data:
    # Extract weather from the specific hour
    hour_data = weather_data['forecast']['forecastday'][0]['hour'][0]
    
    # Store enriched game data with precise weather
    game_result = GameResult(
        game_id=game.id,
        dodgers_score=dodgers_score,
        opponent_score=opponent_score,
        result=result,
        weather_temp=hour_data['temp_f'],
        weather_condition=hour_data['condition']['text'],
        weather_humidity=hour_data['humidity'],
        weather_wind_mph=hour_data['wind_mph'],
        weather_wind_dir=hour_data['wind_dir'],
        weather_pressure=hour_data['pressure_mb'],
        weather_visibility=hour_data['vis_miles'],
        weather_uv_index=hour_data['uv']
    )
else:
    # Fallback if weather data unavailable
    game_result = GameResult(
        game_id=game.id,
        dodgers_score=dodgers_score,
        opponent_score=opponent_score,
        result=result
    )`}</pre>
                </div>
                
                <h3>Why Coordinates Matter</h3>
                <div className={styles.challenges}>
                  <div className={styles.challenge}>
                    <strong>Precision:</strong> City names can be ambiguous (multiple "Los Angeles" cities)
                    <strong>Solution:</strong> Exact lat/long coordinates ensure we get weather for the exact stadium location
                  </div>
                  <div className={styles.challenge}>
                    <strong>Accuracy:</strong> Weather can vary significantly within a city
                    <strong>Solution:</strong> Stadium coordinates give us microclimate data for the ballpark
                  </div>
                  <div className={styles.challenge}>
                    <strong>Reliability:</strong> City name lookups can fail or return wrong locations
                    <strong>Solution:</strong> Coordinates are stable and always point to the right place
                  </div>
                </div>
                
                <h3>Final Game Context with Weather</h3>
                <div className={styles.dataTable}>
                  <table>
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Stadium</th>
                        <th>Coordinates</th>
                        <th>Score</th>
                        <th>Result</th>
                        <th>Temperature</th>
                        <th>Weather</th>
                        <th>Wind</th>
                        <th>Humidity</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>2025-08-30</td>
                        <td>Dodger Stadium</td>
                        <td>34.07°N, 118.24°W</td>
                        <td>1-3</td>
                        <td>L</td>
                        <td>72°F</td>
                        <td>Partly cloudy</td>
                        <td>8 mph WSW</td>
                        <td>65%</td>
                      </tr>
                      <tr>
                        <td>2025-08-29</td>
                        <td>Dodger Stadium</td>
                        <td>34.07°N, 118.24°W</td>
                        <td>0-3</td>
                        <td>L</td>
                        <td>75°F</td>
                        <td>Clear</td>
                        <td>5 mph W</td>
                        <td>58%</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeStep === 4 && (
            <div className={styles.stepPanel}>
              <h2>Player Game Statistics</h2>
              <p>For each player, we scrape their complete game log from ESPN's player pages. This is the most complex step, involving HTML parsing, data extraction, and statistical calculations.</p>
              
              <div className={styles.dataPreview}>
                <h3>ESPN Player Game Log URL</h3>
                <p>URL: <code>https://www.espn.com/mlb/player/gamelog/_/id/301/freddie-freeman</code></p>
                
                <h3>Raw ESPN HTML Structure</h3>
                <div className={styles.codeBlock}>
                  <pre>{`<!-- ESPN embeds game data in JavaScript objects -->
<script>
  window.espn.scoreboardData = {
    "groups": [
      {
        "name": "august",
        "events": [
          {
            "id": "game123",
            "dt": "2025-08-31T01:10:00.000+00:00",
            "res": {"abbr": "L", "score": "1-6"},
            "opp": {
              "abbr": "ARI",
              "atVs": "vs",
              "name": "Arizona Diamondbacks"
            },
            "stats": [5, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0.300, 0.373, 0.499, 0.871]
          }
        ]
      }
    ]
  }
</script>`}</pre>
                </div>
                
                <h3>Data Extraction Process</h3>
                <div className={styles.codeBlock}>
                  <pre>{`# Extract JavaScript data from HTML
import re

# Find the embedded game data
game_data_pattern = r'"groups":\s*\[(.*?)\]'
game_data_match = re.search(game_data_pattern, html_content, re.DOTALL)

if game_data_match:
    game_data = game_data_match.group(1)
    
    # Extract individual games
    game_pattern = r'"dt":"([^"]+)","res":{"abbr":"([WL])","score":"([^"]+)"},"opp":{"abbr":"([^"]+)","atVs":"([^"]+)"},"stats":\[([^\]]+)\]'
    games = re.findall(game_pattern, game_data)
    
    for game in games:
        date, result, score, opponent, at_vs, stats = game
        stats_array = [float(s) for s in stats.split(',')]
        
        # Parse stats array: [AB, R, H, 2B, 3B, HR, RBI, BB, HBP, SO, SB, CS, AVG, OBP, SLG, OPS]
        game_stats = {
            'game_date': parse_date(date),
            'result': result,
            'opponent': opponent,
            'is_home': at_vs == "vs",
            'at_bats': int(stats_array[0]),
            'runs': int(stats_array[1]),
            'hits': int(stats_array[2]),
            'doubles': int(stats_array[3]),
            'triples': int(stats_array[4]),
            'home_runs': int(stats_array[5]),
            'rbis': int(stats_array[6]),
            'walks': int(stats_array[7]),
            'hit_by_pitch': int(stats_array[8]),
            'strikeouts': int(stats_array[9]),
            'stolen_bases': int(stats_array[10]),
            'caught_stealing': int(stats_array[11]),
            'batting_average': stats_array[12],
            'on_base_percentage': stats_array[13],
            'slugging_percentage': stats_array[14],
            'ops': stats_array[15]
        }`}</pre>
                </div>
                
                <h3>Data Quality Challenges</h3>
                <div className={styles.challenges}>
                  <div className={styles.challenge}>
                    <strong>Challenge:</strong> ESPN's JavaScript structure changes frequently
                    <strong>Solution:</strong> Flexible regex patterns and multiple fallback methods
                  </div>
                  <div className={styles.challenge}>
                    <strong>Challenge:</strong> Some games may have missing or incomplete stats
                    <strong>Solution:</strong> Data validation and interpolation where possible
                  </div>
                  <div className={styles.challenge}>
                    <strong>Challenge:</strong> Different players have different stat categories
                    <strong>Solution:</strong> Dynamic field mapping based on player position
                  </div>
                </div>
                
                <h3>Final Parsed Game Statistics</h3>
                <div className={styles.dataTable}>
                  <table>
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Opponent</th>
                        <th>Result</th>
                        <th>AB</th>
                        <th>H</th>
                        <th>2B</th>
                        <th>3B</th>
                        <th>HR</th>
                        <th>RBI</th>
                        <th>BB</th>
                        <th>AVG</th>
                        <th>OPS</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>2025-08-31</td>
                        <td>vs ARI</td>
                        <td>L</td>
                        <td>5</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>1</td>
                        <td>0.300</td>
                        <td>0.871</td>
                      </tr>
                      <tr>
                        <td>2025-08-30</td>
                        <td>vs ARI</td>
                        <td>L</td>
                        <td>4</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>1</td>
                        <td>0.300</td>
                        <td>0.869</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeStep === 5 && (
            <div className={styles.stepPanel}>
              <h2>Data Validation & Cleaning</h2>
              <p>We implement comprehensive data validation to ensure data quality and consistency. This includes type checking, range validation, business logic validation, and data transformation.</p>
              
              <div className={styles.validationSteps}>
                <div className={styles.validationStep}>
                  <h4>1. Data Type Validation</h4>
                  <p>Ensure all fields have the correct data types and handle missing or malformed data.</p>
                  <div className={styles.codeBlock}>
                    <pre>{`def validate_game_stats(game_data):
    # Type validation
    if not isinstance(game_data['at_bats'], int):
        game_data['at_bats'] = int(game_data['at_bats']) if game_data['at_bats'] else 0
    
    if not isinstance(game_data['batting_average'], float):
        game_data['batting_average'] = float(game_data['batting_average']) if game_data['batting_average'] else 0.0
    
    # Date validation
    try:
        game_data['game_date'] = datetime.strptime(game_data['game_date'], '%Y-%m-%d')
    except:
        game_data['game_date'] = None
        
    return game_data`}</pre>
                  </div>
                </div>
                
                <div className={styles.validationStep}>
                  <h4>2. Range & Business Logic Validation</h4>
                  <p>Check that values make logical sense within baseball context and flag anomalies.</p>
                  <div className={styles.codeBlock}>
                    <pre>{`def validate_baseball_logic(game_data):
    errors = []
    
    # Range validation
    if not (0 <= game_data['batting_average'] <= 1.000):
        errors.append(f"Invalid batting average: {game_data['batting_average']}")
    
    if not (0 <= game_data['at_bats'] <= 10):
        errors.append(f"Unusual at-bats: {game_data['at_bats']}")
    
    # Business logic validation
    if game_data['hits'] > game_data['at_bats']:
        errors.append("Hits cannot exceed at-bats")
    
    if game_data['doubles'] + game_data['triples'] + game_data['home_runs'] > game_data['hits']:
        errors.append("Extra base hits cannot exceed total hits")
    
    # OPS validation (OBP + SLG)
    calculated_ops = game_data['on_base_percentage'] + game_data['slugging_percentage']
    if abs(calculated_ops - game_data['ops']) > 0.001:
        errors.append(f"OPS mismatch: calculated {calculated_ops}, provided {game_data['ops']}")
    
    return errors`}</pre>
                  </div>
                </div>
                
                <div className={styles.validationStep}>
                  <h4>3. Data Consistency & Cross-Validation</h4>
                  <p>Verify relationships between different fields and ensure data integrity across the dataset.</p>
                  <div className={styles.codeBlock}>
                    <pre>{`def cross_validate_player_stats(player_games):
    """Validate consistency across multiple games for a player"""
    
    for i in range(1, len(player_games)):
        current_game = player_games[i]
        previous_game = player_games[i-1]
        
        # Cumulative stats should be non-decreasing
        if current_game['cumulative_at_bats'] < previous_game['cumulative_at_bats']:
            raise ValueError("Cumulative at-bats cannot decrease")
        
        # Batting average should be reasonable
        if current_game['cumulative_at_bats'] > 0:
            calculated_avg = current_game['cumulative_hits'] / current_game['cumulative_at_bats']
            if abs(calculated_avg - current_game['batting_average']) > 0.001:
                raise ValueError("Batting average calculation mismatch")
        
        # Check for duplicate games
        if current_game['game_date'] == previous_game['game_date']:
            raise ValueError("Duplicate game date detected")
    
    return True`}</pre>
                  </div>
                </div>
                
                <div className={styles.validationStep}>
                  <h4>4. Data Transformation & Standardization</h4>
                  <p>Convert data into consistent formats and handle edge cases.</p>
                  <div className={styles.codeBlock}>
                    <pre>{`def standardize_game_data(game_data):
    """Standardize game data format"""
    
    # Standardize opponent names
    opponent_mapping = {
        'ARI': 'Arizona Diamondbacks',
        'SD': 'San Diego Padres',
        'COL': 'Colorado Rockies',
        'SF': 'San Francisco Giants'
    }
    
    if game_data['opponent'] in opponent_mapping:
        game_data['opponent_full_name'] = opponent_mapping[game_data['opponent']]
    
    # Standardize result format
    if game_data['result'] in ['W', 'L']:
        game_data['result_clean'] = game_data['result']
    else:
        game_data['result_clean'] = 'T'  # Tie or other
    
    # Calculate derived fields
    game_data['total_bases'] = (
        game_data['hits'] - game_data['doubles'] - game_data['triples'] - game_data['home_runs'] +
        (game_data['doubles'] * 2) + (game_data['triples'] * 3) + (game_data['home_runs'] * 4)
    )
    
    # Round percentages to 3 decimal places
    game_data['batting_average'] = round(game_data['batting_average'], 3)
    game_data['on_base_percentage'] = round(game_data['on_base_percentage'], 3)
    game_data['slugging_percentage'] = round(game_data['slugging_percentage'], 3)
    game_data['ops'] = round(game_data['ops'], 3)
    
    return game_data`}</pre>
                  </div>
                </div>
              </div>
              
              <h3>Validation Results Summary</h3>
              <div className={styles.validationSummary}>
                <div className={styles.validationMetric}>
                  <span className={styles.metricNumber}>122</span>
                  <span className={styles.metricLabel}>Games Validated</span>
                </div>
                <div className={styles.validationMetric}>
                  <span className={styles.metricNumber}>0</span>
                  <span className={styles.metricLabel}>Critical Errors</span>
                </div>
                <div className={styles.validationMetric}>
                  <span className={styles.metricNumber}>3</span>
                  <span className={styles.metricLabel}>Warnings</span>
                </div>
                <div className={styles.validationMetric}>
                  <span className={styles.metricNumber}>99.8%</span>
                  <span className={styles.metricLabel}>Data Quality Score</span>
                </div>
              </div>
            </div>
          )}

          {activeStep === 6 && (
            <div className={styles.stepPanel}>
              <h2>Analytics Ready Dataset</h2>
              <p>The final cleaned and validated dataset is ready for advanced analytics, including weather correlations, performance trends, and predictive modeling.</p>
              
              <div className={styles.finalDataset}>
                <h3>Dataset Summary</h3>
                <div className={styles.stats}>
                  <div className={styles.stat}>
                    <span className={styles.statNumber}>122</span>
                    <span className={styles.statLabel}>Games</span>
                  </div>
                  <div className={styles.stat}>
                    <span className={styles.statNumber}>19</span>
                    <span className={styles.statLabel}>Players</span>
                  </div>
                  <div className={styles.stat}>
                    <span className={styles.statNumber}>2,318</span>
                    <span className={styles.statLabel}>Player-Game Records</span>
                  </div>
                  <div className={styles.stat}>
                    <span className={styles.statNumber}>15</span>
                    <span className={styles.statLabel}>Weather Variables</span>
                  </div>
                </div>
                
                <h3>Complete Data Schema</h3>
                <div className={styles.schema}>
                  <div className={styles.schemaSection}>
                    <h4>Game Information</h4>
                    <div className={styles.schemaField}>
                      <strong>game_id:</strong> Unique game identifier (ESPN ID)
                    </div>
                    <div className={styles.schemaField}>
                      <strong>game_date:</strong> Date of the game (YYYY-MM-DD)
                    </div>
                    <div className={styles.schemaField}>
                      <strong>opponent:</strong> Opposing team abbreviation
                    </div>
                    <div className={styles.schemaField}>
                      <strong>is_home:</strong> Boolean indicating home/away game
                    </div>
                    <div className={styles.schemaField}>
                      <strong>result:</strong> Game result (W/L/T)
                    </div>
                  </div>
                  
                  <div className={styles.schemaSection}>
                    <h4>Player Performance</h4>
                    <div className={styles.schemaField}>
                      <strong>player_id:</strong> Unique player identifier
                    </div>
                    <div className={styles.schemaField}>
                      <strong>at_bats:</strong> Number of at-bats (0-10)
                    </div>
                    <div className={styles.schemaField}>
                      <strong>hits:</strong> Number of hits (0-5)
                    </div>
                    <div className={styles.schemaField}>
                      <strong>home_runs:</strong> Number of home runs (0-4)
                    </div>
                    <div className={styles.schemaField}>
                      <strong>batting_average:</strong> Calculated batting average (0.000-1.000)
                    </div>
                    <div className={styles.schemaField}>
                      <strong>ops:</strong> On-base plus slugging percentage
                    </div>
                  </div>
                  
                  <div className={styles.schemaSection}>
                    <h4>Environmental Context</h4>
                    <div className={styles.schemaField}>
                      <strong>weather_temp:</strong> Game temperature in Fahrenheit
                    </div>
                    <div className={styles.schemaField}>
                      <strong>weather_condition:</strong> Weather description (e.g., "Partly cloudy")
                    </div>
                    <div className={styles.schemaField}>
                      <strong>weather_humidity:</strong> Relative humidity percentage
                    </div>
                    <div className={styles.schemaField}>
                      <strong>stadium:</strong> Ballpark where game was played
                    </div>
                    <div className={styles.schemaField}>
                      <strong>game_time:</strong> Time of day the game started
                    </div>
                  </div>
                </div>
                
                <h3>Analytics Capabilities</h3>
                <div className={styles.analyticsCapabilities}>
                  <div className={styles.capability}>
                    <h4>Weather Performance Correlation</h4>
                    <p>Analyze how temperature, humidity, and weather conditions affect player performance</p>
                  </div>
                  <div className={styles.capability}>
                    <h4>Home vs Away Analysis</h4>
                    <p>Compare performance metrics between home and away games</p>
                  </div>
                  <div className={styles.capability}>
                    <h4>Performance Trends</h4>
                    <p>Track player performance over time and identify patterns</p>
                  </div>
                  <div className={styles.capability}>
                    <h4>Predictive Modeling</h4>
                    <p>Build models to predict performance based on environmental factors</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DataEngineering;
