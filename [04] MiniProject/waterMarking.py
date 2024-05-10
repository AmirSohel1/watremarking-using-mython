import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.geometry("1200x800")
        self.root.configure(bg="light green")

        self.image_path = None
        self.original_img = None
        self.watermarked_img = None
        self.watermark_text = tk.StringVar()
        self.watermark_color = tk.StringVar()
        self.watermark_size = tk.IntVar(value=36)
        self.watermark_position = tk.StringVar(value="Bottom Right")
        self.bold_var = tk.BooleanVar(value=False)
        self.visibility_scale = tk.DoubleVar(value=1.0)
        self.tilt_angle = tk.IntVar(value=0)

        self.create_widgets()

    def create_widgets(self):
        # Frame to contain all widgets
        self.main_frame = tk.Frame(self.root, bg="light green")
        self.main_frame.pack(expand=True, fill="both")

        # Frame for watermark options
        self.watermark_options_frame = tk.Frame(self.main_frame, bg="light green")
        self.watermark_options_frame.pack(side="top", padx=10, pady=10)

        # Entry for watermark text
        watermark_text_label = tk.Label(self.watermark_options_frame, text="Watermark Text:", bg="light green")
        watermark_text_label.grid(row=0, column=0, padx=5, pady=5)
        self.watermark_text_entry = tk.Entry(self.watermark_options_frame, textvariable=self.watermark_text)
        self.watermark_text_entry.grid(row=0, column=1, padx=5, pady=5)

        # Entry for watermark text size
        watermark_size_label = tk.Label(self.watermark_options_frame, text="Text Size:", bg="light green")
        watermark_size_label.grid(row=0, column=2, padx=5, pady=5)
        self.watermark_size_entry = tk.Entry(self.watermark_options_frame, textvariable=self.watermark_size)
        self.watermark_size_entry.grid(row=0, column=3, padx=5, pady=5)

        # Checkbutton for text bold
        self.bold_checkbox = tk.Checkbutton(self.watermark_options_frame, text="Bold", variable=self.bold_var, bg="light green")
        self.bold_checkbox.grid(row=0, column=4, padx=5, pady=5)

        # Button to pick watermark color
        self.watermark_color_button = tk.Button(self.watermark_options_frame, text="Choose Color", command=self.choose_color)
        self.watermark_color_button.grid(row=0, column=5, padx=5, pady=5)

        # Button to open an image
        open_button = tk.Button(self.watermark_options_frame, text="Open Image", command=self.open_image)
        open_button.grid(row=0, column=6, padx=5, pady=5)

        # Option menu to choose watermark position
        watermark_position_label = tk.Label(self.watermark_options_frame, text="Watermark Position:", bg="light green")
        watermark_position_label.grid(row=1, column=0, padx=5, pady=5)
        positions = ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center"]
        self.watermark_position_menu = tk.OptionMenu(self.watermark_options_frame, self.watermark_position, *positions)
        self.watermark_position_menu.grid(row=1, column=1, padx=5, pady=5)

        # Entry for tilt angle
        tilt_angle_label = tk.Label(self.watermark_options_frame, text="Tilt Angle:", bg="light green")
        tilt_angle_label.grid(row=1, column=2, padx=5, pady=5)
        self.tilt_angle_entry = tk.Entry(self.watermark_options_frame, textvariable=self.tilt_angle)
        self.tilt_angle_entry.grid(row=1, column=3, padx=5, pady=5)

        # Scale for visibility strength
        visibility_scale_label = tk.Label(self.watermark_options_frame, text="Visibility:", bg="light green")
        visibility_scale_label.grid(row=1, column=4, padx=5, pady=5)
        self.visibility_scale = tk.Scale(self.watermark_options_frame, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.visibility_scale.grid(row=1, column=5, padx=5, pady=5)

        # Button to apply watermark
        apply_button = tk.Button(self.watermark_options_frame, text="Apply Watermark", command=self.apply_watermark)
        apply_button.grid(row=1, column=6, padx=5, pady=5)

        # Button to save watermarked image
        save_button = tk.Button(self.watermark_options_frame, text="Save Watermark", command=self.save_watermark)
        save_button.grid(row=1, column=7, padx=5, pady=5)

        # Frame for image display
        self.image_frame = tk.Frame(self.main_frame, bg="light green")
        self.image_frame.pack(side="bottom", padx=10, pady=10)

        # Label to display the original image
        self.img_label = tk.Label(self.image_frame, bg="light green")
        self.img_label.pack(side="left")

        # Label to display the watermarked image
        self.watermark_label = tk.Label(self.image_frame, bg="light green")
        self.watermark_label.pack(side="right")

    def open_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.original_img = Image.open(self.image_path)
            self.original_img = self.original_img.resize((500, 500), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(self.original_img)
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.watermark_color.set(color)

    def apply_watermark(self):
        self.watermark_text_value = self.watermark_text.get()
        self.watermark_color_value = self.watermark_color.get()
        self.watermark_size_value = self.watermark_size.get()
        if self.watermark_text_value and self.watermark_color_value and self.watermark_size_value and self.original_img:
            font = ImageFont.truetype("arial.ttf", self.watermark_size_value)
            if self.bold_var.get():
                font = ImageFont.truetype("arialbd.ttf", self.watermark_size_value)
            watermarked_img = self.original_img.copy()
            draw = ImageDraw.Draw(watermarked_img)
            width, height = watermarked_img.size
            margin = 10

            if self.watermark_position.get() == "Top Left":
                position = (margin, margin)
            elif self.watermark_position.get() == "Top Right":
                position = (width - margin, margin)
            elif self.watermark_position.get() == "Bottom Left":
                position = (margin, height - margin)
            elif self.watermark_position.get() == "Bottom Right":
                position = (width - margin, height - margin)
            elif self.watermark_position.get() == "Center":
                position = ((width - margin) // 2, (height - margin) // 2)

            draw.text(position, self.watermark_text_value, fill=self.watermark_color_value, font=font)
            watermarked_img = self.apply_visibility(watermarked_img)
            watermarked_img_tk = ImageTk.PhotoImage(watermarked_img)
            self.watermark_label.config(image=watermarked_img_tk)
            self.watermark_label.image = watermarked_img_tk
            self.watermarked_img = watermarked_img
        else:
            messagebox.showerror("Error", "Please fill all the fields and open an image first.")

    def apply_visibility(self, image):
        alpha = self.visibility_scale.get()
        if alpha < 1.0:
            overlay = Image.new("RGBA", image.size, (255, 255, 255, int(255 * (1 - alpha))))
            image = Image.alpha_composite(image.convert("RGBA"), overlay)
        return image

    def save_watermark(self):
        if self.watermarked_img:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                self.watermarked_img.save(save_path)
                messagebox.showinfo("Watermark Saved", "Watermarked image saved successfully!")
        else:
            messagebox.showerror("Error", "No watermarked image to save. Please apply watermark first.")

root = tk.Tk()
app = WatermarkApp(root)
root.mainloop()
