 # El objetivo principal de la aplicación arcoiris.py es reemplazar los colores negros de una imagen con un degradado arcoíris. En concreto, permite:

# Cargar una imagen.
Identificar los píxeles "negros" (según un umbral ajustable).
Reemplazar esos píxeles negros con colores de un degradado arcoíris horizontal.
Mostrar la imagen original y la procesada en paralelo, seleccionando el umbral de color negro.
Guardar la imagen procesada.


# La aplicación procesa imágenes para reemplazar el negro con los colores del arcoíris mediante estos pasos clave:

# 1. Detección de píxeles negros:
Convierte la imagen en una matriz NumPy.
Crea una máscara que identifica los píxeles donde todos los valores RGB están por debajo del umbral.
El umbral se ajusta mediante un control deslizante (predeterminado: 30).

# 2. Creación de degradado arcoíris:
Crea un degradado arcoíris horizontal con el mismo ancho que la imagen.
Utiliza 7 colores (rojo, naranja, amarillo, verde, azul, índigo y violeta).
Interpola entre colores para crear un degradado suave.

# 3.Reemplazo de píxeles:
Recorre cada píxel de la imagen.
Para los píxeles identificados como "negros" en la máscara, los reemplaza con el color del arcoíris en la posición x correspondiente.
Esto crea un efecto arcoíris horizontal donde había áreas negras.

# 4.Implementación del procesamiento:
    
# Crear una máscara para píxeles negros
    black_mask = np.all(img_array < self.threshold, axis=2)

# Reemplazar los píxeles negros con los colores del arcoíris según la posición x
        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                if black_mask[y, x]:
                    result_array[y, x] = rainbow_array[0, x % rainbow.width]


El resultado es una imagen donde las áreas negras se transforman en vibrantes patrones de arcoíris que siguen la posición horizontal de los píxeles negros originales.



# Componentes clave de la interfaz de usuario e interacciones del usuario en la aplicación:

# Botones principales:
Cargar imagen: Abre el cuadro de diálogo de archivo para seleccionar una imagen
Procesar: Aplica el efecto arcoíris (se activa tras cargar la imagen)
Guardar: Guarda la imagen procesada (se activa tras el procesamiento)

# Control de umbral:
Control deslizante "Umbral Negro"
Ajusta la sensibilidad para lo que se considera "negro" (0-100)
Los cambios se aplican inmediatamente y actualizan la imagen procesada

# Áreas de visualización de la imagen:
Dos lienzos contiguos en marcos etiquetados
Izquierda: "Imagen original"
Derecha: "Imagen procesada"
Las imágenes se redimensionan automáticamente para ajustarse al lienzo, manteniendo la relación de aspecto

# Flujo de trabajo del usuario:
Cargar una imagen con el botón de carga
La imagen se procesa y se muestra automáticamente
Ajustar el control deslizante de umbral para ajustar la detección de negro
Guardar la imagen procesada con el botón de guardar

# Responsivo Diseño:
Las imágenes se redimensionan al redimensionar la ventana.
Enlace de eventos: app.original_canvas.bind("<Configure>", on_resize)
La
interfaz es sencilla e intuitiva, centrada en la transformación de la imagen, con mínimos controles para que el usuario logre el efecto deseado.
