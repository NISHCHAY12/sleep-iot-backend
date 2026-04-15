# backend/main.py

from flask import Flask
from flask_cors import CORS
from routes.sensor import sensor_bp
from routes.control import control_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(sensor_bp)
app.register_blueprint(control_bp)


@app.route("/")
def home():
    return "🚀 IoT Backend Running with Firebase"


if __name__ == "__main__":
    print("🚀 Starting backend server...")
    app.run(host="0.0.0.0", port=10000)