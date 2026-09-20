import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

st.set_page_config(
    page_title="VTU Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st._config.set_option('theme.base', 'light')
st._config.set_option('theme.backgroundColor', '#F5F1E8')
st._config.set_option('theme.secondaryBackgroundColor', '#D8F3DC')
st._config.set_option('theme.textColor', '#1B1B1B')
st._config.set_option('theme.primaryColor', '#40916C')

if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "user" not in st.session_state:
    st.session_state.user = None
if "subject" not in st.session_state:
    st.session_state.subject = None

def go(page):
    st.session_state.page = page

def render_svg(svg_string, height):
    components.html(svg_string, height=height, scrolling=False)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --green-darkest: #1B4332;
    --green-dark: #2D6A4F;
    --green: #40916C;
    --green-light: #52B788;
    --green-pale: #95D5B2;
    --green-mist: #D8F3DC;
    --beige: #F5F1E8;
    --beige-deep: #E6DFCC;
    --accent: #DDBEA9;
    --text-body: #2C2C2C;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text-body); }
.stApp { background: linear-gradient(180deg, var(--beige) 0%, var(--green-mist) 100%); min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }
h1, h2, h3, h4, h5, h6, p, span, div, label, li { color: var(--text-body); }
h1, h2, h3 { font-family: 'Fraunces', serif !important; color: var(--green-darkest) !important; }

.stTextInput input, .stTextInput textarea, .stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] span {
    background: #FFFFFF !important;
    color: #1B1B1B !important;
    -webkit-text-fill-color: #1B1B1B !important;
    border-radius: 10px !important;
    border: 1.5px solid var(--green-mist) !important;
    font-weight: 500 !important;
}
.stTextInput input::placeholder { color: #9CA3AF !important; -webkit-text-fill-color: #9CA3AF !important; }
div[data-baseweb="popover"] ul li,
div[data-baseweb="popover"] div { color: #1B1B1B !important; background: #FFFFFF !important; }
div[data-baseweb="popover"] ul li:hover { background: var(--green-mist) !important; }
label { color: var(--green-darkest) !important; font-weight: 600 !important; }

.stButton > button {
    background: var(--green-dark);
    color: #FFFFFF !important;
    border: none; border-radius: 999px;
    padding: 0.75rem 2.2rem;
    font-weight: 600; font-size: 1rem;
    transition: all 0.25s ease;
    box-shadow: 0 4px 14px rgba(45,106,79,0.28);
    width: 100%; height: 52px;
}
.stButton > button p, .stButton > button span, .stButton > button div { color: #FFFFFF !important; }
.stButton > button:hover {
    background: var(--green-darkest);
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(45,106,79,0.4);
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--green-dark) !important;
    border: 1.5px solid var(--green-dark) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"] p,
.stButton > button[kind="secondary"] span,
.stButton > button[kind="secondary"] div { color: var(--green-dark) !important; }
.stButton > button[kind="secondary"]:hover { background: var(--green-mist) !important; }

.or-divider {
    text-align: center; color: #4A4A4A;
    font-size: 0.85rem; margin: 0.9rem 0;
    font-style: italic; letter-spacing: 0.1em;
}

.hero-quote {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border-left: 6px solid var(--green);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin: 1.5rem 0 2rem 0;
    font-family: 'Fraunces', serif;
    font-size: 1.25rem; font-style: italic;
    color: var(--green-darkest); line-height: 1.5;
    box-shadow: 0 6px 24px rgba(45,106,79,0.08);
}
.hero-quote-author {
    display: block; margin-top: 0.8rem;
    font-family: 'Inter', sans-serif; font-style: normal;
    font-size: 0.75rem; font-weight: 700;
    color: var(--green); letter-spacing: 0.1em; text-transform: uppercase;
}

.metric-card {
    background: rgba(255,255,255,0.95);
    border-radius: 16px; padding: 1.2rem 1.4rem;
    border: 1px solid var(--green-mist);
    box-shadow: 0 2px 10px rgba(45,106,79,0.06);
}
.metric-card h4 {
    margin: 0; font-size: 0.72rem; color: #4A4A4A;
    text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;
}
.metric-card p {
    margin: 0.4rem 0 0 0; font-family: 'Fraunces', serif;
    font-size: 2rem; font-weight: 700; color: var(--green-darkest);
}

.info-card {
    background: rgba(255,255,255,0.95);
    border-radius: 16px; padding: 1.5rem 1.4rem;
    border: 1px solid var(--green-mist);
    box-shadow: 0 4px 14px rgba(45,106,79,0.07);
    height: 100%; transition: transform 0.2s ease;
}
.info-card:hover { transform: translateY(-4px); }
.info-step {
    display: inline-block; width: 40px; height: 40px;
    border-radius: 50%; background: var(--green-dark); color: #FFFFFF;
    font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.2rem;
    text-align: center; line-height: 40px; margin-bottom: 0.8rem;
}
.info-card h4 {
    font-family: 'Fraunces', serif; margin: 0.3rem 0 0.6rem 0;
    font-size: 1.15rem; color: var(--green-darkest);
}
.info-card p { color: #2C2C2C; font-size: 0.92rem; line-height: 1.55; margin: 0; }

.main-title {
    font-family: 'Fraunces', serif; font-size: 3.5rem; font-weight: 900;
    color: var(--green-darkest); line-height: 1.05; margin: 0;
}
.title-accent { color: var(--green); }
.subtitle { color: #2C2C2C; font-size: 1.1rem; margin-top: 1rem; line-height: 1.6; }

.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; border-bottom: 2px solid var(--green-mist); }
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 10px 10px 0 0;
    color: #4A4A4A; font-weight: 600; padding: 0.8rem 1.3rem; font-size: 0.95rem;
}
.stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span, .stTabs [data-baseweb="tab"] div { color: #4A4A4A !important; }
.stTabs [aria-selected="true"] { background: var(--green-mist); }
.stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span, .stTabs [aria-selected="true"] div {
    color: var(--green-darkest) !important; font-weight: 700 !important;
}

.stCaption, small, .stMarkdown small { color: #4A4A4A !important; }

.cat-header {
    display: flex; align-items: center; gap: 1rem;
    padding: 1.2rem 1.6rem;
    background: rgba(255,255,255,0.85);
    border-radius: 14px; margin-bottom: 1.4rem;
    border: 1px solid var(--green-mist);
}
.cat-header .icon { font-size: 2rem; }
.cat-header h3 {
    margin: 0 !important; font-size: 1.3rem !important;
    font-family: 'Fraunces', serif !important; color: var(--green-darkest) !important;
}
.cat-header p { margin: 0.2rem 0 0 0; color: #2C2C2C; font-size: 0.9rem; }
.cat-header .count {
    margin-left: auto; background: var(--green-mist); color: var(--green-dark);
    padding: 0.5rem 1.1rem; border-radius: 999px;
    font-weight: 700; font-size: 0.85rem; font-family: 'Fraunces', serif;
}
</style>
""", unsafe_allow_html=True)


def student_html():
    return """
    <!DOCTYPE html><html><head><style>
      html, body { margin:0; padding:0; background:transparent; overflow:hidden; }
      @keyframes bobBody { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-2px)} }
      @keyframes bobHead { 0%,100%{transform:translateY(0) rotate(-0.6deg)} 50%{transform:translateY(-3px) rotate(0.6deg)} }
      @keyframes blink { 0%,90%,100%{transform:scaleY(1)} 94%{transform:scaleY(0.05)} }
      @keyframes typeL { 0%,100%{transform:translate(0,0)} 50%{transform:translate(0,-3px)} }
      @keyframes typeR { 0%,100%{transform:translate(0,-3px)} 50%{transform:translate(0,0)} }
      @keyframes screenGlow { 0%,100%{opacity:0.55} 50%{opacity:1} }
      @keyframes coffeeSteam { 0%,100%{opacity:0.3;transform:translateY(0)} 50%{opacity:0.7;transform:translateY(-3px)} }
      @keyframes sparkle { 0%,100%{opacity:0.4;transform:scale(0.9)} 50%{opacity:1;transform:scale(1.2)} }
      @keyframes stressZig { 0%,100%{opacity:0.35;transform:translateX(0)} 50%{opacity:0.9;transform:translateX(3px)} }

      .body     { animation: bobBody 3.6s ease-in-out infinite; transform-box: fill-box; transform-origin: center bottom; }
      .head     { animation: bobHead 3.6s ease-in-out infinite; transform-box: fill-box; transform-origin: center bottom; }
      .eye      { animation: blink 4.2s infinite; transform-box: fill-box; transform-origin: center; }
      .hand-l   { animation: typeL 0.55s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
      .hand-r   { animation: typeR 0.55s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
      .screen-gl { animation: screenGlow 2.6s ease-in-out infinite; }
      .steam    { animation: coffeeSteam 2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
      .spark    { animation: sparkle 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
      .zig      { animation: stressZig 1.1s ease-in-out infinite; }
    </style></head><body>
    <svg viewBox="0 0 380 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
      <defs>
        <radialGradient id="halo" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#D8F3DC" stop-opacity="0.9"/>
          <stop offset="100%" stop-color="#D8F3DC" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="screenFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#FFFFFF"/>
          <stop offset="100%" stop-color="#F5F1E8"/>
        </linearGradient>
        <linearGradient id="deskGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#DDBEA9"/>
          <stop offset="100%" stop-color="#C9A78A"/>
        </linearGradient>
      </defs>

      <circle cx="190" cy="200" r="180" fill="url(#halo)"/>

      <g class="spark"><circle cx="55" cy="80" r="5" fill="#52B788"/></g>
      <g class="spark" style="animation-delay:0.8s"><circle cx="330" cy="110" r="4" fill="#40916C"/></g>
      <g class="spark" style="animation-delay:1.6s"><circle cx="320" cy="290" r="5" fill="#52B788"/></g>
      <g class="spark" style="animation-delay:0.4s"><circle cx="60" cy="300" r="4" fill="#40916C"/></g>

      <g class="zig"><path d="M 145 55 l 6 -8 l -6 -8 l 6 -8" stroke="#DDBEA9" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>
      <g class="zig" style="animation-delay:0.3s"><path d="M 190 45 l 6 -8 l -6 -8 l 6 -8" stroke="#DDBEA9" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>
      <g class="zig" style="animation-delay:0.6s"><path d="M 235 55 l 6 -8 l -6 -8 l 6 -8" stroke="#DDBEA9" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>

      <rect x="20" y="330" width="340" height="14" rx="4" fill="url(#deskGrad)"/>
      <rect x="20" y="344" width="340" height="6" fill="#B08D6E" opacity="0.5"/>

      <g>
        <rect x="42" y="300" width="52" height="10" rx="2" fill="#40916C"/>
        <rect x="46" y="290" width="44" height="10" rx="2" fill="#95D5B2"/>
        <rect x="44" y="280" width="48" height="10" rx="2" fill="#2D6A4F"/>
        <rect x="48" y="272" width="40" height="8" rx="2" fill="#DDBEA9"/>
      </g>

      <g>
        <ellipse cx="310" cy="322" rx="24" ry="6" fill="#E6DFCC"/>
        <path d="M 286 300 L 334 300 L 328 330 Q 310 336 292 330 Z" fill="#FFFFFF" stroke="#DDBEA9" stroke-width="2"/>
        <ellipse cx="310" cy="300" rx="24" ry="6" fill="#F5F1E8" stroke="#DDBEA9" stroke-width="2"/>
        <ellipse cx="310" cy="300" rx="18" ry="4" fill="#8B5E3C" opacity="0.85"/>
        <path d="M 334 305 Q 344 310 334 320" stroke="#DDBEA9" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <g class="steam">
          <path d="M 302 288 Q 298 282 302 276" stroke="#DDBEA9" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.7"/>
          <path d="M 318 288 Q 322 282 318 276" stroke="#DDBEA9" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.7"/>
        </g>
      </g>

      <g transform="translate(115, 235)">
        <rect x="0" y="0" width="150" height="95" rx="7" fill="#1B4332"/>
        <rect x="6" y="6" width="138" height="83" rx="4" fill="url(#screenFill)"/>
        <rect x="6" y="6" width="138" height="83" rx="4" fill="#D8F3DC" class="screen-gl"/>

        <rect x="14" y="14" width="50" height="6" rx="2" fill="#2D6A4F"/>
        <rect x="14" y="24" width="90" height="4" rx="2" fill="#95D5B2"/>

        <circle cx="38" cy="58" r="18" fill="none" stroke="#D8F3DC" stroke-width="5"/>
        <circle cx="38" cy="58" r="18" fill="none" stroke="#40916C" stroke-width="5"
                stroke-dasharray="90 120" transform="rotate(-90 38 58)" stroke-linecap="round"/>
        <text x="38" y="62" text-anchor="middle" font-family="Inter, sans-serif"
              font-weight="800" font-size="9" fill="#1B4332">82%</text>

        <rect x="70" y="46" width="6" height="30" rx="1.5" fill="#52B788"/>
        <rect x="80" y="38" width="6" height="38" rx="1.5" fill="#40916C"/>
        <rect x="90" y="52" width="6" height="24" rx="1.5" fill="#95D5B2"/>
        <rect x="100" y="34" width="6" height="42" rx="1.5" fill="#2D6A4F"/>
        <rect x="110" y="48" width="6" height="28" rx="1.5" fill="#52B788"/>
        <rect x="120" y="42" width="6" height="34" rx="1.5" fill="#40916C"/>
        <rect x="130" y="56" width="6" height="20" rx="1.5" fill="#95D5B2"/>

        <path d="M -8 95 L 158 95 L 166 102 L -16 102 Z" fill="#2D6A4F"/>
        <rect x="-16" y="102" width="182" height="4" rx="2" fill="#1B4332"/>
      </g>

      <g class="body" transform="translate(190, 0)">
        <path d="M -55 300 Q -60 200 0 190 Q 60 200 55 300 Z" fill="#DDBEA9"/>
        <path d="M -25 200 Q 0 215 25 200" stroke="#C9A78A" stroke-width="3" fill="none" stroke-linecap="round"/>

        <path d="M -50 230 Q -80 265 -70 300" stroke="#DDBEA9" stroke-width="18" fill="none" stroke-linecap="round"/>
        <g class="hand-l" style="transform-box: fill-box; transform-origin: center;">
          <circle cx="-70" cy="305" r="11" fill="#F5E6D3"/>
        </g>

        <path d="M 50 230 Q 80 265 70 300" stroke="#DDBEA9" stroke-width="18" fill="none" stroke-linecap="round"/>
        <g class="hand-r" style="transform-box: fill-box; transform-origin: center;">
          <circle cx="70" cy="305" r="11" fill="#F5E6D3"/>
        </g>

        <g class="head" transform="translate(0, 0)">
          <circle cx="0" cy="140" r="48" fill="#F5E6D3"/>

          <circle cx="-38" cy="118" r="20" fill="#3D2B1F"/>
          <circle cx="-22" cy="100" r="22" fill="#3D2B1F"/>
          <circle cx="0" cy="94" r="24" fill="#3D2B1F"/>
          <circle cx="22" cy="100" r="22" fill="#3D2B1F"/>
          <circle cx="38" cy="118" r="20" fill="#3D2B1F"/>
          <circle cx="-42" cy="140" r="16" fill="#3D2B1F"/>
          <circle cx="42" cy="140" r="16" fill="#3D2B1F"/>
          <circle cx="-30" cy="98" r="14" fill="#3D2B1F"/>
          <circle cx="30" cy="98" r="14" fill="#3D2B1F"/>

          <ellipse class="eye" cx="-16" cy="146" rx="3" ry="4" fill="#1B1B1B"/>
          <ellipse class="eye" cx="16" cy="146" rx="3" ry="4" fill="#1B1B1B"/>

          <path d="M -24 136 Q -16 132 -8 136" stroke="#3D2B1F" stroke-width="2" fill="none" stroke-linecap="round"/>
          <path d="M 8 136 Q 16 132 24 136" stroke="#3D2B1F" stroke-width="2" fill="none" stroke-linecap="round"/>

          <path d="M -10 165 Q 0 174 10 165" stroke="#1B1B1B" stroke-width="2.2" fill="none" stroke-linecap="round"/>

          <circle cx="-28" cy="158" r="6" fill="#DDBEA9" opacity="0.7"/>
          <circle cx="28" cy="158" r="6" fill="#DDBEA9" opacity="0.7"/>

          <path d="M -46 180 Q 0 200 46 180" stroke="#2D6A4F" stroke-width="4" fill="none" stroke-linecap="round"/>
          <circle cx="-46" cy="180" r="6" fill="#2D6A4F"/>
          <circle cx="46" cy="180" r="6" fill="#2D6A4F"/>
        </g>
      </g>
    </svg>
    </body></html>
    """


def render_welcome():
    left, right = st.columns([1.4, 1], gap="large")
    with left:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">Welcome to <span class="title-accent">VTU Predictor</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Study smart, not scared. We analyse your previous year papers and show you exactly which questions keep coming back — so you walk into the exam knowing what matters most.</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="hero-quote">
            "The excellent student isn't the one who studies the most —<br>it's the one who studies what matters."
            <span class="hero-quote-author">— Study the patterns, not the panic</span>
        </div>
        """, unsafe_allow_html=True)
        st.button("Get Started →", on_click=go, args=("login",), key="welcome_cta", use_container_width=True)
        st.markdown('<div class="or-divider">— or —</div>', unsafe_allow_html=True)
        if st.button("Explore as guest →", key="welcome_skip", type="secondary", use_container_width=True):
            st.session_state.user = {"name": "Guest", "email": "", "usn": "", "branch": "—", "semester": "—", "year": "—"}
            st.session_state.page = "subject"
            st.rerun()
    with right:
        st.markdown('<br>', unsafe_allow_html=True)
        render_svg(student_html(), height=420)
        st.markdown("""
        <div class="info-card" style="margin-top:0.5rem;">
            <h4>📚 Built for VTU students</h4>
            <p>Every subject. Every previous paper. Ranked by how often each question repeats.</p>
        </div>
        """, unsafe_allow_html=True)


def render_login():
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">Hey, <span class="title-accent">scholar.</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Tell us a bit about yourself — we\'ll personalise your dashboard.</p>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        render_svg(student_html(), height=420)
        st.markdown("""
        <div class="info-card" style="margin-top:0.5rem;">
            <h4>💡 Why sign in?</h4>
            <p>We remember your branch and semester so next time you land straight on your subject. Guests can still explore everything.</p>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<h2>Create your profile</h2>', unsafe_allow_html=True)
        st.markdown("##### 👤 Basic details")
        name = st.text_input("Full name", placeholder="e.g. Aditi Sharma", key="in_name")
        email = st.text_input("College email", placeholder="you@college.edu", key="in_email")
        usn = st.text_input("USN", placeholder="1VT21CS001", key="in_usn")
        st.markdown("##### 🎓 Academic details")
        colA, colB = st.columns(2)
        with colA:
            branch = st.selectbox("Branch", ["CSE", "ISE", "ECE", "EEE", "Mechanical", "Civil", "AI & ML", "Data Science", "Other"], index=0, key="in_branch")
        with colB:
            semester = st.selectbox("Semester", [f"Sem {i}" for i in range(1, 9)], index=3, key="in_sem")
        year = st.selectbox("Academic year", ["1st Year", "2nd Year", "3rd Year", "4th Year"], index=2, key="in_year")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Continue →", key="login_submit", use_container_width=True):
            if name.strip() and usn.strip():
                st.session_state.user = {"name": name.strip(), "email": email.strip(), "usn": usn.strip(), "branch": branch, "semester": semester, "year": year}
                st.session_state.page = "subject"
                st.rerun()
            else:
                st.warning("Please enter at least your name and USN.")
        st.markdown('<div class="or-divider">— or —</div>', unsafe_allow_html=True)
        if st.button("Continue as guest →", key="login_skip", type="secondary", use_container_width=True):
            st.session_state.user = {"name": "Guest", "email": "", "usn": "", "branch": "—", "semester": "—", "year": "—"}
            st.session_state.page = "subject"
            st.rerun()


def render_subject():
    st.markdown('<br>', unsafe_allow_html=True)
    name = st.session_state.user["name"] if st.session_state.user else "there"
    st.markdown(f'<h1 class="main-title">Hi {name.split()[0]}, <span class="title-accent">what are we studying?</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Pick a paper. We\'ll pull in every previous year question we have on it and rank them by how often they repeat.</p>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1], gap="large")
    with col1:
        st.markdown('<h2>Choose paper</h2>', unsafe_allow_html=True)
        subject = st.selectbox("Subject code", ["BCS403 — Design and Analysis of Algorithms"], index=0, key="subject_pick")
        st.caption("More subjects coming soon — we're adding papers every week.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Analyse papers →", key="subject_submit", use_container_width=True):
            st.session_state.subject = subject.split(" — ")[0]
            st.session_state.page = "predictor"
            st.rerun()
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom:1rem;">What you\'ll see next</h3>', unsafe_allow_html=True)
        i1, i2 = st.columns(2)
        with i1:
            st.markdown("""
            <div class="info-card">
                <div class="info-step">1</div>
                <h4>Repetition ranking</h4>
                <p>Every question gets a repeat score. Study the top ones first.</p>
            </div>
            """, unsafe_allow_html=True)
        with i2:
            st.markdown("""
            <div class="info-card">
                <div class="info-step">2</div>
                <h4>Year-wise trends</h4>
                <p>See exactly which years each question appeared in.</p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        render_svg(student_html(), height=420)
        st.markdown("""
        <div class="hero-quote" style="font-size:1rem; padding:1.2rem 1.4rem; margin-top:0.5rem;">
            "Don't read everything. Read what's likely."
            <span class="hero-quote-author">— Every topper, ever</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">How it works</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align:center;">Three steps. No fluff.</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3, gap="large")
    with s1:
        st.markdown("""
        <div class="info-card">
            <div class="info-step">1</div>
            <h4>We read the papers</h4>
            <p>You upload the 4 previous year papers as text. We parse every question, marks, and unit.</p>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="info-card">
            <div class="info-step">2</div>
            <h4>We find the patterns</h4>
            <p>Similar questions across years get grouped using text similarity, and each gets a repetition score.</p>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="info-card">
            <div class="info-step">3</div>
            <h4>You study smart</h4>
            <p>Sort by likelihood, filter by unit, and walk into the exam knowing what's most probable.</p>
        </div>
        """, unsafe_allow_html=True)


def render_question_table(df_subset):
    if df_subset.empty:
        st.info("No questions in this category yet.")
        return

    rows_parts = []
    for rank, (_, row) in enumerate(df_subset.iterrows(), start=1):
        rate = row['repetition_rate']
        marks = row.get('marks')
        score = row.get('weighted_score', rate)
        confidence = row.get('confidence', 'Medium')
        papers = row.get('papers', [])

        if rate >= 75:
            rate_pill = f'<span class="pill pill-high">{rate:.0f}%</span>'
        elif rate >= 50:
            rate_pill = f'<span class="pill pill-mid">{rate:.0f}%</span>'
        else:
            rate_pill = f'<span class="pill pill-low">{rate:.0f}%</span>'

        conf_class = {'High': 'pill-conf-high', 'Medium': 'pill-conf-med', 'Low': 'pill-conf-low'}.get(confidence, 'pill-conf-med')
        conf_pill = f'<span class="pill {conf_class}">{confidence}</span>'
        marks_str = f"{marks}" if marks else "—"
        papers_html = " ".join(f"<code>{p}</code>" for p in papers)
        q_text = row['question']
        if len(q_text) > 200:
            q_text = q_text[:200] + "…"

        rows_parts.append(
            f'<tr>'
            f'<td class="rank">{rank}</td>'
            f'<td class="q-text"><strong>{q_text}</strong></td>'
            f'<td class="center">{rate_pill}</td>'
            f'<td class="center">{marks_str}</td>'
            f'<td class="center">{conf_pill}</td>'
            f'<td class="center"><span class="pill pill-score">{score}</span></td>'
            f'<td class="center"><span class="papers-mini">{papers_html}</span></td>'
            f'</tr>'
        )

    rows_joined = "".join(rows_parts)

    table_html = (
        '<style>'
        '.vtu-table-wrap{overflow-x:auto;border-radius:14px;box-shadow:0 4px 18px rgba(45,106,79,0.08);border:1px solid #D8F3DC;background:#FFFFFF;font-family:Inter,-apple-system,sans-serif;}'
        'table.vtu-table{width:100%;border-collapse:collapse;font-size:0.92rem;}'
        'table.vtu-table thead{background:linear-gradient(180deg,#2D6A4F 0%,#1B4332 100%);}'
        'table.vtu-table th{color:#FFFFFF !important;padding:0.95rem 0.9rem;text-align:left;font-weight:700;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;}'
        'table.vtu-table th.center{text-align:center;}'
        'table.vtu-table tbody tr{border-bottom:1px solid #EDE7D9;transition:background 0.15s ease;}'
        'table.vtu-table tbody tr:nth-child(even){background:#FBF9F4;}'
        'table.vtu-table tbody tr:hover{background:#D8F3DC;}'
        'table.vtu-table tbody tr:last-child{border-bottom:none;}'
        'table.vtu-table td{padding:0.9rem 0.9rem;color:#1B1B1B;vertical-align:middle;line-height:1.45;}'
        'table.vtu-table td.rank{font-family:Georgia,serif;font-weight:800;font-size:1.02rem;color:#1B4332;text-align:center;width:44px;}'
        'table.vtu-table td.q-text{max-width:520px;}'
        'table.vtu-table td.q-text strong{font-weight:500;color:#1B1B1B;}'
        'table.vtu-table td.center{text-align:center;white-space:nowrap;}'
        '.pill{display:inline-block;padding:0.28rem 0.7rem;border-radius:999px;font-size:0.72rem;font-weight:700;white-space:nowrap;}'
        '.pill-high{background:#2D6A4F;color:#FFFFFF;}'
        '.pill-mid{background:#95D5B2;color:#1B4332;}'
        '.pill-low{background:#E6DFCC;color:#4A4A4A;}'
        '.pill-conf-high{background:#D8F3DC;color:#1B4332;}'
        '.pill-conf-med{background:#FEF3C7;color:#92400E;}'
        '.pill-conf-low{background:#FEE2E2;color:#991B1B;}'
        '.pill-score{background:linear-gradient(135deg,#40916C,#2D6A4F);color:#FFFFFF;font-family:Georgia,serif;font-size:0.78rem;padding:0.32rem 0.75rem;}'
        '.papers-mini{font-size:0.76rem;color:#4A4A4A;white-space:nowrap;}'
        '.papers-mini code{background:#D8F3DC;color:#1B4332;padding:0.1rem 0.35rem;border-radius:4px;font-size:0.7rem;margin-right:0.15rem;font-family:Courier New,monospace;}'
        '</style>'
        '<div class="vtu-table-wrap">'
        '<table class="vtu-table">'
        '<thead><tr>'
        '<th class="center">#</th>'
        '<th>Question</th>'
        '<th class="center">Repeat</th>'
        '<th class="center">Marks</th>'
        '<th class="center">Confidence</th>'
        '<th class="center">Score</th>'
        '<th class="center">Papers</th>'
        '</tr></thead>'
        f'<tbody>{rows_joined}</tbody>'
        '</table>'
        '</div>'
    )

    st.markdown(table_html, unsafe_allow_html=True)


def render_category_header(icon, title, subtitle, count):
    st.markdown(f"""
    <div class="cat-header">
        <span class="icon">{icon}</span>
        <div>
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
        <span class="count">{count} questions</span>
    </div>
    """, unsafe_allow_html=True)


def render_predictor():
    col_a, col_b = st.columns([3, 1])
    with col_a:
        name = st.session_state.user["name"].split()[0] if st.session_state.user else "there"
        st.markdown(f'<h2 style="margin-bottom:0;">Hey {name} 👋</h2>', unsafe_allow_html=True)
        st.caption(f"Subject: {st.session_state.subject} • Based on previous year papers")
    with col_b:
        if st.button("← Change paper", key="back", type="secondary", use_container_width=True):
            st.session_state.page = "subject"
            st.rerun()

    st.markdown("---")

    try:
        with open('predictions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("⚠️ predictions.json not found. Run `python app.py` first.")
        st.stop()

    df = pd.DataFrame(data)

    c1, c2, c3, c4 = st.columns(4)
    papers_count = len(df["papers"].iloc[0]) if len(df) else 0
    repeats = df[df['times_appeared'] >= 2]
    top_rate = df['repetition_rate'].max() if len(df) else 0

    with c1:
        st.markdown(f'<div class="metric-card"><h4>Papers analysed</h4><p>{papers_count}</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h4>Unique questions</h4><p>{len(df)}</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><h4>Repeated questions</h4><p>{len(repeats)}</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><h4>Top repeat rate</h4><p>{top_rate:.0f}%</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    sort_cols = ['weighted_score', 'times_appeared'] if 'weighted_score' in df.columns else ['repetition_rate', 'times_appeared']
    mostly = df[df['repetition_rate'] >= 75].sort_values(by=sort_cols, ascending=False)
    moderate = df[(df['repetition_rate'] >= 50) & (df['repetition_rate'] < 75)].sort_values(by=sort_cols, ascending=False)
    low = df[df['repetition_rate'] < 50].sort_values(by=sort_cols, ascending=False)

    tab1, tab2, tab3, tab4 = st.tabs([
        f"🔥 Mostly Predictable ({len(mostly)})",
        f"⚡ Moderately Repeated ({len(moderate)})",
        f"📌 Less Repeated ({len(low)})",
        "📊 Analysis"
    ])

    with tab1:
        render_category_header("🔥", "Mostly Predictable", "Appeared in 3 or 4 of your previous papers — study these first.", len(mostly))
        render_question_table(mostly)

    with tab2:
        render_category_header("⚡", "Moderately Repeated", "Appeared in 2 of your previous papers — worth knowing well.", len(moderate))
        render_question_table(moderate)

    with tab3:
        render_category_header("📌", "Less Repeated", "Appeared in only 1 paper — lower priority but good for depth.", len(low))
        render_question_table(low)

    with tab4:
        st.subheader("Top 15 by repetition rate")
        chart_df = df.sort_values('repetition_rate', ascending=False).head(15).copy()
        chart_df['label'] = chart_df['question'].str[:55] + "..."
        st.bar_chart(chart_df.set_index('label')['repetition_rate'], color="#40916C")

        st.subheader("Year-wise appearance")
        show_df = df[df['times_appeared'] >= 2][['question', 'papers', 'times_appeared', 'repetition_rate']].head(20)
        st.dataframe(show_df, use_container_width=True)


page = st.session_state.page
if page == "welcome":
    render_welcome()
elif page == "login":
    render_login()
elif page == "subject":
    render_subject()
elif page == "predictor":
    render_predictor()