# backend/services/sleep_model.py

def estimate_sleep_score(sensor_data):
    """
    Placeholder for ML model
    Currently returns computed score directly
    """
    return sensor_data.get("score", 75)