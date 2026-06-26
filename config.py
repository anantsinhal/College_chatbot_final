import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# API keys
# ---------------------------------------------------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------------------------------------------------------------------
# Crawl settings
# ---------------------------------------------------------------------------
# Always crawl with the canonical (www) host so we never store the same
# page twice under "www.smu.edu.in" and "smu.edu.in".
BASE_URL = "https://www.smu.edu.in/smit"
ALLOWED_DOMAIN = "smu.edu.in"  # used after stripping "www."
ALLOWED_PATH_PREFIX = "/smit"  # only crawl pages under the SMIT section

MAX_PAGES = 300
REQUEST_TIMEOUT = 15
CRAWL_DELAY_SECONDS = 0.5  # be polite to the server

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = "data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

PAGES_JSON = os.path.join(RAW_DIR, "smit_pages.json")
PDF_LINKS_JSON = os.path.join(RAW_DIR, "pdf_links.json")
PDF_TEXT_JSON = os.path.join(RAW_DIR, "pdf_documents.json")
ALL_DOCS_JSON = os.path.join(PROCESSED_DIR, "all_documents.json")

CHROMA_PATH = "./vectorstore/chroma_db"
COLLECTION_NAME = "smit_knowledge_base"

# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
MIN_CONTENT_LENGTH = 150  # discard pages/pdf pages with less real text than this

# ---------------------------------------------------------------------------
# Embeddings / retrieval
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RETRIEVER_K = 5
RETRIEVER_FETCH_K = 20

# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.2
