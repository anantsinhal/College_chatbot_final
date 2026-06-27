import json

with open("data/processed/all_documents.json", encoding="utf-8") as f:
    docs = json.load(f)

targets = [
    "https://smu.edu.in/smit/btech-in-computer-science.php",
    "https://smu.edu.in/smit/btech-in-civil-engineering.php",
    "https://smu.edu.in/smit/achievements.php",
]

print("Total documents:", len(docs))
for d in docs:
    if d["metadata"].get("source") in targets:
        print(d["metadata"]["source"], "| content length:", len(d["content"]))