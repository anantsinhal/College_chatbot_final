"""
Retriever for SMIT RAG chatbot.

Design:
  1. Over-fetch candidates from webpages (primary) and PDFs (secondary)
     using separate, calibrated distance thresholds per source type.
  2. Apply a source-diversity cap (max N chunks per URL) to prevent
     one noisy page from dominating the context window.
  3. Deduplicate near-identical chunks (high word overlap) that arise
     from the chunk-overlap setting in ingestion.
  4. Cross-encoder rerank the surviving candidates and keep the top-k.
  5. Return a confidence score alongside documents so the chain can
     decide whether the context is strong enough to answer.

Fix (vs previous version):
  BaseRetriever is a Pydantic model. Storing a Chroma or CrossEncoder
  object as a Pydantic field (even typed as Any) causes AttributeError
  in Pydantic v2 because the model validator wraps the object and
  method lookups break. Solution: store non-serialisable objects as
  plain Python instance attributes via object.__setattr__, keeping them
  completely outside Pydantic's field system.
"""

from __future__ import annotations

import logging
from typing import List, Tuple

from langchain_chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import model_validator
from sentence_transformers import CrossEncoder

from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    CONFIDENCE_THRESHOLD,
    EMBEDDING_MODEL,
    MAX_CHUNKS_PER_SOURCE,
    PDF_DISTANCE_THRESHOLD,
    RERANKER_MODEL,
    RETRIEVER_FETCH_MULTIPLIER,
    RETRIEVER_K,
    WEBPAGE_DISTANCE_THRESHOLD,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Module-level singletons — loaded once per process, never re-created
# ---------------------------------------------------------------------------

_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=_embeddings,
    collection_name=COLLECTION_NAME,
)

_reranker = CrossEncoder(RERANKER_MODEL)


# ---------------------------------------------------------------------------
# Pure helper functions (no class state needed)
# ---------------------------------------------------------------------------

def _expand_short_query(query: str) -> str:
    """
    Single-word chip queries ("Hostel", "Fees") embed poorly against
    paragraph-length chunks. Prefixing gives the bi-encoder more signal.
    """
    if len(query.split()) <= 3:
        return f"SMIT information about: {query}"
    return query


def _deduplicate(docs: List[Document], overlap_threshold: float = 0.60) -> List[Document]:
    """
    Drop chunks whose word overlap with any already-selected chunk exceeds
    overlap_threshold. Fast set-intersection — no ML needed.
    """
    selected: List[Document] = []
    selected_word_sets: List[set] = []

    for doc in docs:
        words = set(doc.page_content.lower().split())
        is_duplicate = False
        for existing in selected_word_sets:
            if not words or not existing:
                continue
            overlap = len(words & existing) / min(len(words), len(existing))
            if overlap >= overlap_threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            selected.append(doc)
            selected_word_sets.append(words)

    return selected


def _apply_source_cap(
    hits: List[Tuple[Document, float]],
    max_per_source: int,
) -> List[Document]:
    """
    Keep at most max_per_source chunks from any single source URL.
    Preserves the original distance ordering.
    """
    source_counts: dict[str, int] = {}
    result: List[Document] = []
    for doc, _ in hits:
        src = doc.metadata.get("source", "")
        count = source_counts.get(src, 0)
        if count < max_per_source:
            result.append(doc)
            source_counts[src] = count + 1
    return result


def _rerank(
    query: str,
    docs: List[Document],
    top_k: int,
) -> Tuple[List[Document], float]:
    """
    Score each (query, chunk) pair with the cross-encoder.
    Returns (reranked_docs[:top_k], top_score).
    top_score is -999.0 when docs is empty.
    """
    if not docs:
        return [], -999.0

    pairs = [(query, doc.page_content) for doc in docs]
    scores: List[float] = _reranker.predict(pairs).tolist()

    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    top_score = ranked[0][0]

    reranked: List[Document] = []
    for score, doc in ranked[:top_k]:
        doc.metadata["reranker_score"] = round(float(score), 3)
        reranked.append(doc)

    return reranked, top_score


