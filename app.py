from flask import Flask
from routes.user_routes import user_blueprint
from routes.gender_recognition_routes import gender_recognition_blueprint
from routes.object_recognition_routes import object_recognition_blueprint
from routes.face_recognition_routes import face_recognition_blueprint
from routes.recognizer_routes import object_recognition_from_zip_blueprint
from routes.download_routes import download_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(gender_recognition_blueprint, url_prefix='/api')
app.register_blueprint(object_recognition_blueprint, url_prefix='/api')
app.register_blueprint(face_recognition_blueprint, url_prefix='/api')
app.register_blueprint(download_blueprint, url_prefix='/api')
app.register_blueprint(object_recognition_from_zip_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
