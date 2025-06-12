# Cek anomali data
def is_anomaly(data):
    pH, temp, turb = data
    if not (4.0 <= pH <= 9.0): return True
    if not (20 <= temp <= 33): return True
    if not (0 <= turb <= 100): return True
    return False
