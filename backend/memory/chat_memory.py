import json
import os

MEMORY_FILE = "backend/memory/chat_history.json"

def _load():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_message(username: str, role: str, message: str):
    data = _load()

    if username not in data:
        data[username] = []

    data[username].append({
        "role": role,
        "message": message
    })

    _save(data)

def get_memory(username: str) -> str:
    data = _load()
    if username not in data:
        return ""

    return "\n".join(
        f"{m['role']}: {m['message']}"
        for m in data[username]
    )
