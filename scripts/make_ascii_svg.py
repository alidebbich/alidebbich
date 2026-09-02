#!/usr/bin/env python3
"""
Convert prepped grayscale image to self-typing monochrome ASCII SVG.
Wraps each row in a horizontal clip-path that wipes left-to-right,
staggered top to bottom for typewriter effect.
"""

from pathlib import Path
from PIL import Image
import sys

# ASCII ramp: bright (sparse) to dark (dense)
# Leading space clears the background
ASCII_RAMP = " .`:-=+*cs#%@"

def img_to_ascii(img_path: str, width: int = 100) -> list:
    """Convert grayscale image to ASCII art."""
    img = Image.open(img_path).convert('L')
    
    # Downsample to target width
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)  # 0.55 to account for character aspect ratio
    img = img.resize((width, height))
    
    pixels = img.getdata()
    ascii_lines = []
    
    for y in range(height):
        line = ""
        for x in range(width):
            pixel = pixels[y * width + x]
            # Normalize pixel to 0-1, then map to ASCII ramp
            normalized = pixel / 255.0
            ramp_index = int(normalized * (len(ASCII_RAMP) - 1))
            line += ASCII_RAMP[ramp_index]
        ascii_lines.append(line)
    
    return ascii_lines

def create_ascii_svg(ascii_lines: list, output_path: str = "avi-ascii.svg") -> None:
    """Create self-typing ASCII SVG with row-by-row animation."""
    
    char_width = 8
    char_height = 14
    line_height = 16
    
    width = len(ascii_lines[0]) * char_width
    height = len(ascii_lines) * line_height
    
    # Build SVG
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"',
        '     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">',
        '<defs>',
        '<style>',
        '@font-face { font-family: "Menlo"; src: local("Menlo"); }',
        'text { font-family: Menlo, monospace; font-size: 12px; fill: #a0a0a0; }',
        '</style>',
    ]
    
    # Add clip-path for each row
    for row_idx, line in enumerate(ascii_lines):
        y_pos = row_idx * line_height + 12
        clip_id = f"clip-row-{row_idx}"
        
        # Wipe animation: expands from 0 to full width
        # Stagger: each row starts after the previous one finishes
        start_time = row_idx * 0.05  # 50ms stagger
        duration = 0.5
        
        svg_lines.append(f'  <clipPath id="{clip_id}">')
        svg_lines.append(f'    <rect x="0" y="{y_pos - 12}" width="{width}" height="{line_height}">')
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{width}"')
        svg_lines.append(f'               begin="{start_time}s" dur="{duration}s" fill="freeze" />')
        svg_lines.append(f'    </rect>')
        svg_lines.append(f'  </clipPath>')
    
    svg_lines.append('</defs>')
    
    # Render each line with its clip-path
    for row_idx, line in enumerate(ascii_lines):
        y_pos = row_idx * line_height + 12
        clip_id = f"clip-row-{row_idx}"
        
        svg_lines.append(f'<text x="0" y="{y_pos}" clip-path="url(#{clip_id})">{line}</text>')
    
    svg_lines.append('</svg>')
    
    # Write file
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    
    print(f"✅ ASCII SVG saved to {output_path}")
    print(f"   Size: {len(ascii_lines)} rows × {len(ascii_lines[0])} chars")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "avi-ascii.svg"
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    print(f"Converting {input_file} to ASCII art...")
    ascii_art = img_to_ascii(input_file, width)
    create_ascii_svg(ascii_art, output_file)
