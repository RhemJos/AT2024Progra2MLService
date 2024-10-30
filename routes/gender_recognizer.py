from flask import Blueprint, request, jsonify
from utils.file_utils import save_file

gender_recognizer_blueprint = Blueprint('gender_recognizer', __name__)


@gender_recognizer_blueprint.route('/gender_recognizer', methods=['POST'])
def gender_recognizer():
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "message": "No file part"
        }), 400

    file = request.files['file']
    file_path = save_file(file)

    if file_path:
        accuracy = request.form.get('accuracy')
        word = request.form.get('word')
        model = request.form.get('model')

        relative_path = f"/uploads/{file.filename}"

        return jsonify({
            "success": True,
            "message": "File saved successfully",
            "file_path": relative_path
        }), 200
    return jsonify({
        "success": False,
        "message": "File type not allowed"
    }), 400
