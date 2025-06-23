from flask import Blueprint, request, jsonify
from ..models.regresi_class.services import predict_water_quality

api = Blueprint("api", __name__)

@api.route("/predict_class", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        # Validasi input
        required_fields = ['pH_t', 'temperature_t', 'turbidity_t', 'n_step']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        # Batas anomali
        batas_pH = (4.0, 9.0)
        batas_temp = (20, 33)
        batas_turb = (0, 100)
        # Cek anomali
        if not (batas_pH[0] <= data['pH_t'] <= batas_pH[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Nilai pH ({data["pH_t"]}) di luar batas normal ({batas_pH[0]} - {batas_pH[1]})'
            })
        if not (batas_temp[0] <= data['temperature_t'] <= batas_temp[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Suhu air ({data["temperature_t"]}°C) di luar batas normal ({batas_temp[0]} - {batas_temp[1]}°C)'
            })
        if not (batas_turb[0] <= data['turbidity_t'] <= batas_turb[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Nilai kekeruhan ({data["turbidity_t"]} NTU) di luar batas normal ({batas_turb[0]} - {batas_turb[1]} NTU)'
            })
        # Jika tidak ada anomali, lakukan prediksi
        result = predict_water_quality(data)
        prediction = result['quality']
        # Reason sesuai label
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
            'reason': reason,
            'n_step': result['n_step'],
            'pH_pred': result['pH_pred'],
            'temperature_pred': result['temperature_pred'],
            'turbidity_pred': result['turbidity_pred']
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route baru: /predict_anomali
@api.route("/predict_anomali", methods=["POST"])
def predict_anomali():
    try:
        data = request.get_json()
        # Validasi input
        required_fields = ['pH_t', 'temperature_t', 'turbidity_t', 'n_step']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        # Batas anomali
        batas_pH = (4.0, 9.0)
        batas_temp = (20, 33)
        batas_turb = (0, 100)
        # Cek anomali
        if not (batas_pH[0] <= data['pH_t'] <= batas_pH[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Nilai pH ({data["pH_t"]}) di luar batas normal ({batas_pH[0]} - {batas_pH[1]})'
            })
        if not (batas_temp[0] <= data['temperature_t'] <= batas_temp[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Suhu air ({data["temperature_t"]}°C) di luar batas normal ({batas_temp[0]} - {batas_temp[1]}°C)'
            })
        if not (batas_turb[0] <= data['turbidity_t'] <= batas_turb[1]):
            return jsonify({
                'prediction': 'Sangat Tidak Layak (Anomali Terdeteksi!)',
                'reason': f'Nilai kekeruhan ({data["turbidity_t"]} NTU) di luar batas normal ({batas_turb[0]} - {batas_turb[1]} NTU)'
            })
        # Jika tidak ada anomali, lakukan prediksi
        result = predict_water_quality(data)
        prediction = result['quality']
        # Reason sesuai label
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
            'reason': reason,
            'n_step': result['n_step'],
            'pH_pred': result['pH_pred'],
            'temperature_pred': result['temperature_pred'],
            'turbidity_pred': result['turbidity_pred']
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
