# Getting Started with NFL Analytics

This guide will help you get started with the NFL Analytics solution using nflreadpy and Supabase.

## Prerequisites

- Python 3.10 or higher
- A [Supabase](https://supabase.com) account (free tier is fine)
- Basic knowledge of Python and SQL

## Installation

### Step 1: Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Using pip:
```bash
pip install -e .
```

### Step 2: Set Up Supabase

1. **Create a Supabase project:**
   - Go to [supabase.com](https://supabase.com)
   - Sign up or log in
   - Click "New Project"
   - Fill in the project details and wait for it to initialize

2. **Get your credentials:**
   - In your project dashboard, go to Settings > API
   - Copy your "Project URL" and "anon/public" API key
   - Save these for the next step

### Step 3: Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   ```

### Step 4: Set Up Database Schema

1. Run the setup script to see instructions:
   ```bash
   python scripts/setup_database.py
   ```

2. In your Supabase dashboard:
   - Go to SQL Editor
   - Copy the contents of `sql/schema.sql`
   - Paste and run it

This creates all the necessary tables and indexes.

## Loading Data

### Load Current Season Data

Load all data types for the 2024 season:
```bash
python scripts/load_data.py --season 2024
```

### Load Specific Data Types

Load only play-by-play data:
```bash
python scripts/load_data.py --season 2024 --data-types pbp
```

Load multiple data types:
```bash
python scripts/load_data.py --season 2024 --data-types pbp player_stats team_stats
```

### Load Multiple Seasons

```bash
python scripts/load_data.py --season 2023 2024 --data-types all
```

Available data types:
- `pbp` - Play-by-play data
- `player_stats` - Player statistics
- `team_stats` - Team statistics
- `rosters` - Team rosters
- `schedules` - Game schedules
- `reference` - Reference data (players, teams)
- `all` - All of the above

## Running Analytics

### Quick Start (No Database)

Try the quick start example that works without Supabase:
```bash
python examples/quick_start.py
```

Choose option 1 for local analysis.

### Player Performance Analysis

```bash
python examples/player_performance.py
```

This shows:
- Top quarterbacks by EPA
- Rushing leaders
- Receiving leaders
- Individual player game logs

### Team Comparisons

```bash
python examples/team_comparisons.py
```

This shows:
- Offensive rankings
- Defensive rankings
- Team efficiency metrics
- Head-to-head comparisons
- Win probability stats
- Scoring trends

## Using the Python API

### Basic Usage

```python
from src.analytics import PlayerAnalytics, TeamAnalytics

# Player analytics
player_analytics = PlayerAnalytics()
top_qbs = player_analytics.get_top_quarterbacks(season=2024, min_plays=100)
print(top_qbs)

# Team analytics
team_analytics = TeamAnalytics()
offense = team_analytics.get_offensive_rankings(season=2024)
print(offense)
```

### Loading Data Programmatically

```python
from src.data_loader import PlayByPlayLoader
from src.supabase_client import SupabaseClient

# Load data
loader = PlayByPlayLoader()
pbp = loader.load_pbp([2024])

# Upload to Supabase
client = SupabaseClient()
prepared = loader.prepare_for_upload(pbp)
result = client.upload_dataframe(prepared, "play_by_play", upsert=True)
print(f"Uploaded {result['uploaded']} rows")
```

### Custom Queries

```python
from src.supabase_client import SupabaseClient
import polars as pl

client = SupabaseClient()

# Query specific data
chiefs_games = client.query("play_by_play", {"posteam": "KC", "season": 2024})

# Run custom analysis
passing_epa = (
    chiefs_games
    .filter(pl.col("play_type") == "pass")
    .group_by("passer_player_name")
    .agg([
        pl.col("epa").mean().alias("avg_epa"),
        pl.count().alias("passes")
    ])
    .sort("avg_epa", descending=True)
)
print(passing_epa)
```

## Common Issues

### Import Errors

Make sure you're running from the project root and have installed dependencies:
```bash
cd nflreadpy-supabase
uv sync  # or pip install -e .
```

### Supabase Connection Errors

Check your `.env` file:
- URL should start with `https://`
- Key should be the anon/public key (not the service role key unless you need it)

### Data Loading Errors

- Ensure the database schema is set up correctly
- Check that you have enough storage in your Supabase project
- For large datasets, consider loading one season at a time

## Next Steps

- Explore the `src/analytics` directory for more analytics functions
- Create custom analytics by extending `PlayerAnalytics` or `TeamAnalytics`
- Build visualizations using the data (with plotly, matplotlib, etc.)
- Set up scheduled data updates using GitHub Actions or cron jobs
- Explore additional data sources from nflreadpy (injuries, contracts, etc.)

## Resources

- [nflreadpy Documentation](https://nflreadpy.nflverse.com)
- [Supabase Documentation](https://supabase.com/docs)
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [nflverse Discord](https://discord.com/invite/5Er2FBnnQa)
