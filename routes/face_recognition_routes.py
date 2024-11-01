import os
from flask import Blueprint, request, jsonify
from controllers.face_recognition_controller import FaceRecognitionController
from utils.file_utils import save_file

face_recognition_blueprint = Blueprint('face_recognition', __name__)


@face_recognition_blueprint.route('/face_recognition', methods=['POST'])
def recognize_face():
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "message": "No file part"
        }), 400

    file = request.files['file']
    file_path = save_file(file)

    if file_path:
        reference_path = request.form.get('reference_path')

        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "message": "File not found"
            }), 400

        result = FaceRecognitionController.recognize(file_path, reference_path)
        print({result})
        if result is not None:
            relative_path = f"/uploads/{file.filename}"
            return jsonify({
                "success": True,
                "message": "Recognition completed",
                "file_path": relative_path,
                "result": result
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Recognition failed"
            }), 400

    return jsonify({
        "success": False,
        "message": "File type not allowed"
    }), 400
