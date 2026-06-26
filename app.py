"""
Simple CLI loop for testing the chatbot before the Streamlit frontend is
built. Run with: python app.py
"""

from rag.chain import qa_chain

chat_history = []

print("SMIT Chatbot Ready (type 'exit' to quit)\n")

while True:
    query = input("You: ").strip()

    if not query:
        continue
    if query.lower() == "exit":
        break

    result = qa_chain.invoke({"question": query, "chat_history": chat_history})

    print("\nBot:")
    print(result["answer"])

    sources = {doc.metadata.get("source", "unknown") for doc in result["source_documents"]}
    if sources:
        print("\nSources:")
        for source in sources:
            print(f"  - {source}")

    chat_history.append((query, result["answer"]))
    print("-" * 50)
