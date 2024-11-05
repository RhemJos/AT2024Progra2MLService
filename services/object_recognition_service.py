from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo, ObjectRecognizerMobileNet

class ObjectRecognitionService:
    def __init__(self, model_type):
        self.model_type = model_type.lower()
        if self.model_type == 'yolo':
            self.recognizer = ObjectRecognizerYolo()
        elif self.model_type == 'mobilenet':
            self.recognizer = ObjectRecognizerMobileNet()
        else:
            raise ValueError(f"Model type {self.model_type} is not supported")

    def recognize(self, image_path, confidence_threshold, word):
        return self.recognizer.recognize(image_path, confidence_threshold, word)
