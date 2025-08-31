import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Player } from '../types/Player';
import { playerService } from '../services/api';
import styles from './PlayerDetail.module.css';

const PlayerDetail: React.FC = () => {
  const { playerId } = useParams<{ playerId: string }>();
  const navigate = useNavigate();
  const [player, setPlayer] = useState<Player | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (playerId) {
      loadPlayer(parseInt(playerId));
    }
  }, [playerId]);

  const loadPlayer = async (id: number) => {
    try {
      setLoading(true);
      const playerData = await playerService.getPlayer(id);
      setPlayer(playerData);
      setError(null);
    } catch (err) {
      setError('Failed to load player data. Please try again.');
      console.error('Error loading player:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPrimaryPosition = (player: Player) => {
    const primary = player.positions.find(pos => pos.is_primary);
    return primary ? primary.position : player.positions[0]?.position || 'N/A';
  };

  const getAllPositions = (player: Player) => {
    return player.positions.map(pos => pos.position).join(', ');
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return styles.statusActive;
      case 'injured':
        return styles.statusInjured;
      case 'suspended':
        return styles.statusSuspended;
      default:
        return styles.statusDefault;
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Loading player data...</p>
      </div>
    );
  }

  if (error || !player) {
    return (
      <div className={styles.error}>
        <p>{error || 'Player not found'}</p>
        <button onClick={() => navigate('/')} className={styles.backButton}>
          Back to Roster
        </button>
      </div>
    );
  }

  return (
    <div className={styles.playerDetail}>
      {/* Header */}
      <div className={styles.header}>
        <button onClick={() => navigate('/')} className={styles.backButton}>
          ← Back to Roster
        </button>
        <div className={styles.playerHeader}>
          <div className={styles.jerseyNumber}>#{player.uniform_number || 'N/A'}</div>
          <div className={styles.playerInfo}>
            <h1>{player.name}</h1>
            <div className={styles.primaryInfo}>
              <span className={styles.position}>{getPrimaryPosition(player)}</span>
              <span className={`${styles.statusBadge} ${getStatusColor(player.status)}`}>
                {player.status}
              </span>
            </div>
            <div className={styles.secondaryInfo}>
              <span className={styles.team}>{player.team}</span>
              <span className={styles.separator}>•</span>
              <span className={styles.batsThrows}>B: {player.bats || 'N/A'}</span>
              <span className={styles.separator}>•</span>
              <span className={styles.batsThrows}>T: {player.throws || 'N/A'}</span>
              <span className={styles.separator}>•</span>
              <span className={styles.physical}>{player.height || 'N/A'}</span>
              <span className={styles.separator}>•</span>
              <span className={styles.physical}>{player.weight ? `${player.weight} lbs` : 'N/A'}</span>
              <span className={styles.separator}>•</span>
              <span className={styles.positions}>Positions: {getAllPositions(player)}</span>
              <span className={styles.separator}>•</span>
              <span className={styles.updated}>Updated: {player.last_updated ? formatDate(player.last_updated) : 'N/A'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.content}>
        <div className={styles.mainSection}>
          {/* Placeholder for future analytics content */}
          <div className={styles.placeholder}>
            <h2>Player Analytics & Performance</h2>
            <p>This area will contain detailed statistics, performance metrics, game history, and advanced analytics.</p>
            <div className={styles.placeholderGrid}>
              <div className={styles.placeholderCard}>
                <h3>Season Stats</h3>
                <p>Batting average, home runs, RBIs, etc.</p>
              </div>
              <div className={styles.placeholderCard}>
                <h3>Game History</h3>
                <p>Recent games, performance trends</p>
              </div>
              <div className={styles.placeholderCard}>
                <h3>Advanced Metrics</h3>
                <p>OPS+, WAR, defensive metrics</p>
              </div>
              <div className={styles.placeholderCard}>
                <h3>Comparison</h3>
                <p>League rankings, team comparisons</p>
              </div>
            </div>
          </div>
        </div>


      </div>
    </div>
  );
};

export default PlayerDetail;
