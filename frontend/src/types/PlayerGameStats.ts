export interface PlayerGameStats {
  id: number;
  game_id: number;
  player_id: number;
  
  // Game context
  is_starter: boolean;
  position: string;
  
  // Batting stats
  at_bats?: number;
  runs?: number;
  hits?: number;
  doubles?: number;
  triples?: number;
  home_runs?: number;
  rbis?: number;
  walks?: number;
  strikeouts?: number;
  stolen_bases?: number;
  caught_stealing?: number;
  hit_by_pitch?: number;
  sacrifice_bunts?: number;
  sacrifice_flies?: number;
  left_on_base?: number;
  
  // Pitching stats
  innings_pitched?: number;
  hits_allowed?: number;
  runs_allowed?: number;
  earned_runs?: number;
  walks_allowed?: number;
  strikeouts_pitched?: number;
  home_runs_allowed?: number;
  wild_pitches?: number;
  balks?: number;
  hit_batters?: number;
  pitches_thrown?: number;
  strikes_thrown?: number;
  
  // Fielding stats
  putouts?: number;
  assists?: number;
  errors?: number;
  double_plays?: number;
  passed_balls?: number;
  
  // Game outcome
  win?: boolean;
  loss?: boolean;
  save?: boolean;
  hold?: boolean;
  blown_save?: boolean;
  
  // Metadata
  created_at: string;
  updated_at: string;
}
