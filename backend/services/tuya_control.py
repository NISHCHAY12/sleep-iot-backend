from tuya_iot import TuyaOpenAPI

ACCESS_ID = "p7jfuhsa9akgqweh3sev"
ACCESS_SECRET = "1c0066795102439587338992cd001f26"

# 🔁 TRY BOTH IF NEEDED
ENDPOINT = "https://openapi.tuyain.com"
# ENDPOINT = "https://openapi.tuyaeu.com"

DEVICE_ID = "d7d60bf49a939a90beu3xq"

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)


def ensure_connection():
    try:
        if not openapi.token_info:
            print("🔄 Connecting to Tuya...")
            openapi.connect()
            print("✅ Tuya Connected")
    except Exception as e:
        print("❌ Tuya Connect Error:", e)


def turn_on():
    ensure_connection()
    try:
        res = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": [{"code": "switch_led", "value": True}]
        })
        print("💡 TURN ON:", res)
        return res
    except Exception as e:
        print("❌ TURN ON ERROR:", e)
        return {"error": str(e)}


def turn_off():
    ensure_connection()
    try:
        res = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": [{"code": "switch_led", "value": False}]
        })
        print("💡 TURN OFF:", res)
        return res
    except Exception as e:
        print("❌ TURN OFF ERROR:", e)
        return {"error": str(e)}


def set_brightness(value):
    ensure_connection()
    try:
        res = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": [{"code": "bright_value_v2", "value": int(value)}]
        })
        print("💡 BRIGHTNESS:", res)
        return res
    except Exception as e:
        print("❌ BRIGHTNESS ERROR:", e)
        return {"error": str(e)}