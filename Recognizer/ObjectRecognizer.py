#
# @ObjectRecognizer.py Copyright (c) 2021 Jalasoft. # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from Recognizer import Recognizer
from ultralytics import YOLO
import json
import os
import cv2


class ObjectRecognizerYolo(Recognizer):

    def __init__(self):
        super().__init__()
        self.model_path = os.path.join(os.getcwd(), "yolo11n.pt")
        self.loaded_model = None
        self.load_model()
        self.yolo_labels = self.load_labels(os.path.join(os.getcwd(), "classes_yolo.json"))
        self.results = None

    def recognize(self, image_path: str, confidence_threshold: float = 0.1, word: str = None):
        if word is None:
            raise ValueError("The 'word' parameter is required.")
        self.results = self.loaded_model.predict(source=image_path, conf=confidence_threshold,
                                                 classes=[self.get_word_id(word)])
        return [['Yolo11', word.lower(), float(box.conf[0])] for box in self.results[0].boxes]

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


class ObjectRecognizerMobileNet(Recognizer):

    def __init__(self):
        super().__init__()
        self.descriptor_path = os.path.join(os.getcwd(), "deploy.prototxt")
        self.model_path = os.path.join(os.getcwd(), "mobilenet_iter_73000.caffemodel")
        self.loaded_model = None
        self.load_model()
        self.mobilenet_labels = self.load_labels(os.path.join(os.getcwd(), "classes_mobilenet.json"))
        self.results = None

    def recognize(self, image_path: str, confidence_threshold: float = 0.1, word: str = None):
        if word is None:
            raise ValueError("The 'word' parameter is required.")
        image = cv2.imread(image_path)
        (h, w) = image.shape[:2]
        # detections = self.loaded_model.forward(cv2.dnn.blobFromImage(image,0.007843,(300, 300),127.5))
        blob = cv2.dnn.blobFromImage(image,0.007843,(300, 300),127.5)
        self.loaded_model.setInput(blob)
        detections = self.loaded_model.forward()

        results = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > confidence_threshold:
                idx = int(detections[0, 0, i, 1])
                if idx == self.get_word_id(word):
                    fila = ['MobileNet-SSD', word, confidence]
                    results.append(fila)
        return results

    def load_model(self):
        try:
            self.loaded_model = cv2.dnn.readNetFromCaffe(self.descriptor_path, self.model_path)
        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo: {e}")

    def load_labels(self, labels_path: str):
        with open(labels_path, 'r') as file:
            return json.load(file)

    def get_word_id(self, target_word: str):
        for id_label, label in self.mobilenet_labels.items():
            if label == target_word.lower():
                return int(id_label)
        raise ValueError(f"La palabra clave '{target_word}' no está en la lista de etiquetas.")

