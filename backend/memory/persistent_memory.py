import json
import os

FILE_PATH = "backend/memory/chat_history.json"

# Ensure file exists
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump({}, f)


def load_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)


def add_message(username: str, role: str, content: str):
    data = load_data()

    if username not in data:
        data[username] = []

    data[username].append({
        "role": role,
        "content": content
    })

    save_data(data)


def get_memory(username: str) -> str:
    data = load_data()
    messages = data.get(username, [])

    return "\n".join(
        f"{m['role']}: {m['content']}" for m in messages
    )
