import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <Link to="/" className={styles.logoLink}>
            The Dodger Report
          </Link>
        </div>
        <nav className={styles.nav}>
          <Link to="/" className={styles.navLink}>
            Home
          </Link>
          <Link to="/roster" className={styles.navLink}>
            Roster
          </Link>
          <Link to="/games" className={styles.navLink}>
            Game Logs
          </Link>
          <Link to="/data-engineering" className={styles.navLink}>
            Data Engineering
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
