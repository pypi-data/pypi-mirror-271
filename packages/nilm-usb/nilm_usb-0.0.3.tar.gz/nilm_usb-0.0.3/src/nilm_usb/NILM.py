from keras.models import load_model
import numpy as np
from keras.applications.mobilenet_v2 import preprocess_input
from keras.utils import img_to_array
from keras.utils import load_img
import sys

class NILM:
    """
    Clase para realizar predicciones utilizando un modelo de red neuronal convolucional pre-entrenado.

    Attributes:
        model (keras.Model): El modelo de red neuronal cargado.
        actual_classes (list): Lista de las clases actuales utilizadas para la predicción.

    Methods:
        __init__(model_path):
            Inicializa la clase NILM cargando el modelo de red neuronal desde el archivo especificado.

        __loadmodel(model_path):
            Método privado para cargar el modelo de red neuronal desde el archivo especificado.

        __preprocessimage(image):
            Método privado para preprocesar la imagen antes de realizar la predicción.

        predict(image_path):
            Realiza la predicción sobre la imagen en la ruta especificada y devuelve la clase predicha y la probabilidad asociada.
    """

    model = None
    actual_classes = ["DISH", "FRIDGE", "HTPC", "KETTLE", "WASHER"]

    def __init__(self, model_path):
        """
        Inicializa la clase NILM cargando el modelo de red neuronal desde el archivo especificado.

        Args:
            model_path (str): La ruta al archivo que contiene el modelo de red neuronal.

        Returns:
            None
        """
        self.__loadmodel(model_path)

    def __loadmodel(self, model_path):
        """
        Método privado para cargar el modelo de red neuronal desde el archivo especificado.

        Args:
            model_path (str): La ruta al archivo que contiene el modelo de red neuronal.

        Returns:
            None
        """
        try:
            self.model = load_model(model_path)
        except Exception as e:
            print(f"ERROR LOADING MODEL - {str(e)}")
            sys.exit()

    def __preprocessimage(self, image):
        """
        Método privado para preprocesar la imagen antes de realizar la predicción.

        Args:
            image (str): La ruta de la imagen a preprocesar.

        Returns:
            numpy.ndarray: La imagen preprocesada como un array numpy.
        """
        try:
            image = load_img(image)
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            return image
        except Exception as e:
            print(f"ERROR WITH IMAGE - {str(e)}")
            sys.exit()

    def predict(self, image_path):
        """
        Realiza la predicción sobre la imagen en la ruta especificada y devuelve la clase predicha y la probabilidad asociada.

        Args:
            image_path (str): La ruta de la imagen sobre la que realizar la predicción.

        Returns:
            tuple: Una tupla que contiene la clase predicha y la probabilidad asociada.
        """
        img = self.__preprocessimage(image_path)
        try:
            preds = self.model.predict(img)
            result_index = np.argmax(preds[0])
            result_class = self.actual_classes[result_index]
            return result_class, preds[0][result_index]
        except Exception as e:
            print(f"ERROR - {str(e)}")
            return f"ERROR - {str(e)}"