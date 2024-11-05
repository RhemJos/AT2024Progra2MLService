from flask import Blueprint, request, jsonify
from controllers.object_recognition_controller import ObjectRecognitionController
from utils.file_utils import save_file
import numpy as np

object_recognition_blueprint = Blueprint('object_recognition', __name__)


@object_recognition_blueprint.route('/object_recognition', methods=['POST'])
def recognize_object():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400

    file = request.files['file']
    file_path = save_file(file)

    if file_path:
        model_type = request.form.get('model_type')
        confidence_threshold = float(
            request.form.get('confidence_threshold', 0.1))
        word = request.form.get('word')

        result = ObjectRecognitionController.recognize(
            model_type, file_path, confidence_threshold, word)

        if result is not None:

            for item in result:
                if isinstance(item[2], np.float32):
                    item[2] = float(item[2])

            relative_path = f"/uploads/{file.filename}"
            return jsonify({"success": True, "message": "Recognition completed", "file_path": relative_path, "result": result}), 200
        else:
            return jsonify({"success": False, "message": "Recognition failed"}), 400

    return jsonify({"success": False, "message": "File type not allowed"}), 400
