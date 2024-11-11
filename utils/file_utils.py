import os

import requests
import zipfile
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'uploads'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        print(f"RUTA UTILS {file_path}")
        print(f"TIPO RUTA {type(file_path)}")
        return file_path
    return None


def save_file_from_url(url):
    local_filename = os.path.join(
        '', secure_filename(os.path.basename(url)))+'.zip'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def extract_zip(zip_path, extract_folder):
    if not os.path.exists(zip_path): 
        raise FileNotFoundError(f"The file {zip_path} does not exist.") 
    if not os.path.exists(extract_folder): 
        os.makedirs(extract_folder) 
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: 
        zip_ref.extractall(extract_folder) 
    return extract_folder




