# backend/services/logic.py
from backend.services.tuya_control import turn_on, turn_off, set_brightness
from backend.config.settings import settings

buffer = []

def update_buffer(data):
    buffer.append(data)
    if len(buffer) > settings.BUFFER_SIZE:
        buffer.pop(0)

def compute_average():
    if not buffer:
        return None

    keys = ["temp","humidity","light","air","sound","motion","movement"]
    avg = {k: 0 for k in keys}

    for d in buffer:
        for k in keys:
            avg[k] += d[k]

    for k in avg:
        avg[k] /= len(buffer)

    return avg

def compute_score(current, avg):
    if avg is None:
        return 100

    score = 100

    score -= abs(current["temp"] - avg["temp"]) * 5
    score -= abs(current["light"] - avg["light"]) * 0.2
    score -= abs(current["sound"] - avg["sound"]) * 0.02
    score -= abs(current["air"] - avg["air"]) * 0.01

    if current["motion"] == 1:
        score -= 10

    score -= abs(current["movement"] - avg["movement"]) * 50

    return max(score, 0)

def decide_action(score, current, avg, mode, feedback):
    if avg is None:
        return {
            "action": "NONE",
            "brightness": 0,
            "power": False
        }

    # 🔥 MANUAL MODE
    if mode == "manual":
        if feedback > 2:
            return {
                "action": "INCREASE_COMFORT",
                "brightness": 800,
                "power": True
            }
        elif feedback < -2:
            return {
                "action": "DECREASE_COMFORT",
                "brightness": 200,
                "power": True
            }

        return {
            "action": "STABLE",
            "brightness": 500,
            "power": True
        }

    # 🔥 DYNAMIC MODE
    dTemp = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]
    dMove = current["movement"] - avg["movement"]

    # 🌡️ Too hot → dim light + AC
    if score < 60 and dTemp > 1.5:
        return {
            "action": "AC_COOL",
            "brightness": 300,
            "power": True
        }

    # 🔊 Noise → very dim
    elif score < 60 and dSound > 500:
        return {
            "action": "NOISE_ALERT",
            "brightness": 100,
            "power": True
        }

    # 🧠 Restless → soft dim
    elif score < 60 and dMove > 0.2:
        return {
            "action": "RESTLESS_SLEEP",
            "brightness": 150,
            "power": True
        }

    # 😴 Good sleep → turn OFF
    elif score > 85:
        return {
            "action": "SLEEP_OPTIMAL",
            "brightness": 0,
            "power": False
        }

    # 🙂 Normal
    return {
        "action": "STABLE",
        "brightness": 500,
        "power": True
    }