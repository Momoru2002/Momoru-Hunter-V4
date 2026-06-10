# momoru/config.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Karena berada di momoru/config.py, kita butuh .parent.parent untuk keluar ke root project (Momoru-hunter-V4)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables dari file .env di root project
load_dotenv(dotenv_path=ROOT_DIR / ".env")

def load_config():
    config_path = ROOT_DIR / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"⚠️ File konfigurasi tidak ditemukan di {config_path}")

    with open(config_path, "r", encoding="utf-8") as stream:
        try:
            config_data = yaml.safe_load(stream)
        except yaml.YAMLError:
            raise RuntimeError("⚠️ Format penulisan pada file config.yaml salah/rusak!")

    # Injeksi data akun dari environment variables (.env) secara dinamis
    config_data["accounts"] = []
    index = 1
    while True:
        user = os.getenv(f"MOMORU_ACC_{index:02d}_USER")
        if not user:
            break  # Berhenti kalau sudah tidak ada lagi akun terdaftar di .env
            
        config_data["accounts"].append({
            "username": user,
            "email": os.getenv(f"MOMORU_ACC_{index:02d}_EMAIL"),
            "password": os.getenv(f"MOMORU_ACC_{index:02d}_PASS"),
            "proxy": os.getenv(f"MOMORU_ACC_{index:02d}_PROXY")
        })
        index += 1

    return config_data

# Inisialisasi global variable CONFIG
CONFIG = load_config()