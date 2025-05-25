from flask import Flask, jsonify
from app.routes.predict import predict_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Register blueprint dengan prefix /api
    app.register_blueprint(predict_bp, url_prefix='/api')

    # Tambahkan health check endpoint untuk mencegah Render spinning down
    @app.route('/health')
    def health():
        return jsonify({"status": "ok"}), 200
        
    # Tambahkan route sederhana buat tes di browser
    @app.route('/')
    def index():
        return "API is running!", 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
