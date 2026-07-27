import streamlit as st


def init_session():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "pending" not in st.session_state:
        st.session_state.pending = None