


from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    enriched_chunks = []
    for chunk in chunks:
        text = chunk.page_content.strip()
        if len(text) < 30:
            continue

        title = chunk.metadata.get("title", "").strip()
        if title and not text.startswith(title):
            text = f"{title}: {text}"

        enriched_chunks.append(Document(page_content=text, metadata=chunk.metadata))

    print(f"Created {len(enriched_chunks)} chunks from {len(documents)} documents")
    return enriched_chunks
