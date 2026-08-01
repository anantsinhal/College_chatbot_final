from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable

from langchain_openai import ChatOpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, LLM_TEMPERATURE
from rag.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from rag.retriever import retriever

if not DEEPSEEK_API_KEY:
    raise ValueError(
        "DEEPSEEK_API_KEY is not set. Add it to a .env file in the project root."
    )

llm = ChatOpenAI(
    model=DEEPSEEK_MODEL,
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=LLM_TEMPERATURE,
)

# ---------------------------------------------------------------------------
# Intent classification
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


def _is_greeting(text: str) -> bool:
    return text.lower().strip().rstrip("!?. ") in GREETING_PATTERNS


def _is_off_topic(text: str) -> bool:
    if SMIT_KEYWORDS.search(text):
        return False
    return bool(OFF_TOPIC_PATTERNS.match(text.strip()))


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


def _format_documents(documents) -> str:
    chunks = []
    for document in documents:
        source = document.metadata.get("source", "unknown")
        page = document.metadata.get("page")
        prefix = f"Source: {source}"
        if page is not None:
            prefix += f" | Page: {page}"
        chunks.append(f"{prefix}\n{document.page_content}")
    return "\n\n".join(chunks)


# ---------------------------------------------------------------------------
# Chain
# ---------------------------------------------------------------------------

@dataclass
class SimpleConversationalRetrievalChain:
    llm: ChatOpenAI
    retriever: Any

    def _rewrite_question(self, question: str, chat_history) -> str:
        if not chat_history:
            return question
        prompt = CONDENSE_QUESTION_PROMPT.format(
            chat_history=_format_chat_history(chat_history),
            question=question,
        )
        try:
            rewritten = _message_text(self.llm.invoke(prompt)).strip()
        except Exception as exc:
            raise RuntimeError("question rewrite failed") from exc
        return rewritten or question

    def invoke(self, inputs: dict[str, Any]) -> dict[str, Any]:
        question = inputs.get("question", "").strip()
        chat_history = inputs.get("chat_history", [])

        # --- Intent check ---
        if _is_greeting(question):
            return {
                "answer": GREETING_RESPONSE,
                "source_documents": [],
                "question": question,
                "intent": "greeting",
            }

        if _is_off_topic(question):
            return {
                "answer": OFF_TOPIC_RESPONSE,
                "source_documents": [],
                "question": question,
                "intent": "off_topic",
            }

        # --- Full RAG pipeline ---
        standalone_question = self._rewrite_question(question, chat_history)

        try:
            source_documents = list(self.retriever.invoke(standalone_question))
        except Exception as exc:
            raise RuntimeError("retrieval failed") from exc

        context = _format_documents(source_documents)

        answer_prompt = QA_PROMPT.format(
            context=context,
            question=standalone_question,
        )
        try:
            answer = _message_text(self.llm.invoke(answer_prompt)).strip()
        except Exception as exc:
            raise RuntimeError("answer generation failed") from exc

        return {
            "answer": answer,
            "source_documents": source_documents,
            "question": standalone_question,
            "intent": "smit_query",
        }


qa_chain = SimpleConversationalRetrievalChain(llm=llm, retriever=retriever)