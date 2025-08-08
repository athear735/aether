"""
AETHER - Streamlit Cloud Entry Point
This file serves as the main entry point for Streamlit Cloud deployment
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the actual app
from web.app import *
