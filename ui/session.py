import streamlit as st

def init_session():
    defaults = {
        "messages": [],
        "chat_history": [],
        "pending": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value