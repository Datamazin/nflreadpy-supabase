"""Analytics for player performance."""

import polars as pl

from ..supabase_client import SupabaseClient


class PlayerAnalytics:
    """Analytics queries for player performance."""

    def __init__(self, client: SupabaseClient | None = None):
        """
        Initialize player analytics.

        Args:
            client: Optional SupabaseClient instance
        """
        self.client = client or SupabaseClient()

    def get_top_quarterbacks(
        self, season: int, min_plays: int = 100, limit: int = 20
    ) -> pl.DataFrame:
        """
        Get top quarterbacks by EPA per play.

        Args:
            season: NFL season
            min_plays: Minimum number of plays
            limit: Number of results to return

        Returns:
            DataFrame with top quarterbacks
        """
        # Query play-by-play data
        pbp = self.client.query("play_by_play", {"season": season})

        # Filter passing plays
        passing = pbp.filter(
            (pl.col("play_type") == "pass") & (pl.col("passer_player_name").is_not_null())
        )

        # Calculate QB stats
        qb_stats = (
            passing.group_by("passer_player_name")
            .agg(
                [
                    pl.count().alias("plays"),
                    pl.col("epa").mean().alias("epa_per_play"),
                    pl.col("epa").sum().alias("total_epa"),
                    pl.col("yards_gained").sum().alias("passing_yards"),
                ]
            )
            .filter(pl.col("plays") >= min_plays)
            .sort("epa_per_play", descending=True)
            .head(limit)
        )

        return qb_stats

    def get_rushing_leaders(
        self, season: int, min_carries: int = 50, limit: int = 20
    ) -> pl.DataFrame:
        """
        Get rushing leaders by yards.

        Args:
            season: NFL season
            min_carries: Minimum number of carries
            limit: Number of results to return

        Returns:
            DataFrame with rushing leaders
        """
        pbp = self.client.query("play_by_play", {"season": season})

        rushing = pbp.filter(
            (pl.col("play_type") == "run") & (pl.col("rusher_player_name").is_not_null())
        )

        rushing_stats = (
            rushing.group_by("rusher_player_name")
            .agg(
                [
                    pl.count().alias("carries"),
                    pl.col("yards_gained").sum().alias("rushing_yards"),
                    pl.col("yards_gained").mean().alias("yards_per_carry"),
                    pl.col("epa").mean().alias("epa_per_carry"),
                ]
            )
            .filter(pl.col("carries") >= min_carries)
            .sort("rushing_yards", descending=True)
            .head(limit)
        )

        return rushing_stats

    def get_receiving_leaders(
        self, season: int, min_targets: int = 30, limit: int = 20
    ) -> pl.DataFrame:
        """
        Get receiving leaders by yards.

        Args:
            season: NFL season
            min_targets: Minimum number of targets
            limit: Number of results to return

        Returns:
            DataFrame with receiving leaders
        """
        pbp = self.client.query("play_by_play", {"season": season})

        receiving = pbp.filter(
            (pl.col("play_type") == "pass") & (pl.col("receiver_player_name").is_not_null())
        )

        receiving_stats = (
            receiving.group_by("receiver_player_name")
            .agg(
                [
                    pl.count().alias("targets"),
                    pl.col("yards_gained").sum().alias("receiving_yards"),
                    pl.col("yards_gained").mean().alias("yards_per_target"),
                    pl.col("epa").mean().alias("epa_per_target"),
                ]
            )
            .filter(pl.col("targets") >= min_targets)
            .sort("receiving_yards", descending=True)
            .head(limit)
        )

        return receiving_stats

    def get_player_game_log(
        self, player_name: str, season: int, stat_type: str = "passing"
    ) -> pl.DataFrame:
        """
        Get game-by-game stats for a specific player.

        Args:
            player_name: Player's name
            season: NFL season
            stat_type: Type of stats ("passing", "rushing", "receiving")

        Returns:
            DataFrame with player's game log
        """
        pbp = self.client.query("play_by_play", {"season": season})

        if stat_type == "passing":
            plays = pbp.filter(pl.col("passer_player_name") == player_name)
            group_col = "passer_player_name"
        elif stat_type == "rushing":
            plays = pbp.filter(pl.col("rusher_player_name") == player_name)
            group_col = "rusher_player_name"
        else:  # receiving
            plays = pbp.filter(pl.col("receiver_player_name") == player_name)
            group_col = "receiver_player_name"

        game_log = (
            plays.group_by(["game_id", "week"])
            .agg(
                [
                    pl.col("posteam").first(),
                    pl.col("defteam").first(),
                    pl.count().alias("plays"),
                    pl.col("yards_gained").sum().alias("total_yards"),
                    pl.col("epa").mean().alias("avg_epa"),
                    pl.col("epa").sum().alias("total_epa"),
                ]
            )
            .sort("week")
        )

        return game_log

    def get_rushing_touchdowns(
        self, season: int, week: int | None = None, min_tds: int = 1, limit: int = 50
    ) -> pl.DataFrame:
        """
        Get rushing touchdowns for a specific season and optional week.

        Args:
            season: NFL season
            week: Optional week number. If None, gets season totals.
            min_tds: Minimum number of rushing TDs to include
            limit: Number of results to return

        Returns:
            DataFrame with rushing touchdown leaders
        """
        # Build filters
        filters = {"season": season}
        if week is not None:
            filters["week"] = week

        # Query player stats
        player_stats = self.client.query("player_stats", filters)

        # Filter for players with rushing touchdowns
        rushing_td_stats = player_stats.filter(
            pl.col("rushing_tds").is_not_null() & (pl.col("rushing_tds") >= min_tds)
        )

        # Select relevant columns and sort
        result = (
            rushing_td_stats.select(
                [
                    "player_name",
                    "team",
                    "position",
                    "week",
                    "carries",
                    "rushing_yards",
                    "rushing_tds",
                ]
            )
            .sort("rushing_tds", descending=True)
            .head(limit)
        )

        return result
