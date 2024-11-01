from services.gender_recognition_service import GenderRecognitionService


class GenderRecognitionController:
    @staticmethod
    def recognize(file_path, confidence_threshold, word):
        service = GenderRecognitionService()
        return service.recognize(file_path, confidence_threshold, word)
