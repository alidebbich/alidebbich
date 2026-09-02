#!/usr/bin/env python3
"""
Render contribution data as animated SVG heatmap.
Classic 53-week × 7-day grid with GitHub-ish green palette.
Reveals diagonally with slide-down animation.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# GitHub contribution palette (level 0-5)
PALETTE = [
    "#161b22",  # 0: none (dark background)
    "#0e4429",  # 1: low
    "#006d32",  # 2: medium-low
    "#26a641",  # 3: medium
    "#39d353",  # 4: high
    "#69f0a0",  # 5: very high (neon)
]

def load_contributions(data_path: str = "data/contributions.json") -> dict:
    """Load contribution data."""
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  {data_path} not found. Using empty data.")
        return {
            "username": "alidebbich",
            "total_contributions": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": "",
            "best_day_count": 0,
            "daily_data": {},
        }

def get_level(count: int) -> int:
    """Map contribution count to level 0-5."""
    if count == 0:
        return 0
    elif count < 5:
        return 1
    elif count < 10:
        return 2
    elif count < 20:
        return 3
    elif count < 30:
        return 4
    else:
        return 5

def create_heatmap_svg(data: dict, output_path: str = "contrib-heatmap.svg") -> None:
    """Create animated contribution heatmap SVG."""
    
    # Constants
    box_size = 13
    box_gap = 2
    cell_size = box_size + box_gap
    
    legend_y_offset = 280  # Space for grid
    footer_y_offset = 320
    
    width = (53 * cell_size) + 40  # 53 weeks + margins
    height = footer_y_offset + 60
    
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"',
        '     xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<style>',
        '.month-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 11px; fill: #8b949e; text-anchor: start; }',
        '.day-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 11px; fill: #8b949e; text-anchor: middle; }',
        '.legend-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 10px; fill: #8b949e; }',
        '.stat { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 12px; fill: #c9d1d9; }',
        '.stat-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 10px; fill: #8b949e; }',
        '</style>',
        '</defs>',
        '',
    ]
    
    daily_data = data.get("daily_data", {})
    
    # Build week grid (Sun-Sat, going backwards from today)
    today = datetime.now().date()
    start_date = today - timedelta(days=365)
    
    # Align to Sunday for the grid
    while start_date.weekday() != 6:  # 6 = Sunday
        start_date -= timedelta(days=1)
    
    # Group dates into weeks
    weeks = []
    current_week = []
    current_date = start_date
    
    while current_date <= today:
        current_week.append(current_date)
        if len(current_week) == 7 or current_date == today:
            weeks.append(current_week)
            current_week = []
        current_date += timedelta(days=1)
    
    # Render grid
    margin_left = 30
    margin_top = 30
    
    for week_idx, week in enumerate(weeks):
        x = margin_left + (week_idx * cell_size)
        
        for day_idx, date in enumerate(week):
            y = margin_top + (day_idx * cell_size)
            
            date_str = date.strftime("%Y-%m-%d")
            count = daily_data.get(date_str, 0)
            level = get_level(count)
            color = PALETTE[level]
            
            # Animation: staggered slide-down
            # Calculate distance from top-left corner for diagonal effect
            diagonal_delay = (week_idx * 0.03) + (day_idx * 0.02)
            
            if count > 0 or True:  # Always render (including empty days)
                rect_id = f"box-{week_idx}-{day_idx}"
                svg_lines.append(
                    f'<rect id="{rect_id}" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
                    f'fill="{color}" rx="2" ry="2">'
                )
                svg_lines.append(
                    f'  <animate attributeName="opacity" from="0" to="1" '
                    f'begin="{diagonal_delay}s" dur="0.3s" fill="freeze" />'
                )
                svg_lines.append('</rect>')
                svg_lines.append(f'<title>{date_str}: {count} contributions</title>')
    
    # Legend: Less ← → More
    legend_y = legend_y_offset
    svg_lines.append(f'<text x="{margin_left}" y="{legend_y + 20}" class="legend-label">Less</text>')
    
    for level in range(6):
        legend_x = margin_left + 50 + (level * 16)
        svg_lines.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="12" height="12" '
            f'fill="{PALETTE[level]}" rx="2" ry="2" />'
        )
    
    svg_lines.append(f'<text x="{margin_left + 50 + 110}" y="{legend_y + 20}" class="legend-label">More</text>')
    
    # Stats footer
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    best_day_count = data.get("best_day_count", 0)
    
    stats_text = f"{total:,} contributions in the last year"
    svg_lines.append(
        f'<text x="{margin_left}" y="{footer_y_offset + 30}" class="stat">{stats_text}</text>'
    )
    
    if current_streak > 0:
        svg_lines.append(
            f'<text x="{margin_left}" y="{footer_y_offset + 50}" class="stat-label">'
            f'🔥 {current_streak}-day streak</text>'
        )
    
    svg_lines.append('</svg>')
    
    # Write file
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    
    print(f"✅ Heatmap SVG saved to {output_path}")
    print(f"   Contributions: {total}")
    print(f"   Current streak: {current_streak} days")

if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    
    data = load_contributions(data_path)
    create_heatmap_svg(data, output_path)
