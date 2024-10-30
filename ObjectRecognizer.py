from Recognizer import Recognizer
from ultralytics import YOLO
import cv2
import json


class ObjectRecognizer(Recognizer):

    def __init__(self, model: str, model_path: str):
        super().__init__(model=model, model_path=model_path)
        self.loaded_model = None
        self.results = None
        self.yolo_labels = self.load_labels("classes.json")

    def load_model(self):
        if self.model.lower() == "yolo":
            self.loaded_model = YOLO(self.model_path)

        elif self.model.lower() == "mobilenet":
            self.loaded_model = cv2.dnn.readNetFromCaffe(self.model_path+'deploy.prototxt',
                                                         self.model_path+'mobilenet_iter_73000.caffemodel')

        else:
            raise ValueError(f"Modelo {self.model} no soportado o no reconocido.")

    def recognize(self, input_image: str, confidence_threshold: float = 0.1, word: str = 'person'):
        if not self.loaded_model:
            raise Exception("El modelo no ha sido cargado.")

        if self.model.lower() == "yolo":
            self.results = self.loaded_model.predict(source=input_image, conf=confidence_threshold,
                                                     classes=[self.get_word_id(word)])
            for result in self.results:
                result.show()
        elif self.model.lower() == "mobilenet":
            pass
        else:
            raise ValueError(f"Modelo '{self.model}' no soportado para reconocimiento.")

    def get_confidence(self):
        pass

    def load_labels(self, labels_path: str):
        with open(labels_path, 'r') as file:
            return json.load(file)

    def get_word_id(self, target_word: str):
        for id, label in self.yolo_labels.items():
            if label == target_word.lower():
                return int(id)
        raise ValueError(f"La palabra clave '{target_word}' no está en la lista de etiquetas.")

