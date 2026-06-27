from rag.chain import qa_chain

result = qa_chain.invoke({"question": "What B.Tech programs does SMIT offer?", "chat_history": []})
print(result["answer"])
print("\nSources:")
for doc in result["source_documents"]:
    print(" -", doc.metadata.get("source"))