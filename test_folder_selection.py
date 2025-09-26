#!/usr/bin/env python3
"""
Test script to simulate folder selection and show what the GUI sees
"""

import sys
from pathlib import Path
sys.path.insert(0, 'src')
from photo_converter import PhotoConverter

def test_folder_analysis(folder_path):
    """Test what the GUI sees when analyzing a folder"""
    print(f"🔍 Analyzing folder: {folder_path}")
    print("=" * 60)
    
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print("❌ Folder does not exist!")
        return
    
    if not folder_path.is_dir():
        print("❌ Path is not a directory!")
        return
    
    print("✅ Folder exists and is accessible")
    
    # Create converter
    converter = PhotoConverter()
    print(f"\n📋 Supported formats: {list(converter.SUPPORTED_FORMATS.keys())}")
    
    # Get supported image files
    image_files = converter.get_image_files(folder_path)
    print(f"\n✅ Found {len(image_files)} supported image files:")
    
    if image_files:
        # Show file breakdown
        file_types = {}
        for f in image_files:
            ext = f.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        for ext, count in sorted(file_types.items()):
            print(f"   • {count} {ext[1:].upper()} files")
            
        print("\n📁 Files found:")
        for i, f in enumerate(image_files[:10], 1):
            print(f"   {i:2d}. {f.name}")
        if len(image_files) > 10:
            print(f"   ... and {len(image_files) - 10} more files")
    
    # Check for HEIC files specifically
    heic_files = list(folder_path.glob("*.heic")) + list(folder_path.glob("*.HEIC")) + \
                list(folder_path.glob("*.heif")) + list(folder_path.glob("*.HEIF"))
    
    if heic_files:
        print(f"\n📱 Found {len(heic_files)} HEIC files:")
        for i, f in enumerate(heic_files[:5], 1):
            print(f"   {i:2d}. {f.name}")
        if len(heic_files) > 5:
            print(f"   ... and {len(heic_files) - 5} more HEIC files")
            
        if not converter.SUPPORTED_FORMATS.get('.heic'):
            print("⚠️  HEIC files found but not supported!")
            print("   Install HEIC support: pip install pyheif")
            print("   (May also need: sudo dnf install libheif-devel)")
        else:
            print("✅ HEIC files will be processed!")
    
    # Show all files in directory for reference
    all_files = [f for f in folder_path.iterdir() if f.is_file()]
    print(f"\n📊 Total files in directory: {len(all_files)}")
    
    if not image_files and not heic_files:
        print("\n❌ No image files found that can be processed!")
        print("   Double-check the folder contains image files.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_folder = sys.argv[1]
    else:
        test_folder = "/home/bob/Pictures/From-iPhone"
    
    test_folder_analysis(test_folder)