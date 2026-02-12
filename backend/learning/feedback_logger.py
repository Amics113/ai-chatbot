import json
from datetime import datetime

FILE = "data/feedback.json"

def log_feedback(prompt, response, rating):
    entry = {
        "prompt": prompt,
        "response": response,
        "rating": rating,
        "time": datetime.now().isoformat()
    }

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
