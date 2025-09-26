# Photo Converter

A simple and efficient photo conversion tool that allows you to convert images between different formats.

## Features

- Convert between popular image formats (JPEG, PNG, WEBP, GIF, BMP, TIFF, HEIC/HEIF)
- Batch processing support
- Resize images while converting
- Quality adjustment for lossy formats
- Command-line interface for easy automation

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd photo-converter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For HEIC support on Fedora (optional):
   ```bash
   sudo dnf install libheif-freeworld libheif-tools
   ```

## Usage

### Basic conversion:
```bash
python src/photo_converter.py input.jpg output.png
```

### Batch conversion:
```bash
python src/photo_converter.py --batch input_folder/ --output output_folder/ --format png
```

### With quality adjustment:
```bash
python src/photo_converter.py input.jpg output.jpg --quality 85
```

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- HEIC/HEIF (.heic, .heif)

## Development

Run tests:
```bash
python -m pytest tests/
```

## License

MIT License