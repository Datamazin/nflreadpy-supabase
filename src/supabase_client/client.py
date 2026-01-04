"""Supabase client for database operations."""

from typing import Any, Dict, List, Optional

import polars as pl
from supabase import Client, create_client

from ..utils.config import get_settings


class SupabaseClient:
    """Client for interacting with Supabase."""

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize Supabase client.

        Args:
            url: Supabase project URL (defaults to config)
            key: Supabase API key (defaults to config)
        """
        settings = get_settings()
        self.url = url or settings.supabase_url
        self.key = key or settings.supabase_key
        self.client: Client = create_client(self.url, self.key)

    def upload_dataframe(
        self,
        df: pl.DataFrame,
        table_name: str,
        batch_size: int = 1000,
        upsert: bool = False,
    ) -> Dict[str, Any]:
        """
        Upload a Polars DataFrame to Supabase table.

        Args:
            df: Polars DataFrame to upload
            table_name: Name of the table
            batch_size: Number of rows per batch
            upsert: If True, use upsert instead of insert

        Returns:
            Dictionary with upload statistics
        """
        total_rows = len(df)
        print(f"Uploading {total_rows:,} rows to '{table_name}' table...")

        # Convert to list of dicts for Supabase
        records = df.to_dicts()

        uploaded = 0
        errors = []

        # Upload in batches
        for i in range(0, total_rows, batch_size):
            batch = records[i : i + batch_size]
            try:
                if upsert:
                    self.client.table(table_name).upsert(batch).execute()
                else:
                    self.client.table(table_name).insert(batch).execute()
                uploaded += len(batch)
                print(f"  Progress: {uploaded:,}/{total_rows:,} rows")
            except Exception as e:
                errors.append({"batch": i, "error": str(e)})
                print(f"  Error uploading batch {i}: {e}")

        return {
            "total_rows": total_rows,
            "uploaded": uploaded,
            "errors": len(errors),
            "error_details": errors,
        }

    def query(
        self, table_name: str, filters: Optional[Dict[str, Any]] = None
    ) -> pl.DataFrame:
        """
        Query data from a Supabase table.

        Args:
            table_name: Name of the table
            filters: Optional dictionary of column:value filters

        Returns:
            Polars DataFrame with query results
        """
        query = self.client.table(table_name).select("*")

        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)

        response = query.execute()
        return pl.DataFrame(response.data)

    def execute_sql(self, sql: str) -> Any:
        """
        Execute raw SQL query.

        Args:
            sql: SQL query string

        Returns:
            Query results
        """
        return self.client.rpc("execute_sql", {"query": sql}).execute()

    def delete_records(
        self, table_name: str, filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Delete records from a table.

        Args:
            table_name: Name of the table
            filters: Dictionary of column:value filters for deletion

        Returns:
            Dictionary with deletion statistics
        """
        query = self.client.table(table_name).delete()

        for column, value in filters.items():
            query = query.eq(column, value)

        response = query.execute()
        return {"deleted": len(response.data)}

    def get_table_count(self, table_name: str) -> int:
        """
        Get the count of rows in a table.

        Args:
            table_name: Name of the table

        Returns:
            Number of rows
        """
        response = (
            self.client.table(table_name).select("*", count="exact").execute()
        )
        return response.count if response.count else 0
