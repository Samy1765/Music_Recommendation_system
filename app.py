import streamlit as st
import time
from tracker import get_now_playing
from mood_detector import get_track_audio_features, interpret_mood_from_features
from recommender import get_recommendations_from_spotify, get_ytmusic_link, play_song_on_platform, play_playlist_on_platform, get_ytmusic_video_id
from ui_utils import apply_custom_css
import plotly.graph_objects as go
import asyncio

st.set_page_config(page_title="Music Recommender and Analyzer | Home", layout="wide", page_icon="🎧")
apply_custom_css()

# Session state configuration
if "current_song" not in st.session_state:
    st.session_state.current_song = None
if "current_features" not in st.session_state:
    st.session_state.current_features = None
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎧 Auto DJ & Tracker")
st.markdown("<p style='text-align: center; color: #a0aec0; margin-top: -20px; margin-bottom: 40px;'>Live Audio Analysis & Contextual Interpolation</p>", unsafe_allow_html=True)

# Layout setup
col_tracker, col_visual = st.columns([1, 1.5], gap="large")

with col_tracker:
    st.markdown("### 🎙️ Now Playing")
    
    if st.button("SYNC AUDIO SOURCE", type="primary", use_container_width=True):
        with st.spinner("Connecting to Windows Media..."):
            song = get_now_playing()
            if song:
                st.session_state.current_song = song
                st.session_state.history.append({"type": "Song Tracked", "title": song['title'], "artist": song['artist']})
                
                with st.spinner("Analyzing spectral features via AI..."):
                    features = get_track_audio_features(song['title'], song['artist'])
                    if features:
                        st.session_state.current_features = features
                    else:
                        st.warning("Could not resolve audio structural features.")
            else:
                st.info("No media currently playing found on the system.")

    if st.session_state.current_song:
        st.markdown(f'''
        <div class="mood-box" style="margin-top: 20px; border-left: 5px solid #00f2fe;">
            <p style="color:#a0aec0; font-size:12px; margin:0;">Active Track</p>
            <h3 style="margin-top:5px; font-size:1.8em; line-height: 1.2;">{st.session_state.current_song['title']}</h3>
            <p style="color:#ffffff; font-size:1.2em; margin:0;">{st.session_state.current_song['artist']}</p>
        </div>
        ''', unsafe_allow_html=True)

    if st.session_state.current_song and st.session_state.current_features:
        if st.button("Generate Contextual Recommendations", type="primary"):
            with st.spinner("Calculating optimal track flow..."):
                st.session_state.recs_col1 = get_recommendations_from_spotify(
                    seed_track_id=st.session_state.current_features['track_id'],
                    limit=5
                )
        
        if "recs_col1" in st.session_state and st.session_state.recs_col1:
            st.markdown("### Recommendation Queue")
            for r in st.session_state.recs_col1:
                st.markdown(f'''
                <div class="track-card">
                    <p class="track-title">{r['title']}</p>
                    <p class="track-artist">{r['artist']}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"Play Track", key=r['spotify_id'], type="secondary"):
                    yt_url = get_ytmusic_link(r['title'], r['artist'])
                    if yt_url:
                        st.session_state.history.append({"type": "Song Played", "title": r['title'], "artist": r['artist']})
                        play_song_on_platform(yt_url)
                        st.success(f"Launching {r['title']}!")
                    else:
                        st.error("Could not find on YT Music.")
            
            st.write("---")
            if st.button("▶️ Play All as YT Music Playlist", type="primary", key="playlist_col1"):
                with st.spinner("Building custom playlist..."):
                    vids = [get_ytmusic_video_id(r['title'], r['artist']) for r in st.session_state.recs_col1]
                    valid_vids = [v for v in vids if v]
                    st.session_state.history.append({"type": "Playlist Generated", "title": "Auto DJ Track Queue", "artist": f"{len(valid_vids)} Tracks"})
                    play_playlist_on_platform(valid_vids)
                    st.success("Custom playlist launched!")


with col_visual:
    st.markdown("### 📡 Spectral Diagnostics")
    
    if st.session_state.current_features:
        f = st.session_state.current_features
        # Create metric cards
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Valence", f"{f.get('valence', 0)*100:.0f}%")
        m2.metric("Energy", f"{f.get('energy', 0)*100:.0f}%")
        m3.metric("Danceable", f"{f.get('danceability', 0)*100:.0f}%")
        m4.metric("Acoustic", f"{f.get('acousticness', 0)*100:.0f}%")
        
        # Plotly Radar Chart
        categories = ['Valence', 'Energy', 'Danceability', 'Acousticness']
        values = [f.get('valence', 0), f.get('energy', 0), f.get('danceability', 0), f.get('acousticness', 0)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(233, 64, 87, 0.4)',
            line=dict(color='#e94057', width=3),
            name='Track DNA'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='rgba(255,255,255,0.1)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='rgba(255,255,255,0.5)')
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='#e2e8f0', size=14)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            showlegend=False,
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        mood = interpret_mood_from_features(f.get('valence', 0.5), f.get('energy', 0.5))
        st.info(f"**Identified Mood Signature**: {mood}")
        
    else:
        st.markdown('''
        <div class="mood-box" style="text-align: center; border-color: rgba(255,255,255,0.05);">
            <p style="color:#718096; margin-top:20px;">Awaiting Audio Sync. Track a song to display spatial audio diagnostics.</p>
        </div>
        ''', unsafe_allow_html=True)
