import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
import threading
import os

def update_custom_size_visibility(*args):
    """Show or hide custom size fields based on the selected size."""
    if size_var.get() == 'Custom':
        custom_width_label.grid(row=6, column=0, sticky=tk.W)
        custom_width_entry.grid(row=6, column=1, padx=5, pady=5)
        custom_height_label.grid(row=6, column=2, sticky=tk.W)
        custom_height_entry.grid(row=6, column=3, padx=5, pady=5)
    else:
        custom_width_label.grid_forget()
        custom_width_entry.grid_forget()
        custom_height_label.grid_forget()
        custom_height_entry.grid_forget()

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def add_watermark(image, watermark, position='center', watermark_size=(128, 128)):
    """Add a watermark to an image at a specified position with a custom size."""
    if watermark:
        watermark = watermark.resize(watermark_size, Image.LANCZOS)
        padding = 10
        padded_watermark = Image.new('RGBA', (watermark_size[0] + 2 * padding, watermark_size[1] + 2 * padding), (255, 255, 255, 0))
        padded_watermark.paste(watermark, (padding, padding))
        padded_watermark = padded_watermark.convert("RGBA")
        width, height = image.size
        wm_width, wm_height = padded_watermark.size
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

def resize_image(input_path, output_path, size, watermark_img=None, watermark_size=(128, 128), keep_aspect_ratio=True):
    """Resize an image and optionally add a watermark with a custom size."""
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        original_width, original_height = img.size
        original_aspect_ratio = original_width / original_height
        new_width, new_height = size
        if keep_aspect_ratio:
            new_aspect_ratio = new_width / new_height
            if new_aspect_ratio > original_aspect_ratio:
                new_width = int(new_height * original_aspect_ratio)
            else:
                new_height = int(new_width / original_aspect_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img = add_watermark(img, watermark_img, watermark_position_var.get(), watermark_size=(int(watermark_width_var.get()), int(watermark_height_var.get())))
        img.save(output_path, format=format_var.get().upper(), quality=quality_var.get() if format_var.get() == 'JPEG' else None)
        if not keep_metadata_var.get():
            remove_metadata(output_path)

def optimize_image(input_path, output_path, quality=85):
    """Optimize an image for web use by adjusting its quality."""
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(output_path, optimize=True, quality=quality)

def remove_metadata(image_path):
    """Remove EXIF metadata from an image."""
    with Image.open(image_path) as img:
        if img.info:
            img.info.pop('exif', None)
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

def process_images_thread():
    """Thread function to process images."""
    input_path = entry_input_path.get()
    output_dir = entry_output_dir.get()
    watermark_path = entry_watermark.get()
    if not os.path.isfile(input_path):
        root.after(0, lambda: messagebox.showerror("Error", "Please select a valid image file."))
        return
    if not os.path.isdir(output_dir):
        root.after(0, lambda: messagebox.showerror("Error", "Please select a valid output directory."))
        return
    size_name = size_var.get()
    if size_name == 'Custom':
        size = (int(custom_width_var.get()), int(custom_height_var.get()))
    else:
        size = sizes[size_name]
    watermark_img = Image.open(watermark_path) if os.path.isfile(watermark_path) else None
    try:
        output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_{size_name}.{format_var.get().lower()}"
        output_path = os.path.join(output_dir, output_filename)
        resize_image(input_path, output_path, size, watermark_img, watermark_size=(int(watermark_width_var.get()), int(watermark_height_var.get())), keep_aspect_ratio=keep_aspect_ratio_var.get())
        optimized_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_{size_name}_optimized.{format_var.get().lower()}")
        optimize_image(output_path, optimized_path)
        root.after(0, lambda: messagebox.showinfo("Success", "Images processed successfully!"))
        root.after(0, update_label_to_done)
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))

def process_images():
    """Start processing images in a separate thread."""
    threading.Thread(target=process_images_thread).start()

def update_label_to_done():
    """Clear the text of the label indicating that image processing is done."""
    image_processing_label.config(text="Processing Done")

