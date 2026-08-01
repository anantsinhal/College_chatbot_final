"""
Crawls the SMIT section of the SMU website and extracts clean, readable
page content for RAG ingestion.
"""

import json
import os
import time
from urllib.parse import urljoin, urlparse, urlunparse

import requests
import trafilatura
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from config import (
    ALLOWED_DOMAIN,
    ALLOWED_PATH_PREFIX,
    BASE_URL,
    CRAWL_DELAY_SECONDS,
    MAX_PAGES,
    MIN_CONTENT_LENGTH,
    PAGES_JSON,
    PDF_LINKS_JSON,
    RAW_DIR,
    REQUEST_TIMEOUT,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}

BOILERPLATE_SNIPPETS = [
    "Apply now × Search Now × Search Now Search Previous Next Previous Next",
    "Know SMIT History Vision/Mission Administration Mandatory "
    "Disclosures Rankings Achievements Accreditations Affiliations "
    "International Collaboration Cell Institution's Innovation Council "
    "ICC Committees Human Resource Policy Notice NIRF IQAC News Events",
]

# Domains/paths allowed specifically for admissions & application forms
EXTRA_ALLOWED_DOMAINS = ["applysmit.in", "apply.applysmit.in"]
EXTRA_ALLOWED_PATHS = [
    "Eligibility-and-Admission-Process.php",
    "admissions-majitar-campus.php",
    "download-forms.php",
]


def normalize_url(url: str) -> str:
    """
    Collapse URL variants that point to the same page:
      - strip the "www." prefix
      - drop fragments (#...)
      - drop a trailing slash (except for the bare domain root)
      - lowercase the scheme/host (path case is left alone)
    """
    parsed = urlparse(url)

    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    path = parsed.path
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]

    cleaned = urlunparse((parsed.scheme.lower(), netloc, path, "", parsed.query, ""))
    return cleaned


def is_crawlable(url: str) -> bool:
    if not url:
        return False
    if url.startswith(("mailto:", "javascript:", "tel:", "#")):
        return False

    parsed = urlparse(url)
    host = parsed.netloc.lower().lstrip("www.")

    # 1. Allow dedicated application portals
    if any(allowed in host for allowed in EXTRA_ALLOWED_DOMAINS):
        return True

    # 2. Check main domain
    if ALLOWED_DOMAIN not in host:
        return False

    # 3. Allow explicit admission path keywords
    if any(path_kw in parsed.path for path_kw in EXTRA_ALLOWED_PATHS):
        return True

    # 4. Standard path prefix check
    if ALLOWED_PATH_PREFIX not in parsed.path:
        return False

    # Reject nested duplicate relative paths
    if parsed.path.count(ALLOWED_PATH_PREFIX) > 1:
        return False

    return True


def clean_text(text: str) -> str:
    text = " ".join(text.split())
    for snippet in BOILERPLATE_SNIPPETS:
        text = text.replace(snippet, " ")
    return " ".join(text.split())


def extract_with_bs4_fallback(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    junk_selectors = [
        "script", "style", "nav", "footer", "header", "noscript",
        "[class*=menu]", "[class*=nav]", "[class*=footer]",
        "[class*=header]", "[class*=ticker]", "[id*=menu]", "[id*=nav]",
    ]
    for selector in junk_selectors:
        for tag in soup.select(selector):
            tag.decompose()

    main = soup.find("main") or soup.find("article") or soup.find("body")
    if not main:
        return ""

    return clean_text(main.get_text(separator=" ", strip=True))


def extract_content(html: str, url: str) -> str:
    extracted = trafilatura.extract(
        html,
        url=url,
        include_tables=True,
        include_links=False,
        favor_recall=False,
    )

    if extracted:
        cleaned = clean_text(extracted)
        if cleaned:
            return cleaned

    return extract_with_bs4_fallback(html)


def get_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return clean_text(soup.title.string)
    h1 = soup.find("h1")
    if h1:
        return clean_text(h1.get_text())
    return "Untitled Page"


def save_data(documents, pdf_links):
    os.makedirs(RAW_DIR, exist_ok=True)

    pages = [
        {
            "title": doc.metadata.get("title", ""),
            "source": doc.metadata.get("source", ""),
            "content": doc.page_content,
        }
        for doc in documents
    ]

    with open(PAGES_JSON, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

    with open(PDF_LINKS_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted(pdf_links), f, indent=2)

    print("\nData saved successfully!")
    print(f"Saved: {PAGES_JSON}")
    print(f"Saved: {PDF_LINKS_JSON}")


def crawl(start_url: str = BASE_URL, max_pages: int = MAX_PAGES):
    seed_urls = [
        BASE_URL,
        "https://apply.applysmit.in/",
        "https://smu.edu.in/Eligibility-and-Admission-Process.php",
        "https://smu.edu.in/admissions-majitar-campus.php",
    ]

    visited = set()
    queue = [normalize_url(u) for u in seed_urls if u]

    documents = []
    pdf_links = set()

    session = requests.Session()
    session.headers.update(HEADERS)

    while queue and len(visited) < max_pages:
        current_url = queue.pop(0)
        normalized_current = normalize_url(current_url)

        if normalized_current in visited:
            continue

        try:
            print(f"[{len(visited) + 1}/{max_pages}] Crawling: {normalized_current}")

            response = session.get(normalized_current, timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                visited.add(normalized_current)
                continue

            final_url = normalize_url(response.url)
            homepage_url = normalize_url(BASE_URL)
            redirected_to_homepage = (
                response.history
                and final_url == homepage_url
                and normalized_current != homepage_url
            )
            if redirected_to_homepage:
                print("    -> redirected to homepage, skipping")
                visited.add(normalized_current)
                continue

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                visited.add(normalized_current)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            visited.add(normalized_current)

            title = get_title(soup)
            content = extract_content(response.text, normalized_current)

            if len(content) >= MIN_CONTENT_LENGTH:
                documents.append(
                    Document(
                        page_content=content,
                        metadata={"source": normalized_current, "title": title},
                    )
                )
            else:
                print(f"    -> skipped (only {len(content)} chars of real content)")

            for link in soup.find_all("a"):
                href = link.get("href")
                if not href:
                    continue

                absolute_url = urljoin(normalized_current, href)
                absolute_url = absolute_url.split("#")[0]

                if absolute_url.lower().endswith(".pdf"):
                    pdf_links.add(absolute_url)
                    continue

                if is_crawlable(absolute_url):
                    norm = normalize_url(absolute_url)
                    if norm not in visited and norm not in queue:
                        queue.append(norm)

            time.sleep(CRAWL_DELAY_SECONDS)

        except requests.RequestException as e:
            print(f"Error crawling {normalized_current}: {e}")
            visited.add(normalized_current)

    print("\n===== CRAWL COMPLETE =====")
    print(f"Pages Visited: {len(visited)}")
    print(f"Documents Collected: {len(documents)}")
    print(f"PDFs Found: {len(pdf_links)}")

    return documents, list(pdf_links)


if __name__ == "__main__":
    docs, pdfs = crawl(BASE_URL, max_pages=MAX_PAGES)
    save_data(docs, pdfs)
    print(f"\nDocuments: {len(docs)}")
    print(f"PDFs: {len(pdfs)}")