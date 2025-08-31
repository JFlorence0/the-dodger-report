import React, { useState, useEffect, useCallback } from 'react';
import styles from './PlayerAnalytics.module.css';

interface PlayerAnalyticsProps {
  playerId: number;
  playerName: string;
}

interface WeatherFilter {
  temperature: {
    min: number | null;
    max: number | null;
  };
  conditions: string[];
  windSpeed: {
    min: number | null;
    max: number | null;
  };
}

interface GameFilter {
  isHome: boolean | null;
  opponent: string[];
  timeOfDay: string[];
  daysBetweenGames: {
    min: number | null;
    max: number | null;
  };
}

interface FilteredStats {
  gamesPlayed: number;
  atBats: number;
  hits: number;
  doubles: number;
  triples: number;
  homeRuns: number;
  rbis: number;
  walks: number;
  strikeouts: number;
  stolenBases: number;
  caughtStealing: number;
  hitByPitch: number;
  battingAverage: number;
  onBasePercentage: number;
  sluggingPercentage: number;
  ops: number;
}

const PlayerAnalytics: React.FC<PlayerAnalyticsProps> = ({ playerId, playerName }) => {
  const [weatherFilter, setWeatherFilter] = useState<WeatherFilter>({
    temperature: { min: null, max: null },
    conditions: [],
    windSpeed: { min: null, max: null }
  });

  const [gameFilter, setGameFilter] = useState<GameFilter>({
    isHome: null,
    opponent: [],
    timeOfDay: [],
    daysBetweenGames: { min: null, max: null }
  });

  const [filteredStats, setFilteredStats] = useState<FilteredStats | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeFilters, setActiveFilters] = useState<string[]>([]);

  // Weather condition options
  const weatherConditions = [
    'Clear', 'Partly Cloudy', 'Cloudy', 'Rain', 'Light Rain', 
    'Heavy Rain', 'Snow', 'Fog', 'Mist', 'Overcast'
  ];

  // Time of day options
  const timeOfDayOptions = [
    'Day Game', 'Night Game', 'Twilight', 'Afternoon', 'Evening'
  ];

  // Mock opponent teams
  const opponentTeams = [
    'ARI', 'SD', 'COL', 'CIN', 'BOS', 'NYM', 'PHI', 'WAS', 'BAL', 'TOR',
    'SF', 'OAK', 'LAA', 'HOU', 'TEX', 'KC', 'MIN', 'CWS', 'CLE', 'DET'
  ];

  const getFilterCount = useCallback((): number => {
    let count = 0;
    if (weatherFilter.temperature.min !== null || weatherFilter.temperature.max !== null) count++;
    if (weatherFilter.conditions.length > 0) count++;
    if (weatherFilter.windSpeed.min !== null || weatherFilter.windSpeed.max !== null) count++;
    if (gameFilter.isHome !== null) count++;
    if (gameFilter.opponent.length > 0) count++;
    if (gameFilter.timeOfDay.length > 0) count++;
    if (gameFilter.daysBetweenGames.min !== null || gameFilter.daysBetweenGames.max !== null) count++;
    return count;
  }, [weatherFilter, gameFilter]);

  const generateMockFilteredStats = useCallback((): FilteredStats => {
    // Generate realistic stats based on filter complexity
    const filterCount = getFilterCount();
    const baseMultiplier = Math.max(0.3, 1 - (filterCount * 0.1)); // More filters = fewer games
    
    const gamesPlayed = Math.floor(Math.random() * 15 * baseMultiplier) + 5;
    const atBats = gamesPlayed * (Math.floor(Math.random() * 3) + 2);
    const hits = Math.floor(atBats * (0.25 + Math.random() * 0.15)); // .250 to .400 range
    
    return {
      gamesPlayed,
      atBats,
      hits,
      doubles: Math.floor(hits * 0.3),
      triples: Math.floor(hits * 0.05),
      homeRuns: Math.floor(hits * 0.15),
      rbis: Math.floor(hits * 0.8),
      walks: Math.floor(atBats * 0.1),
      strikeouts: Math.floor(atBats * 0.2),
      stolenBases: Math.floor(gamesPlayed * 0.3),
      caughtStealing: Math.floor(gamesPlayed * 0.1),
      hitByPitch: Math.floor(gamesPlayed * 0.2),
      battingAverage: atBats > 0 ? parseFloat((hits / atBats).toFixed(3)) : 0,
      onBasePercentage: (atBats + Math.floor(atBats * 0.1) + Math.floor(gamesPlayed * 0.2)) > 0 
        ? parseFloat(((hits + Math.floor(atBats * 0.1) + Math.floor(gamesPlayed * 0.2)) / (atBats + Math.floor(atBats * 0.1) + Math.floor(gamesPlayed * 0.2))).toFixed(3))
        : 0,
      sluggingPercentage: atBats > 0 ? parseFloat((hits / atBats * 1.2).toFixed(3)) : 0,
      ops: 0 // Will be calculated below
    };
  }, [getFilterCount]);

  const applyFilters = useCallback(async () => {
    setIsLoading(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Generate mock filtered stats based on current filters
    const mockStats = generateMockFilteredStats();
    setFilteredStats(mockStats);
    
    setIsLoading(false);
  }, [generateMockFilteredStats]);

  const updateActiveFilters = useCallback(() => {
    const filters: string[] = [];
    
    if (weatherFilter.temperature.min !== null || weatherFilter.temperature.max !== null) {
      const tempRange = [];
      if (weatherFilter.temperature.min !== null) tempRange.push(`${weatherFilter.temperature.min}°F+`);
      if (weatherFilter.temperature.max !== null) tempRange.push(`up to ${weatherFilter.temperature.max}°F`);
      filters.push(`Temp: ${tempRange.join(' to ')}`);
    }
    
    if (weatherFilter.conditions.length > 0) {
      filters.push(`Weather: ${weatherFilter.conditions.join(', ')}`);
    }
    
    if (weatherFilter.windSpeed.min !== null || weatherFilter.windSpeed.max !== null) {
      const windRange = [];
      if (weatherFilter.windSpeed.min !== null) windRange.push(`${weatherFilter.windSpeed.min}mph+`);
      if (weatherFilter.windSpeed.max !== null) windRange.push(`up to ${weatherFilter.windSpeed.max}mph`);
      filters.push(`Wind: ${windRange.join(' to ')}`);
    }
    
    if (gameFilter.isHome !== null) {
      filters.push(gameFilter.isHome ? 'Home Games' : 'Away Games');
    }
    
    if (gameFilter.opponent.length > 0) {
      filters.push(`vs ${gameFilter.opponent.join(', ')}`);
    }
    
    if (gameFilter.timeOfDay.length > 0) {
      filters.push(`Time: ${gameFilter.timeOfDay.join(', ')}`);
    }
    
    if (gameFilter.daysBetweenGames.min !== null || gameFilter.daysBetweenGames.max !== null) {
      const daysRange = [];
      if (gameFilter.daysBetweenGames.min !== null) daysRange.push(`${gameFilter.daysBetweenGames.min}+ days`);
      if (gameFilter.daysBetweenGames.max !== null) daysRange.push(`up to ${gameFilter.daysBetweenGames.max} days`);
      filters.push(`Rest: ${daysRange.join(' to ')}`);
    }
    
    setActiveFilters(filters);
  }, [weatherFilter, gameFilter]);

  const clearAllFilters = () => {
    setWeatherFilter({
      temperature: { min: null, max: null },
      conditions: [],
      windSpeed: { min: null, max: null }
    });
    setGameFilter({
      isHome: null,
      opponent: [],
      timeOfDay: [],
      daysBetweenGames: { min: null, max: null }
    });
    setFilteredStats(null);
    setActiveFilters([]);
  };

  const removeFilter = (filterIndex: number) => {
    const filter = activeFilters[filterIndex];
    
    // Remove the specific filter based on its content
    if (filter.startsWith('Temp:')) {
      setWeatherFilter(prev => ({ ...prev, temperature: { min: null, max: null } }));
    } else if (filter.startsWith('Weather:')) {
      setWeatherFilter(prev => ({ ...prev, conditions: [] }));
    } else if (filter.startsWith('Wind:')) {
      setWeatherFilter(prev => ({ ...prev, windSpeed: { min: null, max: null } }));
    } else if (filter.startsWith('Home Games') || filter.startsWith('Away Games')) {
      setGameFilter(prev => ({ ...prev, isHome: null }));
    } else if (filter.startsWith('vs ')) {
      setGameFilter(prev => ({ ...prev, opponent: [] }));
    } else if (filter.startsWith('Time:')) {
      setGameFilter(prev => ({ ...prev, timeOfDay: [] }));
    } else if (filter.startsWith('Rest:')) {
      setGameFilter(prev => ({ ...prev, daysBetweenGames: { min: null, max: null } }));
    }
  };

  useEffect(() => {
    updateActiveFilters();
  }, [weatherFilter, gameFilter, updateActiveFilters]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Performance Analytics</h2>
        <p>Filter and analyze {playerName}'s performance by various game conditions</p>
      </div>

      {/* Filter Controls */}
      <div className={styles.filtersSection}>
        <div className={styles.filterGroup}>
          <h3>Weather Conditions</h3>
          
          <div className={styles.filterRow}>
            <label>Temperature Range (°F):</label>
            <div className={styles.rangeInputs}>
              <input
                type="number"
                placeholder="Min"
                value={weatherFilter.temperature.min || ''}
                onChange={(e) => setWeatherFilter(prev => ({
                  ...prev,
                  temperature: { ...prev.temperature, min: e.target.value ? Number(e.target.value) : null }
                }))}
                className={styles.numberInput}
              />
              <span>to</span>
              <input
                type="number"
                placeholder="Max"
                value={weatherFilter.temperature.max || ''}
                onChange={(e) => setWeatherFilter(prev => ({
                  ...prev,
                  temperature: { ...prev.temperature, max: e.target.value ? Number(e.target.value) : null }
                }))}
                className={styles.numberInput}
              />
            </div>
          </div>

          <div className={styles.filterRow}>
            <label>Weather Conditions:</label>
            <div className={styles.checkboxGroup}>
              {weatherConditions.map(condition => (
                <label key={condition} className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={weatherFilter.conditions.includes(condition)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setWeatherFilter(prev => ({
                          ...prev,
                          conditions: [...prev.conditions, condition]
                        }));
                      } else {
                        setWeatherFilter(prev => ({
                          ...prev,
                          conditions: prev.conditions.filter(c => c !== condition)
                        }));
                      }
                    }}
                  />
                  {condition}
                </label>
              ))}
            </div>
          </div>

          <div className={styles.filterRow}>
            <label>Wind Speed (mph):</label>
            <div className={styles.rangeInputs}>
              <input
                type="number"
                placeholder="Min"
                value={weatherFilter.windSpeed.min || ''}
                onChange={(e) => setWeatherFilter(prev => ({
                  ...prev,
                  windSpeed: { ...prev.windSpeed, min: e.target.value ? Number(e.target.value) : null }
                }))}
                className={styles.numberInput}
              />
              <span>to</span>
              <input
                type="number"
                placeholder="Max"
                value={weatherFilter.windSpeed.max || ''}
                onChange={(e) => setWeatherFilter(prev => ({
                  ...prev,
                  windSpeed: { ...prev.windSpeed, max: e.target.value ? Number(e.target.value) : null }
                }))}
                className={styles.numberInput}
              />
            </div>
          </div>
        </div>

        <div className={styles.filterGroup}>
          <h3>Game Context</h3>
          
          <div className={styles.filterRow}>
            <label>Home/Away:</label>
            <div className={styles.radioGroup}>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="homeAway"
                  checked={gameFilter.isHome === true}
                  onChange={() => setGameFilter(prev => ({ ...prev, isHome: true }))}
                />
                Home Games
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="homeAway"
                  checked={gameFilter.isHome === false}
                  onChange={() => setGameFilter(prev => ({ ...prev, isHome: false }))}
                />
                Away Games
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="homeAway"
                  checked={gameFilter.isHome === null}
                  onChange={() => setGameFilter(prev => ({ ...prev, isHome: null }))}
                />
                All Games
              </label>
            </div>
          </div>

          <div className={styles.filterRow}>
            <label>Opponents:</label>
            <div className={styles.checkboxGroup}>
              {opponentTeams.map(team => (
                <label key={team} className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={gameFilter.opponent.includes(team)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setGameFilter(prev => ({
                          ...prev,
                          opponent: [...prev.opponent, team]
                        }));
                      } else {
                        setGameFilter(prev => ({
                          ...prev,
                          opponent: prev.opponent.filter(t => t !== team)
                        }));
                      }
                    }}
                  />
                  {team}
                </label>
              ))}
            </div>
          </div>

          <div className={styles.filterRow}>
            <label>Time of Day:</label>
            <div className={styles.checkboxGroup}>
              {timeOfDayOptions.map(time => (
                <label key={time} className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={gameFilter.timeOfDay.includes(time)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setGameFilter(prev => ({
                          ...prev,
                          timeOfDay: [...prev.timeOfDay, time]
                        }));
                      } else {
                        setGameFilter(prev => ({
                          ...prev,
                          timeOfDay: prev.timeOfDay.filter(t => t !== time)
                        }));
                      }
                    }}
                  />
                  {time}
                </label>
              ))}
            </div>
          </div>

          <div className={styles.filterRow}>
            <label>Days Between Games:</label>
            <div className={styles.rangeInputs}>
              <input
                type="number"
                placeholder="Min"
                value={gameFilter.daysBetweenGames.min || ''}
                onChange={(e) => setGameFilter(prev => ({
                  ...prev,
                  daysBetweenGames: { ...prev.daysBetweenGames, min: e.target.value ? Number(e.target.value) : null }
                }))}
                className={styles.numberInput}
              />
              <span>to</span>
              <input
                type="number"
                placeholder="Max"
                value={gameFilter.daysBetweenGames.max || ''}
                onChange={(e) => setGameFilter(prev => ({
                  ...prev,
                  daysBetweenGames: { ...prev.daysBetweenGames, max: e.target.value ? Number(e.target.value) : null }
                }))}
                className={styles.numberInput}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className={styles.actions}>
        <button 
          onClick={applyFilters} 
          className={styles.applyButton}
          disabled={isLoading}
        >
          {isLoading ? 'Analyzing...' : 'Apply Filters & Analyze'}
        </button>
        <button onClick={clearAllFilters} className={styles.clearButton}>
          Clear All Filters
        </button>
      </div>

      {/* Active Filters Display */}
      {activeFilters.length > 0 && (
        <div className={styles.activeFilters}>
          <h4>Active Filters:</h4>
          <div className={styles.filterTags}>
            {activeFilters.map((filter, index) => (
              <span key={index} className={styles.filterTag}>
                {filter}
                <button 
                  onClick={() => removeFilter(index)}
                  className={styles.removeFilter}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Results Display */}
      {filteredStats && (
        <div className={styles.resultsSection}>
          <h3>Performance Results</h3>
          <p className={styles.resultsSummary}>
            Based on {filteredStats.gamesPlayed} games with current filters
          </p>
          
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <h4>Games & At-Bats</h4>
              <div className={styles.statValue}>{filteredStats.gamesPlayed}</div>
              <div className={styles.statLabel}>Games Played</div>
              <div className={styles.statValue}>{filteredStats.atBats}</div>
              <div className={styles.statLabel}>At-Bats</div>
            </div>

            <div className={styles.statCard}>
              <h4>Hits & Power</h4>
              <div className={styles.statValue}>{filteredStats.hits}</div>
              <div className={styles.statLabel}>Hits</div>
              <div className={styles.statValue}>{filteredStats.homeRuns}</div>
              <div className={styles.statLabel}>Home Runs</div>
            </div>

            <div className={styles.statCard}>
              <h4>Extra Base Hits</h4>
              <div className={styles.statValue}>{filteredStats.doubles}</div>
              <div className={styles.statLabel}>Doubles</div>
              <div className={styles.statValue}>{filteredStats.triples}</div>
              <div className={styles.statLabel}>Triples</div>
            </div>

            <div className={styles.statCard}>
              <h4>Plate Discipline</h4>
              <div className={styles.statValue}>{filteredStats.walks}</div>
              <div className={styles.statLabel}>Walks</div>
              <div className={styles.statValue}>{filteredStats.strikeouts}</div>
              <div className={styles.statLabel}>Strikeouts</div>
            </div>

            <div className={styles.statCard}>
              <h4>Batting Average</h4>
              <div className={styles.statValue}>{filteredStats.battingAverage.toFixed(3)}</div>
              <div className={styles.statLabel}>AVG</div>
            </div>

            <div className={styles.statCard}>
              <h4>On-Base %</h4>
              <div className={styles.statValue}>{filteredStats.onBasePercentage.toFixed(3)}</div>
              <div className={styles.statLabel}>OBP</div>
            </div>

            <div className={styles.statCard}>
              <h4>Slugging %</h4>
              <div className={styles.statValue}>{filteredStats.sluggingPercentage.toFixed(3)}</div>
              <div className={styles.statLabel}>SLG</div>
            </div>

            <div className={styles.statCard}>
              <h4>OPS</h4>
              <div className={styles.statValue}>{(filteredStats.onBasePercentage + filteredStats.sluggingPercentage).toFixed(3)}</div>
              <div className={styles.statLabel}>OPS</div>
            </div>
          </div>
        </div>
      )}

      {!filteredStats && (
        <div className={styles.placeholder}>
          <p>Apply filters above to see performance analytics</p>
        </div>
      )}
    </div>
  );
};

export default PlayerAnalytics;
