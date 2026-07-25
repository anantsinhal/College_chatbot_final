import streamlit as st


def apply_styles():
    st.markdown(
        """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #0b1120;
    color: white;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: white; }

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.08);
    background: #1f2937;
    color: white;
    transition: .25s;
}

.stButton > button:hover {
    background: #7c3aed;
    border-color: #7c3aed;
}

[data-testid="stChatMessage"] {
    background: #111827;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,.06);
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border-top: 1px solid rgba(255,255,255,.08);
    background: #0b1120;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 20px; }
</style>""",
        unsafe_allow_html=True,
    )