def start_image_processing():
    """Start the image processing in a new thread."""
    global image_processing_label
    image_processing_label = tk.Label(root, text="The image is now processing...please standby")
    image_processing_label.grid(row=13, column=1, sticky=tk.W)
    threading.Thread(target=process_images_thread, daemon=True).start()

def preview_image():
    """Preview the resized image with watermark in the GUI."""
    input_path = entry_input_path.get()
    size_name = size_var.get()

    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid image file.")
        return

    try:
        with Image.open(input_path) as img:
            # Determine new size based on the selected option
            if size_name == 'Custom':
                size = (int(custom_width_var.get()), int(custom_height_var.get()))
            else:
                size = sizes[size_name]
                
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
            
            watermark_img = Image.open(entry_watermark.get()) if os.path.isfile(entry_watermark.get()) else None
            img = add_watermark(img, watermark_img, watermark_position_var.get(), watermark_size=(int(watermark_width_var.get()), int(watermark_height_var.get())))
            
            img.thumbnail((400, 400))
            img_tk = ImageTk.PhotoImage(img)

            if hasattr(preview_frame, 'img_label'):
                preview_frame.img_label.config(image=img_tk)
                preview_frame.img_label.image = img_tk
            else:
                preview_frame.img_label = tk.Label(preview_frame, image=img_tk)
                preview_frame.img_label.image = img_tk
                preview_frame.img_label.pack()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while previewing the image: {e}")

# GUI setup
root = tk.Tk()
root.resizable(False, False)
root.title("ImageRevise")

# Input path
tk.Label(root, text="Input Image:").grid(row=0, column=0, sticky=tk.W)
entry_input_path = tk.Entry(root, width=50)
entry_input_path.grid(row=0, column=1, padx=5, pady=5)
browse_input_button = tk.Button(root, text="Browse", command=browse_file)
browse_input_button.grid(row=0, column=2, padx=5, pady=5)
Tooltip(browse_input_button, "Browse for an image file to edit.")
Tooltip(entry_input_path, "Enter the path of the image file here\nOr use the browse button for easier pathing.")

# Output directory
tk.Label(root, text="Output Directory:").grid(row=1, column=0, sticky=tk.W)
entry_output_dir = tk.Entry(root, width=50)
entry_output_dir.grid(row=1, column=1, padx=5, pady=5)
browse_output_button = tk.Button(root, text="Browse", command=browse_directory)
browse_output_button.grid(row=1, column=2, padx=5, pady=5)
Tooltip(browse_output_button, "Browse for an output directory.")
Tooltip(entry_output_dir, "Enter the directory where processed images will be saved\nOr use the browse button for easier pathing.")

# Watermark
tk.Label(root, text="Watermark Image:").grid(row=2, column=0, sticky=tk.W)
entry_watermark = tk.Entry(root, width=50)
entry_watermark.grid(row=2, column=1, padx=5, pady=5)
browse_watermark_button = tk.Button(root, text="Browse", command=browse_watermark)
browse_watermark_button.grid(row=2, column=2, padx=5, pady=5)
Tooltip(browse_watermark_button, "Browse for a watermark image.")
Tooltip(entry_watermark, "Enter the path of the watermark image here\nOr use the browse button for easier pathing.")

# Watermark size
tk.Label(root, text="Watermark Width:").grid(row=3, column=0, sticky=tk.W)
watermark_width_var = tk.StringVar(value='128')
tk.Entry(root, textvariable=watermark_width_var, width=10).grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Watermark Height:").grid(row=3, column=2, sticky=tk.W)
watermark_height_var = tk.StringVar(value='128')
tk.Entry(root, textvariable=watermark_height_var, width=10).grid(row=3, column=3, padx=5, pady=5)

# Position
tk.Label(root, text="Watermark Position:").grid(row=4, column=0, sticky=tk.W)
watermark_position_var = tk.StringVar(value='center')
watermark_position_menu = tk.OptionMenu(root, watermark_position_var, 'center', 'bottom_right', 'bottom_left', 'top_right', 'top_left')
watermark_position_menu.grid(row=4, column=1, padx=5, pady=5)
Tooltip(watermark_position_menu, "Select the position for the watermark on the image.")

