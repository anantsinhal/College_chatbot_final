"""
Downloads every PDF link discovered by the crawler so they can be parsed
into readable text by `ingestion/pdf_loader.py`.
"""

import json
import os
import re

import requests

from config import PDF_DIR, PDF_LINKS_JSON, REQUEST_TIMEOUT

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}


def safe_filename(url: str) -> str:
    name = url.split("/")[-1].split("?")[0]
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return name


def download_pdfs():
    os.makedirs(PDF_DIR, exist_ok=True)

    with open(PDF_LINKS_JSON, "r", encoding="utf-8") as f:
        pdf_links = json.load(f)

    print(f"Found {len(pdf_links)} PDFs")

    downloaded, skipped, failed = 0, 0, 0

    for idx, url in enumerate(pdf_links):
        filename = safe_filename(url)
        filepath = os.path.join(PDF_DIR, filename)

        if os.path.exists(filepath):
            skipped += 1
            continue

        try:
            print(f"[{idx + 1}/{len(pdf_links)}] Downloading {filename}")
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT * 2)

            if response.status_code == 200 and response.content[:4] == b"%PDF":
                with open(filepath, "wb") as f:
                    f.write(response.content)
                downloaded += 1
            else:
                print(f"    -> not a valid PDF response (status {response.status_code})")
                failed += 1

        except requests.RequestException as e:
            print(f"Failed: {url}\n{e}")
            failed += 1

    print(f"\nDone. Downloaded: {downloaded}, Skipped (already had): {skipped}, Failed: {failed}")


if __name__ == "__main__":
    download_pdfs()
