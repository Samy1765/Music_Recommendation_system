import streamlit as st
from ui_utils import apply_custom_css

st.set_page_config(page_title="History | SonicMood", layout="wide", page_icon="⏳")
apply_custom_css()

st.title("⏳ Listening History")
st.markdown("<p style='text-align: center; color: #a0aec0; margin-top: -20px; margin-bottom: 40px;'>Your Sonic Journey</p>", unsafe_allow_html=True)

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("No listening history recorded in this session yet. Go track a song!")
else:
    for item in reversed(st.session_state.history):
        icon = "🎵" if item['type'] == "Song Tracked" else "💿"
        
        st.markdown(f'''
        <div class="track-card">
            <p class="track-title">{icon} {item['title']}</p>
            <p class="track-artist">{item['type']} • {item.get('artist', 'Unknown')} • session</p>
        </div>
        ''', unsafe_allow_html=True)
