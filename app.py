from flask import Flask
from routes.user_routes import user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
