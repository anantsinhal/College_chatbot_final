"""
Global CSS for the SMIT AI dark theme.
Inject once at app startup via apply_styles().
No margin hacks — layout is handled by st.columns() / st.container().
"""

import streamlit as st


_CSS = """
<style>

/* ── Base ──────────────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: #0B1020 !important;
    color: #f1f5f9;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Remove Streamlit's default top padding so logo sits at the top */
[data-testid="stAppViewContainer"] > .main > .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* Sidebar base */
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* ── Header ────────────────────────────────────────────────────────────────── */
.smit-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 0 0 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 12px;
}
.smit-header-text h2 {
    margin: 0 0 2px;
    font-size: 22px;
    font-weight: 700;
    color: #f1f5f9;
}
.smit-header-text p {
    margin: 0;
    font-size: 13px;
    color: #64748b;
}

/* ── Chips ─────────────────────────────────────────────────────────────────── */
.smit-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.smit-chip {
    background: #1e293b;
    border: 1px solid rgba(124,58,237,0.35);
    color: #a5b4fc;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 13px;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
    white-space: nowrap;
}
.smit-chip:hover {
    background: #7c3aed22;
    border-color: #7c3aed;
}

/* Hide the invisible chip buttons (they overlap the HTML chips above) */
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    opacity: 0 !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    pointer-events: auto !important;
    position: absolute !important;
}

/* ── Chat messages ─────────────────────────────────────────────────────────── */
div[data-testid="stChatMessage"] {
    background: #1B2238;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 6px;
}

/* ── Chat input ────────────────────────────────────────────────────────────── */
[data-testid="stChatInput"] {
    border-top: 1px solid rgba(255,255,255,0.08);
    background: #111827;
    border-radius: 12px;
}
[data-testid="stChatInput"] textarea {
    background: #1e293b !important;
    color: #f1f5f9 !important;
    border-radius: 10px;
}

/* ── Empty state cards ─────────────────────────────────────────────────────── */
.smit-empty-title {
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 10px;
}
.smit-empty-card {
    background: #1e293b;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    height: 100%;
}
.smit-empty-card-icon  { font-size: 26px; margin-bottom: 6px; }
.smit-empty-card-label { font-size: 14px; font-weight: 600; color: #e2e8f0; }
.smit-empty-card-sub   { font-size: 11px; color: #64748b; margin-top: 3px; }

/* ── Right panel ───────────────────────────────────────────────────────────── */
.smit-stat-block {
    background: #1e293b;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}
.smit-stat-header {
    font-weight: 700;
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 10px;
}
.smit-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.smit-stat-row:last-child { border-bottom: none; }
.smit-stat-label { font-size: 13px; color: #64748b; }
.smit-stat-value { font-size: 14px; font-weight: 700; color: #a5b4fc; }
.smit-divider    { border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 12px 0; }
.smit-tips { background: #1e293b; border-radius: 14px; padding: 16px; }
.smit-tips-header {
    font-weight: 700;
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 8px;
}
.smit-tip-item {
    font-size: 13px;
    color: #64748b;
    padding: 4px 0;
}

/* ── Sources ───────────────────────────────────────────────────────────────── */
.smit-sources {
    margin-top: 8px;
    padding: 8px 12px;
    background: #0f172a;
    border-radius: 10px;
    font-size: 12px;
}
.smit-sources-label { color: #64748b; font-weight: 600; margin-bottom: 4px; }
.smit-source-link {
    display: inline-block;
    color: #818cf8;
    margin-right: 8px;
    text-decoration: none;
    word-break: break-all;
}
.smit-source-link:hover { text-decoration: underline; }

</style>
"""


def apply_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)