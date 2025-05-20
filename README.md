# Water Quality Prediction API

API untuk memprediksi kualitas air menggunakan kombinasi rule-based + machine learning model.

## Endpoint
- `POST /api/predict`
  - Body (JSON):
    {
      "pH": 7.0,
      "temperature": 25.0,
      "turbidity": 1.5
    }

  - Response (JSON):
    {
      "prediction": "Layak"
    }

## Cara Jalankan
pip install -r requirements.txt
python main.py