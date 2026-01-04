"""Script to get rushing touchdowns for season 2025 week 17."""
from src.supabase_client.client import SupabaseClient

def main():
    """Get rushing touchdowns for season 2025 week 17."""
    client = SupabaseClient()
    
    print("Fetching rushing touchdowns for 2025 season, week 17...")
    print("=" * 70)
    
    # Query player stats for season 2025, week 17, with rushing touchdowns
    result = client.client.table('player_stats') \
        .select('player_name, team, position, carries, rushing_yards, rushing_tds') \
        .eq('season', 2025) \
        .eq('week', 17) \
        .gt('rushing_tds', 0) \
        .order('rushing_tds', desc=True) \
        .execute()
    
    if not result.data:
        print("No rushing touchdown data found for 2025 season, week 17.")
        print("\nNote: Data may not be loaded yet. To load data, run:")
        print("  python scripts/load_data.py --season 2025 --data-types player_stats")
        return
    
    print(f"\nTotal players with rushing TDs: {len(result.data)}")
    print("\nRushing Touchdowns - 2025 Season, Week 17:")
    print("-" * 70)
    print(f"{'Rank':<6}{'Player':<25}{'Team':<6}{'Pos':<6}{'Carries':<10}{'Yards':<10}{'TDs':<5}")
    print("-" * 70)
    
    for i, player in enumerate(result.data, 1):
        player_name = player.get('player_name', 'Unknown')
        team = player.get('team', 'N/A')
        position = player.get('position', 'N/A')
        carries = player.get('carries', 0) or 0
        rushing_yards = player.get('rushing_yards', 0) or 0
        rushing_tds = player.get('rushing_tds', 0) or 0
        
        print(f"{i:<6}{player_name:<25}{team:<6}{position:<6}{carries:<10}{rushing_yards:<10}{rushing_tds:<5}")
    
    print("=" * 70)
    
    # Also calculate totals
    total_rushing_tds = sum(player.get('rushing_tds', 0) or 0 for player in result.data)
    total_rushing_yards = sum(player.get('rushing_yards', 0) or 0 for player in result.data)
    total_carries = sum(player.get('carries', 0) or 0 for player in result.data)
    
    print(f"\nTotals:")
    print(f"  Total Rushing TDs: {total_rushing_tds}")
    print(f"  Total Rushing Yards: {total_rushing_yards:,}")
    print(f"  Total Carries: {total_carries}")
    print("=" * 70)

if __name__ == "__main__":
    main()
