# Electrical Panel Schedule Extractor

Extract electrical panel schedule data from PDF drawings using Google Gemini AI and export to Excel.

## Features

- 🔍 Automatically detects panel schedules in electrical drawings
- 🤖 Uses Google Gemini Flash for intelligent data extraction
- 📊 Exports to formatted Excel files
- 📄 Processes multi-page PDFs
- ⚡ Handles both panelboards and switchboards

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API Key:**
The API key is already configured in `config.py`. Make sure not to commit this file to version control.

## Usage

Basic usage:
```bash
python main.py <path_to_pdf>
```

With custom output filename:
```bash
python main.py <path_to_pdf> output_filename.xlsx
```

### Example:
```bash
python main.py drawings/electrical_plan.pdf
python main.py drawings/electrical_plan.pdf custom_panels.xlsx
```

## Output Format

The Excel file contains:
- **Panel Description** (first row): Panel name, ratings, voltage, phase, wire, poles, KAIC, enclosure
- **Column Headers**:
  1. Load Description
  2. Overcurrent Protection Size (Fuse or CB Trip Size)
  3. Poles
  4. Feeder
  5. Circuit #
- **Circuit Data**: One row per circuit (left side first, then right side)
- **Spacing**: 4 empty rows between each panel

## Project Structure

```
panel-schedules/
├── main.py              # Main script
├── panel_extractor.py   # Gemini API integration
├── excel_writer.py      # Excel file generation
├── config.py            # Configuration (API key, settings)
├── requirements.txt     # Python dependencies
├── output/              # Generated Excel files (auto-created)
└── README.md           # This file
```

## What Gets Extracted

### Panel Header:
- Panel Name/Designation
- Main Rating (MLO/MCB)
- Voltage
- Phase
- Wire configuration
- Number of poles
- KAIC rating
- Enclosure type

### Circuit Information:
- Load Description
- Overcurrent Protection Size
- Number of Poles
- Feeder Size/Type (if available)
- Circuit Number (if available)

## Notes

- The tool uses Google Gemini 2.0 Flash for extraction
- PDF pages are converted to 300 DPI images for processing
- Output files are saved in the `output/` directory
- The tool automatically ignores non-panel tables in the drawings
