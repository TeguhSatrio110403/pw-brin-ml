from flask import Blueprint, request, jsonify
from app.models.class_model.model import predict_quality as predict_quality_class # type: ignore
from app.models.regresi_class.services import predict_water_quality as predict_regresi_class
from app.utils.check_anomaly import is_anomaly # type: ignore

api = Blueprint("api", __name__)

# Endpoint untuk klasifikasi biasa
@api.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        required_fields = ['pH', 'temperature', 'turbidity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        features = [data['pH'], data['temperature'], data['turbidity']]
        prediction, reason = predict_quality_class(features)
        # Tentukan reason jika kosong (bukan anomali)
        if not reason:
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
        return jsonify({'error': str(e)}), 400

# Endpoint untuk regresi+klasifikasi
@api.route("/predict_regresi_class", methods=["POST"])
def predict_regresi_class_route():
    try:
        data = request.get_json()
        required_fields = ['pH_t', 'temperature_t', 'turbidity_t', 'n_step']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        result = predict_regresi_class(data)
        # Tentukan reason berdasarkan prediksi quality
        quality = result['quality']
        if quality == 'Sangat Layak':
            reason = 'Semua parameter berada dalam batas optimal, air dapat digunakan untuk kebutuhan sehari-hari'
        elif quality == 'Cukup Layak':
            reason = 'Parameter mendekati batas normal sehingga perlu perhatian khusus'
        elif quality == 'Layak':
            reason = 'Parameter berada dalam batas normal, air dapat digunakan dengan pengawasan'
        elif quality == 'Tidak Layak':
            reason = 'Parameter berada di luar batas normal, air tidak disarankan untuk digunakan'
        else:
            reason = 'Parameter berada jauh dari batas normal, air tidak layak digunakan'
        response = {
            'n_step': result['n_step'],
            'pH_pred': result['pH_pred'],
            'temperature_pred': result['temperature_pred'],
            'turbidity_pred': result['turbidity_pred'],
            'quality': result['quality'],
            'reason': reason
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
