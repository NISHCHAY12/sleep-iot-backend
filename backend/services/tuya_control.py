import time
import hmac
import hashlib
import requests
import json

ACCESS_ID = "vrr3esusx4kumgrjatpj"
ACCESS_SECRET = "0d7f8327ff3c4b4987217227c7c6e733"
ENDPOINT = "https://openapi.tuyain.com"

DEVICE_ID = "d7d60bf49a939a90beu3x"


def _hmac_sign(secret: str, message: str) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest().upper()


def get_token():
    t = str(int(time.time() * 1000))
    path = "/v1.0/token?grant_type=1"

    # String-to-sign for GET with no body and no access_token
    content_hash = hashlib.sha256(b"").hexdigest()
    string_to_sign = f"GET\n{content_hash}\n\n{path}"
    sign_str = ACCESS_ID + t + string_to_sign

    sign = _hmac_sign(ACCESS_SECRET, sign_str)

    headers = {
        "client_id": ACCESS_ID,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
    }

    res = requests.get(f"{ENDPOINT}{path}", headers=headers).json()
    print("🔑 TOKEN RESPONSE:", res)

    if not res.get("success"):
        raise Exception(res)

    return res["result"]["access_token"]


def send_command(commands):
    token = get_token()
    t = str(int(time.time() * 1000))
    path = f"/v1.0/devices/{DEVICE_ID}/commands"

    body = json.dumps({"commands": commands}, separators=(",", ":"))

    # String-to-sign for POST with body and access_token
    content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    string_to_sign = f"POST\n{content_hash}\n\n{path}"
    sign_str = ACCESS_ID + token + t + string_to_sign

    sign = _hmac_sign(ACCESS_SECRET, sign_str)

    headers = {
        "client_id": ACCESS_ID,
        "access_token": token,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
        "Content-Type": "application/json",
    }

    res = requests.post(f"{ENDPOINT}{path}", data=body, headers=headers).json()
    print("💡 RESPONSE:", res)
    return res


def turn_on():
    return send_command([{"code": "switch_led", "value": True}])


def turn_off():
    return send_command([{"code": "switch_led", "value": False}])


def set_brightness(value):
    return send_command([{"code": "bright_value_v2", "value": int(value)}])