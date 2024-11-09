from flask import Blueprint, request, jsonify
from controllers.recognizer_controller import ObjectRecognitionController


object_recognition_from_zip_blueprint = Blueprint(
    'object_recognition_from_zip', __name__)


@object_recognition_from_zip_blueprint.route('/object_recognition_from_zip', methods=['POST'])
def recognize_object_from_zip():
    print("---INICIANDO---", flush=True)
    data = request.get_json()
    zip_filename = data.get('zip_filename')
    model_type = data.get('model_type')
    confidence_threshold = (data.get('confidence_threshold', 0.1))
    word = data.get('word')

    if not zip_filename or not model_type or not word:
        return jsonify({"success": False, "message": "Missing required parameters"}), 400

    try:
        zip_path = ObjectRecognitionController.UPLOAD_FOLDER + '/' + zip_filename
        extract_folder = ObjectRecognitionController.extract_zip(zip_path)
        image_files = ObjectRecognitionController.list_images(
            model_type, extract_folder)
        results = []
        print('PROCESSING 1')
        for image_file in image_files:
            print('PROCESSING 2')
            results.append((ObjectRecognitionController.recognize(model_type, image_file, confidence_threshold, word)).to_json())

        return jsonify({"success": True, "message": "ZIP extracted and images listed", "results": results}), 200
    except FileNotFoundError as e:
        return jsonify({"success": False, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500
