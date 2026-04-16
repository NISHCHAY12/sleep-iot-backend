import time
import hmac
import hashlib
import requests
import json

ACCESS_ID = "vrr3esusx4kumgrjatpj"
ACCESS_SECRET = "0d7f8327ff3c4b4987217227c7c6e733"
ENDPOINT = "https://openapi.tuyain.com"

DEVICE_ID = "d7d60bf49a939a90beu3xq"


def generate_sign(client_id, t, secret):
    sign_str = client_id + t
    return hmac.new(secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()


def get_token():
    t = str(int(time.time() * 1000))
    sign = generate_sign(ACCESS_ID, t, ACCESS_SECRET)

    headers = {
        "client_id": ACCESS_ID,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256"
    }

    url = f"{ENDPOINT}/v1.0/token?grant_type=1"
    res = requests.get(url, headers=headers).json()

    print("🔑 TOKEN RESPONSE:", res)

    if not res.get("success"):
        raise Exception(res)

    return res["result"]["access_token"]


def send_command(commands):
    token = get_token()
    t = str(int(time.time() * 1000))

    url_path = f"/v1.0/devices/{DEVICE_ID}/commands"

    # 🔥 IMPORTANT: EMPTY BODY HASH (official workaround)
    body_hash = hashlib.sha256(b"").hexdigest()

    sign_str = ACCESS_ID + token + t + body_hash

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

    url = ENDPOINT + url_path
    body = {"commands": commands}

    res = requests.post(url, json=body, headers=headers).json()

    print("💡 TUYA RESPONSE:", res)

    return res


def turn_on():
    return send_command([{"code": "switch_led", "value": True}])


def turn_off():
    return send_command([{"code": "switch_led", "value": False}])


def set_brightness(value):
    return send_command([{"code": "bright_value_v2", "value": int(value)}])