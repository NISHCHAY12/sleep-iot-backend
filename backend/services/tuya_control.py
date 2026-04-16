from tuya_iot import TuyaOpenAPI

ACCESS_ID = "p7jfuhsa9akgqweh3sev"
ACCESS_SECRET = "1c0066795102439587338992cd001f26"
ENDPOINT = "https://openapi.tuya.in"  # India

DEVICE_ID = "d7d60bf49a939a90beu3xq"

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
openapi.connect()


def turn_on():
    return openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "switch_led", "value": True}]
    })


def turn_off():
    return openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "switch_led", "value": False}]
    })


def set_brightness(value):
    return openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "bright_value_v2", "value": value}]
    })