"""
Left sidebar: branding, suggested questions, announcements, events, clear button.
"""

import streamlit as st
from ui.constants import SUGGESTED, ANNOUNCEMENTS, EVENTS


def _h(html: str) -> str:
    return " ".join(html.split())


def render_sidebar() -> None:
    with st.sidebar:

        # ── Branding ──────────────────────────────────────────────────────────
        st.markdown(
            '<div style="text-align:center;padding:20px 10px 10px;">'
            '<div style="font-size:52px;margin-bottom:10px;">&#127891;</div>'
            '<h2 style="margin:0 0 4px;color:#f1f5f9;">SMIT AI</h2>'
            '<p style="color:#9CA3AF;font-size:14px;margin:0;">Campus Assistant</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Suggested questions ───────────────────────────────────────────────
        st.markdown(
            '<p style="color:#94a3b8;font-size:11px;font-weight:700;'
            'text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">'
            '&#128161; Suggested Questions</p>',
            unsafe_allow_html=True,
        )

        for q in SUGGESTED:
            if st.button(q, use_container_width=True, key=f"sq_{q}"):
                st.session_state.pending = q

        st.divider()

        # ── Announcements ─────────────────────────────────────────────────────
        st.markdown(
            '<p style="color:#94a3b8;font-size:11px;font-weight:700;'
            'text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">'
            '&#128226; Announcements</p>',
            unsafe_allow_html=True,
        )

        for icon, text, when in ANNOUNCEMENTS:
            st.markdown(
                '<div style="background:#1f2937;padding:12px;border-radius:12px;margin-bottom:8px;">'
                f'<b style="color:#f1f5f9;">{icon} {text}</b><br>'
                f'<span style="color:#6b7280;font-size:12px;">{when}</span>'
                '</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Upcoming events ───────────────────────────────────────────────────
        st.markdown(
            '<p style="color:#94a3b8;font-size:11px;font-weight:700;'
            'text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">'
            '&#128197; Upcoming Events</p>',
            unsafe_allow_html=True,
        )

        for month, day, title, sub in EVENTS:
            st.markdown(
                '<div style="display:flex;gap:12px;margin-bottom:10px;'
                'background:#1f2937;padding:12px;border-radius:12px;">'
                '<div style="min-width:50px;background:#7c3aed;border-radius:10px;'
                'text-align:center;padding:6px 4px;color:white;flex-shrink:0;">'
                f'<div style="font-size:11px;font-weight:600;">{month}</div>'
                f'<div style="font-size:20px;font-weight:800;line-height:1.1;">{day}</div>'
                '</div>'
                f'<div style="overflow:hidden;">'
                f'<b style="color:#f1f5f9;font-size:13px;">{title}</b><br>'
                f'<span style="color:#6b7280;font-size:12px;">{sub}</span>'
                '</div></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Clear conversation ────────────────────────────────────────────────
        if st.button("&#128465;&#65039; Clear Conversation",
                     use_container_width=True, key="clear_btn"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()