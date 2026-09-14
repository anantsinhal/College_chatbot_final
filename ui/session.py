import streamlit as st
from ui.thread_store import create_thread, get_thread, save_thread


def init_session():

    if "thread_id" not in st.session_state:
        thread = create_thread()
        st.session_state.thread_id = thread.thread_id

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "pending" not in st.session_state:
        st.session_state.pending = None

    if "last_error" not in st.session_state:
        st.session_state.last_error = None

    thread = get_thread(st.session_state.thread_id)
    if thread is not None:
        st.session_state.messages = thread.messages
        st.session_state.chat_history = thread.chat_history


def save_active_thread() -> None:
    save_thread(
        st.session_state.thread_id,
        st.session_state.messages,
        st.session_state.chat_history,
    )