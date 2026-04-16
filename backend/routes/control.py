from flask import Blueprint, jsonify, request

from backend.services.state import system_state
from backend.services.tuya_control import turn_on, turn_off, set_brightness

control_bp = Blueprint("control", __name__)


# -----------------------------
# SYSTEM CONTROL
# -----------------------------

@control_bp.route("/toggle", methods=["POST"])
def toggle():
    system_state["power"] = not system_state["power"]
    return jsonify({
        "status": "ok",
        "power": system_state["power"]
    })


@control_bp.route("/mode/<mode>", methods=["POST"])
def set_mode(mode):
    if mode not in ["manual", "dynamic"]:
        return jsonify({"error": "Invalid mode"}), 400

    system_state["mode"] = mode

    return jsonify({
        "status": "ok",
        "mode": system_state["mode"]
    })


@control_bp.route("/feedback/<int:value>", methods=["POST"])
def feedback(value):
    if value < -5 or value > 5:
        return jsonify({"error": "Range -5 to 5"}), 400

    system_state["feedback"] = value

    return jsonify({
        "status": "ok",
        "feedback": system_state["feedback"]
    })


# -----------------------------
# LIGHT CONTROL (MANUAL API)
# -----------------------------

@control_bp.route("/light/on", methods=["POST"])
def light_on():
    try:
        res = turn_on()
        return jsonify({
            "status": "success",
            "action": "ON",
            "tuya": res
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@control_bp.route("/light/off", methods=["POST"])
def light_off():
    try:
        res = turn_off()
        return jsonify({
            "status": "success",
            "action": "OFF",
            "tuya": res
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@control_bp.route("/light/brightness/<int:value>", methods=["POST"])
def light_brightness(value):
    if value < 10 or value > 1000:
        return jsonify({"error": "Brightness must be 10–1000"}), 400

    try:
        res = set_brightness(value)
        return jsonify({
            "status": "success",
            "brightness": value,
            "tuya": res
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500