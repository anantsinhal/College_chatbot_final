"""
Header component: logo image + time-aware greeting + subtitle.
Renders as a horizontal flex row — no margin hacks needed.
"""

import streamlit as st
from datetime import datetime
import os


def _time_greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def render_header() -> None:
    greeting = _time_greeting()

    # Logo column + text column side-by-side
    logo_col, text_col = st.columns([1, 8], gap="small")

    logo_path = os.path.join("assets", "smit_logo.jpg")
    with logo_col:
        if os.path.exists(logo_path):
            st.image(logo_path, width=64)
        else:
            st.markdown('<div style="font-size:48px;">🎓</div>', unsafe_allow_html=True)

    with text_col:
        st.markdown(
            f"""
            <div style="padding: 6px 0 0 4px;">
              <div style="font-size:22px;font-weight:700;color:#f1f5f9;line-height:1.2;">
                {greeting}! 👋
              </div>
              <div style="font-size:13px;color:#64748b;margin-top:2px;">
                Ask anything about SMIT — academics, admissions, placements, hostel and more.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Thin divider below header
    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:10px 0 14px 0;">',
        unsafe_allow_html=True,
    )
