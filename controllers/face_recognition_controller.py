from services.face_recognition_service import FaceRecognitionService


class FaceRecognitionController:
    @staticmethod
    def recognize(file_path, reference_path):
        service = FaceRecognitionService()
        return service.recognize(file_path, reference_path)
