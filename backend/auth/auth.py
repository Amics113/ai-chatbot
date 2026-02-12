import json
from pathlib import Path
from fastapi import HTTPException

USERS_FILE = Path("data/users.json")

# Ensure file exists
if not USERS_FILE.exists():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text("{}")

def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def register_user(username: str, password: str):
    users = load_users()

    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[username] = password
    save_users(users)

def authenticate_user(username: str, password: str) -> bool:
    users = load_users()
    return users.get(username) == password
