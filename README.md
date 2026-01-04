# NFL Analytics with nflreadpy & Supabase

A comprehensive NFL analytics solution that combines the power of [nflreadpy](https://github.com/nflverse/nflreadpy) for NFL data retrieval with Supabase for cloud-based storage and analytics.

## Features

- 📊 **Automated Data Pipeline**: Fetch and sync NFL data from nflverse repositories
- 🏈 **Comprehensive Coverage**: Play-by-play, player stats, team stats, rosters, and more
- ☁️ **Cloud Storage**: Store data in Supabase PostgreSQL database
- 📈 **Analytics Ready**: Pre-built queries for common analytics use cases
- 🚀 **Easy to Use**: Simple Python API with sensible defaults

## Data Sources

This project leverages nflreadpy to access:
- **Play-by-Play Data** (1999-present)
- **Player Statistics** (seasonal and weekly)
- **Team Statistics** (seasonal and weekly)
- **Rosters** (1920-present)
- **Game Schedules & Results**
- **Next Gen Stats** (2016-present)
- **Injuries, Contracts, Draft Picks, and more**

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -e .
```

### 2. Set Up Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Copy your project URL and API key

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 4. Run Initial Setup

```bash
# Initialize database schema
python scripts/setup_database.py

# Load initial data
python scripts/load_data.py --season 2024
```

### 5. Run Analytics

```bash
# Run example analytics
python examples/player_performance.py
python examples/team_comparisons.py
```

## Project Structure

```
nflreadpy-supabase/
├── src/
│   ├── data_loader/        # NFL data fetching modules
│   ├── supabase_client/    # Supabase integration
│   ├── analytics/          # Analytics queries and reports
│   └── utils/              # Utilities and helpers
├── scripts/                # Setup and data loading scripts
├── examples/               # Usage examples
├── sql/                    # Database schemas and migrations
└── tests/                  # Unit tests
```

## Usage Examples

### Load Play-by-Play Data

```python
from src.data_loader.pbp_loader import PlayByPlayLoader

loader = PlayByPlayLoader()
loader.load_and_sync(seasons=[2023, 2024])
```

### Query Player Performance

```python
from src.analytics.player_analytics import PlayerAnalytics

analytics = PlayerAnalytics()
top_qbs = analytics.get_top_quarterbacks(season=2024, min_plays=100)
print(top_qbs)
```

### Team Analysis

```python
from src.analytics.team_analytics import TeamAnalytics

analytics = TeamAnalytics()
offensive_rankings = analytics.get_offensive_rankings(season=2024)
print(offensive_rankings)
```

## Configuration

Configure the application through environment variables or the `Config` class:

```python
from src.utils.config import get_settings

settings = get_settings()
print(settings.supabase_url)
```

## Available Analytics

- **Player Performance**: QB ratings, rushing yards, receiving stats
- **Team Comparisons**: Offensive/defensive rankings, efficiency metrics
- **Game Analysis**: Win probability, scoring trends
- **Fantasy Football**: Player projections, opportunity metrics
- **Advanced Stats**: Next Gen Stats, PFF grades, EPA/CPOE

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- [nflverse](https://github.com/nflverse) for providing comprehensive NFL data
- [nflreadpy](https://github.com/nflverse/nflreadpy) for the Python data access library
- [Supabase](https://supabase.com) for the backend infrastructure
