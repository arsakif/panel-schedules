"""
Module for extracting electrical panel schedule data from images using Google Gemini.
"""

from PIL import Image
import json
from typing import List, Dict, Any
from api_config import get_gemini_model
from prompts import PANEL_EXTRACTION_PROMPT
import api_config


class PanelExtractor:
    """Handles extraction of panel schedule data using Google Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini API client."""
        self.client = get_gemini_model()
    
    def extract_from_image(self, image: Image.Image, image_name: str) -> List[Dict[str, Any]]:
        """
        Extract panel schedule data from a single image.
        
        Args:
            image: PIL Image object
            image_name: Name of the image file for logging
            
        Returns:
            List containing one panel dictionary with extracted data
        """
        try:
            print(f"\nProcessing: {image_name}")
            
            response = self.client.models.generate_content(
                model=api_config.MODEL_NAME,
                contents=[PANEL_EXTRACTION_PROMPT, image]
            )
            
            if not response.text:
                print(f"  Warning: Empty response from Gemini API")
                return []
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse the two separate JSON structures
            # Expected format:
            # PANEL_HEADER:
            # {json}
            # CIRCUITS:
            # [{json}]
            
            panel_header = {}
            circuits = []
            
            if "PANEL_HEADER:" in response_text and "CIRCUITS:" in response_text:
                # Split at CIRCUITS: marker
                parts = response_text.split("CIRCUITS:")
                
                # Extract panel header JSON (after PANEL_HEADER:)
                header_part = parts[0].replace("PANEL_HEADER:", "").strip()
                panel_header = json.loads(header_part)
                
                # Extract circuits JSON array
                circuits_part = parts[1].strip()
                circuits = json.loads(circuits_part)
            else:
                print(f"  ✗ Response format incorrect - missing PANEL_HEADER: or CIRCUITS: labels")
                print(f"    First 300 chars: {response_text[:300]}")
                return []
            
            # Construct panel dictionary
            panel = {
                "panel_header": panel_header,
                "circuits": circuits if isinstance(circuits, list) else []
            }
            
            panel_name = panel_header.get("panel_name", "Unknown")
            circuit_count = len(circuits) if isinstance(circuits, list) else 0
            print(f"  ✓ Extracted panel: {panel_name} ({circuit_count} circuits)")
            
            return [panel]
            
        except json.JSONDecodeError as e:
            print(f"  ✗ Error parsing JSON response: {e}")
            if 'response_text' in locals():
                print(f"    First 300 chars: {response_text[:300]}")
            return []
        except Exception as e:
            print(f"  ✗ Error extracting data: {e}")
            return []
