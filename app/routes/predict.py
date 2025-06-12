import pickle
import numpy as np
from flask import Blueprint, request, jsonify
from app.models.model import predict_quality

# Buat Blueprint
predict_bp = Blueprint("predict_bp", __name__)

# Batas nilai untuk deteksi anomali
batas_pH = (4.0, 9.0)
batas_temp = (20, 33)
batas_turb = (0, 100)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        # Validasi input
        required_fields = ['pH', 'temperature', 'turbidity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Field {field} is required'
                }), 400

        # Cek anomali
        if not (batas_pH[0] <= data['pH'] <= batas_pH[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Nilai pH ({data["pH"]}) di luar batas normal ({batas_pH[0]} - {batas_pH[1]})'
            })
            
        if not (batas_temp[0] <= data['temperature'] <= batas_temp[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Suhu air ({data["temperature"]}°C) di luar batas normal ({batas_temp[0]} - {batas_temp[1]}°C)'
            })
            
        if not (batas_turb[0] <= data['turbidity'] <= batas_turb[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Nilai kekeruhan ({data["turbidity"]} NTU) di luar batas normal ({batas_turb[0]} - {batas_turb[1]} NTU)'
            })

        # Jika tidak ada anomali, gunakan model
        features = [data['pH'], data['temperature'], data['turbidity']]
        prediction = predict_quality(features)
        
        # Tentukan reason berdasarkan prediksi
        if prediction == 'Sangat Layak':
            reason = 'Semua parameter berada dalam batas optimal, air dapat digunakan untuk kebutuhan sehari-hari'
        elif prediction == 'Cukup Layak':
            reason = 'Parameter mendekati batas normal sehingga perlu perhatian khusus'
        elif prediction == 'Layak':
            reason = 'Parameter berada dalam batas normal, air dapat digunakan dengan pengawasan'
        elif prediction == 'Tidak Layak':
            reason = 'Parameter berada di luar batas normal, air tidak disarankan untuk digunakan'
        else:
            reason = 'Parameter berada jauh dari batas normal, air tidak layak digunakan'
        
        response = {
            'prediction': prediction,
            'reason': reason
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400
