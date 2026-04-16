import time
import hashlib
import hmac
import requests

ACCESS_ID = "p7jfuhsa9akgqweh3sev"
ACCESS_SECRET = "1c0066795102439587338992cd001f26"
DEVICE_ID = "d7d60bf49a939a90beu3xq"

BASE_URL = "https://openapi.tuya.in"


def generate_sign(client_id, t, method, path, body=""):
    message = client_id + str(t) + method + path + body
    sign = hmac.new(
        ACCESS_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest().upper()
    return sign


def get_headers(method, path, body=""):
    t = int(time.time() * 1000)
    sign = generate_sign(ACCESS_ID, t, method, path, body)

    return {
        "client_id": ACCESS_ID,
        "sign": sign,
        "t": str(t),
        "sign_method": "HMAC-SHA256",
        "Content-Type": "application/json"
    }


def send_command(commands):
    path = f"/v1.0/devices/{DEVICE_ID}/commands"
    url = BASE_URL + path

    body = {"commands": commands}

    headers = get_headers("POST", path)

    try:
        res = requests.post(url, json=body, headers=headers)
        print("TUYA RESPONSE:", res.json())
        return res.json()
    except Exception as e:
        print("TUYA ERROR:", str(e))
        return {"error": str(e)}


def turn_on():
    return send_command([
        {"code": "switch_led", "value": True}
    ])


def turn_off():
    return send_command([
        {"code": "switch_led", "value": False}
    ])


def set_brightness(value):
    return send_command([
        {"code": "bright_value_v2", "value": value}
    ])