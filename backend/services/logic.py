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
        return "NONE"

    # 🔥 MANUAL MODE
    if mode == "manual":
        if feedback > 2:
            set_brightness(800)
            turn_on()
            return "INCREASE_COMFORT"

        elif feedback < -2:
            set_brightness(200)
            return "DECREASE_COMFORT"

        return "STABLE"

    # 🔥 DYNAMIC MODE
    dTemp = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]
    dMove = current["movement"] - avg["movement"]

    # 🌡️ Temperature too high → AC / cooling logic
    if score < 60 and dTemp > 1.5:
        set_brightness(300)  # dim light for comfort
        return "AC_COOL"

    # 🔊 Noise detected
    elif score < 60 and dSound > 500:
        set_brightness(100)  # very dim
        return "NOISE_ALERT"

    # 🧠 Restless sleep
    elif score < 60 and dMove > 0.2:
        set_brightness(150)
        return "RESTLESS_SLEEP"

    # 😴 Good sleep → turn off lights
    elif score > 85:
        turn_off()
        return "SLEEP_OPTIMAL"

    # 🙂 Normal case
    set_brightness(500)
    turn_on()
    return "STABLE"