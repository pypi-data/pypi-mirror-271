# NILM: Clasificador de Imágenes Utilizando Redes Neuronales Convolucionales

Este proyecto consiste en una clase de Python llamada NILM (Neural Network Image Classifier) diseñada para realizar predicciones sobre imágenes utilizando un modelo de red neuronal convolucional pre-entrenado. El propósito principal de esta clase es predecir y clasificar imágenes en una de las cuatro clases distintas.

## Uso

Para utilizar la clase NILM, sigue estos pasos:

1. **Instalación de dependencias:** Asegúrate de tener instaladas las siguientes dependencias:
   - Keras
   - numpy

2. **Importa la clase NILM:** En tu script de Python, importa la clase NILM desde el archivo que contiene su definición.

   from NILM import NILM

3. **Inicializa la clase NILM:** Carga el modelo de red neuronal convolucional pre-entrenado proporcionando la ruta al archivo del modelo como argumento.

    classifier = NILM("ruta/al/modelo.h5")

4. **Realiza predicciones:** Utiliza el método predict() para realizar predicciones sobre imágenes. Este método toma la ruta de la imagen como argumento y devuelve la clase predicha y la probabilidad asociada.

    clase_predicha, probabilidad = classifier.predict("ruta/a/la/imagen.jpg")
    print("Clase predicha:", clase_predicha)
    print("Probabilidad:", probabilidad)

**Clases Disponibles**
    
El modelo de red neuronal convolucional pre-entrenado está configurado para clasificar las imágenes en las siguientes cuatro clases:

DISH
FRIDGE
HTPC
KETTLE
WASHER

**Atributos y Métodos**

La clase NILM tiene los siguientes atributos y métodos:

model: El modelo de red neuronal cargado.
actual_classes: Lista de las clases actuales utilizadas para la predicción.

**Métodos:**

__init__(model_path): Inicializa la clase NILM cargando el modelo de red neuronal desde el archivo especificado.
predict(image_path): Realiza la predicción sobre la imagen en la ruta especificada y devuelve la clase predicha y la probabilidad asociada.


**Contribución**
Siéntete libre de contribuir a este proyecto añadiendo nuevas funcionalidades, corrigiendo errores o mejorando la documentación. ¡Toda ayuda es bienvenida!

**Licencia**
Este proyecto está bajo la licencia MIT.