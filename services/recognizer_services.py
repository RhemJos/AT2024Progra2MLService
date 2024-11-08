import os
from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo, ObjectRecognizerMobileNet

class ObjectRecognitionService:
    def __init__(self, model_type):
        self.model_type = model_type.lower()
        if self.model_type == 'yolo':
            self.recognizer = ObjectRecognizerYolo()
        elif self.model_type == 'mobilenet':
            self.recognizer = ObjectRecognizerMobileNet()
        if self.model_type not in ['yolo', 'mobilenet']:
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