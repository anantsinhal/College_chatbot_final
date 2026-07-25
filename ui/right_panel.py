import streamlit as st


def render_right_panel():
    with st.container():
        st.markdown("### 📊 Quick Stats")

        st.metric("Documents", "100+")
        st.metric("Departments", "10")
        st.metric("Response Time", "<2 sec")

        st.markdown("---")

        st.markdown("### 💡 Tips")

        st.info(
            """
Ask questions like:

• Admission Process

• Fee Structure

• Placements

• Hostel

• Scholarships

• Faculty
"""
        )