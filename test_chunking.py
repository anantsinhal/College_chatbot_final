

from config import BASE_URL
from ingestion.chunk_documents import chunk_documents
from scraper.crawl_smit import crawl

print("Crawling a small sample of pages for testing...")
docs, pdf_links = crawl(BASE_URL, max_pages=5)

print(f"\nDocuments loaded: {len(docs)}")
print(f"PDF links discovered (not downloaded in this test): {len(pdf_links)}")

chunks = chunk_documents(docs)
print(f"Total chunks created: {len(chunks)}")

print("\n" + "=" * 60)
print("FIRST CHUNK")
print("=" * 60)
print(chunks[0].page_content)

print("\n" + "=" * 60)
print("FIRST CHUNK METADATA")
print("=" * 60)
print(chunks[0].metadata)

print("\n" + "=" * 60)
print("CHUNK LENGTH STATS")
print("=" * 60)
lengths = [len(c.page_content) for c in chunks]
print(f"min={min(lengths)} max={max(lengths)} avg={sum(lengths) / len(lengths):.0f}")
