"""
Main script for extracting panel schedule data from images using Google Gemini API.
"""

from PIL import Image
from panel_extractor import PanelExtractor
from excel_writer import ExcelWriter
from csv_writer import PanelHeadersCSVWriter, PanelCircuitsCSVWriter
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
    
    # Initialize extractor and CSV writers
    extractor = PanelExtractor()
    headers_csv_path = get_output_path("panel_headers.csv")
    circuits_csv_path = get_output_path("panel_circuits.csv")
    headers_writer = PanelHeadersCSVWriter(headers_csv_path)
    circuits_writer = PanelCircuitsCSVWriter(circuits_csv_path)
    all_panels = []
    
    print(f"Writing results to:")
    print(f"  - {headers_csv_path}")
    print(f"  - {circuits_csv_path}")
    print("(Each panel will be saved immediately after processing)\n")
    
    # Process each image
    for idx, image_path in enumerate(image_files, 1):
        try:
            image = Image.open(image_path)
            image_name = image_path.split('/')[-1]
            
            panels = extractor.extract_from_image(image, image_name)
            
            # Write each panel to both CSV files immediately
            for panel in panels:
                headers_writer.write_panel_header(panel, image_name)
                circuits_writer.write_circuits(panel, image_name)
            
            all_panels.extend(panels)
            print(f"  → Progress: {idx}/{len(image_files)} images processed")
            
        except Exception as e:
            print(f"  ✗ Error loading {image_path}: {e}")
    
    # Generate Excel output at the end
    if all_panels:
        print("\n" + "="*60)
        print(f"GENERATING EXCEL OUTPUT")
        print("="*60)
        
        excel_output_path = get_output_path("panel_schedules.xlsx")
        
        writer = ExcelWriter(excel_output_path)
        writer.write_all_panels(all_panels)
        writer.save()
        
        print(f"\n✓ Successfully created:")
        print(f"  Panel Headers CSV: {headers_csv_path}")
        print(f"  Circuits CSV:      {circuits_csv_path}")
        print(f"  Excel:             {excel_output_path}")
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
