from models.Recognizer.FaceRecognizer import FaceRecognizer

class FaceRecognitionService:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def recognize(self, target_image_path, reference_path):
        return self.recognizer.face_recognition(target_image_path, reference_path)
