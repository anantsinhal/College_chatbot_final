import streamlit as st

from rag.chain import qa_chain

from ui.styles import apply_styles
from ui.session import init_session
from ui.sidebar import render_sidebar
from ui.greeting import render_greeting
from ui.hero import render_hero
from ui.chips import render_chips
from ui.chat import render_chat
from ui.right_panel import render_right_panel
from ui.constants import MAX_HISTORY


st.set_page_config(
    page_title="SMIT AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

st.markdown(
    """
    <style>
    .block-container{
        padding-top:3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_session()


def ask(question: str):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

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

        answer = (
            "I'm temporarily unable to reach the knowledge base."
        )

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
                question,
                answer,
            )
        )

        st.session_state.chat_history = (
            st.session_state.chat_history[-MAX_HISTORY:]
        )


render_sidebar()
st.markdown("""
<style>
.block-container{
    padding-top:1rem !important;
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([3.5, 1.2], gap="large")

with left:
    import streamlit as st

st.image(
    "assets/smit_logo.jpg",
    width=180
)

render_greeting()

   # render_hero()

render_chips()

render_chat(
        st.session_state.messages,
        ask,
    )

with right:

    render_right_panel()