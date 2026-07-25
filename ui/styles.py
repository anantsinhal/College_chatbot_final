import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Single authoritative CSS block.
# Rules are grouped:
#   1. Reset / global
#   2. Sidebar
#   3. Buttons (Streamlit native)
#   4. Chat messages & input
#   5. Hero card
#   6. Greeting
#   7. Chips
#   8. Empty state
#   9. Source cards
#  10. Right panel stats
#  11. Scrollbar
# ─────────────────────────────────────────────────────────────────────────────

_CSS = """\
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── 1. Reset / global ───────────────────────────────────────────────────── */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #0b1120;
    color: #f1f5f9;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* ── 2. Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label { color: #f1f5f9; }

/* ── 3. Buttons ──────────────────────────────────────────────────────────── */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.08);
    background: #1f2937;
    color: #f1f5f9;
    font-size: 13px;
    padding: 8px 14px;
    text-align: left;
    transition: background .2s, border-color .2s;
}
.stButton > button:hover {
    background: #7c3aed;
    border-color: #7c3aed;
    color: white;
}

/* ── 4. Chat messages & input ────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: #111827;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,.06);
    margin-bottom: 12px;
}
[data-testid="stChatInput"] textarea {
    background: #1f2937 !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 14px !important;
}

/* ── 5. Hero card ────────────────────────────────────────────────────────── */
.smit-hero {
    background: linear-gradient(135deg, #6d28d9, #9333ea, #7c3aed);
    border-radius: 24px;
    padding: 35px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 15px 45px rgba(124,58,237,.35);
    position: relative;
    overflow: hidden;
}
.smit-hero-toprow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}
.smit-hero-eyebrow {
    background: rgba(255,255,255,.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,.25);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
}
.smit-hero-badge {
    background: rgba(255,255,255,.2);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
}
.smit-hero h2 {
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 8px 0;
    color: white;
}
.smit-hero p {
    color: #ede9fe;
    font-size: 15px;
    line-height: 1.6;
    margin: 0 0 18px 0;
}
.smit-hero-stats {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}
.smit-hero-stat {
    background: rgba(255,255,255,.12);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,.2);
    padding: 10px 16px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 500;
}
.smit-hero-icon {
    position: absolute;
    right: 30px;
    bottom: 20px;
    font-size: 80px;
    opacity: .15;
    pointer-events: none;
    line-height: 1;
}

/* ── 6. Greeting ─────────────────────────────────────────────────────────── */
.smit-greeting {
    margin-bottom: 6px;
}
.smit-greeting h3 {
    font-size: 22px;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px 0;
}
.smit-greeting p {
    color: #94a3b8;
    font-size: 14px;
    margin: 0;
}

/* ── 7. Topic chips ──────────────────────────────────────────────────────── */
.smit-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 14px 0 20px 0;
}
.smit-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1e293b;
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 13px;
    font-weight: 500;
    color: #cbd5e1;
    cursor: pointer;
    transition: background .2s, border-color .2s, color .2s;
    white-space: nowrap;
}
.smit-chip:hover {
    background: #7c3aed;
    border-color: #7c3aed;
    color: white;
}

/* ── 8. Empty state ──────────────────────────────────────────────────────── */
.smit-empty {
    margin: 10px 0 24px 0;
}
.smit-empty-title {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 12px;
}
.smit-empty-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
    gap: 12px;
}
.smit-empty-card {
    background: #1e293b;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px;
    padding: 16px;
    cursor: pointer;
    transition: border-color .2s, background .2s;
}
.smit-empty-card:hover {
    background: #263347;
    border-color: #7c3aed;
}
.smit-empty-card-icon {
    font-size: 24px;
    margin-bottom: 8px;
}
.smit-empty-card-label {
    font-size: 14px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 4px;
}
.smit-empty-card-sub {
    font-size: 12px;
    color: #64748b;
}

/* ── 9. Source cards ─────────────────────────────────────────────────────── */
.smit-sources {
    margin-top: 10px;
    background: #1e293b;
    border-left: 4px solid #8b5cf6;
    padding: 12px 14px;
    border-radius: 10px;
}
.smit-sources-label {
    color: #a78bfa;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 6px;
}
.smit-source-link {
    display: block;
    color: #c4b5fd;
    font-size: 13px;
    word-break: break-all;
    text-decoration: none;
    margin-top: 4px;
}
.smit-source-link:hover { color: #ede9fe; text-decoration: underline; }

/* ── 10. Right panel stats ───────────────────────────────────────────────── */
.smit-stat-block {
    margin-bottom: 24px;
}
.smit-stat-header {
    font-size: 18px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.smit-stat-row {
    margin-bottom: 16px;
}
.smit-stat-label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 2px;
}
.smit-stat-value {
    font-size: 32px;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1.1;
}
.smit-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,.08);
    margin: 20px 0;
}
.smit-tips {
    background: #1e293b;
    border-radius: 16px;
    padding: 16px;
}
.smit-tips-header {
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.smit-tip-item {
    color: #94a3b8;
    font-size: 13px;
    padding: 5px 0;
    border-bottom: 1px solid rgba(255,255,255,.05);
}
.smit-tip-item:last-child { border-bottom: none; }

/* ── 11. Scrollbar ───────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 20px; }
</style>
"""


def apply_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)