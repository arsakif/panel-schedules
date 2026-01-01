"""
Module for writing extracted panel schedule data to Excel files.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from typing import List, Dict, Any


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
    
    def write_panel_header(self, panel_header: Dict[str, str]) -> None:
        """
        Write panel header information to Excel.
        
        Args:
            panel_header: Dictionary containing panel header information
        """
        # Format panel description
        description_parts = []
        if panel_header.get("panel_name"):
            description_parts.append(f"Panel {panel_header['panel_name']}")
        if panel_header.get("main_rating"):
            description_parts.append(panel_header['main_rating'])
        if panel_header.get("voltage"):
            description_parts.append(panel_header['voltage'])
        if panel_header.get("phase"):
            description_parts.append(panel_header['phase'])
        if panel_header.get("wire"):
            description_parts.append(panel_header['wire'])
        if panel_header.get("poles"):
            description_parts.append(f"{panel_header['poles']} poles")
        if panel_header.get("kaic"):
            description_parts.append(panel_header['kaic'])
        if panel_header.get("enclosure"):
            description_parts.append(panel_header['enclosure'])
        
        panel_description = ", ".join(description_parts)
        
        # Write panel description
        cell = self.sheet.cell(row=self.current_row, column=1, value=panel_description)
        cell.font = Font(bold=True, size=12)
        self.current_row += 1
    
    def write_column_headers(self) -> None:
        """Write the column headers for circuit data."""
        headers = [
            "Load Description",
            "Overcurrent Protection Size (Fuse or CB Trip Size)",
            "Poles",
            "Feeder",
            "Circuit #"
        ]
        
        for col_idx, header in enumerate(headers, start=1):
            cell = self.sheet.cell(row=self.current_row, column=col_idx, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(wrap_text=True)
        
        self.current_row += 1
    
    def write_circuit(self, circuit: Dict[str, str]) -> None:
        """
        Write a single circuit row to Excel.
        
        Args:
            circuit: Dictionary containing circuit information
        """
        values = [
            circuit.get("load_description", ""),
            circuit.get("ocp_size", ""),
            circuit.get("poles", ""),
            circuit.get("feeder", ""),
            circuit.get("circuit_number", "")
        ]
        
        for col_idx, value in enumerate(values, start=1):
            self.sheet.cell(row=self.current_row, column=col_idx, value=value)
        
        self.current_row += 1
    
    def add_panel_spacing(self) -> None:
        """Add 4 empty rows between panels."""
        self.current_row += 4
    
    def write_panel(self, panel: Dict[str, Any]) -> None:
        """
        Write a complete panel (header + circuits) to Excel.
        
        Args:
            panel: Dictionary containing panel header and circuits
        """
        # Write panel header
        panel_header = panel.get("panel_header", {})
        self.write_panel_header(panel_header)
        
        # Write column headers
        self.write_column_headers()
        
        # Write circuits
        circuits = panel.get("circuits", [])
        for circuit in circuits:
            self.write_circuit(circuit)
    
    def write_all_panels(self, panels: List[Dict[str, Any]]) -> None:
        """
        Write all panels to the Excel file.
        
        Args:
            panels: List of panel dictionaries
        """
        for idx, panel in enumerate(panels):
            self.write_panel(panel)
            
            # Add spacing between panels (except after the last one)
            if idx < len(panels) - 1:
                self.add_panel_spacing()
    
    def adjust_column_widths(self) -> None:
        """Auto-adjust column widths for better readability."""
        column_widths = {
            1: 40,  # Load Description
            2: 30,  # Overcurrent Protection Size
            3: 10,  # Poles
            4: 30,  # Feeder
            5: 12   # Circuit #
        }
        
        for col_idx, width in column_widths.items():
            column_letter = self.sheet.cell(row=1, column=col_idx).column_letter
            self.sheet.column_dimensions[column_letter].width = width
    
    def save(self) -> None:
        """Save the Excel workbook to file."""
        self.adjust_column_widths()
        self.workbook.save(self.filename)
        print(f"Excel file saved: {self.filename}")
