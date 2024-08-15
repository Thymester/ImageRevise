import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ExifTags
import os

def add_watermark(image, watermark, position='center'):
    """
    Add a watermark to an image at a specified position.
    
    Args:
        image (PIL.Image): The image to which the watermark will be added.
        watermark (PIL.Image): The watermark image.
        position (str): Position where the watermark should be placed ('center', 'bottom_right', 'bottom_left', 'top_right', 'top_left').

    Returns:
        PIL.Image: The image with the watermark added.
    """
    if watermark:
        # Resize watermark
        watermark = watermark.resize((128, 128), Image.LANCZOS)
        
        # Create a new image with padding for watermark
        padding = 10
        padded_watermark = Image.new('RGBA', (128 + 2 * padding, 128 + 2 * padding), (255, 255, 255, 0))
        padded_watermark.paste(watermark, (padding, padding))
        
        # Add watermark to the main image
        padded_watermark = padded_watermark.convert("RGBA")
        width, height = image.size
        wm_width, wm_height = padded_watermark.size
        
        # Determine position
        if position == 'center':
            position = ((width - wm_width) // 2, (height - wm_height) // 2)
        elif position == 'bottom_right':
            position = (width - wm_width, height - wm_height)
        elif position == 'bottom_left':
            position = (0, height - wm_height)
        elif position == 'top_right':
            position = (width - wm_width, 0)
        elif position == 'top_left':
            position = (0, 0)
        
        image.paste(padded_watermark, position, padded_watermark)
    return image

def resize_image(input_path, output_path, size, watermark_img=None, keep_aspect_ratio=True):
    """
    Resize an image and optionally add a watermark.
    
    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the resized image.
        size (tuple): New size for the image (width, height).
        watermark_img (PIL.Image): Optional watermark image.
        keep_aspect_ratio (bool): Whether to keep the original aspect ratio.
    """
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Get the original size and aspect ratio
        original_width, original_height = img.size
        original_aspect_ratio = original_width / original_height
        
        # Determine new size while maintaining aspect ratio
        new_width, new_height = size
        if keep_aspect_ratio:
            new_aspect_ratio = new_width / new_height
            if new_aspect_ratio > original_aspect_ratio:
                new_width = int(new_height * original_aspect_ratio)
            else:
                new_height = int(new_width / original_aspect_ratio)
        
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img = add_watermark(img, watermark_img, watermark_position_var.get())
        img.save(output_path, format=format_var.get().upper(), quality=quality_var.get() if format_var.get() == 'JPEG' else None)
        if not keep_metadata_var.get():
            remove_metadata(output_path)

def optimize_image(input_path, output_path, quality=85):
    """
    Optimize an image for web use by adjusting its quality.
    
    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the optimized image.
        quality (int): Quality level for the JPEG image (1-100).
    """
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(output_path, optimize=True, quality=quality)

def remove_metadata(image_path):
    """
    Remove EXIF metadata from an image.
    
    Args:
        image_path (str): Path to the image file.
    """
    with Image.open(image_path) as img:
        if img.info:
            img.info.pop('exif', None)  # Remove EXIF data
        img.save(image_path)

def browse_file():
    """Open a file dialog to select an image file."""
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")],
        title="Select an Image"
    )
    if filename:
        entry_input_path.delete(0, tk.END)
        entry_input_path.insert(0, filename)

def browse_directory():
    """Open a file dialog to select an output directory."""
    directory = filedialog.askdirectory(title="Select Output Directory")
    if directory:
        entry_output_dir.delete(0, tk.END)
        entry_output_dir.insert(0, directory)

def browse_watermark():
    """Open a file dialog to select a watermark image."""
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg")],
        title="Select a Watermark Image"
    )
    if filename:
        entry_watermark.delete(0, tk.END)
        entry_watermark.insert(0, filename)

