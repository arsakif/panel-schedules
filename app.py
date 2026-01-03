"""
Streamlit web application for extracting panel schedule data from images.
Accessible via web browser on local network.
"""

import os
import shutil
import streamlit as st
from pathlib import Path
from datetime import datetime
from PIL import Image
import tempfile
import zipfile
from io import BytesIO

from panel_extractor import PanelExtractor
from excel_writer import ExcelWriter
from csv_writer import PanelHeadersCSVWriter, PanelCircuitsCSVWriter, CombinedCSVWriter
from panel_schedule_image_extractor import extract_panel_schedules


# Page configuration
st.set_page_config(
    page_title="SKF Panel Schedule Extractor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add logo if it exists
if os.path.exists("Logo_white.png"):
    st.sidebar.image("Logo_white.png", width=200)

st.title("⚡ Electrical Panel Schedule Extractor")
st.markdown("---")


def create_output_folder():
    """Create temporary output folder with date-based naming."""
    date_str = datetime.now().strftime("%y%m%d")
    folder_name = f"AI_Panel_Schedules_{date_str}"
    output_path = Path(tempfile.gettempdir()) / folder_name
    
    if output_path.exists():
        shutil.rmtree(output_path)
    
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def process_images(image_files, status_container):
    """Process uploaded images and extract panel data."""
    
    # Create output folder
    output_folder = create_output_folder()
    data_output_folder = output_folder / "Extracted_Data"
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
    
    # Progress bar
    progress_bar = status_container.progress(0)
    status_text = status_container.empty()
    
    # Process each image
    for idx, uploaded_file in enumerate(image_files):
        try:
            # Update progress
            progress = (idx + 1) / len(image_files)
            progress_bar.progress(progress)
            status_text.text(f"Processing {uploaded_file.name} ({idx + 1}/{len(image_files)})...")
            
            # Load image
            image = Image.open(uploaded_file)
            
            # Extract panel data
            panels = extractor.extract_from_image(image, uploaded_file.name)
            
            # Write each panel to CSV files immediately
            for panel in panels:
                headers_writer.write_panel_header(panel, uploaded_file.name)
                circuits_writer.write_circuits(panel, uploaded_file.name)
                combined_writer.write_panel(panel, uploaded_file.name)
            
            all_panels.extend(panels)
            
        except Exception as e:
            status_container.error(f"Error processing {uploaded_file.name}: {e}")
    
    # Generate Excel output
    if all_panels:
        status_text.text("Generating Excel output...")
        excel_output_path = str(data_output_folder / "panel_schedules.xlsx")
        
        writer = ExcelWriter(excel_output_path)
        writer.write_all_panels(all_panels)
        writer.save()
        
        status_text.text("✓ Processing complete!")
        progress_bar.progress(1.0)
        
        return {
            "success": True,
            "panels_count": len(all_panels),
            "headers_csv": headers_csv_path,
            "circuits_csv": circuits_csv_path,
            "combined_csv": combined_csv_path,
            "excel": excel_output_path,
            "output_folder": data_output_folder
        }
    else:
        status_container.error("No panels were extracted from the images.")
        return {"success": False}


def process_pdfs(pdf_files, status_container):
    """Extract panel schedules from PDF files."""
    
    # Create output folder
    output_folder = create_output_folder()
    images_folder = output_folder / "Panel_Schedule_Images"
    images_folder.mkdir(parents=True, exist_ok=True)
    
    status_container.info("Extracting panel schedules from PDFs...")
    
    try:
        # Save PDFs temporarily
        temp_pdf_paths = []
        for pdf_file in pdf_files:
            temp_path = Path(tempfile.gettempdir()) / pdf_file.name
            with open(temp_path, "wb") as f:
                f.write(pdf_file.read())
            temp_pdf_paths.append(str(temp_path))
        
        # Extract panel schedules
        result = extract_panel_schedules(
            pdf_paths=temp_pdf_paths,
            output_folder=str(images_folder),
            cleanup_previous=True
        )
        
        # Clean up temp PDFs
        for temp_path in temp_pdf_paths:
            os.remove(temp_path)
        
        if result["success"] and result["panel_schedules_found"] > 0:
            status_container.success(f"✓ Extracted {result['panel_schedules_found']} panel schedule(s) from PDFs")
            
            # Get extracted image files
            image_folder = Path(result['panel_schedule_folder'])
            image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
            image_paths = []
            
            for filename in sorted(os.listdir(image_folder)):
                if any(filename.lower().endswith(ext) for ext in image_extensions):
                    image_paths.append(image_folder / filename)
            
            return image_paths
        else:
            status_container.error("No panel schedules found in the PDFs")
            return None
            
    except Exception as e:
        status_container.error(f"Error during PDF extraction: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_download_zip(output_folder):
    """Create a zip file of all output files for download."""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in output_folder.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(output_folder)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    return zip_buffer


# Main UI
st.sidebar.header("📤 Upload Files")

# Choose input method
input_method = st.sidebar.radio(
    "Select input method:",
    ["Upload Panel Schedule Images", "Upload PDF Drawings"],
    index=1
)

st.sidebar.markdown("---")

# File uploader based on method
if input_method == "Upload Panel Schedule Images":
    uploaded_files = st.sidebar.file_uploader(
        "Choose panel schedule images",
        type=["png", "jpg", "jpeg", "bmp", "tiff"],
        accept_multiple_files=True,
        help="Upload one or more panel schedule images"
    )
    
    if uploaded_files:
        st.sidebar.success(f"✓ {len(uploaded_files)} image(s) uploaded")
        
        # Show preview of uploaded images
        with st.expander("🖼️ Preview Uploaded Images"):
            cols = st.columns(3)
            for idx, uploaded_file in enumerate(uploaded_files):
                with cols[idx % 3]:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=uploaded_file.name, use_container_width=True)
                    uploaded_file.seek(0)  # Reset file pointer

else:  # Upload PDF Drawings
    uploaded_files = st.sidebar.file_uploader(
        "Choose PDF drawings",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files containing panel schedules"
    )
    
    if uploaded_files:
        st.sidebar.success(f"✓ {len(uploaded_files)} PDF(s) uploaded")
        
        # Show list of uploaded PDFs
        with st.expander("📄 Uploaded PDF Files"):
            for uploaded_file in uploaded_files:
                st.write(f"- {uploaded_file.name}")

# Process button
if uploaded_files:
    st.sidebar.markdown("---")
    if st.sidebar.button("🚀 Start Processing", type="primary", use_container_width=True):
        
        # Create status container in main area
        status_container = st.container()
        
        with st.spinner("Processing..."):
            
            if input_method == "Upload PDF Drawings":
                # First extract images from PDFs
                extracted_images = process_pdfs(uploaded_files, status_container)
                
                if extracted_images:
                    # Convert paths to file-like objects for processing
                    image_files_to_process = []
                    for img_path in extracted_images:
                        with open(img_path, 'rb') as f:
                            image_files_to_process.append(BytesIO(f.read()))
                            image_files_to_process[-1].name = img_path.name
                    
                    # Process the extracted images
                    result = process_images(image_files_to_process, status_container)
                else:
                    result = {"success": False}
            else:
                # Process images directly
                result = process_images(uploaded_files, status_container)
            
            if result["success"]:
                st.success(f"✅ Successfully extracted {result['panels_count']} panel(s)!")
                
                st.markdown("---")
                st.subheader("📥 Download Results")
                
                # Create download buttons for each file
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    with open(result["headers_csv"], "rb") as f:
                        st.download_button(
                            label="📄 Download Panel Headers CSV",
                            data=f.read(),
                            file_name="panel_headers.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                with col2:
                    with open(result["circuits_csv"], "rb") as f:
                        st.download_button(
                            label="📄 Download Circuits CSV",
                            data=f.read(),
                            file_name="panel_circuits.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                with col3:
                    with open(result["combined_csv"], "rb") as f:
                        st.download_button(
                            label="📄 Download Combined CSV",
                            data=f.read(),
                            file_name="panel_schedules_combined.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                # Excel download
                st.markdown("")
                with open(result["excel"], "rb") as f:
                    st.download_button(
                        label="📊 Download Excel File",
                        data=f.read(),
                        file_name="panel_schedules.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                # Download all as ZIP
                st.markdown("")
                zip_data = create_download_zip(result["output_folder"])
                st.download_button(
                    label="📦 Download All Files (ZIP)",
                    data=zip_data,
                    file_name=f"panel_schedules_{datetime.now().strftime('%y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )

else:
    # Show instructions
    st.info("👈 Upload files using the sidebar to get started")
    
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. **Choose Input Method** - Select either panel schedule images or PDF drawings
    2. **Upload Files** - Use the file uploader in the sidebar
    3. **Start Processing** - Click the "Start Processing" button
    4. **Download Results** - Download CSV and Excel files with extracted data
    
    ### ℹ️ Supported Formats
    - **Images**: PNG, JPG, JPEG, BMP, TIFF
    - **PDFs**: Multi-page PDF drawings (will auto-extract panel schedules)
    
    ### 🔧 Features
    - Extracts panel headers and circuit information
    - Generates multiple CSV formats and Excel output
    - Processes multiple files in batch
    - Download individual files or all as ZIP
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ⚡ by SKF")
