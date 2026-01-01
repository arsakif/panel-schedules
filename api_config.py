"""
Google Gemini API configuration settings.
"""

from google import genai
from config import GOOGLE_API_KEY

# Gemini model to use
MODEL_NAME = "gemini-3-pro-preview"

# Generation configuration
GENERATION_CONFIG = {
    "temperature": 0.1,  # Low temperature for more consistent/factual outputs
    "max_output_tokens": 65536,  # Increased to handle large panel schedules (3x+ increase)
}


def configure_gemini_api():
    """Configure the Gemini API with the API key."""
    client = genai.Client(api_key=GOOGLE_API_KEY)
    return client


def get_gemini_model():
    """
    Get configured Gemini client instance.
    
    Returns:
        Genai Client instance
    """
    return configure_gemini_api()
