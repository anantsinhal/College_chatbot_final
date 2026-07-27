"""
Chat area: empty-state cards when no messages, then message history,
then the chat input fixed at the bottom.
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

    # ── Chat input (Streamlit keeps this at the bottom automatically) ─────────
    typed = st.chat_input("Ask anything about SMIT...")

    # Consume a pending question fired by a chip or sidebar button
    active = st.session_state.pending or typed
    st.session_state.pending = None

    if active:
        ask_callback(active.strip())
        st.rerun()