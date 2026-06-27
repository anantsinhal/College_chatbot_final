from rag.retriever import vectorstore

target_sources = [
    "https://smu.edu.in/smit/btech-in-computer-science.php",
    "https://smu.edu.in/smit/btech-in-civil-engineering.php",
    "https://smu.edu.in/smit/achievements.php",
]

all_docs = vectorstore.get(where={"type": "webpage"})
for source, doc, meta in zip(all_docs["ids"], all_docs["documents"], all_docs["metadatas"]):
    if meta.get("source") in target_sources:
        print(meta.get("source"))
        print("  ", doc[:200])
        print()