from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo
from models.Recognizer.GenderRecognizer import GenderRecognizer

class ObjectRecognitionService:
    def __init__(self, model_type):
        self.model_type = model_type.lower()
        if self.model_type == 'yolo':
            self.recognizer = ObjectRecognizerYolo()
        elif self.model_type == 'gender':
            self.recognizer = GenderRecognizer()
        else:
            raise ValueError(f"Model type {self.model_type} is not supported")

    def recognize(self, image_path, confidence_threshold, word):
        return self.recognizer.recognize(image_path, confidence_threshold, word)
