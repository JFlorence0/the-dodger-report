import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import PlayerDetail from './pages/PlayerDetail';
import GameLogs from './pages/GameLogs';
import { playerService } from './services/api';
import './App.css';

function App() {
  const [isSyncing, setIsSyncing] = useState(false);

  const handleSyncRoster = async () => {
    try {
      setIsSyncing(true);
      await playerService.syncRoster();
      // Refresh the page to show updated data
      window.location.reload();
    } catch (error) {
      console.error('Failed to sync roster:', error);
      alert('Failed to sync roster. Please try again.');
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <Router>
      <div className="App">
        <Header onSyncRoster={handleSyncRoster} isSyncing={isSyncing} />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/roster" element={<Home />} />
            <Route path="/player/:playerId" element={<PlayerDetail />} />
            <Route path="/games" element={<GameLogs />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
