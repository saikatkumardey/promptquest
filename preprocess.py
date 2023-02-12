# %%
from utils import load_json, save_json
from pathlib import Path
import os
import json
import joblib

data_path = Path("data")


def extract_messages(file):
    messages = []
    with open(file) as f:
        data = json.load(f)
        for message in data["messages"]:
            for content in message:
                messages.append(
                    {
                        "prompt": content["content"],
                        "images": [
                            item.get("url") for item in content["attachments"]
                        ],
                    }
                )
    return messages


data = []
for dirname, _, filenames in os.walk(data_path / "midjourney-raw"):
    # call extract_messages in paralllel using joblib
    data += joblib.Parallel(n_jobs=-1)(
        joblib.delayed(extract_messages)(os.path.join(dirname, filename))
        for filename in filenames
    )
# flatten data
data = [item for sublist in data for item in sublist]

# %%

# clean rows with empty data['images']

data = [item for item in data if item["images"]]

save_json(data, data_path / "midjourney-prompts.json")

# %%


# given a prompt like '**some stuff** xyz', keep only the text within ** **
def extract_text(prompt):
    if prompt.startswith("**"):
        return prompt.split("**")[1]
    return prompt


from cleantext import clean

data = load_json(data_path / "midjourney-prompts.json")
for item in data:
    item["prompt"] = extract_text(item["prompt"])
    item["prompt"] = clean(
        item["prompt"],
        no_line_breaks=True,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=False,
        no_digits=False,
        no_currency_symbols=False,
        no_punct=False,
        lang="en",
    )

# %%
for item in data:
    item["prompt"] = item["prompt"].replace("<<url>", "").strip()

# remove empty prompts
data = [item for item in data if item["prompt"]]
# %%
save_json(data, data_path / "midjourney-cleaned.json")

# %%
