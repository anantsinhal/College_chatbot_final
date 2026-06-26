"""
Loads the crawled page JSON and parsed PDF JSON into a single list of
LangChain Documents, ready for chunking.

This file existed in the original project but was empty -- there was no
actual code path that turned `data/raw/smit_pages.json` (and PDFs) into
Documents for the chunker. ingest.py now calls `load_all_documents()`.
"""

import json
import os

from langchain_core.documents import Document

from config import ALL_DOCS_JSON, MIN_CONTENT_LENGTH, PAGES_JSON, PDF_TEXT_JSON, PROCESSED_DIR
from ingestion.pdf_loader import load_pdfs


def load_scraped_pages() -> list[Document]:
    if not os.path.exists(PAGES_JSON):
        print(f"No scraped pages found at {PAGES_JSON}. Run the crawler first.")
        return []

    with open(PAGES_JSON, "r", encoding="utf-8") as f:
        pages = json.load(f)

    documents = []
    seen_sources = set()

    for page in pages:
        content = page.get("content", "")
        source = page.get("source", "")

        if len(content) < MIN_CONTENT_LENGTH:
            continue
        # Defensive de-dup in case the crawler ever produces duplicate
        # entries for the same normalized source.
        if source in seen_sources:
            continue
        seen_sources.add(source)

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": source,
                    "title": page.get("title", ""),
                    "type": "webpage",
                },
            )
        )

    print(f"Loaded {len(documents)} web page documents")
    return documents


def load_pdf_documents() -> list[Document]:
    # If PDFs were already parsed in a previous run, reuse the cached
    # JSON instead of re-parsing every PDF from scratch.
    if os.path.exists(PDF_TEXT_JSON):
        with open(PDF_TEXT_JSON, "r", encoding="utf-8") as f:
            cached = json.load(f)
        documents = [
            Document(
                page_content=item["content"],
                metadata={"source": item["source"], "title": item["title"], "type": "pdf"},
            )
            for item in cached
        ]
        print(f"Loaded {len(documents)} cached PDF documents")
        return documents

    return load_pdfs()


def load_all_documents(refresh_pdfs: bool = False) -> list[Document]:
    """
    Combine scraped web pages and parsed PDFs into one document set.

    Set refresh_pdfs=True to force re-parsing PDFs from data/pdfs/ even
    if a cached data/raw/pdf_documents.json already exists.
    """
    web_docs = load_scraped_pages()

    if refresh_pdfs and os.path.exists(PDF_TEXT_JSON):
        os.remove(PDF_TEXT_JSON)

    pdf_docs = load_pdf_documents()

    all_docs = web_docs + pdf_docs
    print(f"\nTotal documents loaded: {len(all_docs)} ({len(web_docs)} web + {len(pdf_docs)} pdf)")

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    serializable = [{"content": d.page_content, "metadata": d.metadata} for d in all_docs]
    with open(ALL_DOCS_JSON, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"Saved combined document set: {ALL_DOCS_JSON}")

    return all_docs


if __name__ == "__main__":
    load_all_documents()
