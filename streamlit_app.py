"""
SMIT AI Assistant — main entry point.
Layout:
    [sidebar]  |  [left: header + chips + chat]  |  [right: stats + tips]

Backend (qa_chain, session state, ask()) is untouched.
"""

import streamlit as st

from rag.chain import qa_chain

from ui.styles import apply_styles
from ui.session import init_session
from ui.sidebar import render_sidebar
from ui.header import render_header
from ui.chips import render_chips
from ui.chat import render_chat
from ui.right_panel import render_right_panel
from ui.constants import MAX_HISTORY

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

    except Exception:
        answer = "I'm temporarily unable to reach the knowledge base."
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