from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL, RETRIEVER_FETCH_K, RETRIEVER_K

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": RETRIEVER_K,
        "fetch_k": RETRIEVER_FETCH_K,
        "lambda_mult": 0.5,  # balance relevance vs. diversity
    },
)
