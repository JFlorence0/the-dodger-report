import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import RosterList from './components/RosterList';
import PlayerDetail from './pages/PlayerDetail';
import GameLogs from './pages/GameLogs';
import DataEngineering from './pages/DataEngineering';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/roster" element={<RosterList />} />
            <Route path="/player/:playerId" element={<PlayerDetail />} />
            <Route path="/games" element={<GameLogs />} />
            <Route path="/data-engineering" element={<DataEngineering />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
