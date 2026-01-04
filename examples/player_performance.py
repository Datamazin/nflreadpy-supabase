"""
Example: Analyze player performance.

This script demonstrates how to use the PlayerAnalytics class
to analyze NFL player performance.
"""

from src.analytics import PlayerAnalytics


def main():
    """Run player performance analysis."""
    print("=" * 70)
    print("NFL Player Performance Analysis")
    print("=" * 70)

    # Initialize analytics
    analytics = PlayerAnalytics()

    # Example 1: Top Quarterbacks by EPA
    print("\n1. Top 10 Quarterbacks by EPA per Play (2024 season)")
    print("-" * 70)
    try:
        top_qbs = analytics.get_top_quarterbacks(
            season=2024, min_plays=100, limit=10
        )
        print(top_qbs)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have loaded play-by-play data for 2024")

    # Example 2: Rushing Leaders
    print("\n2. Top 10 Rushing Leaders (2024 season)")
    print("-" * 70)
    try:
        rushing_leaders = analytics.get_rushing_leaders(
            season=2024, min_carries=50, limit=10
        )
        print(rushing_leaders)
    except Exception as e:
        print(f"Error: {e}")

    # Example 3: Receiving Leaders
    print("\n3. Top 10 Receiving Leaders (2024 season)")
    print("-" * 70)
    try:
        receiving_leaders = analytics.get_receiving_leaders(
            season=2024, min_targets=30, limit=10
        )
        print(receiving_leaders)
    except Exception as e:
        print(f"Error: {e}")

    # Example 4: Player Game Log
    print("\n4. Patrick Mahomes Passing Game Log (2024 season)")
    print("-" * 70)
    try:
        game_log = analytics.get_player_game_log(
            player_name="P.Mahomes", season=2024, stat_type="passing"
        )
        print(game_log)
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
