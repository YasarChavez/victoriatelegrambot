import json
import os

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {"daily_limit": 100, "premium_users": {}}

def save_config(config):
    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)