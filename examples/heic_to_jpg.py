#!/usr/bin/env python3
"""
Example script demonstrating HEIC to JPEG conversion
"""

import sys
from pathlib import Path

# Add src directory to path so we can import our photo_converter module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from photo_converter import PhotoConverter


def convert_heic_to_jpg(heic_file: str, output_dir: str = "converted"):
    """Convert a HEIC file to JPEG format"""
    
    converter = PhotoConverter()
    
    # Check if HEIC is supported
    if '.heic' not in converter.SUPPORTED_FORMATS:
        print("Error: HEIC support not available. Please install pyheif:")
        print("pip install pyheif")
        print("\nOn Fedora, you may also need:")
        print("sudo dnf install libheif-freeworld libheif-tools")
        return False
    
    input_path = Path(heic_file)
    output_path = Path(output_dir) / f"{input_path.stem}.jpg"
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting {input_path} to {output_path}...")
    
    # Convert with high quality JPEG settings
    success = converter.convert_image(
        input_path=input_path,
        output_path=output_path,
        quality=95  # High quality JPEG
    )
    
    if success:
        print("✅ Conversion successful!")
        print(f"Output saved to: {output_path}")
    else:
        print("❌ Conversion failed!")
    
    return success


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python heic_to_jpg.py <input_heic_file>")
        print("Example: python heic_to_jpg.py photo.heic")
        sys.exit(1)
    
    heic_file = sys.argv[1]
    convert_heic_to_jpg(heic_file)