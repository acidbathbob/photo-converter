#!/usr/bin/env python3
"""
Photo Converter - A simple tool for converting images between different formats
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

import click
from PIL import Image
from tqdm import tqdm

# Import pillow-heif for HEIC support (more compatible than pyheif)
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    # Fallback to pyheif if available
    try:
        import pyheif
        HEIC_SUPPORTED = True
        USE_PYHEIF = True
    except ImportError:
        HEIC_SUPPORTED = False
        USE_PYHEIF = False
else:
    USE_PYHEIF = False


class PhotoConverter:
    """Main photo conversion class"""
    
    SUPPORTED_FORMATS = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.webp': 'WEBP',
        '.gif': 'GIF',
        '.bmp': 'BMP',
        '.tiff': 'TIFF',
        '.tif': 'TIFF'
    }
    
    def __init__(self):
        self.converted_count = 0
        self.failed_count = 0
        
        # Add HEIC support if available
        if HEIC_SUPPORTED:
            self.SUPPORTED_FORMATS.update({
                '.heic': 'HEIF',
                '.heif': 'HEIF'
            })
    
    def convert_image(self, input_path: Path, output_path: Path, 
                     quality: Optional[int] = None, resize: Optional[tuple] = None) -> bool:
        """Convert a single image file"""
        try:
            # Handle HEIC files - pillow-heif allows direct Image.open() usage
            if input_path.suffix.lower() in ['.heic', '.heif'] and HEIC_SUPPORTED and USE_PYHEIF:
                # Fallback to pyheif method if pillow-heif not available
                import pyheif
                heif_file = pyheif.read(str(input_path))
                img = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
            else:
                # For all formats including HEIC (when using pillow-heif)
                img = Image.open(input_path)
            
            with img:
                # Convert to RGB if necessary (especially important for HEIC files)
                if img.mode not in ('RGB', 'RGBA', 'L', 'LA'):
                    img = img.convert('RGB')
                
                # Handle transparency for formats that don't support it
                if output_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA'):
                    # Create white background for transparent images when converting to JPEG
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                
                # Resize if specified
                if resize:
                    img = img.resize(resize, Image.Resampling.LANCZOS)
                
                # Save with appropriate options
                save_kwargs = {}
                if output_path.suffix.lower() in ['.jpg', '.jpeg'] and quality:
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif output_path.suffix.lower() == '.webp' and quality:
                    save_kwargs['quality'] = quality
                
                img.save(output_path, **save_kwargs)
                self.converted_count += 1
                return True
                
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            self.failed_count += 1
            return False
    
    def get_image_files(self, directory: Path) -> List[Path]:
        """Get all image files from a directory"""
        image_files = []
        for ext in self.SUPPORTED_FORMATS.keys():
            image_files.extend(directory.glob(f"*{ext}"))
            image_files.extend(directory.glob(f"*{ext.upper()}"))
        return sorted(image_files)


@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.argument('output_path', type=click.Path(path_type=Path), required=False)
@click.option('--batch', is_flag=True, help='Process all images in the input directory')
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output directory for batch processing')
@click.option('--format', '-f', type=str, help='Target format for batch conversion (jpg, png, webp, etc.)')
@click.option('--quality', '-q', type=int, help='Quality for lossy formats (1-100)')
@click.option('--resize', type=str, help='Resize images (format: WIDTHxHEIGHT, e.g., 800x600)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(input_path: Path, output_path: Path, batch: bool, output: Path, 
         format: str, quality: int, resize: str, verbose: bool):
    """Convert images between different formats"""
    
    converter = PhotoConverter()
    
    # Display supported formats
    if verbose:
        formats_list = list(converter.SUPPORTED_FORMATS.keys())
        click.echo(f"Supported formats: {', '.join(formats_list)}")
        if not HEIC_SUPPORTED:
            click.echo("Note: HEIC support not available. Install pillow-heif for HEIC support.")
        elif USE_PYHEIF:
            click.echo("Note: Using pyheif for HEIC support. Consider upgrading to pillow-heif for better compatibility.")
    
    # Parse resize parameter
    resize_dims = None
    if resize:
        try:
            width, height = map(int, resize.split('x'))
            resize_dims = (width, height)
        except ValueError:
            click.echo("Error: Invalid resize format. Use WIDTHxHEIGHT (e.g., 800x600)")
            return
    
    # Validate quality parameter
    if quality and not (1 <= quality <= 100):
        click.echo("Error: Quality must be between 1 and 100")
        return
    
    if batch:
        # Batch processing
        if not input_path.is_dir():
            click.echo("Error: Input path must be a directory for batch processing")
            return
        
        if not output:
            output = input_path / "converted"
        
        if not format:
            click.echo("Error: Format must be specified for batch processing")
            return
        
        # Ensure format has a dot prefix
        if not format.startswith('.'):
            format = '.' + format
        
        if format.lower() not in converter.SUPPORTED_FORMATS:
            click.echo(f"Error: Unsupported format '{format}'. Supported: {list(converter.SUPPORTED_FORMATS.keys())}")
            return
        
        # Create output directory
        output.mkdir(parents=True, exist_ok=True)
        
        # Get all image files
        image_files = converter.get_image_files(input_path)
        
        if not image_files:
            click.echo("No image files found in the input directory")
            return
        
        click.echo(f"Found {len(image_files)} image files to convert")
        
        # Process files with progress bar
        with tqdm(image_files, desc="Converting") as pbar:
            for image_file in pbar:
                output_file = output / f"{image_file.stem}{format.lower()}"
                if verbose:
                    pbar.write(f"Converting: {image_file} -> {output_file}")
                converter.convert_image(image_file, output_file, quality, resize_dims)
        
        click.echo(f"\nConversion complete!")
        click.echo(f"Successfully converted: {converter.converted_count} files")
        if converter.failed_count > 0:
            click.echo(f"Failed conversions: {converter.failed_count} files")
    
    else:
        # Single file conversion
        if not output_path:
            click.echo("Error: Output path is required for single file conversion")
            return
        
        if not input_path.is_file():
            click.echo("Error: Input path must be a file")
            return
        
        # Check if input format is supported
        input_ext = input_path.suffix.lower()
        if input_ext not in converter.SUPPORTED_FORMATS:
            click.echo(f"Error: Unsupported input format '{input_ext}'. Supported: {list(converter.SUPPORTED_FORMATS.keys())}")
            return
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            click.echo(f"Converting: {input_path} -> {output_path}")
        
        success = converter.convert_image(input_path, output_path, quality, resize_dims)
        
        if success:
            click.echo("Conversion successful!")
        else:
            click.echo("Conversion failed!")
            sys.exit(1)


if __name__ == '__main__':
    main()