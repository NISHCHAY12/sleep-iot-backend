import time
import hmac
import hashlib
import requests

ACCESS_ID = "vrr3esusx4kumgrjatpj"
ACCESS_SECRET = "0d7f8327ff3c4b4987217227c7c6e733"

# 🔁 Try this first
ENDPOINT = "https://openapi.tuyain.com"
# If still fails → use:
# ENDPOINT = "https://openapi.tuyaeu.com"

DEVICE_ID = "d7d60bf49a939a90beu3xq"


def get_token():
    url = f"{ENDPOINT}/v1.0/token?grant_type=1"
    t = str(int(time.time() * 1000))

    sign_str = ACCESS_ID + t
    sign = hmac.new(
        ACCESS_SECRET.encode(),
        sign_str.encode(),
        hashlib.sha256
    ).hexdigest().upper()

    headers = {
        "client_id": ACCESS_ID,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256"
    }

    res = requests.get(url, headers=headers).json()
    print("🔑 TOKEN RESPONSE:", res)

    return res["result"]["access_token"]


def send_command(commands):
    token = get_token()

    url = f"{ENDPOINT}/v1.0/devices/{DEVICE_ID}/commands"
    t = str(int(time.time() * 1000))

    body = {"commands": commands}

    sign_str = ACCESS_ID + token + t + "POST\n" + hashlib.sha256(
        str(body).encode()
    ).hexdigest()

    sign = hmac.new(
        ACCESS_SECRET.encode(),
        sign_str.encode(),
        hashlib.sha256
    ).hexdigest().upper()

    headers = {
        "client_id": ACCESS_ID,
        "access_token": token,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=body, headers=headers).json()
    print("💡 TUYA RESPONSE:", res)

    return res


def turn_on():
    return send_command([{"code": "switch_led", "value": True}])


def turn_off():
    return send_command([{"code": "switch_led", "value": False}])


def set_brightness(value):
    return send_command([{"code": "bright_value_v2", "value": int(value)}])