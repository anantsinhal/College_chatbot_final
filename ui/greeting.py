"""
Greeting bar shown below the hero.
Displays a time-aware greeting and a short subtitle.
"""

import streamlit as st
from datetime import datetime


def _time_greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def _h(html: str) -> str:
    return " ".join(html.split())


def render_greeting() -> None:
    greeting = _time_greeting()
    html = _h(f"""
        <div class="smit-greeting">
          <h3>{greeting}! How can I help you today?</h3>
          <p>Ask me anything about SMIT &mdash; academics, admissions, placements, hostel and more.</p>
        </div>
    """)
    st.markdown(html, unsafe_allow_html=True)