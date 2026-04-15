# backend/services/logic.py

from config.settings import settings

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
        return "NONE"

    # 🔥 MANUAL MODE
    if mode == "manual":
        if feedback > 2:
            return "INCREASE_COMFORT"
        elif feedback < -2:
            return "DECREASE_COMFORT"
        return "STABLE"

    # 🔥 DYNAMIC MODE
    dTemp = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]
    dMove = current["movement"] - avg["movement"]

    if score < 60 and dTemp > 1.5:
        return "AC_COOL"
    elif score < 60 and dSound > 500:
        return "NOISE_ALERT"
    elif score < 60 and dMove > 0.2:
        return "RESTLESS_SLEEP"

    return "NONE"