def _fetch_candidates(
    query: str,
    vs: Chroma,
    fetch_k: int,
    webpage_threshold: float,
    pdf_threshold: float,
    max_per_source: int,
) -> List[Document]:
    """
    Fetch and filter candidate documents from the vectorstore.
    Kept as a module-level function so it works regardless of how
    SmitRetriever stores its references.
    """
    # --- Webpage candidates ---
    try:
        webpage_hits = vs.similarity_search_with_score(
            query, k=fetch_k, filter={"type": "webpage"}
        )
    except Exception as exc:
        logger.warning("Webpage retrieval failed: %s", exc)
        webpage_hits = []

    webpage_candidates = [
        (doc, score) for doc, score in webpage_hits if score <= webpage_threshold
    ]

    # --- PDF candidates (fill remaining budget) ---
    pdf_budget = max(0, fetch_k - len(webpage_candidates))
    pdf_candidates: List[Tuple[Document, float]] = []

    if pdf_budget > 0:
        try:
            pdf_hits = vs.similarity_search_with_score(
                query, k=pdf_budget, filter={"type": "pdf"}
            )
            pdf_candidates = [
                (doc, score) for doc, score in pdf_hits if score <= pdf_threshold
            ]
        except Exception as exc:
            logger.warning("PDF retrieval failed: %s", exc)

    all_hits = webpage_candidates + pdf_candidates

    # Diversity cap → deduplication
    capped = _apply_source_cap(all_hits, max_per_source)
    return _deduplicate(capped)


# ---------------------------------------------------------------------------
# Retriever class
# ---------------------------------------------------------------------------

class SmitRetriever(BaseRetriever):
    """
    Two-stage retriever: webpage-first with PDF fallback, then cross-encoder
    reranking with diversity cap and deduplication.

    IMPORTANT: vectorstore and _reranker are NOT Pydantic fields.
    They are stored as plain Python instance attributes via object.__setattr__
    to avoid Pydantic v2 validation wrapping non-serialisable objects, which
    causes AttributeError when methods are called on them.

    All configurable numeric parameters ARE Pydantic fields (int/float) —
    these are safe because Pydantic handles primitives correctly.
    """

    # --- Pydantic fields: primitives only ---
    k:                 int   = RETRIEVER_K
    fetch_multiplier:  int   = RETRIEVER_FETCH_MULTIPLIER
    webpage_threshold: float = WEBPAGE_DISTANCE_THRESHOLD
    pdf_threshold:     float = PDF_DISTANCE_THRESHOLD
    max_per_source:    int   = MAX_CHUNKS_PER_SOURCE

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def _attach_singletons(self) -> "SmitRetriever":
        """
        Attach the module-level singletons as plain Python attributes
        AFTER Pydantic has finished model construction. Using
        object.__setattr__ bypasses Pydantic's __setattr__ so these
        objects are never validated or wrapped.
        """
        object.__setattr__(self, "_vs", vectorstore)
        object.__setattr__(self, "_reranker_ref", _reranker)
        return self

    # --- Internal retrieval ---

    def _get_candidates(self, query: str) -> List[Document]:
        fetch_k = self.k * self.fetch_multiplier
        return _fetch_candidates(
            query=query,
            vs=self._vs,
            fetch_k=fetch_k,
            webpage_threshold=self.webpage_threshold,
            pdf_threshold=self.pdf_threshold,
            max_per_source=self.max_per_source,
        )

    # --- LangChain BaseRetriever interface ---

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Called by .invoke() — returns docs only (no confidence score)."""
        expanded = _expand_short_query(query)
        candidates = self._get_candidates(expanded)
        reranked, _ = _rerank(expanded, candidates, self.k)
        return reranked

    # --- Extended interface used by chain.py ---

    def retrieve_with_confidence(self, query: str) -> Tuple[List[Document], float]:
        """
        Returns (docs, top_reranker_score).
        Used by chain.py for confidence-based fallback logic.
        """
        expanded = _expand_short_query(query)
        candidates = self._get_candidates(expanded)
        reranked, top_score = _rerank(expanded, candidates, self.k)
        logger.debug(
            "query=%r | candidates=%d | returned=%d | top_score=%.3f",
            query, len(candidates), len(reranked), top_score,
        )
        return reranked, top_score


# ---------------------------------------------------------------------------
# Global singleton exported to chain.py
# ---------------------------------------------------------------------------

retriever = SmitRetriever(
    k=RETRIEVER_K,
    fetch_multiplier=RETRIEVER_FETCH_MULTIPLIER,
    webpage_threshold=WEBPAGE_DISTANCE_THRESHOLD,
    pdf_threshold=PDF_DISTANCE_THRESHOLD,
    max_per_source=MAX_CHUNKS_PER_SOURCE,
)