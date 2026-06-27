import json

with open("data/raw/smit_pages.json", encoding="utf-8") as f:
    pages = json.load(f)

print("Pages in smit_pages.json:", len(pages))

from config import MIN_CONTENT_LENGTH
print("MIN_CONTENT_LENGTH:", MIN_CONTENT_LENGTH)

too_short = [p for p in pages if len(p["content"]) < MIN_CONTENT_LENGTH]
print("Pages below min length:", len(too_short))

sources = [p["source"] for p in pages]
unique_sources = set(sources)
print("Unique sources:", len(unique_sources))
print("Duplicate sources:", len(sources) - len(unique_sources))