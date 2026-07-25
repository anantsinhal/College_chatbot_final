import streamlit as st


def _h(html: str) -> str:
    """Collapse multi-line HTML to a single line.

    Streamlit's CommonMark parser treats any line indented >=4 spaces
    as a fenced code block, escaping the HTML to plain text even when
    unsafe_allow_html=True.  Collapsing to one line makes that rule
    impossible to trigger.
    """
    return " ".join(html.split())


def render_hero() -> None:
    html = _h("""
        <div class="smit-hero">

          <div class="smit-hero-toprow">
            <div class="smit-hero-eyebrow">&#10024; SMIT AI Assistant</div>
            <div class="smit-hero-badge">AI Powered</div>
          </div>

          <h2>Your Intelligent Campus Companion</h2>

          <p>
            Get instant answers about admissions, academics, placements,
            scholarships, hostel facilities, faculty, campus events and
            student life.
          </p>

          <div class="smit-hero-stats">
            <div class="smit-hero-stat">&#128218; 100+ Documents</div>
            <div class="smit-hero-stat">&#9889; Instant Answers</div>
            <div class="smit-hero-stat">&#127891; Campus AI</div>
          </div>

          <div class="smit-hero-icon">&#127891;</div>

        </div>
    """)
    st.markdown(html, unsafe_allow_html=True)