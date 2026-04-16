from tuya_iot import TuyaOpenAPI

ACCESS_ID = "p7jfuhsa9akgqweh3sev"
ACCESS_SECRET = "1c0066795102439587338992cd001f26"

# 🔁 Try this first
ENDPOINT = "https://openapi.tuyain.com"
# If still fails → use:
# ENDPOINT = "https://openapi.tuyaeu.com"

DEVICE_ID = "d7d60bf49a939a90beu3xq"

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)


def refresh_token():
    try:
        print("🔄 Refreshing Tuya token...")
        openapi.connect()
        print("✅ Token refreshed")
    except Exception as e:
        print("❌ Token refresh failed:", e)


def send_command(commands):
    refresh_token()   # 🔥 ALWAYS refresh before request

    try:
        res = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": commands
        })

        print("📡 TUYA RESPONSE:", res)
        return res

    except Exception as e:
        print("❌ TUYA ERROR:", e)
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
        {"code": "bright_value_v2", "value": int(value)}
    ])