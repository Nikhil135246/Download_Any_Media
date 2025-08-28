from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
import subprocess

class IconPreview:
    def __init__(self, root):
        self.root = root
        self.root.title("Icon Preview & Converter")
        self.root.geometry("1000x700")
        
        # Variables
        self.current_image = None
        self.preview_images = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main canvas and scrollbar for the entire content
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure the scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window in canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas only when mouse is over the main area
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse enter/leave events to the main canvas
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Main content frame (now inside scrollable frame)
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # File selection
        ttk.Label(main_frame, text="Select Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.file_var = tk.StringVar()
        file_combo = ttk.Combobox(main_frame, textvariable=self.file_var, width=40)
        file_combo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Populate with available images
        icon_folder = "icon"
        if os.path.exists(icon_folder):
            image_files = [f for f in os.listdir(icon_folder) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico'))]
            file_combo['values'] = image_files
            if image_files:
                file_combo.set(image_files[0])
        
        ttk.Button(main_frame, text="Load Preview", 
                  command=self.load_preview).grid(row=0, column=2, padx=5)
        
        # Resize options
        ttk.Label(main_frame, text="Resize Method:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.resize_var = tk.StringVar(value="contain")
        resize_frame = ttk.Frame(main_frame)
        resize_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(resize_frame, text="Contain (fit inside)", 
                       variable=self.resize_var, value="contain").pack(side=tk.LEFT)
        ttk.Radiobutton(resize_frame, text="Cover (fill area)", 
                       variable=self.resize_var, value="cover").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(resize_frame, text="Stretch", 
                       variable=self.resize_var, value="stretch").pack(side=tk.LEFT)
        
        # Background color for transparent areas
        ttk.Label(main_frame, text="Background Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.bg_var = tk.StringVar(value="white")
        bg_frame = ttk.Frame(main_frame)
        bg_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(bg_frame, text="White", 
                       variable=self.bg_var, value="white").pack(side=tk.LEFT)
        ttk.Radiobutton(bg_frame, text="Black", 
                       variable=self.bg_var, value="black").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(bg_frame, text="Transparent", 
                       variable=self.bg_var, value="transparent").pack(side=tk.LEFT)
        
        # Update button
        ttk.Button(main_frame, text="Update Preview", 
                  command=self.update_preview).grid(row=3, column=1, pady=10)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Icon Preview (Different Sizes)", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Create preview labels for different sizes
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
        self.preview_labels = {}
        
        for i, size in enumerate(sizes):
            frame = ttk.Frame(preview_frame)
            frame.grid(row=0, column=i, padx=10, pady=5)
            
            ttk.Label(frame, text=f"{size[0]}x{size[1]}").pack()
            
            # Create a canvas with border to show the exact icon size
            canvas_preview = tk.Canvas(frame, width=size[0]+4, height=size[1]+4, 
                             relief="solid", borderwidth=1, bg="white")
            canvas_preview.pack(pady=5)
            
            # Prevent scroll events on preview canvases
            def _prevent_scroll(event):
                return "break"
            canvas_preview.bind("<MouseWheel>", _prevent_scroll)
            
            # Store both canvas and a label for the image
            label = ttk.Label(frame)
            self.preview_labels[size] = {'canvas': canvas_preview, 'label': label}
        
        # Original image preview
        original_frame = ttk.LabelFrame(main_frame, text="Original Image", padding="10")
        original_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.original_label = ttk.Label(original_frame)
        self.original_label.pack()
        
        # Information text
        info_frame = ttk.LabelFrame(main_frame, text="Tips", padding="10")
        info_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        info_text = ttk.Label(info_frame, text=(
            "• Contain: Best for logos - keeps proportions, adds background if needed\n"
            "• Cover: Fills entire icon area - may crop parts of the image\n"
            "• Stretch: May distort the image but uses full icon area\n"
            "• Use white background for dark icons, black for light icons"), 
            justify=tk.LEFT, wraplength=800)
        info_text.pack(anchor="w")
        
        # Convert button
        convert_frame = ttk.Frame(main_frame)
        convert_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        ttk.Button(convert_frame, text="Convert to ICO", 
                  command=self.convert_to_ico).pack(side=tk.LEFT, padx=5)
        ttk.Button(convert_frame, text="Apply to Executable", 
                  command=self.apply_to_exe).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)
        
        # Bind resize method change
        self.resize_var.trace('w', lambda *args: self.update_preview())
        self.bg_var.trace('w', lambda *args: self.update_preview())
        
    def load_preview(self):
        if not self.file_var.get():
            messagebox.showerror("Error", "Please select an image file")
            return
            
        try:
            image_path = os.path.join("icon", self.file_var.get())
            self.current_image = Image.open(image_path)
            
            # Show original image (scaled down if too large)
            original = self.current_image.copy()
            if original.width > 300 or original.height > 300:
                original.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            original_tk = ImageTk.PhotoImage(original)
            self.original_label.configure(image=original_tk)
            self.original_label.image = original_tk
            
            self.status_label.config(text=f"Loaded: {self.file_var.get()} ({self.current_image.width}x{self.current_image.height})")
            self.update_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            self.status_label.config(text="Error loading image")
    
    def resize_image(self, image, size):
        """Resize image based on selected method"""
        method = self.resize_var.get()
        
        if method == "stretch":
            return image.resize(size, Image.Resampling.LANCZOS)
        
        elif method == "contain":
            # Fit image inside the size while maintaining aspect ratio
            img_copy = image.copy()
            img_copy.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Create new image with background
            if self.bg_var.get() == "transparent":
                new_img = Image.new("RGBA", size, (0, 0, 0, 0))
            else:
                color = (255, 255, 255) if self.bg_var.get() == "white" else (0, 0, 0)
                new_img = Image.new("RGBA", size, color + (255,))
            
            # Paste the resized image in the center
            x = (size[0] - img_copy.width) // 2
            y = (size[1] - img_copy.height) // 2
            
            if img_copy.mode == "RGBA":
                new_img.paste(img_copy, (x, y), img_copy)
            else:
                new_img.paste(img_copy, (x, y))
            
            return new_img
        
        elif method == "cover":
            # Fill the entire area, cropping if necessary
            img_ratio = image.width / image.height
            target_ratio = size[0] / size[1]
            
            if img_ratio > target_ratio:
                # Image is wider, scale by height
                new_height = size[1]
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller, scale by width
                new_width = size[0]
                new_height = int(new_width / img_ratio)
            
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to fit
            x = (new_width - size[0]) // 2
            y = (new_height - size[1]) // 2
            return resized.crop((x, y, x + size[0], y + size[1]))
    
    def update_preview(self):
        if not self.current_image:
            return
            
        try:
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
            
            for size in sizes:
                # Convert to RGBA if needed
                img = self.current_image.convert("RGBA")
                resized = self.resize_image(img, size)
                
                # Clear the canvas
                canvas = self.preview_labels[size]['canvas']
                canvas.delete("all")
                
                # Convert to PhotoImage for display
                preview_tk = ImageTk.PhotoImage(resized)
                
                # Draw on canvas at exact position
                canvas.create_image(2, 2, anchor=tk.NW, image=preview_tk)
                canvas.image = preview_tk  # Keep reference
                
            self.status_label.config(text=f"Preview updated - Method: {self.resize_var.get()}, Background: {self.bg_var.get()}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not update preview: {e}")
            self.status_label.config(text="Error updating preview")
    
    def convert_to_ico(self):
        if not self.current_image:
            messagebox.showerror("Error", "Please load an image first")
            return
            
        try:
            # Create ICO with multiple sizes
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            
            # Convert to RGBA
            img = self.current_image.convert("RGBA")
            
            # Create images for all sizes using the current settings
            ico_images = []
            for size in sizes:
                resized = self.resize_image(img, size)
                ico_images.append(resized)
            
            # Save as ICO
            filename = os.path.splitext(self.file_var.get())[0]
            output_path = os.path.join("icon", f"{filename}.ico")
            
            # Save the first image with all sizes
            ico_images[0].save(output_path, format='ICO', sizes=sizes)
            
            self.status_label.config(text=f"Icon saved as {output_path}")
            messagebox.showinfo("Success", f"Icon saved as {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not convert to ICO: {e}")
            self.status_label.config(text="Error converting to ICO")
    
    def apply_to_exe(self):
        if not self.current_image:
            messagebox.showerror("Error", "Please load an image first")
            return
            
        try:
            # First convert to ICO
            self.convert_to_ico()
            
            # Update the spec file
            filename = os.path.splitext(self.file_var.get())[0]
            icon_path = f"icon/{filename}.ico"
            
            # Read the spec file
            spec_path = "YouTube-Downloader.spec"
            if not os.path.exists(spec_path):
                messagebox.showerror("Error", f"Spec file not found: {spec_path}")
                return
            
            with open(spec_path, 'r') as f:
                content = f.read()
            
            # Update the icon parameter
            # Look for existing icon parameter
            if "icon=" in content:
                content = re.sub(r"icon='[^']*'", f"icon='{icon_path}'", content)
                content = re.sub(r'icon="[^"]*"', f'icon="{icon_path}"', content)
            else:
                # Add icon parameter before the closing parenthesis of EXE
                content = re.sub(
                    r"(\s+entitlements_file=None,?\s*)\)",
                    f"\\1\n    icon='{icon_path}',\n)",
                    content
                )
            
            # Write back the spec file
            with open(spec_path, 'w') as f:
                f.write(content)
            
            self.status_label.config(text="Spec file updated")
            
            # Ask if user wants to rebuild
            if messagebox.askyesno("Rebuild", "Icon updated in spec file. Do you want to rebuild the executable now?\n\nThis may take a few minutes."):
                self.status_label.config(text="Building executable... Please wait")
                self.root.update()
                
                try:
                    result = subprocess.run(["pyinstaller", spec_path], 
                                          capture_output=True, text=True, cwd=os.getcwd())
                    
                    if result.returncode == 0:
                        self.status_label.config(text="Executable rebuilt successfully!")
                        messagebox.showinfo("Success", "Executable rebuilt successfully with new icon!\n\nCheck the 'dist' folder for your updated executable.")
                    else:
                        self.status_label.config(text="Build failed")
                        messagebox.showerror("Build Error", f"Build failed. Error details:\n\n{result.stderr[:500]}...")
                except FileNotFoundError:
                    messagebox.showerror("Error", "PyInstaller not found. Please make sure it's installed:\npip install pyinstaller")
                    self.status_label.config(text="PyInstaller not found")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply to executable: {e}")
            self.status_label.config(text="Error applying to executable")

if __name__ == "__main__":
    root = tk.Tk()
    app = IconPreview(root)
    root.mainloop()
