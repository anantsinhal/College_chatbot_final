"""
Embeds chunks and persists them into a Chroma vector store.

Improvements: uses the configured collection name (so retriever.py and
this file are guaranteed to point at the same collection), and wipes any
existing store at CHROMA_PATH before rebuilding -- otherwise re-running
ingestion repeatedly appends duplicate vectors instead of replacing them,
which is what most likely produced your bloated/duplicated 2160-chunk
store in the first place.
"""

import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL


def create_vectorstore(chunks: list[Document]) -> Chroma:
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    chroma_dir = Path(CHROMA_PATH)
    if chroma_dir.exists():
        print(f"Removing existing vector store at {CHROMA_PATH} before rebuild...")
        shutil.rmtree(chroma_dir)
    chroma_dir.mkdir(parents=True, exist_ok=True)

    print("Creating Chroma vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )

    print(f"Vector store created successfully with {len(chunks)} chunks.")
    return vectorstore
