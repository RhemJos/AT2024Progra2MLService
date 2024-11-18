import json
import re
from utils.file_utils import extract_filename
from utils.path_utils import normalize_path


class DetectedFrame:
    def __init__(self, path, algorithm, word, percentage, time):
        self.path = extract_filename(normalize_path(path))  # Dirección del archivo
        self.algorithm = algorithm  # Algoritmo usado para detectar la imagen
        self.word = word  # Palabra utilizada para la detección
        self.percentage = percentage  # Porcentaje de asertividad en la detección
        self.time = self.get_time()  # Tiempo HH:MM:SS en el que se detectó

    def to_json(self):
        # Creamos un diccionario con los atributos de la clase
        data = {
            "name": self.path,
            "algorithm": self.algorithm,
            "word": self.word,
            "percentage": self.percentage,
            "second": self.time
        }
        # Convertimos el diccionario a una cadena JSON
        return json.dumps(data, indent=4)

    def __str__(self):
        return (f"DetectedFrame(path={self.path}, algorithm={self.algorithm}, "
                f"word={self.word}, percentage={self.percentage}%, "
                f"second={self.time})")

    def get_time(self) -> str:
        # Dividimos el path por '/' para obtener el nombre del archivo
        parts = self.path.split('/')

        # Tomamos la última parte (nombre del archivo) y separamos la extensión
        if parts:
            filename = parts[-1].split('.')[0]

            # Si el nombre del archivo es un número, lo devolvemos como tiempo
            if filename.isdigit():
                return filename
            else:
                return "No valid time found in the text."
        return "No valid time found in the text."
