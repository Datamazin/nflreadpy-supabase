"""
Example: Quick start guide for loading and analyzing data.

This script demonstrates a complete workflow from loading data
to running analytics.
"""

import nflreadpy as nfl
from src.analytics import PlayerAnalytics, TeamAnalytics
from src.data_loader import PlayByPlayLoader, TeamDataLoader
from src.supabase_client import SupabaseClient


def quick_local_analysis():
    """
    Quick analysis using nflreadpy directly (without Supabase).

    This is useful for getting started quickly without setting up
    a database.
    """
    print("=" * 70)
    print("Quick Local Analysis (No Database Required)")
    print("=" * 70)

    # Load current season play-by-play data
    print("\nLoading play-by-play data...")
    pbp = nfl.load_pbp(2024)
    print(f"Loaded {len(pbp):,} plays")

    # Basic QB analysis
    print("\nTop Quarterbacks by EPA per Play:")
    print("-" * 70)

    import polars as pl

    passing = pbp.filter(
        (pl.col("play_type") == "pass") & (pl.col("passer_player_name").is_not_null())
    )

    qb_stats = (
        passing.group_by("passer_player_name")
        .agg(
            [
                pl.count().alias("plays"),
                pl.col("epa").mean().alias("epa_per_play"),
                pl.col("yards_gained").sum().alias("passing_yards"),
            ]
        )
        .filter(pl.col("plays") >= 100)
        .sort("epa_per_play", descending=True)
        .head(10)
    )

    print(qb_stats)

    print("\n" + "=" * 70)


def full_workflow_with_supabase():
    """
    Complete workflow with Supabase (requires setup).

    This demonstrates:
    1. Loading data from nflreadpy
    2. Uploading to Supabase
    3. Running analytics queries
    """
    print("=" * 70)
    print("Full Workflow with Supabase")
    print("=" * 70)

    try:
        # Initialize Supabase client
        client = SupabaseClient()
        print("✓ Connected to Supabase")

        # Load and upload play-by-play data
        print("\nLoading play-by-play data...")
        pbp_loader = PlayByPlayLoader()
        pbp = pbp_loader.load_pbp([2024])
        pbp_prepared = pbp_loader.prepare_for_upload(pbp)

        print("Uploading to Supabase...")
        result = client.upload_dataframe(
            pbp_prepared, "play_by_play", batch_size=1000, upsert=False
        )
        print(f"✓ Uploaded {result['uploaded']:,} rows")

        # Run analytics
        print("\nRunning analytics...")
        player_analytics = PlayerAnalytics(client)
        top_qbs = player_analytics.get_top_quarterbacks(season=2024, limit=10)
        print("\nTop 10 Quarterbacks:")
        print(top_qbs)

        team_analytics = TeamAnalytics(client)
        offense_rankings = team_analytics.get_offensive_rankings(season=2024)
        print("\nTop 10 Offenses:")
        print(offense_rankings.head(10))

        print("\n" + "=" * 70)
        print("✓ Workflow complete!")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Set up your .env file with Supabase credentials")
        print("  2. Run the database schema setup")
        print("\nFor a quick start without database, try the local analysis option.")


def main():
    """Main function."""
    print("\nNFL Analytics Quick Start Guide")
    print("=" * 70)
    print("\nChoose an option:")
    print("  1. Quick local analysis (no database required)")
    print("  2. Full workflow with Supabase (requires setup)")
    print()

    choice = input("Enter choice (1 or 2, default=1): ").strip() or "1"

    if choice == "1":
        quick_local_analysis()
    elif choice == "2":
        full_workflow_with_supabase()
    else:
        print("Invalid choice. Running local analysis...")
        quick_local_analysis()


if __name__ == "__main__":
    main()
