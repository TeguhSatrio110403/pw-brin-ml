# Water Quality Prediction API
API untuk memprediksi kualitas air menggunakan kombinasi rule-based + machine learning model.

Rentang Waktu (n_step) 
'1 jam (12 langkah)': 12,
'3 jam (36 langkah)': 36,
'6 jam (72 langkah)': 72,
'12 jam (144 langkah)': 144,
'1 hari (288 langkah)': 288,
'3 hari (864 langkah)': 864,
'1 minggu (2016 langkah)': 2016

# Endpoint Klasifikasi
- `POST /api/predict`
  - {
        "pH_t": 7.0,
        "temperature_t": 25.0,
        "turbidity_t": 0.53,
    }

  - Response (JSON):
  {
      "prediction": "Layak",
      "reason": "Parameter berada dalam batas normal, air dapat digunakan dengan pengawasan"
    }

# Endpoint Regresi dan Klasifikasi
- `POST /api/predict_regresi_class`
  - {
        "pH_t": 7.0,
        "temperature_t": 25.0,
        "turbidity_t": 0.53,
        "n_step": 36
    }

  - Response (JSON):
    {
        "n_step": 36,
        "pH_pred": 7.15,
        "quality": "Sangat Layak",
        "temperature_pred": 25.34,
        "turbidity_pred": 1.67
    }

## Cara Jalankan
pip install -r requirements.txt
python main.py
