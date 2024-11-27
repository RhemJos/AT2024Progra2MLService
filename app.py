from flask import Flask
from routes.recognizer_routes import recognition_blueprint,face_recognition_blueprint

app = Flask(__name__)
app.register_blueprint(recognition_blueprint, url_prefix='/api')
app.register_blueprint(face_recognition_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
