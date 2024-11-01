from flask import Blueprint, request, jsonify
from controllers.gender_recognition_controller import GenderRecognitionController
from utils.file_utils import save_file
import numpy as np

gender_recognition_blueprint = Blueprint('gender_recognition', __name__)


@gender_recognition_blueprint.route('/gender_recognition', methods=['POST'])
def recognize_gender():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400

    file = request.files['file']
    file_path = save_file(file)

    if file_path:
        confidence_threshold = request.form.get('confidence_threshold', 0.1)
        word = request.form.get('word')

        result = GenderRecognitionController.recognize(
            file_path, confidence_threshold, word)

        if result is not None:
            
            for key, value in result.items():
                if isinstance(value, np.float32):
                    result[key] = float(value)

            relative_path = f"/uploads/{file.filename}"
            return jsonify({"success": True, "message": "Recognition completed", "file_path": relative_path, "result": result}), 200
        else:
            return jsonify({"success": False, "message": "Recognition failed"}), 400

    return jsonify({"success": False, "message": "File type not allowed"}), 400
