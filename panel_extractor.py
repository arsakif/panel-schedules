"""
Module for extracting electrical panel schedule data from PDF images using Google Gemini.
"""

from PIL import Image
import json
from typing import List, Dict, Any
from api_config import get_gemini_model
from prompts import PANEL_EXTRACTION_PROMPT
from panel_detection_prompt import PANEL_DETECTION_PROMPT
import api_config
from paths import get_debug_path
from opencv_detector import detect_panels_with_opencv


class PanelExtractor:
    """Handles extraction of panel schedule data using Google Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini API client."""
        self.client = get_gemini_model()
    
    def detect_panels_in_image(self, image: Image.Image, page_num: int) -> List[Dict[str, Any]]:
        """
        Detect panel locations in an image and save cropped panels.
        
        Args:
            image: PIL Image object of the PDF page
            page_num: Page number for naming saved files
            
        Returns:
            List of dictionaries with panel_name and bbox coordinates
        """
        try:
            response = self.client.models.generate_content(
                model=api_config.MODEL_NAME,
                contents=[PANEL_DETECTION_PROMPT, image]
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
                print(f"  Detected {len(panels)} panel(s) with bounding boxes")
                
                # Crop and save each panel
                img_width, img_height = image.size
                
                for idx, panel_info in enumerate(panels):
                    panel_name = panel_info.get("panel_name", f"unknown_{idx}")
                    bbox = panel_info.get("bbox", {})
                    
                    # Convert percentage coordinates to pixels
                    x1 = int(bbox.get("x1", 0) * img_width / 100)
                    y1 = int(bbox.get("y1", 0) * img_height / 100)
                    x2 = int(bbox.get("x2", 100) * img_width / 100)
                    y2 = int(bbox.get("y2", 100) * img_height / 100)
                    
                    # Crop the panel
                    cropped_panel = image.crop((x1, y1, x2, y2))
                    
                    # Save cropped panel
                    # Clean panel name for filename
                    safe_name = panel_name.replace("/", "-").replace(":", "-").replace(" ", "_")
                    filename = f"page_{page_num:02d}_panel_{idx+1:02d}_{safe_name}.png"
                    save_path = get_debug_path(filename)
                    cropped_panel.save(save_path)
                    
                    print(f"    Saved: {filename}")
            
            return panels
            
        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON response: {e}")
            if 'response_text' in locals():
                print(f"  Response: {response_text[:200]}")
            return []
        except Exception as e:
            print(f"  Error detecting panels: {e}")
            return []
    
    def extract_from_image(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Extract panel schedule data from a single image.
        
        Args:
            image: PIL Image object of the PDF page
            
        Returns:
            List of panel dictionaries with extracted data
        """
        try:
            response = self.client.models.generate_content(
                model=api_config.MODEL_NAME,
                contents=[PANEL_EXTRACTION_PROMPT, image]
            )
            
            # Check if response is blocked or empty
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
            
            # Check for incomplete JSON (common issue with large responses)
            if not response_text.endswith('}') and not response_text.endswith(']'):
                print(f"  Warning: Response appears incomplete, attempting to fix...")
                # Try to close the JSON structure
                response_text = response_text.rstrip(',') + ']}}'
            
            # Parse JSON response
            data = json.loads(response_text)
            panels = data.get("panels", [])
            
            # Print panel names for verification
            if panels:
                panel_names = [p.get("panel_header", {}).get("panel_name", "Unknown") for p in panels]
                print(f"  Extracted panels: {', '.join(panel_names)}")
            
            return panels
            
        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON response: {e}")
            print(f"  Response length: {len(response_text) if 'response_text' in locals() else 'unknown'}")
            if 'response_text' in locals():
                print(f"  First 200 chars: {response_text[:200]}")
                print(f"  Last 200 chars: {response_text[-200:]}")
            return []
        except Exception as e:
            print(f"  Error extracting data from image: {e}")
            return []
    
    def extract_from_pdf_page_images(self, images: List[Image.Image], use_opencv: bool = True) -> List[Dict[str, Any]]:
        """
        Extract panel schedule data from multiple PDF page images.
        
        Args:
            images: List of PIL Image objects
            use_opencv: If True, use OpenCV for detection; if False, use Gemini
            
        Returns:
            List of all panels found across all pages
        """
        all_panels = []
        
        print("\n" + "="*60)
        if use_opencv:
            print("PHASE 1: DETECTING PANELS WITH OPENCV (CONTOUR DETECTION)")
        else:
            print("PHASE 1: DETECTING PANELS WITH GEMINI AI")
        print("="*60)
        
        for idx, image in enumerate(images):
            page_num = idx + 1
            print(f"\nProcessing page {page_num} of {len(images)}...")
            
            if use_opencv:
                # Use OpenCV-based detection
                detected_panels = detect_panels_with_opencv(image, page_num)
                if detected_panels:
                    print(f"  ✓ Successfully detected and saved {len(detected_panels)} panel(s)")
                else:
                    print(f"  - No panels detected on this page")
            else:
                # Use Gemini-based detection
                detected_panels = self.detect_panels_in_image(image, page_num)
                if detected_panels:
                    print(f"  ✓ Successfully detected and saved {len(detected_panels)} panel(s)")
                else:
                    print(f"  - No panels detected on this page")
        
        print("\n" + "="*60)
        print("PANEL DETECTION COMPLETE")
        print("="*60)
        print("\nPlease check the 'debug_images/' folder to verify cropped panels.")
        if use_opencv:
            print("Cropped panels are saved as: page_XX_opencv_panel_XX.png")
        else:
            print("\nPlease check the 'debug_images/' folder to verify cropped panels.")
        print("Cropped panels are saved as: page_XX_panel_XX_PanelName.png")
        print("\nSkipping data extraction until you verify the images are correct.")
        print("="*60 + "\n")
        
        return all_panels
