import json
import re

class DetectedFrame:
    def __init__(self, path, algorithm, word, percentage, time):
        self.path = path  # Dirección del archivo
        self.algorithm = algorithm  # Algoritmo usado para detectar la imagen
        self.word = word  # Palabra utilizada para la detección
        self.percentage = percentage  # Porcentaje de asertividad en la detección
        self.time = self.get_time()  # Tiempo HH:MM:SS en el que se detectó

    def to_json(self):
        # Creamos un diccionario con los atributos de la clase
        data = {
            "path": self.path,
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
    # We divide the path into parts using the forward slash as a reference
        parts = self.path.split('/')

    # We take the las part of the path and separate the file name from the extension
        if parts:
            filenamepart = parts[-1]
            filename = filenamepart.split('.')[0]
            if (filename.isdigit()):
                return filename
            else:
                return "No valid time found in the text."
