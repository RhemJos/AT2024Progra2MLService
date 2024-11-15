#
# @ObjectRecognizer.py Copyright (c) 2021 Jalasoft. # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
from .Recognizer import Recognizer
from ultralytics import YOLO
from .DetectedFrame import DetectedFrame
import os
import json


class ObjectRecognizerYolo(Recognizer):

    def __init__(self):
        super().__init__()
        self.model_path = os.path.join(os.getcwd(), "yolo11n.pt")
        self.loaded_model = None
        self.load_model()
        self.yolo_labels = self.load_labels(os.path.join(os.getcwd(), "models/Recognizer/classes_yolo.json"))
        self.results = None

    def recognize(self, image_path: str, confidence_threshold: float = 0.1, word: str = None):
        if word is None:
            raise ValueError("The 'word' parameter is required.")

        # Ejecutamos la predicción del modelo para la palabra especificada
        self.results = self.loaded_model.predict(source=image_path, conf=confidence_threshold,
                                                 classes=[self.get_word_id(word)])

        # Verificamos si se detectaron cuadros
        if not self.results or not self.results[0].boxes:
            return False  # Indica que no hubo detecciones

        # Creamos una lista para almacenar los frames detectados
        detected_frames = []

        # Procesamos cada cuadro detectado para crear un DetectedFrame
        for box in self.results[0].boxes:
            confidence_score = float(box.conf[0]) * 100  # Convertimos a porcentaje
            if confidence_score >= (confidence_threshold * 100):
                detected_frame = DetectedFrame(
                    path=image_path,
                    algorithm='Yolo11',
                    word=word.lower(),
                    percentage=round(confidence_score, 2),
                    time="00:00:00"
                )
                detected_frames.append(detected_frame)

        # Retornamos el primer cuadro detectado si existe alguno
        return detected_frames[0] if detected_frames else False

    def load_model(self):
        try:
            self.loaded_model = YOLO(self.model_path)
        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo: {e}")

    def load_labels(self, labels_path: str):
        with open(labels_path, 'r') as file:
            return json.load(file)

    def get_word_id(self, target_word: str):
        for id_label, label in self.yolo_labels.items():
            if label == target_word.lower():
                return int(id_label)
        raise ValueError(f"La palabra clave '{target_word}' no está en la lista de etiquetas.")
