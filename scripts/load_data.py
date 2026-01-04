"""
Load NFL data into Supabase.

This script loads data from nflreadpy and uploads it to Supabase.
"""

import argparse
from typing import List

from src.data_loader import PlayByPlayLoader, PlayerStatsLoader, TeamDataLoader
from src.supabase_client import SupabaseClient
from src.utils.config import get_settings


def load_play_by_play(seasons: List[int], client: SupabaseClient):
    """Load play-by-play data."""
    print("\n" + "=" * 70)
    print("Loading Play-by-Play Data")
    print("=" * 70)

    loader = PlayByPlayLoader()
    df = loader.load_pbp(seasons)
    df_prepared = loader.prepare_for_upload(df)

    result = client.upload_dataframe(
        df_prepared, "play_by_play", batch_size=1000, upsert=True
    )

    print(f"✓ Upload complete: {result['uploaded']:,} rows uploaded")
    if result["errors"] > 0:
        print(f"⚠ Errors: {result['errors']}")


def load_player_stats(seasons: List[int], client: SupabaseClient):
    """Load player statistics."""
    print("\n" + "=" * 70)
    print("Loading Player Statistics")
    print("=" * 70)

    loader = PlayerStatsLoader()
    df = loader.load_player_stats(seasons, summary_level="week")
    df_prepared = loader.prepare_for_upload(df)

    result = client.upload_dataframe(
        df_prepared, "player_stats", batch_size=1000, upsert=True
    )

    print(f"✓ Upload complete: {result['uploaded']:,} rows uploaded")
    if result["errors"] > 0:
        print(f"⚠ Errors: {result['errors']}")


def load_team_stats(seasons: List[int], client: SupabaseClient):
    """Load team statistics."""
    print("\n" + "=" * 70)
    print("Loading Team Statistics")
    print("=" * 70)

    loader = TeamDataLoader()
    df = loader.load_team_stats(seasons, summary_level="week")
    df_prepared = loader.prepare_for_upload(df, data_type="stats")

    result = client.upload_dataframe(
        df_prepared, "team_stats", batch_size=1000, upsert=True
    )

    print(f"✓ Upload complete: {result['uploaded']:,} rows uploaded")
    if result["errors"] > 0:
        print(f"⚠ Errors: {result['errors']}")


def load_rosters(seasons: List[int], client: SupabaseClient):
    """Load team rosters."""
    print("\n" + "=" * 70)
    print("Loading Team Rosters")
    print("=" * 70)

    loader = TeamDataLoader()
    df = loader.load_rosters(seasons)
    df_prepared = loader.prepare_for_upload(df, data_type="rosters")

    result = client.upload_dataframe(
        df_prepared, "rosters", batch_size=1000, upsert=True
    )

    print(f"✓ Upload complete: {result['uploaded']:,} rows uploaded")
    if result["errors"] > 0:
        print(f"⚠ Errors: {result['errors']}")


def load_schedules(seasons: List[int], client: SupabaseClient):
    """Load game schedules."""
    print("\n" + "=" * 70)
    print("Loading Game Schedules")
    print("=" * 70)

    loader = TeamDataLoader()
    df = loader.load_schedules(seasons)
    df_prepared = loader.prepare_for_upload(df, data_type="schedules")

    result = client.upload_dataframe(
        df_prepared, "schedules", batch_size=1000, upsert=True
    )

    print(f"✓ Upload complete: {result['uploaded']:,} rows uploaded")
    if result["errors"] > 0:
        print(f"⚠ Errors: {result['errors']}")


def load_reference_data(client: SupabaseClient):
    """Load reference data (players and teams)."""
    print("\n" + "=" * 70)
    print("Loading Reference Data")
    print("=" * 70)

    # Load players
    player_loader = PlayerStatsLoader()
    players_df = player_loader.load_player_info()
    players_prepared = player_loader.prepare_player_info_for_upload(players_df)
    result = client.upload_dataframe(
        players_prepared, "players", batch_size=1000, upsert=True
    )
    print(f"✓ Players uploaded: {result['uploaded']:,} rows")

    # Load teams
    team_loader = TeamDataLoader()
    teams_df = team_loader.load_team_info()
    teams_prepared = team_loader.prepare_for_upload(teams_df, data_type="info")
    result = client.upload_dataframe(
        teams_prepared, "teams", batch_size=1000, upsert=True
    )
    print(f"✓ Teams uploaded: {result['uploaded']:,} rows")


def main():
    """Main data loading function."""
    parser = argparse.ArgumentParser(
        description="Load NFL data into Supabase"
    )
    parser.add_argument(
        "--season",
        type=int,
        nargs="+",
        default=[2024],
        help="Season(s) to load (default: 2024)",
    )
    parser.add_argument(
        "--data-types",
        nargs="+",
        choices=["pbp", "player_stats", "team_stats", "rosters", "schedules", "reference", "all"],
        default=["all"],
        help="Types of data to load (default: all)",
    )

    args = parser.parse_args()
    seasons = args.season
    data_types = args.data_types

    # Expand "all" to all data types
    if "all" in data_types:
        data_types = ["pbp", "player_stats", "team_stats", "rosters", "schedules", "reference"]

    # Initialize client
    try:
        settings = get_settings()
        client = SupabaseClient()
        print("\n✓ Connected to Supabase")
    except Exception as e:
        print(f"\n✗ Failed to connect to Supabase: {e}")
        print("\nMake sure you have:")
        print("  1. Created a .env file (copy from .env.example)")
        print("  2. Added your Supabase URL and API key")
        return

    print(f"\nLoading data for seasons: {seasons}")
    print(f"Data types: {', '.join(data_types)}")

    try:
        # Load reference data first
        if "reference" in data_types:
            load_reference_data(client)

        # Load seasonal data
        if "pbp" in data_types:
            load_play_by_play(seasons, client)

        if "player_stats" in data_types:
            load_player_stats(seasons, client)

        if "team_stats" in data_types:
            load_team_stats(seasons, client)

        if "rosters" in data_types:
            load_rosters(seasons, client)

        if "schedules" in data_types:
            load_schedules(seasons, client)

        print("\n" + "=" * 70)
        print("✓ Data loading complete!")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ Error during data loading: {e}")
        print("\nPlease check:")
        print("  1. Your Supabase connection")
        print("  2. Database schema is set up correctly")
        print("  3. You have the necessary permissions")


if __name__ == "__main__":
    main()
