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

    # 🔥 MANUAL MODE
    if mode == "manual":
        brightness = 500 + feedback * 100
        brightness = max(10, min(1000, brightness))

        return {
            "action": "MANUAL",
            "brightness": brightness
        }

    # 🔥 DYNAMIC MODE
    dTemp  = current["temp"] - avg["temp"]
    dSound = current["sound"] - avg["sound"]
    dMove  = current["movement"] - avg["movement"]
    light  = current["light"]

    # 🔥 LIGHT CONTROL (THIS WAS MISSING EARLIER!)
    if light > 200:
        return {
            "action": "TOO_BRIGHT",
            "brightness": 5   # dim bulb
        }
    
    if light > 20 and light < 200:
        return {
            "action": "Ideal_Light",
            "brightness": 50   
        }
    
    if light < 20:
        return {
            "action": "TOO_DARK",
            "brightness": 500   
        }

    # 🌡️ TEMP
    if score < 60 and dTemp > 1.5:
        return {"action": "AC_COOL", "brightness": 300}

    # 🔊 SOUND
    if score < 60 and dSound > 500:
        return {"action": "NOISE_ALERT", "brightness": 100}

    # 🧠 MOVEMENT
    if score < 60 and dMove > 0.2:
        return {"action": "RESTLESS_SLEEP", "brightness": 150}

    # 😴 GOOD SLEEP
    return {
        "action": "SLEEP_OPTIMAL",
        "brightness": 50
    }