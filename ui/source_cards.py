"""
Source citation strip rendered below each assistant message.
"""

import streamlit as st


def render_sources(sources: list) -> None:
    if not sources:
        return

    links_html = "".join(
        '<a class="smit-source-link" href="{s}" target="_blank">{s}</a>'.format(s=s)
        for s in sources
        if s
    )

    # Build as one continuous string — no newlines — so CommonMark never
    # sees a line with >=4 leading spaces (which would trigger a code block).
    html = (
        '<div class="smit-sources">'
        '<div class="smit-sources-label">&#128206; Sources</div>'
        + links_html
        + "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)