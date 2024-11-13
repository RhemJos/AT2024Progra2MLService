from flask import Blueprint, request, jsonify
from controllers.recognizer_controller import ModelRecognitionController
import json
from utils.error_handler_factory import ErrorHandlerFactory
from utils.file_utils import download_file_from_url

object_recognition_from_zip_blueprint = Blueprint(
    'object_recognition_from_zip', __name__)

#TODO un nuevo POST para face recognizer
@object_recognition_from_zip_blueprint.route('/object_recognition_from_zip', methods=['POST'])
def recognize_object_from_zip():
    print("---INICIANDO---", flush=True)
    data = request.get_json()
    # Extraer parametros
    zip_url = data.get('zip_url')
    model_type = data.get('model_type')
    confidence_threshold = (data.get('confidence_threshold', 0.1))
    word = data.get('word')

    #Identificar parametros faltantes
    missing_params = []
    if not zip_url:
        missing_params.append("zip_url")
    if not model_type:
        missing_params.append("model_type")
    if not word:
        missing_params.append("word")

    # Si faltan parametros, manejamos el error antes de continuar
    if missing_params:
        error_message = f"Missing required parameters: {', '.join(missing_params)}"
        error_handler = ErrorHandlerFactory.get_error_handler(ValueError(error_message))
        return error_handler.handle()

    try: #TODO esto podria ser un metodo en UTILS
        zip_filename =  download_file_from_url(zip_url)
        zip_path = ModelRecognitionController.UPLOAD_FOLDER + '/' + zip_filename
        extract_folder = ModelRecognitionController.extract_zip(zip_path)
        image_files = ModelRecognitionController.list_images(
            model_type, extract_folder)
        results = []
        print('PROCESSING 1')
        for image_file in image_files:
            print('PROCESSING 2')
            verification = ModelRecognitionController.recognize(model_type, image_file, confidence_threshold, word)
            if verification:
                results.append(verification.to_json())

        cleaned_results = [json.loads(result) for result in results]

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": cleaned_results}), 200
    except FileNotFoundError as e:
        return ErrorHandlerFactory.get_error_handler(e).handle()
    except Exception as e:
        return ErrorHandlerFactory.get_error_handler(e).handle()
