import streamlit as st


def render_hero():
    st.markdown("""
    <div class="smit-hero">

    <div style="display:flex;justify-content:space-between;align-items:center;">

        <div class="smit-hero-eyebrow">
            ✨ SMIT AI Assistant
        </div>

        <div class="smit-greeting-badge">
            AI Powered
        </div>

    </div>

    <h2>Your Intelligent Campus Companion</h2>

    <p>
    Get instant answers about admissions, academics,
    placements, scholarships, hostel facilities,
    faculty, campus events and student life.
    </p>

    <div style="display:flex;gap:14px;margin-top:18px;flex-wrap:wrap;position:relative;z-index:2;">

        <div class="hero-stat">📚 100+ Documents</div>

        <div class="hero-stat">⚡ Instant Answers</div>

        <div class="hero-stat">🎓 Campus AI</div>

    </div>

    <div class="smit-hero-icon">
        🎓
    </div>

    </div>
    """, unsafe_allow_html=True)