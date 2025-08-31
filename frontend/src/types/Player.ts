export interface PlayerPosition {
  id: number;
  player_id: number;
  position: string;
  is_primary: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface Player {
  id: number;
  name: string;
  positions: PlayerPosition[];
  uniform_number?: number;
  height?: string;
  weight?: number;
  birth_date?: string;
  bats?: string;
  throws?: string;
  team: string;
  status: string;
  last_updated?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PlayerCreate {
  name: string;
  positions: string[];
  uniform_number?: number;
  height?: string;
  weight?: number;
  birth_date?: string;
  bats?: string;
  throws?: string;
  team?: string;
  status?: string;
}

export interface PlayerUpdate {
  name?: string;
  positions?: string[];
  uniform_number?: number;
  height?: string;
  weight?: number;
  birth_date?: string;
  bats?: string;
  throws?: string;
  team?: string;
  status?: string;
}

export interface RosterFilters {
  position?: string;
  status?: string;
}
