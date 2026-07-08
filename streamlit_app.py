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
    page_title="SMIT Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens & custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    :root {
        --bg-primary: #07111f;
        --bg-surface: rgba(8, 18, 33, 0.88);
        --bg-surface-strong: rgba(11, 24, 42, 0.96);
        --bg-surface-soft: rgba(255, 255, 255, 0.04);
        --accent: #7dd3fc;
        --accent-strong: #38bdf8;
        --accent-warm: #fbbf24;
        --text-primary: #f8fafc;
        --text-muted: #a6b3c6;
        --border: rgba(148, 163, 184, 0.22);
        --shadow: 0 18px 50px rgba(2, 8, 23, 0.35);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 28%),
            radial-gradient(circle at top right, rgba(251, 191, 36, 0.10), transparent 22%),
            linear-gradient(180deg, #07111f 0%, #0b172a 48%, #050b14 100%);
        color: var(--text-primary);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.6rem 1.5rem 1.35rem 1.5rem;
        margin-bottom: 1.1rem;
        background: linear-gradient(135deg, rgba(8, 18, 33, 0.94), rgba(14, 28, 48, 0.82));
        box-shadow: var(--shadow);
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(125, 211, 252, 0.14), transparent 30%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.7rem;
        border: 1px solid rgba(125, 211, 252, 0.22);
        border-radius: 999px;
        background: rgba(125, 211, 252, 0.08);
        color: var(--accent);
        font-size: 0.73rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }

    .hero-title {
        font-size: 2.1rem;
        line-height: 1.05;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 0.55rem 0;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
    }

    .hero-copy {
        color: var(--text-muted);
        font-size: 0.98rem;
        line-height: 1.6;
        max-width: 760px;
        margin: 0 0 1rem 0;
        position: relative;
        z-index: 1;
    }

    .hero-stats {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.75rem;
        position: relative;
        z-index: 1;
    }

    .hero-stat {
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.8rem 0.9rem;
        background: rgba(255, 255, 255, 0.04);
    }

    .hero-stat-value {
        color: var(--text-primary);
        font-weight: 800;
        font-size: 1.02rem;
        margin-bottom: 0.15rem;
    }

    .hero-stat-label {
        color: var(--text-muted);
        font-size: 0.82rem;
        line-height: 1.45;
    }

    [data-testid="stChatMessage"] {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 18px;
        box-shadow: var(--shadow);
        margin-bottom: 0.75rem;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        color: var(--text-primary);
        font-size: 0.98rem;
        line-height: 1.65;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        padding: 0.1rem 0.2rem;
    }

    .source-strip {
        margin-top: 0.75rem;
        padding-top: 0.6rem;
        border-top: 1px dashed var(--border);
    }

    .source-strip-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--accent);
        margin-bottom: 0.4rem;
        font-weight: 600;
    }

    .source-tag {
        display: inline-block;
        font-size: 0.74rem;
        color: #fbbf24;
        background: rgba(251, 191, 36, 0.09);
        border: 1px solid rgba(251, 191, 36, 0.22);
        border-radius: 999px;
        padding: 0.28rem 0.6rem;
        margin: 0.15rem 0.3rem 0.15rem 0;
        text-decoration: none;
    }

    .source-tag:hover {
        background: rgba(251, 191, 36, 0.18);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8, 18, 33, 0.98), rgba(5, 11, 20, 0.98));
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.3rem;
    }

    .sidebar-eyebrow {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--accent);
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 0.55rem;
    }

    .sidebar-desc {
        font-size: 0.85rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin-bottom: 1.25rem;
    }

    .sidebar-card {
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.9rem;
        background: var(--bg-surface-soft);
        margin-bottom: 1rem;
    }

    .sidebar-card-title {
        color: var(--text-primary);
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .sidebar-card-copy {
        color: var(--text-muted);
        font-size: 0.82rem;
        line-height: 1.45;
    }

    .stButton button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        color: var(--text-primary);
        text-align: left;
        font-size: 0.84rem;
        padding: 0.6rem 0.85rem;
        border-radius: 12px;
        width: 100%;
        transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
    }

    .stButton button:hover {
        border-color: rgba(125, 211, 252, 0.45);
        color: var(--accent);
        transform: translateY(-1px);
        background: rgba(125, 211, 252, 0.08);
    }

    [data-testid="stChatInput"] textarea {
        background: var(--bg-surface-strong) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 16px !important;
        box-shadow: var(--shadow);
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-muted) !important;
    }

    [data-testid="stChatInput"] button {
        border-radius: 14px;
        background: linear-gradient(135deg, var(--accent-strong), var(--accent));
        color: #052033;
        font-weight: 700;
    }

    .empty-state {
        text-align: center;
        padding: 2.8rem 1rem 1.6rem 1rem;
        color: var(--text-muted);
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.015));
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }

    .empty-state-icon {
        font-size: 2.3rem;
        margin-bottom: 0.75rem;
        opacity: 0.6;
    }

    .empty-state h3 {
        color: var(--text-primary);
        font-size: 1.15rem;
        margin-bottom: 0.45rem;
    }

    .empty-state p {
        font-size: 0.88rem;
        max-width: 420px;
        margin: 0 auto;
        line-height: 1.6;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_HISTORY_TURNS = 3
MAX_QUESTION_LENGTH = 500

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
        "official website and documents — every response cites its "
        "source so you can verify it yourself.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">What this bot knows</div>
            <div class="sidebar-card-copy">
                Admissions, programs, eligibility, fees, placements, and
                official notices indexed from SMIT pages and PDFs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-eyebrow" style="margin-top: 0.5rem;">Try asking</div>',
        unsafe_allow_html=True,
    )
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
    <div class="hero">
        <div class="hero-badge">SMIT knowledge assistant</div>
        <div class="hero-title">A cleaner way to explore SMIT.</div>
        <div class="hero-copy">
            Ask about admissions, fees, courses, placements, or policy
            details. The assistant pulls answers from the knowledge base and
            shows the sources it used.
        </div>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-value">Source-backed answers</div>
                <div class="hero-stat-label">Every response can be traced back to an indexed document.</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">Admissions to placements</div>
                <div class="hero-stat-label">Covers the core questions students usually ask first.</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">Fast follow-up chat</div>
                <div class="hero-stat-label">Conversation context stays short and focused for better replies.</div>
            </div>
        </div>
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
            <p>Programs, fees, eligibility, admissions, placements —
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
    if len(active_question) > MAX_QUESTION_LENGTH:
        st.error(
            f"Please keep your question under {MAX_QUESTION_LENGTH} characters."
        )
        st.stop()
    ask(active_question)
    st.rerun()
