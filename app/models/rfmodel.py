import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dataset", "perbaikan_dataset_kualitas_air_400_fixed.csv")
df = pd.read_csv(DATA_PATH)

# Tampilkan unique labels dalam dataset
print("\nLabel yang ada dalam dataset:")
print(df['kualitas'].unique())

# Pisahkan fitur dan label
X = df[['pH', 'temperature', 'turbidity']]
y = df['kualitas']

# Label encoding (ubah teks ke angka)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Tampilkan mapping label
print("\nMapping label:")
for i, label in enumerate(label_encoder.classes_):
    print(f"{i}: {label}")

# Standardisasi fitur
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data train-test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(
    criterion="gini", random_state=42, n_estimators=100
)
model.fit(X_train, y_train)

# Evaluasi model
y_pred = model.predict(X_test)
print("\nAkurasi Model:", accuracy_score(y_test, y_pred))
print("\nLaporan Klasifikasi:\n", classification_report(y_test, y_pred))

# Persiapkan path penyimpanan
SAVE_DIR = os.path.join(os.path.dirname(__file__))
os.makedirs(SAVE_DIR, exist_ok=True)

# Save model
with open(os.path.join(SAVE_DIR, "model.pkl"), "wb") as f:
    pickle.dump(model, f)

# Save scaler
with open(os.path.join(SAVE_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

# Save label encoder
with open(os.path.join(SAVE_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(label_encoder, f)

print(f"\n✅ Model, Scaler, dan LabelEncoder berhasil disimpan di {SAVE_DIR}") 