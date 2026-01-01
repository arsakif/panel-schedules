"""
CSV writer for saving panel schedules incrementally.
Writes to TWO separate CSV files: panel headers and circuits.
"""

import csv
import os
import re
from typing import Dict, Any


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


class PanelHeadersCSVWriter:
    """Handles writing panel header information to CSV."""
    
    def __init__(self, output_path: str):
        """
        Initialize panel headers CSV writer.
        
        Args:
            output_path: Full path to the panel headers CSV file
        """
        self.output_path = output_path
        self.is_new_file = not os.path.exists(output_path)
        
    def write_panel_header(self, panel: Dict[str, Any], image_name: str):
        """
        Write panel header information to CSV.
        
        Args:
            panel: Panel dictionary with header info
            image_name: Name of the source image
        """
        mode = 'w' if self.is_new_file else 'a'
        
        with open(self.output_path, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header row only for new file
            if self.is_new_file:
                writer.writerow([
                    'Source Image',
                    'Panel Name',
                    'Panel Amperage of Lugs and Bus',
                    'Panel Amperage of Main Circuit Breaker or Main Fuse',
                    'Panel Voltages',
                    'Panel Phases',
                    'Panel Wire',
                    'Panel Pole(Circuit)#',
                    'Panel Short Circuit Rating (KAIC)',
                    'Panel Enclosure Type'
                ])
                self.is_new_file = False
            
            # Get panel header info
            header = panel.get('panel_header', {})
            
            writer.writerow([
                image_name,
                header.get('panel_name', ''),
                header.get('bus_amperage', ''),
                header.get('main_ocpd', ''),
                header.get('voltage', ''),
                header.get('phase', ''),
                header.get('wire', ''),
                header.get('poles', ''),
                header.get('kaic', ''),
                header.get('enclosure', '')
            ])


class PanelCircuitsCSVWriter:
    """Handles writing circuit information to CSV."""
    
    def __init__(self, output_path: str):
        """
        Initialize circuits CSV writer.
        
        Args:
            output_path: Full path to the circuits CSV file
        """
        self.output_path = output_path
        self.is_new_file = not os.path.exists(output_path)
        
    def write_circuits(self, panel: Dict[str, Any], image_name: str):
        """
        Write circuit information to CSV.
        
        Args:
            panel: Panel dictionary with circuits
            image_name: Name of the source image
        """
        mode = 'w' if self.is_new_file else 'a'
        
        with open(self.output_path, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header row only for new file
            if self.is_new_file:
                writer.writerow([
                    'Source Image',
                    'Load Description',
                    'OCP Size',
                    'Poles',
                    'Feeder',
                    'Circuit Number'
                ])
                self.is_new_file = False
            
            # Get panel info
            header = panel.get('panel_header', {})
            panel_name = header.get('panel_name', '')
            
            # Write each circuit
            circuits = panel.get('circuits', [])
            if circuits:
                for circuit in circuits:
                    writer.writerow([
                        image_name,
                        circuit.get('load_description', ''),
                        clean_ocp_size(circuit.get('ocp_size', '')),
                        circuit.get('poles', ''),
                        circuit.get('feeder', ''),
                        circuit.get('circuit_number', '')
                    ])


class CombinedCSVWriter:
    """Handles writing combined panel header and circuits to a single CSV."""
    
    def __init__(self, output_path: str):
        """
        Initialize combined CSV writer.
        
        Args:
            output_path: Full path to the combined CSV file
        """
        self.output_path = output_path
        self.is_first_panel = not os.path.exists(output_path)
        
    def write_panel(self, panel: Dict[str, Any], image_name: str):
        """
        Write panel header and circuits in combined format.
        
        Format:
        - Row 1: Concatenated panel header in first column
        - Row 2: Circuit column headers
        - Row 3+: Circuit data (each field in separate column)
        - 2 empty rows after each panel
        
        Args:
            panel: Panel dictionary with header and circuits
            image_name: Name of the source image
        """
        mode = 'w' if self.is_first_panel else 'a'
        
        with open(self.output_path, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Get panel header info
            header = panel.get('panel_header', {})
            
            # Build concatenated panel header text (shortened format)
            header_parts = []
            if image_name:
                header_parts.append(f"Source: {image_name}")
            if header.get('panel_name'):
                header_parts.append(f"Pnl: {header['panel_name']}")
            if header.get('bus_amperage'):
                header_parts.append(f"Bus/Lug: {header['bus_amperage']}")
            if header.get('main_ocpd'):
                # Extract just amperage value from main_ocpd (e.g., "60.00A MCB" -> "60A")
                main_ocpd = header['main_ocpd']
                # Extract numbers and 'A' only, remove decimals and suffixes like MCB, MB, MLO
                import re
                match = re.search(r'(\d+(?:\.\d+)?)\s*A', main_ocpd)
                if match:
                    amperage = float(match.group(1))
                    # Remove .00 decimals if present
                    if amperage == int(amperage):
                        main_ocpd = f"{int(amperage)}A"
                    else:
                        main_ocpd = f"{amperage}A"
                header_parts.append(f"Main: {main_ocpd}")
            if header.get('voltage'):
                header_parts.append(header['voltage'])
            if header.get('phase'):
                header_parts.append(header['phase'])
            if header.get('wire'):
                header_parts.append(header['wire'])
            if header.get('poles'):
                header_parts.append(f"Poles: {header['poles']}")
            if header.get('kaic'):
                header_parts.append(header['kaic'])
            if header.get('enclosure'):
                header_parts.append(header['enclosure'])
            
            panel_description = " | ".join(header_parts)
            panel_name = header.get('panel_name', '')
            
            # Write concatenated panel header in first column (with 3 columns before it)
            writer.writerow(['', '', '1', panel_description])
            
            # Write circuit column headers (with 3 columns before: empty, panel name header, empty)
            writer.writerow(['', 'Panel Name', '2', 'Load Description', 'Quantity', 'OCP', 'Poles', 'Feeder', 'Ckt#'])
            
            # Write each circuit
            circuits = panel.get('circuits', [])
            if circuits:
                for circuit in circuits:
                    writer.writerow([
                        '',  # Empty column
                        panel_name,  # Panel name for circuit rows
                        '',  # Empty column
                        circuit.get('load_description', ''),
                        '1',  # Quantity
                        clean_ocp_size(circuit.get('ocp_size', '')),
                        circuit.get('poles', ''),
                        circuit.get('feeder', ''),
                        circuit.get('circuit_number', '')
                    ])
            else:
                writer.writerow(['', panel_name, '', 'NO CIRCUITS FOUND'])
            
            # Add 2 empty rows between panels
            writer.writerow([])
            writer.writerow([])
            
            self.is_first_panel = False
