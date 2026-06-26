"""
End-to-end ingestion pipeline:

  1. Crawl the SMIT website (clean content, deduplicated URLs)
  2. Download any PDFs linked from those pages
  3. Extract readable text from those PDFs (with OCR fallback if scanned)
  4. Merge web + PDF documents
  5. Chunk them with structure-aware splitting
  6. Embed + persist into Chroma

Run stages individually if you're iterating (e.g. you already have
data/raw/smit_pages.json and just want to re-chunk/re-embed):

    python ingest.py --skip-crawl --skip-pdf-download
"""

import argparse
import json
import os

from config import BASE_URL, MAX_PAGES, PAGES_JSON, PDF_LINKS_JSON
from ingestion.build_vectorstore import create_vectorstore
from ingestion.chunk_documents import chunk_documents
from ingestion.load_documents import load_all_documents
from scraper.crawl_smit import crawl, save_data
from scraper.download_pdf import download_pdfs


def run(skip_crawl: bool, skip_pdf_download: bool, skip_pdf_parse: bool, max_pages: int):
    print("=" * 60)
    print("SMIT KNOWLEDGE BASE INGESTION")
    print("=" * 60)

    if not skip_crawl:
        print("\nStep 1: Crawling website...")
        docs, pdf_links = crawl(BASE_URL, max_pages=max_pages)
        save_data(docs, pdf_links)
        print(f"Documents collected: {len(docs)} | PDF links found: {len(pdf_links)}")
    else:
        print("\nStep 1: Skipped (using existing data/raw/smit_pages.json)")
        if not os.path.exists(PAGES_JSON):
            raise FileNotFoundError(
                f"{PAGES_JSON} not found. Run without --skip-crawl at least once."
            )

    if not skip_pdf_download:
        print("\nStep 2: Downloading PDFs...")
        if os.path.exists(PDF_LINKS_JSON):
            download_pdfs()
        else:
            print(f"No {PDF_LINKS_JSON} found, skipping PDF download.")
    else:
        print("\nStep 2: Skipped (using already-downloaded PDFs, if any)")

    print("\nStep 3: Loading + merging documents (web pages + parsed PDFs)...")
    all_docs = load_all_documents(refresh_pdfs=not skip_pdf_parse)

    print("\nStep 4: Chunking documents...")
    chunks = chunk_documents(all_docs)

    print("\nStep 5: Building Chroma vector store...")
    create_vectorstore(chunks)

    print("\nKnowledge base created successfully!")
    print(f"Total documents: {len(all_docs)} | Total chunks: {len(chunks)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the SMIT chatbot ingestion pipeline.")
    parser.add_argument("--skip-crawl", action="store_true", help="Reuse existing scraped pages JSON")
    parser.add_argument("--skip-pdf-download", action="store_true", help="Don't re-download PDFs")
    parser.add_argument(
        "--skip-pdf-parse",
        action="store_true",
        help="Reuse cached parsed-PDF JSON instead of re-running OCR/text extraction",
    )
    parser.add_argument("--max-pages", type=int, default=MAX_PAGES, help="Max pages to crawl")
    args = parser.parse_args()

    run(
        skip_crawl=args.skip_crawl,
        skip_pdf_download=args.skip_pdf_download,
        skip_pdf_parse=args.skip_pdf_parse,
        max_pages=args.max_pages,
    )
