from flask import Blueprint, request, jsonify
from controllers.recognizer_controller import ModelRecognitionController
import json
from utils.file_utils import download_file_from_url, save_image


recognition_blueprint = Blueprint(
    'recognition', __name__)
face_recognition_blueprint = Blueprint(
    'face_recognition', __name__)


@recognition_blueprint.route('/recognition', methods=['POST'])
def recognition():
    print("---INICIANDO---", flush=True)
    data = request.get_json()
    zip_url = data.get('zip_url')
    zip_filename =  download_file_from_url(zip_url)
    model_type = data.get('model_type')
    confidence_threshold = (data.get('confidence_threshold', 0.1))
    word = data.get('word')

    if not zip_filename or not model_type or not word:
        return jsonify({"success": False, "message": "Missing required parameters"}), 400

    try:
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
        return jsonify({"success": False, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

@face_recognition_blueprint.route('/face_recognition', methods=['POST'])
def face_recognition():
    print("---INICIANDO FACE RECOGNITION---", flush=True)
    data = request.form
    zip_url = data.get('zip_url')
    zip_filename =  download_file_from_url(zip_url)
    print(zip_filename)
    model_type = data.get('model_type')
    confidence_threshold = (data.get('confidence_threshold', 0.1))
    word = data.get('word')
    image_file_reference = request.files.get('image_file_reference')
    reference_path = save_image(image_file_reference)

    try:
        zip_path = ModelRecognitionController.UPLOAD_FOLDER + '/' + zip_filename
        extract_folder = ModelRecognitionController.extract_zip(zip_path)
        image_files = ModelRecognitionController.list_images(
            model_type, extract_folder)
        results = []
        print('PROCESSING 1')
        for image_file in image_files:
            print('PROCESSING 2')
            verification = ModelRecognitionController.recognize_face(image_file, reference_path, float(confidence_threshold), word)
            if verification:
                results.append(verification.to_json())

        cleaned_results = [json.loads(result) for result in results]

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": cleaned_results}), 200
    except FileNotFoundError as e:
        return jsonify({"success": False, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500

