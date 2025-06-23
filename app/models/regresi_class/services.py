import joblib
import os
import numpy as np
from ...config import Config

model_path = Config.MODEL_PATH

def load_models(n_step):
    suffix = f"_{n_step}"
    try:
        ph_model = joblib.load(os.path.join(model_path, f"trained_ph_model{suffix}.pkl"))
        temp_model = joblib.load(os.path.join(model_path, f"trained_temp_model{suffix}.pkl"))
        turb_model = joblib.load(os.path.join(model_path, f"trained_turb_model{suffix}.pkl"))
        classifier = joblib.load(os.path.join(model_path, f"trained_quality_classifier{suffix}.pkl"))
        label_encoder = joblib.load(os.path.join(model_path, f"label_encoder{suffix}.pkl"))
    except Exception as e:
        raise FileNotFoundError(f"Model untuk n_step={n_step} belum dilatih. Silakan jalankan training untuk n_step tersebut. Error: {e}")
    return ph_model, temp_model, turb_model, classifier, label_encoder

def predict_water_quality(data):
    # Ambil n_step dari input, default 12 jika tidak ada
    n_step = int(data.get("n_step", 12))
    ph_model, temp_model, turb_model, classifier, label_encoder = load_models(n_step)
    # Input: pH_t, temperature_t, turbidity_t
    features_lag = np.array([[data["pH_t"], data["temperature_t"], data["turbidity_t"]]])
    # Prediksi fitur ke depan
    pH_pred = ph_model.predict(features_lag)[0]
    temp_pred = temp_model.predict(features_lag)[0]
    turb_pred = turb_model.predict(features_lag)[0]
    # Batasi 3 angka di belakang koma
    pH_pred = round(float(pH_pred), 2)
    temp_pred = round(float(temp_pred), 2)
    turb_pred = round(float(turb_pred), 2)
    # Prediksi kualitas air
    features_pred = np.array([[pH_pred, temp_pred, turb_pred]])
    quality_encoded = classifier.predict(features_pred)
    quality_label = label_encoder.inverse_transform(quality_encoded)
    return {
        "n_step": n_step,
        "pH_pred": pH_pred,
        "temperature_pred": temp_pred,
        "turbidity_pred": turb_pred,
        "quality": quality_label[0]
    }
