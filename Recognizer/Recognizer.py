from abc import ABC, abstractmethod


class Recognizer(ABC):

    @abstractmethod
    def recognize(self, image_path: str, percentage: float = 0.1, word : str =None, model =None):
        pass