export interface Game {
  id: number;
  espn_id: string;
  game_date: string;
  home_team: string;
  away_team: string;
  home_score?: number;
  away_score?: number;
  venue?: string;
  attendance?: number;
  game_time?: string;
  game_duration?: string;
  extra_innings: boolean;
  neutral_site: boolean;
  is_final: boolean;
  game_result?: string;
  day_of_week?: string;
  is_night_game?: boolean;
  days_since_last_game?: number;
  weather_temp?: number;
  weather_conditions?: string;
  wind_speed?: number;
  wind_direction?: string;
  humidity?: number;
  created_at?: string;
  updated_at?: string;
}

export interface GameResult {
  id: number;
  game_id: number;
  home_team: string;
  away_team: string;
  home_score: number;
  away_score: number;
  home_record_after?: string;
  away_record_after?: string;
  home_hits?: number;
  home_errors?: number;
  home_lob?: number;
  home_risp?: string;
  away_hits?: number;
  away_errors?: number;
  away_lob?: number;
  away_risp?: string;
  created_at?: string;
  updated_at?: string;
}
