import json

with open("data/raw/smit_pages.json", encoding="utf-8") as f:
    pages = json.load(f)

targets = [
    "https://smu.edu.in/smit/btech-in-computer-science.php",
    "https://smu.edu.in/smit/btech-in-civil-engineering.php",
    "https://smu.edu.in/smit/achievements.php",
]

for p in pages:
    if p["source"] in targets:
        print(p["source"], "| content length:", len(p["content"]))