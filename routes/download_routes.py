from flask import Blueprint, request, jsonify
from utils.file_utils import download_file

download_blueprint = Blueprint('download', __name__)


@download_blueprint.route('/download/<filename>', methods=['GET'])
def download(filename):
    file = download_file(filename)
    if file:
        return file
    return jsonify({
        "success": False,
        "message": "File not found"
    }), 404
