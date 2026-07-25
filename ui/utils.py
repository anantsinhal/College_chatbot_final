import streamlit as st


def initialize_session():
    defaults = {
        "messages": [],
        "chat_history": [],
        "pending": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_chat():
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.rerun()