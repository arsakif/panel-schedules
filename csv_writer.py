"""
CSV writer for saving panel schedules incrementally.
Writes to TWO separate CSV files: panel headers and circuits.
"""

import csv
import os
from typing import Dict, Any


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
                    'Panel Name',
                    'Circuit Number',
                    'Load Description',
                    'OCP Size',
                    'Poles',
                    'Feeder'
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
                        panel_name,
                        circuit.get('circuit_number', ''),
                        circuit.get('load_description', ''),
                        circuit.get('ocp_size', ''),
                        circuit.get('poles', ''),
                        circuit.get('feeder', '')
                    ])

