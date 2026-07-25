import streamlit as st


def render_sources(sources: list):
    if not sources:
        return

    links_html = "".join(
        '<a href="{s}" target="_blank" style="display:block;color:#c4b5fd;font-size:13px;'
        'word-break:break-all;text-decoration:none;margin-top:4px;">{s}</a>'.format(s=s)
        for s in sources
        if s
    )

    # Single-line HTML: CommonMark code-block rule cannot fire on a one-liner.
    html = (
        '<div style="margin-top:10px;background:#1e293b;border-left:4px solid #8b5cf6;'
        'padding:12px 14px;border-radius:10px;">'
        '<div style="color:#a78bfa;font-size:12px;font-weight:600;text-transform:uppercase;'
        'letter-spacing:.05em;margin-bottom:6px;">Sources</div>'
        + links_html
        + "</div>"
    )

    st.markdown(html, unsafe_allow_html=True)