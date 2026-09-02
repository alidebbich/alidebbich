#!/usr/bin/env python3
"""
Prep a photo for ASCII conversion:
1. Remove background with rembg
2. Boost local contrast with CLAHE
3. Composite onto white background
Output: source-prepped.png
"""

import sys
from pathlib import Path
import numpy as np
import cv2
from rembg import remove
from PIL import Image

def prep_photo(input_path: str, output_path: str = "source-prepped.png"):
    """Prepare photo for ASCII conversion."""
    
    # Read the input image
    print(f"📷 Reading {input_path}...")
    img = Image.open(input_path)
    
    # Remove background
    print("🔄 Removing background...")
    img_no_bg = remove(img)
    
    # Convert to numpy array for OpenCV processing
    img_array = np.array(img_no_bg)
    
    # Extract alpha channel for masking
    if img_array.shape[2] == 4:
        alpha = img_array[:, :, 3]
        rgb = img_array[:, :, :3]
    else:
        alpha = np.ones((img_array.shape[0], img_array.shape[1]), dtype=np.uint8) * 255
        rgb = img_array
    
    # Convert to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    print("✨ Boosting local contrast with CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrast_boosted = clahe.apply(gray)
    
    # Create white background and composite
    white_bg = np.ones_like(contrast_boosted) * 255
    
    # Normalize alpha to 0-1 for blending
    alpha_normalized = alpha.astype(float) / 255.0
    
    # Composite: subject on white background
    result = (contrast_boosted.astype(float) * alpha_normalized + 
              white_bg.astype(float) * (1 - alpha_normalized)).astype(np.uint8)
    
    # Save output
    output_img = Image.fromarray(result, mode='L')
    output_img.save(output_path)
    print(f"✅ Saved prepped image to {output_path}")
    print(f"   Size: {output_img.size}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image> [output_path]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    
    prep_photo(input_file, output_file)
