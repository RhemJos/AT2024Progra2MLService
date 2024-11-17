from flask import Blueprint, request, jsonify
from werkzeug.datastructures import FileStorage
from common.exceptions.parameter_exception import ParameterException
from common.validations.composite_validator import CompositeValidator
from common.validations.context import Context
from common.validations.error_handler_facade import ErrorHandlerFacade
from common.validations.range_validator import RangeValidator
from common.validations.required_type_validator import RequiredTypeValidator
from controllers.recognizer_controller import ModelRecognitionController
import json
from utils.file_utils import download_file_from_url, save_image


recognition_blueprint = Blueprint(
    'recognition', __name__)
face_recognition_blueprint = Blueprint(
    'face_recognition', __name__)

error_handler = ErrorHandlerFacade()

@recognition_blueprint.route('/recognition', methods=['POST'])
def recognition():
    print("---INICIANDO---", flush=True)
    try:
        # Get body data
        data = request.get_json()
        zip_url = data.get('zip_url')
        model_type = data.get('model_type')
        confidence_threshold = data.get('confidence_threshold', 0.1)
        word = data.get('word')
        
        # Ensure that 'confidence_threshold is converted to float'
        try:
            confidence_threshold = float(confidence_threshold)
        except ValueError:
            raise ParameterException("confidence_threshold must be a valid number")

        # Define validations
        validations = [
            RequiredTypeValidator("zip_url", zip_url, str),
            RequiredTypeValidator("model_type", model_type, str),
            RequiredTypeValidator("confidence_threshold", confidence_threshold,(float, int)),
            RangeValidator("confidence_threshold", confidence_threshold, 0.0, 1.0) ,
            RequiredTypeValidator("word", word, str),
        ]

        # Run validation
        composite_validator = CompositeValidator(validations)
        composite_validator.validate()   

        # Main endpoint logic
        zip_filename = download_file_from_url(zip_url)
        zip_path = ModelRecognitionController.UPLOAD_FOLDER + '/' + zip_filename
        extract_folder = ModelRecognitionController.extract_zip(zip_path)
        image_files = ModelRecognitionController.list_images(
            model_type, extract_folder)
        results = []
        print('PROCESSING 1')
        for image_file in image_files:
            print('PROCESSING 2')
            verification = ModelRecognitionController.recognize(
                model_type, image_file, confidence_threshold, word)
            if verification:
                results.append(verification.to_json())

        cleaned_results = [json.loads(result) for result in results]

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": cleaned_results}), 200
    except ParameterException as e:
        return jsonify({"success": False, "message":str(e)}), 400
    except Exception as e:
        return error_handler.handle_error(e)


@face_recognition_blueprint.route('/face_recognition', methods=['POST'])
def recognize_from_zip():
    print("---INICIANDO FACE RECOGNITION---", flush=True)
    try:
        # Get form data
        data = request.form
        zip_url = data.get('zip_url')
        model_type = data.get('model_type')
        confidence_threshold = data.get('confidence_threshold', 0.1)
        word = data.get('word')
        image_file_reference = request.files.get('image_file_reference')

        # Ensure that 'confidence_threshold is converted to float'
        try:
            confidence_threshold = float(confidence_threshold)
        except ValueError:
            raise ParameterException("confidence_threshold must be a valid number")
        print(f'VALOR CONFIDENCE: {confidence_threshold} es del tipo {type(confidence_threshold)}')
        # Define validations
        validations=[
            RequiredTypeValidator("zip_url", zip_url, str),
            RequiredTypeValidator("model_type", model_type, str),
            RequiredTypeValidator("confidence_threshold", confidence_threshold, (float, int)),
            RangeValidator("confidence_threshold", confidence_threshold, 0.0, 1.0),
            RequiredTypeValidator("word", word, str),
            RequiredTypeValidator("image_file_reference", image_file_reference, FileStorage)
        ]

        # Run validation
        composite_validator = CompositeValidator(validations)
        composite_validator.validate()
        
        # Main endpoint logic
        zip_filename = download_file_from_url(zip_url)
        reference_path = save_image(image_file_reference)
        zip_path = ModelRecognitionController.UPLOAD_FOLDER + '/' + zip_filename
        extract_folder = ModelRecognitionController.extract_zip(zip_path)
        image_files = ModelRecognitionController.list_images(
            model_type, extract_folder)
        results = []
        print('PROCESSING 1')
        for image_file in image_files:
            print('PROCESSING 2')
            verification = ModelRecognitionController.recognize_face(
                image_file, reference_path, float(confidence_threshold), word)
            if verification:
                results.append(verification.to_json())

        cleaned_results = [json.loads(result) for result in results]

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": cleaned_results}), 200
    except ParameterException as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return error_handler.handle_error(e)
