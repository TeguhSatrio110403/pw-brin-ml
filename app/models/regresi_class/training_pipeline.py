import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os
import sys

# Ambil dataset
DATA_PATH = "data/dataset_kualitas_air_mingguan.csv"
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Ambil n_step dari argumen command line jika ada, default 12
if len(sys.argv) > 1:
    n_step = int(sys.argv[1])
else:
    n_step = 12

print(f"Training untuk n_step = {n_step}")

# Cek panjang data
if len(df) <= n_step + 1:
    raise ValueError(f"Jumlah data ({len(df)} baris) terlalu sedikit untuk melakukan prediksi sebanyak {n_step} langkah.")
else:
    # Buat fitur t-1
    for feat in ['pH', 'temperature', 'turbidity']:
        df[f'{feat}_t'] = df[feat].shift(1)

    # Buat target ke depan (t+n_step)
    df['pH_target'] = df['pH'].shift(-n_step)
    df['temperature_target'] = df['temperature'].shift(-n_step)
    df['turbidity_target'] = df['turbidity'].shift(-n_step)
    df['kualitas_target'] = df['kualitas'].shift(-n_step)

    # Hapus baris yang mengandung NaN
    df_model = df.dropna().reset_index(drop=True)

    # Fitur input untuk regresi
    X_reg = df_model[['pH_t', 'temperature_t', 'turbidity_t']]
    y_pH = df_model['pH_target']
    y_temp = df_model['temperature_target']
    y_turb = df_model['turbidity_target']

    # Inisialisasi dan training model regresi
    model_pH = XGBRegressor()
    model_temp = XGBRegressor()
    model_turb = XGBRegressor()
    model_pH.fit(X_reg, y_pH)
    model_temp.fit(X_reg, y_temp)
    model_turb.fit(X_reg, y_turb)

    # Prediksi hasil regresi
    df_model['pH_pred'] = model_pH.predict(X_reg)
    df_model['temperature_pred'] = model_temp.predict(X_reg)
    df_model['turbidity_pred'] = model_turb.predict(X_reg)

    # Fitur input untuk klasifikasi
    X_clf = df_model[['pH_pred', 'temperature_pred', 'turbidity_pred']]
    y_clf = df_model['kualitas_target']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y_clf)

    # TimeSeriesSplit untuk evaluasi (opsional, bisa di-comment jika tidak perlu)
    tscv = TimeSeriesSplit(n_splits=5)
    for i, (train_index, test_index) in enumerate(tscv.split(X_clf)):
        X_train, X_test = X_clf.iloc[train_index], X_clf.iloc[test_index]
        y_train, y_test = y_encoded[train_index], y_encoded[test_index]
        clf = RandomForestClassifier(random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        unique_labels = np.unique(np.concatenate((y_test, y_pred)))
        print(f"\nSplit {i+1}:")
        print(classification_report(y_test, y_pred, labels=unique_labels, target_names=le.inverse_transform(unique_labels)))

    # Training final model klasifikasi pada seluruh data
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_clf, y_encoded)

    # Simpan model dan encoder dengan suffix n_step
    os.makedirs("app/models/regresi_class/model_pkl", exist_ok=True)
    suffix = f"_{n_step}"
    joblib.dump(model_pH, f"app/models/regresi_class/model_pkl/trained_ph_model{suffix}.pkl")
    joblib.dump(model_temp, f"app/models/regresi_class/model_pkl/trained_temp_model{suffix}.pkl")
    joblib.dump(model_turb, f"app/models/regresi_class/model_pkl/trained_turb_model{suffix}.pkl")
    joblib.dump(clf, f"app/models/regresi_class/model_pkl/trained_quality_classifier{suffix}.pkl")
    joblib.dump(le, f"app/models/regresi_class/model_pkl/label_encoder{suffix}.pkl")
    # Simpan n_step agar konsisten saat prediksi
    with open(f"app/models/regresi_class/model_pkl/n_step{suffix}.txt", "w") as f:
        f.write(str(n_step))
