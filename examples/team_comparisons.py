"""
Example: Team comparisons and analysis.

This script demonstrates how to use the TeamAnalytics class
to analyze NFL team performance.
"""

from src.analytics import TeamAnalytics


def main():
    """Run team comparison analysis."""
    print("=" * 70)
    print("NFL Team Comparison Analysis")
    print("=" * 70)

    # Initialize analytics
    analytics = TeamAnalytics()

    # Example 1: Offensive Rankings
    print("\n1. Top 10 Offenses by EPA per Play (2024 season)")
    print("-" * 70)
    try:
        offense_rankings = analytics.get_offensive_rankings(season=2024)
        print(offense_rankings.head(10))
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have loaded play-by-play data for 2024")

    # Example 2: Defensive Rankings
    print("\n2. Top 10 Defenses by EPA per Play (2024 season)")
    print("-" * 70)
    try:
        defense_rankings = analytics.get_defensive_rankings(season=2024)
        print(defense_rankings.head(10))
    except Exception as e:
        print(f"Error: {e}")

    # Example 3: Team Efficiency (Pass vs Run)
    print("\n3. Kansas City Chiefs Efficiency (Pass vs Run)")
    print("-" * 70)
    try:
        kc_efficiency = analytics.get_team_efficiency(season=2024, team="KC")
        print(kc_efficiency)
    except Exception as e:
        print(f"Error: {e}")

    # Example 4: Head-to-Head Comparison
    print("\n4. Kansas City vs Buffalo Head-to-Head (2024 season)")
    print("-" * 70)
    try:
        matchup = analytics.get_team_vs_team(season=2024, team1="KC", team2="BUF")
        print(matchup)
    except Exception as e:
        print(f"Error: {e}")

    # Example 5: Win Probability Stats
    print("\n5. Top 10 Teams by Win Probability Added (2024 season)")
    print("-" * 70)
    try:
        wp_stats = analytics.get_win_probability_by_team(season=2024)
        print(wp_stats.head(10))
    except Exception as e:
        print(f"Error: {e}")

    # Example 6: Scoring Trends
    print("\n6. Average Points Scored by Week (2024 season)")
    print("-" * 70)
    try:
        scoring_trends = analytics.get_scoring_trends(season=2024)
        print(scoring_trends)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have loaded schedule data for 2024")

    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
