#!/usr/bin/env python3
"""
Demo script showing how to use the Photo Converter GUI
This script creates a simple test image and demonstrates the GUI functionality
"""

import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def create_demo_image():
    """Create a demo image for testing"""
    demo_dir = Path(__file__).parent / "demo_images"
    demo_dir.mkdir(exist_ok=True)
    
    # Create a simple test image
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes
    draw.rectangle([50, 50, 150, 150], fill='red', outline='black')
    draw.ellipse([200, 100, 350, 200], fill='green', outline='black')
    draw.text((160, 250), "Photo Converter Test", fill='black')
    
    # Save as PNG
    demo_file = demo_dir / "test_image.png"
    img.save(demo_file)
    
    print(f"Created demo image: {demo_file}")
    return demo_file

def launch_gui_with_demo():
    """Launch the GUI and provide instructions"""
    demo_file = create_demo_image()
    
    print("\n" + "="*60)
    print("PHOTO CONVERTER GUI DEMO")
    print("="*60)
    print(f"Demo image created at: {demo_file}")
    print("\nTo test the GUI:")
    print("1. Click 'Browse File' and select the demo image")
    print("2. Choose an output format (e.g., jpg, webp)")
    print("3. Adjust quality and resize settings if desired")
    print("4. Click 'Browse' for output and choose a destination")
    print("5. Click 'Convert' to process the image")
    print("\nFor batch processing:")
    print("1. Click 'Browse Folder' and select the demo_images folder")
    print("2. Enable 'Batch Mode' checkbox")
    print("3. Select output folder and target format")
    print("4. Click 'Convert' to process all images")
    print("\nStarting GUI now...")
    print("="*60)
    
    # Launch GUI
    try:
        from photo_converter_gui import main
        main()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Make sure you have tkinter and all dependencies installed")

if __name__ == "__main__":
    launch_gui_with_demo()