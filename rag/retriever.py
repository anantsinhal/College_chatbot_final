"""
Two-stage retriever: webpages first, PDFs as fallback/supplement.

Why this exists: testing showed that for a query like "What B.Tech
programs does SMIT offer?", raw vector similarity returned 8 of the top
10 chunks from data/pdfs/Prospectus.pdf -- generic marketing language
("industry-driven curriculum", "hands-on learning") that's semantically
similar to almost any program-related question. Meanwhile the actual
best answer, btech-in-computer-science.php (which names the specific
degree programs), barely made the top 10 and lost out.

The PDF isn't useless -- it likely has unique info (fee tables, semester
structure, hostel costs) the website doesn't. So instead of excluding it,
this retriever treats webpages as the primary source and only pulls in
PDF chunks to fill remaining slots, ensuring webpages can never be
crowded out by sheer PDF chunk volume.
"""

from typing import List

from langchain_chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL, RETRIEVER_FETCH_K, RETRIEVER_K

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
)

WEBPAGE_RESERVED_SLOTS = RETRIEVER_K
MAX_TRUSTED_DISTANCE = 1.2


class WebFirstPDFFallbackRetriever(BaseRetriever):
    """Retrieves webpage chunks first; fills remaining slots with PDF
    chunks only if webpages don't fully cover the requested k."""

    vectorstore: Chroma
    k: int = RETRIEVER_K
    fetch_k: int = RETRIEVER_FETCH_K

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        webpage_hits = self.vectorstore.similarity_search_with_score(
            query,
            k=self.k,
            filter={"type": "webpage"},
        )
        webpage_docs = [doc for doc, score in webpage_hits if score <= MAX_TRUSTED_DISTANCE]

        remaining = self.k - len(webpage_docs)
        if remaining <= 0:
            return webpage_docs[: self.k]

        pdf_hits = self.vectorstore.similarity_search_with_score(
            query,
            k=remaining,
            filter={"type": "pdf"},
        )
        pdf_docs = [doc for doc, score in pdf_hits]

        return webpage_docs + pdf_docs


retriever = WebFirstPDFFallbackRetriever(
    vectorstore=vectorstore,
    k=RETRIEVER_K,
    fetch_k=RETRIEVER_FETCH_K,
)