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
            List of panel dictionaries with extracted data
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
            
            # Parse JSON response
            data = json.loads(response_text)
            panels = data.get("panels", [])
            
            if panels:
                panel_names = [p.get("panel_header", {}).get("panel_name", "Unknown") for p in panels]
                print(f"  ✓ Extracted {len(panels)} panel(s): {', '.join(panel_names)}")
            else:
                print(f"  - No panels found in this image")
            
            return panels
            
        except json.JSONDecodeError as e:
            print(f"  ✗ Error parsing JSON response: {e}")
            if 'response_text' in locals():
                print(f"    First 200 chars: {response_text[:200]}")
            return []
        except Exception as e:
            print(f"  ✗ Error extracting data: {e}")
            return []
