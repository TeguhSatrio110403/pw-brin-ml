from flask import Flask
from app.routes.predict import predict_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprint tanpa prefix
    app.register_blueprint(predict_bp)

    # Tambahkan route sederhana buat tes di browser
    @app.route('/')
    def index():
        return "Random Forest Classifier API is running!", 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
