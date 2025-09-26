#!/usr/bin/env python3
"""
Launcher script for Photo Converter GUI
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Import and run the GUI
try:
    from photo_converter_gui import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing GUI: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error running GUI: {e}")
    sys.exit(1)