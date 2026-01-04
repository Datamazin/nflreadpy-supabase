"""Data loader for NFL team statistics and rosters."""

from typing import List, Literal, Optional, Union

import nflreadpy as nfl
import polars as pl


class TeamDataLoader:
    """Load NFL team data using nflreadpy."""

    def __init__(self):
        """Initialize the team data loader."""
        pass

    def load_team_stats(
        self,
        seasons: Union[int, List[int], None] = None,
        summary_level: Literal["week", "reg", "post", "reg+post"] = "week",
    ) -> pl.DataFrame:
        """
        Load team statistics for specified seasons.

        Args:
            seasons: Season(s) to load. If None, loads current season.
            summary_level: Summary level ("week", "reg", "post", "reg+post").

        Returns:
            Polars DataFrame with team statistics enriched with points from schedules.
        """
        print(f"Loading team stats for seasons: {seasons}, level: {summary_level}")
        stats = nfl.load_team_stats(seasons, summary_level)
        print(f"Loaded stats for {len(stats):,} team-game records")
        
        # Load schedules to get points data
        schedules = nfl.load_schedules(seasons)
        
        # Create lookup for points: team + season + week -> points
        # Each game appears in schedules once, so we need to create entries for both teams
        home_points = schedules.select([
            pl.col("season"),
            pl.col("week"),
            pl.col("home_team").alias("team"),
            pl.col("home_score").alias("points")
        ])
        
        away_points = schedules.select([
            pl.col("season"),
            pl.col("week"),
            pl.col("away_team").alias("team"),
            pl.col("away_score").alias("points")
        ])
        
        # Combine home and away points
        points_lookup = pl.concat([home_points, away_points])
        
        # Join points back to stats
        stats = stats.join(
            points_lookup,
            on=["season", "week", "team"],
            how="left"
        )
        
        return stats

    def load_rosters(
        self, seasons: Union[int, List[int], None] = None
    ) -> pl.DataFrame:
        """
        Load team rosters for specified seasons.

        Args:
            seasons: Season(s) to load. If None, loads current roster year.

        Returns:
            Polars DataFrame with roster data.
        """
        print(f"Loading rosters for seasons: {seasons}")
        df = nfl.load_rosters(seasons)
        print(f"Loaded {len(df):,} roster entries")
        return df

    def load_schedules(
        self, seasons: Union[int, List[int], None] = None
    ) -> pl.DataFrame:
        """
        Load game schedules for specified seasons.

        Args:
            seasons: Season(s) to load.

        Returns:
            Polars DataFrame with schedule data.
        """
        print(f"Loading schedules for seasons: {seasons}")
        df = nfl.load_schedules(seasons)
        print(f"Loaded {len(df):,} games")
        return df

    def load_team_info(self) -> pl.DataFrame:
        """
        Load team information including colors, logos, etc.

        Returns:
            Polars DataFrame with team data.
        """
        print("Loading team information...")
        df = nfl.load_teams()
        print(f"Loaded info for {len(df):,} teams")
        return df

    def prepare_for_upload(
        self, df: pl.DataFrame, data_type: str = "stats"
    ) -> pl.DataFrame:
        """
        Prepare team data for Supabase upload.

        Args:
            df: Raw DataFrame
            data_type: Type of data ("stats", "rosters", "schedules", "info")

        Returns:
            Processed DataFrame ready for upload
        """
        if data_type == "schedules":
            # Select only columns that exist in the database schema
            schema_columns = [
                "game_id", "season", "week", "game_type", "gameday",
                "home_team", "away_team", "home_score", "away_score",
                "stadium", "location", "roof", "surface", "temp", "wind"
            ]
            available = [col for col in schema_columns if col in df.columns]
            df = df.select(available)
            
            # Rename gameday to game_date to match database schema
            if "gameday" in df.columns:
                df = df.rename({"gameday": "game_date"})
            
            # Cast numeric columns
            int_cols = ["season", "week", "home_score", "away_score", "temp", "wind"]
            for col in int_cols:
                if col in df.columns:
                    df = df.with_columns(pl.col(col).cast(pl.Int32, strict=False))
        
        elif data_type == "rosters":
            # Filter out rows with null gsis_id FIRST (maps to player_id primary key)
            if "gsis_id" in df.columns:
                df = df.filter(pl.col("gsis_id").is_not_null())
            
            # Convert date to string BEFORE renaming (for JSON serialization)
            if "birth_date" in df.columns:
                df = df.with_columns(
                    pl.col("birth_date").cast(pl.Utf8).alias("birth_date")
                )
            
            # Rename columns to match database schema
            rename_map = {}
            if "gsis_id" in df.columns:
                rename_map["gsis_id"] = "player_id"
            if "full_name" in df.columns:
                rename_map["full_name"] = "player_name"
            if rename_map:
                df = df.rename(rename_map)
            
            # Select only columns that exist in the database schema
            schema_columns = [
                "player_id", "player_name", "season", "team", "position",
                "depth_chart_position", "jersey_number", "status",
                "height", "weight", "birth_date", "college"
            ]
            available = [col for col in schema_columns if col in df.columns]
            result = df.select(available)
            
            # Cast numeric columns
            int_cols = ["season", "jersey_number", "weight"]
            for col in int_cols:
                if col in result.columns:
                    result = result.with_columns(pl.col(col).cast(pl.Int32, strict=False))
        
        elif data_type == "info":
            # Team info
            schema_columns = [
                "team_abbr", "team_name", "team_nick", "team_color", 
                "team_color2", "team_logo_espn", "team_logo_wikipedia",
                "team_conference", "team_division"
            ]
            available = [col for col in schema_columns if col in df.columns]
            df = df.select(available)
        
        elif data_type == "stats":
            # Calculate derived fields before selecting columns
            
            # 1. Calculate total_yards = passing_yards + rushing_yards
            if "passing_yards" in df.columns and "rushing_yards" in df.columns:
                df = df.with_columns(
                    (pl.col("passing_yards").fill_null(0) + pl.col("rushing_yards").fill_null(0)).alias("total_yards")
                )
            
            # 2. Calculate turnovers = interceptions + fumbles_lost
            turnover_cols = []
            if "passing_interceptions" in df.columns:
                turnover_cols.append(pl.col("passing_interceptions").fill_null(0))
            if "rushing_fumbles_lost" in df.columns:
                turnover_cols.append(pl.col("rushing_fumbles_lost").fill_null(0))
            if "sack_fumbles_lost" in df.columns:
                turnover_cols.append(pl.col("sack_fumbles_lost").fill_null(0))
            
            if turnover_cols:
                df = df.with_columns(
                    pl.sum_horizontal(*turnover_cols).alias("turnovers")
                )
            
            # 3. Rename opponent_team to opponent
            if "opponent_team" in df.columns:
                df = df.rename({"opponent_team": "opponent"})
            
            # 4. Rename passing_interceptions to interceptions
            if "passing_interceptions" in df.columns:
                df = df.rename({"passing_interceptions": "interceptions"})
            
            # Team stats - select only columns in schema
            schema_columns = [
                "team", "season", "week", "opponent", "completions", "attempts",
                "passing_yards", "passing_tds", "interceptions", "carries",
                "rushing_yards", "rushing_tds", "total_yards", "turnovers", "points"
            ]
            available = [col for col in schema_columns if col in df.columns]
            df = df.select(available)
            
            # Cast numeric columns
            int_cols = ["season", "week", "completions", "attempts", "passing_yards",
                       "passing_tds", "interceptions", "carries", "rushing_yards",
                       "rushing_tds", "total_yards", "turnovers", "points"]
            for col in int_cols:
                if col in df.columns:
                    df = df.with_columns(pl.col(col).cast(pl.Int32, strict=False))
        
        # Return result for rosters, df for all others
        if data_type == "rosters":
            return result
        return df
