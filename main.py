"""
Main script for extracting panel schedule data from images using Google Gemini API.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from tkinter import Tk, filedialog, messagebox
from PIL import Image
from panel_extractor import PanelExtractor
from excel_writer import ExcelWriter
from csv_writer import PanelHeadersCSVWriter, PanelCircuitsCSVWriter, CombinedCSVWriter
from panel_schedule_image_extractor import extract_panel_schedules


def create_output_folder(base_location):
    """
    Create output folder with date-based naming.
    
    Args:
        base_location: Parent directory where output folder will be created
        
    Returns:
        Path: Path to the created output folder
    """
    # Generate folder name with today's date
    date_str = datetime.now().strftime("%y%m%d")
    folder_name = f"AI Panel Schedules - {date_str}"
    output_path = Path(base_location) / folder_name
    
    # Remove existing folder if it exists
    if output_path.exists():
        shutil.rmtree(output_path)
        print(f"  Removed existing folder: {folder_name}")
    
    # Create main output folder
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"  Created output folder: {output_path}")
    
    return output_path


def get_user_choice():
    """
    Ask user whether to use existing cropped images or extract from PDFs.
    
    Returns:
        str: 'images' or 'pdf', or None if cancelled
    """
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # Create custom dialog
    result = messagebox.askquestion(
        "Electrical Panel Schedule Extractor",
        "Choose your input method:\n\n" +
        "YES - Upload PDF Drawings\n" +
        "(Browse and select PDF files)\n\n" +
        "NO - Use Existing Panel Schedule Images\n" +
        "(Browse and select image folder)",
        icon='question'
    )
    
    root.destroy()
    
    if result == 'yes':
        print("\n✓ Selected: Upload PDF Drawings")
        return 'pdf'
    else:
        print("\n✓ Selected: Use Existing Panel Schedule Images")
        return 'images'


def browse_pdf_files():
    """
    Open file browser to select PDF files.
    
    Returns:
        list: List of selected PDF file paths
    """
    root = Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring dialog to front
    
    print("\n📂 Opening file browser to select PDF files...")
    file_paths = filedialog.askopenfilenames(
        title="Select PDF Drawing Files",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    root.destroy()
    
    if file_paths:
        print(f"✓ Selected {len(file_paths)} PDF file(s)")
        for path in file_paths:
            print(f"  - {Path(path).name}")
    else:
        print("❌ No files selected")
    
    return list(file_paths)


def browse_image_folder():
    """
    Open folder browser to select folder with panel schedule images.
    
    Returns:
        str: Path to selected folder, or None if cancelled
    """
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    print("\n📂 Opening folder browser to select image folder...")
    folder_path = filedialog.askdirectory(
        title="Select Folder with Panel Schedule Images"
    )
    
    root.destroy()
    
    if folder_path:
        print(f"✓ Selected folder: {folder_path}")
    else:
        print("❌ No folder selected")
    
    return folder_path if folder_path else None


def browse_output_location():
    """
    Open folder browser to select output location.
    
    Returns:
        str: Path to selected location, or None if cancelled
    """
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    print("\n📂 Opening folder browser to select output location...")
    folder_path = filedialog.askdirectory(
        title="Select Output Location"
    )
    
    root.destroy()
    
    if folder_path:
        print(f"✓ Selected output location: {folder_path}")
    else:
        print("❌ No location selected")
    
    return folder_path if folder_path else None


def extract_from_pdfs(output_base_path):
    """
    Extract panel schedule images from PDF drawings.
    
    Args:
        output_base_path: Base path where output folders will be created
    
    Returns:
        tuple: (bool, str) - Success status and path to extracted images folder
    """
    print("\n" + "="*60)
    print("PDF EXTRACTION MODE")
    print("="*60)
    
    # Browse for PDF files
    pdf_files = browse_pdf_files()
    
    if not pdf_files:
        return False, None
    
    # Create "Panel Schedule Images" subfolder for extracted images
    images_output_folder = output_base_path / "Panel Schedule Images"
    images_output_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        # Extract panel schedules from PDFs
        result = extract_panel_schedules(
            pdf_paths=pdf_files,
            output_folder=str(images_output_folder),
            cleanup_previous=True
        )
        
        if result["success"] and result["panel_schedules_found"] > 0:
            print(f"\n✓ Successfully extracted {result['panel_schedules_found']} panel schedule(s)")
            print(f"  Images saved to: {result['panel_schedule_folder']}")
            return True, result['panel_schedule_folder']
        else:
            print("\n❌ No panel schedules were found in the PDFs")
            return False, None
            
    except Exception as e:
        print(f"\n❌ Error during PDF extraction: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def process_images(image_folder, output_folder):
    """
    Process all images in the specified folder.
    
    Args:
        image_folder: Path to folder containing panel schedule images
        output_folder: Path to folder where outputs will be saved
    """
    print("\n" + "="*60)
    print("IMAGE PROCESSING MODE")
    print("="*60)
    
    # Get all images from folder
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    image_files = []
    
    for filename in sorted(os.listdir(image_folder)):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            image_files.append(str(Path(image_folder) / filename))
    
    if not image_files:
        print(f"\n❌ No images found in '{image_folder}'!")
        print("Supported formats: .png, .jpg, .jpeg, .bmp, .tiff")
        return
    
    print(f"\n✓ Found {len(image_files)} image(s) to process\n")
    
    # Create "Extracted Data" subfolder
    data_output_folder = Path(output_folder) / "Extracted Data"
    data_output_folder.mkdir(parents=True, exist_ok=True)
    
    # Initialize extractor and CSV writers
    extractor = PanelExtractor()
    headers_csv_path = str(data_output_folder / "panel_headers.csv")
    circuits_csv_path = str(data_output_folder / "panel_circuits.csv")
    combined_csv_path = str(data_output_folder / "panel_schedules_combined.csv")
    headers_writer = PanelHeadersCSVWriter(headers_csv_path)
    circuits_writer = PanelCircuitsCSVWriter(circuits_csv_path)
    combined_writer = CombinedCSVWriter(combined_csv_path)
    all_panels = []
    
    print(f"Writing results to: {data_output_folder}")
    print(f"  - panel_headers.csv")
    print(f"  - panel_circuits.csv")
    print(f"  - panel_schedules_combined.csv")
    print("(Each panel will be saved immediately after processing)\n")
    
    # Process each image
    for idx, image_path in enumerate(image_files, 1):
        try:
            image = Image.open(image_path)
            image_name = Path(image_path).name
            
            panels = extractor.extract_from_image(image, image_name)
            
            # Write each panel to all three CSV files immediately
            for panel in panels:
                headers_writer.write_panel_header(panel, image_name)
                circuits_writer.write_circuits(panel, image_name)
                combined_writer.write_panel(panel, image_name)
            
            all_panels.extend(panels)
            print(f"  → Progress: {idx}/{len(image_files)} images processed")
            
        except Exception as e:
            print(f"  ✗ Error loading {image_path}: {e}")
    
    # Generate Excel output at the end
    if all_panels:
        print("\n" + "="*60)
        print(f"GENERATING EXCEL OUTPUT")
        print("="*60)
        
        excel_output_path = str(data_output_folder / "panel_schedules.xlsx")
        
        writer = ExcelWriter(excel_output_path)
        writer.write_all_panels(all_panels)
        writer.save()
        
        print(f"\n✓ Successfully created:")
        print(f"  Panel Headers CSV:   {headers_csv_path}")
        print(f"  Circuits CSV:        {circuits_csv_path}")
        print(f"  Combined CSV:        {combined_csv_path}")
        print(f"  Excel:               {excel_output_path}")
        print(f"  Total panels extracted: {len(all_panels)}")
        print("="*60 + "\n")
    else:
        print("\n❌ No panels were extracted from the images.")
        print("="*60 + "\n")


def main():
    """Main entry point."""
    # Ask user for input method
    choice = get_user_choice()
    
    # Browse for output location
    output_location = browse_output_location()
    if not output_location:
        print("\n❌ No output location selected. Exiting.")
        return
    
    # Create dated output folder
    print("\n" + "="*60)
    print("CREATING OUTPUT FOLDER")
    print("="*60)
    output_folder = create_output_folder(output_location)
    
    image_folder_to_process = None
    
    if choice == 'pdf':
        # Extract from PDFs first
        success, extracted_images_folder = extract_from_pdfs(output_folder)
        if not success:
            print("\n❌ PDF extraction failed. Exiting.")
            return
        
        image_folder_to_process = extracted_images_folder
        
    else:  # choice == 'images'
        # Browse for existing images folder
        image_folder_to_process = browse_image_folder()
        if not image_folder_to_process:
            print("\n❌ No image folder selected. Exiting.")
            return
    
    # Process images
    process_images(image_folder_to_process, output_folder)
    
    print(f"\n✅ All outputs saved to: {output_folder}")


if __name__ == "__main__":
    main()
