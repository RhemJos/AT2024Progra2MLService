from models.Recognizer.GenderRecognizer import GenderRecognizer


class GenderRecognitionService:
    def __init__(self):
        self.recognizer = GenderRecognizer()

    def recognize(self, image_path, confidence_threshold, word):
        return self.recognizer.recognize(image_path, confidence_threshold)
