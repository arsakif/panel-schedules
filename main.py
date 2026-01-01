"""
Main script for extracting panel schedule data from images using Google Gemini API.
"""

from PIL import Image
from panel_extractor import PanelExtractor
from excel_writer import ExcelWriter
from paths import get_output_path, get_input_images


def process_images():
    """
    Process all images in the panel_schedule_images folder.
    """
    print("\n" + "="*60)
    print("ELECTRICAL PANEL SCHEDULE EXTRACTOR")
    print("="*60)
    
    # Get all images from input folder
    image_files = get_input_images()
    
    if not image_files:
        print("\n❌ No images found in 'panel_schedule_images/' folder!")
        print("\nPlease add panel schedule images to the 'panel_schedule_images/' folder.")
        print("Supported formats: .png, .jpg, .jpeg, .bmp, .tiff")
        return
    
    print(f"\n✓ Found {len(image_files)} image(s) to process\n")
    
    # Initialize extractor
    extractor = PanelExtractor()
    all_panels = []
    
    # Process each image
    for image_path in image_files:
        try:
            image = Image.open(image_path)
            image_name = image_path.split('/')[-1]
            
            panels = extractor.extract_from_image(image, image_name)
            all_panels.extend(panels)
            
        except Exception as e:
            print(f"  ✗ Error loading {image_path}: {e}")
    
    # Generate Excel output
    if all_panels:
        print("\n" + "="*60)
        print(f"GENERATING EXCEL OUTPUT")
        print("="*60)
        
        output_filename = "panel_schedules.xlsx"
        output_path = get_output_path(output_filename)
        
        writer = ExcelWriter()
        writer.create_workbook(all_panels, output_path)
        
        print(f"\n✓ Successfully created: {output_path}")
        print(f"  Total panels extracted: {len(all_panels)}")
        print("="*60 + "\n")
    else:
        print("\n❌ No panels were extracted from the images.")
        print("="*60 + "\n")


def main():
    """Main entry point."""
    process_images()


if __name__ == "__main__":
    main()
