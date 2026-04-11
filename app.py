from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-project-72cfe-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

BUFFER_SIZE = 60

buffer = []


def compute_average():
    if not buffer:
        return None

    avg = {
        "temp": 0,
        "humidity": 0,
        "light": 0,
        "air": 0,
        "sound": 0,
        "motion": 0
    }

    for d in buffer:
        avg["temp"] += d["temp"]
        avg["humidity"] += d["humidity"]
        avg["light"] += d["light"]
        avg["air"] += d["air"]
        avg["sound"] += d["sound"]
        avg["motion"] += d["motion"]

    count = len(buffer)

    for key in avg:
        avg[key] /= count

    return avg


def compute_score(current, avg):
    if avg is None:
        return 100

    score = 100

    # Deviation-based scoring
    score -= abs(current["temp"] - avg["temp"]) * 5
    score -= abs(current["light"] - avg["light"]) * 0.2
    score -= abs(current["sound"] - avg["sound"]) * 0.02
    score -= abs(current["air"] - avg["air"]) * 0.01

    if current["motion"] == 1:
        score -= 15

    return max(score, 0)


def decide_action(score, current, avg):
    action = "NONE"

    if avg is None:
        return action

    # Dynamic logic (not constant thresholds)
    dTemp = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]

    if score < 60 and dTemp > 1.5:
        action = "AC_COOL"

    elif score < 60 and dSound > 500:
        action = "NOISE_ALERT"

    return action


# -------- ROUTES --------

@app.route('/')
def home():
    return "Flask Backend Running 🚀"


@app.route('/data', methods=['POST'])
def receive_data():
    global buffer

    data = request.json

    # ---- Validate ----
    required_keys = ["temp", "humidity", "light", "air", "sound", "motion"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing {key}"}), 400

    # ---- Store in buffer ----
    buffer.append(data)

    if len(buffer) > BUFFER_SIZE:
        buffer.pop(0)

    # ---- Compute ----
    avg = compute_average()
    score = compute_score(data, avg)
    action = decide_action(score, data, avg)

    ref = db.reference("sensor_data")

    ref.push({
        "temp": data["temp"],
        "humidity": data["humidity"],
        "light": data["light"],
        "air": data["air"],
        "sound": data["sound"],
        "motion": data["motion"],
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