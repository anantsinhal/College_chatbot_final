import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# API keys / LLM provider
# ---------------------------------------------------------------------------
DEEPSEEK_API_KEY  = os.getenv("GROQ_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
DEEPSEEK_MODEL    = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ---------------------------------------------------------------------------
# Crawl settings
# ---------------------------------------------------------------------------
BASE_URL            = "https://www.smu.edu.in/smit"
ALLOWED_DOMAIN      = "smu.edu.in"
ALLOWED_PATH_PREFIX = "/smit"

MAX_PAGES            = 300
REQUEST_TIMEOUT      = 15
CRAWL_DELAY_SECONDS  = 0.5

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR      = "data"
RAW_DIR       = os.path.join(DATA_DIR, "raw")
PDF_DIR       = os.path.join(DATA_DIR, "pdfs")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

PAGES_JSON    = os.path.join(RAW_DIR, "smit_pages.json")
PDF_LINKS_JSON = os.path.join(RAW_DIR, "pdf_links.json")
PDF_TEXT_JSON = os.path.join(RAW_DIR, "pdf_documents.json")
ALL_DOCS_JSON = os.path.join(PROCESSED_DIR, "all_documents.json")

CHROMA_PATH     = "./vectorstore/chroma_db"
COLLECTION_NAME = "smit_knowledge_base"

# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
CHUNK_SIZE         = 800
CHUNK_OVERLAP      = 120
MIN_CONTENT_LENGTH = 150   # discard pages shorter than this
MIN_CHUNK_LENGTH   = 60    # discard individual chunks shorter than this

# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# Retrieval — candidate fetch
# ---------------------------------------------------------------------------
# How many results to pull per source type before filtering + reranking.
# We over-fetch by a multiplier so reranking has a real candidate pool.
RETRIEVER_K              = 6    # final number of chunks sent to LLM
RETRIEVER_FETCH_MULTIPLIER = 3  # fetch K * multiplier candidates before reranking

# Chroma L2 distance thresholds per source type.
# all-MiniLM-L6-v2 L2 distances: ~0.3-0.6 = very close, ~0.8-1.1 = related,
# >1.3 = probably irrelevant.  Webpages are structured so a tighter gate is
# appropriate; PDFs use formal language so they embed slightly further.
WEBPAGE_DISTANCE_THRESHOLD = 0.85
PDF_DISTANCE_THRESHOLD     = 1.05

# Maximum chunks allowed from a single source URL (diversity cap).
MAX_CHUNKS_PER_SOURCE = 2

# ---------------------------------------------------------------------------
# Reranking
# ---------------------------------------------------------------------------
# Cross-encoder used to score (query, chunk) relevance after initial retrieval.
# ms-marco-MiniLM-L-6-v2 is 22 MB, CPU-fast, proven on passage ranking.
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# If the top reranked chunk scores below this, the retrieved context is too weak
# to answer reliably.  The chain will return a graceful fallback rather than
# hallucinating.  Cross-encoder raw scores are log-odds; ~-3 = weak match,
# ~0 = okay, ~3+ = strong.  Set conservatively so genuine edge-case questions
# still get attempted.
CONFIDENCE_THRESHOLD = -6.0

# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------
LLM_TEMPERATURE = 0.2
LLM_TIMEOUT     = 30    # seconds before giving up on an API call
LLM_MAX_RETRIES = 2     # automatic retry with backoff on transient errors
