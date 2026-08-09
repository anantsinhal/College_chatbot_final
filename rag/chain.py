"""
Conversational RAG chain for the SMIT chatbot.

Key design decisions:
  - Question rewrite only fires when the question contains a real dependency
    signal (pronoun, "what about", etc.).  Self-contained questions skip the
    extra LLM call entirely, halving API usage for the majority of queries.
  - Rewrite failure is non-fatal: falls back to the original question and logs
    a warning instead of aborting the whole request.
  - Uses retrieve_with_confidence() to get a reranker score alongside docs.
    If no chunk scores above CONFIDENCE_THRESHOLD, returns a graceful fallback
    rather than sending weak context to the LLM.
  - Returns a structured `citations` dict so the UI can show exact sources.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from langchain_openai import ChatOpenAI

from config import (
    CONFIDENCE_THRESHOLD,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    LLM_MAX_RETRIES,
    LLM_TEMPERATURE,
    LLM_TIMEOUT,
)
from rag.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from rag.retriever import retriever

logger = logging.getLogger(__name__)

if not DEEPSEEK_API_KEY:
    raise ValueError(
        "DEEPSEEK_API_KEY is not set. Add it to a .env file in the project root."
    )

llm = ChatOpenAI(
    model=DEEPSEEK_MODEL,
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=LLM_TEMPERATURE,
    timeout=LLM_TIMEOUT,
    max_retries=LLM_MAX_RETRIES,
)

# ---------------------------------------------------------------------------
# Intent classification (unchanged from original)
# ---------------------------------------------------------------------------

GREETING_PATTERNS = {
    "hi", "hello", "hey", "hii", "helo", "helloo", "heyy",
    "good morning", "good afternoon", "good evening", "good night",
    "how are you", "how r u", "how are u", "how do you do",
    "what's up", "whats up", "sup", "yo", "namaste", "hola",
    "greetings", "howdy",
}

GREETING_RESPONSE = (
    "Hello! 👋 I'm the SMIT Student Assistant — I can help you with "
    "information about B.Tech programs, fees, admissions, placements, "
    "scholarships, and more at Sikkim Manipal Institute of Technology.\n\n"
    "What would you like to know?"
)

OFF_TOPIC_RESPONSE = (
    "I'm designed specifically to answer questions about SMIT — "
    "programs, fees, admissions, placements, campus life, and official "
    "policies. I can't help with that particular request, but feel free "
    "to ask anything about SMIT!"
)

DIRECTOR_RESPONSE = "Prof. (Dr.) Savitha G.Kini is the director of smit as of now 2026"
HIGHEST_PACKAGE_RESPONSE = "The highest package offered at smit is INR 54 LPA"

SMIT_KEYWORDS = re.compile(
    r"\b(smit|smu|sikkim|manipal|b\.?tech|mtech|mba|mca|bca|bba|"
    r"admission|fee|fees|placement|scholarship|hostel|campus|faculty|"
    r"program|course|syllabus|rank|accreditat|eligib|apply|seat|cutoff|"
    r"department|research|lab|library|iqac|nirf|nba|aicte)\b",
    re.IGNORECASE,
)

OFF_TOPIC_PATTERNS = re.compile(
    r"^(write (a |me )?(poem|story|essay|song|code|email)|"
    r"(what is |what'?s |define )(love|life|[0-9])|"
    r"(who (is |was )(god|allah|jesus|modi|trump|musk|biden))|"
    r"tell me a joke|make me laugh|play (a song|music)|"
    r"(weather|temperature) in|translate (this )?to|"
    r"capital of [a-z]+$)",
    re.IGNORECASE,
)

DIRECTOR_PATTERNS = re.compile(
    r"\bwho\s+(?:is|was)\s+(?:the\s+)?director\s+(?:of|at)\s+"
    r"(?:smit|sikkim manipal institute of technology)\b|"
    r"\bdirector\s+(?:of|at)\s+(?:smit|sikkim manipal institute of technology)\b",
    re.IGNORECASE,
)

HIGHEST_PACKAGE_PATTERNS = re.compile(
    r"\b(what\s+is\s+)?(the\s+)?(highest)\s+package\s+"
    r"(of|at|offered\s+at)\s+(smit|sikkim manipal institute of technology)\b|"
    r"\b(package\s+of\s+smit|smit\s+package\s+highest)\b",
    re.IGNORECASE,
)

# Signals that a question depends on prior context and needs rewriting.
# If none of these appear, the question is already standalone — skip the
# rewrite LLM call entirely.
_DEPENDENCY_SIGNALS = re.compile(
    r"\b(it|its|that|those|these|they|them|their|this|there|"
    r"the same|the above|what about|how about|and what|also|"
    r"more about|tell me more|elaborate|explain further|what else)\b|^\s*(for|about|and|but)\s+\w",
    re.IGNORECASE,
)


def _is_greeting(text: str) -> bool:
    return text.lower().strip().rstrip("!?. ") in GREETING_PATTERNS


def _is_off_topic(text: str) -> bool:
    if SMIT_KEYWORDS.search(text):
        return False
    return bool(OFF_TOPIC_PATTERNS.match(text.strip()))


def _is_director_question(text: str) -> bool:
    return bool(DIRECTOR_PATTERNS.search(text.strip()))


def _is_highest_package_question(text: str) -> bool:
    return bool(HIGHEST_PACKAGE_PATTERNS.search(text.strip()))


def _needs_rewrite(question: str, chat_history: list) -> bool:
    """Return True only when a rewrite LLM call is actually necessary."""
    if not chat_history:
        return False
    return bool(_DEPENDENCY_SIGNALS.search(question))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _message_text(response: Any) -> str:
    content = getattr(response, "content", response)
    if isinstance(content, list):
        return "".join(str(part) for part in content)
    return str(content)


def _format_chat_history(chat_history: Iterable[tuple[str, str]]) -> str:
    turns = []
    for question, answer in chat_history:
        turns.append(f"Human: {question}\nAssistant: {answer}")
    return "\n".join(turns)


def _format_documents(documents: list) -> tuple[str, dict]:
    """
    Build a numbered context string and a parallel citations dict.

    Returns:
        context_str  — what gets injected into the QA prompt.
        citations    — {citation_number: {source, page, type, score}} for the UI.

    Numbering ([1], [2], ...) lets the LLM reference specific sources
    in its answer, and lets the UI link them.
    """
    chunks: list[str] = []
    citations: dict[int, dict] = {}

    for idx, doc in enumerate(documents, start=1):
        meta = doc.metadata
        source = meta.get("source", "unknown")
        page   = meta.get("page")
        dtype  = meta.get("type", "unknown")
        score  = meta.get("reranker_score")

        # Build citation record for the UI
        citation: dict[str, Any] = {"source": source, "type": dtype}
        if page is not None:
            citation["page"] = page
        if score is not None:
            citation["score"] = score
        citations[idx] = citation

        # Build context block shown to the LLM
        header_parts = [f"[{idx}] Source: {source}"]
        if page is not None:
            header_parts.append(f"Page {page}")
        header_parts.append(f"({dtype})")
        header = " | ".join(header_parts)

        chunks.append(f"{header}\n{doc.page_content}")

    return "\n\n---\n\n".join(chunks), citations


# ---------------------------------------------------------------------------
# Chain
# ---------------------------------------------------------------------------

@dataclass
class SimpleConversationalRetrievalChain:
    llm: ChatOpenAI
    retriever: Any

    def _rewrite_question(self, question: str, chat_history: list) -> str:
        """
        Rewrite only when the question contains a real dependency signal.
        If the rewrite LLM call fails, log a warning and return the original
        question — never abort the whole request over a rewrite failure.
        """
        if not _needs_rewrite(question, chat_history):
            return question

        prompt = CONDENSE_QUESTION_PROMPT.format(
            chat_history=_format_chat_history(chat_history),
            question=question,
        )
        try:
            rewritten = _message_text(self.llm.invoke(prompt)).strip()
            logger.debug("Rewrite: %r -> %r", question, rewritten)
            return rewritten or question
        except Exception as exc:
            logger.warning(
                "Question rewrite failed (%s: %s); using original question.",
                type(exc).__name__, exc,
            )
            return question   # non-fatal fallback

    def invoke(self, inputs: dict[str, Any]) -> dict[str, Any]:
        question    = inputs.get("question", "").strip()
        chat_history = inputs.get("chat_history", [])

        # --- Intent shortcuts ---
        if _is_greeting(question):
            return {
                "answer": GREETING_RESPONSE,
                "source_documents": [],
                "citations": {},
                "question": question,
                "intent": "greeting",
                "confidence": 999.0,
            }

        if _is_director_question(question):
            return {
                "answer": DIRECTOR_RESPONSE,
                "source_documents": [],
                "citations": {},
                "question": question,
                "intent": "director_lookup",
                "confidence": 999.0,
            }

        if _is_highest_package_question(question):
            return {
                "answer": HIGHEST_PACKAGE_RESPONSE,
                "source_documents": [],
                "citations": {},
                "question": question,
                "intent": "highest_package_lookup",
                "confidence": 999.0,
            }

        if _is_off_topic(question):
            return {
                "answer": OFF_TOPIC_RESPONSE,
                "source_documents": [],
                "citations": {},
                "question": question,
                "intent": "off_topic",
                "confidence": 999.0,
            }

        # --- Rewrite (only when needed) ---
        standalone_question = self._rewrite_question(question, chat_history)

        # --- Retrieval with confidence score ---
        try:
            source_documents, top_confidence = self.retriever.retrieve_with_confidence(
                standalone_question
            )
        except Exception as exc:
            raise RuntimeError("retrieval failed") from exc

        # --- Weak-context guard ---
        # If no chunk is genuinely relevant, don't send thin context to the LLM.
        if not source_documents or top_confidence < CONFIDENCE_THRESHOLD:
            logger.info(
                "Low confidence (%.3f < %.3f) for query %r; returning fallback.",
                top_confidence, CONFIDENCE_THRESHOLD, standalone_question,
            )
            return {
                "answer": "I couldn't find that information in the SMIT knowledge base.",
                "source_documents": [],
                "citations": {},
                "question": standalone_question,
                "intent": "low_confidence",
                "confidence": top_confidence,
            }

        # --- Build context & prompt ---
        context, citations = _format_documents(source_documents)

        answer_prompt = QA_PROMPT.format(
            context=context,
            question=standalone_question,
        )

        # --- LLM answer generation ---
        try:
            answer = _message_text(self.llm.invoke(answer_prompt)).strip()
        except Exception as exc:
            raise RuntimeError("answer generation failed") from exc

        return {
            "answer": answer,
            "source_documents": source_documents,
            "citations": citations,
            "question": standalone_question,
            "intent": "smit_query",
            "confidence": top_confidence,
        }


qa_chain = SimpleConversationalRetrievalChain(llm=llm, retriever=retriever)
