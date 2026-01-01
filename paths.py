"""
Path management for panel schedule extraction project.
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "panel_schedule_images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_output_path(filename: str) -> str:
    """Get full path for output file."""
    return os.path.join(OUTPUT_DIR, filename)


def get_input_images():
    """Get list of all image files in the input directory."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    images = []
    
    if not os.path.exists(INPUT_DIR):
        return images
    
    for filename in sorted(os.listdir(INPUT_DIR)):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            images.append(os.path.join(INPUT_DIR, filename))
    
    return images
