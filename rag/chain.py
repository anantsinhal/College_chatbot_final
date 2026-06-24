from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains import ConversationalRetrievalChain

from rag.retriever import retriever

from config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)