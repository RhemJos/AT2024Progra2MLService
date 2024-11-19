import os

from services.generic_recognition_service import GenericRecognitionService
from services.recognizer_strategy import GenderRecognitionStrategy, ObjectRecognitionStrategy
from utils.file_utils import extract_zip
from services.recognizer_services import RecognitionService
from services.face_recognition_service import FaceRecognitionService


class ModelRecognitionController:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'uploads'))

    @staticmethod
    def extract_zip(zip_path):
        extract_folder = os.path.splitext(zip_path)[0]
        extract_zip(zip_path, extract_folder)
        return extract_folder

    @staticmethod
    def list_images(model_type, folder_path):
        strategy = ModelRecognitionController._get_strategy(model_type)
        service = GenericRecognitionService(strategy)
        return service.list_images(folder_path)

    @staticmethod
    def recognize(model_type, file_path, confidence_threshold, word):
        strategy = ModelRecognitionController._get_strategy(model_type)
        service = GenericRecognitionService(strategy)
        return service.recognize(file_path, confidence_threshold, word)

    @staticmethod
    def recognize_face(image_path, image_reference, confidence_threshold, word):
        service = FaceRecognitionService()
        return service.recognize(image_path, image_reference, confidence_threshold, word)

    @staticmethod
    def _get_strategy(model_type):
        model_type = model_type.lower()
        if model_type == 'object':
            return ObjectRecognitionStrategy()
        elif model_type == 'gender':
            return GenderRecognitionStrategy()
        else:
            raise ValueError(f"Unkown model type: {model_type}")
