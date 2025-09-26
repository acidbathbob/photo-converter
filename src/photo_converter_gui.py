#!/usr/bin/env python3
"""
Photo Converter GUI - A graphical interface for the photo converter tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from typing import List, Optional
import sys
import os

# Add the src directory to the path so we can import photo_converter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photo_converter import PhotoConverter


class PhotoConverterGUI:
    """GUI application for photo conversion"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Initialize converter
        self.converter = PhotoConverter()
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_format = tk.StringVar(value="jpg")
        self.quality = tk.IntVar(value=90)
        self.resize_width = tk.StringVar()
        self.resize_height = tk.StringVar()
        self.batch_mode = tk.BooleanVar(value=False)
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Photo Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input selection
        ttk.Label(main_frame, text="Input:").grid(row=1, column=0, sticky=tk.W, pady=5)
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse File", 
                  command=self.select_input_file).grid(row=0, column=1)
        ttk.Button(input_frame, text="Browse Folder", 
                  command=self.select_input_folder).grid(row=0, column=2)
        
        # Output selection
        ttk.Label(main_frame, text="Output:").grid(row=2, column=0, sticky=tk.W, pady=5)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Browse", 
                  command=self.select_output).grid(row=0, column=1)
        
        # Batch mode checkbox
        ttk.Checkbutton(main_frame, text="Batch Mode (Process folder)", 
                       variable=self.batch_mode,
                       command=self.toggle_batch_mode).grid(
            row=3, column=1, sticky=tk.W, pady=10)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Format selection
        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, pady=5)
        format_combo = ttk.Combobox(options_frame, textvariable=self.selected_format,
                                   values=list(self.get_supported_formats()),
                                   state="readonly", width=15)
        format_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Quality setting
        ttk.Label(options_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, pady=5)
        quality_frame = ttk.Frame(options_frame)
        quality_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        quality_scale = ttk.Scale(quality_frame, from_=1, to=100, 
                                 variable=self.quality, orient=tk.HORIZONTAL)
        quality_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        quality_frame.columnconfigure(0, weight=1)
        
        quality_label = ttk.Label(quality_frame, text="90")
        quality_label.grid(row=0, column=1, padx=(5, 0))
        
        # Update quality label when scale changes
        def update_quality_label(*args):
            quality_label.config(text=str(self.quality.get()))
        self.quality.trace('w', update_quality_label)
        
        # Resize options
        ttk.Label(options_frame, text="Resize:").grid(row=2, column=0, sticky=tk.W, pady=5)
        resize_frame = ttk.Frame(options_frame)
        resize_frame.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Entry(resize_frame, textvariable=self.resize_width, width=8).grid(
            row=0, column=0, padx=(0, 2))
        ttk.Label(resize_frame, text="×").grid(row=0, column=1, padx=2)
        ttk.Entry(resize_frame, textvariable=self.resize_height, width=8).grid(
            row=0, column=2, padx=(2, 5))
        ttk.Label(resize_frame, text="(optional)").grid(row=0, column=3, padx=(5, 0))
        
        # Convert button
        self.convert_button = ttk.Button(main_frame, text="Convert", 
                                        command=self.start_conversion)
        self.convert_button.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status/log area
        log_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initial log message
        self.log_message("Photo Converter GUI ready!")
        if not self.converter.SUPPORTED_FORMATS.get('.heic'):
            self.log_message("Note: HEIC support not available. Install pyheif for HEIC support.")
    
    def get_supported_formats(self):
        """Get list of supported output formats"""
        formats = []
        for ext, fmt in self.converter.SUPPORTED_FORMATS.items():
            if ext.startswith('.'):
                formats.append(ext[1:])  # Remove the dot
        return sorted(set(formats))
    
    def select_input_file(self):
        """Select input file"""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.webp *.gif *.bmp *.tiff *.tif *.heic *.heif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path.set(filename)
            self.batch_mode.set(False)
    
    def select_input_folder(self):
        """Select input folder for batch processing"""
        folder = filedialog.askdirectory()
        if folder:
            self.input_path.set(folder)
            self.batch_mode.set(True)
    
    def select_output(self):
        """Select output file or folder"""
        if self.batch_mode.get():
            # Select output folder for batch mode
            folder = filedialog.askdirectory()
            if folder:
                self.output_path.set(folder)
        else:
            # Select output file for single file mode
            format_ext = self.selected_format.get()
            filetypes = [
                (f"{format_ext.upper()} files", f"*.{format_ext}"),
                ("All files", "*.*")
            ]
            filename = filedialog.asksaveasfilename(filetypes=filetypes,
                                                   defaultextension=f".{format_ext}")
            if filename:
                self.output_path.set(filename)
    
    def toggle_batch_mode(self):
        """Toggle between single file and batch mode"""
        # Clear paths when switching modes
        self.output_path.set("")
    
    def log_message(self, message):
        """Add message to log area"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input file or folder")
            return False
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output location")
            return False
        
        input_path = Path(self.input_path.get())
        if not input_path.exists():
            messagebox.showerror("Error", "Input path does not exist")
            return False
        
        # Validate resize dimensions if provided
        if self.resize_width.get() or self.resize_height.get():
            try:
                if self.resize_width.get():
                    width = int(self.resize_width.get())
                    if width <= 0:
                        raise ValueError("Width must be positive")
                if self.resize_height.get():
                    height = int(self.resize_height.get())
                    if height <= 0:
                        raise ValueError("Height must be positive")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid resize dimensions: {e}")
                return False
        
        return True
    
    def get_resize_dimensions(self):
        """Get resize dimensions tuple or None"""
        if self.resize_width.get() and self.resize_height.get():
            try:
                return (int(self.resize_width.get()), int(self.resize_height.get()))
            except ValueError:
                return None
        return None
    
    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        if not self.validate_inputs():
            return
        
        # Disable convert button and start progress
        self.convert_button.config(state='disabled')
        self.progress.start()
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        self.log_message("Starting conversion...")
        
        # Start conversion in separate thread to prevent GUI freezing
        conversion_thread = threading.Thread(target=self.perform_conversion)
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def perform_conversion(self):
        """Perform the actual conversion"""
        try:
            input_path = Path(self.input_path.get())
            output_path = Path(self.output_path.get())
            format_ext = f".{self.selected_format.get()}"
            quality = self.quality.get() if self.quality.get() != 90 else None
            resize_dims = self.get_resize_dimensions()
            
            # Reset converter counters
            self.converter.converted_count = 0
            self.converter.failed_count = 0
            
            if self.batch_mode.get():
                # Batch processing
                self.log_message(f"Processing folder: {input_path}")
                self.log_message(f"Output folder: {output_path}")
                self.log_message(f"Target format: {format_ext}")
                
                # Create output directory
                output_path.mkdir(parents=True, exist_ok=True)
                
                # Get image files
                image_files = self.converter.get_image_files(input_path)
                
                if not image_files:
                    self.log_message("No image files found in the input directory")
                    return
                
                self.log_message(f"Found {len(image_files)} image files to convert")
                
                # Process files
                for i, image_file in enumerate(image_files, 1):
                    output_file = output_path / f"{image_file.stem}{format_ext}"
                    self.log_message(f"Converting ({i}/{len(image_files)}): {image_file.name}")
                    
                    success = self.converter.convert_image(image_file, output_file, 
                                                         quality, resize_dims)
                    if not success:
                        self.log_message(f"Failed to convert: {image_file.name}")
            
            else:
                # Single file conversion
                self.log_message(f"Converting: {input_path.name}")
                self.log_message(f"Output: {output_path}")
                
                # Create output directory if needed
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                success = self.converter.convert_image(input_path, output_path, 
                                                     quality, resize_dims)
                if not success:
                    self.log_message("Conversion failed!")
            
            # Show results
            self.log_message("\n" + "="*50)
            self.log_message("Conversion Complete!")
            self.log_message(f"Successfully converted: {self.converter.converted_count} files")
            if self.converter.failed_count > 0:
                self.log_message(f"Failed conversions: {self.converter.failed_count} files")
            
        except Exception as e:
            self.log_message(f"Error during conversion: {str(e)}")
        
        finally:
            # Re-enable button and stop progress (must be done in main thread)
            self.root.after(0, self.conversion_finished)
    
    def conversion_finished(self):
        """Called when conversion is finished (runs in main thread)"""
        self.convert_button.config(state='normal')
        self.progress.stop()


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = PhotoConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()