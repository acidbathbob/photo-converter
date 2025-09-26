# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based photo conversion tool that supports converting images between various formats including JPEG, PNG, WebP, GIF, BMP, TIFF, and HEIC/HEIF. The project uses a single-module architecture with the core functionality in `src/photo_converter.py`.

## Architecture

### Core Components
- **PhotoConverter Class**: Main conversion engine that handles format detection, image processing, and batch operations
- **CLI Interface**: Click-based command-line interface supporting both single file and batch conversion
- **HEIC Support**: Optional HEIC/HEIF support via pyheif library with graceful fallback

### Key Design Patterns
- **Modular Format Support**: Format mappings stored in `SUPPORTED_FORMATS` dictionary for easy extension
- **Error Resilience**: Each conversion is wrapped in try-catch with counters for success/failure tracking  
- **Progress Tracking**: Uses tqdm for batch operation progress bars
- **Transparent Image Handling**: Automatic background insertion for formats that don't support transparency

## Development Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install HEIC Support (Fedora)
```bash
sudo dnf install libheif-freeworld libheif-tools
pip install pyheif
```

### Run Single File Conversion
```bash
python src/photo_converter.py input.jpg output.png
```

### Run Batch Conversion
```bash
python src/photo_converter.py --batch input_folder/ --output output_folder/ --format png
```

### Run with Quality/Resize Options
```bash
python src/photo_converter.py input.jpg output.jpg --quality 85 --resize 800x600
```

### Run Example Script
```bash
python examples/heic_to_jpg.py photo.heic
```

### Testing
The README mentions running tests with `python -m pytest tests/` but no test directory currently exists.

## Important Implementation Details

### Format Handling
- HEIC files require special handling via pyheif library before PIL processing
- JPEG conversion from transparent images automatically adds white background
- Quality settings only apply to lossy formats (JPEG, WebP)
- Case-insensitive file extension matching

### Batch Processing Logic
- Automatically creates output directory if not specified
- Scans input directory for all supported image formats
- Progress tracking with tqdm
- Maintains separate counters for successful/failed conversions

### Error Handling
- Graceful degradation when HEIC support unavailable
- Individual file errors don't stop batch processing
- Detailed error messages for common validation failures

## Project Structure
```
src/photo_converter.py    # Main conversion logic and CLI
examples/heic_to_jpg.py   # HEIC conversion example
requirements.txt          # Python dependencies
```

## Adding New Features

### Adding Format Support
1. Add format mapping to `SUPPORTED_FORMATS` dictionary
2. Handle any special preprocessing in `convert_image()` method
3. Add format-specific save options if needed

### Extending CLI Options
- New click options can be added to the `main()` function decorator
- Parameter validation should be added before processing begins
- Progress output should use click.echo() for consistency

### Example Usage Patterns
- Check `examples/heic_to_jpg.py` for programmatic API usage
- The PhotoConverter class can be imported and used independently of CLI