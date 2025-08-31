import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

interface HeaderProps {
  onSyncRoster?: () => void;
  isSyncing?: boolean;
}

const Header: React.FC<HeaderProps> = ({ onSyncRoster, isSyncing = false }) => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <h1>Dodger Report</h1>
          <span className={styles.subtitle}>Analytics Dashboard • 2025 Season</span>
        </div>
        <nav className={styles.nav}>
          <Link to="/" className={styles.navLink}>Home</Link>
          <Link to="/roster" className={styles.navLink}>Roster</Link>
          <Link to="/games" className={styles.navLink}>Game Logs</Link>
          {onSyncRoster && (
            <button 
              onClick={onSyncRoster}
              disabled={isSyncing}
              className={styles.syncButton}
            >
              {isSyncing ? 'Syncing...' : '🔄 Sync Roster'}
            </button>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
