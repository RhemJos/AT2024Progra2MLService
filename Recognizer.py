from abc import ABC, abstractmethod


class Recognizer(ABC):
    def __init__(self, model: str, model_path: str):
        self.model = model
        self.model_path = model_path

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def recognize(self, input_image: str, confidence_threshold: float = 0.1):
        pass

    @abstractmethod
    def get_confidence(self):
        pass
