import json
import os
import random
import string
from datetime import datetime, timedelta

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_license(user_id, plan):
    now = datetime.now()
    date_str = now.strftime("%Y%m%d%H%M")
    half_id = str(user_id)[:len(str(user_id)) // 2]
    rand_letters = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
    license_key = f"{user_id}{half_id}{date_str}{rand_letters}"
    return license_key

def save_user(user_id, license_key):
    data = load_users()
    now = datetime.now()
    plan_duration = timedelta(days=7 if "week" in license_key else 30)
    start_date = now.strftime("%Y-%m-%d %H:%M")
    end_date = (now + plan_duration).strftime("%Y-%m-%d %H:%M")
    data[str(user_id)] = {
        "status": "active",
        "plan": "week" if "week" in license_key else "month",
        "start_date": start_date,
        "end_date": end_date,
        "license": license_key
    }
    save_users(data)

def validate_license(user_id, license_key):
    user_id = str(user_id)
    if not license_key.startswith(user_id):
        return False
    data = load_users()
    for uid, info in data.items():
        if info["license"] == license_key:
            if uid != user_id:
                return False  # licence volée
            return True
    return True  # première utilisation

def is_authorized(user_id):
    user_id = str(user_id)
    data = load_users()
    if user_id in data and data[user_id]["status"] == "active":
        now = datetime.now()
        end = datetime.strptime(data[user_id]["end_date"], "%Y-%m-%d %H:%M")
        if now < end:
            return True
    return False
