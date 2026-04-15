# backend/config/firebase.py

import os
import json
import firebase_admin
from firebase_admin import credentials, db

print("🔍 Initializing Firebase...")

firebase_key_raw = os.environ.get("FIREBASE_KEY")

if not firebase_key_raw:
    raise Exception("❌ FIREBASE_KEY not set in Railway")

firebase_key = json.loads(firebase_key_raw)

cred = credentials.Certificate(firebase_key)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-project-72cfe-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

print("🔥 Firebase initialized successfully")

def get_ref():
    return db.reference("sensor_data")