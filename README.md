# Panel Schedule Extractor

Extracts electrical panel schedule data from images using Google Gemini 3 Flash Preview API.

## Setup

1. Install Python 3.12+
2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Google API key to `config.py`:
   ```python
   GOOGLE_API_KEY = "your-api-key-here"
   ```

## Usage

1. Place your panel schedule images in the `panel_schedule_images/` folder
   - Supported formats: PNG, JPG, JPEG, BMP, TIFF
   - Images should contain clear views of electrical panel schedules

2. Run the extractor:
   ```bash
   python main.py
   ```

3. Find the extracted data in `output/panel_schedules.xlsx`

## Output Format

The Excel file contains:
- Panel header information (name, voltage, phase, ratings, etc.)
- Complete circuit listings from both left and right sides
- Proper formatting with headers and spacing

## Project Structure

```
panel-schedules/
├── panel_schedule_images/   # Input: Place your images here
├── output/                   # Output: Excel files
├── main.py                   # Main execution script
├── panel_extractor.py        # Gemini API integration
├── excel_writer.py           # Excel generation
├── prompts.py                # AI extraction prompts
├── api_config.py             # Gemini configuration
├── paths.py                  # Path management
└── requirements.txt          # Dependencies
```
