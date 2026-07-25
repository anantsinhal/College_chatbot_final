import streamlit as st


def render_sources(sources):
    if not sources:
        return

    links = "".join(
        f'<a class="smit-source-link" href="{s}" target="_blank">{s}</a>'
        for s in sources
        if s
    )

    st.markdown(
        f"""
        <div class="smit-sources">
            <div class="smit-sources-label">Sources</div>
            {links}
        </div>
        """,
        unsafe_allow_html=True,
    )