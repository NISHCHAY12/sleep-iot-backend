from backend.config.settings import settings

# 🔥 BUFFER FOR MOVING AVERAGE
buffer = []


# -------------------------------
# 📥 STORE DATA
# -------------------------------
def update_buffer(data):
    buffer.append(data)
    if len(buffer) > settings.BUFFER_SIZE:
        buffer.pop(0)


# -------------------------------
# 📊 COMPUTE AVERAGE
# -------------------------------
def compute_average():
    if not buffer:
        return None

    keys = ["temp", "humidity", "light", "air", "sound", "motion", "movement"]
    avg = {k: 0 for k in keys}

    for d in buffer:
        for k in keys:
            avg[k] += d[k]

    for k in avg:
        avg[k] /= len(buffer)

    return avg


# -------------------------------
# 🧠 COMPUTE SLEEP SCORE
# -------------------------------
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


# -------------------------------
# ⚙️ DECISION LOGIC
# -------------------------------
def decide_action(score, current, avg, mode, feedback):

    if avg is None:
        return {"action": "NONE", "brightness": 500}

    # ======================================
    # 🔥 MANUAL MODE (USER CONTROL)
    # ======================================
    if mode == "manual":
        brightness = 500 + (feedback * 100)

        # 🔥 Turn OFF if too low
        if brightness <= 0:
            return {
                "action": "MANUAL_OFF",
                "brightness": 0
            }

        brightness = min(1000, brightness)

        return {
            "action": "MANUAL",
            "brightness": brightness
        }

    # ======================================
    # 🔥 DYNAMIC MODE
    # ======================================
    dTemp  = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]
    dMove  = current["movement"] - avg["movement"]
    light  = current["light"]

    # ======================================
    # 🚨 PRIORITY 1: SLEEP DISTURBANCES
    # ======================================
    if score < 60 and dSound > 500:
        return {
            "action": "NOISE_ALERT",
            "brightness": 100
        }

    if score < 60 and dMove > 0.2:
        return {
            "action": "RESTLESS_SLEEP",
            "brightness": 150
        }

    if score < 60 and dTemp > 1.5:
        return {
            "action": "AC_COOL",
            "brightness": 300
        }

    # ======================================
    # 🌞 PRIORITY 2: LIGHT CONTROL
    # ======================================
    if light > 250:
        return {
            "action": "TOO_BRIGHT",
            "brightness": 0   # turn OFF
        }

    elif light > 150:
        return {
            "action": "BRIGHT",
            "brightness": 50
        }

    elif light > 50:
        return {
            "action": "NORMAL_LIGHT",
            "brightness": 150
        }

    else:
        return {
            "action": "TOO_DARK",
            "brightness": 400
        }

    # ======================================
    # 😴 DEFAULT FALLBACK
    # ======================================
    return {
        "action": "SLEEP_OPTIMAL",
        "brightness": 50
    }