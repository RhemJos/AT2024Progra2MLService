from flask import Flask
from routes.user_routes import user_blueprint
from routes.recognizer_routes import object_recognition_from_zip_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(object_recognition_from_zip_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
