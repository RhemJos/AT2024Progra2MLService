import os
from models.Recognizer.FaceRecognizer import FaceRecognizer


class FaceRecognitionService:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def recognize(self, image_path: str, image_reference: str, confidence_threshold: float, word: str):
        return self.recognizer.recognize(image_path, image_reference, confidence_threshold, word)
