# aplicación gráfica para sustituir el color negro por el arcoiris en una imágen. El arcoiris se dibujará en gradiente con capacidad para millones de colores.

from tkinter import Tk, Frame, Button, Label, Scale, Canvas, LabelFrame, TOP, BOTTOM, LEFT, RIGHT, X, BOTH, HORIZONTAL, CENTER, NORMAL, DISABLED
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
from PIL import ImageFont, ImagePalette
from PIL import Image, ImageFont, ImagePalette, ImageDraw
import os
import sys
import numpy as np


class ArcoirisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arcoiris - Reemplazar Negro por Arcoiris")
        self.root.geometry("1000x600")

        self.original_image = None
        self.processed_image = None
        self.threshold = 30  # Default threshold for black detection

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = Frame(self.root)
        button_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        # Load image button
        self.load_button = Button(
            button_frame, text="Cargar Imagen", command=self.load_image
        )
        self.load_button.pack(side=LEFT, padx=5)

        # Process image button
        self.process_button = Button(
            button_frame, text="Procesar", command=self.process_image, state=DISABLED
        )
        self.process_button.pack(side=LEFT, padx=5)

        # Save image button
        self.save_button = Button(
            button_frame, text="Guardar", command=self.save_image, state=DISABLED
        )
        self.save_button.pack(side=LEFT, padx=5)

        # Threshold slider
        Label(button_frame, text="Umbral Negro:").pack(side=LEFT, padx=(20, 5))
        self.threshold_slider = Scale(
            button_frame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            command=self.update_threshold,
        )
        self.threshold_slider.set(self.threshold)
        self.threshold_slider.pack(side=LEFT, padx=5)

        # Image display area
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Original image
        self.original_frame = LabelFrame(self.canvas_frame, text="Imagen Original")
        self.original_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.original_canvas = Canvas(self.original_frame, bg="gray90")
        self.original_canvas.pack(fill=BOTH, expand=True)

        # Processed image
        self.processed_frame = LabelFrame(self.canvas_frame, text="Imagen Procesada")
        self.processed_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
        self.processed_canvas = Canvas(self.processed_frame, bg="gray90")
        self.processed_canvas.pack(fill=BOTH, expand=True)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )

        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.original_canvas)
            self.process_button.config(state=NORMAL)
            self.process_image()

    def display_image(self, image, canvas):
        canvas.delete("all")

        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1:  # Canvas not yet realized
            canvas_width = 400
            canvas_height = 400

        img_width, img_height = image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        # Store reference to prevent garbage collection
        canvas.image = photo
        canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=photo, anchor=CENTER
        )

    def update_threshold(self, val):
        self.threshold = int(val)
        if self.original_image:
            self.process_image()

    def create_rainbow_gradient(self, width, height):
        # Create rainbow gradient image
        rainbow = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(rainbow)

        # Rainbow colors (red, orange, yellow, green, blue, indigo, violet)
        colors = [
            (255, 0, 0),  # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (75, 0, 130),  # Indigo
            (148, 0, 211),  # Violet
        ]

        # Draw horizontal gradient
        for i in range(width):
            # Calculate color based on position
            idx = (i / width) * (len(colors) - 1)
            idx_floor = int(idx)
            idx_ceil = min(idx_floor + 1, len(colors) - 1)
            fraction = idx - idx_floor

            r = int(
                colors[idx_floor][0] * (1 - fraction) + colors[idx_ceil][0] * fraction
            )
            g = int(
                colors[idx_floor][1] * (1 - fraction) + colors[idx_ceil][1] * fraction
            )
            b = int(
                colors[idx_floor][2] * (1 - fraction) + colors[idx_ceil][2] * fraction
            )

            draw.line([(i, 0), (i, height)], fill=(r, g, b))

        return rainbow

    def process_image(self):
        if self.original_image:
            # Convert image to numpy array for processing
            img_array = np.array(self.original_image.convert("RGB"))

            # Create a mask for black pixels
            black_mask = np.all(img_array < self.threshold, axis=2)

            # Create rainbow gradient
            rainbow = self.create_rainbow_gradient(self.original_image.width, 1)
            rainbow_array = np.array(rainbow)

            # Create output image
            result_array = img_array.copy()

            # Replace black pixels with rainbow colors based on x-position
            for y in range(img_array.shape[0]):
                for x in range(img_array.shape[1]):
                    if black_mask[y, x]:
                        result_array[y, x] = rainbow_array[0, x % rainbow.width]

            # Convert back to PIL Image
            self.processed_image = Image.fromarray(result_array)
            self.display_image(self.processed_image, self.processed_canvas)
            self.save_button.config(state=NORMAL)

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*"),
                ],
            )

            if file_path:
                self.processed_image.save(file_path)


if __name__ == "__main__":
    root = Tk()
    app = ArcoirisApp(root)

    # Update canvas when window is resized
    def on_resize(event):
        if app.original_image:
            app.display_image(app.original_image, app.original_canvas)
        if app.processed_image:
            app.display_image(app.processed_image, app.processed_canvas)

    app.original_canvas.bind("<Configure>", on_resize)
    app.processed_canvas.bind("<Configure>", on_resize)

    # Start the main event loop
    root.mainloop()

