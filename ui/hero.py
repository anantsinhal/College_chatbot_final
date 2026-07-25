import streamlit as st


def _one_line(html: str) -> str:
    """Collapse multi-line HTML to a single line.

    Streamlit uses a CommonMark parser.  Any line indented ≥4 spaces from
    column-0 is treated as a fenced code block — the HTML gets escaped and
    rendered as plain text even when unsafe_allow_html=True.  A single-line
    string can never trigger that rule, so this helper is the definitive fix.
    """
    return " ".join(html.split())


def render_hero():
    html = _one_line("""
        <div style="
            background:linear-gradient(135deg,#6d28d9,#9333ea,#7c3aed);
            border-radius:24px;
            padding:35px;
            color:white;
            margin-bottom:25px;
            box-shadow:0 15px 45px rgba(124,58,237,.35);
            position:relative;
            overflow:hidden;
        ">

            <div style="display:flex;justify-content:space-between;align-items:center;">

                <div style="
                    background:rgba(255,255,255,.15);
                    backdrop-filter:blur(8px);
                    border:1px solid rgba(255,255,255,.25);
                    border-radius:20px;
                    padding:6px 14px;
                    font-size:13px;
                    font-weight:600;
                    display:inline-block;
                ">
                    &#10024; SMIT AI Assistant
                </div>

                <div style="
                    background:rgba(255,255,255,.2);
                    border-radius:20px;
                    padding:6px 14px;
                    font-size:13px;
                    font-weight:600;
                ">
                    AI Powered
                </div>

            </div>

            <h2 style="font-size:28px;font-weight:800;margin:12px 0 8px;color:white;">
                Your Intelligent Campus Companion
            </h2>

            <p style="color:#ede9fe;font-size:15px;line-height:1.6;margin:0;">
                Get instant answers about admissions, academics,
                placements, scholarships, hostel facilities,
                faculty, campus events and student life.
            </p>

            <div style="display:flex;gap:14px;margin-top:18px;flex-wrap:wrap;">

                <div style="
                    background:rgba(255,255,255,.12);
                    backdrop-filter:blur(12px);
                    border:1px solid rgba(255,255,255,.2);
                    padding:10px 16px;
                    border-radius:12px;
                    font-size:13px;
                    font-weight:500;
                ">&#128218; 100+ Documents</div>

                <div style="
                    background:rgba(255,255,255,.12);
                    backdrop-filter:blur(12px);
                    border:1px solid rgba(255,255,255,.2);
                    padding:10px 16px;
                    border-radius:12px;
                    font-size:13px;
                    font-weight:500;
                ">&#9889; Instant Answers</div>

                <div style="
                    background:rgba(255,255,255,.12);
                    backdrop-filter:blur(12px);
                    border:1px solid rgba(255,255,255,.2);
                    padding:10px 16px;
                    border-radius:12px;
                    font-size:13px;
                    font-weight:500;
                ">&#127891; Campus AI</div>

            </div>

            <div style="
                position:absolute;
                right:30px;
                bottom:20px;
                font-size:80px;
                opacity:.15;
                pointer-events:none;
            ">&#127891;</div>

        </div>
    """)

    st.markdown(html, unsafe_allow_html=True)