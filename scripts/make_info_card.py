#!/usr/bin/env python3
"""
Hand-author a neofetch-style info card SVG with fade-in animations.
Customize the content (Now, Prev, Stack, Highlights) here.
"""

import os

def create_info_card_svg(output_path: str = "info-card.svg") -> None:
    """Create an animated neofetch-style card."""
    
    # Customize these fields
    card_data = [
        ("Now", "Full Stack Developer"),
        ("Prev", "Contract Development"),
        ("Stack", "JavaScript, Python, React"),
        ("Highlights", "53-week contribution streak"),
    ]
    
    # Dimensions
    card_width = 490
    card_height = 280
    margin_x = 20
    margin_y = 20
    line_height = 40
    
    static = os.getenv("STATIC") == "1"
    
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{card_width}" height="{card_height}" viewBox="0 0 {card_width} {card_height}"',
        '     xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<style>',
        '@font-face { font-family: "Menlo"; src: local("Menlo"); }',
        '.title { font-family: Menlo, monospace; font-size: 13px; font-weight: bold; fill: #58a6ff; }',
        '.key { font-family: Menlo, monospace; font-size: 12px; fill: #79c0ff; }',
        '.value { font-family: Menlo, monospace; font-size: 12px; fill: #c9d1d9; }',
        '.border { stroke: #30363d; stroke-width: 1; fill: none; }',
        '</style>',
        '</defs>',
        '',
        '<!-- Border -->',
        f'<rect x="1" y="1" width="{card_width-2}" height="{card_height-2}" class="border"/>',
        '',
        '<!-- Title bar -->',
        f'<rect x="1" y="1" width="{card_width-2}" height="30" fill="#161b22" stroke="#30363d" stroke-width="1"/>',
        f'<text x="10" y="21" class="title">alidebbich@github</text>',
        '',
        '<!-- Content lines -->',
    ]
    
    for idx, (key, value) in enumerate(card_data):
        y_pos = 50 + (idx * line_height)
        
        # Key
        svg_lines.append(f'<text x="{margin_x}" y="{y_pos}" class="key">{key}:</text>')
        
        # Value with fade-in animation (if not static)
        if static:
            svg_lines.append(f'<text x="120" y="{y_pos}" class="value">{value}</text>')
        else:
            start_time = 0.3 + (idx * 0.1)
            svg_lines.append(f'<text x="120" y="{y_pos}" class="value">')
            svg_lines.append(f'  <tspan>{value}</tspan>')
            svg_lines.append(f'  <animate attributeName="opacity" from="0" to="1"')
            svg_lines.append(f'           begin="{start_time}s" dur="0.3s" fill="freeze" />')
            svg_lines.append(f'</text>')
    
    svg_lines.append('</svg>')
    
    # Write file
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    
    print(f"✅ Info card saved to {output_path}")

if __name__ == "__main__":
    create_info_card_svg()
