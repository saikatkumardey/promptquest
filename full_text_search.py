# %%
import os
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
from utils import load_json

# Define the schema for the index
schema = Schema(prompt=TEXT(stored=True), images=KEYWORD(stored=True))

# Create the index
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = index.create_in("indexdir", schema)

# Open a writer to add the JSON document to the index
writer = ix.writer()


data = load_json("data/midjourney-cleaned.json")

# remove duplicate prompts
data = {item["prompt"]: item for item in data}.values()

# Add each prompt in the JSON document to the index
for item in data:
    writer.add_document(prompt=item["prompt"], images=str(item["images"]))

# Commit the changes to the index
writer.commit()

# Open a searcher to search the index
searcher = ix.searcher()

# %%

# Define the query
query = QueryParser("prompt", ix.schema).parse("dog happy")

# Search the index and retrieve the top 5 results
results = searcher.search(query, limit=5)

# Print the results
for result in results:
    print("Prompt:", result["prompt"])
    print("Images:", result["images"])
    print("\n")

# %%
