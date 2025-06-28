from flask import Flask
from .config import Config
from .routes.predict import api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(api)

    CORS(app, origins=["https://pw-brin-main.vercel.app", "http://localhost:5173"])
    # Untuk production, ganti "*" dengan domain frontend kamu, misal:
    # CORS(app, origins=["https://namadomainfrontend.com"])

    @app.route("/")
    def index():
        return "Predict Water Quality  API is running!", 200

    return app
