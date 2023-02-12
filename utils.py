import json


# function to load json file
def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)


# function to save json file
def save_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
