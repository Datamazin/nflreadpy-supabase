# Rushing Touchdowns Query for 2025 Season, Week 17

This document explains how to query rushing touchdowns for the 2025 NFL season, week 17.

## Quick Start

There are two ways to get rushing touchdowns data:

### Option 1: Using the Direct Script (Simple)

Run the standalone script that queries the database directly:

```bash
python scripts/get_rushing_touchdowns.py
```

This will display:
- List of all players who scored rushing TDs in week 17
- Player names, teams, positions, carries, yards, and TDs
- Totals for the week

### Option 2: Using the Analytics Class (Flexible)

Run the example that uses the PlayerAnalytics class:

```bash
python examples/rushing_touchdowns_week17.py
```

This provides the same data but demonstrates how to use the analytics API programmatically.

## Prerequisites

Before running these scripts, make sure you have:

1. **Set up Supabase connection**
   - Create a `.env` file with your Supabase credentials
   - See `GETTING_STARTED.md` for details

2. **Loaded the data**
   ```bash
   python scripts/load_data.py --season 2025 --data-types player_stats
   ```

## Using the API Programmatically

You can also use the `PlayerAnalytics` class in your own code:

```python
from src.analytics import PlayerAnalytics

analytics = PlayerAnalytics()

# Get rushing TDs for week 17
rushing_tds = analytics.get_rushing_touchdowns(
    season=2025, 
    week=17, 
    min_tds=1,  # Minimum TDs to include
    limit=50     # Max results to return
)

print(rushing_tds)
```

### Parameters

- `season` (int): NFL season year
- `week` (int, optional): Week number. If None, returns season totals
- `min_tds` (int): Minimum rushing TDs to include (default: 1)
- `limit` (int): Maximum number of results (default: 50)

### Return Value

Returns a Polars DataFrame with columns:
- `player_name`: Player's name
- `team`: Team abbreviation
- `position`: Position
- `week`: Week number
- `carries`: Number of carries
- `rushing_yards`: Rushing yards
- `rushing_tds`: Rushing touchdowns

## Example Output

```
======================================================================
NFL Rushing Touchdowns - 2025 Season, Week 17
======================================================================

Total players with rushing TDs: 15

Rushing Touchdown Leaders:
┌─────────────────┬──────┬──────────┬──────┬─────────┬───────────────┬──────────────┐
│ player_name     │ team │ position │ week │ carries │ rushing_yards │ rushing_tds  │
├─────────────────┼──────┼──────────┼──────┼─────────┼───────────────┼──────────────┤
│ J.Taylor        │ IND  │ RB       │ 17   │ 23      │ 114           │ 2            │
│ A.Jones         │ GB   │ RB       │ 17   │ 18      │ 89            │ 2            │
│ D.Henry         │ TEN  │ RB       │ 17   │ 20      │ 95            │ 1            │
└─────────────────┴──────┴──────────┴──────┴─────────┴───────────────┴──────────────┘

======================================================================
Week 17 Totals:
  Total Rushing TDs: 20
  Total Rushing Yards: 1,245
  Total Carries: 285
======================================================================
```

## Customization

### Query Different Weeks

To query a different week, modify the script or use the API:

```python
# Week 1 rushing TDs
rushing_tds = analytics.get_rushing_touchdowns(season=2025, week=1)

# Entire season rushing TDs
rushing_tds = analytics.get_rushing_touchdowns(season=2025, week=None)
```

### Filter by Minimum TDs

Only show players with 2+ TDs:

```python
rushing_tds = analytics.get_rushing_touchdowns(
    season=2025, 
    week=17, 
    min_tds=2
)
```

## Data Sources

The data comes from the `player_stats` table in Supabase, which is populated using nflreadpy's `load_player_stats()` function with weekly-level data.

## Troubleshooting

### "No rushing touchdown data found"

This means the data hasn't been loaded yet. Run:
```bash
python scripts/load_data.py --season 2025 --data-types player_stats
```

### Connection Errors

Check your `.env` file has valid Supabase credentials:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### Import Errors

Make sure you've installed dependencies:
```bash
uv sync
# or
pip install -e .
```

## Related Files

- `scripts/get_rushing_touchdowns.py` - Standalone query script
- `examples/rushing_touchdowns_week17.py` - Example using analytics API
- `src/analytics/player_analytics.py` - PlayerAnalytics class with `get_rushing_touchdowns()` method
- `sql/schema.sql` - Database schema showing `player_stats` table structure
