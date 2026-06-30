"""
Streamlit frontend for the SMIT RAG chatbot.

Run with:
    streamlit run streamlit_app.py

This is the user-facing chat interface. The CLI version (app.py) stays
unchanged for quick terminal testing -- this file wraps the same
rag.chain.qa_chain in a proper web UI.
"""

import streamlit as st

from rag.chain import qa_chain

# ---------------------------------------------------------------------------
# Page config -- must be the first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SMIT Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens & custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    :root {
        --bg-primary: #0F172A;
        --bg-panel: #1E293B;
        --bg-panel-hover: #273449;
        --accent: #38BDF8;
        --accent-dim: #1A4A63;
        --text-primary: #F1F5F9;
        --text-muted: #94A3B8;
        --source-tag: #F59E0B;
        --border: #334155;
    }

    .stApp {
        background: var(--bg-primary);
    }

    .smit-header {
        padding: 1.25rem 0 0.5rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    .smit-header h1 {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.01em;
    }
    .smit-header p {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin: 0.25rem 0 0 0;
    }

    [data-testid="stChatMessage"] {
        background: var(--bg-panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.25rem 0.5rem;
    }

    .source-strip {
        margin-top: 0.75rem;
        padding-top: 0.6rem;
        border-top: 1px dashed var(--border);
    }
    .source-strip-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 0.4rem;
        font-weight: 600;
    }
    .source-tag {
        display: inline-block;
        font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
        font-size: 0.72rem;
        color: var(--source-tag);
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 5px;
        padding: 0.2rem 0.5rem;
        margin: 0.15rem 0.3rem 0.15rem 0;
        text-decoration: none;
    }
    .source-tag:hover {
        background: rgba(245, 158, 11, 0.16);
    }

    [data-testid="stSidebar"] {
        background: var(--bg-panel);
        border-right: 1px solid var(--border);
    }
    .sidebar-eyebrow {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--accent);
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .sidebar-desc {
        font-size: 0.82rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin-bottom: 1.25rem;
    }

    .stButton button {
        background: var(--bg-panel-hover);
        border: 1px solid var(--border);
        color: var(--text-primary);
        text-align: left;
        font-size: 0.82rem;
        padding: 0.55rem 0.8rem;
        border-radius: 8px;
        width: 100%;
        transition: border-color 0.15s ease;
    }
    .stButton button:hover {
        border-color: var(--accent);
        color: var(--accent);
    }

    [data-testid="stChatInput"] textarea {
        background: var(--bg-panel) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
    }

    .empty-state {
        text-align: center;
        padding: 2.5rem 1rem;
        color: var(--text-muted);
    }
    .empty-state-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        opacity: 0.6;
    }
    .empty-state h3 {
        color: var(--text-primary);
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }
    .empty-state p {
        font-size: 0.85rem;
        max-width: 360px;
        margin: 0 auto;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_HISTORY_TURNS = 3

SUGGESTED_QUESTIONS = [
    "What B.Tech programs does SMIT offer?",
    "What is the fee structure for B.Tech?",
    "How do I get admission into SMIT?",
    "What is the placement record at SMIT?",
]

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def ask(question: str):
    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("Looking through SMIT's records..."):
        try:
            result = qa_chain.invoke(
                {"question": question, "chat_history": st.session_state.chat_history}
            )
            answer = result["answer"]
            sources = sorted(
                {doc.metadata.get("source", "") for doc in result["source_documents"]}
            )
        except Exception as e:
            answer = (
                "I'm temporarily unable to reach the knowledge base. "
                "This is usually a rate limit or connection issue on our "
                "end -- please try again in a moment."
            )
            sources = []
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources, "error": str(e)}
            )
            return

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
    st.session_state.chat_history.append((question, answer))
    st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY_TURNS:]


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-eyebrow">SMIT · Sikkim</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Ask about SMIT</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-desc">Answers are pulled directly from SMIT\'s '
        "official website and documents \u2014 every response cites its "
        "source so you can verify it yourself.</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-eyebrow" style="margin-top: 0.5rem;">Try asking</div>', unsafe_allow_html=True)
    for question in SUGGESTED_QUESTIONS:
        if st.button(question, key=f"suggest_{question}", use_container_width=True):
            st.session_state.pending_question = question

    st.markdown("---")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="smit-header">
        <h1>SMIT Assistant</h1>
        <p>Sikkim Manipal Institute of Technology \u00b7 Programs, fees, admissions & more</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">🎓</div>
            <h3>Ask anything about SMIT</h3>
            <p>Programs, fees, eligibility, admissions, placements \u2014
            pick a question on the left or type your own below.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            tags = "".join(
                f'<span class="source-tag">{source}</span>'
                for source in message["sources"]
            )
            st.markdown(
                f"""
                <div class="source-strip">
                    <div class="source-strip-label">Sources</div>
                    {tags}
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------
typed_question = st.chat_input("Ask about SMIT...")

active_question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if active_question:
    ask(active_question)
    st.rerun()