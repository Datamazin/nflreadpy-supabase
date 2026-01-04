"""Analytics for team performance."""

from typing import List, Optional

import polars as pl

from ..supabase_client import SupabaseClient


class TeamAnalytics:
    """Analytics queries for team performance."""

    def __init__(self, client: Optional[SupabaseClient] = None):
        """
        Initialize team analytics.

        Args:
            client: Optional SupabaseClient instance
        """
        self.client = client or SupabaseClient()

    def get_offensive_rankings(
        self, season: int, metric: str = "epa_per_play"
    ) -> pl.DataFrame:
        """
        Get offensive rankings by team.

        Args:
            season: NFL season
            metric: Metric to rank by ("epa_per_play", "yards", "points")

        Returns:
            DataFrame with offensive rankings
        """
        pbp = self.client.query("play_by_play", {"season": season})

        # Calculate offensive stats
        offense = (
            pbp.filter(pl.col("posteam").is_not_null())
            .group_by("posteam")
            .agg(
                [
                    pl.count().alias("plays"),
                    pl.col("epa").mean().alias("epa_per_play"),
                    pl.col("yards_gained").sum().alias("total_yards"),
                    pl.col("yards_gained").mean().alias("yards_per_play"),
                ]
            )
            .sort("epa_per_play", descending=True)
        )

        return offense

    def get_defensive_rankings(
        self, season: int, metric: str = "epa_per_play"
    ) -> pl.DataFrame:
        """
        Get defensive rankings by team.

        Args:
            season: NFL season
            metric: Metric to rank by ("epa_per_play", "yards", "points")

        Returns:
            DataFrame with defensive rankings
        """
        pbp = self.client.query("play_by_play", {"season": season})

        # Calculate defensive stats (lower EPA is better for defense)
        defense = (
            pbp.filter(pl.col("defteam").is_not_null())
            .group_by("defteam")
            .agg(
                [
                    pl.count().alias("plays"),
                    pl.col("epa").mean().alias("epa_per_play"),
                    pl.col("yards_gained").sum().alias("total_yards_allowed"),
                    pl.col("yards_gained").mean().alias("yards_per_play_allowed"),
                ]
            )
            .sort("epa_per_play")  # Lower is better for defense
        )

        return defense

    def get_team_efficiency(
        self, season: int, team: Optional[str] = None
    ) -> pl.DataFrame:
        """
        Get team efficiency metrics (pass vs run, early down vs late down).

        Args:
            season: NFL season
            team: Optional team abbreviation (e.g., "KC", "BUF")

        Returns:
            DataFrame with efficiency metrics
        """
        pbp = self.client.query("play_by_play", {"season": season})

        if team:
            pbp = pbp.filter(pl.col("posteam") == team)

        # Calculate efficiency by play type and down
        efficiency = (
            pbp.filter(pl.col("play_type").is_in(["pass", "run"]))
            .group_by(["posteam", "play_type"])
            .agg(
                [
                    pl.count().alias("plays"),
                    pl.col("epa").mean().alias("epa_per_play"),
                    pl.col("yards_gained").mean().alias("yards_per_play"),
                    (pl.col("epa") > 0).mean().alias("success_rate"),
                ]
            )
            .sort(["posteam", "play_type"])
        )

        return efficiency

    def get_win_probability_by_team(self, season: int) -> pl.DataFrame:
        """
        Get average win probability metrics by team.

        Args:
            season: NFL season

        Returns:
            DataFrame with win probability stats
        """
        pbp = self.client.query("play_by_play", {"season": season})

        wp_stats = (
            pbp.filter(pl.col("wp").is_not_null())
            .group_by("posteam")
            .agg(
                [
                    pl.col("wp").mean().alias("avg_win_prob"),
                    pl.col("wpa").sum().alias("total_wpa"),
                    pl.count().alias("plays"),
                ]
            )
            .sort("total_wpa", descending=True)
        )

        return wp_stats

    def get_team_vs_team(
        self, season: int, team1: str, team2: str
    ) -> pl.DataFrame:
        """
        Compare two teams head-to-head.

        Args:
            season: NFL season
            team1: First team abbreviation
            team2: Second team abbreviation

        Returns:
            DataFrame with comparison
        """
        pbp = self.client.query("play_by_play", {"season": season})

        # Get games between the two teams
        matchup = pbp.filter(
            ((pl.col("posteam") == team1) & (pl.col("defteam") == team2))
            | ((pl.col("posteam") == team2) & (pl.col("defteam") == team1))
        )

        stats = (
            matchup.group_by("posteam")
            .agg(
                [
                    pl.count().alias("plays"),
                    pl.col("epa").mean().alias("epa_per_play"),
                    pl.col("yards_gained").sum().alias("total_yards"),
                ]
            )
        )

        return stats

    def get_scoring_trends(self, season: int) -> pl.DataFrame:
        """
        Get scoring trends by week.

        Args:
            season: NFL season

        Returns:
            DataFrame with weekly scoring trends
        """
        schedules = self.client.query("schedules", {"season": season})

        # Calculate average scores by week
        scoring = (
            schedules.filter(
                pl.col("home_score").is_not_null() & pl.col("away_score").is_not_null()
            )
            .group_by("week")
            .agg(
                [
                    pl.col("home_score").mean().alias("avg_home_score"),
                    pl.col("away_score").mean().alias("avg_away_score"),
                    (pl.col("home_score") + pl.col("away_score")).mean().alias("avg_total_points"),
                    pl.count().alias("games"),
                ]
            )
            .sort("week")
        )

        return scoring
