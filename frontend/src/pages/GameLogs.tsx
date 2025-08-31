import React, { useState, useEffect } from 'react';
import { Game } from '../types/Game';
import { gameService } from '../services/api';
import styles from './GameLogs.module.css';

const GameLogs: React.FC = () => {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('all'); // all, home, away, final, upcoming
  const [showAllGames, setShowAllGames] = useState(false);

  useEffect(() => {
    loadGames();
  }, []);

  const loadGames = async () => {
    try {
      setLoading(true);
      // Load 50 games by default to show more completed games
      const gamesData = await gameService.getGames(50);
      console.log('Loaded games:', gamesData.length, 'games:', gamesData);
      setGames(gamesData);
      setShowAllGames(false); // Reset to show only loaded games
    } catch (err) {
      setError('Failed to load games');
      console.error('Error loading games:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadAllGames = async () => {
    try {
      setLoading(true);
      // Load all 128 games
      const allGamesData = await gameService.getGames(200);
      setGames(allGamesData);
      setShowAllGames(true);
    } catch (err) {
      setError('Failed to load all games');
      console.error('Error loading all games:', err);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredGames = () => {
    switch (filter) {
      case 'home':
        return games.filter(game => game.home_team === 'Los Angeles Dodgers');
      case 'away':
        return games.filter(game => game.away_team === 'Los Angeles Dodgers');
      case 'final':
        return games.filter(game => game.is_final);
      case 'upcoming':
        return games.filter(game => !game.is_final);
      default:
        return games;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  };

  const getGameResult = (game: Game) => {

    console.log('Game RES', game);
    // Use the stored game_result if available, otherwise calculate it
    if (game.game_result) {
      return game.game_result;
    }
    
    // Fallback to calculation if no stored result
    if (!game.is_final || !game.home_score || !game.away_score) {
      return 'TBD';
    }
    
    if (game.home_team === 'Los Angeles Dodgers') {
      return game.home_score > game.away_score ? 'W' : 'L';
    } else {
      return game.away_score > game.home_score ? 'W' : 'L';
    }
  };

  const getResultClass = (result: string) => {
    if (result === 'W') return styles.win;
    if (result === 'L') return styles.loss;
    return styles.tbd;
  };

  const getVenueDisplay = (game: Game) => {
    if (game.home_team === 'Los Angeles Dodgers') {
      return `vs ${game.away_team}`;
    } else {
      return `@ ${game.home_team}`;
    }
  };

  const getWeatherEmoji = (conditions: string, temp: number) => {
    const condition = conditions.toLowerCase();
    
    // Temperature-based emojis
    if (temp >= 90) return '🔥'; // Hot
    if (temp >= 80) return '☀️'; // Warm
    if (temp >= 70) return '🌤️'; // Nice
    if (temp >= 60) return '⛅'; // Cool
    if (temp >= 50) return '🌥️'; // Chilly
    if (temp < 50) return '❄️'; // Cold
    
    // Condition-based emojis (fallback)
    if (condition.includes('sunny') || condition.includes('clear')) return '☀️';
    if (condition.includes('cloudy') || condition.includes('overcast')) return '☁️';
    if (condition.includes('rain') || condition.includes('drizzle')) return '🌧️';
    if (condition.includes('snow')) return '❄️';
    if (condition.includes('fog') || condition.includes('mist')) return '🌫️';
    if (condition.includes('thunder') || condition.includes('storm')) return '⛈️';
    if (condition.includes('wind')) return '💨';
    
    return '🌤️'; // Default
  };

  const getWeatherDisplay = (game: Game) => {
    if (game.weather_temp && game.weather_conditions) {
      const emoji = getWeatherEmoji(game.weather_conditions, game.weather_temp);
      let display = `${emoji} ${game.weather_temp}°F`;
      
      // Add wind info if available (only if significant wind)
      if (game.wind_speed && game.wind_speed > 10) {
        display += ` 💨${game.wind_speed}`;
      }
      
      return display;
    }
    return '🌫️ N/A';
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading game logs...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  const filteredGames = getFilteredGames();

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Game Logs</h1>
        <p>Los Angeles Dodgers • 2025 Season</p>
        <div className={styles.buttonGroup}>
          <button 
            onClick={async () => {
              try {
                setLoading(true);
                const result = await gameService.syncResults();
                console.log('Sync results:', result);
                // Reload games after syncing
                await loadGames();
              } catch (err) {
                console.error('Error syncing results:', err);
              } finally {
                setLoading(false);
              }
            }}
            className={styles.syncButton}
            disabled={loading}
          >
            {loading ? 'Syncing...' : '🌤️ Sync Game Results & Weather'}
          </button>
          
          <button 
            onClick={async () => {
              try {
                setLoading(true);
                const result = await gameService.syncWeather();
                console.log('Sync weather:', result);
                // Reload games after syncing weather
                await loadGames();
              } catch (err) {
                console.error('Error syncing weather:', err);
              } finally {
                setLoading(false);
              }
            }}
            className={styles.weatherButton}
            disabled={loading}
          >
            {loading ? 'Syncing...' : '🌦️ Sync Weather Only'}
          </button>
        </div>
      </div>

      <div className={styles.filters}>
        <button 
          className={`${styles.filterBtn} ${filter === 'all' ? styles.active : ''}`}
          onClick={() => setFilter('all')}
        >
          All Games ({games.length})
        </button>
        <button 
          className={`${styles.filterBtn} ${filter === 'home' ? styles.active : ''}`}
          onClick={() => setFilter('home')}
        >
          Home ({games.filter(g => g.home_team === 'Los Angeles Dodgers').length})
        </button>
        <button 
          className={`${styles.filterBtn} ${filter === 'away' ? styles.active : ''}`}
          onClick={() => setFilter('away')}
        >
          Away ({games.filter(g => g.away_team === 'Los Angeles Dodgers').length})
        </button>
        <button 
          className={`${styles.filterBtn} ${filter === 'final' ? styles.active : ''}`}
          onClick={() => setFilter('final')}
        >
          Completed ({games.filter(g => g.is_final).length})
        </button>
        <button 
          className={`${styles.filterBtn} ${filter === 'upcoming' ? styles.active : ''}`}
          onClick={() => setFilter('upcoming')}
        >
          Upcoming ({games.filter(g => !g.is_final).length})
        </button>
      </div>
      
      <div className={styles.loadMoreSection}>
        <button 
          className={styles.loadMoreBtn}
          onClick={loadAllGames}
          disabled={loading || showAllGames}
        >
          {showAllGames ? 'All Games Loaded' : '📋 Load All Games (128 total)'}
        </button>
        {!showAllGames && (
          <span className={styles.gamesInfo}>
            Showing {games.length} of 128 games. Click to load all games.
          </span>
        )}
      </div>

      <div className={styles.gamesList}>
        {/* Column Headers */}
        <div className={styles.columnHeaders}>
          <div className={styles.headerDate}>Date</div>
          <div className={styles.headerMatchup}>Matchup</div>
          <div className={styles.headerVenue}>Venue</div>
          <div className={styles.headerScore}>Score</div>
          <div className={styles.headerResult}>Result</div>
          <div className={styles.headerWeather}>🌤️ Weather</div>
          <div className={styles.headerDetails}>Details</div>
        </div>
        
        {filteredGames.length === 0 ? (
          <div className={styles.noGames}>No games found for the selected filter.</div>
        ) : (
          filteredGames.map(game => (
            <div key={game.id} className={styles.gameRow}>
              <div className={styles.gameDate}>
                {formatDate(game.game_date)}
              </div>
              
              <div className={styles.gameMatchup}>
                {getVenueDisplay(game)}
              </div>
              
              <div className={styles.gameVenue}>
                {game.venue}
              </div>
              
              <div className={styles.gameScore}>
                {game.is_final && game.home_score !== null && game.away_score !== null ? (
                  <>
                    <span className={game.home_team === 'Los Angeles Dodgers' ? styles.dodgersScore : ''}>
                      {game.home_score}
                    </span>
                    <span className={styles.scoreSeparator}>-</span>
                    <span className={game.away_team === 'Los Angeles Dodgers' ? styles.dodgersScore : ''}>
                      {game.away_score}
                    </span>
                  </>
                ) : (
                  <span className={styles.tbd}>TBD</span>
                )}
              </div>
              
              <div className={styles.gameResult}>
                <span className={`${styles.resultBadge} ${getResultClass(getGameResult(game))}`}>
                  {getGameResult(game)}
                </span>
              </div>
              
              <div className={styles.gameWeather} title={game.weather_temp && game.weather_conditions ? 
                `${game.weather_temp}°F, ${game.weather_conditions}${game.wind_speed ? `, Wind: ${game.wind_speed}mph${game.wind_direction ? ` ${game.wind_direction}` : ''}` : ''}${game.humidity ? `, Humidity: ${game.humidity}%` : ''}` : 
                'Weather data not available'}>
                {getWeatherDisplay(game)}
              </div>
              
              <div className={styles.gameDetails}>
                {game.attendance && (
                  <span className={styles.attendance}>
                    {game.attendance.toLocaleString()} fans
                  </span>
                )}
                {game.game_duration && (
                  <span className={styles.duration}>
                    {game.game_duration}
                  </span>
                )}
                {game.extra_innings && (
                  <span className={styles.extraInnings}>Extra Innings</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default GameLogs;
