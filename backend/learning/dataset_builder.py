import json

def build_dataset():
    dataset = []
    with open("learning_logs.json") as f:
        for line in f:
            data = json.loads(line)
            if data["rating"] >= 4:
                dataset.append({
                    "instruction": data["prompt"],
                    "output": data["response"]
                })

    with open("dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)

    print("LoRA dataset created")
