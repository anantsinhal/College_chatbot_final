import streamlit as st


def apply_styles():
    st.markdown(
        """
<style>

html, body, .stApp{
    background:#0B1020;
}

div[data-testid="stChatMessage"]{
    background:#1B2238;
    border-radius:18px;
    padding:12px;
}

.stChatInput{
    border-top:1px solid rgba(255,255,255,.08);
}

</style>
""",
        unsafe_allow_html=True,
    )