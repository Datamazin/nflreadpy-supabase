"""Data loader for NFL player statistics."""

from typing import List, Literal, Optional, Union

import nflreadpy as nfl
import polars as pl


class PlayerStatsLoader:
    """Load NFL player statistics using nflreadpy."""

    def __init__(self):
        """Initialize the player stats loader."""
        pass

    def load_player_stats(
        self,
        seasons: Union[int, List[int], None] = None,
        summary_level: Literal["week", "reg", "post", "reg+post"] = "week",
    ) -> pl.DataFrame:
        """
        Load player statistics for specified seasons.

        Args:
            seasons: Season(s) to load. If None, loads current season.
            summary_level: Summary level ("week", "reg", "post", "reg+post").

        Returns:
            Polars DataFrame with player statistics.
        """
        print(f"Loading player stats for seasons: {seasons}, level: {summary_level}")
        df = nfl.load_player_stats(seasons, summary_level)
        print(f"Loaded stats for {len(df):,} player-game records")
        return df

    def load_player_info(self) -> pl.DataFrame:
        """
        Load comprehensive player information.

        Returns:
            Polars DataFrame with player data.
        """
        print("Loading player information...")
        df = nfl.load_players()
        print(f"Loaded info for {len(df):,} players")
        return df

    def prepare_for_upload(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Prepare player stats data for Supabase upload.

        Args:
            df: Raw player stats DataFrame

        Returns:
            Processed DataFrame ready for upload
        """
        # Filter out rows with null player_id (required for primary key)
        if "player_id" in df.columns:
            df = df.filter(pl.col("player_id").is_not_null())
        
        # Select only columns that exist in the database schema
        schema_columns = [
            "player_id", "player_name", "season", "week", "team", "position",
            "completions", "attempts", "passing_yards", "passing_tds",
            "interceptions", "carries", "rushing_yards", "rushing_tds",
            "receptions", "receiving_yards", "receiving_tds", "targets",
            "fantasy_points", "fantasy_points_ppr"
        ]
        
        # Map nflreadpy column names to database schema
        rename_map = {}
        if "passing_interceptions" in df.columns and "interceptions" not in df.columns:
            rename_map["passing_interceptions"] = "interceptions"
        if rename_map:
            df = df.rename(rename_map)
        
        available = [col for col in schema_columns if col in df.columns]
        result = df.select(available)
        
        # Cast numeric columns
        int_cols = [
            "season", "week", "completions", "attempts", "passing_yards",
            "passing_tds", "interceptions", "carries", "rushing_yards",
            "rushing_tds", "receptions", "receiving_yards", "receiving_tds",
            "targets"
        ]
        for col in int_cols:
            if col in result.columns:
                result = result.with_columns(pl.col(col).cast(pl.Int32, strict=False))
        
        return result
    
    def prepare_player_info_for_upload(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Prepare player info data for Supabase upload.

        Args:
            df: Raw player info DataFrame

        Returns:
            Processed DataFrame ready for upload
        """
        # Filter out rows with null gsis_id FIRST (maps to player_id primary key)
        if "gsis_id" in df.columns:
            df = df.filter(pl.col("gsis_id").is_not_null())
        
        # Create player_id from gsis_id (keep both columns)
        if "gsis_id" in df.columns:
            df = df.with_columns(pl.col("gsis_id").alias("player_id"))
        
        # Rename display_name to player_name
        if "display_name" in df.columns:
            df = df.rename({"display_name": "player_name"})
        
        # Select only columns that exist in the database schema
        schema_columns = [
            "player_id", "player_name", "position", "height", "weight",
            "college", "birth_date", "draft_year", "draft_round", 
            "draft_pick", "draft_team", "gsis_id", "espn_id", "yahoo_id"
        ]
        available = [col for col in schema_columns if col in df.columns]
        result = df.select(available)
        
        # Cast numeric columns
        int_cols = ["weight", "draft_year", "draft_round", "draft_pick"]
        for col in int_cols:
            if col in result.columns:
                result = result.with_columns(pl.col(col).cast(pl.Int32, strict=False))
        
        # Convert date to string for JSON serialization
        if "birth_date" in result.columns:
            result = result.with_columns(
                pl.col("birth_date").cast(pl.Utf8).alias("birth_date")
            )
        
        return result
