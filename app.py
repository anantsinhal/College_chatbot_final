"""
Simple CLI loop for testing the chatbot before the Streamlit frontend is
built. Run with: python app.py
"""

from rag.chain import qa_chain

# Only the most recent N turns are sent to the condense-question step.
# Without this cap, a long session keeps accumulating every prior
# question/answer, increasing the chance that an old, unrelated topic
# (e.g. fees) leaks into the rewrite of a brand-new question (e.g.
# admissions) -- which is exactly what caused inconsistent answers
# during testing. Keeping a short rolling window still allows genuine
# follow-ups ("what about its fees?") to work, without letting the
# whole conversation pile up.
MAX_HISTORY_TURNS = 3

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
    chat_history = chat_history[-MAX_HISTORY_TURNS:]

    print("-" * 50)