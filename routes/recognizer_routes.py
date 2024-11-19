import os
from flask import Blueprint, request, jsonify
from werkzeug.datastructures import FileStorage
from common.exceptions.parameter_exception import ParameterException
from common.validations.composite_validator import CompositeValidator
from common.validations.range_validator import RangeValidator
from common.validations.required_type_validator import RequiredTypeValidator
from controllers.recognizer_controller import ModelRecognitionController
from utils.file_utils import download_file_from_url, save_image
from common.validations.error_handler_facade import ErrorHandlerFacade
import json


recognition_blueprint = Blueprint('recognition', __name__)
face_recognition_blueprint = Blueprint('face_recognition', __name__)
error_handler = ErrorHandlerFacade()


@recognition_blueprint.route('/recognition', methods=['POST'])
def recognition():
    print("---INICIANDO---", flush=True)
    try:
        data = request.get_json()
        zip_url, model_type, confidence_threshold, word = validate_recognition_inputs(
            data)

        # Main endpoint logic
        zip_filename = download_file_from_url(zip_url)
        zip_path = ModelRecognitionController.UPLOAD_FOLDER + '/' + zip_filename
        extract_folder = ModelRecognitionController.extract_zip(zip_path)
        image_files = ModelRecognitionController.list_images(
            model_type, extract_folder)
        results = [
            json.loads(ModelRecognitionController.recognize(
                model_type, image, confidence_threshold, word).to_json())
            for image in image_files
            if ModelRecognitionController.recognize(model_type, image, confidence_threshold, word)
        ]

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": results}), 200
    except ParameterException as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return error_handler.handle_error(e)


@face_recognition_blueprint.route('/face_recognition', methods=['POST'])
def recognize_from_zip():
    print("---INICIANDO FACE RECOGNITION---", flush=True)
    try:
        # Obtener los datos del formulario y archivo
        data = request.form.to_dict()  # Obtener los datos del formulario (solo texto)
        data['image_file_reference'] = request.files.get(
            'image_file_reference')  # Agregar el archivo al diccionario

        print(f"Datos combinados del formulario: {data}")

        # Validar inputs
        zip_url, model_type, confidence_threshold, word = validate_recognition_inputs(
            data, is_face_recognition=True)

        # Validar y manejar el archivo de referencia
        image_file_reference = data['image_file_reference']
        if isinstance(image_file_reference, FileStorage):
            # Guardar el archivo si es de tipo FileStorage
            image_file_reference_path = save_image(image_file_reference)
        elif isinstance(image_file_reference, str):
            # Usar la ruta directamente si es de tipo str
            image_file_reference_path = image_file_reference
        else:
            raise ParameterException("Invalid type for image_file_reference")

        # Lógica principal del endpoint
        zip_filename = download_file_from_url(zip_url)
        zip_path = os.path.join(
            ModelRecognitionController.UPLOAD_FOLDER, zip_filename)
        extract_folder = ModelRecognitionController.extract_zip(zip_path)
        image_files = ModelRecognitionController.list_images(
            model_type, extract_folder)

        results = [
            json.loads(ModelRecognitionController.recognize_face(
                image, image_file_reference_path, confidence_threshold, word).to_json())
            for image in image_files
            if ModelRecognitionController.recognize_face(image, image_file_reference_path, confidence_threshold, word)
        ]

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": results}), 200
    except ParameterException as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return error_handler.handle_error(e)


def validate_recognition_inputs(data, is_face_recognition=False):
    """Validaciones estándar para los endpoints de reconocimiento."""
    zip_url = data.get('zip_url')
    model_type = data.get('model_type')
    confidence_threshold = data.get('confidence_threshold', 0.1)
    word = data.get('word')

    # Convertir confidence_threshold a float
    try:
        confidence_threshold = float(confidence_threshold)
    except ValueError:
        raise ParameterException("confidence_threshold must be a valid number")

    # Definir validaciones comunes
    validations = [
        RequiredTypeValidator("zip_url", zip_url, str),
        RequiredTypeValidator("model_type", model_type, str),
        RequiredTypeValidator("confidence_threshold",
                              confidence_threshold, (float, int)),
        RangeValidator("confidence_threshold", confidence_threshold, 0.0, 1.0),
        RequiredTypeValidator("word", word, str),
    ]

    # Validación adicional para reconocimiento facial
    if is_face_recognition:
        image_file_reference = data.get('image_file_reference')
        if not isinstance(image_file_reference, (FileStorage, str)):
            raise ParameterException(
                "Invalid or missing 'image_file_reference' parameter")
        validations.append(
            RequiredTypeValidator("image_file_reference",
                                  image_file_reference, (FileStorage, str))
        )

    # Ejecutar validaciones
    CompositeValidator(validations).validate()

    return zip_url, model_type, confidence_threshold, word
