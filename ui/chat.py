import streamlit as st
from ui.source_cards import render_sources


def render_chat(messages, ask_callback):
    """
    Renders chat history and chat input.
    """

    # Display previous messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if msg["role"] == "assistant":
                render_sources(msg.get("sources", []))

    # Chat input
    typed = st.chat_input("Ask anything about SMIT...")

    # Either user typed a question or clicked a suggestion/chip
    active = st.session_state.pending or typed
    st.session_state.pending = None

    if active:
        ask_callback(active.strip())
        st.rerun()