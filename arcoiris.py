# Aplicación gráfica para sustituir el color negro por el arcoíris en una imagen.
# El arcoíris se dibujará en gradiente con capacidad para millones de colores.
# Esta aplicación utiliza Tkinter para la interfaz gráfica y PIL para el procesamiento de imágenes.

from tkinter import Tk, Frame, Button, Label, Scale, Canvas, LabelFrame, TOP, BOTTOM, LEFT, RIGHT, X, BOTH, HORIZONTAL, CENTER, NORMAL, DISABLED
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
from PIL import ImageFont, ImagePalette
from PIL import Image, ImageFont, ImagePalette, ImageDraw
import os
import sys
import numpy as np


# Clase principal de la aplicación Arcoiris
class ArcoirisApp:
    def __init__(self, root):
        # Inicializa la aplicación con la ventana raíz
        self.root = root
        self.root.title("Arcoiris - Reemplazar Negro por Arcoiris")
        self.root.geometry("1000x600")

        self.original_image = None  # Imagen original cargada
        self.processed_image = None  # Imagen procesada con arcoíris
        self.threshold = 30  # Umbral por defecto para detectar negro

        self.create_widgets()  # Crear los widgets de la interfaz

    def create_widgets(self):
        # Crea y configura todos los widgets de la interfaz gráfica
        # Frame para los botones
        button_frame = Frame(self.root)
        button_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        # Botón para cargar imagen
        self.load_button = Button(
            button_frame, text="Cargar Imagen", command=self.load_image
        )
        self.load_button.pack(side=LEFT, padx=5)

        # Botón para procesar la imagen
        self.process_button = Button(
            button_frame, text="Procesar", command=self.process_image, state=DISABLED
        )
        self.process_button.pack(side=LEFT, padx=5)

        # Botón para guardar la imagen procesada
        self.save_button = Button(
            button_frame, text="Guardar", command=self.save_image, state=DISABLED
        )
        self.save_button.pack(side=LEFT, padx=5)

        # Etiqueta y slider para el umbral de negro
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

        # Área de visualización de imágenes
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame para la imagen original
        self.original_frame = LabelFrame(self.canvas_frame, text="Imagen Original")
        self.original_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.original_canvas = Canvas(self.original_frame, bg="gray90")
        self.original_canvas.pack(fill=BOTH, expand=True)

        # Frame para la imagen procesada
        self.processed_frame = LabelFrame(self.canvas_frame, text="Imagen Procesada")
        self.processed_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
        self.processed_canvas = Canvas(self.processed_frame, bg="gray90")
        self.processed_canvas.pack(fill=BOTH, expand=True)

    def load_image(self):
        # Carga una imagen desde el disco duro usando un diálogo de archivos
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )

        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.original_canvas)
            self.process_button.config(state=NORMAL)
            self.process_image()  # Procesar automáticamente al cargar

    def display_image(self, image, canvas):
        # Muestra una imagen en el canvas especificado, redimensionándola para que quepa
        canvas.delete("all")

        # Obtener dimensiones del canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1:  # Canvas no realizado aún
            canvas_width = 400
            canvas_height = 400

        img_width, img_height = image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        # Almacenar referencia para evitar recolección de basura
        canvas.image = photo
        canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=photo, anchor=CENTER
        )

    def update_threshold(self, val):
        # Actualiza el umbral de detección de negro y reprocesa la imagen si existe
        self.threshold = int(val)
        if self.original_image:
            self.process_image()

    def create_rainbow_gradient(self, width, height):
        # Crea una imagen de gradiente de arcoíris horizontal
        rainbow = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(rainbow)

        # Colores del arcoíris (rojo, naranja, amarillo, verde, azul, índigo, violeta)
        colors = [
            (255, 0, 0),  # Rojo
            (255, 127, 0),  # Naranja
            (255, 255, 0),  # Amarillo
            (0, 255, 0),  # Verde
            (0, 0, 255),  # Azul
            (75, 0, 130),  # Índigo
            (148, 0, 211),  # Violeta
        ]

        # Dibujar gradiente horizontal
        for i in range(width):
            # Calcular color basado en la posición
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
        # Procesa la imagen reemplazando píxeles negros con colores del arcoíris
        if self.original_image:
            # Convertir imagen a array de numpy para procesamiento
            img_array = np.array(self.original_image.convert("RGB"))

            # Crear máscara para píxeles negros
            black_mask = np.all(img_array < self.threshold, axis=2)

            # Crear gradiente de arcoíris
            rainbow = self.create_rainbow_gradient(self.original_image.width, 1)
            rainbow_array = np.array(rainbow)

            # Crear imagen de salida
            result_array = img_array.copy()

            # Reemplazar píxeles negros con colores del arcoíris basados en la posición x
            for y in range(img_array.shape[0]):
                for x in range(img_array.shape[1]):
                    if black_mask[y, x]:
                        result_array[y, x] = rainbow_array[0, x % rainbow.width]

            # Convertir de vuelta a imagen PIL
            self.processed_image = Image.fromarray(result_array)
            self.display_image(self.processed_image, self.processed_canvas)
            self.save_button.config(state=NORMAL)

    def save_image(self):
        # Guarda la imagen procesada en el disco duro usando un diálogo de guardar
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
    # Punto de entrada principal del programa
    root = Tk()
    app = ArcoirisApp(root)

    # Actualizar canvas al redimensionar la ventana
    def on_resize(event):
        if app.original_image:
            app.display_image(app.original_image, app.original_canvas)
        if app.processed_image:
            app.display_image(app.processed_image, app.processed_canvas)

    app.original_canvas.bind("<Configure>", on_resize)
    app.processed_canvas.bind("<Configure>", on_resize)

    # Iniciar el bucle principal de eventos
    root.mainloop()

