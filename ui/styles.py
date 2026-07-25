import streamlit as st


def apply_styles():
    st.markdown(
        """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp{
    font-family:'Inter',sans-serif;
    background:#0b1120;
    color:white;
}

#MainMenu,
footer,
header{
    visibility:hidden;
}

/* Main */

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
    max-width:1400px;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span{
    color:white;
}

/* Buttons */

.stButton>button{
    width:100%;
    border-radius:14px;
    border:1px solid rgba(255,255,255,.08);
    background:#1f2937;
    color:white;
    transition:.25s;
}

.stButton>button:hover{
    background:#7c3aed;
    border-color:#7c3aed;
}

/* Chat */

[data-testid="stChatMessage"]{
    background:#111827;
    border-radius:18px;
    padding:18px;
    border:1px solid rgba(255,255,255,.06);
    margin-bottom:12px;
}

/* Chat input */

[data-testid="stChatInput"]{
    border-top:1px solid rgba(255,255,255,.08);
    background:#0b1120;
}

/* Hero Card */

.hero-card{
    background:linear-gradient(135deg,#6d28d9,#9333ea,#7c3aed);
    border-radius:24px;
    padding:35px;
    color:white;
    margin-bottom:25px;
    box-shadow:0 15px 45px rgba(124,58,237,.35);
}

.hero-title{
    font-size:34px;
    font-weight:800;
}

.hero-sub{
    margin-top:12px;
    color:#ede9fe;
    font-size:16px;
}

.stat-row{
    display:flex;
    gap:15px;
    margin-top:25px;
}

.stat-card{
    background:rgba(255,255,255,.12);
    backdrop-filter:blur(12px);
    padding:12px 18px;
    border-radius:14px;
    font-size:14px;
}

/* Section */

.section-title{
    color:white;
    font-size:20px;
    font-weight:700;
    margin-top:10px;
    margin-bottom:15px;
}

/* Source Box */

.source-box{
    margin-top:12px;
    background:#1f2937;
    border-left:4px solid #8b5cf6;
    padding:12px;
    border-radius:10px;
}

/* Scroll */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#7c3aed;
    border-radius:20px;
}

</style>
""",
        unsafe_allow_html=True,
    )