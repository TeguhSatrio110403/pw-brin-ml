from flask import Flask
from .config import Config
from .routes.predict import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(api)

    @app.route("/")
    def index():
        return "Predict Water Quality  API is running!", 200

    return app
