import pickle
import numpy as np
from flask import Blueprint, request, jsonify

# Buat Blueprint
predict_bp = Blueprint('predict_bp', __name__)

# Load model, scaler, dan label encoder
with open('app/model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('app/model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('app/model/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

@predict_bp.route('/predict', methods=['POST']) #Endpoint
def predict():
    data = request.get_json()
    
    # Batas nilai dari preprocessing.py
    batas_pH = (6.5, 9.5)
    batas_temp = (10, 27)
    batas_turb = (0.1, 5)

    try:
        # Validasi input
        required_fields = ['pH', 'temperature', 'turbidity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Field {field} is required'
                }), 400

        # Validasi batas nilai
        if not (batas_pH[0] <= data['pH'] <= batas_pH[1]):
            return jsonify({
                'prediction': 'Tidak Layak',
                'reason': 'pH di luar batas normal'
            })
        
        if not (batas_temp[0] <= data['temperature'] <= batas_temp[1]):
            return jsonify({
                'prediction': 'Tidak Layak',
                'reason': 'temperature di luar batas normal'
            })
        
        if not (batas_turb[0] <= data['turbidity'] <= batas_turb[1]):
            return jsonify({
                'prediction': 'Tidak Layak',
                'reason': 'turbidity di luar batas normal'
            })

        # Jika semua nilai dalam batas, gunakan model
        features = [data['pH'], data['temperature'], data['turbidity']]
        features = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features)
        pred_numeric = model.predict(features_scaled)
        pred_label = label_encoder.inverse_transform(pred_numeric)[0]
        
        return jsonify({
            'prediction': pred_label,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400
