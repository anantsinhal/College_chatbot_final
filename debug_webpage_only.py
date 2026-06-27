from rag.retriever import vectorstore

results = vectorstore.similarity_search_with_score(
    "What B.Tech programs does SMIT offer?",
    k=10,
    filter={"type": "webpage"}
)
for doc, score in results:
    print(f"{score:.4f} | {doc.metadata.get('source')}")
    print("   ", doc.page_content[:150])
    print()