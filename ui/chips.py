"""
Topic chips shown below the header.
Clicking a chip sets it as the pending question.
"""

import streamlit as st
from ui.constants import CHIPS


def render_chips() -> None:
    # Render the visual chip strip (HTML only — for styling)
    chips_html = "".join(
        f'<span class="smit-chip">{icon} {label}</span>'
        for icon, label in CHIPS
    )
    st.markdown(
        f'<div class="smit-chips">{chips_html}</div>',
        unsafe_allow_html=True,
    )

    # Invisible Streamlit buttons overlapping the chips above — same row
    cols = st.columns(len(CHIPS))
    for col, (icon, label) in zip(cols, CHIPS):
        with col:
            if st.button(label, key=f"chip_{label}", use_container_width=True):
                st.session_state.pending = label