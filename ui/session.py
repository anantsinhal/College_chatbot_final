import streamlit as st


def init_session() -> None:
    """Initialise all session-state keys that the app relies on."""
    defaults = {
        "messages":     [],   # list of {role, content, sources, intent}
        "chat_history": [],   # list of (question, answer) tuples for RAG context
        "pending":      None, # question injected by sidebar button or chip click
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value