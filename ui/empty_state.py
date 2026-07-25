"""
Empty-state card grid shown when there are no messages yet.
Each card is a clickable topic shortcut.
"""

import streamlit as st
from ui.constants import EMPTY_PROMPTS


def _h(html: str) -> str:
    return " ".join(html.split())


def render_empty_state() -> None:
    title_html = _h(
        '<div class="smit-empty-title">Popular topics &mdash; click to explore</div>'
    )
    st.markdown(title_html, unsafe_allow_html=True)

    # Render cards in rows of 3
    for row_start in range(0, len(EMPTY_PROMPTS), 3):
        row = EMPTY_PROMPTS[row_start : row_start + 3]
        cols = st.columns(len(row))
        for col, (icon, label, sub) in zip(cols, row):
            with col:
                card_html = _h(f"""
                    <div class="smit-empty-card">
                      <div class="smit-empty-card-icon">{icon}</div>
                      <div class="smit-empty-card-label">{label}</div>
                      <div class="smit-empty-card-sub">{sub}</div>
                    </div>
                """)
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button(label, key=f"empty_{label}", use_container_width=True):
                    st.session_state.pending = label