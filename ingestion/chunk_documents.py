"""
Document chunking for the SMIT ingestion pipeline.

Changes vs original:
  - Title prepend is now conditional: skip if the title is longer than
    60 chars (it's a filename, not a heading) or is already present at
    the start of the chunk text.  The original prepend inflated chunks
    beyond CHUNK_SIZE for PDF documents with long filenames.
  - Minimum chunk length raised to MIN_CHUNK_LENGTH (config.py) from the
    hardcoded 30, which let single-line headers through as standalone chunks.
  - Whitespace normalised before storing: multiple blank lines and runs of
    spaces are collapsed so embeddings are more stable.
"""

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE, MIN_CHUNK_LENGTH

# Maximum title length to consider as a meaningful heading worth prepending.
# Longer strings are PDF filenames, not document titles.
_MAX_TITLE_PREPEND_LEN = 60

_MULTI_BLANK = re.compile(r"\n{3,}")
_MULTI_SPACE  = re.compile(r" {2,}")


def _normalize_whitespace(text: str) -> str:
    text = _MULTI_BLANK.sub("\n\n", text)
    text = _MULTI_SPACE.sub(" ", text)
    return text.strip()


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    enriched_chunks: list[Document] = []
    for chunk in chunks:
        text = _normalize_whitespace(chunk.page_content)

        if len(text) < MIN_CHUNK_LENGTH:
            continue

        title = chunk.metadata.get("title", "").strip()

        # Prepend title only when it's a short, meaningful heading that isn't
        # already present at the start of the chunk.
        if (
            title
            and len(title) <= _MAX_TITLE_PREPEND_LEN
            and not text.lower().startswith(title.lower())
        ):
            text = f"{title}: {text}"

        enriched_chunks.append(
            Document(page_content=text, metadata=chunk.metadata)
        )

    print(f"Created {len(enriched_chunks)} chunks from {len(documents)} documents")
    return enriched_chunks