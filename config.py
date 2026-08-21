import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# API keys / LLM provider - Groq
# ---------------------------------------------------------------------------
DEEPSEEK_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1"
)
DEEPSEEK_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

# ---------------------------------------------------------------------------
# Crawl settings
# ---------------------------------------------------------------------------
BASE_URL = "https://www.smu.edu.in/smit"
ALLOWED_DOMAIN = "smu.edu.in"
ALLOWED_PATH_PREFIX = "/smit"

MAX_PAGES = 300
REQUEST_TIMEOUT = 15
CRAWL_DELAY_SECONDS = 0.5

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
MIN_CONTENT_LENGTH = 150
MIN_CHUNK_LENGTH = 60

# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# Retrieval - candidate fetch
# ---------------------------------------------------------------------------
RETRIEVER_K = 6
RETRIEVER_FETCH_MULTIPLIER = 3

WEBPAGE_DISTANCE_THRESHOLD = 0.85
PDF_DISTANCE_THRESHOLD = 1.05

MAX_CHUNKS_PER_SOURCE = 2

# ---------------------------------------------------------------------------
# Reranking
# ---------------------------------------------------------------------------
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

CONFIDENCE_THRESHOLD = -6.0

# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------
LLM_TEMPERATURE = 0.2
LLM_TIMEOUT = 30
LLM_MAX_RETRIES = 2