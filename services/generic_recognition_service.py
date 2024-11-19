import os
from services.recognizer_strategy import IRecognizerStrategy

class GenericRecognitionService:
    def __init__(self, strategy: IRecognizerStrategy):
        self.strategy = strategy

    def list_images(self, folder_path: str):
        image_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_files.append(os.path.join(root, file))
        return image_files
    
    def recognize(self, file_path: str, confidence_threshold: float, word: str):
        return self.strategy.recognize(file_path, confidence_threshold, word)