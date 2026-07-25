import streamlit as st
from ui.constants import SUGGESTED, ANNOUNCEMENTS, EVENTS


def render_sidebar():
    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;padding:20px 10px;">
                <div style="
                    font-size:52px;
                    margin-bottom:10px;">
                    🎓
                </div>

                <h2 style="margin-bottom:4px;">
                    SMIT AI
                </h2>

                <p style="color:#9CA3AF;font-size:14px;">
                    Campus Assistant
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.subheader("💡 Suggested Questions")

        for q in SUGGESTED:
            if st.button(q, use_container_width=True):
                st.session_state.pending = q

        st.divider()

        st.subheader("📢 Announcements")

        for icon, text, time in ANNOUNCEMENTS:
            st.markdown(
                f"""
                <div style="
                    background:#1f2937;
                    padding:12px;
                    border-radius:12px;
                    margin-bottom:10px;
                ">
                    <b>{icon} {text}</b><br>
                    <span style="color:#9CA3AF;font-size:12px;">
                        {time}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        st.subheader("📅 Upcoming Events")

        for month, day, title, sub in EVENTS:

            st.markdown(
                f"""
                <div style="
                    display:flex;
                    gap:12px;
                    margin-bottom:12px;
                    background:#1f2937;
                    padding:12px;
                    border-radius:12px;
                ">

                    <div style="
                        width:55px;
                        background:#7c3aed;
                        border-radius:12px;
                        text-align:center;
                        padding:6px;
                        color:white;
                    ">
                        <div style="font-size:12px;">{month}</div>
                        <div style="font-size:22px;font-weight:700;">
                            {day}
                        </div>
                    </div>

                    <div>
                        <b>{title}</b><br>
                        <span style="color:#9CA3AF;font-size:12px;">
                            {sub}
                        </span>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        if st.button(
            "🗑 Clear Conversation",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()