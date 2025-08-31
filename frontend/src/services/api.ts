import axios from 'axios';
import { Player, PlayerCreate, PlayerUpdate, RosterFilters } from '../types/Player';
import { Game } from '../types/Game';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const playerService = {
  // Get all players with optional filters
  getRoster: async (filters?: RosterFilters): Promise<Player[]> => {
    const params = new URLSearchParams();
    if (filters?.position) params.append('position', filters.position);
    if (filters?.status) params.append('status', filters.status);
    
    const response = await api.get<Player[]>(`/api/v1/roster?${params.toString()}`);
    return response.data;
  },

  // Get a single player by ID
  getPlayer: async (id: number): Promise<Player> => {
    const response = await api.get<Player>(`/api/v1/roster/${id}`);
    return response.data;
  },

  // Create a new player
  createPlayer: async (player: PlayerCreate): Promise<Player> => {
    const response = await api.post<Player>('/api/v1/roster', player);
    return response.data;
  },

  // Update an existing player
  updatePlayer: async (id: number, player: PlayerUpdate): Promise<Player> => {
    const response = await api.put<Player>(`/api/v1/roster/${id}`, player);
    return response.data;
  },

  // Delete a player
  deletePlayer: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/roster/${id}`);
  },

  // Search players by name
  searchPlayers: async (searchTerm: string): Promise<Player[]> => {
    const response = await api.get<Player[]>(`/api/v1/roster?search=${searchTerm}`);
    return response.data;
  },

  // Sync roster from ESPN
  syncRoster: async (): Promise<any> => {
    const response = await api.post('/api/v1/roster-espn-sync');
    return response.data;
  },

  // Check roster sync status
  getSyncStatus: async (): Promise<any> => {
    const response = await api.get('/api/v1/roster-sync-status');
    return response.data;
  },

  // Get player game log
  getPlayerGameLog: async (playerId: number): Promise<any> => {
    const response = await api.get(`/api/v1/players/${playerId}/game-log`);
    return response.data;
  },

  // Sync player game log from ESPN
  syncPlayerGameLog: async (playerId: number): Promise<any> => {
    const response = await api.post(`/api/v1/players/${playerId}/sync-game-log`);
    return response.data;
  },
};

export const healthService = {
  // Check API health
  checkHealth: async (): Promise<{ status: string; service: string }> => {
    const response = await api.get<{ status: string; service: string }>('/health');
    return response.data;
  },
};

export const gameService = {
  // Get all games
  getGames: async (limit?: number): Promise<Game[]> => {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    
    const response = await api.get<Game[]>(`/api/v1/games?${params.toString()}`);
    return response.data;
  },

  // Get a single game by ESPN ID
  getGame: async (espnId: string): Promise<Game> => {
    const response = await api.get<Game>(`/api/v1/games/${espnId}`);
    return response.data;
  },

  // Get Dodgers record
  getRecord: async (): Promise<any> => {
    const response = await api.get('/api/v1/games/record');
    return response.data;
  },

  // Sync schedule from ESPN
  syncSchedule: async (): Promise<any> => {
    const response = await api.post('/api/v1/games/sync-schedule');
    return response.data;
  },

  // Sync game results from ESPN
  syncResults: async (): Promise<any> => {
    const response = await api.post('/api/v1/games/sync-results');
    return response.data;
  },

  // Fix existing game results
  fixExistingResults: async (): Promise<any> => {
    const response = await api.post('/api/v1/games/fix-existing-results');
    return response.data;
  },

  // Sync weather data
  syncWeather: async (): Promise<any> => {
    const response = await api.post('/api/v1/games/sync-weather');
    return response.data;
  },


};

export default api;
