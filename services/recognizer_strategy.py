from abc import ABC, abstractmethod
from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo
from models.Recognizer.GenderRecognizer import GenderRecognizer


class IRecognizerStrategy(ABC):
    """Interface to recognition strategies"""

    @abstractmethod
    def recognize(self, file_path: str, confidence_threshold: float, word: str):
        pass

class ObjectRecognitionStrategy(IRecognizerStrategy):
    def __init__(self):
        self.recognizer = ObjectRecognizerYolo()

    def recognize(self, file_path, confidence_threshold, word):
        return self.recognizer.recognize(file_path, confidence_threshold, word)
    
class GenderRecognitionStrategy(IRecognizerStrategy):
    def __init__(self):
        self.recognizer = GenderRecognizer()

    def recognize(self, file_path, confidence_threshold, word):
        return self.recognizer.recognize(file_path, confidence_threshold, word)