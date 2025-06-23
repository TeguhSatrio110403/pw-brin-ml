# Cek anomali data
def is_anomaly(data):
    pH, temp, turb = data
    reasons = []
    if not (4.0 <= pH <= 9.0):
        reasons.append('pH di luar rentang normal (4.0 - 9.0)')
    if not (20 <= temp <= 33):
        reasons.append('Suhu di luar rentang normal (20 - 33)')
    if not (0 <= turb < 100):
        reasons.append('Kekeruhan di luar rentang normal (0 - 100)')
    if reasons:
        return True, ', '.join(reasons)
    return False, ''
