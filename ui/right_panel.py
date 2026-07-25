"""
Right panel: Quick Stats and Tips sections.
Uses CSS classes from styles.py for consistent dark-theme styling.
"""

import streamlit as st


def _h(html: str) -> str:
    return " ".join(html.split())


def render_right_panel() -> None:

    # ── Quick Stats ───────────────────────────────────────────────────────────
    st.markdown(_h("""
        <div class="smit-stat-block">

          <div class="smit-stat-header">&#128202; Quick Stats</div>

          <div class="smit-stat-row">
            <div class="smit-stat-label">Documents</div>
            <div class="smit-stat-value">100+</div>
          </div>

          <div class="smit-stat-row">
            <div class="smit-stat-label">Departments</div>
            <div class="smit-stat-value">10</div>
          </div>

          <div class="smit-stat-row">
            <div class="smit-stat-label">Response Time</div>
            <div class="smit-stat-value">&lt;2 sec</div>
          </div>

        </div>
    """), unsafe_allow_html=True)

    st.markdown('<hr class="smit-divider">', unsafe_allow_html=True)

    # ── Tips ──────────────────────────────────────────────────────────────────
    tips = [
        "Admission Process",
        "Fee Structure",
        "Placements",
        "Hostel",
        "Scholarships",
        "Faculty",
    ]
    tips_items = "".join(
        f'<div class="smit-tip-item">&#8226; {t}</div>' for t in tips
    )
    st.markdown(_h(f"""
        <div class="smit-tips">
          <div class="smit-tips-header">&#128161; Tips</div>
          <p style="color:#64748b;font-size:12px;margin:0 0 10px;">Ask questions like:</p>
          {tips_items}
        </div>
    """), unsafe_allow_html=True)