"""
OpenCV-based panel detection using contour detection.
"""

import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple
from paths import get_debug_path


def detect_panels_with_opencv(image: Image.Image, page_num: int, min_width_percent=10, min_height_percent=10, max_width_percent=95, max_height_percent=95, padding=20) -> List[Tuple[str, Image.Image]]:
    """
    Detect panel schedules using OpenCV contour detection.
    
    Args:
        image: PIL Image object
        page_num: Page number for naming
        min_width_percent: Minimum width as % of image width (default 5%)
        min_height_percent: Minimum height as % of image height (default 5%)
        max_width_percent: Maximum width as % of image width (default 60%)
        max_height_percent: Maximum height as % of image height (default 60%)
        padding: Pixels to add around detected border (default 20)
        
    Returns:
        List of tuples (panel_name, cropped_image)
    """
    # Convert PIL Image to OpenCV format
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Dilate to connect broken lines
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get bounding boxes and sort them (top to bottom, left to right)
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    bounding_boxes.sort(key=lambda x: (x[1] // 100, x[0]))
    
    # Filter and crop panels
    panels = []
    panel_count = 0
    
    img_height, img_width = img_bgr.shape[:2]
    min_width = img_width * (min_width_percent / 100)
    min_height = img_height * (min_height_percent / 100)
    max_width = img_width * (max_width_percent / 100)
    max_height = img_height * (max_height_percent / 100)
    
    print(f"  Found {len(contours)} contours, filtering for panels...")
    print(f"  Image size: {img_width}x{img_height}")
    print(f"  Looking for panels: width {min_width:.0f}-{max_width:.0f}px, height {min_height:.0f}-{max_height:.0f}px")
    
    for (x, y, w, h) in bounding_boxes:
        # Print size info for first few large contours for debugging
        if panel_count < 3 and (w > img_width * 0.05 or h > img_height * 0.05):
            print(f"    Contour: {w}x{h} ({w/img_width*100:.1f}% x {h/img_height*100:.1f}%)")
        
        # Filter: must be large enough but not too large (not the full page border)
        if (w > min_width and h > min_height and 
            w < max_width and h < max_height):
            # Add padding
            x_pad = max(0, x - padding)
            y_pad = max(0, y - padding)
            w_pad = min(img_width - x_pad, w + (padding * 2))
            h_pad = min(img_height - y_pad, h + (padding * 2))
            
            # Crop from original image
            crop_bgr = img_bgr[y_pad:y_pad+h_pad, x_pad:x_pad+w_pad]
            
            # Convert back to PIL Image
            crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_rgb)
            
            panel_count += 1
            panel_name = f"Panel_{panel_count:02d}"
            
            # Save cropped panel
            filename = f"page_{page_num:02d}_opencv_panel_{panel_count:02d}.png"
            save_path = get_debug_path(filename)
            crop_pil.save(save_path)
            
            panels.append((panel_name, crop_pil))
            print(f"    Saved: {filename} (Size: {w}x{h})")
    
    return panels
