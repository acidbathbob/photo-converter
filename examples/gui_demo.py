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

def create_demo_images():
    """Create multiple demo images for testing"""
    demo_dir = Path(__file__).parent / "demo_images"
    demo_dir.mkdir(exist_ok=True)
    
    demo_files = []
    
    # Create first test image
    img1 = Image.new('RGB', (400, 300), color='lightblue')
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([50, 50, 150, 150], fill='red', outline='black')
    draw1.ellipse([200, 100, 350, 200], fill='green', outline='black')
    draw1.text((140, 250), "Photo Converter Test 1", fill='black')
    
    demo_file1 = demo_dir / "test_image_1.png"
    img1.save(demo_file1)
    demo_files.append(demo_file1)
    
    # Create second test image
    img2 = Image.new('RGB', (300, 400), color='lightyellow')
    draw2 = ImageDraw.Draw(img2)
    draw2.ellipse([50, 50, 250, 250], fill='blue', outline='black')
    draw2.rectangle([100, 300, 200, 350], fill='orange', outline='black')
    draw2.text((110, 370), "Test Image 2", fill='black')
    
    demo_file2 = demo_dir / "test_image_2.png"
    img2.save(demo_file2)
    demo_files.append(demo_file2)
    
    # Create third test image (different format)
    img3 = Image.new('RGB', (350, 250), color='lightgreen')
    draw3 = ImageDraw.Draw(img3)
    draw3.polygon([(50, 50), (150, 100), (100, 200), (25, 150)], fill='purple', outline='black')
    draw3.text((200, 120), "Test Image 3", fill='black')
    
    demo_file3 = demo_dir / "test_image_3.bmp"
    img3.save(demo_file3)
    demo_files.append(demo_file3)
    
    print(f"Created {len(demo_files)} demo images in: {demo_dir}")
    for f in demo_files:
        print(f"  - {f.name}")
    
    return demo_files

def launch_gui_with_demo():
    """Launch the GUI and provide instructions"""
    demo_files = create_demo_images()
    demo_dir = demo_files[0].parent
    
    print("\n" + "="*70)
    print("PHOTO CONVERTER GUI DEMO - Enhanced Version")
    print("="*70)
    print(f"Demo images created in: {demo_dir}")
    print("\n🔧 NEW FEATURES:")
    print("• Multiple file selection for batch processing")
    print("• Dependency installer (Tools menu)")
    print("• Improved output path handling")
    print("• Better progress tracking")
    
    print("\n📁 TESTING OPTIONS:")
    print("\n1. SINGLE FILE MODE:")
    print("   • Click 'Single File' and select one demo image")
    print("   • Choose output format and settings")
    print("   • Click 'Browse' for output file location")
    print("   • Convert!")
    
    print("\n2. MULTIPLE FILES MODE:")
    print("   • Click 'Multiple Files' and select several demo images")
    print("   • Batch Mode will be enabled automatically")
    print("   • Choose output folder and format")
    print("   • Convert all selected files!")
    
    print("\n3. FOLDER MODE:")
    print("   • Click 'Folder' and select the demo_images folder")
    print("   • All images in folder will be processed")
    print("   • Great for processing entire directories")
    
    print("\n🛠️ DEPENDENCY MANAGEMENT:")
    print("   • Tools → Check Dependencies (see what's installed)")
    print("   • Tools → Install Dependencies (auto-install missing packages)")
    
    print("\nStarting GUI now...")
    print("="*70)
    
    # Launch GUI
    try:
        from photo_converter_gui import main
        main()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Make sure you have tkinter and all dependencies installed")

if __name__ == "__main__":
    launch_gui_with_demo()