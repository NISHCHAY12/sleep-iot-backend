from flask import Blueprint, request, jsonify

from backend.services.logic import (
    update_buffer,
    compute_average,
    compute_score,
    decide_action
)

from backend.services.state import system_state
from backend.config.firebase import get_ref

# 🔥 TUYA CONTROL
from backend.services.tuya_control import set_brightness

sensor_bp = Blueprint("sensor", __name__)

latest_data = {}


@sensor_bp.route("/data", methods=["POST"])
def receive_data():
    global latest_data

    # 🔒 SYSTEM POWER CHECK
    if not system_state["power"]:
        return jsonify({"status": "system_off"})

    data = request.json
    print("📥 Incoming data:", data)

    required = ["temp", "humidity", "light", "air", "sound", "motion", "movement"]

    for key in required:
        if key not in data:
            return jsonify({"error": f"Missing {key}"}), 400

    # -------------------------
    # PROCESSING
    # -------------------------
    update_buffer(data)

    avg = compute_average()
    score = compute_score(data, avg)

    latest_data = data.copy()
    latest_data["sleep_score"] = round(score, 2)

    action = decide_action(
        score,
        data,
        avg,
        system_state["mode"],
        system_state["feedback"]
    )

    print("➡️ ACTION:", action)

    # -------------------------
    # 🔥 TUYA CONTROL
    # -------------------------
    try:
        try:
            brightness = int(action["brightness"])

            if brightness <= 0:
                print("💡 Turning OFF bulb")
                turn_off()
            else:
                print(f"💡 Setting brightness: {brightness}")
                turn_on()
                set_brightness(max(10, brightness))

        except Exception as e:
            print("❌ Tuya Control Error:", e)

    except Exception as e:
        print("❌ Tuya Control Error:", e)

    # -------------------------
    # FIREBASE STORE
    # -------------------------
    try:
        ref = get_ref()
        ref.push({
            **latest_data,
            "action": action["action"],
            "brightness": action["brightness"],
            "power": system_state["power"],   # ✅ FIXED
            "mode": system_state["mode"]
        })
        print("🔥 Firebase WRITE SUCCESS")

    except Exception as e:
        print("❌ Firebase ERROR:", e)

    # -------------------------
    # RESPONSE TO ESP
    # -------------------------
    return jsonify({
        "sleep_score": round(score, 2),
        "action": action["action"],
        "brightness": action["brightness"],
        "power": system_state["power"],   # ✅ FIXED
        "mode": system_state["mode"]
    })


# -------------------------
# STATUS API
# -------------------------
@sensor_bp.route("/status", methods=["GET"])
def status():
    try:
        ref = get_ref()
        data = ref.order_by_key().limit_to_last(1).get()

        if data:
            latest = list(data.values())[0]
        else:
            latest = {}

        return jsonify({
            **latest,
            **system_state   # ✅ OVERRIDE LAST
        })

    except Exception as e:
        print("❌ Firebase READ ERROR:", e)
        return jsonify(system_state)