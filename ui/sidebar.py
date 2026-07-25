import streamlit as st
from ui.constants import SUGGESTED, ANNOUNCEMENTS, EVENTS


def render_sidebar():
    with st.sidebar:

        # ── Logo / brand ──────────────────────────────────────────────────
        st.markdown(
            '<div style="text-align:center;padding:20px 10px;">'
            '<div style="font-size:52px;margin-bottom:10px;">&#127891;</div>'
            '<h2 style="margin-bottom:4px;color:white;">SMIT AI</h2>'
            '<p style="color:#9CA3AF;font-size:14px;">Campus Assistant</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Suggested questions ───────────────────────────────────────────
        st.subheader("&#128161; Suggested Questions")

        for q in SUGGESTED:
            if st.button(q, use_container_width=True):
                st.session_state.pending = q

        st.divider()

        # ── Announcements ─────────────────────────────────────────────────
        st.subheader("&#128226; Announcements")

        for icon, text, time in ANNOUNCEMENTS:
            st.markdown(
                '<div style="background:#1f2937;padding:12px;border-radius:12px;margin-bottom:10px;">'
                f'<b>{icon} {text}</b><br>'
                f'<span style="color:#9CA3AF;font-size:12px;">{time}</span>'
                '</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Upcoming events ───────────────────────────────────────────────
        st.subheader("&#128197; Upcoming Events")

        for month, day, title, sub in EVENTS:
            st.markdown(
                '<div style="display:flex;gap:12px;margin-bottom:12px;background:#1f2937;padding:12px;border-radius:12px;">'
                '<div style="width:55px;background:#7c3aed;border-radius:12px;text-align:center;padding:6px;color:white;flex-shrink:0;">'
                f'<div style="font-size:12px;">{month}</div>'
                f'<div style="font-size:22px;font-weight:700;">{day}</div>'
                '</div>'
                f'<div><b style="color:white;">{title}</b><br>'
                f'<span style="color:#9CA3AF;font-size:12px;">{sub}</span></div>'
                '</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Clear button ──────────────────────────────────────────────────
        if st.button("&#128465; Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()