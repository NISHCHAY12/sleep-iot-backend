# backend/config/settings.py

import os

class Settings:
    BUFFER_SIZE = 60
    FIREBASE_URL = "https://iot-project-72cfe-default-rtdb.asia-southeast1.firebasedatabase.app/"
    
    # Optional future configs
    DEFAULT_MODE = "dynamic"
    DEFAULT_POWER = True

settings = Settings()