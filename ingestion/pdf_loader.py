"""
Extracts readable text from every PDF in data/pdfs/ and turns each one
into a LangChain Document.

This step was missing from the original pipeline: PDFs were downloaded
but never parsed, and a different script (save_pdf.py) was incorrectly
being used as if it were a PDF *reader* when it actually only *writes*
new PDFs from already-scraped HTML text. That script is no longer part
of the ingestion pipeline -- see ingestion/export_debug_pdf.py if you
still want a human-readable export of the scraped pages for spot-checking.
"""

import json
import os

from langchain_core.documents import Document
from pypdf import PdfReader

from config import MIN_CONTENT_LENGTH, PDF_DIR, PDF_TEXT_JSON, RAW_DIR

# OCR is optional. Several SMIT documents (mandatory disclosures, old
# circulars) are scanned images with no embedded text layer, so pypdf
# alone returns nothing for them. If pytesseract + pdf2image + the
# tesseract binary are available, we fall back to OCR for any PDF that
# came back empty/too-short from normal extraction. If they aren't
# installed, we just skip those PDFs instead of crashing the pipeline.
try:
    import pytesseract
    from pdf2image import convert_from_path

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def clean_text(text: str) -> str:
    return " ".join(text.split())


def extract_pdf_text(filepath: str) -> str:
    try:
        reader = PdfReader(filepath)
    except Exception as e:
        print(f"    -> could not open {filepath}: {e}")
        return ""

    pages_text = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            pages_text.append(text)

    extracted = clean_text("\n".join(pages_text))

    if len(extracted) >= MIN_CONTENT_LENGTH or not OCR_AVAILABLE:
        return extracted

    # Likely a scanned/image-only PDF -- try OCR before giving up.
    print("    -> little/no embedded text found, attempting OCR...")
    try:
        images = convert_from_path(filepath, dpi=200)
        ocr_pages = [pytesseract.image_to_string(img) for img in images]
        ocr_text = clean_text("\n".join(ocr_pages))
        return ocr_text if len(ocr_text) > len(extracted) else extracted
    except Exception as e:
        print(f"    -> OCR failed: {e}")
        return extracted


def load_pdfs() -> list[Document]:
    documents = []

    if not os.path.isdir(PDF_DIR):
        print(f"No PDF directory found at {PDF_DIR}, skipping.")
        return documents

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} downloaded PDFs to parse")

    for idx, filename in enumerate(pdf_files):
        filepath = os.path.join(PDF_DIR, filename)
        print(f"[{idx + 1}/{len(pdf_files)}] Extracting text from {filename}")

        text = extract_pdf_text(filepath)

        if len(text) < MIN_CONTENT_LENGTH:
            print(f"    -> skipped (only {len(text)} chars extracted, likely scanned/image-based)")
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": filepath,
                    "title": filename.replace(".pdf", "").replace("_", " "),
                    "type": "pdf",
                },
            )
        )

    print(f"\nSuccessfully extracted readable text from {len(documents)}/{len(pdf_files)} PDFs")

    os.makedirs(RAW_DIR, exist_ok=True)
    serializable = [
        {"title": d.metadata["title"], "source": d.metadata["source"], "content": d.page_content}
        for d in documents
    ]
    with open(PDF_TEXT_JSON, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"Saved: {PDF_TEXT_JSON}")

    return documents


if __name__ == "__main__":
    load_pdfs()
