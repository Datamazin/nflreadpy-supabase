# NFL Data Loading Guide

## Successfully Loaded Data (2023-2025 Seasons)

### Reference Data
- **Players**: 24,354 players
- **Teams**: 36 teams

### Team Data
- **Rosters**: 9,436 roster entries (2023-2025)
- **Team Stats**: 1,652 team-game records (weekly statistics)
- **Schedules**: 842 games

### Player Data
- **Player Stats**: 55,035 player-game records (weekly statistics)

## Loading Team Data

### Quick Start
To load all team data for specific seasons:

```bash
uv run python scripts/load_data.py --season 2023 2024 2025 --data-types rosters team_stats schedules reference
```

### Individual Data Types

#### Load Rosters Only
```bash
uv run python scripts/load_data.py --season 2023 --data-types rosters
```

#### Load Team Statistics Only
```bash
uv run python scripts/load_data.py --season 2023 2024 --data-types team_stats
```

#### Load Schedules Only
```bash
uv run python scripts/load_data.py --season 2023 2024 2025 --data-types schedules
```

#### Load Reference Data (Players & Teams)
```bash
uv run python scripts/load_data.py --data-types reference
```

## Data Types Explained

### `reference`
Loads foundational data:
- **players**: All NFL players with biographical info (gsis_id, name, position, college, etc.)
- **teams**: All NFL teams with basic information

### `rosters`
Team rosters by season, showing which players were on which teams. Includes:
- Player assignments to teams
- Position information
- Jersey numbers
- Player status (active, injured reserve, etc.)

### `team_stats`
Weekly team statistics including:
- Offensive and defensive performance
- Points scored
- Yardage totals
- Turnovers
- Game-by-game breakdowns

### `schedules`
Game schedules with:
- Matchups (home/away teams)
- Game dates
- Scores
- Stadium information
- Weather conditions

### `pbp` (Play-by-Play)
Detailed play-by-play data:
```bash
uv run python scripts/load_data.py --season 2023 --data-types pbp
```

### `player_stats`
Individual player statistics:
```bash
uv run python scripts/load_data.py --season 2023 --data-types player_stats
```

## Multiple Seasons

Load data for multiple seasons in one command:
```bash
uv run python scripts/load_data.py --season 2020 2021 2022 2023 2024 --data-types rosters team_stats schedules
```

## Data Relationships

```
Teams (36 teams)
  │
  ├─→ Rosters (9,436 entries for 2023-2025)
  │     └─→ Players (24,354 players)
  │
  ├─→ Team Stats (1,652 records)
  │     └─→ Schedules (842 games)
  │
  └─→ Schedules (home_team/away_team)
```

## Common Workflows

### 1. Load Complete Season Data
```bash
# Load everything for 2024 season
uv run python scripts/load_data.py --season 2024 --data-types reference rosters team_stats schedules player_stats pbp
```

### 2. Load Just Team Information
```bash
# Quick team data for analysis
uv run python scripts/load_data.py --season 2024 --data-types rosters team_stats schedules
```

### 3. Update With Latest Season
```bash
# Add 2025 data to existing database
uv run python scripts/load_data.py --season 2025 --data-types rosters team_stats schedules
```

## Database Schema

The data is stored in these Supabase tables:

- **players**: Player biographical information
- **teams**: NFL teams
- **rosters**: Season rosters (player-team assignments)
- **team_stats**: Weekly team statistics
- **schedules**: Game schedules and results
- **player_stats**: Individual player statistics
- **play_by_play**: Detailed play-by-play data

## Configuration

Make sure your `.env` file has valid Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

## Troubleshooting

### Duplicate Key Errors
The script uses upsert by default, so running it multiple times will update existing records.

### Missing Data
If certain columns are missing, check that:
1. The nflreadpy version supports those columns
2. The data is available for the requested season
3. The database schema includes those columns

### Null Values
The loaders automatically filter out rows with null primary keys (player_id, game_id, etc.).

## Performance Tips

- Load one season at a time for large datasets
- Use specific data types instead of loading everything
- Reference data only needs to be loaded once
- Upsert mode allows safe re-runs without duplicates
