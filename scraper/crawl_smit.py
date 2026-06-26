"""
Crawls the SMIT section of the SMU website and extracts clean, readable
page content for RAG ingestion.

Key improvements over the original crawler:
  1. URL normalization -> no more duplicate pages from "www" vs non-"www"
     hosts, trailing slashes, or query-string noise.
  2. trafilatura-based main-content extraction -> nav bars, footers,
     announcement tickers and menu links are reliably stripped, even when
     the site doesn't use semantic <nav>/<header> tags.
  3. A BeautifulSoup fallback (with explicit junk-block removal) for the
     rare page where trafilatura returns too little text.
  4. Real link discovery restricted to the SMIT path, so we don't wander
     into unrelated parts of the university site.
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

# Blocks of text that show up on nearly every page (nav labels, generic
# CTAs, ticker text) and add noise instead of signal. Matched as
# substrings after whitespace-normalization, so keep them lowercase here
# is not required -- comparison is done case-sensitively against the
# cleaned text, matching the site's own casing.
BOILERPLATE_SNIPPETS = [
    "Apply now × Search Now × Search Now Search Previous Next Previous Next",
]


def normalize_url(url: str) -> str:
    """
    Collapse URL variants that point to the same page:
      - strip the "www." prefix
      - drop fragments (#...)
      - drop a trailing slash (except for the bare domain root)
      - lowercase the scheme/host (path case is left alone since some
        servers are case-sensitive)
    """
    parsed = urlparse(url)

    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    path = parsed.path
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]

    # Drop fragment entirely; keep query string since some pages (e.g.
    # event-details.php?url=1063) are genuinely distinct content.
    cleaned = urlunparse((parsed.scheme.lower(), netloc, path, "", parsed.query, ""))
    return cleaned


def is_crawlable(url: str) -> bool:
    if not url:
        return False
    if url.startswith(("mailto:", "javascript:", "tel:", "#")):
        return False

    parsed = urlparse(url)
    host = parsed.netloc.lower().lstrip("www.")

    if ALLOWED_DOMAIN not in host:
        return False
    if ALLOWED_PATH_PREFIX not in parsed.path:
        return False

    return True


def clean_text(text: str) -> str:
    text = " ".join(text.split())
    for snippet in BOILERPLATE_SNIPPETS:
        text = text.replace(snippet, " ")
    return " ".join(text.split())


def extract_with_bs4_fallback(html: str) -> str:
    """Used only when trafilatura comes back empty/too short."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove obvious non-content elements, including common class/id
    # patterns this site (and most CMS-driven sites) use for menus and
    # tickers even when they aren't wrapped in semantic tags.
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

    if extracted and len(extracted) >= MIN_CONTENT_LENGTH:
        return clean_text(extracted)

    # Fallback for pages trafilatura can't parse well (rare, but
    # heavily-scripted or unusually-structured pages happen).
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
    start_url = normalize_url(start_url)

    visited = set()
    queue = [start_url]

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
