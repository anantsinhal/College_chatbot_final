from rag.chain import qa_chain

chat_history = []

print("SMIT Chatbot Ready")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break

    result = qa_chain.invoke(
        {
            "question": query,
            "chat_history": chat_history
        }
    )

    print("\nBot:")
    print(result["answer"])

    print("\nSources:")

    for doc in result["source_documents"]:

        print(doc.metadata["source"])

    chat_history.append(
        (query, result["answer"])
    )

    print("-" * 50)