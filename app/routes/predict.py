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
    
    # Batas peringatan (untuk nilai yang sedikit melebihi batas)
    batas_peringatan_turb = 6 

    try:
        # Validasi input
        required_fields = ['pH', 'temperature', 'turbidity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Field {field} is required'
                }), 400

        # List untuk menyimpan parameter yang bermasalah
        masalah = []

        # Validasi batas nilai pH
        if data['pH'] < batas_pH[0]:
            masalah.append(f'Nilai pH ({data["pH"]}) terlalu rendah')
        elif data['pH'] > batas_pH[1]:
            masalah.append(f'Nilai pH ({data["pH"]}) terlalu tinggi')
        
        # Validasi batas nilai temperature
        if data['temperature'] < batas_temp[0]:
            masalah.append(f'Suhu air ({data["temperature"]}°C) terlalu rendah')
        elif data['temperature'] > batas_temp[1]:
            masalah.append(f'Suhu air ({data["temperature"]}°C) terlalu tinggi')
        
        # Validasi batas nilai turbidity
        if data['turbidity'] < batas_turb[0]:
            masalah.append(f'Nilai kekeruhan ({data["turbidity"]} NTU) terlalu rendah')
        elif data['turbidity'] > batas_turb[1]:
            if data['turbidity'] <= batas_peringatan_turb:
                masalah.append(f'Nilai kekeruhan ({data["turbidity"]} NTU) melebihi batas normal')
            else:
                masalah.append(f'Nilai kekeruhan ({data["turbidity"]} NTU) terlalu tinggi')

        # Jika ada parameter yang bermasalah
        if masalah:
            if len(masalah) > 2:
                reason = ', '.join(masalah[:-1]) + ' dan ' + masalah[-1]
            else:
                reason = ' dan '.join(masalah)
                
            return jsonify({
                'prediction': 'Tidak Layak',
                'reason': reason
            })

        # Jika semua nilai dalam batas
        features = [data['pH'], data['temperature'], data['turbidity']]
        features = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features)
        pred_numeric = model.predict(features_scaled)
        pred_label = label_encoder.inverse_transform(pred_numeric)[0]
        
        # Tentukan reason berdasarkan prediksi
        if pred_label == 'Sangat Layak':
            reason = 'Semua parameter berada dalam batas optimal, air dapat digunakan untuk kebutuhan sehari-hari'
        elif pred_label == 'Cukup Layak':
            reason = 'Parameter berada dalam mendekati batas normal sehingga perlu perhatian khusus'
        else:
            reason = 'Semua parameter berada dalam batas normal'
        
        response = {
            'prediction': pred_label,
            'reason': reason
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400
