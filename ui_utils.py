import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Atmospheric animated background */
    .stApp {
        background: linear-gradient(-45deg, #0d0e15, #1a1c29, #2a1b38, #0d0e15);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e2e8f0;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Primary Button Styling */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #ff007f, #7928ca);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4);
        width: 100%;
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(121, 40, 202, 0.6);
        color: white;
        border: none;
    }

    /* Secondary Button Styling */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05);
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.3);
        color: white;
    }

    /* Glassmorphism containers */
    .mood-box {
        padding: 24px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }

    .mood-box:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .mood-box h3 {
        margin-top: 0;
        background: -webkit-linear-gradient(#f27121, #e94057);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Track Cards */
    .track-card {
        background: rgba(0, 0, 0, 0.2);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #7928ca;
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
    }

    .track-title {
        margin: 0;
        font-size: 1.1em;
        font-weight: 600;
        color: #ffffff;
    }

    .track-artist {
        margin: 4px 0 0 0;
        font-size: 0.9em;
        color: #a0aec0;
    }

    h1 {
        font-weight: 800 !important;
        background: -webkit-linear-gradient(#fff, #a0aec0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* Global Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d0e15 !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """, unsafe_allow_html=True)
