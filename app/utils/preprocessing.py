def prediksi_kualitas_air(data_baru, model, scaler):
    """
    Prediksi kualitas air dengan hybrid rule + model.
    data_baru: DataFrame dengan kolom ['pH', 'temperature', 'turbidity']
    """
    batas_pH = (6.5, 9.5)
    batas_temp = (10, 27)
    batas_turb = (0.1, 5)

    hasil_prediksi = []

    for _, row in data_baru.iterrows():
        if not (batas_pH[0] <= row['pH'] <= batas_pH[1]) or not (batas_temp[0] <= row['temperature'] <= batas_temp[1]) or not (batas_turb[0] <= row['turbidity'] <= batas_turb[1]):
            hasil_prediksi.append("Tidak Layak")
        else:
            data_scaled = scaler.transform([row])
            hasil_prediksi.append(model.predict(data_scaled)[0])
    
    return hasil_prediksi