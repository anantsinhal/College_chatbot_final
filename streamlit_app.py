"""
SMIT AI Assistant — main entry point.
Layout:
    [sidebar]  |  [left: header + chips + chat]  |  [right: stats + tips]

Backend (qa_chain, session state, ask()) is untouched.
"""

import streamlit as st
import traceback

from rag.chain import qa_chain

from ui.styles import apply_styles
from ui.session import init_session
from ui.sidebar import render_sidebar
from ui.header import render_header
from ui.chips import render_chips
from ui.chat import render_chat
from ui.right_panel import render_right_panel
from ui.constants import MAX_HISTORY


def _exception_text(exc: Exception) -> str:
    parts = [f"{type(exc).__name__}: {exc}"]
    cause = exc.__cause__
    while cause is not None:
        parts.append(f"caused by {type(cause).__name__}: {cause}")
        cause = cause.__cause__
    return " | ".join(parts)


def _is_quota_error(exc: Exception) -> bool:
    text = _exception_text(exc).lower()
    return "resource_exhausted" in text or "quota exceeded" in text or "429" in text


def _fallback_answer(exc: Exception) -> str:
    if _is_quota_error(exc):
        return (
            "The Gemini API quota for this project has been exceeded. "
            "Please try again later or switch to a paid/API-enabled model."
        )
    return "I'm temporarily unable to reach the knowledge base."

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="SMIT AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ─────────────────────────────────────────────────────────────
apply_styles()

# ── Session state ─────────────────────────────────────────────────────────────
init_session()


# ── Backend: ask() — DO NOT MODIFY ───────────────────────────────────────────
def ask(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})

    try:
        st.session_state.last_error = None
        result = qa_chain.invoke(
            {
                "question": question,
                "chat_history": st.session_state.chat_history,
            }
        )

        answer = result["answer"]
        intent = result.get("intent", "smit_query")
        sources = sorted(
            {
                doc.metadata.get("source", "")
                for doc in result.get("source_documents", [])
            }
        )

    except Exception as exc:
        st.session_state.last_error = _exception_text(exc)
        traceback.print_exc()
        answer = _fallback_answer(exc)
        sources = []
        intent = "error"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "intent": intent,
        }
    )

    if intent == "smit_query":
        st.session_state.chat_history.append((question, answer))
        st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY:]


# ── Sidebar (left nav) ────────────────────────────────────────────────────────
render_sidebar()

# ── Main layout: chat area (left) + quick-info panel (right) ─────────────────
main_col, right_col = st.columns([3.5, 1.2], gap="large")

with main_col:
    # 1. Logo + greeting + subtitle
    render_header()

    # 2. Topic chips
    render_chips()

    # 3. Chat messages + input (st.chat_input auto-sticks to bottom)
    render_chat(st.session_state.messages, ask)

with right_col:
    # Quick Stats + Tips panel
    render_right_panel()