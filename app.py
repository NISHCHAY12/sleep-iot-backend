from flask import Flask, request, jsonify
import os
import json
import firebase_admin
from firebase_admin import credentials, db

firebase_key = json.loads(os.environ["FIREBASE_KEY"])

cred = credentials.Certificate(firebase_key)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-project-72cfe-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

app = Flask(__name__)

BUFFER_SIZE = 60
buffer = []

# -------- AVERAGE --------
def compute_average():
    if not buffer:
        return None

    avg = {
        "temp": 0,
        "humidity": 0,
        "light": 0,
        "air": 0,
        "sound": 0,
        "motion": 0,
        "movement": 0   # 🔥 NEW
    }

    for d in buffer:
        avg["temp"] += d["temp"]
        avg["humidity"] += d["humidity"]
        avg["light"] += d["light"]
        avg["air"] += d["air"]
        avg["sound"] += d["sound"]
        avg["motion"] += d["motion"]
        avg["movement"] += d["movement"]  # 🔥 NEW

    count = len(buffer)

    for key in avg:
        avg[key] /= count

    return avg

# -------- SCORE --------
def compute_score(current, avg):
    if avg is None:
        return 100

    score = 100

    # Existing factors
    score -= abs(current["temp"] - avg["temp"]) * 5
    score -= abs(current["light"] - avg["light"]) * 0.2
    score -= abs(current["sound"] - avg["sound"]) * 0.02
    score -= abs(current["air"] - avg["air"]) * 0.01

    # 🔥 MOTION (binary)
    if current["motion"] == 1:
        score -= 10

    # 🔥 NEW: CONTINUOUS MOVEMENT PENALTY
    movement_diff = abs(current["movement"] - avg["movement"])
    score -= movement_diff * 50   # 🔥 very important weight

    return max(score, 0)

# -------- ACTION --------
def decide_action(score, current, avg):
    action = "NONE"

    if avg is None:
        return action

    dTemp = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]
    dMove = current["movement"] - avg["movement"]

    if score < 60 and dTemp > 1.5:
        action = "AC_COOL"

    elif score < 60 and dSound > 500:
        action = "NOISE_ALERT"

    elif score < 60 and dMove > 0.2:
        action = "RESTLESS_SLEEP"   # 🔥 NEW

    return action

# -------- ROUTES --------
@app.route('/')
def home():
    return "Flask Backend Running 🚀"

@app.route('/data', methods=['POST'])
def receive_data():
    global buffer

    data = request.json

    # 🔥 UPDATED REQUIRED KEYS
    required_keys = ["temp", "humidity", "light", "air", "sound", "motion", "movement"]

    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing {key}"}), 400

    # Store
    buffer.append(data)

    if len(buffer) > BUFFER_SIZE:
        buffer.pop(0)

    # Compute
    avg = compute_average()
    score = compute_score(data, avg)
    action = decide_action(score, data, avg)

    # Firebase
    ref = db.reference("sensor_data")

    ref.push({
        "temp": data["temp"],
        "humidity": data["humidity"],
        "light": data["light"],
        "air": data["air"],
        "sound": data["sound"],
        "motion": data["motion"],
        "movement": data["movement"],   # 🔥 NEW
        "score": round(score, 2)
    })

    return jsonify({
        "sleep_score": round(score, 2),
        "action": action,
        "buffer_size": len(buffer)
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "buffer_size": len(buffer),
        "message": "Backend running"
    })

# -------- MAIN --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)