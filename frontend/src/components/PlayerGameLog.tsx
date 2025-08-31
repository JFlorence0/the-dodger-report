import React, { useState, useEffect, useCallback } from 'react';
import { playerService } from '../services/api';
import styles from './PlayerGameLog.module.css';

interface GameLogRow {
  game_date: string;
  opponent: string;
  is_home: boolean;
  result: string;
  at_bats: number;
  runs: number;
  hits: number;
  doubles: number;
  triples: number;
  home_runs: number;
  rbis: number;
  walks: number;
  hit_by_pitch: number;
  strikeouts: number;
  stolen_bases: number;
  caught_stealing: number;
  batting_average: number;
  on_base_percentage: number;
  slugging_percentage: number;
  ops: number;
}

interface PlayerGameLogProps {
  playerId: number;
  playerName: string;
  season: number;
}

const PlayerGameLog: React.FC<PlayerGameLogProps> = ({ playerId, playerName, season }) => {
  const [gameLogs, setGameLogs] = useState<GameLogRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadPlayerGameLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // For now, we'll sync to get the data since the get endpoint returns empty data
      const response = await playerService.syncPlayerGameLog(playerId);
      if (response.success && response.games) {
        setGameLogs(response.games);
      } else {
        setError('Failed to load game logs');
      }
    } catch (err) {
      setError('Error loading game logs');
      console.error('Error loading game logs:', err);
    } finally {
      setLoading(false);
    }
  }, [playerId]);

  const syncGameLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await playerService.syncPlayerGameLog(playerId);
      if (response.success) {
        // Reload the game logs after syncing
        await loadPlayerGameLogs();
      } else {
        setError('Failed to sync game logs');
      }
    } catch (err) {
      setError('Error syncing game logs');
      console.error('Error syncing game logs:', err);
    } finally {
      setLoading(false);
    }
  }, [playerId, loadPlayerGameLogs]);

  useEffect(() => {
    loadPlayerGameLogs();
  }, [loadPlayerGameLogs]);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const formatOpponent = (opponent: string, isHome: boolean) => {
    const cleanOpponent = opponent.replace(/^vs/, '').replace(/^@/, '');
    return `${isHome ? 'vs' : '@'} ${cleanOpponent}`;
  };

  const formatResult = (result: string) => {
    if (result.startsWith('W')) return 'W';
    if (result.startsWith('L')) return 'L';
    return result;
  };

  if (loading) {
    return <div className={styles.loading}>Loading game logs...</div>;
  }

  if (error) {
    return (
      <div className={styles.error}>
        <p>{error}</p>
        <button onClick={syncGameLogs} className={styles.syncButton}>
          Retry Sync
        </button>
      </div>
    );
  }

  return (
    <div className={styles.playerGameLog}>
      <div className={styles.header}>
        <h3>{playerName} - {season} Game Log</h3>
        <div className={styles.controls}>
          <button onClick={syncGameLogs} className={styles.syncButton}>
            Sync Game Logs
          </button>
          <span className={styles.gameCount}>
            {gameLogs.length} games loaded
          </span>
        </div>
      </div>

      {gameLogs.length === 0 ? (
        <div className={styles.noData}>
          <p>No game logs available. Click "Sync Game Logs" to fetch data.</p>
        </div>
      ) : (
        <div className={styles.tableContainer}>
          <table className={styles.gameLogTable}>
            <thead>
              <tr>
                <th>Date</th>
                <th>Opponent</th>
                <th>Result</th>
                <th>AB</th>
                <th>R</th>
                <th>H</th>
                <th>2B</th>
                <th>3B</th>
                <th>HR</th>
                <th>RBI</th>
                <th>BB</th>
                <th>HBP</th>
                <th>SO</th>
                <th>SB</th>
                <th>CS</th>
                <th>AVG</th>
                <th>OBP</th>
                <th>SLG</th>
                <th>OPS</th>
              </tr>
            </thead>
            <tbody>
              {gameLogs.map((game, index) => (
                <tr key={index} className={styles.gameRow}>
                  <td>{formatDate(game.game_date)}</td>
                  <td>{formatOpponent(game.opponent, game.is_home)}</td>
                  <td className={game.result.startsWith('W') ? styles.win : styles.loss}>
                    {formatResult(game.result)}
                  </td>
                  <td>{game.at_bats}</td>
                  <td>{game.runs}</td>
                  <td>{game.hits}</td>
                  <td>{game.doubles}</td>
                  <td>{game.triples}</td>
                  <td>{game.home_runs}</td>
                  <td>{game.rbis}</td>
                  <td>{game.walks}</td>
                  <td>{game.hit_by_pitch}</td>
                  <td>{game.strikeouts}</td>
                  <td>{game.stolen_bases}</td>
                  <td>{game.caught_stealing}</td>
                  <td>{game.batting_average.toFixed(3)}</td>
                  <td>{game.on_base_percentage.toFixed(3)}</td>
                  <td>{game.slugging_percentage.toFixed(3)}</td>
                  <td>{game.ops.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PlayerGameLog;
