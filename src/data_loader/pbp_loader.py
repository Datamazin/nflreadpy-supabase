"""Data loader for NFL play-by-play data."""

from typing import List, Optional, Union

import nflreadpy as nfl
import polars as pl


class PlayByPlayLoader:
    """Load NFL play-by-play data using nflreadpy."""

    def __init__(self):
        """Initialize the play-by-play loader."""
        pass

    def load_pbp(
        self, seasons: Union[int, List[int], None] = None
    ) -> pl.DataFrame:
        """
        Load play-by-play data for specified seasons.

        Args:
            seasons: Season(s) to load. If None, loads current season.
                    If int or list of ints, loads specified season(s).

        Returns:
            Polars DataFrame with play-by-play data.
        """
        print(f"Loading play-by-play data for seasons: {seasons}")
        df = nfl.load_pbp(seasons)
        print(f"Loaded {len(df):,} plays")
        return df

    def prepare_for_upload(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Prepare play-by-play data for Supabase upload.

        Args:
            df: Raw play-by-play DataFrame

        Returns:
            Processed DataFrame ready for upload
        """
        # Select key columns for database storage
        # This can be customized based on your analytics needs
        key_columns = [
            "play_id",
            "game_id",
            "season",
            "week",
            "game_date",
            "posteam",
            "defteam",
            "quarter",
            "time",
            "down",
            "ydstogo",
            "yardline_100",
            "play_type",
            "yards_gained",
            "epa",
            "wp",
            "wpa",
            "passer_player_name",
            "receiver_player_name",
            "rusher_player_name",
            "desc",
            "score_differential",
        ]

        # Filter to only columns that exist in the DataFrame
        available_columns = [col for col in key_columns if col in df.columns]
        
        result = df.select(available_columns)
        
        # Convert numeric columns to appropriate types for PostgreSQL
        # Cast integer columns that might be floats
        int_columns = ["season", "week", "quarter", "down", "ydstogo", 
                      "yardline_100", "yards_gained", "score_differential"]
        for col in int_columns:
            if col in result.columns:
                result = result.with_columns(
                    pl.col(col).cast(pl.Int32, strict=False)
                )
        
        # Remove duplicates based on play_id (keep first occurrence)
        if "play_id" in result.columns:
            result = result.unique(subset=["play_id"], keep="first")

        return result
