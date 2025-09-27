# Photo Converter

A user-friendly Python application for converting images between different formats with special support for iPhone HEIC photos.

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)

## ✨ Features

- **🖼️ Multiple Format Support**: Convert between JPEG, PNG, WebP, GIF, BMP, TIFF, HEIC/HEIF
- **📱 iPhone Photo Support**: Seamless conversion of HEIC photos from iPhones
- **🎛️ GUI Interface**: Easy-to-use graphical interface built with tkinter
- **⚡ Batch Processing**: Convert entire folders of images at once
- **🎨 Quality Control**: Adjust compression quality for JPEG/WebP formats
- **📏 Image Resizing**: Optional resizing during conversion
- **🔧 Command Line**: Full CLI support for automation and scripting
- **🐧 Cross Platform**: Works on Linux, macOS, and Windows

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/acidbathbob/photo-converter.git
cd photo-converter
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **For HEIC support (iPhone photos):**
```bash
pip install pillow-heif
```

### Usage

#### GUI Mode (Recommended for beginners)
```bash
python3 launch_gui.py
```

#### Command Line Mode

**Single file conversion:**
```bash
python3 src/photo_converter.py input.heic output.jpg
```

**Batch conversion:**
```bash
python3 src/photo_converter.py /path/to/photos/ --batch --format jpg --output /path/to/converted/
```

**With quality and resize options:**
```bash
python3 src/photo_converter.py input.heic output.jpg --quality 85 --resize 1920x1080
```

## 📋 Requirements

- Python 3.8+
- Pillow (PIL) 10.0.0+
- pillow-heif (for HEIC support)
- tkinter (usually included with Python)
- click 8.0.0+
- tqdm 4.65.0+

### System Requirements for HEIC Support

**Linux (Fedora/RHEL/CentOS):**
```bash
sudo dnf install libheif-devel libheif-freeworld
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libheif-dev
```

**macOS:**
```bash
brew install libheif
```

## 🖥️ GUI Features

The intuitive graphical interface supports:
- **Input Selection**: Single file, multiple files, or entire folders
- **Output Options**: Choose destination and format
- **Quality Control**: Adjust compression settings
- **Image Resizing**: Optional resizing during conversion
- **Progress Tracking**: Real-time conversion status
- **Dependency Management**: Built-in installer for HEIC support

## 📖 Command Line Reference

```
Usage: photo_converter.py [OPTIONS] INPUT_PATH [OUTPUT_PATH]

Options:
  --batch              Process all images in the input directory
  -o, --output PATH    Output directory for batch processing
  -f, --format TEXT    Target format (jpg, png, webp, etc.)
  -q, --quality INT    Quality for lossy formats (1-100)
  --resize TEXT        Resize images (format: WIDTHxHEIGHT, e.g., 800x600)
  -v, --verbose        Verbose output
  --help               Show this message and exit
```

## 🔧 Development

### Running Tests
```bash
python3 test_folder_selection.py "/path/to/test/images"
```

### Project Structure
```
photo-converter/
├── src/
│   ├── photo_converter.py      # Core conversion logic
│   └── photo_converter_gui.py  # GUI implementation
├── examples/
│   ├── gui_demo.py            # GUI demonstration
│   └── heic_to_jpg.py         # Simple HEIC converter
├── launch_gui.py              # GUI launcher
├── test_folder_selection.py   # Folder analysis tool
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🐛 Troubleshooting

### HEIC Files Won't Convert
1. **Install pillow-heif:**
   ```bash
   pip install pillow-heif
   ```

2. **Install system libraries:**
   - **Linux:** `sudo dnf install libheif-devel libheif-freeworld`
   - **macOS:** `brew install libheif`
   - **Windows:** Usually works out of the box with pillow-heif

3. **Check dependencies:**
   Use the GUI menu: Tools → Check Dependencies

### Common Issues

**"struct heif_decoding_options" error:**
- This is fixed in the latest version using pillow-heif instead of pyheif
- Update to the latest version: `git pull origin main`

**GUI won't start:**
- Ensure tkinter is installed: `python3 -m tkinter`
- On some Linux distributions: `sudo dnf install python3-tkinter`

**Permission errors:**
- Ensure you have read access to input files
- Ensure you have write access to output directory

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pillow](https://pillow.readthedocs.io/) for image processing
- [pillow-heif](https://github.com/bigcat88/pillow_heif) for HEIC support
- [click](https://click.palletsprojects.com/) for command-line interface
- [tqdm](https://tqdm.github.io/) for progress bars

## 📞 Support

If you encounter any problems:
1. Check the [Issues](https://github.com/acidbathbob/photo-converter/issues) page
2. Create a new issue with details about your problem
3. Include your operating system, Python version, and error messages

---

**Made with ❤️ for easy image conversion**
