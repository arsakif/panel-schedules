"""
Main script for processing electrical panel schedules from PDF drawings.
"""

import fitz  # PyMuPDF
from PIL import Image
import io
import os
import sys
from panel_extractor import PanelExtractor
from excel_writer import ExcelWriter
import config
from paths import OUTPUT_DIR, get_output_path, get_debug_path

# Increase PIL's image size limit for high-DPI images
Image.MAX_IMAGE_PIXELS = None


def pdf_to_images(pdf_path: str) -> list:
    """
    Convert PDF pages to PIL Images.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of PIL Image objects, one per page
    """
    images = []
    
    try:
        pdf_document = fitz.open(pdf_path)
        print(f"Processing PDF: {pdf_path}")
        print(f"Total pages: {len(pdf_document)}")
        
        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document[page_num]
            
            # Render page to an image (pixmap)
            # Use matrix to increase resolution (zoom factor)
            zoom = config.DPI / 72  # 72 is the default DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert pixmap to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
            
            print(f"  Converted page {page_num + 1} to image")
        
        pdf_document.close()
        return images
        
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []


def process_pdf(pdf_path: str, output_filename: str = None) -> None:
    """
    Process a PDF file and extract panel schedules to Excel.
    
    Args:
        pdf_path: Path to the input PDF file
        output_filename: Optional custom output filename for Excel
    """
    # Validate input file
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: File must be a PDF: {pdf_path}")
        return
    
    # Generate output filename if not provided
    if output_filename is None:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_filename = f"{base_name}_panel_schedules.xlsx"
    
    # Get output path
    output_path = get_output_path(output_filename)
    
    print("\n" + "="*60)
    print("ELECTRICAL PANEL SCHEDULE EXTRACTOR")
    print("="*60 + "\n")
    
    # Step 1: Convert PDF to images
    print("Step 1: Converting PDF pages to images...")
    images = pdf_to_images(pdf_path)
    
    if not images:
        print("Error: Could not convert PDF to images")
        return
    
    print(f"Successfully converted {len(images)} page(s)\n")
    
    # Step 2: Extract panel data using Gemini
    print("Step 2: Detecting panel locations and cropping images...")
    extractor = PanelExtractor()
    panels = extractor.extract_from_pdf_page_images(images)
    
    if len(panels) == 0:
        print("\nPanel detection complete. No data extraction performed yet.")
        print("Check debug_images/ folder to verify the cropped panels.")
        return
    
    print(f"\nSuccessfully extracted {len(panels)} panel schedule(s)\n")
    
    # Step 3: Skipped for now
    print("Step 3: Skipped - Data extraction not performed yet")
    
    print("\n" + "="*60)
    print("DETECTION COMPLETE")
    print("="*60)
    print(f"Cropped panel images saved in: debug_images/")
    print("Please verify the cropped panels before proceeding with data extraction.")
    print()


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_file_path> [output_filename.xlsx]")
        print("\nExample:")
        print("  python main.py drawings/electrical_plan.pdf")
        print("  python main.py drawings/electrical_plan.pdf custom_output.xlsx")
        return
    
    pdf_path = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_pdf(pdf_path, output_filename)


if __name__ == "__main__":
    main()
