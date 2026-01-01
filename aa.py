from PIL import Image
import os

def crop_panels(image_path, output_dir="cropped_panels"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        img = Image.open(image_path)
        width, height = img.size
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Define relative coordinates for each panel (Left, Top, Right, Bottom)
    # These coordinates are estimated based on the standard layout of your drawing sheet.
    # Format: (x_min, y_min, x_max, y_max) as percentages of the total image size.
    
    panel_coords = {
        "Panel_01_PC-DP-01-01": (0.08, 0.05, 0.30, 0.22), # Top Left (Distribution Panel)
        "Panel_02_PC-LP-01-02": (0.33, 0.04, 0.56, 0.28), # Top Middle
        "Panel_03_PC-LP-01-03": (0.58, 0.04, 0.81, 0.28), # Top Right
        
        "Panel_04_PC-LP-UPS-02-01": (0.08, 0.32, 0.30, 0.52), # Row 2 Left
        "Panel_05_PC-LP-UPS-02-02": (0.33, 0.32, 0.56, 0.52), # Row 2 Middle
        "Panel_06_PC-LP-INV-01-01": (0.58, 0.32, 0.81, 0.52), # Row 2 Right
        
        "Panel_07_PC-LP-03-03": (0.08, 0.53, 0.30, 0.72), # Row 3 Left
        "Panel_08_PC-LP-03-04": (0.33, 0.53, 0.56, 0.72), # Row 3 Middle
        
        "Panel_09_PC-LP-03-05": (0.08, 0.74, 0.30, 0.92), # Row 4 Left
        "Panel_10_PC-LP-03-06": (0.33, 0.74, 0.56, 0.92), # Row 4 Middle
    }

    print(f"Processing image: {image_path} ({width}x{height})")

    for name, coords in panel_coords.items():
        # Convert relative coords to absolute pixels
        left = int(coords[0] * width)
        top = int(coords[1] * height)
        right = int(coords[2] * width)
        bottom = int(coords[3] * height)

        # Crop and save
        cropped_img = img.crop((left, top, right, bottom))
        save_path = os.path.join(output_dir, f"{name}.jpg")
        cropped_img.save(save_path)
        print(f"Saved: {save_path}")

# --- USAGE ---
# Make sure 'page_03.jpg' is in the same folder as this script
crop_panels("page_03.png")