"""
SMIT AI Assistant - Dark purple theme Streamlit UI
Run with: streamlit run streamlit_app.py
"""
import streamlit as st
from rag.chain import qa_chain

st.set_page_config(
    page_title="SMIT AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { font-family: 'Inter', system-ui, sans-serif !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* ── page ── */
.stApp { background: #0d0f1a !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #13152a !important;
    border-right: 1px solid rgba(108,99,255,0.15) !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── sidebar scrollbar ── */
[data-testid="stSidebar"]::-webkit-scrollbar { width: 3px; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: #6c63ff44; border-radius: 2px; }

/* ── all sidebar text ── */
[data-testid="stSidebar"] * { color: #c8cfe0 !important; }

/* ── sidebar buttons ── */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: none !important;
    color: #8892a4 !important;
    text-align: left !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    width: 100% !important;
    transition: all 0.15s !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(108,99,255,0.15) !important;
    color: #a78bfa !important;
}

/* ── main area buttons (chips) ── */
.main-content .stButton button {
    background: #1e2140 !important;
    border: 1px solid rgba(108,99,255,0.25) !important;
    color: #c8cfe0 !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    padding: 5px 14px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.15s !important;
    white-space: nowrap !important;
}
.main-content .stButton button:hover {
    background: rgba(108,99,255,0.2) !important;
    border-color: #6c63ff !important;
    color: #a78bfa !important;
}

/* ── chat messages ── */
[data-testid="stChatMessage"] {
    background: #1a1d35 !important;
    border: 1px solid rgba(108,99,255,0.12) !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: #e0e4f0 !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── chat input area ── */
[data-testid="stChatInput"] {
    background: #13152a !important;
    border-top: 1px solid rgba(108,99,255,0.15) !important;
    padding: 12px 20px !important;
}
[data-testid="stChatInput"] textarea {
    background: #1e2140 !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    border-radius: 28px !important;
    color: #e0e4f0 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px 20px !important;
    box-shadow: 0 0 0 0 transparent !important;
    transition: border-color 0.2s !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #4a5270 !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #6c63ff, #a78bfa) !important;
    border: none !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.4) !important;
}

/* ── spinner ── */
[data-testid="stSpinner"] { color: #6c63ff !important; }

/* ── custom HTML components ── */
.smit-sidebar-header {
    padding: 18px 16px 14px;
    border-bottom: 1px solid rgba(108,99,255,0.15);
    margin-bottom: 4px;
}
.smit-logo-row {
    display: flex;
    align-items: center;
    gap: 10px;
}
.smit-logo-icon {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6c63ff, #a78bfa);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 12px rgba(108,99,255,0.4);
    flex-shrink: 0;
}
.smit-logo-name { font-size: 14px; font-weight: 700; color: #e8eaf0; line-height: 1.2; }
.smit-logo-sub  { font-size: 11px; color: #6c7494; margin-top: 1px; }

.sidebar-section-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6c63ff !important;
    font-weight: 700;
    padding: 14px 16px 6px;
}

.announce-item {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    padding: 8px 16px;
    cursor: pointer;
    transition: background 0.15s;
}
.announce-item:hover { background: rgba(108,99,255,0.08); }
.announce-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}
.announce-text { font-size: 12px; color: #c0c8de; line-height: 1.4; font-weight: 500; }
.announce-time { font-size: 11px; color: #555d7a; margin-top: 2px; }

.event-item {
    display: flex;
    gap: 10px;
    padding: 8px 16px;
    align-items: flex-start;
    cursor: pointer;
    transition: background 0.15s;
}
.event-item:hover { background: rgba(108,99,255,0.08); }
.event-date-box {
    min-width: 40px;
    background: #1e2140;
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 10px;
    padding: 6px 4px;
    text-align: center;
}
.event-month { font-size: 9px; color: #6c63ff; font-weight: 700; text-transform: uppercase; }
.event-day   { font-size: 18px; font-weight: 800; color: #e8eaf0; line-height: 1.1; }
.event-info  {}
.event-title { font-size: 12px; font-weight: 600; color: #d0d8f0; line-height: 1.4; }
.event-sub   { font-size: 11px; color: #555d7a; margin-top: 2px; }

/* ── hero banner ── */
.smit-hero {
    background: linear-gradient(135deg, #1a0a5e 0%, #3d2a9e 30%, #6c63ff 65%, #c084fc 100%);
    border-radius: 20px;
    padding: 26px 28px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(108,99,255,0.35);
}
.smit-hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.smit-hero::after {
    content: '';
    position: absolute;
    bottom: -30px; right: 60px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.smit-hero-eyebrow {
    font-size: 11px;
    color: #c4b5fd;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
    position: relative; z-index: 1;
}
.smit-hero h2 {
    font-size: 22px;
    font-weight: 800;
    color: #fff;
    margin: 0 0 8px 0;
    line-height: 1.3;
    position: relative; z-index: 1;
}
.smit-hero p {
    font-size: 13px;
    color: #ddd6fe;
    margin: 0;
    line-height: 1.6;
    max-width: 480px;
    position: relative; z-index: 1;
}
.smit-hero-icon {
    position: absolute;
    right: 28px; top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.15;
    z-index: 0;
}

/* ── greeting ── */
.smit-greeting {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0 14px;
}
.smit-greeting-name { font-size: 20px; font-weight: 700; color: #e8eaf0; }
.smit-greeting-sub  { font-size: 13px; color: #5a6280; margin-top: 2px; }
.smit-greeting-badge {
    background: linear-gradient(135deg, #6c63ff, #a78bfa);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(108,99,255,0.4);
}

/* ── chips row ── */
.smit-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 4px;
}
.smit-chip {
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid rgba(108,99,255,0.25);
    background: #1a1d35;
    color: #9aa3c0;
    font-size: 12px;
    white-space: nowrap;
}

/* ── source block ── */
.smit-sources {
    margin-top: 10px;
    padding: 10px 14px;
    background: rgba(108,99,255,0.08);
    border-left: 3px solid #6c63ff;
    border-radius: 0 10px 10px 0;
}
.smit-sources-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6c63ff;
    font-weight: 700;
    margin-bottom: 5px;
}
.smit-source-link {
    display: block;
    font-size: 12px;
    color: #a78bfa;
    text-decoration: none;
    line-height: 1.7;
    word-break: break-all;
}
.smit-source-link:hover { text-decoration: underline; }

/* ── empty state ── */
.smit-empty {
    text-align: center;
    padding: 48px 24px;
    background: #13152a;
    border: 1px dashed rgba(108,99,255,0.2);
    border-radius: 20px;
    margin: 8px 0 16px;
}
.smit-empty-icon { font-size: 48px; margin-bottom: 14px; opacity: 0.8; }
.smit-empty h3 { font-size: 18px; font-weight: 700; color: #e0e4f0; margin-bottom: 8px; }
.smit-empty p  { font-size: 13px; color: #5a6280; line-height: 1.6; max-width: 380px; margin: 0 auto; }

/* ── scrollbar (main) ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(108,99,255,0.25); border-radius: 2px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────
MAX_HISTORY = 3

SUGGESTED = [
    "What B.Tech programs does SMIT offer?",
    "What is the fee structure for B.Tech CSE?",
    "How do I get admission into SMIT?",
    "What is the placement record at SMIT?",
    "Does SMIT offer scholarships?",
]

CHIPS = [
    ("📅", "Academic Calendar"), ("💰", "Fee Structure"),
    ("🔬", "Internship Opportunities"), ("🚌", "Transport Info"),
    ("🍽", "Mess Menu"), ("🗺", "Campus Map"),
]

ANNOUNCEMENTS = [
    ("#e53e3e", "Mid-Sem Exam Schedule Released", "2 days ago"),
    ("#6c63ff", "SMIT Tech Fest 'Kaalrav' Registrations Open!", "1 week ago"),
    ("#a78bfa", "Internship Drive by Infosys on 15th July", "1 week ago"),
]

EVENTS = [
    ("JUL", "15", "Kaalrav 2026 - Tech Fest", "SMIT Campus · 10:00 AM"),
    ("JUL", "20", "End Sem Form Deadline", "All Departments · 11:59 PM"),
    ("AUG", "05", "Independence Day Event", "SMIT Auditorium · 09:00 AM"),
]

# ── Session state ─────────────────────────────────────────────────────────
for key, val in [("messages", []), ("chat_history", []), ("pending", None)]:
    if key not in st.session_state:
        st.session_state[key] = val


def ask(question: str):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner(""):
        try:
            result = qa_chain.invoke({
                "question": question,
                "chat_history": st.session_state.chat_history,
            })
            answer  = result["answer"]
            intent  = result.get("intent", "smit_query")
            sources = sorted({
                doc.metadata.get("source", "")
                for doc in result.get("source_documents", [])
            }) if intent == "smit_query" else []
        except Exception:
            answer, sources, intent = (
                "I'm temporarily unable to reach the knowledge base. Please try again.",
                [], "error",
            )
    st.session_state.messages.append({
        "role": "assistant", "content": answer,
        "sources": sources, "intent": intent,
    })
    if intent == "smit_query":
        st.session_state.chat_history.append(
            (result.get("question", question), answer)
        )
        st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY:]


# ── SIDEBAR ──────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo header
    st.markdown("""
    <div class="smit-sidebar-header">
        <div class="smit-logo-row">
            <div class="smit-logo-icon">🎓</div>
            <div>
                <div class="smit-logo-name">SMIT AI Assistant</div>
                <div class="smit-logo-sub">Sikkim Manipal University</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Suggested questions
    st.markdown('<div class="sidebar-section-label">Ask me about</div>', unsafe_allow_html=True)
    for q in SUGGESTED:
        if st.button(q, key=f"s_{q}", use_container_width=True):
            st.session_state.pending = q

    # Announcements
    st.markdown('<div class="sidebar-section-label">Announcements</div>', unsafe_allow_html=True)
    ann_html = ""
    for dot, title, time in ANNOUNCEMENTS:
        ann_html += f"""
        <div class="announce-item">
            <div class="announce-dot" style="background:{dot}"></div>
            <div>
                <div class="announce-text">{title}</div>
                <div class="announce-time">{time}</div>
            </div>
        </div>"""
    st.markdown(ann_html, unsafe_allow_html=True)

    # Events
    st.markdown('<div class="sidebar-section-label">Upcoming Events</div>', unsafe_allow_html=True)
    ev_html = ""
    for month, day, title, sub in EVENTS:
        ev_html += f"""
        <div class="event-item">
            <div class="event-date-box">
                <div class="event-month">{month}</div>
                <div class="event-day">{day}</div>
            </div>
            <div class="event-info">
                <div class="event-title">{title}</div>
                <div class="event-sub">{sub}</div>
            </div>
        </div>"""
    st.markdown(ev_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Clear conversation", use_container_width=True, key="clear"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ── MAIN ─────────────────────────────────────────────────────────────────
# Greeting
st.markdown("""
<div class="smit-greeting">
    <div>
        <div class="smit-greeting-name">Hey, Anant 👋</div>
        <div class="smit-greeting-sub">How can I help you today?</div>
    </div>
    <div class="smit-greeting-badge">AI Powered</div>
</div>
""", unsafe_allow_html=True)

# Hero banner
st.markdown("""
<div class="smit-hero">
    <div class="smit-hero-eyebrow">✦ SMIT AI Assistant</div>
    <h2>Get instant answers about SMIT.</h2>
    <p>Academics, campus, events, placements and more — all in one place.</p>
    <div class="smit-hero-icon">🏛</div>
</div>
""", unsafe_allow_html=True)

# Chips (display only — actual clicks below)
chips_display = '<div class="smit-chips">' + "".join(
    f'<div class="smit-chip">{i} {l}</div>' for i, l in CHIPS
) + "</div>"
st.markdown(chips_display, unsafe_allow_html=True)

# Chip buttons (functional)
cols = st.columns(len(CHIPS))
for idx, (icon, label) in enumerate(CHIPS):
    with cols[idx]:
        if st.button(f"{icon} {label}", key=f"c_{label}"):
            st.session_state.pending = label

st.markdown("<br>", unsafe_allow_html=True)

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="smit-empty">
        <div class="smit-empty-icon">🤖</div>
        <h3>Ask anything about SMIT</h3>
        <p>Programs, fees, eligibility, admissions, placements, scholarships —
        choose a topic above or type your question below.</p>
    </div>
    """, unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        sources = msg.get("sources", [])
        if msg["role"] == "assistant" and sources:
            links = "".join(
                f'<a class="smit-source-link" href="{s}" target="_blank">{s}</a>'
                for s in sources if s
            )
            st.markdown(f"""
            <div class="smit-sources">
                <div class="smit-sources-label">Sources</div>
                {links}
            </div>""", unsafe_allow_html=True)

# Input
typed = st.chat_input("Ask anything about SMIT...")
active = st.session_state.pending or typed
st.session_state.pending = None
if active:
    ask(active.strip())
    st.rerun()