import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Player } from '../types/Player';
import { playerService } from '../services/api';
import styles from './RosterList.module.css';

interface RosterListProps {
  onEditPlayer?: (player: Player) => void;
}

const RosterList: React.FC<RosterListProps> = ({ onEditPlayer }) => {
  const navigate = useNavigate();
  const [players, setPlayers] = useState<Player[]>([]);
  const [filteredPlayers, setFilteredPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  
  // Filter states
  const [positionFilter, setPositionFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');

  // Available positions and statuses for filters
  const positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH', 'SP', 'RP'];
  const statuses = ['Active', 'Injured', 'Suspended'];

  const loadRoster = async () => {
    try {
      setLoading(true);
      const roster = await playerService.getRoster();
      setPlayers(roster);
      setError(null);
    } catch (err) {
      setError('Failed to load roster. Please try again.');
      console.error('Error loading roster:', err);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = useCallback(() => {
    let filtered = [...players];

    // Apply position filter
    if (positionFilter) {
      filtered = filtered.filter(player => 
        player.positions.some(pos => pos.position === positionFilter)
      );
    }

    // Apply status filter
    if (statusFilter) {
      filtered = filtered.filter(player => player.status === statusFilter);
    }

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(player =>
        player.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredPlayers(filtered);
  }, [players, positionFilter, statusFilter, searchTerm]);



  const clearFilters = () => {
    setPositionFilter('');
    setStatusFilter('');
    setSearchTerm('');
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

  // useEffect hooks
  useEffect(() => {
    loadRoster();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [applyFilters]);

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Loading Dodgers roster...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.error}>
        <p>{error}</p>
        <button onClick={loadRoster} className={styles.retryButton}>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className={styles.rosterList}>
      {/* Filters */}
      <div className={styles.filters}>
        <div className={styles.searchBox}>
          <input
            type="text"
            placeholder="Search players..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className={styles.searchInput}
          />
        </div>
        
        <div className={styles.filterControls}>
          <select
            value={positionFilter}
            onChange={(e) => setPositionFilter(e.target.value)}
            className={styles.filterSelect}
          >
            <option value="">All Positions</option>
            {positions.map(pos => (
              <option key={pos} value={pos}>{pos}</option>
            ))}
          </select>
          
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className={styles.filterSelect}
          >
            <option value="">All Statuses</option>
            {statuses.map(status => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
          
          <button onClick={clearFilters} className={styles.clearButton}>
            Clear Filters
          </button>
        </div>
      </div>

      {/* Results count */}
      <div className={styles.resultsCount}>
        Showing {filteredPlayers.length} of {players.length} players
      </div>

      {/* Players list */}
      {filteredPlayers.length === 0 ? (
        <div className={styles.noResults}>
          <p>No players found matching your criteria.</p>
          <button onClick={clearFilters} className={styles.clearButton}>
            Clear Filters
          </button>
        </div>
      ) : (
        <div className={styles.list}>
          {filteredPlayers.map(player => (
            <div key={player.id} className={styles.playerRow}>
              <div className={styles.playerInfo}>
                <div className={styles.jerseyNumber}>
                  #{player.uniform_number || 'N/A'}
                </div>
                <div 
                  className={styles.name}
                  onClick={() => navigate(`/player/${player.id}`)}
                >
                  {player.name}
                  <span className={styles.clickIndicator}> →</span>
                </div>
                <div className={styles.primaryPosition}>{getPrimaryPosition(player)}</div>
                <div className={styles.batsThrows}>
                  B: {player.bats || 'N/A'} / T: {player.throws || 'N/A'}
                </div>
                <div className={styles.physical}>
                  {player.height || 'N/A'} • {player.weight ? `${player.weight} lbs` : 'N/A'}
                </div>
                <div className={styles.status}>
                  <span className={`${styles.statusBadge} ${getStatusColor(player.status)}`}>
                    {player.status}
                  </span>
                </div>
                <div className={styles.actions}>
                  <button 
                    className={styles.viewDetailsButton}
                    onClick={() => navigate(`/player/${player.id}`)}
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RosterList;