def view_metadata():
    """Display the EXIF metadata of the selected image."""
    input_path = entry_input_path.get()
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid image file.")
        return

    try:
        with Image.open(input_path) as img:
            exif_data = img._getexif()
            if exif_data:
                metadata = "\n".join(f"{ExifTags.TAGS.get(tag, tag)}: {value}" for tag, value in exif_data.items() if tag in ExifTags.TAGS)
                messagebox.showinfo("Image Metadata", metadata)
            else:
                messagebox.showinfo("Image Metadata", "No EXIF data found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def process_images():
    """Process the selected image according to user settings."""
    input_path = entry_input_path.get()
    output_dir = entry_output_dir.get()
    watermark_path = entry_watermark.get()
    
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid image file.")
        return
    if not os.path.isdir(output_dir):
        messagebox.showerror("Error", "Please select a valid output directory.")
        return

    size_name = size_var.get()
    size = sizes[size_name]

    # Load watermark if provided
    watermark_img = Image.open(watermark_path) if os.path.isfile(watermark_path) else None
    
    try:
        output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_{size_name}.{format_var.get().lower()}"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"Resizing {input_path} to {size_name} size...")
        resize_image(input_path, output_path, size, watermark_img, keep_aspect_ratio_var.get())
        print(f"Saving resized image to {output_path}")

        # Optimize the image for web use
        optimized_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_{size_name}_optimized.{format_var.get().lower()}")
        print(f"Optimizing {output_filename}...")
        optimize_image(output_path, optimized_path)

        messagebox.showinfo("Success", "Images processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def preview_image():
    """Preview the resized image with watermark in the GUI."""
    input_path = entry_input_path.get()
    size_name = size_var.get()
    size = sizes[size_name]

    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid image file.")
        return

    try:
        with Image.open(input_path) as img:
            # Get original aspect ratio
            original_width, original_height = img.size
            original_aspect_ratio = original_width / original_height
            
            # Determine new size while maintaining aspect ratio
            new_width, new_height = size
            if keep_aspect_ratio_var.get():
                new_aspect_ratio = new_width / new_height
                if new_aspect_ratio > original_aspect_ratio:
                    new_width = int(new_height * original_aspect_ratio)
                else:
                    new_height = int(new_width / original_aspect_ratio)
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img = add_watermark(img, Image.open(entry_watermark.get()) if os.path.isfile(entry_watermark.get()) else None, watermark_position_var.get())
            
            # Resize the image for preview
            img.thumbnail((400, 300), Image.LANCZOS)
            
            # Convert image to a format Tkinter can handle
            img_tk = ImageTk.PhotoImage(img)
            
            # Update the preview label with the new image
            preview_label.config(image=img_tk)
            preview_label.image = img_tk  # Keep a reference to prevent garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("ImageRevise")

# Input Path
tk.Label(root, text="Input Image:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_input_path = tk.Entry(root, width=50)
entry_input_path.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=5)

# Output Directory
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_output_dir = tk.Entry(root, width=50)
entry_output_dir.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_directory).grid(row=1, column=2, padx=10, pady=5)

# Watermark
tk.Label(root, text="Watermark Image:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
entry_watermark = tk.Entry(root, width=50)
entry_watermark.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_watermark).grid(row=2, column=2, padx=10, pady=5)

# Size Options
sizes = {
    "Small": (800, 600),
    "Medium": (1280, 960),
    "Large": (1920, 1080),
}
tk.Label(root, text="Select Size:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
size_var = tk.StringVar(value="Medium")
size_menu = tk.OptionMenu(root, size_var, *sizes.keys())
size_menu.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

# Format Options
tk.Label(root, text="Select Format:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
format_var = tk.StringVar(value="JPEG")
format_menu = tk.OptionMenu(root, format_var, "JPEG", "PNG")
format_menu.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

# Quality Options
tk.Label(root, text="Select Quality (for JPEG):").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
quality_var = tk.IntVar(value=85)
quality_scale = tk.Scale(root, variable=quality_var, from_=0, to=100, orient=tk.HORIZONTAL)
quality_scale.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

# Aspect Ratio
keep_aspect_ratio_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Keep Aspect Ratio", variable=keep_aspect_ratio_var).grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

# Metadata Option
keep_metadata_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Remove Metadata", variable=keep_metadata_var).grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

# Watermark Position
tk.Label(root, text="Watermark Position:").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
watermark_position_var = tk.StringVar(value="center")
watermark_position_menu = tk.OptionMenu(root, watermark_position_var, 'center', 'bottom_right', 'bottom_left', 'top_right', 'top_left')
watermark_position_menu.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

# Preview
preview_label = tk.Label(root)
preview_label.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

# Buttons
tk.Button(root, text="Process Images", command=process_images).grid(row=9, column=0, padx=10, pady=10)
tk.Button(root, text="View Metadata", command=view_metadata).grid(row=9, column=1, padx=10, pady=10)

# Run the GUI
root.mainloop()
