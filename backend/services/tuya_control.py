from tuya_iot import TuyaOpenAPI

ACCESS_ID = "YOUR_ACCESS_ID"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"
ENDPOINT = "https://openapi.tuya.in"
DEVICE_ID = "YOUR_DEVICE_ID"

openapi = None


def get_api():
    global openapi
    if openapi is None:
        print("🔌 Connecting to Tuya...")
        openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
        openapi.connect()
        print("✅ Tuya Connected")
    return openapi


def turn_on():
    try:
        api = get_api()
        res = api.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": [{"code": "switch_led", "value": True}]
        })
        print("💡 TURN ON RESPONSE:", res)
        return res
    except Exception as e:
        print("❌ TUYA ERROR:", str(e))
        return {"error": str(e)}


def turn_off():
    try:
        api = get_api()
        res = api.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": [{"code": "switch_led", "value": False}]
        })
        print("💡 TURN OFF RESPONSE:", res)
        return res
    except Exception as e:
        print("❌ TUYA ERROR:", str(e))
        return {"error": str(e)}


def set_brightness(value):
    try:
        api = get_api()
        res = api.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
            "commands": [{"code": "bright_value_v2", "value": value}
        ]})
        print("🔆 BRIGHTNESS RESPONSE:", res)
        return res
    except Exception as e:
        print("❌ TUYA ERROR:", str(e))
        return {"error": str(e)}