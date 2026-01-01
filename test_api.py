"""Quick test of Gemini API connection"""
from api_config import get_gemini_model
import api_config

print("Testing Gemini API connection...")
print(f"Model: {api_config.MODEL_NAME}")

try:
    client = get_gemini_model()
    response = client.models.generate_content(
        model=api_config.MODEL_NAME,
        contents=["Say 'hello' in one word"]
    )
    print(f"✓ API is working! Response: {response.text}")
except Exception as e:
    print(f"✗ API Error: {e}")
