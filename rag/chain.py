from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from rag.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from rag.retriever import retriever

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not set. Add it to a .env file in the project root."
    )

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=LLM_TEMPERATURE,
)


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


@dataclass
class SimpleConversationalRetrievalChain:
    llm: ChatGoogleGenerativeAI
    retriever: Any

    def _rewrite_question(self, question: str, chat_history) -> str:
        if not chat_history:
            return question

        prompt = CONDENSE_QUESTION_PROMPT.format(
            chat_history=_format_chat_history(chat_history),
            question=question,
        )
        rewritten = _message_text(self.llm.invoke(prompt)).strip()
        return rewritten or question

    def invoke(self, inputs: dict[str, Any]) -> dict[str, Any]:
        question = inputs.get("question", "").strip()
        chat_history = inputs.get("chat_history", [])

        standalone_question = self._rewrite_question(question, chat_history)
        source_documents = list(self.retriever.invoke(standalone_question))
        context = _format_documents(source_documents)

        answer_prompt = QA_PROMPT.format(
            context=context,
            question=standalone_question,
        )
        answer = _message_text(self.llm.invoke(answer_prompt)).strip()

        return {
            "answer": answer,
            "source_documents": source_documents,
            "question": standalone_question,
        }


qa_chain = SimpleConversationalRetrievalChain(llm=llm, retriever=retriever)
