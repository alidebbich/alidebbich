#!/usr/bin/env python3
"""
Fetch real contribution data from GitHub profile (no token needed).
Scrapes the public HTML at https://github.com/users/<username>/contributions
and exports JSON with day counts and derived stats.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_contributions(username: str, output_path: str = "data/contributions.json") -> dict:
    """Fetch and parse contribution data."""
    
    # Ensure data directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    url = f"https://github.com/users/{username}/contributions"
    
    print(f"🌐 Fetching contributions from {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching contributions: {e}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all day cells
    days = soup.find_all('td', {'data-date': True})
    
    contributions = {}
    total = 0
    today = datetime.now().date()
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for day_cell in reversed(days):  # Start from most recent
        date_str = day_cell.get('data-date')
        count_str = day_cell.get('data-count', '0')
        
        try:
            count = int(count_str)
        except (ValueError, TypeError):
            count = 0
        
        contributions[date_str] = count
        total += count
        
        # Track streaks
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if count > 0:
            if date == today or date == today - timedelta(days=1):
                current_streak += 1
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0
    
    # Find best day
    best_day = max(contributions.items(), key=lambda x: x[1]) if contributions else ("", 0)
    
    # Calculate monthly totals
    monthly_totals = {}
    for date_str, count in contributions.items():
        year_month = date_str[:7]  # YYYY-MM
        monthly_totals[year_month] = monthly_totals.get(year_month, 0) + count
    
    data = {
        "username": username,
        "updated_at": datetime.now().isoformat(),
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day[0],
        "best_day_count": best_day[1],
        "monthly_totals": monthly_totals,
        "daily_data": contributions,
    }
    
    # Write output
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Contributions saved to {output_path}")
    print(f"   Total: {total} contributions")
    print(f"   Current streak: {current_streak} days")
    print(f"   Longest streak: {longest_streak} days")
    
    return data

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "alidebbich"
    output = sys.argv[2] if len(sys.argv) > 2 else "data/contributions.json"
    
    fetch_contributions(username, output)
