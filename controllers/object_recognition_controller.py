from services.object_recognition_service import ObjectRecognitionService

class ObjectRecognitionController:
    @staticmethod
    def recognize(model_type, file_path, confidence_threshold, word):
        service = ObjectRecognitionService(model_type)
        return service.recognize(file_path, confidence_threshold, word)
