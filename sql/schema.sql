-- Play-by-play data table
CREATE TABLE IF NOT EXISTS play_by_play (
    play_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    week INTEGER,
    game_date DATE,
    posteam TEXT,
    defteam TEXT,
    quarter INTEGER,
    time TEXT,
    down INTEGER,
    ydstogo INTEGER,
    yardline_100 INTEGER,
    play_type TEXT,
    yards_gained INTEGER,
    epa REAL,
    wp REAL,
    wpa REAL,
    passer_player_name TEXT,
    receiver_player_name TEXT,
    rusher_player_name TEXT,
    "desc" TEXT,
    score_differential INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_pbp_game_id ON play_by_play(game_id);
CREATE INDEX IF NOT EXISTS idx_pbp_season ON play_by_play(season);
CREATE INDEX IF NOT EXISTS idx_pbp_posteam ON play_by_play(posteam);
CREATE INDEX IF NOT EXISTS idx_pbp_play_type ON play_by_play(play_type);

-- Player statistics table
CREATE TABLE IF NOT EXISTS player_stats (
    player_id TEXT,
    player_name TEXT,
    season INTEGER NOT NULL,
    week INTEGER,
    team TEXT,
    position TEXT,
    completions INTEGER,
    attempts INTEGER,
    passing_yards INTEGER,
    passing_tds INTEGER,
    interceptions INTEGER,
    carries INTEGER,
    rushing_yards INTEGER,
    rushing_tds INTEGER,
    receptions INTEGER,
    receiving_yards INTEGER,
    receiving_tds INTEGER,
    targets INTEGER,
    fantasy_points REAL,
    fantasy_points_ppr REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (player_id, season, week)
);

CREATE INDEX IF NOT EXISTS idx_player_stats_season ON player_stats(season);
CREATE INDEX IF NOT EXISTS idx_player_stats_team ON player_stats(team);
CREATE INDEX IF NOT EXISTS idx_player_stats_position ON player_stats(position);

-- Team statistics table
CREATE TABLE IF NOT EXISTS team_stats (
    team TEXT,
    season INTEGER NOT NULL,
    week INTEGER,
    opponent TEXT,
    completions INTEGER,
    attempts INTEGER,
    passing_yards INTEGER,
    passing_tds INTEGER,
    interceptions INTEGER,
    carries INTEGER,
    rushing_yards INTEGER,
    rushing_tds INTEGER,
    total_yards INTEGER,
    turnovers INTEGER,
    points INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (team, season, week)
);

CREATE INDEX IF NOT EXISTS idx_team_stats_season ON team_stats(season);
CREATE INDEX IF NOT EXISTS idx_team_stats_team ON team_stats(team);

-- Rosters table
CREATE TABLE IF NOT EXISTS rosters (
    player_id TEXT,
    player_name TEXT,
    season INTEGER NOT NULL,
    team TEXT,
    position TEXT,
    depth_chart_position TEXT,
    jersey_number INTEGER,
    status TEXT,
    height TEXT,
    weight INTEGER,
    birth_date DATE,
    college TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (player_id, season, team)
);

CREATE INDEX IF NOT EXISTS idx_rosters_season ON rosters(season);
CREATE INDEX IF NOT EXISTS idx_rosters_team ON rosters(team);
CREATE INDEX IF NOT EXISTS idx_rosters_position ON rosters(position);

-- Schedules table
CREATE TABLE IF NOT EXISTS schedules (
    game_id TEXT PRIMARY KEY,
    season INTEGER NOT NULL,
    week INTEGER,
    game_type TEXT,
    game_date DATE,
    home_team TEXT,
    away_team TEXT,
    home_score INTEGER,
    away_score INTEGER,
    stadium TEXT,
    location TEXT,
    roof TEXT,
    surface TEXT,
    temp INTEGER,
    wind INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_schedules_season ON schedules(season);
CREATE INDEX IF NOT EXISTS idx_schedules_home_team ON schedules(home_team);
CREATE INDEX IF NOT EXISTS idx_schedules_away_team ON schedules(away_team);
CREATE INDEX IF NOT EXISTS idx_schedules_game_date ON schedules(game_date);

-- Players reference table
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    player_name TEXT,
    position TEXT,
    height TEXT,
    weight INTEGER,
    college TEXT,
    birth_date DATE,
    draft_year INTEGER,
    draft_round INTEGER,
    draft_pick INTEGER,
    draft_team TEXT,
    gsis_id TEXT,
    espn_id TEXT,
    yahoo_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_players_position ON players(position);
CREATE INDEX IF NOT EXISTS idx_players_college ON players(college);

-- Teams reference table
CREATE TABLE IF NOT EXISTS teams (
    team_abbr TEXT PRIMARY KEY,
    team_name TEXT,
    team_nick TEXT,
    team_color TEXT,
    team_color2 TEXT,
    team_logo_espn TEXT,
    team_logo_wikipedia TEXT,
    team_conference TEXT,
    team_division TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS) on all tables
ALTER TABLE play_by_play ENABLE ROW LEVEL SECURITY;
ALTER TABLE player_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE rosters ENABLE ROW LEVEL SECURITY;
ALTER TABLE schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;

-- Create policies for authenticated users (adjust as needed)
CREATE POLICY "Enable read access for all users" ON play_by_play FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON player_stats FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON team_stats FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON rosters FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON schedules FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON players FOR SELECT USING (true);
CREATE POLICY "Enable read access for all users" ON teams FOR SELECT USING (true);
