"""Test script to get passing yards leaders by team."""
from src.supabase_client.client import SupabaseClient
from collections import defaultdict

client = SupabaseClient()

# Get all player stats for 2024 season (need to paginate to get all 18k+ records)
print("Fetching player stats for 2024 season...")

all_data = []
page_size = 1000
offset = 0

while True:
    result = client.client.table('player_stats') \
        .select('player_name, team, passing_yards') \
        .eq('season', 2024) \
        .range(offset, offset + page_size - 1) \
        .execute()
    
    if not result.data:
        break
    
    all_data.extend(result.data)
    offset += page_size
    print(f"Fetched {len(all_data)} records...")
    
    if len(result.data) < page_size:
        break

print(f"Total records: {len(all_data)}")

# Aggregate passing yards by team
team_totals = defaultdict(int)
for record in all_data:
    if record['passing_yards']:
        team_totals[record['team']] += record['passing_yards']

# Sort and display top 10
sorted_teams = sorted(team_totals.items(), key=lambda x: x[1], reverse=True)

print("\nTop 10 Teams by Passing Yards (2024 Season):")
print("-" * 50)
for i, (team, yards) in enumerate(sorted_teams[:10], 1):
    print(f"{i:2}. {team:4} - {yards:,} yards")
