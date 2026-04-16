# backend/main.py

import os
from flask import Flask
from flask_cors import CORS
from backend.routes.sensor import sensor_bp
from backend.routes.control import control_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(sensor_bp)
app.register_blueprint(control_bp)


@app.route("/")
def home():
    return "🚀 IoT Backend Running with Firebase"


if __name__ == "__main__":
    print("🚀 Starting backend server...")

    # 🔥 IMPORTANT FIX
    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)