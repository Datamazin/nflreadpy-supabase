"""
Example: Get rushing touchdowns for a specific week.

This script demonstrates how to use the PlayerAnalytics class
to get rushing touchdown data for a specific season and week.
"""

from src.analytics import PlayerAnalytics


def main():
    """Get rushing touchdowns for 2025 season, week 17."""
    print("=" * 70)
    print("NFL Rushing Touchdowns - 2025 Season, Week 17")
    print("=" * 70)

    # Initialize analytics
    analytics = PlayerAnalytics()

    try:
        # Get rushing touchdowns for week 17
        rushing_tds = analytics.get_rushing_touchdowns(season=2025, week=17, min_tds=1, limit=50)

        if len(rushing_tds) == 0:
            print("\nNo rushing touchdown data found for 2025 season, week 17.")
            print("\nNote: Data may not be loaded yet. To load data, run:")
            print("  python scripts/load_data.py --season 2025 --data-types player_stats")
        else:
            print(f"\nTotal players with rushing TDs: {len(rushing_tds)}")
            print("\nRushing Touchdown Leaders:")
            print(rushing_tds)

            # Calculate totals
            total_tds = rushing_tds["rushing_tds"].sum()
            total_yards = rushing_tds["rushing_yards"].sum()
            total_carries = rushing_tds["carries"].sum()

            print("\n" + "=" * 70)
            print("Week 17 Totals:")
            print(f"  Total Rushing TDs: {total_tds}")
            print(f"  Total Rushing Yards: {total_yards:,}")
            print(f"  Total Carries: {total_carries}")
            print("=" * 70)

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("  1. Set up your Supabase connection (.env file)")
        print("  2. Loaded player stats data for 2025 season")
        print("     Run: python scripts/load_data.py --season 2025 --data-types player_stats")


if __name__ == "__main__":
    main()
