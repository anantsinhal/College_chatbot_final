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
from ingestion.load_documents import load_all_documents
from ingestion.chunk_documents import chunk_documents


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


if __name__ == "__main__":
    print("=== Starting Vector Store Build Pipeline ===")
    
    # 1. Load web pages and PDFs
    print("Step 1: Loading raw documents...")
    raw_docs = load_all_documents()
    
    # 2. Chunk documents
    print("Step 2: Chunking documents...")
    chunks = chunk_documents(raw_docs)
    
    # 3. Create and persist ChromaDB vectorstore
    print("Step 3: Generating embeddings & storing in ChromaDB...")
    create_vectorstore(chunks)
    
    print("=== Ingestion Complete! ===")