import streamlit as st

from rag.chain import qa_chain

from ui.styles import apply_styles
from ui.sidebar import render_sidebar

from ui.session import init_session
from ui.constants import MAX_HISTORY


st.set_page_config(
    page_title="SMIT AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()
init_session()


def ask(question: str):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.spinner(""):
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
            ) if intent == "smit_query" else []

        except Exception:
            answer = "I'm temporarily unable to reach the knowledge base. Please try again."
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
        st.session_state.chat_history.append(
            (
                result.get("question", question),
                answer,
            )
        )

        st.session_state.chat_history = (
            st.session_state.chat_history[-MAX_HISTORY:]
        )


render_sidebar()

