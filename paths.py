"""
Directory paths configuration for input and output files.
"""

import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Input directory for PDF files
INPUT_DIR = os.path.join(PROJECT_ROOT, "drawings")

# Output directory for Excel files
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Debug directory for saving extracted images
DEBUG_DIR = os.path.join(PROJECT_ROOT, "debug_images")

# Create directories if they don't exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DEBUG_DIR, exist_ok=True)


def get_input_path(filename: str) -> str:
    """
    Get full path for an input file.
    
    Args:
        filename: Name of the input file
        
    Returns:
        Full path to the input file
    """
    return os.path.join(INPUT_DIR, filename)


def get_output_path(filename: str) -> str:
    """
    Get full path for an output file.
    
    Args:
        filename: Name of the output file
        
    Returns:
        Full path to the output file
    """
    return os.path.join(OUTPUT_DIR, filename)


def get_debug_path(filename: str) -> str:
    """
    Get full path for a debug file.
    
    Args:
        filename: Name of the debug file
        
    Returns:
        Full path to the debug file
    """
    return os.path.join(DEBUG_DIR, filename)