# Size
sizes = {'Small': (600, 600), 'Medium': (1100, 1100), 'Large': (2000, 2000)}
size_var = tk.StringVar(value='Medium')
tk.Label(root, text="Size:").grid(row=5, column=0, sticky=tk.W)
size_menu = tk.OptionMenu(root, size_var, *sizes.keys(), 'Custom', command=update_custom_size_visibility)
size_menu.grid(row=5, column=1, padx=5, pady=5)
Tooltip(size_menu, "Select the size of the output image.")

# Custom size fields
custom_width_var = tk.StringVar(value='800')
custom_height_var = tk.StringVar(value='600')

custom_width_label = tk.Label(root, text="Custom Width:")
custom_width_label.grid(row=6, column=0, sticky=tk.W)
custom_width_entry = tk.Entry(root, textvariable=custom_width_var, width=10)
custom_width_entry.grid(row=6, column=1, padx=5, pady=5)
Tooltip(custom_width_entry, "Enter the custom width for the image in pixels.")

custom_height_label = tk.Label(root, text="Custom Height:")
custom_height_label.grid(row=6, column=2, sticky=tk.W)
custom_height_entry = tk.Entry(root, textvariable=custom_height_var, width=10)
custom_height_entry.grid(row=6, column=3, padx=5, pady=5)
Tooltip(custom_height_entry, "Enter the custom height for the image in pixels.")

# Format
tk.Label(root, text="Format:").grid(row=7, column=0, sticky=tk.W)
format_var = tk.StringVar(value='JPEG')
format_menu = tk.OptionMenu(root, format_var, 'JPEG', 'PNG')
format_menu.grid(row=7, column=1, padx=5, pady=5)
Tooltip(format_menu, "Select your output format:\nJPEG is used for reducing file size/image quality—the reduction can be as much as 90%\nPNG is used for increasing file size/image quality—the increase can be as much as 90%")

# Quality
tk.Label(root, text="Quality:").grid(row=8, column=0, sticky=tk.W)
quality_var = tk.IntVar(value=85)
quality_slider = tk.Scale(root, from_=1, to_=100, orient=tk.HORIZONTAL, variable=quality_var)
quality_slider.grid(row=8, column=1, padx=5, pady=5)
Tooltip(quality_slider, "Set the quality level for the output image.")

# Keep aspect ratio
keep_aspect_ratio_var = tk.BooleanVar(value=False)
keep_aspect_ratio_checkbox = tk.Checkbutton(root, text="Keep Aspect Ratio", variable=keep_aspect_ratio_var)
keep_aspect_ratio_checkbox.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
Tooltip(keep_aspect_ratio_checkbox, "Check this box to maintain the aspect ratio of the image.")

# Keep metadata
keep_metadata_var = tk.BooleanVar(value=True)
keep_metadata_checkbox = tk.Checkbutton(root, text="Keep Metadata", variable=keep_metadata_var)
keep_metadata_checkbox.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
Tooltip(keep_metadata_checkbox, "Uncheck this box to remove the information about your visual file.")

# Buttons
process_images_button = tk.Button(root, text="Process Images", command=start_image_processing)
process_images_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

preview_image_button = tk.Button(root, text="Preview Image", command=preview_image)
preview_image_button.grid(row=11, column=2, columnspan=2, padx=5, pady=5)
Tooltip(preview_image_button, "Click to preview the processed image.\nThe previewed image is not true to size, only meant as a rough preview.")

view_metadata_button = tk.Button(root, text="View Metadata", command=view_metadata)
view_metadata_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5)
Tooltip(view_metadata_button, "Click to view metadata of the selected image.")

# Preview frame
preview_frame = tk.Frame(root, bg='white')
preview_frame.grid(row=14, column=0, columnspan=6, rowspan=6, padx=5, pady=5)

# Initialize custom size visibility
update_custom_size_visibility()

root.mainloop()