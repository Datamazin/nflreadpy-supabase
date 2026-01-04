"""
Setup database schema in Supabase.

This script reads the schema.sql file and provides instructions
for setting it up in Supabase.
"""

from pathlib import Path


def main():
    """Display database setup instructions."""
    schema_file = Path(__file__).parent.parent / "sql" / "schema.sql"

    print("=" * 70)
    print("NFL Analytics Database Setup")
    print("=" * 70)
    print()
    print("To set up your Supabase database:")
    print()
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to the SQL Editor")
    print("3. Copy and paste the contents of sql/schema.sql")
    print("4. Run the SQL script")
    print()
    print("The schema file is located at:")
    print(f"   {schema_file}")
    print()
    print("Schema includes tables for:")
    print("  • play_by_play - Play-by-play data")
    print("  • player_stats - Player statistics")
    print("  • team_stats - Team statistics")
    print("  • rosters - Team rosters")
    print("  • schedules - Game schedules")
    print("  • players - Player reference data")
    print("  • teams - Team reference data")
    print()
    print("=" * 70)
    print()

    # Read and display the schema
    with open(schema_file, "r") as f:
        schema_content = f.read()

    print("Schema SQL Preview (first 1000 characters):")
    print("-" * 70)
    print(schema_content[:1000])
    print("...")
    print("-" * 70)
    print()
    print("For the complete schema, open:")
    print(f"   {schema_file}")
    print()


if __name__ == "__main__":
    main()
