"""
Two-stage retriever: webpages first, PDFs as fallback/supplement.

Optimized for speed over large (12k+) chunk databases.
"""

from typing import List

from langchain_chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL, RETRIEVER_FETCH_K, RETRIEVER_K

# Distance threshold (adjust based on embedding model metric, e.g., cosine vs L2)
MAX_TRUSTED_DISTANCE = 1.0 


class WebFirstPDFFallbackRetriever(BaseRetriever):
    """Retrieves webpage chunks first; fills remaining slots with PDF
    chunks only if webpage hits fall short of 'k'."""

    vectorstore: Chroma
    k: int = RETRIEVER_K
    fetch_k: int = RETRIEVER_FETCH_K

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # 1. Search Webpages first
        webpage_hits = self.vectorstore.similarity_search_with_score(
            query,
            k=self.k,
            filter={"type": "webpage"},
        )
        
        # Keep strong webpage matches
        webpage_docs = [doc for doc, score in webpage_hits if score <= MAX_TRUSTED_DISTANCE]

        # Calculate if we actually need PDF chunks to reach total k
        remaining = self.k - len(webpage_docs)

        # If webpage matches satisfied 'k', return immediately (Saves 50%+ execution time!)
        if remaining <= 0:
            return webpage_docs

        # 2. Search PDFs only if we need filler context
        try:
            # Use a capped fetch_k (max 15) so CPU matrix operations remain fast
            fast_fetch_k = min(self.fetch_k, 15)
            pdf_docs = self.vectorstore.max_marginal_relevance_search(
                query,
                k=remaining,
                fetch_k=fast_fetch_k,
                filter={"type": "pdf"},
            )
        except Exception:
            # Fallback to standard similarity search if MMR fails
            pdf_docs = self.vectorstore.similarity_search(
                query,
                k=remaining,
                filter={"type": "pdf"},
            )

        # 3. Combine and return
        return webpage_docs + pdf_docs


# Global Vectorstore & Retriever Setup
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
)

retriever = WebFirstPDFFallbackRetriever(
    vectorstore=vectorstore,
    k=RETRIEVER_K,
    fetch_k=RETRIEVER_FETCH_K,
)