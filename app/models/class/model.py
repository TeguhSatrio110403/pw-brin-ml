# Model loading & prediction logic
import pickle
import numpy as np
import sys
import os

# Tambahkan path parent directory ke sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.check_anomaly import is_anomaly

# Load model, scaler, dan label encoder
with open("app/models/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("app/models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("app/models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

def predict_quality(data):
    if is_anomaly(data):
        return "Sangat Tidak Layak (Anomali Terdeteksi!)"
    
    # Transformasi data
    scaled = scaler.transform([data])
    prediction = model.predict(scaled)[0]
    
    # Konversi prediksi numerik ke label asli
    quality_label = label_encoder.inverse_transform([prediction])[0]
    return quality_label
