"""
CSV writer for saving panel schedules incrementally.
"""

import csv
import os
from typing import Dict, Any


class CSVWriter:
    """Handles writing panel data to CSV files."""
    
    def __init__(self, output_path: str):
        """
        Initialize CSV writer.
        
        Args:
            output_path: Full path to the CSV file
        """
        self.output_path = output_path
        self.is_new_file = not os.path.exists(output_path)
        
    def write_panel(self, panel: Dict[str, Any], image_name: str):
        """
        Write a single panel to CSV file.
        
        Args:
            panel: Panel dictionary with header and circuits
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
                    'Main Rating',
                    'Voltage',
                    'Phase',
                    'Wire',
                    'Poles',
                    'KAIC',
                    'Enclosure',
                    'Circuit Number',
                    'Load Description',
                    'OCP Size',
                    'Circuit Poles',
                    'Feeder'
                ])
                self.is_new_file = False
            
            # Get panel header info
            header = panel.get('panel_header', {})
            panel_name = header.get('panel_name', '')
            main_rating = header.get('main_rating', '')
            voltage = header.get('voltage', '')
            phase = header.get('phase', '')
            wire = header.get('wire', '')
            poles = header.get('poles', '')
            kaic = header.get('kaic', '')
            enclosure = header.get('enclosure', '')
            
            # Write each circuit
            circuits = panel.get('circuits', [])
            if circuits:
                for circuit in circuits:
                    writer.writerow([
                        image_name,
                        panel_name,
                        main_rating,
                        voltage,
                        phase,
                        wire,
                        poles,
                        kaic,
                        enclosure,
                        circuit.get('circuit_number', ''),
                        circuit.get('load_description', ''),
                        circuit.get('ocp_size', ''),
                        circuit.get('poles', ''),
                        circuit.get('feeder', '')
                    ])
            else:
                # Write panel header even if no circuits
                writer.writerow([
                    image_name,
                    panel_name,
                    main_rating,
                    voltage,
                    phase,
                    wire,
                    poles,
                    kaic,
                    enclosure,
                    '',  # circuit_number
                    'NO CIRCUITS FOUND',
                    '',  # ocp_size
                    '',  # circuit_poles
                    ''   # feeder
                ])
