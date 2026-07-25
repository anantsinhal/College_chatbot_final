"""
Topic chips shown below the greeting.
Clicking a chip fires that topic as a pending question.
"""

import streamlit as st
from ui.constants import CHIPS


def _h(html: str) -> str:
    return " ".join(html.split())


def render_chips() -> None:
    # Render the chip strip as styled HTML (display only)
    chips_inner = "".join(
        f'<span class="smit-chip">{icon} {label}</span>'
        for icon, label in CHIPS
    )
    html = _h(f'<div class="smit-chips">{chips_inner}</div>')
    st.markdown(html, unsafe_allow_html=True)

    # Invisible Streamlit buttons that actually fire the pending question.
    # They are stacked in one row using columns to look like the chip row above.
    cols = st.columns(len(CHIPS))
    for col, (icon, label) in zip(cols, CHIPS):
        with col:
            # zero-height button trick: style makes it invisible; the chip HTML
            # above is what the user sees and clicks-area overlaps.
            if st.button(label, key=f"chip_{label}", use_container_width=True):
                st.session_state.pending = label