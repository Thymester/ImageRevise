import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
import threading
import os

class ModernTooltip:
    def __init__(self, widget, text, delay=750):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip = None
        self.timer_id = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        self.schedule_tooltip()

    def on_leave(self, event=None):
        self.cancel_tooltip()
        self.hide_tooltip()

    def on_motion(self, event=None):
        self.cancel_tooltip()
        self.schedule_tooltip()

    def schedule_tooltip(self):
        self.cancel_tooltip()
        self.timer_id = self.widget.after(self.delay, self.show_tooltip)

    def cancel_tooltip(self):
        if self.timer_id:
            self.widget.after_cancel(self.timer_id)
            self.timer_id = None

    def show_tooltip(self):
        if self.tooltip:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.attributes("-topmost", True)
        
        # Modern styling
        frame = tk.Frame(self.tooltip, bg="#2D3748", relief="solid", borderwidth=1)
        frame.pack()
        
        label = tk.Label(frame, text=self.text, 
                        bg="#2D3748", fg="#E2E8F0", 
                        font=("Segoe UI", 9),
                        padx=12, pady=8)
        label.pack()

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack elements
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        self.bind_mousewheel()

    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

class ModernImageProcessor:
    def __init__(self, root):
        self.root = root
        self.setup_styles()
        self.setup_variables()
        self.create_interface()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure modern colors
        self.colors = {
            'bg': '#F7FAFC',
            'card_bg': '#FFFFFF',
            'primary': '#4299E1',
            'primary_dark': '#3182CE',
            'secondary': '#718096',
            'text': '#2D3748',
            'text_light': '#718096',
            'border': '#E2E8F0',
            'success': '#48BB78',
            'warning': '#ED8936'
        }
        
        # Configure styles
        self.style.configure('Card.TFrame', 
                           background=self.colors['card_bg'],
                           relief='solid',
                           borderwidth=1)
        
        self.style.configure('Modern.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(15, 8))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['primary_dark'])])
        
        self.style.configure('Secondary.TButton',
                           background=self.colors['secondary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(10, 6))
        
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           borderwidth=1,
                           relief='solid',
                           padding=8)
        
        self.style.configure('Modern.TCombobox',
                           fieldbackground='white',
                           borderwidth=1,
                           relief='solid',
                           padding=6)

    def setup_variables(self):
        self.input_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.watermark_path_var = tk.StringVar()
        self.watermark_width_var = tk.StringVar(value='128')
        self.watermark_height_var = tk.StringVar(value='128')
        self.watermark_position_var = tk.StringVar(value='center')
        self.size_var = tk.StringVar(value='Medium')
        self.custom_width_var = tk.StringVar(value='800')
        self.custom_height_var = tk.StringVar(value='600')
        self.format_var = tk.StringVar(value='JPEG')
        self.quality_var = tk.IntVar(value=85)
        self.keep_aspect_ratio_var = tk.BooleanVar(value=False)
        self.keep_metadata_var = tk.BooleanVar(value=True)
        
        self.sizes = {'Small': (600, 600), 'Medium': (1100, 1100), 'Large': (2000, 2000)}

    def create_interface(self):
        self.root.configure(bg=self.colors['bg'])
        self.root.title("ImageRevise Pro")
        self.root.geometry("1000x650")
        self.root.minsize(900, 500)
        
        # Create main container with two columns
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left column - scrollable content
        left_frame = tk.Frame(main_container, bg=self.colors['bg'])
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Title
        title_label = tk.Label(left_frame, 
                              text="ImageRevise Pro", 
                              font=("Segoe UI", 20, "bold"),
                              bg=self.colors['bg'], 
                              fg=self.colors['text'])
        title_label.pack(pady=(0, 15))
        
        # Scrollable content area
        self.scroll_frame = ScrollableFrame(left_frame, bg=self.colors['bg'])
        self.scroll_frame.pack(fill='both', expand=True)
        
        # Create sections in scrollable area
        self.create_input_section(self.scroll_frame.scrollable_frame)
        self.create_watermark_section(self.scroll_frame.scrollable_frame)
        self.create_output_section(self.scroll_frame.scrollable_frame)
        self.create_actions_section(self.scroll_frame.scrollable_frame)
        
        # Right column - preview (fixed)
        right_frame = tk.Frame(main_container, bg=self.colors['bg'], width=350)
        right_frame.pack(side='right', fill='y')
        right_frame.pack_propagate(False)
        
        self.create_preview_section(right_frame)
        
    def create_card_frame(self, parent, title, compact=False):
        # Card container
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill='x', pady=(0, 10))
        
        # Card title
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        padding_y = (10, 5) if compact else (12, 8)
        title_frame.pack(fill='x', padx=15, pady=padding_y)
        
        title_label = tk.Label(title_frame,
                              text=title,
                              font=("Segoe UI", 12, "bold"),
                              bg=self.colors['card_bg'],
                              fg=self.colors['text'])
        title_label.pack(anchor='w')
        
        # Content frame
        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        padding_y = (0, 10) if compact else (0, 15)
        content_frame.pack(fill='x', padx=15, pady=padding_y)
        
        return content_frame
        
    def create_input_section(self, parent):
        content = self.create_card_frame(parent, "📁 Files", compact=True)
        
        # Input file
        tk.Label(content, text="Input Image", 
                font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor='w')
        
        input_frame = tk.Frame(content, bg=self.colors['card_bg'])
        input_frame.pack(fill='x', pady=(3, 8))
        
        self.input_entry = ttk.Entry(input_frame, 
                                   textvariable=self.input_path_var,
                                   style='Modern.TEntry',
                                   font=("Segoe UI", 9))
        self.input_entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        ttk.Button(input_frame, text="Browse", command=self.browse_file,
                  style='Secondary.TButton').pack(side='right')
        
        # Output directory
        tk.Label(content, text="Output Directory", 
                font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor='w')
        
        output_frame = tk.Frame(content, bg=self.colors['card_bg'])
        output_frame.pack(fill='x', pady=(3, 0))
        
        self.output_entry = ttk.Entry(output_frame, 
                                    textvariable=self.output_dir_var,
                                    style='Modern.TEntry',
                                    font=("Segoe UI", 9))
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        ttk.Button(output_frame, text="Browse", command=self.browse_directory,
                  style='Secondary.TButton').pack(side='right')
        
        ModernTooltip(self.input_entry, "Select the image file to process")
        ModernTooltip(self.output_entry, "Choose where to save processed images")
        
    def create_watermark_section(self, parent):
        content = self.create_card_frame(parent, "💧 Watermark", compact=True)
        
        # Watermark file
        tk.Label(content, text="Watermark Image (Optional)", 
                font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor='w')
        
        watermark_frame = tk.Frame(content, bg=self.colors['card_bg'])
        watermark_frame.pack(fill='x', pady=(3, 8))
        
        self.watermark_entry = ttk.Entry(watermark_frame, 
                                       textvariable=self.watermark_path_var,
                                       style='Modern.TEntry',
                                       font=("Segoe UI", 9))
        self.watermark_entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        ttk.Button(watermark_frame, text="Browse", command=self.browse_watermark,
                  style='Secondary.TButton').pack(side='right')
        
        # Watermark settings in grid
        settings_frame = tk.Frame(content, bg=self.colors['card_bg'])
        settings_frame.pack(fill='x')
        
        # Size
        tk.Label(settings_frame, text="Size:", font=("Segoe UI", 9),
                bg=self.colors['card_bg'], fg=self.colors['text']).grid(row=0, column=0, sticky='w')
        
        size_frame = tk.Frame(settings_frame, bg=self.colors['card_bg'])
        size_frame.grid(row=0, column=1, sticky='w', padx=(5, 15))
        
        ttk.Entry(size_frame, textvariable=self.watermark_width_var, width=6,
                 style='Modern.TEntry', font=("Segoe UI", 9)).pack(side='left')
        tk.Label(size_frame, text="×", bg=self.colors['card_bg']).pack(side='left', padx=3)
        ttk.Entry(size_frame, textvariable=self.watermark_height_var, width=6,
                 style='Modern.TEntry', font=("Segoe UI", 9)).pack(side='left')
        
        # Position
        tk.Label(settings_frame, text="Position:", font=("Segoe UI", 9),
                bg=self.colors['card_bg'], fg=self.colors['text']).grid(row=0, column=2, sticky='w')
        
        ttk.Combobox(settings_frame, textvariable=self.watermark_position_var,
                    values=['center', 'bottom_right', 'bottom_left', 'top_right', 'top_left'],
                    style='Modern.TCombobox', state='readonly', width=12,
                    font=("Segoe UI", 9)).grid(row=0, column=3, sticky='w', padx=(5, 0))
        
    def create_output_section(self, parent):
        content = self.create_card_frame(parent, "⚙️ Settings", compact=True)
        
        # First row: Size and Format
        row1 = tk.Frame(content, bg=self.colors['card_bg'])
        row1.pack(fill='x', pady=(0, 8))
        
        # Size
        size_frame = tk.Frame(row1, bg=self.colors['card_bg'])
        size_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        tk.Label(size_frame, text="Output Size", font=("Segoe UI", 9, "bold"),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor='w')
        
        self.size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                     values=list(self.sizes.keys()) + ['Custom'],
                                     style='Modern.TCombobox', state='readonly',
                                     font=("Segoe UI", 9))
        self.size_combo.pack(fill='x', pady=(3, 0))
        self.size_combo.bind('<<ComboboxSelected>>', self.update_custom_size_visibility)
        
        # Format
        format_frame = tk.Frame(row1, bg=self.colors['card_bg'])
        format_frame.pack(side='right')
        
        tk.Label(format_frame, text="Format", font=("Segoe UI", 9, "bold"),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor='w')
        
        ttk.Combobox(format_frame, textvariable=self.format_var,
                    values=['JPEG', 'PNG'], style='Modern.TCombobox',
                    state='readonly', width=8, font=("Segoe UI", 9)).pack(pady=(3, 0))
        
        # Custom size frame
        self.custom_size_frame = tk.Frame(content, bg=self.colors['card_bg'])
        
        tk.Label(self.custom_size_frame, text="Custom Dimensions", 
                font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor='w')
        
        custom_inputs = tk.Frame(self.custom_size_frame, bg=self.colors['card_bg'])
        custom_inputs.pack(fill='x', pady=(3, 0))
        
        ttk.Entry(custom_inputs, textvariable=self.custom_width_var, width=8,
                 style='Modern.TEntry', font=("Segoe UI", 9)).pack(side='left')
        tk.Label(custom_inputs, text="×", bg=self.colors['card_bg']).pack(side='left', padx=5)
        ttk.Entry(custom_inputs, textvariable=self.custom_height_var, width=8,
                 style='Modern.TEntry', font=("Segoe UI", 9)).pack(side='left')
        
        # Quality and checkboxes
        bottom_frame = tk.Frame(content, bg=self.colors['card_bg'])
        bottom_frame.pack(fill='x')
        
        # Quality
        quality_frame = tk.Frame(bottom_frame, bg=self.colors['card_bg'])
        quality_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        tk.Label(quality_frame, text="Quality", font=("Segoe UI", 9, "bold"),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor='w')
        
        self.quality_slider = tk.Scale(quality_frame, from_=1, to_=100, orient=tk.HORIZONTAL,
                                     variable=self.quality_var, bg=self.colors['card_bg'],
                                     fg=self.colors['text'], highlightthickness=0,
                                     length=150, showvalue=True)
        self.quality_slider.pack(anchor='w', pady=(3, 0))
        
        # Checkboxes
        checkbox_frame = tk.Frame(bottom_frame, bg=self.colors['card_bg'])
        checkbox_frame.pack(side='right', anchor='n')
        
        tk.Checkbutton(checkbox_frame, text="Keep Aspect Ratio",
                      variable=self.keep_aspect_ratio_var, bg=self.colors['card_bg'],
                      fg=self.colors['text'], font=("Segoe UI", 9),
                      activebackground=self.colors['card_bg']).pack(anchor='w')
        
        tk.Checkbutton(checkbox_frame, text="Keep Metadata",
                      variable=self.keep_metadata_var, bg=self.colors['card_bg'],
                      fg=self.colors['text'], font=("Segoe UI", 9),
                      activebackground=self.colors['card_bg']).pack(anchor='w')
        
    def create_actions_section(self, parent):
        content = self.create_card_frame(parent, "🚀 Actions", compact=True)
        
        # Buttons in a row
        buttons_frame = tk.Frame(content, bg=self.colors['card_bg'])
        buttons_frame.pack()
        
        self.process_btn = ttk.Button(buttons_frame, text="🎯 Process Images",
                                    command=self.start_image_processing,
                                    style='Modern.TButton')
        self.process_btn.pack(side='left', padx=(0, 8))
        
        ttk.Button(buttons_frame, text="👁️ Preview", command=self.preview_image,
                  style='Secondary.TButton').pack(side='left', padx=(0, 8))
        
        ttk.Button(buttons_frame, text="📊 Metadata", command=self.view_metadata,
                  style='Secondary.TButton').pack(side='left')
        
        # Status
        self.status_label = tk.Label(content, text="Ready to process images",
                                   font=("Segoe UI", 9), bg=self.colors['card_bg'],
                                   fg=self.colors['text_light'])
        self.status_label.pack(pady=(8, 0))
        
    def create_preview_section(self, parent):
        # Preview title
        tk.Label(parent, text="👁️ Preview", font=("Segoe UI", 12, "bold"),
                bg=self.colors['bg'], fg=self.colors['text']).pack(pady=(0, 10))
        
        # Preview card
        preview_card = ttk.Frame(parent, style='Card.TFrame')
        preview_card.pack(fill='both', expand=True)
        
        self.preview_frame = tk.Frame(preview_card, bg=self.colors['card_bg'])
        self.preview_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Placeholder
        self.preview_placeholder = tk.Label(self.preview_frame,
                                          text="Preview will appear here\n\nClick 'Preview' to see\nprocessed image",
                                          font=("Segoe UI", 10),
                                          bg=self.colors['card_bg'],
                                          fg=self.colors['text_light'],
                                          justify='center')
        self.preview_placeholder.pack(expand=True)
        
    def update_custom_size_visibility(self, event=None):
        if self.size_var.get() == 'Custom':
            self.custom_size_frame.pack(fill='x', pady=(8, 0))
        else:
            self.custom_size_frame.pack_forget()
            
    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")],
            title="Select an Image"
        )
        if filename:
            self.input_path_var.set(filename)
            
    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            
    def browse_watermark(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")],
            title="Select a Watermark Image"
        )
        if filename:
            self.watermark_path_var.set(filename)
            
    def view_metadata(self):
        input_path = self.input_path_var.get()
        if not os.path.isfile(input_path):
            messagebox.showerror("Error", "Please select a valid image file.")
            return
        try:
            with Image.open(input_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    metadata = "\n".join(f"{ExifTags.TAGS.get(tag, tag)}: {value}" 
                                       for tag, value in exif_data.items() 
                                       if tag in ExifTags.TAGS)
                    messagebox.showinfo("Image Metadata", metadata)
                else:
                    messagebox.showinfo("Image Metadata", "No EXIF data found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            
    def add_watermark(self, image, watermark, position='center', watermark_size=(128, 128)):
        if watermark:
            watermark = watermark.resize(watermark_size, Image.LANCZOS)
            padding = 10
            padded_watermark = Image.new('RGBA', 
                                       (watermark_size[0] + 2 * padding, watermark_size[1] + 2 * padding), 
                                       (255, 255, 255, 0))
            padded_watermark.paste(watermark, (padding, padding))
            padded_watermark = padded_watermark.convert("RGBA")
            width, height = image.size
            wm_width, wm_height = padded_watermark.size
            
            position_map = {
                'center': ((width - wm_width) // 2, (height - wm_height) // 2),
                'bottom_right': (width - wm_width, height - wm_height),
                'bottom_left': (0, height - wm_height),
                'top_right': (width - wm_width, 0),
                'top_left': (0, 0)
            }
            
            pos = position_map.get(position, position_map['center'])
            image.paste(padded_watermark, pos, padded_watermark)
        return image
        
    def resize_image(self, input_path, output_path, size, watermark_img=None, watermark_size=(128, 128), keep_aspect_ratio=True):
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
            img = self.add_watermark(img, watermark_img, 
                                   self.watermark_position_var.get(), 
                                   watermark_size=(int(self.watermark_width_var.get()), 
                                                 int(self.watermark_height_var.get())))
            
            # Apply optimization directly during save
            save_kwargs = {
                'format': self.format_var.get().upper(),
                'optimize': True
            }
            
            # Only add quality parameter for JPEG
            if self.format_var.get() == 'JPEG':
                save_kwargs['quality'] = self.quality_var.get()
            
            img.save(output_path, **save_kwargs)
            
            if not self.keep_metadata_var.get():
                self.remove_metadata(output_path)
                
    def remove_metadata(self, image_path):
        with Image.open(image_path) as img:
            if img.info:
                img.info.pop('exif', None)
            img.save(image_path)
            
    def optimize_image(self, input_path, output_path, quality=85):
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(output_path, optimize=True, quality=quality)
            
    def update_status(self, message, color=None):
        if color is None:
            color = self.colors['text_light']
        self.status_label.config(text=message, fg=color)
        
    def process_images_thread(self):
        input_path = self.input_path_var.get()
        output_dir = self.output_dir_var.get()
        watermark_path = self.watermark_path_var.get()
        
        if not os.path.isfile(input_path):
            self.root.after(0, lambda: messagebox.showerror("Error", "Please select a valid image file."))
            self.root.after(0, lambda: self.update_status("Error: Invalid input file", self.colors['warning']))
            return
            
        if not os.path.isdir(output_dir):
            self.root.after(0, lambda: messagebox.showerror("Error", "Please select a valid output directory."))
            self.root.after(0, lambda: self.update_status("Error: Invalid output directory", self.colors['warning']))
            return
            
        size_name = self.size_var.get()
        if size_name == 'Custom':
            size = (int(self.custom_width_var.get()), int(self.custom_height_var.get()))
        else:
            size = self.sizes[size_name]
            
        watermark_img = Image.open(watermark_path) if os.path.isfile(watermark_path) else None
        
        try:
            output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_{size_name}.{self.format_var.get().lower()}"
            output_path = os.path.join(output_dir, output_filename)
            
            self.root.after(0, lambda: self.update_status("Processing image...", self.colors['primary']))
            
            self.resize_image(input_path, output_path, size, watermark_img, 
                            watermark_size=(int(self.watermark_width_var.get()), 
                                          int(self.watermark_height_var.get())), 
                            keep_aspect_ratio=self.keep_aspect_ratio_var.get())
            
            self.root.after(0, lambda: messagebox.showinfo("Success", "Image processed successfully!"))
            self.root.after(0, lambda: self.update_status("✅ Processing completed!", self.colors['success']))
            self.root.after(0, self.enable_process_button)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
            self.root.after(0, lambda: self.update_status("❌ Processing failed", self.colors['warning']))
            self.root.after(0, self.enable_process_button)
            
    def start_image_processing(self):
        self.process_btn.config(text="⏳ Processing...", state='disabled')
        self.update_status("🚀 Starting image processing...", self.colors['primary'])
        threading.Thread(target=self.process_images_thread, daemon=True).start()
        
    def enable_process_button(self):
        self.process_btn.config(text="🎯 Process Images", state='normal')
        
    def preview_image(self):
        input_path = self.input_path_var.get()
        size_name = self.size_var.get()
        
        if not os.path.isfile(input_path):
            messagebox.showerror("Error", "Please select a valid image file.")
            return
            
        try:
            with Image.open(input_path) as img:
                # Determine new size based on the selected option
                if size_name == 'Custom':
                    size = (int(self.custom_width_var.get()), int(self.custom_height_var.get()))
                else:
                    size = self.sizes[size_name]
                    
                # Get original aspect ratio
                original_width, original_height = img.size
                original_aspect_ratio = original_width / original_height
                
                # Determine new size while maintaining aspect ratio
                new_width, new_height = size
                if self.keep_aspect_ratio_var.get():
                    new_aspect_ratio = new_width / new_height
                    if new_aspect_ratio > original_aspect_ratio:
                        new_width = int(new_height * original_aspect_ratio)
                    else:
                        new_height = int(new_width / original_aspect_ratio)
                
                img = img.resize((new_width, new_height), Image.LANCZOS)
                
                watermark_img = Image.open(self.watermark_path_var.get()) if os.path.isfile(self.watermark_path_var.get()) else None
                img = self.add_watermark(img, watermark_img, 
                                       self.watermark_position_var.get(), 
                                       watermark_size=(int(self.watermark_width_var.get()), 
                                                     int(self.watermark_height_var.get())))
                
                # Create thumbnail for preview
                img.thumbnail((320, 240), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                
                # Clear placeholder and show image
                for widget in self.preview_frame.winfo_children():
                    widget.destroy()
                    
                preview_label = tk.Label(self.preview_frame, 
                                       image=img_tk,
                                       bg=self.colors['card_bg'])
                preview_label.image = img_tk  # Keep a reference
                preview_label.pack(expand=True, pady=10)
                
                # Add image info
                info_label = tk.Label(self.preview_frame,
                                    text=f"Preview: {new_width}×{new_height}px",
                                    font=("Segoe UI", 8),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['text_light'])
                info_label.pack(pady=(0, 5))
                
                self.update_status("Preview updated", self.colors['success'])
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while previewing the image: {e}")
            self.update_status("Preview failed", self.colors['warning'])

def main():
    root = tk.Tk()
    root.resizable(True, True)
    root.minsize(900, 500)
    
    # Set modern window properties
    try:
        # Try to set the window icon and properties for Windows
        root.wm_attributes('-alpha', 0.98)  # Slight transparency for modern look
    except:
        pass
    
    app = ModernImageProcessor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
