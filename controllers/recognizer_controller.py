import os
from services.recognizer_services import ObjectRecognitionService
from utils.file_utils import extract_zip


class ObjectRecognitionController:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'uploads'))

    @staticmethod
    def extract_zip(zip_path):
        extract_folder = os.path.splitext(zip_path)[0]
        extract_zip(zip_path, extract_folder)
        return extract_folder

    @staticmethod
    def list_images(model_type, folder_path):
        service = ObjectRecognitionService(model_type)
        return service.list_images(folder_path)

    @staticmethod
    def recognize(model_type, file_path, confidence_threshold, word):
        service = ObjectRecognitionService(model_type)
        return service.recognize(file_path, confidence_threshold, word)