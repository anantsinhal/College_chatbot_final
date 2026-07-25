"""
Chat history display and input handler.
"""

import streamlit as st
from ui.source_cards import render_sources
from ui.empty_state import render_empty_state


def render_chat(messages: list, ask_callback) -> None:
    # ── Empty state ───────────────────────────────────────────────────────────
    if not messages:
        render_empty_state()

    # ── Message history ───────────────────────────────────────────────────────
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                render_sources(msg.get("sources", []))

    # ── Input ─────────────────────────────────────────────────────────────────
    typed = st.chat_input("Ask anything about SMIT...")

    # Consume pending question (from sidebar button / chip click)
    active = st.session_state.pending or typed
    st.session_state.pending = None

    if active:
        ask_callback(active.strip())
        st.rerun()