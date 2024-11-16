import os

from models.Recognizer.FaceRecognizer import FaceRecognizer
from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo
from models.Recognizer.GenderRecognizer import GenderRecognizer

class RecognitionService:
    def __init__(self, model_type):
        self.model_type = model_type.lower()
        if self.model_type == 'object':
            self.recognizer = ObjectRecognizerYolo()
        elif self.model_type == 'gender':
            self.recognizer = GenderRecognizer()
        if self.model_type not in ['object', 'gender']:
            raise ValueError(f"Model type {self.model_type} is not supported")

    def list_images(self, folder_path):
        image_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_files.append(os.path.join(root, file))
        return image_files

    def recognize(self, image_path, confidence_threshold, word):
        return self.recognizer.recognize(image_path, confidence_threshold, word)

class FaceRecognitionService:
    def __init__(self):
        self.recognizer = FaceRecognizer()
        print("entra a services")
    def list_images(self, folder_path):
        image_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_files.append(os.path.join(root, file))
        return image_files

    def recognize(self, image_path,image_reference, confidence_threshold, word):
        return self.recognizer.recognize(image_path, image_reference , confidence_threshold, word)
