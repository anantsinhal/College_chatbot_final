import sys
from rag.retriever import vectorstore
from rag.chain import qa_chain

mode = sys.argv[1] if len(sys.argv) > 1 else "ask"

if mode == "ask":
    question = sys.argv[2]
    result = qa_chain.invoke({"question": question, "chat_history": []})
    print(result["answer"])
    print("\nSources:")
    for doc in result["source_documents"]:
        print(" -", doc.metadata.get("source"))

elif mode == "raw":
    question = sys.argv[2]
    results = vectorstore.similarity_search_with_score(question, k=10)
    for doc, score in results:
        print(f"{score:.4f} | {doc.metadata.get('source')}")
        print("   ", doc.page_content[:150])
        print()

elif mode == "page":
    source_url = sys.argv[2]
    results = vectorstore.get(where={"source": source_url})
    for doc in results["documents"]:
        print(doc[:300])
        print("---")

elif mode == "webonly":
    question = sys.argv[2]
    results = vectorstore.similarity_search_with_score(question, k=10, filter={"type": "webpage"})
    for doc, score in results:
        print(f"{score:.4f} | {doc.metadata.get('source')}")
        print("   ", doc.page_content[:150])
        print()