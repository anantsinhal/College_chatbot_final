# SMIT College RAG Chatbot

A conversational, RAG-based chatbot for Sikkim Manipal Institute of
Technology (SMIT), built with LangChain, Chroma, HuggingFace
sentence-transformers, and Gemini 2.5 Flash. Streamlit frontend to be
added separately.

## What changed from the original version

| Problem | Fix |
|---|---|
| Same pages crawled twice (`www.smu.edu.in` vs `smu.edu.in`) | `normalize_url()` in `scraper/crawl_smit.py` collapses both to one canonical form |
| Every chunk polluted with nav/menu/ticker text (site doesn't use `<nav>`/`<header>` tags) | Switched extraction to `trafilatura`, which identifies main content vs. boilerplate regardless of HTML tag structure, with a BeautifulSoup fallback |
| Chunks split mid-sentence with no page context | `RecursiveCharacterTextSplitter` now prefers paragraph/sentence boundaries, and each chunk is prefixed with its source page's title |
| PDFs downloaded but never parsed into text | New `ingestion/pdf_loader.py` extracts real text via `pypdf`, with optional OCR fallback (`pytesseract`/`pdf2image`) for scanned documents |
| `save_pdf.py` misused as a "reader" (it only writes PDFs, and crashed on `&`/`<`/`>` in scraped text) | Replaced with `ingestion/export_debug_pdf.py` — a debug-only tool with proper XML escaping, no longer part of the ingestion path |
| `load_documents.py` was empty | Implemented `load_all_documents()` to merge web + PDF documents with dedup and min-length filtering |
| Broken imports (`scraper.*`, `ingestion.*`, `rag.*` packages didn't exist) | Added `__init__.py` files, consistent package structure, fixed all imports |
| Re-running ingestion appended duplicate vectors | `build_vectorstore.py` now wipes the old Chroma store before rebuilding |
| Retriever/vectorstore could silently point at different collections | Both now read `COLLECTION_NAME` from `config.py` |
| No conversation-aware prompt structure | Added `CONDENSE_QUESTION_PROMPT` + `QA_PROMPT` in `rag/prompts.py`, wired into `ConversationalRetrievalChain` |

## Project structure

```
smit_chatbot/
├── config.py                     # all settings in one place
├── ingest.py                     # run this to (re)build the knowledge base
├── app.py                        # CLI chat loop (temporary, pre-Streamlit)
├── test_chunking.py              # quick sanity check on a 5-page crawl
├── requirements.txt
├── .env.example                  # copy to .env and add GOOGLE_API_KEY
│
├── scraper/
│   ├── crawl_smit.py              # crawls site, trafilatura extraction, URL normalization
│   └── download_pdf.py            # downloads PDFs linked from crawled pages
│
├── ingestion/
│   ├── pdf_loader.py              # pypdf text extraction + optional OCR fallback
│   ├── load_documents.py          # merges web pages + PDFs into Documents
│   ├── chunk_documents.py         # structure-aware chunking
│   ├── build_vectorstore.py       # embeds + persists to Chroma
│   └── export_debug_pdf.py        # optional: dump documents to a readable PDF for spot-checks
│
├── rag/
│   ├── retriever.py                # Chroma MMR retriever
│   ├── prompts.py                  # condense-question + QA prompt templates
│   └── chain.py                    # ConversationalRetrievalChain wiring
│
└── data/
    ├── raw/                        # smit_pages.json, pdf_links.json, pdf_documents.json
    ├── pdfs/                       # downloaded PDF files
    └── processed/                  # all_documents.json (final merged set before chunking)
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your GOOGLE_API_KEY
```

OCR is optional. If you want scanned PDFs (e.g. mandatory disclosure
forms) to be readable too, also install the system Tesseract binary:

```bash
# Debian/Ubuntu
sudo apt install tesseract-ocr
# macOS
brew install tesseract
```

If you skip this, `pdf_loader.py` just skips scanned PDFs instead of
crashing.

## Running the pipeline

Full run (crawl + download PDFs + parse + chunk + embed):

```bash
python ingest.py
```

Useful flags while iterating:

```bash
# Already crawled? Re-chunk/re-embed without re-crawling:
python ingest.py --skip-crawl --skip-pdf-download

# Crawl a smaller sample first to sanity-check extraction quality:
python ingest.py --max-pages 20
```

Quick sanity check on extraction + chunking only (no embedding, no LLM
calls needed):

```bash
python test_chunking.py
```

## Talking to the bot (CLI, pre-Streamlit)

```bash
python app.py
```

## Notes on the crawl target

`config.py` sets `BASE_URL = "https://www.smu.edu.in/smit"` and restricts
crawling to URLs containing `/smit` on the `smu.edu.in` domain, so it
won't wander into unrelated parts of the wider Manipal university site.
Adjust `ALLOWED_PATH_PREFIX` if SMIT's section of the site is restructured.

## When you build the Streamlit frontend

Import `qa_chain` from `rag.chain` and call:

```python
result = qa_chain.invoke({"question": query, "chat_history": chat_history})
result["answer"]              # the response text
result["source_documents"]    # list of Documents used, each with .metadata["source"]
```

Keep `chat_history` as a list of `(question, answer)` tuples across the
Streamlit session (e.g. in `st.session_state`).
