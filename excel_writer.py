"""
Module for writing extracted panel schedule data to Excel files.
Format: Concatenated header in first column, circuits below, 2 empty rows between panels.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from typing import List, Dict, Any
import re


def clean_ocp_size(ocp_value: str) -> str:
    """
    Extract just the numeric value from OCP size.
    Examples: "20A" -> "20", "60.00A" -> "60", "30 Amps" -> "30"
    """
    if not ocp_value:
        return ""
    # Extract number from string
    match = re.search(r'(\d+(?:\.\d+)?)', ocp_value)
    if match:
        number = float(match.group(1))
        # Remove .00 decimals if present
        if number == int(number):
            return str(int(number))
        else:
            return str(number)
    return ocp_value  # Return original if no number found


class ExcelWriter:
    """Handles writing panel schedule data to Excel files."""
    
    def __init__(self, filename: str = "panel_schedules.xlsx"):
        """
        Initialize Excel writer.
        
        Args:
            filename: Output filename for the Excel file
        """
        self.filename = filename
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "Panel Schedules"
        self.current_row = 1
    
    def write_panel(self, panel: Dict[str, Any]) -> None:
        """
        Write a complete panel to Excel:
        - Row 1: Concatenated panel header info in first column
        - Following rows: Circuit data (each field in its own column)
        - 2 empty rows after each panel
        
        Args:
            panel: Dictionary containing panel header and circuits
        """
        panel_header = panel.get("panel_header", {})
        circuits = panel.get("circuits", [])
        
        # Build concatenated panel header text
        header_parts = []
        if panel_header.get("panel_name"):
            header_parts.append(f"Panel Name: {panel_header['panel_name']}")
        if panel_header.get("bus_amperage"):
            header_parts.append(f"Bus Amperage: {panel_header['bus_amperage']}")
        if panel_header.get("main_ocpd"):
            header_parts.append(f"Main OCPD: {panel_header['main_ocpd']}")
        if panel_header.get("voltage"):
            header_parts.append(f"Voltage: {panel_header['voltage']}")
        if panel_header.get("phase"):
            header_parts.append(f"Phase: {panel_header['phase']}")
        if panel_header.get("wire"):
            header_parts.append(f"Wire: {panel_header['wire']}")
        if panel_header.get("poles"):
            header_parts.append(f"Poles: {panel_header['poles']}")
        if panel_header.get("kaic"):
            header_parts.append(f"KAIC: {panel_header['kaic']}")
        if panel_header.get("enclosure"):
            header_parts.append(f"Enclosure: {panel_header['enclosure']}")
        
        panel_description = " | ".join(header_parts)
        
        # Write concatenated panel header in first column, first row
        cell = self.sheet.cell(row=self.current_row, column=1, value=panel_description)
        cell.font = Font(bold=True, size=11)
        cell.alignment = Alignment(wrap_text=True)
        self.current_row += 1
        
        # Write circuit headers
        circuit_headers = ["Circuit Number", "Load Description", "OCP Size", "Poles", "Feeder"]
        for col_idx, header in enumerate(circuit_headers, start=1):
            cell = self.sheet.cell(row=self.current_row, column=col_idx, value=header)
            cell.font = Font(bold=True)
        self.current_row += 1
        
        # Write each circuit
        if circuits:
            for circuit in circuits:
                self.sheet.cell(row=self.current_row, column=1, value=circuit.get("circuit_number", ""))
                self.sheet.cell(row=self.current_row, column=2, value=circuit.get("load_description", ""))
                self.sheet.cell(row=self.current_row, column=3, value=clean_ocp_size(circuit.get("ocp_size", "")))
                self.sheet.cell(row=self.current_row, column=4, value=circuit.get("poles", ""))
                self.sheet.cell(row=self.current_row, column=5, value=circuit.get("feeder", ""))
                self.current_row += 1
        else:
            # No circuits found
            self.sheet.cell(row=self.current_row, column=1, value="NO CIRCUITS FOUND")
            self.current_row += 1
        
        # Add 2 empty rows between panels
        self.current_row += 2
        """
        Write a complete panel (header + circuits) to Excel.
        
        Args:
            panel: Dictionary containing panel header and circuits
        """
        # Write panel header
        panel_header = panel.get("panel_header", {})
        # Add 2 empty rows between panels
        self.current_row += 2
    
    def write_all_panels(self, panels: List[Dict[str, Any]]) -> None:
        """
        Write all panels to the Excel file.
        
        Args:
            panels: List of panel dictionaries
        """
        for panel in panels:
            self.write_panel(panel)
    
    def adjust_column_widths(self) -> None:
        """Auto-adjust column widths for better readability."""
        column_widths = {
            1: 15,  # Circuit Number
            2: 50,  # Load Description
            3: 15,  # OCP Size
            4: 10,  # Poles
            5: 40   # Feeder
        }
        
        for col_idx, width in column_widths.items():
            column_letter = self.sheet.cell(row=1, column=col_idx).column_letter
            self.sheet.column_dimensions[column_letter].width = width
    
    def save(self) -> None:
        """Save the Excel workbook to file."""
        self.adjust_column_widths()
        self.workbook.save(self.filename)
        print(f"Excel file saved: {self.filename}")

