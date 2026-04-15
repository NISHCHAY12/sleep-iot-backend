# backend/routes/control.py
from backend.services.state import system_state

from flask import Blueprint, jsonify

control_bp = Blueprint("control", __name__)


@control_bp.route("/toggle", methods=["POST"])
def toggle():
    system_state["power"] = not system_state["power"]
    return jsonify(system_state)

@control_bp.route("/mode/<mode>", methods=["POST"])
def set_mode(mode):
    if mode not in ["manual", "dynamic"]:
        return jsonify({"error": "Invalid mode"}), 400

    system_state["mode"] = mode
    return jsonify(system_state)

@control_bp.route("/feedback/<int:value>", methods=["POST"])
def feedback(value):
    if value < -5 or value > 5:
        return jsonify({"error": "Range -5 to 5"}), 400

    system_state["feedback"] = value
    return jsonify(system_state)